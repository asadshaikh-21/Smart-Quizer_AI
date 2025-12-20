<!-- <script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header class="navbar">
    <nav>
      <RouterLink to="/">SmartQuizzer</RouterLink>
      <div class="nav-links">
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/profile">Profile</RouterLink>
          <button @click="authStore.logout()" class="logout-btn">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register">Register</RouterLink>
        </template>
      </div>
    </nav>
  </header>

  <main class="container">
    <RouterView /> 
  </main>
</template>

<style scoped>
/* Basic styling for the navigation bar */
.navbar {
  background-color: #34495e; 
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
}

.navbar a {
  color: #ecf0f1; 
  text-decoration: none;
  padding: 0 15px;
  font-weight: bold;
}

.nav-links a {
  margin-left: 15px;
}

.logout-btn {
  background: none;
  border: none;
  color: #f1c40f; 
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  margin-left: 15px;
  padding: 0;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: #e67e22;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
}
</style> -->



<!-- 

<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header class="navbar">
    <nav>
      <RouterLink to="/">SmartQuizzer</RouterLink>
      <div class="nav-links">
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/content">Upload Notes</RouterLink> 
          <RouterLink to="/profile">Profile</RouterLink>
          <button @click="authStore.logout()" class="logout-btn">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register">Register</RouterLink>
        </template>
      </div>
    </nav>
  </header>

  <main class="container">
    <RouterView /> 
  </main>
</template>

<style scoped>
/* Basic styling for the navigation bar */
.navbar {
  background-color: #34495e; 
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
}

.navbar a {
  color: #ecf0f1; 
  text-decoration: none;
  padding: 0 15px;
  font-weight: bold;
}

.nav-links a {
  margin-left: 15px;
}

.logout-btn {
  background: none;
  border: none;
  color: #f1c40f; 
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  margin-left: 15px;
  padding: 0;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: #e67e22;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
}
</style> -->










<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header class="navbar">
    <nav>
      <RouterLink to="/">SmartQuizzer</RouterLink>
      <div class="nav-links">
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/content">Upload Notes</RouterLink> 
          <RouterLink to="/quiz">Start Quiz</RouterLink> 
          <RouterLink to="/analytics">Analytics</RouterLink> 
          <RouterLink to="/admin">Admin</RouterLink> 
          <RouterLink to="/profile">Profile</RouterLink>
          <button @click="authStore.logout()" class="logout-btn">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register">Register</RouterLink>
        </template>
      </div>
    </nav>
  </header>

  <main class="container">
    <RouterView /> 
  </main>
</template>

<style scoped>
/* Basic styling for the navigation bar */
.navbar {
  background-color: #34495e; 
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
}

.navbar a {
  color: #ecf0f1; 
  text-decoration: none;
  padding: 0 15px;
  font-weight: bold;
}

.nav-links a {
  margin-left: 15px;
}

.logout-btn {
  background: none;
  border: none;
  color: #f1c40f; 
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  margin-left: 15px;
  padding: 0;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: #e67e22;
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
}
</style>