// D:\SmartQuizzer\frontend\vue-project\src\stores\auth.ts

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
// CRITICAL FIX: Explicitly import the router instance from the index file.
import router from '@/router/index' 

// Base URL for the Flask backend
const API_URL = 'http://localhost:5000/api'

// Define the shape of a user's profile data
interface UserProfile {
  _id: string;
  email: string;
  subjects_of_interest: string[];
  difficulty_level: 'Beginner' | 'Intermediate' | 'Expert';
  performance_history: any[]; 
}

export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const isAuthenticated = computed(() => !!accessToken.value)
  const userProfile = ref<UserProfile | null>(null)

  // --- Getters ---
  const authHeader = computed(() => {
    return {
      headers: {
        Authorization: `Bearer ${accessToken.value}`
      }
    }
  })

  // --- Actions ---

  async function authenticateUser(endpoint: 'login' | 'register', credentials: any) {
    try {
      const response = await axios.post(`${API_URL}/auth/${endpoint}`, credentials)
      
      const token = response.data.access_token
      accessToken.value = token
      localStorage.setItem('access_token', token)
      
      await loadUserProfile() 

      router.push('/profile') 
    } catch (error: any) {
      const msg = error.response?.data?.msg || `Authentication failed for ${endpoint}.`
      throw new Error(msg)
    }
  }

  async function loadUserProfile() {
    if (!isAuthenticated.value) {
      userProfile.value = null
      return
    }
    try {
      const response = await axios.get(`${API_URL}/profile`, authHeader.value)
      userProfile.value = response.data as UserProfile
    } catch (error) {
      console.error("Error loading user profile. Token might be invalid.", error)
      logout() 
    }
  }

  async function updateProfile(data: Partial<UserProfile>) {
    if (!isAuthenticated.value) return
    try {
      await axios.put(`${API_URL}/profile`, data, authHeader.value)
      await loadUserProfile() 
    } catch (error: any) {
      const msg = error.response?.data?.msg || "Failed to update profile."
      throw new Error(msg)
    }
  }

  function logout() {
    accessToken.value = null
    localStorage.removeItem('access_token')
    userProfile.value = null
    router.push('/login')
  }

  if (accessToken.value) {
    loadUserProfile()
  }

  return { 
    accessToken, 
    isAuthenticated, 
    userProfile, 
    authHeader, 
    authenticateUser, 
    logout, 
    loadUserProfile, 
    updateProfile 
  }
})