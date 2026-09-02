<template>
  <nav class="navbar bg-maroon px-3" v-if="user">
    <span class="navbar-brand mb-0 h1 text-white">
      <span class="brand-logo me-2">&#9650;</span>
      SkillSetu
      <span class="tagline ms-2">Setu se Sapno Tak</span>
    </span>
    <div>
      <span class="text-white me-3">{{ user.name }} ({{ user.role }})</span>
      <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
    </div>
  </nav>

  <div class="container mt-4 mb-5">
    <LoginPage v-if="page==='login'" @logged-in="onLogin" @go-register="page='register'" />
    <RegisterPage v-else-if="page==='register'" @go-login="page='login'" />
    <StudentDashboard v-else-if="page==='student'" :user="user" @profile-updated="onProfileUpdated" />
    <IndustryDashboard v-else-if="page==='industry'" :user="user" />
    <AcademicianDashboard v-else-if="page==='academician'" :user="user" />
    <InstitutionDashboard v-else-if="page==='admin'" />
  </div>
</template>

<script>
import LoginPage from './components/LoginPage.vue'
import RegisterPage from './components/RegisterPage.vue'
import StudentDashboard from './components/StudentDashboard.vue'
import IndustryDashboard from './components/IndustryDashboard.vue'
import AcademicianDashboard from './components/AcademicianDashboard.vue'
import InstitutionDashboard from './components/InstitutionDashboard.vue'
import { apiGet } from './api.js'

export default {
  name: 'App',
  components: { LoginPage, RegisterPage, StudentDashboard, IndustryDashboard, AcademicianDashboard, InstitutionDashboard },
  data() {
    return { page: 'login', user: null }
  },
  methods: {
    onLogin(user) {
      this.user = user
      this.goToDashboard()
    },
    goToDashboard() {
      if (this.user.role === 'admin') this.page = 'admin'
      else if (this.user.role === 'industry') this.page = 'industry'
      else if (this.user.role === 'academician') this.page = 'academician'
      else this.page = 'student'
    },
    onProfileUpdated({ name, email }) {
      this.user.name = name
      this.user.email = email
    },
    async logout() {
      await apiGet('/logout')
      this.user = null
      this.page = 'login'
    }
  }
}
</script>
