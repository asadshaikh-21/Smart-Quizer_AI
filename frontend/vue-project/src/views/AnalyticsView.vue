<!-- <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter(); // Correct local instance of router

const performanceData = ref<any[]>([]);
const overallScore = ref(0);
const isLoading = ref(true);
const errorMsg = ref('');

// --- Data Fetching ---
const fetchAnalytics = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/analytics/performance',
            authStore.authHeader
        );
        
        performanceData.value = response.data;
        
        // Calculate Overall Score (Last 20 attempts)
        const answeredData = response.data.filter((d: { is_correct: any; }) => d.is_correct !== undefined);
        const correctAnswers = answeredData.filter((d: { is_correct: any; }) => d.is_correct).length;
        const totalAnswers = answeredData.length;
        
        overallScore.value = totalAnswers > 0 ? Math.round((correctAnswers / totalAnswers) * 100) : 0;
        
    } catch (error: any) {
        errorMsg.value = 'Failed to load analytics data: ' + (error.response?.data?.msg || 'Network error.');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};

// --- Computed Data for Visualization ---
const masteryBreakdown = computed(() => {
    // Groups history by question type to show where the user is weak
    const breakdown = new Map();
    performanceData.value.forEach(d => {
        const type = d.question_type;
        if (!breakdown.has(type)) {
            breakdown.set(type, { total: 0, correct: 0 });
        }
        const stats = breakdown.get(type);
        stats.total++;
        if (d.is_correct) {
            stats.correct++;
        }
    });

    const result = [];
    breakdown.forEach((stats, type) => {
        result.push({
            type: type,
            percentage: Math.round((stats.correct / stats.total) * 100),
            total: stats.total
        });
    });
    
    // Sort by percentage (worst performance first)
    return result.sort((a, b) => a.percentage - b.percentage);
});

// --- Handlers ---

// FIX: Use router.push directly for navigation handlers
const viewQuizConfig = () => {
    router.push({ name: 'quizConfig' });
};

onMounted(fetchAnalytics);
</script>

<template>
  <div class="analytics-container">
    <h1 class="main-title">📈 Learning Performance Dashboard</h1>
    <p class="subtitle">Analysis of your last {{ performanceData.length }} quiz interactions.</p>

    <div v-if="isLoading" class="loading-state">Loading adaptive analytics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else-if="performanceData.length === 0" class="empty-state analytics-card">
        <p>No quiz history available yet. Start a quiz to see your data!</p>
        <button @click="viewQuizConfig" class="start-quiz-btn">Configure New Quiz</button>
    </div>
    
    <div v-else class="analytics-card">
        <div class="gauge-section">
            <div class="gauge-item">
                <span class="gauge-value" :style="{ color: overallScore >= 70 ? '#2ecc71' : '#f1c40f' }">{{ overallScore }}%</span>
                <p class="gauge-label">Overall Accuracy</p>
            </div>
            <div class="gauge-item">
                 <p class="gauge-label">Total Questions Logged</p>
                 <span class="gauge-value">{{ performanceData.length }}</span>
            </div>
        </div>
        
        <h2 class="chart-title">Weakness Breakdown by Question Type</h2>
        
        <div class="bar-chart-section">
            <div v-for="item in masteryBreakdown" :key="item.type" class="bar-item">
                <span class="bar-label">{{ item.type }} ({{ item.total }} attempts)</span>
                <div class="bar-track">
                    <div 
                        class="bar-fill" 
                        :style="{ width: item.percentage + '%' }"
                        :class="{'bar-mastered': item.percentage >= 80, 'bar-weak': item.percentage < 50}"
                    >
                        {{ item.percentage }}%
                    </div>
                </div>
            </div>
        </div>
        
        <button @click="viewQuizConfig" class="view-analytics-btn">Return to Quiz Configuration</button>
    </div>
  </div>
</template>

<style scoped>
.analytics-container {
    max-width: 900px;
    margin: 30px auto;
    color: #e0e0e0;
    text-align: center;
}

.main-title {
    color: #fff;
    text-shadow: 0 0 5px #82aaff;
    margin-bottom: 5px;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}

.analytics-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.loading-state, .empty-state {
    color: #c0c0c0;
    padding: 40px;
    background-color: #2a2a44;
    border-radius: 12px;
}

.start-quiz-btn, .view-analytics-btn {
    width: 100%;
    padding: 14px; 
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 6px 0 #2980b9;
    transition: all 0.15s ease;
    margin-top: 20px;
}

.start-quiz-btn:active, .view-analytics-btn:active {
    box-shadow: 0 2px 0 #2980b9;
    transform: translateY(4px);
}


