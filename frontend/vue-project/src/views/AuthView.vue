<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()

// Determine if we are on the login or register path
const isLogin = computed(() => route.path === '/login')
const formTitle = computed(() => isLogin.value ? 'User Login' : 'User Registration')
const buttonText = computed(() => isLogin.value ? 'Log In' : 'Sign Up')

// Form State
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)

// Handle Form Submission
async function handleSubmit() {
  errorMsg.value = ''
  isLoading.value = true
  
  if (!email.value || !password.value) {
    errorMsg.value = 'Email and password are required.'
    isLoading.value = false
    return
  }

  try {
    const credentials = { email: email.value, password: password.value }
    const endpoint = isLogin.value ? 'login' : 'register'

    // Call the Pinia store action
    await authStore.authenticateUser(endpoint, credentials)
    
    // Success: Redirect handled by Pinia store
  } catch (err: any) {
    // Error handling from the Pinia store (which gets it from the backend)
    errorMsg.value = err.message || 'An unknown error occurred during authentication.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-card">
    <h2>{{ formTitle }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" type="password" v-model="password" required>
      </div>

      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>

      <button type="submit" :disabled="isLoading">
        <span v-if="isLoading">Processing...</span>
        <span v-else>{{ buttonText }}</span>
      </button>

      <div class="switch-link">
        <p v-if="isLogin">
          Don't have an account? 
          <RouterLink to="/register">Register here</RouterLink>
        </p>
        <p v-else>
          Already have an account? 
          <RouterLink to="/login">Log in here</RouterLink>
        </p>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Basic Card and Form Styling */
.auth-card {
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-width: 400px;
  margin: 50px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 12px; /* Slightly larger padding */
  background-color: #3498db; /* Blue background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.15s ease;
  
  /* 3D EFFECT STYLES */
  box-shadow: 0 5px 0 #2980b9; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #2980b9; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #2980b9;
  transform: translateY(3px);
}

button:disabled {
  background-color: #95a5a6;
  box-shadow: 0 4px 0 #7f8c8d;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.error-message {
  color: #e74c3c;
  margin-bottom: 15px;
  text-align: center;
}

.switch-link {
    margin-top: 20px;
    text-align: center;
    font-size: 0.9em;
}

.switch-link a {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}
</style>