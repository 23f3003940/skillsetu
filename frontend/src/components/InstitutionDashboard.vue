<template>
  <div>
    <div class="alert alert-success" v-if="msg">{{ msg }}</div>
    <div class="alert alert-danger" v-if="err">{{ err }}</div>

    <h2 class="h5 mb-3 text-maroon">Institution Admin Dashboard</h2>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.students[0] }}</h3>
            <p class="text-muted small mb-0">Students</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.academicians[0] }}</h3>
            <p class="text-muted small mb-0">Academicians</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.industries[0] }}</h3>
            <p class="text-muted small mb-0">Industries</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.postings[0] }}</h3>
            <p class="text-muted small mb-0">Postings</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.applications[0] }}</h3>
            <p class="text-muted small mb-0">Applications</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-2">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.assessed[0] }}</h3>
            <p class="text-muted small mb-0">Assessed Students</p>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-3">
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='analytics'}" href="#" @click.prevent="tab='analytics'">Analytics</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='students'}" href="#" @click.prevent="tab='students'">Students</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='academicians'}" href="#" @click.prevent="tab='academicians'">Academicians</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='industries'}" href="#" @click.prevent="tab='industries'">Industries</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='applications'}" href="#" @click.prevent="tab='applications'">Applications</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='opportunities'}" href="#" @click.prevent="tab='opportunities'">Opportunities</a></li>
    </ul>

    <!-- ANALYTICS -->
    <div v-if="tab==='analytics'">
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h6 class="mb-3">Skill Gap Distribution (average score by category)</h6>
              <div v-if="analytics.skill_gap.length===0" class="alert alert-secondary small mb-0">No assessment data yet.</div>
              <div v-for="(s, i) in analytics.skill_gap" :key="i" class="mb-2">
                <div class="d-flex justify-content-between small"><span>{{ s[0] }}</span><span>{{ Math.round(s[2]) }}%</span></div>
                <div class="bar-track"><div :class="s[2]>=60 ? 'bar-fill' : 'bar-fill-gold'" :style="{ width: s[2] + '%' }"></div></div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h6 class="mb-3">Application Funnel</h6>
              <div v-if="analytics.funnel.length===0" class="alert alert-secondary small mb-0">No applications yet.</div>
              <div v-for="(f, i) in analytics.funnel" :key="i" class="mb-2">
                <div class="d-flex justify-content-between small"><span>{{ f[0] }}</span><span>{{ f[1] }}</span></div>
                <div class="bar-track"><div class="bar-fill" :style="{ width: barWidth(f[1], analytics.funnel) + '%' }"></div></div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h6 class="mb-3">Skill Demand Trend (from industry postings)</h6>
              <div v-if="analytics.skill_demand.length===0" class="alert alert-secondary small mb-0">No postings yet.</div>
              <div v-for="(d, i) in analytics.skill_demand" :key="i" class="mb-2">
                <div class="d-flex justify-content-between small"><span>{{ d[0] }}</span><span>{{ d[1] }} postings</span></div>
                <div class="bar-track"><div class="bar-fill-gold" :style="{ width: barWidth(d[1], analytics.skill_demand) + '%' }"></div></div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h6 class="mb-3">Placement Readiness</h6>
              <div v-if="analytics.readiness.length===0" class="alert alert-secondary small mb-0">No assessed students yet.</div>
              <div class="table-responsive" v-else>
                <table class="table table-sm align-middle mb-0">
                  <thead class="table-light"><tr><th>Student</th><th>Degree</th><th>Year</th><th>Readiness</th></tr></thead>
                  <tbody>
                    <tr v-for="(r, i) in analytics.readiness" :key="i">
                      <td>{{ r[0] }}</td><td class="small">{{ r[1] }}</td><td>{{ r[2] }}</td>
                      <td><span class="badge" :class="r[3]>=70 ? 'bg-success' : (r[3]>=45 ? 'badge-gold' : 'bg-danger')">{{ Math.round(r[3]) }}%</span></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- STUDENTS -->
    <div v-if="tab==='students'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">Students</h6>
            <input class="form-control" style="max-width:260px" placeholder="Search students..." v-model="studentSearch" @input="searchStudentList">
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Name</th><th>Email</th><th>Degree</th><th>Year</th><th>Resume</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="s in studentList" :key="s[0]">
                  <td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td><td class="small">{{ s[6] }}</td><td>{{ s[7] }}</td>
                  <td>
                    <a class="btn btn-sm btn-outline-maroon" v-if="s[8]" :href="resumeLink(s[8])" target="_blank">View</a>
                    <span class="text-muted small" v-else>-</span>
                  </td>
                  <td><span class="badge" :class="s[9]==='Active' ? 'bg-success' : 'bg-secondary'">{{ s[9] }}</span></td>
                  <td>
                    <button class="btn btn-sm" :class="s[9]==='Active' ? 'btn-outline-danger' : 'btn-outline-success'" @click="toggleStudent(s[0])">{{ s[9]==='Active' ? 'Block' : 'Unblock' }}</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="alert alert-info small mb-0 mt-3">Blocked students cannot login or apply to postings.</div>
        </div>
      </div>
    </div>

    <!-- ACADEMICIANS -->
    <div v-if="tab==='academicians'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">Academicians</h6>
            <input class="form-control" style="max-width:260px" placeholder="Search academicians..." v-model="academicianSearch" @input="searchAcademicianList">
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="a in academicianList" :key="a[0]">
                  <td>{{ a[0] }}</td><td>{{ a[1] }}</td><td>{{ a[2] }}</td><td>{{ a[6] }}</td>
                  <td><span class="badge" :class="a[7]==='Active' ? 'bg-success' : 'bg-secondary'">{{ a[7] }}</span></td>
                  <td>
                    <button class="btn btn-sm" :class="a[7]==='Active' ? 'btn-outline-danger' : 'btn-outline-success'" @click="toggleAcademician(a[0])">{{ a[7]==='Active' ? 'Block' : 'Unblock' }}</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- INDUSTRIES -->
    <div v-if="tab==='industries'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Registered Industries</h6>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Company</th><th>Email</th><th>Sector</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="i in industryList" :key="i[0]">
                  <td>{{ i[0] }}</td><td>{{ i[1] }}</td><td>{{ i[2] }}</td><td>{{ i[5] }}</td>
                  <td><span class="badge" :class="i[6]==='Active' ? 'bg-success' : 'bg-secondary'">{{ i[6] }}</span></td>
                  <td>
                    <button class="btn btn-sm" :class="i[6]==='Active' ? 'btn-outline-danger' : 'btn-outline-success'" @click="toggleIndustry(i[0])">{{ i[6]==='Active' ? 'Block' : 'Unblock' }}</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div v-if="tab==='applications'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">All Applications</h6>
          <div v-if="applicationList.length===0" class="alert alert-secondary small mb-0">No applications yet.</div>
          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Student</th><th>Posting</th><th>Company</th><th>Applied On</th><th>Match</th><th>Resume</th><th>Status</th></tr></thead>
              <tbody>
                <tr v-for="a in applicationList" :key="a[0]">
                  <td>{{ a[0] }}</td><td>{{ a[1] }}</td><td>{{ a[2] }}</td><td>{{ a[3] }}</td><td>{{ a[4] }}</td><td>{{ a[6] }}%</td>
                  <td>
                    <a class="btn btn-sm btn-outline-maroon" v-if="a[7]" :href="resumeLink(a[7])" target="_blank">View</a>
                    <span class="text-muted small" v-else>-</span>
                  </td>
                  <td><span class="badge" :class="a[5]==='Selected' ? 'bg-success' : (a[5]==='Shortlisted' ? 'badge-gold' : 'bg-secondary')">{{ a[5] }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- OPPORTUNITIES -->
    <div v-if="tab==='opportunities'">
      <div class="card shadow-sm border-0 mb-3">
        <div class="card-body">
          <h6 class="mb-3">Publish New Opportunity</h6>
          <div class="row g-2">
            <div class="col-md-4"><input class="form-control" placeholder="Title" v-model="opportunityForm.title"></div>
            <div class="col-md-2">
              <select class="form-select" v-model="opportunityForm.opportunity_type">
                <option>FDP</option><option>Industrial Training</option><option>Research</option>
              </select>
            </div>
            <div class="col-md-3"><input class="form-control" placeholder="Organizer" v-model="opportunityForm.organizer"></div>
            <div class="col-md-2"><input class="form-control" type="date" v-model="opportunityForm.start_date"></div>
            <div class="col-md-1"><input class="form-control" type="number" placeholder="Seats" v-model="opportunityForm.seats"></div>
            <div class="col-md-3"><button class="btn btn-maroon w-100" @click="saveOpportunity">Publish Opportunity</button></div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Opportunities &amp; Registrations</h6>
          <div class="table-responsive mb-4">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Title</th><th>Type</th><th>Organizer</th><th>Start Date</th><th>Seats Left</th><th>Status</th></tr></thead>
              <tbody>
                <tr v-for="o in opportunityList" :key="o[0]">
                  <td>{{ o[0] }}</td><td>{{ o[1] }}</td><td><span class="badge badge-gold">{{ o[2] }}</span></td>
                  <td>{{ o[3] }}</td><td>{{ o[4] }}</td><td>{{ o[5] }}</td>
                  <td><span class="badge" :class="o[6]==='Open' ? 'bg-success' : 'bg-secondary'">{{ o[6] }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <h6 class="mb-3">Academician Registrations</h6>
          <div v-if="registrationList.length===0" class="alert alert-secondary small mb-0">No registrations yet.</div>
          <div class="table-responsive" v-else>
            <table class="table table-sm align-middle mb-0">
              <thead class="table-light"><tr><th>ID</th><th>Academician</th><th>Opportunity</th><th>Type</th><th>Registered On</th><th>Status</th></tr></thead>
              <tbody>
                <tr v-for="r in registrationList" :key="r[0]">
                  <td>{{ r[0] }}</td><td>{{ r[1] }}</td><td>{{ r[2] }}</td><td>{{ r[3] }}</td><td>{{ r[4] }}</td>
                  <td><span class="badge" :class="r[5]==='Registered' ? 'bg-success' : 'bg-danger'">{{ r[5] }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiGet, apiSend, resumeUrl } from '../api.js'

export default {
  name: 'InstitutionDashboard',
  data() {
    return {
      tab: 'analytics',
      studentList: [], academicianList: [], industryList: [],
      applicationList: [], opportunityList: [], registrationList: [],
      stats: { students: [0], academicians: [0], industries: [0], postings: [0], applications: [0], assessed: [0] },
      analytics: { skill_gap: [], funnel: [], skill_demand: [], readiness: [] },
      opportunityForm: { title: '', opportunity_type: 'FDP', organizer: '', start_date: '', seats: '', status: 'Open' },
      studentSearch: '', academicianSearch: '',
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
        this.studentList = await apiGet('/all_students')
        this.academicianList = await apiGet('/all_academicians')
        this.industryList = await apiGet('/all_industries')
        this.applicationList = await apiGet('/all_applications')
        this.opportunityList = await apiGet('/admin_opportunities')
        this.registrationList = await apiGet('/all_registrations')
        this.stats = await apiGet('/admin_stats')
        this.analytics = await apiGet('/admin_analytics')
      } catch (e) { this.showErr(e.message || 'Could not load dashboard') }
    },

    async toggleStudent(id) { await apiGet('/block_student/' + id); this.loadAll() },
    async toggleAcademician(id) { await apiGet('/block_academician/' + id); this.loadAll() },
    async toggleIndustry(id) { await apiGet('/block_industry/' + id); this.loadAll() },

    async searchStudentList() {
      this.studentList = this.studentSearch ? await apiSend('/all_students', 'POST', { search: this.studentSearch }) : await apiGet('/all_students')
    },
    async searchAcademicianList() {
      this.academicianList = this.academicianSearch ? await apiSend('/all_academicians', 'POST', { search: this.academicianSearch }) : await apiGet('/all_academicians')
    },

    async saveOpportunity() {
      try {
        await apiSend('/create_opportunity', 'POST', this.opportunityForm)
        this.opportunityForm = { title: '', opportunity_type: 'FDP', organizer: '', start_date: '', seats: '', status: 'Open' }
        this.loadAll()
        this.showMsg('Opportunity published')
      } catch (e) { this.showErr(e.message || 'Could not publish opportunity') }
    },

    resumeLink(filename) { return resumeUrl(filename) },

    barWidth(value, list) {
      const max = Math.max(...list.map(x => x[1]), 1)
      return (value * 100) / max
    }
  }
}
</script>
