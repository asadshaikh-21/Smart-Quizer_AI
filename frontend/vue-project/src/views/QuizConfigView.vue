<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useQuizStore } from '@/stores/quiz_store'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const quizStore = useQuizStore();
const router = useRouter();

// State
const contentList = ref<any[]>([]);
const selectedContentId = ref<string | null>(null);
const numQuestions = ref(10); // Default to 10 questions
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list',
            authStore.authHeader
        );
        contentList.value = response.data;
        if (contentList.value.length > 0) {
            // Use the most recently uploaded content by default (or the first one)
            selectedContentId.value = contentList.value[0]._id; 
        }
    } catch (error: any) {
        errorMsg.value = 'Failed to load content list. Please upload notes.';
    } finally {
        isLoading.value = false;
    }
};

// --- Start Quiz Action ---
const startQuiz = () => {
    if (!selectedContentId.value) {
        errorMsg.value = "Please select a set of notes.";
        return;
    }
    if (numQuestions.value < 1) {
        errorMsg.value = "Please enter a valid number of questions.";
        return;
    }
    
    // Pass the required configuration to the store and navigate to the active quiz view
    quizStore.setConfig(selectedContentId.value, numQuestions.value);
    router.push({ name: 'activeQuiz' }); // Navigate to the page where the quiz actually runs
};

onMounted(fetchContentList);
</script>

<template>
    <div class="quiz-config-container">
        <h1>Configure Your Adaptive Quiz</h1>

        <div class="config-card">
            <p class="section-subtitle">Select the material and quiz length.</p>

            <div v-if="isLoading">Loading content...</div>
            <div v-else-if="contentList.length === 0" class="empty-state">
                No notes found. Please <router-link to="/content">Upload Notes</router-link> first!
            </div>
            <div v-else>
                <div class="form-group">
                    <label for="contentSelect">Study Material:</label>
                    <select v-model="selectedContentId" id="contentSelect" class="content-select">
                        <option v-for="content in contentList" :key="content._id" :value="content._id">
                            {{ content.title }} ({{ content.chunk_count }} Chunks)
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="numQuestions">Number of Questions (1-50):</label>
                    <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="50">
                </div>
                
                <p class="note">Difficulty: <strong class="difficulty">{{ authStore.userProfile?.difficulty_level || 'Intermediate' }}</strong> (Set in Profile)</p>
                
                <button @click="startQuiz" :disabled="!selectedContentId || numQuestions < 1" class="start-btn">
                    Start Quiz Generation
                </button>
            </div>
            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<style scoped>
.quiz-config-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}

h1 {
    color: #fff;
    margin-bottom: 40px;
    text-shadow: 0 0 5px #82aaff;
}

.config-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.section-subtitle {
    color: #e0e0e0;
    margin-bottom: 20px;
    font-size: 1.1rem;
    text-align: center;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="number"], .content-select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #3e3e5a;
    color: #fff;
    border: 1px solid #555;
    font-size: 1rem;
    box-sizing: border-box;
}

.note {
    color: #c0c0c0;
    font-size: 1rem;
    margin-top: 20px;
    margin-bottom: 25px;
    text-align: center;
}

.difficulty {
    color: #f1c40f; /* Highlight difficulty */
}

.empty-state {
    color: #e74c3c;
    margin: 30px 0;
    text-align: center;
}

.start-btn {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; /* Green for Start */
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
    margin-top: 20px;
}

.start-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}
</style> -->








<!-- 
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useQuizStore } from '@/stores/quiz_store'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const quizStore = useQuizStore();
const router = useRouter();

// State
const contentList = ref<any[]>([]);
const selectedContentId = ref<string | null>(null);
const numQuestions = ref(10); // Default to 10 questions
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list',
            authStore.authHeader
        );
        contentList.value = response.data;
        if (contentList.value.length > 0) {
            // Select the most recently uploaded content by default
            // By sorting by created_at (if we fetched it), or just selecting the first one for simplicity
            selectedContentId.value = contentList.value[0]._id; 
        }
    } catch (error: any) {
        // The message is displayed to the user if the fetch fails
        errorMsg.value = 'Failed to load content list. Please upload notes.';
    } finally {
        isLoading.value = false;
    }
};

// --- Start Quiz Action ---
const startQuiz = () => {
    // 1. Basic Validation
    if (!selectedContentId.value) {
        errorMsg.value = "Please select a set of notes.";
        return;
    }
    if (numQuestions.value < 1) {
        errorMsg.value = "Please enter a valid number of questions.";
        return;
    }
    
    // 2. Pass the required configuration to the store
    quizStore.setConfig(selectedContentId.value, numQuestions.value);
    
    // 3. Navigate to the Active Quiz Runner page
    router.push({ name: 'activeQuiz' }); 
};

onMounted(fetchContentList);
</script>

