<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card shadow-sm border-0">
        <div class="card-body p-4">
          <h5 class="mb-1 text-maroon">Create Account</h5>
          <p class="text-muted small mb-4">Register on SkillSetu</p>

          <div class="alert alert-danger py-2" v-if="err">{{ err }}</div>
          <div class="alert alert-success py-2" v-if="msg">{{ msg }}</div>

          <label class="form-label small text-muted">Register As</label>
          <select class="form-select mb-3" v-model="role">
            <option value="student">Student</option>
            <option value="industry">Industry</option>
            <option value="academician">Academician</option>
          </select>

          <div v-if="role==='industry'">
            <label class="form-label small text-muted">Company Name</label>
            <input class="form-control mb-2" placeholder="Company Name" v-model="form.company_name">
          </div>

          <div v-else>
            <label class="form-label small text-muted">Full Name</label>
            <input class="form-control mb-2" placeholder="Full Name" v-model="form.full_name">
          </div>

          <label class="form-label small text-muted">Email address</label>
          <input class="form-control mb-2" placeholder="Email address" v-model="form.email">

          <label class="form-label small text-muted">Password</label>
          <input class="form-control mb-2" type="password" placeholder="Password" v-model="form.password">

          <label class="form-label small text-muted">Contact Number</label>
          <input class="form-control mb-2" placeholder="Contact Number" v-model="form.phone">

          <div v-if="role==='student'" class="row g-2">
            <div class="col-md-7">
              <label class="form-label small text-muted">Degree</label>
              <input class="form-control mb-2" placeholder="B.Tech Computer Engineering" v-model="form.degree">
            </div>
            <div class="col-md-5">
              <label class="form-label small text-muted">Year of Study</label>
              <select class="form-select mb-2" v-model="form.year_of_study">
                <option>1st Year</option><option>2nd Year</option>
                <option>3rd Year</option><option>4th Year</option>
              </select>
            </div>
          </div>

          <div v-if="role==='industry'">
            <label class="form-label small text-muted">Sector</label>
            <input class="form-control mb-2" placeholder="Information Technology" v-model="form.sector">
          </div>

          <div v-if="role==='academician'">
            <label class="form-label small text-muted">Department</label>
            <input class="form-control mb-2" placeholder="Computer Engineering" v-model="form.department">
          </div>

          <button class="btn btn-maroon w-100 mt-2" @click="register">Register</button>

          <p class="text-center mt-3 mb-2">
            Already have an account? <a href="#" class="text-maroon" @click.prevent="$emit('go-login')">Login here</a>
          </p>

          <div class="alert alert-info small mb-0 mt-3">
            Note: Institution Admin accounts are created by the institution, not through registration.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiSend } from '../api.js'

export default {
  name: 'RegisterPage',
  emits: ['go-login'],
  data() {
    return {
      role: 'student',
      form: { full_name: '', company_name: '', email: '', password: '', phone: '', degree: '', year_of_study: '1st Year', sector: '', department: '' },
      err: '', msg: ''
    }
  },
  methods: {
    async register() {
      this.err = ''
      const url = this.role === 'industry' ? '/industry_register'
                : this.role === 'academician' ? '/academician_register'
                : '/student_register'
      try {
        await apiSend(url, 'POST', this.form)
        this.msg = 'Registered successfully. Please login.'
        setTimeout(() => this.$emit('go-login'), 1200)
      } catch (e) {
        this.err = e.message || 'Registration failed'
      }
    }
  }
}
</script>