/* --- GAUGE SECTION (Circular Stat Analog) --- */
.gauge-section {
    display: flex;
    justify-content: space-around;
    padding-bottom: 20px;
    margin-bottom: 30px;
    border-bottom: 1px dashed #444;
}

.gauge-item {
    text-align: center;
}

.gauge-value {
    display: block;
    font-size: 2.5rem;
    font-weight: 900;
    text-shadow: 0 0 5px #f1c40f;
}

.gauge-label {
    color: #9b59b6;
    font-size: 0.9rem;
}

/* --- BAR CHART SECTION --- */
.chart-title {
    color: #c990ff;
    font-size: 1.5rem;
    margin-bottom: 25px;
    text-align: center;
}

.bar-chart-section {
    padding-bottom: 20px;
}

.bar-item {
    margin-bottom: 15px;
}

.bar-label {
    display: block;
    font-weight: 600;
    margin-bottom: 5px;
    color: #e0e0e0;
}

.bar-track {
    background-color: #3e3e5a;
    height: 25px;
    border-radius: 5px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    color: #1a1a2e; 
    font-weight: bold;
    border-radius: 5px 0 0 5px;
    transition: width 1s ease-out; 
    text-align: left;
    
    background-color: #3498db; 
}

.bar-mastered {
    background-color: #2ecc71; 
}

.bar-weak {
    background-color: #e74c3c; 
}
</style> -->












<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter(); // Correct local instance of router

const performanceData = ref<any[]>([]);
const overallScore = ref(0);
const isLoading = ref(true);
const errorMsg = ref('');

// --- FIX: NEW SCORE STATE VARIABLES (CRITICAL) ---
const totalQuestionsAnswered = ref(0);
const totalCorrectCount = ref(0);
// -------------------------------------------------


// --- Data Fetching ---
const fetchAnalytics = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // Reset core metrics before fetching
    totalQuestionsAnswered.value = 0;
    totalCorrectCount.value = 0;
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/analytics/performance',
            authStore.authHeader
        );
        
        performanceData.value = response.data;
        
        // Calculate and assign score to the new ref variables
        const answeredData = response.data.filter((d: { is_correct: any; }) => d.is_correct !== undefined);
        const correctAnswers = answeredData.filter((d: { is_correct: any; }) => d.is_correct).length;
        const totalAnswers = answeredData.length;
        
        totalQuestionsAnswered.value = totalAnswers; // Set the total questions answered
        totalCorrectCount.value = correctAnswers; // Set the total correct count
        
        overallScore.value = totalAnswers > 0 ? Math.round((correctAnswers / totalAnswers) * 100) : 0;
        
    } catch (error: any) {
        errorMsg.value = 'Failed to load analytics data: ' + (error.response?.data?.msg || 'Network error.');
        console.error(error);
    } finally {
        isLoading.value = false;
    }
};

// --- Computed Data for Visualization ---

// FIX: Score Breakdown now uses the globally available ref variables
const scoreBreakdown = computed(() => {
    const total = totalQuestionsAnswered.value; // Use ref variable
    if (total === 0) return { correct: 0, incorrect: 0 };
    
    const correct = totalCorrectCount.value; // Use ref variable
    const incorrect = total - correct;
    
    return {
        correct: Math.round((correct / total) * 100),
        incorrect: Math.round((incorrect / total) * 100)
    };
});


const masteryBreakdown = computed(() => {
    // Groups history by question type to show where the user is weak
    const breakdown = new Map();
    performanceData.value.forEach(d => {
        const type = d.question_type;
        if (!breakdown.has(type)) {
            breakdown.set(type, { total: 0, correct: 0 });
        }
        const stats = breakdown.get(type);
        stats.total++;
        if (d.is_correct) {
            stats.correct++;
        }
    });

    const result = [];
    breakdown.forEach((stats, type) => {
        result.push({
            type: type,
            percentage: Math.round((stats.correct / stats.total) * 100),
            total: stats.total
        });
    });
    
    // Sort by percentage (worst performance first)
    return result.sort((a, b) => a.percentage - b.percentage);
});


// --- Handlers ---
const viewQuizConfig = () => {
    router.push({ name: 'quizConfig' });
};

onMounted(fetchAnalytics);
</script>

