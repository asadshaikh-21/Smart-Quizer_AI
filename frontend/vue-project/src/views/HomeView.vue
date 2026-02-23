<!-- <script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue';

// 1. Import and instantiate the store
const authStore = useAuthStore()

// 2. Create a computed property to check authentication status
//    Note: Pinia state/getters are reactive and must be accessed with .value in setup()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<template>
  <div class="home-container">
    <h1 class="main-title">🧠 SmartQuizzer: Adaptive Learning Platform</h1>
    <p class="tagline">Your personalized path to mastery, powered by AI.</p>
    
    <div class="cta-section">
      <p v-if="!isAuthenticated">
        To begin your adaptive learning journey, please **<router-link to="/login">Log In</router-link>** or **<router-link to="/register">Register</router-link>**.
      </p>
      <p v-else>
        Welcome back! Visit your **<router-link to="/profile">Profile</router-link>** to set your learning preferences and start a new quiz.
      </p>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  text-align: center;
  padding: 50px 20px;
}

.main-title {
  font-size: 2.5rem;
  color: #34495e; 
  margin-bottom: 10px;
}

.tagline {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 30px;
}

.cta-section {
  padding: 30px;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  background-color: #fcfcfc;
  display: inline-block;
}

.cta-section a {
  color: #3498db; 
  font-weight: bold;
  text-decoration: none;
}
</style> -->




<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue';

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<template>
  <div class="landing-container">
    <div class="glow-sphere"></div>
    <h1 class="landing-title">SMART QUIZZER AI</h1>
    <h2 class="landing-subtitle">ADAPTIVE QUIZ GENERATOR</h2>
    <p class="landing-tagline">Welcome to Smart Learning. Your personalized path to mastery.</p>
    
    <div class="button-group">
      <router-link v-if="!isAuthenticated" to="/register" class="action-btn register-btn">
        REGISTER
      </router-link>
      
      <router-link v-if="!isAuthenticated" to="/login" class="action-btn login-btn">
        LOG IN
      </router-link>
      
      <router-link v-else to="/profile" class="action-btn dashboard-btn">
        GO TO DASHBOARD
      </router-link>
    </div>
    
  </div>
</template>

<style scoped>
.landing-container {
  padding: 100px 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 10; /* Ensures content is above the glow sphere */
}

.landing-title {
  font-size: 3.5rem;
  font-weight: 900;
  color: #fff;
  letter-spacing: 5px;
  text-shadow: 0 0 10px #82aaff; /* Text glow effect */
  margin-bottom: 5px;
}

.landing-subtitle {
  font-size: 1.8rem;
  font-weight: 300;
  color: #c990ff;
  letter-spacing: 3px;
  margin-bottom: 40px;
}

.landing-tagline {
  font-size: 1.2rem;
  color: #e0e0e0;
  margin-bottom: 50px;
}

/* --- GLOW SPHERE EFFECT --- */
.glow-sphere {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 350px;
    height: 350px;
    background: radial-gradient(#82aaff, rgba(130, 170, 255, 0));
    border-radius: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.3;
    filter: blur(50px);
    z-index: 5;
    animation: pulse 5s infinite alternate;
}

@keyframes pulse {
    0% { transform: translate(-50%, -50%) scale(0.9); opacity: 0.3; }
    100% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.45; }
}

/* --- 3D GLOW BUTTON STYLES --- */
.button-group {
    display: flex;
    gap: 30px;
}

.action-btn {
    text-decoration: none;
    padding: 15px 35px;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: bold;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    /* Base 3D shadow */
    box-shadow: 0 8px 0 rgba(0, 0, 0, 0.4); 
    transform: translateY(0);
    position: relative;
}

/* REGISTER (Vibrant Blue) */
.register-btn {
    background-color: #007bff; 
    color: #fff;
    box-shadow: 0 8px 0 #0056b3; 
    /* Outer glow effect */
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
    filter: drop-shadow(0 0 10px #007bff);
}

.register-btn:hover {
    background-color: #0056b3;
    filter: drop-shadow(0 0 15px #007bff);
}

.register-btn:active {
    box-shadow: 0 2px 0 #0056b3; 
    transform: translateY(6px); /* Press down */
}

/* LOGIN (Vibrant Green) */
.login-btn, .dashboard-btn {
    background-color: #2ecc71; 
    color: #1a1a2e; /* Darker text for contrast */
    box-shadow: 0 8px 0 #219d5c;
    /* Outer glow effect */
    text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
    filter: drop-shadow(0 0 10px #2ecc71);
}

.login-btn:hover, .dashboard-btn:hover {
    background-color: #219d5c;
    filter: drop-shadow(0 0 15px #2ecc71);
}

.login-btn:active, .dashboard-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(6px); /* Press down */
}
</style>