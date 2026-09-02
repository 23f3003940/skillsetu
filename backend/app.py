import os
from flask import Flask, request, jsonify, session, send_from_directory
from config.conf import Config
from datetime import datetime
from flask_cors import CORS
from database.db import init_db
from models.admin import getAdminUser, getInstitution, getAllInstitutions, getTotalStudents, getTotalAcademicians, getTotalIndustries, getTotalPostings, getTotalApplications, getTotalAssessedStudents, getPlacementReadiness
from models.student import getStudent, getStudentByEmail, getStudentById, createStudent, updateStudentProfile, updateStudentResume, getAllStudents, searchStudents, updateStudentStatus, getCertificationsByStudent
from models.industry import getIndustry, getIndustryByEmail, getIndustryById, createIndustry, getAllIndustries, updateIndustryStatus
from models.academician import getAcademician, getAcademicianByEmail, createAcademician, getAllAcademicians, searchAcademicians, updateAcademicianStatus
from models.skill import getAllSkills, getAllQuestions, getQuestionById, createStudentSkill, deleteStudentSkills, getSkillProfileByStudent, getSkillGapDistribution
from models.posting import getAllPostings, getOpenPostings, getPostingsByIndustry, getPosting, createPosting, updatePosting, updatePostingStatus, deletePosting, searchPostings, getPostingsByType, getSkillDemandCount
from models.application import createApplication, getApplication, getExistingApplication, getApplicationsByStudent, getApplicationsByIndustry, getApplicationsByPosting, getAllApplications, updateApplicationStatus, getApplicationFunnel, getApplicationFunnelByIndustry
from models.opportunity import getAllOpportunities, getOpportunity, getOpportunitiesByType, createOpportunity, updateOpportunitySeats, createOpportunityRegistration, getExistingRegistration, getRegistration, getRegistrationsByAcademician, getAllRegistrations, updateRegistrationStatus
from matching import getMatchScore, getMatchedSkills, getRecommendedPostings, getRecommendedRoles, getCareerRoadmap, getPercentile, getStudentNotifications

app = Flask(__name__)
os.makedirs("resumes", exist_ok=True)
app.secret_key = "skillsetusecretkey123"

app.config.from_object(Config)

CORS(
    app,
    supports_credentials=True,
    origins=[
    "http://localhost:5173",
    "https://skillsetu-1-qp6o.onrender.com"
]
)
init_db()

def admin_required():
    return "user" in session and session["user"]["role"] == "admin"


def student_required():
    return "user" in session and session["user"]["role"] == "student"


def industry_required():
    return "user" in session and session["user"]["role"] == "industry"


def academician_required():
    return "user" in session and session["user"]["role"] == "academician"


# INSTITUTION ADMIN LOGIN
@app.route("/", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = getAdminUser(email, password)

    if not user:
        return jsonify({
            "status": "error",
            "message": "Invalid Email or Password"
        }), 401

    session["user"] = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": "admin"
    }

    return jsonify({
        "status": "success",
        "user": session["user"]
    })


@app.route("/dashboard")
def dashboard():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify(session["user"])


# STUDENT REGISTRATION
@app.route("/student_register", methods=["POST"])
def student_register():
    data = request.get_json()

    existing = getStudentByEmail(data.get("email"))

    if existing:
        return jsonify({
            "status": "error",
            "message": "Email Already Registered"
        }), 400

    createStudent(
        data.get("full_name"),
        data.get("email"),
        data.get("password"),
        data.get("phone"),
        1,
        data.get("degree"),
        data.get("year_of_study")
    )

    return jsonify({
        "status": "success"
    })


# STUDENT LOGIN
@app.route("/student_login", methods=["POST"])
def student_login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    student = getStudent(email, password)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Invalid Email or Password"
        }), 401

    if student[9] != "Active":
        return jsonify({
            "status": "error",
            "message": "Student Account Blocked"
        }), 403

    session["user"] = {
        "id": student[0],
        "name": student[1],
        "email": student[2],
        "role": "student"
    }

    return jsonify({
        "status": "success",
        "user": session["user"]
    })


@app.route("/student_dashboard")
def student_dashboard():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify(session["user"])


