import sqlite3
DATABASE = "database.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ADMIN (INSTITUTION ADMIN)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            institution_id INTEGER
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO admin(id, name, email, password, institution_id)
        VALUES
        (1, 'Institution Administrator', 'admin@skillsetu.in', 'admin', 1)
    """)

    # INSTITUTION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS institution(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT,
            state TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO institution(id, name, city, state)
        VALUES
        (1, 'Government Engineering College, Gandhinagar', 'Gandhinagar', 'Gujarat')
    """)

    # STUDENT
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            institution_id INTEGER,
            degree TEXT,
            year_of_study TEXT,
            filepath TEXT,
            status TEXT DEFAULT 'Active',

            FOREIGN KEY (institution_id)
                REFERENCES institution(id)
        )
    """)

    # INDUSTRY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS industry(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            sector TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    # ACADEMICIAN
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academician(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            institution_id INTEGER,
            department TEXT,
            status TEXT DEFAULT 'Active',

            FOREIGN KEY (institution_id)
                REFERENCES institution(id)
        )
    """)

    # SKILL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # ASSESSMENT QUESTION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,

            FOREIGN KEY (skill_id)
                REFERENCES skill(id)
        )
    """)

    # STUDENT SKILL PROFILE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_skill(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            level TEXT NOT NULL,

            FOREIGN KEY (student_id)
                REFERENCES student(id),

            FOREIGN KEY (skill_id)
                REFERENCES skill(id)
        )
    """)

    # POSTING
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posting(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            posting_type TEXT NOT NULL,
            location TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            stipend TEXT,
            openings INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_date DATE,

            FOREIGN KEY (industry_id)
                REFERENCES industry(id)
        )
    """)

    # APPLICATION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS application(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            posting_id INTEGER NOT NULL,
            applied_date DATE NOT NULL,
            status TEXT NOT NULL,
            match_score INTEGER,

            FOREIGN KEY (student_id)
                REFERENCES student(id),

            FOREIGN KEY (posting_id)
                REFERENCES posting(id)
        )
    """)

    # OPPORTUNITY (FDP / INDUSTRIAL TRAINING / RESEARCH)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunity(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            opportunity_type TEXT NOT NULL,
            organizer TEXT NOT NULL,
            start_date DATE,
            seats INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # OPPORTUNITY REGISTRATION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunity_registration(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            academician_id INTEGER NOT NULL,
            opportunity_id INTEGER NOT NULL,
            registered_date DATE NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (academician_id)
                REFERENCES academician(id),

            FOREIGN KEY (opportunity_id)
                REFERENCES opportunity(id)
        )
    """)

    # CERTIFICATION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certification(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            issuer TEXT NOT NULL,
            issue_date DATE,

            FOREIGN KEY (student_id)
                REFERENCES student(id)
        )
    """)

    conn.commit()
    conn.close()

    seed_db()


