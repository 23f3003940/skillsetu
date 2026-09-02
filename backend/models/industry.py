from database.db import get_connection


def getIndustry(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM industry
        WHERE email=? AND password=?
    """, (email, password))

    industry = cursor.fetchone()
    conn.close()
    return industry


def getIndustryByEmail(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM industry
        WHERE email=?
    """, (email,))

    industry = cursor.fetchone()
    conn.close()
    return industry


def getIndustryById(industry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM industry
        WHERE id=?
    """, (industry_id,))

    industry = cursor.fetchone()
    conn.close()
    return industry


def createIndustry(company_name, email, password, phone, sector):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO industry
        (company_name, email, password, phone, sector, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company_name, email, password, phone, sector, "Active"))

    conn.commit()
    conn.close()


def getAllIndustries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM industry
    """)

    industries = cursor.fetchall()
    conn.close()
    return industries


def updateIndustryStatus(industry_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE industry
        SET status=?
        WHERE id=?
    """, (status, industry_id))

    conn.commit()
    conn.close()