@app.route("/student_profile")
def student_profile():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    student = getStudentById(session["user"]["id"])
    institution = getInstitution(student[5])

    return jsonify({
        "id": student[0],
        "full_name": student[1],
        "email": student[2],
        "password": student[3],
        "phone": student[4],
        "institution": institution[1] if institution else "",
        "degree": student[6],
        "year_of_study": student[7],
        "filepath": student[8],
        "status": student[9]
    })


@app.route("/update_student_profile", methods=["PUT"])
def update_student_profile():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    updateStudentProfile(
        session["user"]["id"],
        data.get("full_name"),
        data.get("email"),
        data.get("password"),
        data.get("phone"),
        data.get("degree"),
        data.get("year_of_study")
    )

    session["user"]["name"] = data.get("full_name")
    session["user"]["email"] = data.get("email")

    return jsonify({
        "status": "success"
    })


# SKILL ASSESSMENT
@app.route("/assessment_questions")
def assessment_questions():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllQuestions())


@app.route("/submit_assessment", methods=["POST"])
def submit_assessment():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    answers = data.get("answers")

    student_id = session["user"]["id"]

    skillResult = {}

    for question_id in answers:
        question = getQuestionById(int(question_id))

        if not question:
            continue

        skill_id = question[1]

        if skill_id not in skillResult:
            skillResult[skill_id] = [0, 0]

        skillResult[skill_id][1] = skillResult[skill_id][1] + 1

        if answers[question_id] == question[7]:
            skillResult[skill_id][0] = skillResult[skill_id][0] + 1

    deleteStudentSkills(student_id)

    for skill_id in skillResult:
        correct = skillResult[skill_id][0]
        total = skillResult[skill_id][1]

        score = int((correct * 100) / total)

        if score >= 75:
            level = "Strong"
        elif score >= 40:
            level = "Average"
        else:
            level = "Gap"

        createStudentSkill(student_id, skill_id, score, level)

    return jsonify({
        "status": "success",
        "message": "Assessment Submitted Successfully"
    })


@app.route("/skill_profile")
def skill_profile():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    profile = getSkillProfileByStudent(session["user"]["id"])

    return jsonify({
        "profile": profile,
        "roles": getRecommendedRoles(profile),
        "roadmap": getCareerRoadmap(profile),
        "percentile": getPercentile(session["user"]["id"])
    })


# BROWSE AND APPLY
@app.route("/view_postings")
def view_postings():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getRecommendedPostings(session["user"]["id"]))


@app.route("/search_postings")
def search_postings():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    search = request.args.get("search")
    posting_type = request.args.get("posting_type")

    if search:
        return jsonify(searchPostings(search))

    if posting_type:
        return jsonify(getPostingsByType(posting_type))

    return jsonify(getOpenPostings())


@app.route("/apply_posting/<int:posting_id>", methods=["POST"])
def apply_posting(posting_id):
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({
            "status": "error",
            "message": "Posting Not Found"
        }), 404

    if posting[8] != "Open":
        return jsonify({
            "status": "error",
            "message": "Posting is Closed"
        }), 400

    existingApplication = getExistingApplication(session["user"]["id"], posting_id)

    if not existingApplication:
        score = getMatchScore(session["user"]["id"], posting[5])

        createApplication(
            session["user"]["id"],
            posting_id,
            datetime.now().strftime("%Y-%m-%d"),
            "Applied",
            score
        )

        return jsonify({
            "status": "success",
            "message": "Applied Successfully"
        })
    else:
        return jsonify({
            "status": "success",
            "message": "Already Applied for this Posting"
        })


@app.route("/my_applications")
def my_applications():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getApplicationsByStudent(session["user"]["id"]))


@app.route("/withdraw_application/<int:application_id>", methods=["POST"])
def withdraw_application(application_id):
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    existingApplication = getApplication(application_id)

    if not existingApplication:
        return jsonify({
            "status": "error",
            "message": "Application does not exist"
        }), 404

    if existingApplication[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    updateApplicationStatus(application_id, "Withdrawn")

    return jsonify({
        "status": "success",
        "message": "Application Withdrawn"
    })


# DIGITAL PORTFOLIO
@app.route("/portfolio")
def portfolio():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    student_id = session["user"]["id"]

    student = getStudentById(student_id)
    institution = getInstitution(student[5])
    profile = getSkillProfileByStudent(student_id)

    return jsonify({
        "student": {
            "full_name": student[1],
            "email": student[2],
            "phone": student[4],
            "institution": institution[1] if institution else "",
            "degree": student[6],
            "year_of_study": student[7],
            "filepath": student[8]
        },
        "skills": profile,
        "certifications": getCertificationsByStudent(student_id),
        "applications": getApplicationsByStudent(student_id),
        "roadmap": getCareerRoadmap(profile),
        "percentile": getPercentile(student_id)
    })


@app.route("/student_notifications")
def student_notifications():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getStudentNotifications(session["user"]["id"]))


