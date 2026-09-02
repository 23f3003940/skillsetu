from database.db import get_connection


def getAdminUser(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM admin
        WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()
    return user


def getInstitution(institution_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM institution
        WHERE id=?
    """, (institution_id,))

    institution = cursor.fetchone()
    conn.close()
    return institution


def getAllInstitutions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM institution
    """)

    institutions = cursor.fetchall()
    conn.close()
    return institutions


def getTotalStudents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(1) FROM student
    """)

    students = cursor.fetchone()
    conn.close()
    return students


def getTotalAcademicians():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(1) FROM academician
    """)

    academicians = cursor.fetchone()
    conn.close()
    return academicians


def getTotalIndustries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(1) FROM industry
    """)

    industries = cursor.fetchone()
    conn.close()
    return industries


def getTotalPostings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(1) FROM posting
    """)

    postings = cursor.fetchone()
    conn.close()
    return postings


def getTotalApplications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(1) FROM application
    """)

    applications = cursor.fetchone()
    conn.close()
    return applications


def getTotalAssessedStudents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(distinct student_id) FROM student_skill
    """)

    students = cursor.fetchone()
    conn.close()
    return students


def getPlacementReadiness():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select s.full_name, s.degree, s.year_of_study, avg(ss.score)
        FROM student s
        inner join student_skill ss ON ss.student_id = s.id
        group by s.id
        order by avg(ss.score) desc
    """)

    readiness = cursor.fetchall()
    conn.close()
    return readiness