<template>
  <div class="analytics-container">
    <h1 class="main-title">📈 Learning Performance Dashboard</h1>
    <p class="subtitle">Analysis of your last {{ performanceData.length }} quiz interactions.</p>

    <div v-if="isLoading" class="loading-state">Loading adaptive analytics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else-if="performanceData.length === 0" class="empty-state analytics-card">
        <p>No quiz history available yet. Start a quiz to see your data!</p>
        <button @click="viewQuizConfig" class="start-quiz-btn">Configure New Quiz</button>
    </div>
    
    <div v-else class="analytics-card">
        
        <div class="gauge-section">
            
            <div class="chart-gauge">
                <div class="doughnut-chart-container">
                    <div 
                        class="doughnut-chart" 
                        :style="{ background: `conic-gradient(#2ecc71 0% ${scoreBreakdown.correct}%, #e74c3c ${scoreBreakdown.correct}% 100%)` }"
                    >
                        <div class="chart-center">
                            <span class="gauge-value" :class="{'score-high': overallScore >= 70, 'score-low': overallScore < 40}">
                                {{ overallScore }}%
                            </span>
                        </div>
                    </div>
                </div>
                <p class="gauge-label">Accuracy Breakdown</p>
            </div>
            
            <div class="stat-group">
                <div class="stat-item">
                    <p class="stat-value">{{ totalQuestionsAnswered }}</p>
                    <p class="gauge-label">Total Questions Logged</p>
                </div>
                 <div class="stat-item">
                    <p class="stat-value score-high">{{ totalCorrectCount }}</p>
                    <p class="gauge-label">Total Correct Answers</p>
                </div>
            </div>
        </div>
        
        <h2 class="chart-title">Weakness Breakdown by Question Type</h2>
        
        <div class="bar-chart-section">
            <div v-for="item in masteryBreakdown" :key="item.type" class="bar-item">
                <span class="bar-label">{{ item.type }} ({{ item.total }} attempts)</span>
                <div class="bar-track">
                    <div 
                        class="bar-fill" 
                        :style="{ width: item.percentage + '%' }"
                        :class="{'bar-mastered': item.percentage >= 80, 'bar-weak': item.percentage < 50}"
                    >
                        {{ item.percentage }}%
                    </div>
                </div>
            </div>
        </div>
        
        <button @click="viewQuizConfig" class="view-analytics-btn">Return to Quiz Configuration</button>
    </div>
  </div>
</template>

<style scoped>
.analytics-container {
    max-width: 900px;
    margin: 30px auto;
    color: #e0e0e0;
    text-align: center;
}

.main-title {
    color: #fff;
    text-shadow: 0 0 5px #82aaff;
    margin-bottom: 5px;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}

.analytics-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.loading-state, .empty-state {
    color: #c0c0c0;
    padding: 40px;
    background-color: #2a2a44;
    border-radius: 12px;
}

.start-quiz-btn, .view-analytics-btn {
    width: 100%;
    padding: 14px; 
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 6px 0 #2980b9;
    transition: all 0.15s ease;
    margin-top: 20px;
}

.start-quiz-btn:active, .view-analytics-btn:active {
    box-shadow: 0 2px 0 #2980b9;
    transform: translateY(4px);
}


/* --- GAUGE SECTION (Flex Layout for Charts and Stats) --- */
.gauge-section {
    display: flex;
    justify-content: space-around;
    align-items: center; /* Vertically aligns items in the row */
    padding-bottom: 20px;
    margin-bottom: 30px;
    border-bottom: 1px dashed #444;
    gap: 20px;
}

.chart-gauge, .stat-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 30%; /* Allocate width to make space for the chart */
}

.stat-item {
    text-align: center;
    padding: 10px;
}

.stat-value {
    display: block;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1c40f;
}

.gauge-label {
    color: #9b59b6;
    font-size: 0.9rem;
}

/* --- DOUGHNUT CHART STYLES --- */
.doughnut-chart-container {
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 10px;
}

.doughnut-chart {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    /* Conic-gradient is dynamic in template: Correct=Green, Incorrect=Red */
    background: #3e3e5a; 
    display: flex;
    align-items: center;
    justify-content: center;
}

.chart-center {
    position: absolute;
    width: 90px;
    height: 90px;
    background: #2a2a44; 
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.gauge-value {
    font-size: 1.5rem;
    font-weight: 900;
}

/* Score Color Classes */
.score-high { color: #2ecc71; }
.score-mid { color: #f1c40f; }
.score-low { color: #e74c3c; }

/* --- BAR CHART SECTION --- */
.chart-title {
    color: #c990ff;
    font-size: 1.5rem;
    margin-bottom: 25px;
    text-align: center;
}

.bar-chart-section {
    padding-bottom: 20px;
}

.bar-item {
    margin-bottom: 15px;
}

.bar-label {
    display: block;
    font-weight: 600;
    margin-bottom: 5px;
    color: #e0e0e0;
}

.bar-track {
    background-color: #3e3e5a;
    height: 25px;
    border-radius: 5px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    color: #1a1a2e; 
    font-weight: bold;
    border-radius: 5px 0 0 5px;
    transition: width 1s ease-out; 
    text-align: left;
    
    background-color: #3498db; 
}

.bar-mastered {
    background-color: #2ecc71; 
}

.bar-weak {
    background-color: #e74c3c; 
}
</style>