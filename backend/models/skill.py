from database.db import get_connection


def getAllSkills():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM skill
    """)

    skills = cursor.fetchall()
    conn.close()
    return skills


def getSkillByName(skill_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM skill
        WHERE skill_name=?
    """, (skill_name,))

    skill = cursor.fetchone()
    conn.close()
    return skill


def getAllQuestions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select q.id, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d, s.skill_name, s.category
        FROM question q
        inner join skill s ON q.skill_id = s.id
        order by s.category
    """)

    questions = cursor.fetchall()
    conn.close()
    return questions


def getQuestionById(question_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM question
        WHERE id=?
    """, (question_id,))

    question = cursor.fetchone()
    conn.close()
    return question


def createStudentSkill(student_id, skill_id, score, level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student_skill
        (student_id, skill_id, score, level)
        VALUES (?, ?, ?, ?)
    """, (student_id, skill_id, score, level))

    conn.commit()
    conn.close()


def deleteStudentSkills(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM student_skill
        WHERE student_id=?
    """, (student_id,))

    conn.commit()
    conn.close()


def getSkillProfileByStudent(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select ss.id, s.skill_name, s.category, ss.score, ss.level
        FROM student_skill ss
        inner join skill s ON ss.skill_id = s.id
        where ss.student_id = ?
        order by ss.score desc
    """, (student_id,))

    profile = cursor.fetchall()
    conn.close()
    return profile


def getSkillNamesByStudent(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select s.skill_name, ss.score
        FROM student_skill ss
        inner join skill s ON ss.skill_id = s.id
        where ss.student_id = ?
    """, (student_id,))

    skills = cursor.fetchall()
    conn.close()
    return skills


def getAverageScoreByStudent(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT avg(score) FROM student_skill
        WHERE student_id=?
    """, (student_id,))

    average = cursor.fetchone()
    conn.close()
    return average


def getAllAverageScores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select student_id, avg(score)
        FROM student_skill
        group by student_id
    """)

    averages = cursor.fetchall()
    conn.close()
    return averages


def getSkillGapDistribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select s.category, count(1), avg(ss.score)
        FROM student_skill ss
        inner join skill s ON ss.skill_id = s.id
        group by s.category
    """)

    distribution = cursor.fetchall()
    conn.close()
    return distribution
