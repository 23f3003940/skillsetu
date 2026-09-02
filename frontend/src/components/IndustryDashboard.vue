<template>
  <div>
    <div class="alert alert-success" v-if="msg">{{ msg }}</div>
    <div class="alert alert-danger" v-if="err">{{ err }}</div>

    <h2 class="h5 mb-3 text-maroon">Industry Dashboard</h2>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.postings }}</h3>
            <p class="text-muted small mb-0">Total Postings</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.open_postings }}</h3>
            <p class="text-muted small mb-0">Open Postings</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.applications }}</h3>
            <p class="text-muted small mb-0">Applications</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ stats.shortlisted }}</h3>
            <p class="text-muted small mb-0">Shortlisted</p>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-3">
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='postings'}" href="#" @click.prevent="tab='postings'">Postings</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='candidates'}" href="#" @click.prevent="tab='candidates'">Matched Candidates</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='pipeline'}" href="#" @click.prevent="tab='pipeline'">Applicant Pipeline</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='analytics'}" href="#" @click.prevent="tab='analytics'">Analytics</a></li>
    </ul>

    <!-- POSTINGS -->
    <div v-if="tab==='postings'">
      <div class="card shadow-sm border-0 mb-3">
        <div class="card-body">
          <h6 class="mb-3">{{ editingPostingId ? 'Edit Posting' : 'Create New Posting' }}</h6>
          <div class="row g-2">
            <div class="col-md-4"><input class="form-control" placeholder="Title" v-model="postingForm.title"></div>
            <div class="col-md-2">
              <select class="form-select" v-model="postingForm.posting_type">
                <option>Internship</option>
                <option>Job</option>
                <option>Apprenticeship</option>
              </select>
            </div>
            <div class="col-md-3"><input class="form-control" placeholder="Location" v-model="postingForm.location"></div>
            <div class="col-md-3"><input class="form-control" placeholder="Stipend / CTC" v-model="postingForm.stipend"></div>

            <div class="col-md-6"><input class="form-control" placeholder="Required Skills (comma separated)" v-model="postingForm.required_skills"></div>
            <div class="col-md-2"><input class="form-control" type="number" placeholder="Openings" v-model="postingForm.openings"></div>
            <div class="col-md-2">
              <select class="form-select" v-model="postingForm.status">
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
            <div class="col-md-2"><input class="form-control" type="date" v-model="postingForm.last_date"></div>

            <div class="col-md-3"><button class="btn btn-maroon w-100" @click="savePosting">{{ editingPostingId ? 'Update Posting' : 'Create Posting' }}</button></div>
          </div>
          <div class="alert alert-info small mb-0 mt-3">
            Available skills: {{ skillNames }}
          </div>
        </div>
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">My Postings</h6>

          <div v-if="postingList.length===0" class="alert alert-secondary small mb-0">No postings created yet.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Title</th><th>Type</th><th>Location</th><th>Skills</th><th>Openings</th><th>Status</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="p in postingList" :key="p[0]">
                  <td>{{ p[0] }}</td><td>{{ p[1] }}</td><td>{{ p[2] }}</td><td>{{ p[3] }}</td>
                  <td class="small">{{ p[4] }}</td><td>{{ p[6] }}</td>
                  <td><span class="badge" :class="p[7]==='Open' ? 'bg-success' : 'bg-secondary'">{{ p[7] }}</span></td>
                  <td>
                    <button class="btn btn-sm btn-outline-maroon me-1" @click="editPosting(p)">Edit</button>
                    <button class="btn btn-sm btn-outline-secondary me-1" @click="togglePostingStatus(p[0])">{{ p[7]==='Open' ? 'Close' : 'Open' }}</button>
                    <button class="btn btn-sm btn-outline-danger" @click="removePosting(p[0])">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MATCHED CANDIDATES -->
    <div v-if="tab==='candidates'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">Candidates Ranked by Skill Match</h6>
            <select class="form-select" style="max-width:320px" v-model="selectedPostingId" @change="loadCandidates">
              <option value="">Select a posting</option>
              <option v-for="p in postingList" :key="p[0]" :value="p[0]">{{ p[1] }}</option>
            </select>
          </div>

          <div v-if="!selectedPostingId" class="alert alert-secondary small mb-0">Select a posting to see matched candidates.</div>
          <div v-else-if="candidateList.length===0" class="alert alert-secondary small mb-0">No assessed candidates matched this posting yet.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Student</th><th>Degree</th><th>Year</th><th>Match Score</th><th>Matched Skills</th><th>Missing Skills</th><th>Resume</th></tr>
              </thead>
              <tbody>
                <tr v-for="c in candidateList" :key="c[0]">
                  <td>{{ c[0] }}</td><td>{{ c[1] }}</td><td>{{ c[2] }}</td><td>{{ c[3] }}</td>
                  <td style="min-width:130px">
                    <div class="bar-track"><div class="bar-fill" :style="{ width: c[4] + '%' }"></div></div>
                    <span class="small">{{ c[4] }}%</span>
                  </td>
                  <td class="small text-success">{{ c[5] || '-' }}</td>
                  <td class="small text-danger">{{ c[6] || '-' }}</td>
                  <td>
                    <a class="btn btn-sm btn-outline-maroon" v-if="c[7]" :href="resumeLink(c[7])" target="_blank">View</a>
                    <span class="text-muted small" v-else>-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- APPLICANT PIPELINE -->
    <div v-if="tab==='pipeline'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Applicant Pipeline</h6>

          <div v-if="applicantList.length===0" class="alert alert-secondary small mb-0">No applications received yet.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Student</th><th>Degree</th><th>Year</th><th>Posting</th><th>Applied On</th><th>Match</th><th>Resume</th><th>Status</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="a in applicantList" :key="a[0]">
                  <td>{{ a[0] }}</td><td>{{ a[1] }}</td><td>{{ a[2] }}</td><td>{{ a[3] }}</td>
                  <td>{{ a[4] }}</td><td>{{ a[5] }}</td><td>{{ a[7] }}%</td>
                  <td>
                    <a class="btn btn-sm btn-outline-maroon" v-if="a[8]" :href="resumeLink(a[8])" target="_blank">View</a>
                    <span class="text-muted small" v-else>-</span>
                  </td>
                  <td>
                    <span class="badge" :class="a[6]==='Selected' ? 'bg-success' : (a[6]==='Shortlisted' ? 'badge-gold' : (a[6]==='Rejected' || a[6]==='Withdrawn' ? 'bg-danger' : 'bg-secondary'))">{{ a[6] }}</span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-maroon me-1" @click="setStatus(a[0], 'Shortlisted')">Shortlist</button>
                    <button class="btn btn-sm btn-outline-success me-1" @click="setStatus(a[0], 'Selected')">Select</button>
                    <button class="btn btn-sm btn-outline-danger" @click="setStatus(a[0], 'Rejected')">Reject</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ANALYTICS -->
    <div v-if="tab==='analytics'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">Applicant Funnel</h6>

          <div v-if="stats.funnel.length===0" class="alert alert-secondary small mb-0">No application data yet.</div>

          <div v-for="(f, i) in stats.funnel" :key="i" class="mb-2">
            <div class="d-flex justify-content-between small"><span>{{ f[0] }}</span><span>{{ f[1] }}</span></div>
            <div class="bar-track"><div class="bar-fill" :style="{ width: barWidth(f[1]) + '%' }"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiGet, apiSend, resumeUrl } from '../api.js'

