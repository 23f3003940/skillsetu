from database.db import get_connection


def getAllPostings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select p.id, p.title, p.posting_type, p.location, p.required_skills, p.stipend, p.openings, p.status, p.last_date, i.company_name
        FROM posting p
        inner join industry i ON p.industry_id = i.id
    """)

    postings = cursor.fetchall()
    conn.close()
    return postings


def getOpenPostings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select p.id, p.title, p.posting_type, p.location, p.required_skills, p.stipend, p.openings, p.status, p.last_date, i.company_name
        FROM posting p
        inner join industry i ON p.industry_id = i.id
        where p.status = 'Open'
    """, )

    postings = cursor.fetchall()
    conn.close()
    return postings


def getPostingsByIndustry(industry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select p.id, p.title, p.posting_type, p.location, p.required_skills, p.stipend, p.openings, p.status, p.last_date, i.company_name
        FROM posting p
        inner join industry i ON p.industry_id = i.id
        where p.industry_id = ?
    """, (industry_id,))

    postings = cursor.fetchall()
    conn.close()
    return postings


def getPosting(posting_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM posting
        WHERE id=?
    """, (posting_id,))

    posting = cursor.fetchone()
    conn.close()
    return posting


def createPosting(industry_id, title, posting_type, location, required_skills, stipend, openings, status, last_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posting
        (industry_id, title, posting_type, location, required_skills, stipend, openings, status, last_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (industry_id, title, posting_type, location, required_skills, stipend, openings, status, last_date))

    conn.commit()
    conn.close()


def updatePosting(posting_id, title, posting_type, location, required_skills, stipend, openings, status, last_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posting
        SET
            title=?,
            posting_type=?,
            location=?,
            required_skills=?,
            stipend=?,
            openings=?,
            status=?,
            last_date=?
        WHERE id=?
    """, (title, posting_type, location, required_skills, stipend, openings, status, last_date, posting_id))

    conn.commit()
    conn.close()


def updatePostingStatus(posting_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posting
        SET status=?
        WHERE id=?
    """, (status, posting_id))

    conn.commit()
    conn.close()


def deletePosting(posting_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM posting
        WHERE id=?
    """, (posting_id,))

    conn.commit()
    conn.close()


def searchPostings(search_query):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select p.id, p.title, p.posting_type, p.location, p.required_skills, p.stipend, p.openings, p.status, p.last_date, i.company_name
        FROM posting p
        inner join industry i ON p.industry_id = i.id
        where p.title LIKE ? and p.status = 'Open'
    """, ('%' + search_query + '%',))

    postings = cursor.fetchall()
    conn.close()
    return postings


def getPostingsByType(posting_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select p.id, p.title, p.posting_type, p.location, p.required_skills, p.stipend, p.openings, p.status, p.last_date, i.company_name
        FROM posting p
        inner join industry i ON p.industry_id = i.id
        where p.posting_type = ? and p.status = 'Open'
    """, (posting_type,))

    postings = cursor.fetchall()
    conn.close()
    return postings


def getSkillDemandCount():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT required_skills FROM posting
    """)

    postings = cursor.fetchall()
    conn.close()
    return postings
