<template>
  <div>
    <div class="alert alert-success" v-if="msg">{{ msg }}</div>
    <div class="alert alert-danger" v-if="err">{{ err }}</div>

    <h2 class="h5 mb-3 text-maroon">Student Dashboard</h2>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ profile.length }}</h3>
            <p class="text-muted small mb-0">Skills Assessed</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ strongCount }}</h3>
            <p class="text-muted small mb-0">Strong Skills</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ gapCount }}</h3>
            <p class="text-muted small mb-0">Skill Gaps</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ applicationList.length }}</h3>
            <p class="text-muted small mb-0">Applications</p>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-3">
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='notifications'}" href="#" @click.prevent="tab='notifications'">Notifications</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='assessment'}" href="#" @click.prevent="tab='assessment'">Skill Assessment</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='profile'}" href="#" @click.prevent="tab='profile'">Skill Profile</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='postings'}" href="#" @click.prevent="tab='postings'">Opportunities</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='applications'}" href="#" @click.prevent="tab='applications'">My Applications</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='portfolio'}" href="#" @click.prevent="tab='portfolio'">Portfolio</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='account'}" href="#" @click.prevent="tab='account'">My Account</a></li>
    </ul>

    <!-- NOTIFICATIONS -->
    <div v-if="tab==='notifications'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Notifications</h6>
          <div v-if="notificationList.length===0" class="alert alert-secondary small mb-0">
            No notifications right now.
          </div>
          <div v-for="(n, i) in notificationList" :key="i" class="alert py-2 mb-2" :class="'alert-' + n.type">
            {{ n.message }}
          </div>
        </div>
      </div>
    </div>

    <!-- SKILL ASSESSMENT -->
    <div v-if="tab==='assessment'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">Skill Assessment</h6>
            <span class="badge badge-gold">{{ answeredCount }} / {{ questionList.length }} answered</span>
          </div>

          <div v-if="questionList.length===0" class="alert alert-secondary small">Loading questions...</div>

          <div v-for="q in questionList" :key="q[0]" class="mb-3 pb-3 border-bottom">
            <p class="mb-1">
              <span class="badge badge-gold me-2">{{ q[7] }}</span>
              <span class="text-muted small">{{ q[6] }}</span>
            </p>
            <p class="mb-2">{{ q[1] }}</p>
            <div class="row g-2">
              <div class="col-md-6" v-for="(opt, idx) in ['a','b','c','d']" :key="opt">
                <button class="btn btn-sm w-100 text-start"
                        :class="answers[q[0]]===opt ? 'btn-maroon' : 'btn-outline-maroon'"
                        @click="answers[q[0]]=opt">
                  {{ opt.toUpperCase() }}. {{ q[2 + idx] }}
                </button>
              </div>
            </div>
          </div>

          <button class="btn btn-maroon" @click="submitAssessment" v-if="questionList.length>0">Submit Assessment</button>
          <div class="alert alert-info small mb-0 mt-3">
            Your answers generate a real skill profile with strengths and gaps. You can retake it any time.
          </div>
        </div>
      </div>
    </div>

    <!-- SKILL PROFILE -->
    <div v-if="tab==='profile'">
      <div v-if="profile.length===0" class="alert alert-warning">
        No skill profile yet. Take the Skill Assessment first.
      </div>

      <div v-else>
        <div class="row g-3">
          <div class="col-md-7">
            <div class="card shadow-sm border-0 h-100">
              <div class="card-body">
                <h6 class="mb-3">Skill Strength &amp; Gap Breakdown</h6>
                <div v-for="p in profile" :key="p[0]" class="mb-2">
                  <div class="d-flex justify-content-between small">
                    <span>{{ p[1] }} <span class="text-muted">({{ p[2] }})</span></span>
                    <span>
                      {{ p[3] }}%
                      <span class="badge ms-1" :class="p[4]==='Strong' ? 'bg-success' : (p[4]==='Average' ? 'badge-gold' : 'bg-danger')">{{ p[4] }}</span>
                    </span>
                  </div>
                  <div class="bar-track">
                    <div :class="p[3]>=75 ? 'bar-fill' : 'bar-fill-gold'" :style="{ width: p[3] + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-5">
            <div class="card shadow-sm border-0 mb-3">
              <div class="card-body">
                <h6 class="mb-2">Peer Benchmarking</h6>
                <h3 class="text-maroon mb-0">{{ percentile }}th percentile</h3>
                <p class="text-muted small mb-0">Compared to assessed students in your institution</p>
              </div>
            </div>

            <div class="card shadow-sm border-0">
              <div class="card-body">
                <h6 class="mb-3">Recommended Roles</h6>
                <div v-for="(r, i) in roles" :key="i" class="d-flex justify-content-between border-bottom py-2">
                  <span>{{ r.role }}<br><span class="text-muted small">{{ r.category }}</span></span>
                  <span class="badge badge-gold align-self-center">{{ r.readiness }}% ready</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-3">
          <div class="card-body">
            <h6 class="mb-1">Career Roadmap</h6>
            <p class="text-muted small mb-3">Current Level: <b>{{ roadmap.current_level }}</b> &middot; Average Score: {{ roadmap.average_score }}%</p>
            <div v-for="(s, i) in roadmap.stages" :key="i" class="roadmap-step" :class="{done: s.done}">
              <span class="roadmap-dot" :class="{done: s.done}"></span>
              <b>{{ s.stage }} &mdash; {{ s.title }}</b>
              <span class="badge ms-2" :class="s.done ? 'bg-success' : 'bg-secondary'">{{ s.done ? 'Reached' : 'Pending' }}</span>
              <p class="text-muted small mb-0 mt-1">{{ s.detail }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- OPPORTUNITIES -->
    <div v-if="tab==='postings'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">Internships &amp; Jobs (ranked by your match score)</h6>
            <input class="form-control" style="max-width:260px" placeholder="Search postings..." v-model="postingSearch" @input="searchPostingList">
          </div>

          <div v-if="postingList.length===0" class="alert alert-secondary small mb-0">No postings available.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>Title</th><th>Company</th><th>Type</th><th>Location</th><th>Match</th><th>Matched Skills</th><th>Missing</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="p in postingList" :key="p[0]">
                  <td>{{ p[1] }}</td>
                  <td>{{ p[9] }}</td>
                  <td>{{ p[2] }}</td>
                  <td>{{ p[3] }}</td>
                  <td style="min-width:120px">
                    <div class="bar-track"><div class="bar-fill" :style="{ width: (p[10] || 0) + '%' }"></div></div>
                    <span class="small">{{ p[10] || 0 }}%</span>
                  </td>
                  <td class="small text-success">{{ p[11] || '-' }}</td>
                  <td class="small text-danger">{{ p[12] || '-' }}</td>
                  <td><button class="btn btn-sm btn-maroon" @click="applyPosting(p[0])">Apply</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MY APPLICATIONS -->
    <div v-if="tab==='applications'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Application Tracker</h6>

          <div v-if="applicationList.length===0" class="alert alert-secondary small mb-0">You have not applied anywhere yet.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Posting</th><th>Company</th><th>Location</th><th>Applied On</th><th>Match</th><th>Status</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="a in applicationList" :key="a[0]">
                  <td>{{ a[0] }}</td><td>{{ a[1] }}</td><td>{{ a[2] }}</td><td>{{ a[3] }}</td><td>{{ a[4] }}</td>
                  <td>{{ a[6] }}%</td>
                  <td>
                    <span class="badge" :class="a[5]==='Selected' ? 'bg-success' : (a[5]==='Shortlisted' ? 'badge-gold' : (a[5]==='Rejected' || a[5]==='Withdrawn' ? 'bg-danger' : 'bg-secondary'))">{{ a[5] }}</span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-danger" v-if="a[5]==='Applied'" @click="withdraw(a[0])">Withdraw</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- PORTFOLIO -->
    <div v-if="tab==='portfolio'">
      <div v-if="!portfolio.student" class="alert alert-secondary small">Loading portfolio...</div>

      <div v-else>
        <div class="card shadow-sm border-0 mb-3">
          <div class="card-body">
            <h5 class="mb-1 text-maroon">{{ portfolio.student.full_name }}</h5>
            <p class="text-muted small mb-1">{{ portfolio.student.degree }} &middot; {{ portfolio.student.year_of_study }}</p>
            <p class="text-muted small mb-0">{{ portfolio.student.institution }} &middot; {{ portfolio.student.email }} &middot; {{ portfolio.student.phone }}</p>
            <span class="badge badge-gold mt-2">Peer Percentile: {{ portfolio.percentile }}</span>
            <a class="btn btn-sm btn-outline-maroon ms-2 mt-2" v-if="portfolio.student.filepath" :href="resumeLink(portfolio.student.filepath)" target="_blank">View Resume</a>
          </div>
        </div>

        <div class="row g-3">
          <div class="col-md-6">
            <div class="card shadow-sm border-0 h-100">
              <div class="card-body">
                <h6 class="mb-3">Verified Skills</h6>
                <div v-if="portfolio.skills.length===0" class="alert alert-secondary small mb-0">No skills yet.</div>
                <span v-for="s in portfolio.skills" :key="s[0]" class="badge me-1 mb-1" :class="s[4]==='Strong' ? 'bg-success' : (s[4]==='Average' ? 'badge-gold' : 'bg-secondary')">
                  {{ s[1] }} &middot; {{ s[3] }}%
                </span>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="card shadow-sm border-0 h-100">
              <div class="card-body">
                <h6 class="mb-3">Certifications</h6>
                <div v-if="portfolio.certifications.length===0" class="alert alert-secondary small mb-0">No certifications added.</div>
                <div v-for="c in portfolio.certifications" :key="c[0]" class="border-bottom py-2">
                  <b>{{ c[2] }}</b>
                  <p class="text-muted small mb-0">{{ c[3] }} &middot; {{ c[4] }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0 mt-3">
          <div class="card-body">
            <h6 class="mb-3">Application History</h6>
            <div v-if="portfolio.applications.length===0" class="alert alert-secondary small mb-0">No applications yet.</div>
            <div class="table-responsive" v-else>
              <table class="table table-sm align-middle mb-0">
                <thead class="table-light"><tr><th>Posting</th><th>Company</th><th>Applied On</th><th>Status</th></tr></thead>
                <tbody>
                  <tr v-for="a in portfolio.applications" :key="a[0]">
                    <td>{{ a[1] }}</td><td>{{ a[2] }}</td><td>{{ a[4] }}</td><td>{{ a[5] }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MY ACCOUNT -->
    <div v-if="tab==='account'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Update Profile</h6>
          <div class="row g-2">
            <div class="col-md-4"><input class="form-control" placeholder="Full Name" v-model="accountForm.full_name"></div>
            <div class="col-md-4"><input class="form-control" placeholder="Email address" v-model="accountForm.email"></div>
            <div class="col-md-4"><input class="form-control" placeholder="Password" v-model="accountForm.password"></div>
            <div class="col-md-4"><input class="form-control" placeholder="Contact Number" v-model="accountForm.phone"></div>
            <div class="col-md-4"><input class="form-control" placeholder="Degree" v-model="accountForm.degree"></div>
            <div class="col-md-4">
              <select class="form-select" v-model="accountForm.year_of_study">
                <option>1st Year</option><option>2nd Year</option>
                <option>3rd Year</option><option>4th Year</option>
              </select>
            </div>
            <div class="col-md-3"><button class="btn btn-maroon w-100" @click="saveProfile">Update Profile</button></div>
          </div>

          <hr class="my-4">

          <h6 class="mb-3">Resume</h6>
          <div class="row g-2 align-items-center">
            <div class="col-md-5">
              <input class="form-control" type="file" @change="onResumeSelected">
            </div>
            <div class="col-md-3">
              <button class="btn btn-maroon w-100" @click="uploadResume">Upload Resume</button>
            </div>
            <div class="col-md-4">
              <a class="btn btn-outline-maroon w-100" v-if="accountForm.filepath" :href="resumeLink(accountForm.filepath)" target="_blank">View Current Resume</a>
              <span class="text-muted small" v-else>No resume uploaded yet</span>
            </div>
          </div>
          <div class="alert alert-info small mb-0 mt-3">
            Your resume is visible to industries whose postings you apply to, and to your institution admin.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiGet, apiSend, apiUpload, resumeUrl } from '../api.js'

export default {
  name: 'StudentDashboard',
  props: ['user'],
  emits: ['profile-updated'],
  data() {
    return {
      tab: 'notifications',
      questionList: [], answers: {},
      profile: [], roles: [], roadmap: { stages: [] }, percentile: 0,
      postingList: [], applicationList: [], notificationList: [],
      portfolio: {},
      accountForm: { full_name: '', email: '', password: '', phone: '', degree: '', year_of_study: '1st Year', filepath: '' },
      resumeFile: null,
      postingSearch: '',
      msg: '', err: ''
    }
  },
  mounted() {
    this.loadAll()
  },
  methods: {
    showMsg(m) { this.msg = m; this.err = ''; setTimeout(() => this.msg = '', 3000) },
    showErr(m) { this.err = m; this.msg = ''; setTimeout(() => this.err = '', 3000) },

    async loadAll() {
      try {
        this.questionList = await apiGet('/assessment_questions')
        const res = await apiGet('/skill_profile')
        this.profile = res.profile
        this.roles = res.roles
        this.roadmap = res.roadmap && res.roadmap.stages ? res.roadmap : { stages: [], current_level: '-', average_score: 0 }
        this.percentile = res.percentile
        this.postingList = await apiGet('/view_postings')
        this.applicationList = await apiGet('/my_applications')
        this.notificationList = await apiGet('/student_notifications')
        this.portfolio = await apiGet('/portfolio')

        const p = await apiGet('/student_profile')
        this.accountForm = {
          full_name: p.full_name, email: p.email, password: p.password,
          phone: p.phone, degree: p.degree, year_of_study: p.year_of_study,
          filepath: p.filepath
        }
      } catch (e) { this.showErr(e.message || 'Could not load dashboard') }
    },

    resumeLink(filename) { return resumeUrl(filename) },

    onResumeSelected(e) { this.resumeFile = e.target.files[0] },

    async uploadResume() {
      if (!this.resumeFile) { this.showErr('Please choose a file first'); return }
      try {
        const formData = new FormData()
        formData.append('resume', this.resumeFile)
        await apiUpload('/upload_resume', formData)
        this.loadAll()
        this.showMsg('Resume uploaded successfully')
      } catch (e) { this.showErr(e.message || 'Could not upload resume') }
    },

    async submitAssessment() {
      try {
        await apiSend('/submit_assessment', 'POST', { answers: this.answers })
        this.loadAll()
        this.tab = 'profile'
        this.showMsg('Assessment submitted. Your skill profile is ready.')
      } catch (e) { this.showErr(e.message || 'Could not submit assessment') }
    },

    async applyPosting(id) {
      try {
        const res = await apiSend('/apply_posting/' + id, 'POST')
        this.loadAll()
        this.showMsg(res.message)
      } catch (e) { this.showErr(e.message || 'Could not apply') }
    },

    async withdraw(id) {
      if (!confirm('Withdraw this application?')) return
      try {
        await apiSend('/withdraw_application/' + id, 'POST')
        this.loadAll()
        this.showMsg('Application withdrawn')
      } catch (e) { this.showErr(e.message || 'Could not withdraw') }
    },

    async searchPostingList() {
      this.postingList = this.postingSearch
        ? await apiGet('/search_postings?search=' + this.postingSearch)
        : await apiGet('/view_postings')
    },

    async saveProfile() {
      try {
        await apiSend('/update_student_profile', 'PUT', this.accountForm)
        this.$emit('profile-updated', { name: this.accountForm.full_name, email: this.accountForm.email })
        this.loadAll()
        this.showMsg('Profile updated')
      } catch (e) { this.showErr(e.message || 'Could not update profile') }
    }
  },
  computed: {
    answeredCount() { return Object.keys(this.answers).length },
    strongCount() { return this.profile.filter(p => p[4] === 'Strong').length },
    gapCount() { return this.profile.filter(p => p[4] === 'Gap').length }
  }
}
</script>
