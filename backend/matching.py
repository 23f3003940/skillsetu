from models.skill import getSkillNamesByStudent, getAverageScoreByStudent, getAllAverageScores
from models.posting import getOpenPostings
from models.student import getStudentById, getCertificationsByStudent
from models.application import getApplicationsByStudent


# WEIGHTED SKILL OVERLAP MATCHING
# score = (sum of student score for matched skills) / (100 * number of required skills)
def getMatchScore(student_id, required_skills):
    studentSkills = getSkillNamesByStudent(student_id)

    skillMap = {}

    for s in studentSkills:
        skillMap[s[0].strip().lower()] = s[1]

    required = [r.strip().lower() for r in required_skills.split(",") if r.strip()]

    if len(required) == 0:
        return 0

    total = 0

    for r in required:
        if r in skillMap:
            total = total + skillMap[r]

    score = (total * 100) / (100 * len(required))

    return int(score)


def getMatchedSkills(student_id, required_skills):
    studentSkills = getSkillNamesByStudent(student_id)

    skillMap = {}

    for s in studentSkills:
        skillMap[s[0].strip().lower()] = s[1]

    required = [r.strip() for r in required_skills.split(",") if r.strip()]

    matched = []
    missing = []

    for r in required:
        if r.lower() in skillMap and skillMap[r.lower()] >= 40:
            matched.append(r)
        else:
            missing.append(r)

    return matched, missing


def getRecommendedPostings(student_id):
    postings = getOpenPostings()

    recommended = []

    for p in postings:
        score = getMatchScore(student_id, p[4])
        matched, missing = getMatchedSkills(student_id, p[4])

        recommended.append([
            p[0], p[1], p[2], p[3], p[4], p[5], p[6],
            p[7], p[8], p[9],
            score,
            ", ".join(matched),
            ", ".join(missing)
        ])

    recommended.sort(key=lambda x: x[10], reverse=True)

    return recommended


# RULE BASED ROLE RECOMMENDATION
ROLE_MAP = {
    "Programming": ["Software Developer", "Backend Engineer", "Application Developer"],
    "Data": ["Data Analyst", "Business Analyst", "Machine Learning Engineer"],
    "Web Development": ["Frontend Developer", "Full Stack Developer", "UI Engineer"],
    "Soft Skills": ["Business Development Associate", "Project Coordinator", "Technical Support Lead"],
    "Core Engineering": ["Network Engineer", "System Administrator", "DevOps Trainee"]
}


def getRecommendedRoles(profile):
    categoryScore = {}

    for p in profile:
        category = p[2]

        if category not in categoryScore:
            categoryScore[category] = []

        categoryScore[category].append(p[3])

    averages = []

    for category in categoryScore:
        scores = categoryScore[category]
        averages.append([category, int(sum(scores) / len(scores))])

    averages.sort(key=lambda x: x[1], reverse=True)

    roles = []

    for a in averages[:2]:
        for role in ROLE_MAP.get(a[0], []):
            roles.append({
                "role": role,
                "category": a[0],
                "readiness": a[1]
            })

    return roles


# CAREER ROADMAP LADDER
def getCareerRoadmap(profile):
    if len(profile) == 0:
        return []

    average = int(sum([p[3] for p in profile]) / len(profile))

    weak = [p[1] for p in profile if p[3] < 50]

    if average >= 75:
        level = "Advanced"
    elif average >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    roadmap = [
        {
            "stage": "Stage 1",
            "title": "Foundation",
            "detail": "Core programming and problem solving fundamentals",
            "done": average >= 40
        },
        {
            "stage": "Stage 2",
            "title": "Skill Building",
            "detail": "Close the gap in " + (", ".join(weak[:3]) if weak else "your weaker skill areas"),
            "done": average >= 55
        },
        {
            "stage": "Stage 3",
            "title": "Project and Certification",
            "detail": "Build 2 real projects and add verified certifications",
            "done": average >= 70
        },
        {
            "stage": "Stage 4",
            "title": "Internship Ready",
            "detail": "Apply to matched internships through SkillSetu",
            "done": average >= 80
        },
        {
            "stage": "Stage 5",
            "title": "Placement Ready",
            "detail": "Target full time roles with a complete verified portfolio",
            "done": average >= 90
        }
    ]

    return {
        "current_level": level,
        "average_score": average,
        "stages": roadmap
    }


# PEER BENCHMARKING PERCENTILE
def getPercentile(student_id):
    average = getAverageScoreByStudent(student_id)

    if not average or average[0] is None:
        return 0

    myScore = average[0]

    allScores = getAllAverageScores()

    if len(allScores) <= 1:
        return 100

    below = 0

    for a in allScores:
        if a[1] < myScore:
            below = below + 1

    return int((below * 100) / len(allScores))


# IN APP NOTIFICATIONS COMPUTED ON PAGE LOAD
def getStudentNotifications(student_id):
    notifications = []

    student = getStudentById(student_id)
    profile = getSkillNamesByStudent(student_id)
    applications = getApplicationsByStudent(student_id)
    certifications = getCertificationsByStudent(student_id)

    if len(profile) == 0:
        notifications.append({
            "type": "warning",
            "message": "Your skill profile is empty. Take the skill assessment to unlock matching."
        })

    if not student[4]:
        notifications.append({
            "type": "warning",
            "message": "Your profile is incomplete. Add your contact number."
        })

    if len(certifications) == 0:
        notifications.append({
            "type": "info",
            "message": "No certifications added yet. Certifications improve your portfolio."
        })

    if len(profile) > 0:
        recommended = getRecommendedPostings(student_id)

        for r in recommended[:3]:
            if r[10] >= 60:
                notifications.append({
                    "type": "success",
                    "message": "New match found: " + r[1] + " at " + r[9] + " (" + str(r[10]) + "% match)"
                })

    for a in applications:
        if a[5] == "Shortlisted":
            notifications.append({
                "type": "success",
                "message": "You have been shortlisted for " + a[1] + " at " + a[2]
            })

        if a[5] == "Selected":
            notifications.append({
                "type": "success",
                "message": "Congratulations! You are selected for " + a[1] + " at " + a[2]
            })

        if a[5] == "Rejected":
            notifications.append({
                "type": "danger",
                "message": "Your application for " + a[1] + " was not taken forward."
            })

    return notifications
