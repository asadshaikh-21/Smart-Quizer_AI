<!-- <script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully!'
  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    setTimeout(() => updateStatus.value = '', 3000) // Clear status message after 3 seconds
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style> -->





<!-- 
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; // <-- NEW IMPORT

const authStore = useAuthStore()
const router = useRouter(); // <-- NEW INSTANCE

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully! Redirecting...'
    
    // --- CRITICAL: REDIRECT TO CONTENT INGESTION PAGE ---
    setTimeout(() => {
        router.push('/content'); // <-- REDIRECT AFTER 1.5 SECONDS
    }, 1500);
    // ----------------------------------------------------

  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    // Note: The success message is now cleared by the redirect, 
    // but the error message needs its own timeout if the redirect fails.
    if (updateStatus.value.startsWith('❌')) {
        setTimeout(() => updateStatus.value = '', 3000);
    }
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    /* Ensure text color is light for the dark background */
    color: #e0e0e0; 
}

/* Ensure inner elements are visible */
.current-stats h3, .current-stats strong {
    color: #fff;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style> -->







<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; // <-- NEW IMPORT

const authStore = useAuthStore()
const router = useRouter(); // <-- NEW INSTANCE

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully! Redirecting...'
    
    // --- CRITICAL: REDIRECT TO CONTENT INGESTION PAGE ---
    setTimeout(() => {
        // Redirects to /content to allow user to upload material or be quizzed on existing material.
        router.push('/content'); 
    }, 1500);
    // ----------------------------------------------------

  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    // Clear error message if redirect fails
    if (updateStatus.value.startsWith('❌')) {
        setTimeout(() => updateStatus.value = '', 3000);
    }
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    /* Ensure text color is light for the dark background */
    color: #e0e0e0; 
}

/* Ensure inner elements are visible */
.current-stats h3, .current-stats strong {
    color: #fff;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style>