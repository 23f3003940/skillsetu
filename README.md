# SkillSetu — Setu se Sapno Tak

SIH26044 · Team Vintage Coders · IIT Madras BS Degree Programme

A skill-development and placement bridge platform connecting Students, Industry, Academicians
and Institutions. Built as a full working prototype covering Day 1 and Day 2 of the sprint plan.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Flask (single `app.py`, session auth) |
| Database | SQLite via raw `sqlite3` |
| Frontend | Vue 3 (Options API) + Vite |
| Styling | Bootstrap 5 (CDN) + custom SkillSetu theme |
| Charts | Pure CSS bar visuals (no external chart library) |
| API | JSON over `fetch` with `credentials: include` |

No Celery, no Redis, no SQLAlchemy, no vue-router, no external chart library.

---

## Folder Structure

```
skillsetu/
├── backend/
│   ├── app.py                 # all routes for all 4 roles
│   ├── matching.py            # skill matching, roadmap, notifications
│   ├── requirements.txt
│   ├── resumes/               # uploaded resumes (auto-created)
│   ├── config/
│   │   ├── __init__.py
│   │   └── conf.py
│   ├── database/
│   │   └── db.py              # schema + seed data
│   └── models/
│       ├── admin.py
│       ├── student.py
│       ├── industry.py
│       ├── academician.py
│       ├── skill.py
│       ├── posting.py
│       ├── application.py
│       └── opportunity.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── api.js
        ├── style.css
        ├── App.vue
        └── components/
            ├── LoginPage.vue
            ├── RegisterPage.vue
            ├── StudentDashboard.vue
            ├── IndustryDashboard.vue
            ├── AcademicianDashboard.vue
            └── InstitutionDashboard.vue
```

---

## How to Run

### Backend (port 5000)

```
cd backend
pip install -r requirements.txt
python app.py
```

The database file `database.db` is created and seeded automatically on first run.
To reset all data, delete `database.db` and start the server again.

### Frontend (port 5173)

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Demo Logins

| Role | Email | Password |
|---|---|---|
| Student | rohan@skillsetu.in | student |
| Student | priya@skillsetu.in | student |
| Industry | infosys@skillsetu.in | industry |
| Industry | adani@skillsetu.in | industry |
| Academician | kavita@skillsetu.in | academician |
| Institution Admin | admin@skillsetu.in | admin |

---

## Features Implemented

### Student
- Register, login, update profile
- Skill assessment (17 questions across 5 skill categories)
- Skill profile with strength / average / gap breakdown and CSS bar visuals
- Rule-based recommended roles
- 5-stage career roadmap visual
- Peer benchmarking percentile
- Browse postings ranked by live match score, with matched and missing skills
- Apply, track status, withdraw — duplicate applications blocked
- Upload resume from My Account (stored in `backend/resumes/`, path saved in `student.filepath`)
- Digital portfolio: skills, certifications, application history, resume link
- In-app notifications computed on page load

### Industry
- Register, login
- Create, edit, open/close, delete postings with required skills
- Matched candidates per posting, ranked by weighted skill overlap
- Applicant pipeline: Applied → Shortlisted → Selected / Rejected
- View resume of every applicant and matched candidate
- Applicant funnel analytics

### Academician
- Register, login
- Browse FDP / Industrial Training / Research opportunities, filter by type
- Register and cancel — seats update live, duplicate registration blocked

### Institution Admin
- Six live count cards from real database queries
- Skill gap distribution by category
- Application funnel
- Skill demand trend derived from industry postings
- Placement readiness table
- Manage students, academicians, industries (block / unblock, search)
- View resume of any student, from the Students and Applications tabs
- Publish new opportunities and view all registrations

---

## Matching Logic

Weighted skill overlap, in plain Python (`matching.py`):

```
score = (sum of student score for each required skill) / (100 × number of required skills) × 100
```

A skill counts as *matched* when the student's assessed score for it is 40 or above.
Everything else is reported as a *missing* skill so the student sees an actionable gap.

---

## Scope Cuts (planned for the full build)

| Full Feature | Prototype Substitute |
|---|---|
| PostgreSQL | SQLite |
| Redis + Celery scheduled jobs | In-app notification list computed on page load |
| pgvector similarity matching | Weighted skill-overlap scoring |
| Regional language support | English-only UI |
| Cloudflare R2 document storage | Local `resumes/` folder via `send_from_directory` |
| Full document verification workflow | Role-scoped resume visibility |