export default {
  name: 'IndustryDashboard',
  props: ['user'],
  data() {
    return {
      tab: 'postings',
      postingList: [], applicantList: [], candidateList: [],
      stats: { postings: 0, open_postings: 0, applications: 0, shortlisted: 0, funnel: [] },
      postingForm: { title: '', posting_type: 'Internship', location: '', required_skills: '', stipend: '', openings: '', status: 'Open', last_date: '' },
      editingPostingId: null,
      selectedPostingId: '',
      skillNames: 'Python, Java, C Programming, SQL, Data Analysis, Machine Learning, HTML CSS, JavaScript, Vue JS, Flask, Communication, Teamwork, Problem Solving, Networking Basics, Operating Systems',
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
        this.postingList = await apiGet('/my_postings')
        this.applicantList = await apiGet('/applicants')
        this.stats = await apiGet('/industry_stats')
      } catch (e) { this.showErr(e.message || 'Could not load dashboard') }
    },

    editPosting(p) {
      this.editingPostingId = p[0]
      this.postingForm = {
        title: p[1], posting_type: p[2], location: p[3], required_skills: p[4],
        stipend: p[5], openings: p[6], status: p[7], last_date: p[8]
      }
    },

    async savePosting() {
      try {
        if (this.editingPostingId) await apiSend('/update_posting/' + this.editingPostingId, 'PUT', this.postingForm)
        else await apiSend('/create_posting', 'POST', this.postingForm)
        this.editingPostingId = null
        this.postingForm = { title: '', posting_type: 'Internship', location: '', required_skills: '', stipend: '', openings: '', status: 'Open', last_date: '' }
        this.loadAll()
        this.showMsg('Posting saved')
      } catch (e) { this.showErr(e.message || 'Could not save posting') }
    },

    async togglePostingStatus(id) { await apiGet('/close_posting/' + id); this.loadAll() },

    async removePosting(id) {
      if (!confirm('Delete this posting?')) return
      await apiSend('/delete_posting/' + id, 'DELETE')
      this.loadAll()
    },

    async loadCandidates() {
      if (!this.selectedPostingId) { this.candidateList = []; return }
      try {
        this.candidateList = await apiGet('/matched_candidates/' + this.selectedPostingId)
      } catch (e) { this.showErr(e.message || 'Could not load candidates') }
    },

    async setStatus(id, status) {
      try {
        await apiSend('/update_application/' + id, 'POST', { status: status })
        this.loadAll()
        this.showMsg('Application marked as ' + status)
      } catch (e) { this.showErr(e.message || 'Could not update application') }
    },

    resumeLink(filename) { return resumeUrl(filename) },

    barWidth(value) {
      const max = Math.max(...this.stats.funnel.map(f => f[1]), 1)
      return (value * 100) / max
    }
  }
}
</script>