<template>
    <div class="quiz-config-container">
        <h1>Configure Your Adaptive Quiz</h1>

        <div class="config-card">
            <p class="section-subtitle">Select the material and quiz length.</p>

            <div v-if="isLoading">Loading content...</div>
            <div v-else-if="contentList.length === 0" class="empty-state">
                No notes found. Please <router-link to="/content">Upload Notes</router-link> first!
            </div>
            <div v-else>
                <div class="form-group">
                    <label for="contentSelect">Study Material:</label>
                    <select v-model="selectedContentId" id="contentSelect" class="content-select">
                        <option v-for="content in contentList" :key="content._id" :value="content._id">
                            {{ content.title }} ({{ content.chunk_count }} Chunks)
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="numQuestions">Number of Questions (1-50):</label>
                    <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="50">
                </div>
                
                <p class="note">Difficulty: <strong class="difficulty">{{ authStore.userProfile?.difficulty_level || 'Intermediate' }}</strong> (Set in Profile)</p>
                
                <button @click="startQuiz" :disabled="!selectedContentId || numQuestions < 1" class="start-btn">
                    Start Quiz Generation
                </button>
            </div>
            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<style scoped>
.quiz-config-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}

h1 {
    color: #fff;
    margin-bottom: 40px;
    text-shadow: 0 0 5px #82aaff;
}

.config-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.section-subtitle {
    color: #e0e0e0;
    margin-bottom: 20px;
    font-size: 1.1rem;
    text-align: center;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="number"], .content-select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #3e3e5a;
    color: #fff;
    border: 1px solid #555;
    font-size: 1rem;
    box-sizing: border-box;
}

.note {
    color: #c0c0c0;
    font-size: 1rem;
    margin-top: 20px;
    margin-bottom: 25px;
    text-align: center;
}

.difficulty {
    color: #f1c40f; /* Highlight difficulty */
}

.empty-state {
    color: #e74c3c;
    margin: 30px 0;
    text-align: center;
}

.start-btn {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; /* Green for Start */
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
    margin-top: 20px;
}

.start-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}

.error-message {
    color: #e74c3c;
    margin-top: 15px;
    text-align: center;
}
</style> -->








<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useQuizStore } from '@/stores/quiz_store'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const quizStore = useQuizStore();
const router = useRouter();

// State
const contentList = ref<any[]>([]);
const selectedContentId = ref<string | null>(null);
const numQuestions = ref(10); // Default to 10 questions
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list',
            authStore.authHeader
        );
        contentList.value = response.data;
        if (contentList.value.length > 0) {
            // Select the most recently uploaded content by default (or the first one)
            selectedContentId.value = contentList.value[0]._id; 
        }
    } catch (error: any) {
        // The message is displayed to the user if the fetch fails
        errorMsg.value = 'Failed to load content list. Please upload notes.';
    } finally {
        isLoading.value = false;
    }
};

// --- Start Quiz Action ---
const startQuiz = () => {
    // 1. Basic Validation
    if (!selectedContentId.value) {
        errorMsg.value = "Please select a set of notes.";
        return;
    }
    if (numQuestions.value < 1) {
        errorMsg.value = "Please enter a valid number of questions.";
        return;
    }
    
    // 2. Pass the required configuration to the store
    quizStore.setConfig(selectedContentId.value, numQuestions.value);
    
    // 3. Navigate to the Active Quiz Runner page
    router.push({ name: 'activeQuiz' }); 
};

// --- Analytics Handler ---
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};

onMounted(fetchContentList);
</script>

<template>
    <div class="quiz-config-container">
        <h1>Configure Your Adaptive Quiz</h1>

        <div class="config-card">
            <p class="section-subtitle">Select the material and quiz length.</p>

            <div v-if="isLoading">Loading content...</div>
            <div v-else-if="contentList.length === 0" class="empty-state">
                No notes found. Please <router-link to="/content">Upload Notes</router-link> first!
            </div>
            <div v-else>
                <div class="form-group">
                    <label for="contentSelect">Study Material:</label>
                    <select v-model="selectedContentId" id="contentSelect" class="content-select">
                        <option v-for="content in contentList" :key="content._id" :value="content._id">
                            {{ content.title }} ({{ content.chunk_count }} Chunks)
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="numQuestions">Number of Questions (1-50):</label>
                    <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="50">
                </div>
                
                <p class="note">Difficulty: <strong class="difficulty">{{ authStore.userProfile?.difficulty_level || 'Intermediate' }}</strong> (Set in Profile)</p>
                
                <button @click="startQuiz" :disabled="!selectedContentId || numQuestions < 1" class="start-btn">
                    Start Quiz Generation
                </button>
            </div>
            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        </div>
        
        <button @click="viewAnalytics" class="view-analytics-btn">
            View Performance Analytics
        </button>
    </div>
</template>

<style scoped>
.quiz-config-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}

h1 {
    color: #fff;
    margin-bottom: 40px;
    text-shadow: 0 0 5px #82aaff;
}