# INDUSTRY REGISTRATION
@app.route("/industry_register", methods=["POST"])
def industry_register():
    data = request.get_json()

    existing = getIndustryByEmail(data.get("email"))

    if existing:
        return jsonify({
            "status": "error",
            "message": "Email Already Registered"
        }), 400

    createIndustry(
        data.get("company_name"),
        data.get("email"),
        data.get("password"),
        data.get("phone"),
        data.get("sector")
    )

    return jsonify({
        "status": "success"
    })


# INDUSTRY LOGIN
@app.route("/industry_login", methods=["POST"])
def industry_login():
    data = request.get_json()

    industry = getIndustry(data.get("email"), data.get("password"))

    if not industry:
        return jsonify({
            "status": "error",
            "message": "Invalid Email or Password"
        }), 401

    if industry[6] != "Active":
        return jsonify({
            "status": "error",
            "message": "Industry Account Blocked"
        }), 403

    session["user"] = {
        "id": industry[0],
        "name": industry[1],
        "email": industry[2],
        "role": "industry"
    }

    return jsonify({
        "status": "success",
        "user": session["user"]
    })


@app.route("/industry_dashboard")
def industry_dashboard():
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify(session["user"])


@app.route("/my_postings")
def my_postings():
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getPostingsByIndustry(session["user"]["id"]))


@app.route("/create_posting", methods=["POST"])
def create_posting():
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    createPosting(
        session["user"]["id"],
        data.get("title"),
        data.get("posting_type"),
        data.get("location"),
        data.get("required_skills"),
        data.get("stipend"),
        data.get("openings"),
        data.get("status"),
        data.get("last_date")
    )

    return jsonify({"status": "success"})


