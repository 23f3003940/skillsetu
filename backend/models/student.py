from database.db import get_connection


def getStudent(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student
        WHERE email=? AND password=?
    """, (email, password))

    student = cursor.fetchone()
    conn.close()
    return student


def getStudentByEmail(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student
        WHERE email=?
    """, (email,))

    student = cursor.fetchone()
    conn.close()
    return student


def getStudentById(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student
        WHERE id=?
    """, (student_id,))

    student = cursor.fetchone()
    conn.close()
    return student


def createStudent(full_name, email, password, phone, institution_id, degree, year_of_study):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student
        (full_name, email, password, phone, institution_id, degree, year_of_study, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (full_name, email, password, phone, institution_id, degree, year_of_study, "Active"))

    conn.commit()
    conn.close()


def updateStudentResume(student_id, filepath):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student
        SET filepath=?
        WHERE id=?
    """, (filepath, student_id))

    conn.commit()
    conn.close()


def updateStudentProfile(student_id, full_name, email, password, phone, degree, year_of_study):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student
        SET
            full_name=?,
            email=?,
            password=?,
            phone=?,
            degree=?,
            year_of_study=?
        WHERE id=?
    """, (full_name, email, password, phone, degree, year_of_study, student_id))

    conn.commit()
    conn.close()


def getAllStudents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student
    """)

    students = cursor.fetchall()
    conn.close()
    return students


def searchStudents(search_query):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student
        WHERE full_name LIKE ?
    """, ('%' + search_query + '%',))

    students = cursor.fetchall()
    conn.close()
    return students


def updateStudentStatus(student_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE student
        SET status=?
        WHERE id=?
    """, (status, student_id))

    conn.commit()
    conn.close()


def getCertificationsByStudent(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM certification
        WHERE student_id=?
    """, (student_id,))

    certifications = cursor.fetchall()
    conn.close()
    return certifications
