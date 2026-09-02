from database.db import get_connection


def getAcademician(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM academician
        WHERE email=? AND password=?
    """, (email, password))

    academician = cursor.fetchone()
    conn.close()
    return academician


def getAcademicianByEmail(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM academician
        WHERE email=?
    """, (email,))

    academician = cursor.fetchone()
    conn.close()
    return academician


def createAcademician(full_name, email, password, phone, institution_id, department):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO academician
        (full_name, email, password, phone, institution_id, department, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name, email, password, phone, institution_id, department, "Active"))

    conn.commit()
    conn.close()


def getAllAcademicians():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM academician
    """)

    academicians = cursor.fetchall()
    conn.close()
    return academicians


def searchAcademicians(search_query):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM academician
        WHERE full_name LIKE ?
    """, ('%' + search_query + '%',))

    academicians = cursor.fetchall()
    conn.close()
    return academicians


def updateAcademicianStatus(academician_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE academician
        SET status=?
        WHERE id=?
    """, (status, academician_id))

    conn.commit()
    conn.close()
