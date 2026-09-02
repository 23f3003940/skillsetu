from database.db import get_connection


def createApplication(student_id, posting_id, applied_date, status, match_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO application
        (student_id, posting_id, applied_date, status, match_score)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, posting_id, applied_date, status, match_score))

    conn.commit()
    conn.close()


def getApplication(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM application
        WHERE id=?
    """, (application_id,))

    application = cursor.fetchone()
    conn.close()
    return application


def getExistingApplication(student_id, posting_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM application
        WHERE student_id=? and posting_id=?
    """, (student_id, posting_id))

    applications = cursor.fetchall()
    conn.close()
    return applications


def getApplicationsByStudent(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select a.id, p.title, i.company_name, p.location, a.applied_date, a.status, a.match_score
        FROM application a
        inner join posting p ON a.posting_id = p.id
        inner join industry i ON p.industry_id = i.id
        where a.student_id = ?
    """, (student_id,))

    applications = cursor.fetchall()
    conn.close()
    return applications


def getApplicationsByIndustry(industry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select a.id, s.full_name, s.degree, s.year_of_study, p.title, a.applied_date, a.status, a.match_score, s.filepath
        FROM application a
        inner join posting p ON a.posting_id = p.id
        inner join student s ON a.student_id = s.id
        where p.industry_id = ?
        order by a.match_score desc
    """, (industry_id,))

    applications = cursor.fetchall()
    conn.close()
    return applications


def getApplicationsByPosting(posting_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select a.id, s.full_name, s.degree, s.year_of_study, a.applied_date, a.status, a.match_score, s.filepath
        FROM application a
        inner join student s ON a.student_id = s.id
        where a.posting_id = ?
        order by a.match_score desc
    """, (posting_id,))

    applications = cursor.fetchall()
    conn.close()
    return applications


def getAllApplications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select a.id, s.full_name, p.title, i.company_name, a.applied_date, a.status, a.match_score, s.filepath
        FROM application a
        inner join posting p ON a.posting_id = p.id
        inner join student s ON a.student_id = s.id
        inner join industry i ON p.industry_id = i.id
    """)

    applications = cursor.fetchall()
    conn.close()
    return applications


def updateApplicationStatus(application_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE application
        SET status=?
        WHERE id=?
    """, (status, application_id))

    conn.commit()
    conn.close()


def getApplicationFunnel():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select status, count(1)
        FROM application
        group by status
    """)

    funnel = cursor.fetchall()
    conn.close()
    return funnel


def getApplicationFunnelByIndustry(industry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select a.status, count(1)
        FROM application a
        inner join posting p ON a.posting_id = p.id
        where p.industry_id = ?
        group by a.status
    """, (industry_id,))

    funnel = cursor.fetchall()
    conn.close()
    return funnel
