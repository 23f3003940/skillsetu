from database.db import get_connection


def getAllOpportunities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM opportunity
    """)

    opportunities = cursor.fetchall()
    conn.close()
    return opportunities


def getOpportunity(opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM opportunity
        WHERE id=?
    """, (opportunity_id,))

    opportunity = cursor.fetchone()
    conn.close()
    return opportunity


def getOpportunitiesByType(opportunity_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM opportunity
        WHERE opportunity_type=?
    """, (opportunity_type,))

    opportunities = cursor.fetchall()
    conn.close()
    return opportunities


def createOpportunity(title, opportunity_type, organizer, start_date, seats, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO opportunity
        (title, opportunity_type, organizer, start_date, seats, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, opportunity_type, organizer, start_date, seats, status))

    conn.commit()
    conn.close()


def updateOpportunitySeats(opportunity_id, seats):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE opportunity
        SET seats=?
        WHERE id=?
    """, (seats, opportunity_id))

    conn.commit()
    conn.close()


def createOpportunityRegistration(academician_id, opportunity_id, registered_date, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO opportunity_registration
        (academician_id, opportunity_id, registered_date, status)
        VALUES (?, ?, ?, ?)
    """, (academician_id, opportunity_id, registered_date, status))

    conn.commit()
    conn.close()


def getExistingRegistration(academician_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM opportunity_registration
        WHERE academician_id=? and opportunity_id=? and status='Registered'
    """, (academician_id, opportunity_id))

    registrations = cursor.fetchall()
    conn.close()
    return registrations


def getRegistration(registration_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM opportunity_registration
        WHERE id=?
    """, (registration_id,))

    registration = cursor.fetchone()
    conn.close()
    return registration


def getRegistrationsByAcademician(academician_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select r.id, o.title, o.opportunity_type, o.organizer, o.start_date, r.registered_date, r.status
        FROM opportunity_registration r
        inner join opportunity o ON r.opportunity_id = o.id
        where r.academician_id = ?
    """, (academician_id,))

    registrations = cursor.fetchall()
    conn.close()
    return registrations


def getAllRegistrations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        Select r.id, a.full_name, o.title, o.opportunity_type, r.registered_date, r.status
        FROM opportunity_registration r
        inner join academician a ON r.academician_id = a.id
        inner join opportunity o ON r.opportunity_id = o.id
    """)

    registrations = cursor.fetchall()
    conn.close()
    return registrations


def updateRegistrationStatus(registration_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE opportunity_registration
        SET status=?
        WHERE id=?
    """, (status, registration_id))

    conn.commit()
    conn.close()