.config-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    margin-bottom: 20px; /* Space above analytics button */
}

.section-subtitle {
    color: #e0e0e0;
    margin-bottom: 20px;
    font-size: 1.1rem;
    text-align: center;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="number"], .content-select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #3e3e5a;
    color: #fff;
    border: 1px solid #555;
    font-size: 1rem;
    box-sizing: border-box;
}

.note {
    color: #c0c0c0;
    font-size: 1rem;
    margin-top: 20px;
    margin-bottom: 25px;
    text-align: center;
}

.difficulty {
    color: #f1c40f; /* Highlight difficulty */
}

.empty-state {
    color: #e74c3c;
    margin: 30px 0;
    text-align: center;
}

.start-btn {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; /* Green for Start */
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
    margin-top: 20px;
}

.start-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}

.error-message {
    color: #e74c3c;
    margin-top: 15px;
    text-align: center;
}

/* --- NEW ANALYTICS BUTTON STYLING --- */
.view-analytics-btn {
    width: 100%;
    padding: 14px;
    background-color: #3498db; /* Blue color */
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.view-analytics-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}
</style> -->









<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useQuizStore } from '@/stores/quiz_store'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const quizStore = useQuizStore();
const router = useRouter();

// State
const contentList = ref<any[]>([]);
const selectedContentId = ref<string | null>(null);
const numQuestions = ref(10); // Default to 10 questions
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list',
            authStore.authHeader
        );
        contentList.value = response.data;
        if (contentList.value.length > 0) {
            // Select the most recently uploaded content by default (or the first one)
            selectedContentId.value = contentList.value[0]._id; 
        }
    } catch (error: any) {
        // The message is displayed to the user if the fetch fails
        errorMsg.value = 'Failed to load content list. Please upload notes.';
    } finally {
        isLoading.value = false;
    }
};

// --- Start Quiz Action ---
const startQuiz = () => {
    // 1. Basic Validation
    if (!selectedContentId.value) {
        errorMsg.value = "Please select a set of notes.";
        return;
    }
    if (numQuestions.value < 1) {
        errorMsg.value = "Please enter a valid number of questions.";
        return;
    }
    
    // 2. Pass the required configuration to the store
    quizStore.setConfig(selectedContentId.value, numQuestions.value);
    
    // 3. Navigate to the Active Quiz Runner page
    router.push({ name: 'activeQuiz' }); 
};

// --- Analytics Handler (CRITICAL: Navigation logic) ---
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};

onMounted(fetchContentList);
</script>

<template>
    <div class="quiz-config-container">
        <h1>Configure Your Adaptive Quiz</h1>

        <div class="config-card">
            <p class="section-subtitle">Select the material and quiz length.</p>

            <div v-if="isLoading">Loading content...</div>
            <div v-else-if="contentList.length === 0" class="empty-state">
                No notes found. Please <router-link to="/content">Upload Notes</router-link> first!
            </div>
            <div v-else>
                <div class="form-group">
                    <label for="contentSelect">Study Material:</label>
                    <select v-model="selectedContentId" id="contentSelect" class="content-select">
                        <option v-for="content in contentList" :key="content._id" :value="content._id">
                            {{ content.title }} ({{ content.chunk_count }} Chunks)
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="numQuestions">Number of Questions (1-50):</label>
                    <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="50">
                </div>
                
                <p class="note">Difficulty: <strong class="difficulty">{{ authStore.userProfile?.difficulty_level || 'Intermediate' }}</strong> (Set in Profile)</p>
                
                <button @click="startQuiz" :disabled="!selectedContentId || numQuestions < 1" class="start-btn">
                    Start Quiz Generation
                </button>
            </div>
            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<style scoped>
.quiz-config-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}

h1 {
    color: #fff;
    margin-bottom: 40px;
    text-shadow: 0 0 5px #82aaff;
}

.config-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    margin-bottom: 20px; /* Space above analytics button */
}

.section-subtitle {
    color: #e0e0e0;
    margin-bottom: 20px;
    font-size: 1.1rem;
    text-align: center;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="number"], .content-select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #3e3e5a;
    color: #fff;
    border: 1px solid #555;
    font-size: 1rem;
    box-sizing: border-box;
}

.note {
    color: #c0c0c0;
    font-size: 1rem;
    margin-top: 20px;
    margin-bottom: 25px;
    text-align: center;
}

.difficulty {
    color: #f1c40f; /* Highlight difficulty */
}

.empty-state {
    color: #e74c3c;
    margin: 30px 0;
    text-align: center;
}

.start-btn {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; /* Green for Start */
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
    margin-top: 20px;
}

.start-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}

.error-message {
    color: #e74c3c;
    margin-top: 15px;
    text-align: center;
}

/* --- NEW ANALYTICS BUTTON STYLING --- */
.view-analytics-btn {
    width: 100%;
    padding: 14px;
    background-color: #3498db; /* Blue color */
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.view-analytics-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}
</style>