@app.route("/update_posting/<int:posting_id>", methods=["PUT"])
def update_posting(posting_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({"message": "Posting Not Found"}), 404

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    updatePosting(
        posting_id,
        data.get("title"),
        data.get("posting_type"),
        data.get("location"),
        data.get("required_skills"),
        data.get("stipend"),
        data.get("openings"),
        data.get("status"),
        data.get("last_date")
    )

    return jsonify({"status": "success"})


@app.route("/close_posting/<int:posting_id>")
def close_posting(posting_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({"message": "Posting Not Found"}), 404

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    st = "Closed" if posting[8] == "Open" else "Open"

    updatePostingStatus(posting_id, st)

    return jsonify({"status": st})


@app.route("/delete_posting/<int:posting_id>", methods=["DELETE"])
def delete_posting(posting_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({"message": "Posting Not Found"}), 404

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    deletePosting(posting_id)

    return jsonify({"status": "success"})


# MATCHED CANDIDATES FOR A POSTING
@app.route("/matched_candidates/<int:posting_id>")
def matched_candidates(posting_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({"message": "Posting Not Found"}), 404

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    students = getAllStudents()

    candidates = []

    for s in students:
        score = getMatchScore(s[0], posting[5])
        matched, missing = getMatchedSkills(s[0], posting[5])

        if score > 0:
            candidates.append([
                s[0], s[1], s[6], s[7],
                score,
                ", ".join(matched),
                ", ".join(missing),
                s[8]
            ])

    candidates.sort(key=lambda x: x[4], reverse=True)

    return jsonify(candidates)


@app.route("/applicants")
def applicants():
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getApplicationsByIndustry(session["user"]["id"]))


@app.route("/posting_applicants/<int:posting_id>")
def posting_applicants(posting_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    posting = getPosting(posting_id)

    if not posting:
        return jsonify({"message": "Posting Not Found"}), 404

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getApplicationsByPosting(posting_id))


@app.route("/update_application/<int:application_id>", methods=["POST"])
def update_application(application_id):
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    application = getApplication(application_id)

    if not application:
        return jsonify({"message": "Application Not Found"}), 404

    posting = getPosting(application[2])

    if posting[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    updateApplicationStatus(application_id, data.get("status"))

    return jsonify({
        "status": "success",
        "message": "Application Status Updated"
    })


@app.route("/industry_stats")
def industry_stats():
    if not industry_required():
        return jsonify({"message": "Unauthorized"}), 401

    postings = getPostingsByIndustry(session["user"]["id"])
    applications = getApplicationsByIndustry(session["user"]["id"])
    funnel = getApplicationFunnelByIndustry(session["user"]["id"])

    openPostings = len([p for p in postings if p[7] == "Open"])

    return jsonify({
        "postings": len(postings),
        "open_postings": openPostings,
        "applications": len(applications),
        "shortlisted": len([a for a in applications if a[6] == "Shortlisted"]),
        "funnel": funnel
    })


# ACADEMICIAN REGISTRATION
@app.route("/academician_register", methods=["POST"])
def academician_register():
    data = request.get_json()

    existing = getAcademicianByEmail(data.get("email"))

    if existing:
        return jsonify({
            "status": "error",
            "message": "Email Already Registered"
        }), 400

    createAcademician(
        data.get("full_name"),
        data.get("email"),
        data.get("password"),
        data.get("phone"),
        1,
        data.get("department")
    )

    return jsonify({
        "status": "success"
    })


# ACADEMICIAN LOGIN
@app.route("/academician_login", methods=["POST"])
def academician_login():
    data = request.get_json()

    academician = getAcademician(data.get("email"), data.get("password"))

    if not academician:
        return jsonify({
            "status": "error",
            "message": "Invalid Email or Password"
        }), 401

    if academician[7] != "Active":
        return jsonify({
            "status": "error",
            "message": "Academician Account Blocked"
        }), 403

    session["user"] = {
        "id": academician[0],
        "name": academician[1],
        "email": academician[2],
        "role": "academician"
    }

    return jsonify({
        "status": "success",
        "user": session["user"]
    })


@app.route("/academician_dashboard")
def academician_dashboard():
    if not academician_required():
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify(session["user"])


@app.route("/view_opportunities")
def view_opportunities():
    if not academician_required():
        return jsonify({"message": "Unauthorized"}), 401

    opportunity_type = request.args.get("opportunity_type")

    if opportunity_type:
        return jsonify(getOpportunitiesByType(opportunity_type))

    return jsonify(getAllOpportunities())


@app.route("/register_opportunity/<int:opportunity_id>", methods=["POST"])
def register_opportunity(opportunity_id):
    if not academician_required():
        return jsonify({"message": "Unauthorized"}), 401

    opportunity = getOpportunity(opportunity_id)

    if not opportunity:
        return jsonify({
            "status": "error",
            "message": "Opportunity Not Found"
        }), 404

    if opportunity[6] != "Open":
        return jsonify({
            "status": "error",
            "message": "Registration is Closed"
        }), 400

    if opportunity[5] <= 0:
        return jsonify({
            "status": "error",
            "message": "No Seats Available"
        }), 400

    existingRegistration = getExistingRegistration(session["user"]["id"], opportunity_id)

    if not existingRegistration:
        createOpportunityRegistration(
            session["user"]["id"],
            opportunity_id,
            datetime.now().strftime("%Y-%m-%d"),
            "Registered"
        )

        updateOpportunitySeats(opportunity_id, opportunity[5] - 1)

        return jsonify({
            "status": "success",
            "message": "Registered Successfully"
        })
    else:
        return jsonify({
            "status": "success",
            "message": "Already Registered for this Opportunity"
        })


@app.route("/my_registrations")
def my_registrations():
    if not academician_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getRegistrationsByAcademician(session["user"]["id"]))


@app.route("/cancel_registration/<int:registration_id>", methods=["POST"])
def cancel_registration(registration_id):
    if not academician_required():
        return jsonify({"message": "Unauthorized"}), 401

    existingRegistration = getRegistration(registration_id)

    if not existingRegistration:
        return jsonify({
            "status": "error",
            "message": "Registration does not exist"
        }), 404

    if existingRegistration[1] != session["user"]["id"]:
        return jsonify({"message": "Unauthorized"}), 401

    opportunity = getOpportunity(existingRegistration[2])

    updateRegistrationStatus(registration_id, "Cancelled")

    updateOpportunitySeats(opportunity[0], opportunity[5] + 1)

    return jsonify({
        "status": "success",
        "message": "Registration Cancelled"
    })


# INSTITUTION ADMIN
@app.route("/all_students", methods=["GET", "POST"])
def all_students():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    if request.method == "POST":
        data = request.get_json()
        return jsonify(searchStudents(data.get("search", "")))

    return jsonify(getAllStudents())


@app.route("/all_academicians", methods=["GET", "POST"])
def all_academicians():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    if request.method == "POST":
        data = request.get_json()
        return jsonify(searchAcademicians(data.get("search", "")))

    return jsonify(getAllAcademicians())


@app.route("/all_industries")
def all_industries():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllIndustries())


@app.route("/all_postings")
def all_postings():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllPostings())


@app.route("/all_applications")
def all_applications():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllApplications())


