<template>
  <div>
    <div class="alert alert-success" v-if="msg">{{ msg }}</div>
    <div class="alert alert-danger" v-if="err">{{ err }}</div>

    <h2 class="h5 mb-3 text-maroon">Academician Dashboard</h2>

    <div class="row g-3 mb-4">
      <div class="col-6 col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ opportunityList.length }}</h3>
            <p class="text-muted small mb-0">Available Opportunities</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ activeCount }}</h3>
            <p class="text-muted small mb-0">My Active Registrations</p>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h3 class="mb-0 text-maroon">{{ registrationList.length }}</h3>
            <p class="text-muted small mb-0">Total Registrations</p>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-3">
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='opportunities'}" href="#" @click.prevent="tab='opportunities'">Opportunities</a></li>
      <li class="nav-item"><a class="nav-link" :class="{active: tab==='registrations'}" href="#" @click.prevent="tab='registrations'">My Registrations</a></li>
    </ul>

    <!-- OPPORTUNITIES -->
    <div v-if="tab==='opportunities'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="mb-0">FDP, Industrial Training &amp; Research Opportunities</h6>
            <select class="form-select" style="max-width:260px" v-model="filterType" @change="loadOpportunities">
              <option value="">All Types</option>
              <option value="FDP">FDP</option>
              <option value="Industrial Training">Industrial Training</option>
              <option value="Research">Research</option>
            </select>
          </div>

          <div v-if="opportunityList.length===0" class="alert alert-secondary small mb-0">No opportunities available.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Title</th><th>Type</th><th>Organizer</th><th>Start Date</th><th>Seats</th><th>Status</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="o in opportunityList" :key="o[0]">
                  <td>{{ o[0] }}</td><td>{{ o[1] }}</td>
                  <td><span class="badge badge-gold">{{ o[2] }}</span></td>
                  <td>{{ o[3] }}</td><td>{{ o[4] }}</td><td>{{ o[5] }}</td>
                  <td><span class="badge" :class="o[6]==='Open' ? 'bg-success' : 'bg-secondary'">{{ o[6] }}</span></td>
                  <td><button class="btn btn-sm btn-maroon" @click="register(o[0])">Register</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MY REGISTRATIONS -->
    <div v-if="tab==='registrations'">
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h6 class="mb-3">My Registrations</h6>

          <div v-if="registrationList.length===0" class="alert alert-secondary small mb-0">You have not registered for any opportunity yet.</div>

          <div class="table-responsive" v-else>
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th>ID</th><th>Title</th><th>Type</th><th>Organizer</th><th>Start Date</th><th>Registered On</th><th>Status</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="r in registrationList" :key="r[0]">
                  <td>{{ r[0] }}</td><td>{{ r[1] }}</td>
                  <td><span class="badge badge-gold">{{ r[2] }}</span></td>
                  <td>{{ r[3] }}</td><td>{{ r[4] }}</td><td>{{ r[5] }}</td>
                  <td><span class="badge" :class="r[6]==='Registered' ? 'bg-success' : 'bg-danger'">{{ r[6] }}</span></td>
                  <td>
                    <button class="btn btn-sm btn-outline-danger" v-if="r[6]==='Registered'" @click="cancel(r[0])">Cancel</button>
                  </td>
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
import { apiGet, apiSend } from '../api.js'

export default {
  name: 'AcademicianDashboard',
  props: ['user'],
  data() {
    return {
      tab: 'opportunities',
      opportunityList: [], registrationList: [],
      filterType: '',
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
        await this.loadOpportunities()
        this.registrationList = await apiGet('/my_registrations')
      } catch (e) { this.showErr(e.message || 'Could not load dashboard') }
    },

    async loadOpportunities() {
      this.opportunityList = this.filterType
        ? await apiGet('/view_opportunities?opportunity_type=' + this.filterType)
        : await apiGet('/view_opportunities')
    },

    async register(id) {
      try {
        const res = await apiSend('/register_opportunity/' + id, 'POST')
        this.loadAll()
        this.showMsg(res.message)
      } catch (e) { this.showErr(e.message || 'Could not register') }
    },

    async cancel(id) {
      if (!confirm('Cancel this registration?')) return
      try {
        await apiSend('/cancel_registration/' + id, 'POST')
        this.loadAll()
        this.showMsg('Registration cancelled')
      } catch (e) { this.showErr(e.message || 'Could not cancel') }
    }
  },
  computed: {
    activeCount() { return this.registrationList.filter(r => r[6] === 'Registered').length }
  }
}
</script>