def seed_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT count(1) FROM skill")

    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    skills = [
        (1, 'Python', 'Programming'),
        (2, 'Java', 'Programming'),
        (3, 'C Programming', 'Programming'),
        (4, 'SQL', 'Data'),
        (5, 'Data Analysis', 'Data'),
        (6, 'Machine Learning', 'Data'),
        (7, 'HTML CSS', 'Web Development'),
        (8, 'JavaScript', 'Web Development'),
        (9, 'Vue JS', 'Web Development'),
        (10, 'Flask', 'Web Development'),
        (11, 'Communication', 'Soft Skills'),
        (12, 'Teamwork', 'Soft Skills'),
        (13, 'Problem Solving', 'Soft Skills'),
        (14, 'Networking Basics', 'Core Engineering'),
        (15, 'Operating Systems', 'Core Engineering')
    ]

    cursor.executemany("""
        INSERT INTO skill(id, skill_name, category)
        VALUES (?, ?, ?)
    """, skills)

    questions = [
        (1, 'Which keyword is used to define a function in Python?', 'func', 'def', 'function', 'define', 'b'),
        (1, 'What does len() return for the list [10, 20, 30]?', '2', '3', '30', 'None', 'b'),
        (2, 'Which keyword is used to inherit a class in Java?', 'extends', 'inherits', 'implement', 'super', 'a'),
        (3, 'Which symbol is used to declare a pointer in C?', '&', '#', '*', '@', 'c'),
        (4, 'Which SQL clause is used to filter rows?', 'ORDER BY', 'GROUP BY', 'WHERE', 'HAVING', 'c'),
        (4, 'Which SQL keyword removes duplicate rows from a result?', 'UNIQUE', 'DISTINCT', 'FILTER', 'ONLY', 'b'),
        (5, 'Which measure is most affected by outliers?', 'Median', 'Mode', 'Mean', 'Range', 'c'),
        (6, 'Which of these is a supervised learning task?', 'Clustering', 'Classification', 'Dimensionality Reduction', 'Association', 'b'),
        (7, 'Which HTML tag is used to create a hyperlink?', '<link>', '<href>', '<a>', '<url>', 'c'),
        (8, 'Which keyword declares a block scoped variable in JavaScript?', 'var', 'let', 'define', 'static', 'b'),
        (9, 'Which Vue directive is used for two way binding on inputs?', 'v-bind', 'v-model', 'v-for', 'v-if', 'b'),
        (10, 'Which decorator maps a URL to a function in Flask?', '@app.url', '@app.map', '@app.route', '@app.path', 'c'),
        (11, 'What is the most important part of good communication?', 'Speaking fast', 'Using difficult words', 'Listening clearly', 'Talking more', 'c'),
        (12, 'In a team, a task is delayed. What is the best first step?', 'Blame someone', 'Inform the team early', 'Hide the delay', 'Do nothing', 'b'),
        (13, 'What should you do first when solving a new problem?', 'Start coding', 'Understand the requirement', 'Ask for a deadline', 'Copy a solution', 'b'),
        (14, 'Which device connects two different networks?', 'Switch', 'Hub', 'Router', 'Repeater', 'c'),
        (15, 'Which scheduling algorithm can cause starvation?', 'Round Robin', 'Priority Scheduling', 'FCFS', 'None', 'b')
    ]

    cursor.executemany("""
        INSERT INTO question
        (skill_id, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, questions)

    students = [
        ('Rohan Mehta', 'rohan@skillsetu.in', 'student', '9876500011', 1, 'B.Tech Computer Engineering', '3rd Year', None, 'Active'),
        ('Priya Sharma', 'priya@skillsetu.in', 'student', '9876500012', 1, 'B.Tech Information Technology', '4th Year', None, 'Active'),
        ('Aman Patel', 'aman@skillsetu.in', 'student', '9876500013', 1, 'B.Tech Electronics', '3rd Year', None, 'Active'),
        ('Sneha Desai', 'sneha@skillsetu.in', 'student', '9876500014', 1, 'B.Tech Computer Engineering', '2nd Year', None, 'Active')
    ]

    cursor.executemany("""
        INSERT INTO student
        (full_name, email, password, phone, institution_id, degree, year_of_study, filepath, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, students)

    industries = [
        ('Infosys Limited', 'infosys@skillsetu.in', 'industry', '9876500021', 'Information Technology', 'Active'),
        ('Adani Digital Labs', 'adani@skillsetu.in', 'industry', '9876500022', 'Technology Services', 'Active')
    ]

    cursor.executemany("""
        INSERT INTO industry
        (company_name, email, password, phone, sector, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, industries)

    academicians = [
        ('Dr. Kavita Joshi', 'kavita@skillsetu.in', 'academician', '9876500031', 1, 'Computer Engineering', 'Active'),
        ('Prof. Anil Kumar', 'anil@skillsetu.in', 'academician', '9876500032', 1, 'Electronics', 'Active')
    ]

    cursor.executemany("""
        INSERT INTO academician
        (full_name, email, password, phone, institution_id, department, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, academicians)

    postings = [
        (1, 'Backend Developer Intern', 'Internship', 'Ahmedabad', 'Python,Flask,SQL', '25000 / month', 5, 'Open', '2026-10-15'),
        (1, 'Data Analyst Trainee', 'Job', 'Pune', 'SQL,Data Analysis,Python', '6.5 LPA', 3, 'Open', '2026-10-20'),
        (2, 'Frontend Developer Intern', 'Internship', 'Gandhinagar', 'HTML CSS,JavaScript,Vue JS', '20000 / month', 4, 'Open', '2026-10-18'),
        (2, 'Machine Learning Intern', 'Internship', 'Bengaluru', 'Python,Machine Learning,Data Analysis', '30000 / month', 2, 'Open', '2026-11-01')
    ]

    cursor.executemany("""
        INSERT INTO posting
        (industry_id, title, posting_type, location, required_skills, stipend, openings, status, last_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, postings)

    opportunities = [
        ('Faculty Development Programme on AI in Education', 'FDP', 'AICTE ATAL Academy', '2026-09-20', 40, 'Open'),
        ('Industrial Training on Cloud Infrastructure', 'Industrial Training', 'Adani Digital Labs', '2026-10-05', 25, 'Open'),
        ('Research Collaboration in Applied Data Science', 'Research', 'IIT Gandhinagar', '2026-10-12', 15, 'Open'),
        ('FDP on Outcome Based Education', 'FDP', 'NITTTR Bhopal', '2026-11-02', 50, 'Open')
    ]

    cursor.executemany("""
        INSERT INTO opportunity
        (title, opportunity_type, organizer, start_date, seats, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, opportunities)

    certifications = [
        (1, 'Python for Everybody', 'Coursera', '2026-02-10'),
        (1, 'SQL Basics', 'HackerRank', '2026-04-22'),
        (2, 'Data Analysis with Python', 'NPTEL', '2026-03-15'),
        (3, 'Web Development Bootcamp', 'Udemy', '2026-05-08')
    ]

    cursor.executemany("""
        INSERT INTO certification
        (student_id, title, issuer, issue_date)
        VALUES (?, ?, ?, ?)
    """, certifications)

    conn.commit()
    conn.close()