@app.route("/all_registrations")
def all_registrations():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllRegistrations())


@app.route("/block_student/<int:student_id>")
def block_student(student_id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    s = getStudentById(student_id)
    st = "Blocked" if s[9] == "Active" else "Active"

    updateStudentStatus(student_id, st)

    return jsonify({"status": st})


@app.route("/block_industry/<int:industry_id>")
def block_industry(industry_id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    i = getIndustryById(industry_id)
    st = "Blocked" if i[6] == "Active" else "Active"

    updateIndustryStatus(industry_id, st)

    return jsonify({"status": st})


@app.route("/block_academician/<int:academician_id>")
def block_academician(academician_id):
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    academicians = getAllAcademicians()

    a = None

    for x in academicians:
        if x[0] == academician_id:
            a = x

    if not a:
        return jsonify({"message": "Academician Not Found"}), 404

    st = "Blocked" if a[7] == "Active" else "Active"

    updateAcademicianStatus(academician_id, st)

    return jsonify({"status": st})


@app.route("/create_opportunity", methods=["POST"])
def create_opportunity():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    createOpportunity(
        data.get("title"),
        data.get("opportunity_type"),
        data.get("organizer"),
        data.get("start_date"),
        data.get("seats"),
        data.get("status")
    )

    return jsonify({"status": "success"})


@app.route("/admin_opportunities")
def admin_opportunities():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify(getAllOpportunities())


@app.route("/admin_stats")
def admin_stats():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    stats = {
        "students": getTotalStudents(),
        "academicians": getTotalAcademicians(),
        "industries": getTotalIndustries(),
        "postings": getTotalPostings(),
        "applications": getTotalApplications(),
        "assessed": getTotalAssessedStudents()
    }

    return jsonify(stats)


@app.route("/admin_analytics")
def admin_analytics():
    if not admin_required():
        return jsonify({"message": "Unauthorized"}), 401

    postings = getSkillDemandCount()

    demand = {}

    for p in postings:
        for skill in p[0].split(","):
            skill = skill.strip()

            if skill == "":
                continue

            if skill not in demand:
                demand[skill] = 0

            demand[skill] = demand[skill] + 1

    demandList = [[k, demand[k]] for k in demand]
    demandList.sort(key=lambda x: x[1], reverse=True)

    return jsonify({
        "skill_gap": getSkillGapDistribution(),
        "funnel": getApplicationFunnel(),
        "skill_demand": demandList[:8],
        "readiness": getPlacementReadiness()
    })


@app.route("/institutions")
def institutions():
    return jsonify(getAllInstitutions())


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if not student_required():
        return jsonify({"message": "Unauthorized"}), 401

    resume = request.files["resume"]

    filename = None

    if resume:
        filename = str(session["user"]["id"]) + "_" + resume.filename
        filepath = os.path.join("resumes", filename)
        resume.save(filepath)

        updateStudentResume(session["user"]["id"], filename)

    return jsonify({
        "status": "success",
        "filepath": filename
    })


@app.route("/view_resume/<string:filename>")
def view_resume(filename):
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    return send_from_directory("resumes", filename)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
