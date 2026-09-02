<template>
  <div class="row justify-content-center">
    <div class="col-md-9">
      <div class="card shadow-sm border-0">
        <div class="row g-0">

          <div class="col-md-5 border-end p-4">
            <h5 class="mb-1 text-maroon">
              <span class="brand-logo me-2">&#9650;</span> SkillSetu
            </h5>
            <p class="text-muted small mb-4">Setu se Sapno Tak</p>

            <label class="form-label text-uppercase small text-muted">Roles</label>
            <div class="list-group">
              <a href="#" class="list-group-item list-group-item-action" :class="{active: role==='student'}" @click.prevent="role='student'">
                Student
              </a>
              <a href="#" class="list-group-item list-group-item-action" :class="{active: role==='industry'}" @click.prevent="role='industry'">
                Industry
              </a>
              <a href="#" class="list-group-item list-group-item-action" :class="{active: role==='academician'}" @click.prevent="role='academician'">
                Academician
              </a>
              <a href="#" class="list-group-item list-group-item-action" :class="{active: role==='admin'}" @click.prevent="role='admin'">
                Institution Admin
              </a>
            </div>
          </div>

          <div class="col-md-7 p-4">
            <h5 class="mb-1">Welcome Back!</h5>
            <p class="text-muted small mb-3">Login to your account</p>

            <div class="alert alert-danger py-2" v-if="err">{{ err }}</div>

            <label class="form-label small text-muted">Email address</label>
            <input class="form-control mb-2" placeholder="Email address" v-model="form.email">

            <label class="form-label small text-muted">Password</label>
            <input class="form-control mb-2" type="password" placeholder="Password" v-model="form.password">

            <button class="btn btn-maroon w-100" @click="login">Login</button>

            <p class="text-center mt-3 mb-2" v-if="role!=='admin'">
              Don't have an account?
              <a href="#" class="text-maroon" @click.prevent="$emit('go-register')">Register here</a>
            </p>

            <div class="alert alert-info small mb-0 mt-3">
              Demo Logins &mdash;
              Student: rohan@skillsetu.in / student |
              Industry: infosys@skillsetu.in / industry |
              Academician: kavita@skillsetu.in / academician |
              Admin: admin@skillsetu.in / admin
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiSend } from '../api.js'

export default {
  name: 'LoginPage',
  emits: ['logged-in', 'go-register'],
  data() {
    return {
      role: 'student',
      form: { email: '', password: '' },
      err: ''
    }
  },
  methods: {
    async login() {
      this.err = ''
      const url = this.role === 'admin' ? '/'
                : this.role === 'industry' ? '/industry_login'
                : this.role === 'academician' ? '/academician_login'
                : '/student_login'
      try {
        const res = await apiSend(url, 'POST', this.form)
        this.$emit('logged-in', res.user)
      } catch (e) {
        this.err = e.message || 'Login failed'
      }
    }
  }
}
</script>
