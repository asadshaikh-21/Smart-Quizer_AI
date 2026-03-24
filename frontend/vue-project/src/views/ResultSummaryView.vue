<!-- <script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

const totalQuestions = computed(() => quizStore.quizQuestions.length);
const correctCount = computed(() => 
    quizStore.quizQuestions.filter(q => q.isCorrect === true).length
);
const finalScorePercentage = computed(() => {
    if (totalQuestions.value === 0) return 0;
    return Math.round((correctCount.value / totalQuestions.value) * 100);
});

// Redirect away if no quiz data is present
onMounted(() => {
    if (totalQuestions.value === 0) {
        router.push('/quiz');
    }
});
</script>

<template>
  <div class="summary-container">
    <div class="summary-header">
        <h1>Quiz Complete! 🎉</h1>
        <p class="final-score">Your Score: 
            <span :class="{'score-high': finalScorePercentage >= 70, 'score-low': finalScorePercentage < 40, 'score-mid': finalScorePercentage >= 40 && finalScorePercentage < 70}">
                {{ finalScorePercentage }}%
            </span>
        </p>
        <p class="summary-count">({{ correctCount }} correct out of {{ totalQuestions }} questions)</p>
    </div>

    <div class="review-section">
        <h2>Detailed Review</h2>
        <div v-for="(q, index) in quizStore.quizQuestions" :key="index" class="question-review-card">
            <div 
                class="review-header"
                :class="{'header-correct': q.isCorrect, 'header-incorrect': !q.isCorrect}"
            >
                <span class="review-status">
                    {{ index + 1 }}. {{ q.isCorrect ? '✅ Correct' : '❌ Incorrect' }} ({{ q.type }})
                </span>
                <span class="subject-tag">{{ q.content_chunk.substring(0, 50) }}...</span>
            </div>

            <p class="review-question-text">{{ q.question }}</p>
            
            <div class="review-explanation">
                <p><strong>Correct Answer:</strong> <span class="final-answer-text">{{ q.answer }}</span></p>
                <p><strong>Explanation:</strong> {{ q.explanation }}</p>
            </div>
        </div>
    </div>

    <button @click="router.push('/quiz')" class="new-quiz-btn">Start New Quiz</button>
  </div>
</template>

<style scoped>
.summary-container {
    max-width: 900px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}

.summary-header {
    background-color: #3e3e5a;
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 40px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.summary-header h1 {
    color: #fff;
    text-shadow: 0 0 8px #c990ff;
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.final-score {
    font-size: 2.5rem;
    font-weight: 900;
}

.score-high { color: #2ecc71; } /* Green */
.score-mid { color: #f1c40f; } /* Yellow */
.score-low { color: #e74c3c; } /* Red */

.summary-count {
    color: #c0c0c0;
    font-size: 1.1rem;
}

.review-section {
    text-align: left;
    margin-bottom: 40px;
}

.review-section h2 {
    color: #c990ff;
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.question-review-card {
    background-color: #2a2a44;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.review-header {
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #1a1a2e; 
}

.header-correct {
    background-color: #2ecc71; /* Green header for correct */
}

.header-incorrect {
    background-color: #e74c3c; /* Red header for incorrect */
}

.review-question-text {
    padding: 15px 20px 10px;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e0e0e0;
}

.review-explanation {
    background-color: #3e3e5a;
    padding: 15px 20px;
    border-top: 1px solid #444;
    font-size: 0.95rem;
}

.review-explanation strong {
    color: #f1c40f; /* Highlight explanation labels */
    margin-right: 5px;
}

.final-answer-text {
    font-weight: bold;
    color: #b3e0ff; /* Light blue for answer text */
}

/* Button style inherits from other components */
.new-quiz-btn {
    padding: 12px 30px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 6px 0 #2980b9;
    transition: all 0.15s ease;
}

.new-quiz-btn:active {
    box-shadow: 0 2px 0 #2980b9;
    transform: translateY(4px);
}
</style> -->




<!-- 
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

const totalQuestions = computed(() => quizStore.quizQuestions.length);
const correctCount = computed(() => 
    quizStore.quizQuestions.filter(q => q.isCorrect === true).length
);
const finalScorePercentage = computed(() => {
    if (totalQuestions.value === 0) return 0;
    return Math.round((correctCount.value / totalQuestions.value) * 100);
});

// Redirect away if no quiz data is present
onMounted(() => {
    if (totalQuestions.value === 0) {
        router.push('/quiz');
    }
});

// Handler for the new Analytics button
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};
</script>

<template>
  <div class="summary-container">
    <div class="summary-header">
        <h1>Quiz Complete! 🎉</h1>
        <p class="final-score">Your Score: 
            <span :class="{'score-high': finalScorePercentage >= 70, 'score-low': finalScorePercentage < 40, 'score-mid': finalScorePercentage >= 40 && finalScorePercentage < 70}">
                {{ finalScorePercentage }}%
            </span>
        </p>
        <p class="summary-count">({{ correctCount }} correct out of {{ totalQuestions }} questions)</p>
    </div>

    <div class="review-section">
        <h2>Detailed Review</h2>
        <div v-for="(q, index) in quizStore.quizQuestions" :key="index" class="question-review-card">
            <div 
                class="review-header"
                :class="{'header-correct': q.isCorrect, 'header-incorrect': !q.isCorrect}"
            >
                <span class="review-status">
                    {{ index + 1 }}. {{ q.isCorrect ? '✅ Correct' : '❌ Incorrect' }} ({{ q.type }})
                </span>
                <span class="subject-tag">{{ q.content_chunk.substring(0, 50) }}...</span> 
            </div>

            <p class="review-question-text">{{ q.question }}</p>
            
            <div class="review-explanation">
                <p><strong>Correct Answer:</strong> <span class="final-answer-text">{{ q.answer }}</span></p>
                <p><strong>Explanation:</strong> {{ q.explanation }}</p>
            </div>
        </div>
    </div>

    <div class="button-group-footer">
        <button @click="viewAnalytics" class="new-quiz-btn view-analytics-btn">
            View Performance Analytics
        </button>

        <button @click="router.push('/quiz')" class="new-quiz-btn start-new-quiz-btn">
            Start New Quiz
        </button>
    </div>
  </div>
</template>

<style scoped>
.summary-container {
    max-width: 900px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}

.summary-header {
    background-color: #3e3e5a;
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 40px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.summary-header h1 {
    color: #fff;
    text-shadow: 0 0 8px #c990ff;
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.final-score {
    font-size: 2.5rem;
    font-weight: 900;
}

.score-high { color: #2ecc71; } /* Green */
.score-mid { color: #f1c40f; } /* Yellow */
.score-low { color: #e74c3c; } /* Red */

.summary-count {
    color: #c0c0c0;
    font-size: 1.1rem;
}

.review-section {
    text-align: left;
    margin-bottom: 40px;
}

.review-section h2 {
    color: #c990ff;
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.question-review-card {
    background-color: #2a2a44;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.review-header {
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #1a1a2e; 
}

.header-correct {
    background-color: #2ecc71; /* Green header for correct */
}

.header-incorrect {
    background-color: #e74c3c; /* Red header for incorrect */
}

.review-question-text {
    padding: 15px 20px 10px;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e0e0e0;
}

.review-explanation {
    background-color: #3e3e5a;
    padding: 15px 20px;
    border-top: 1px solid #444;
    font-size: 0.95rem;
}

.review-explanation strong {
    color: #f1c40f; /* Highlight explanation labels */
    margin-right: 5px;
}

.final-answer-text {
    font-weight: bold;
    color: #b3e0ff; /* Light blue for answer text */
}

/* --- BUTTON GROUP LAYOUT (NEW) --- */
.button-group-footer {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 20px;
}

/* Base button style (for Start New Quiz) */
.new-quiz-btn {
    flex-grow: 1;
    padding: 12px 20px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 6px 0 #2980b9;
    transition: all 0.15s ease;
}

.new-quiz-btn:active {
    box-shadow: 0 2px 0 #2980b9;
    transform: translateY(4px);
}

/* Distinct style for Analytics Button */
.view-analytics-btn {
    background-color: #9b59b6; /* Purple color */
    box-shadow: 0 6px 0 #8e44ad;
}

.view-analytics-btn:active {
    box-shadow: 0 2px 0 #8e44ad;
    transform: translateY(4px);
}
</style> -->













<!-- <script setup lang="ts">
import { computed, onMounted, ref } from 'vue'; // Added 'ref'
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; // For API calls
import { useAuthStore } from '@/stores/auth'; // Must be imported to get auth header

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); // Instantiate auth store

const totalQuestions = computed(() => quizStore.quizQuestions.length);
const correctCount = computed(() => 
    quizStore.quizQuestions.filter(q => q.isCorrect === true).length
);
const finalScorePercentage = computed(() => {
    if (totalQuestions.value === 0) return 0;
    return Math.round((correctCount.value / totalQuestions.value) * 100);
});

// --- STATE FOR MODULE 7 (COACHING) ---
const coachingText = ref('');
const isCoachingLoading = ref(false);
// --------------------------------------

// Redirect away if no quiz data is present
onMounted(() => {
    if (totalQuestions.value === 0) {
        router.push('/quiz');
    }
});

// MOCK FUNCTION: In a real app, you would send coachingText to a TTS API here
const generateTtsUrl = (text: string) => {
    // Return a mocked URL for audio playback (Limited to 200 chars for API safety)
    const encodedText = encodeURIComponent(text.substring(0, 200));
    return `https://mock-tts-service.com/generate?text=${encodedText}`;
};


// Function to generate and fetch the coaching text (Module 7)
const getCoachingSuggestion = async () => {
    if (isCoachingLoading.value || totalQuestions.value === 0 || coachingText.value) return; // Prevent double-click
    
    isCoachingLoading.value = true;
    coachingText.value = 'Generating personalized suggestion...'; // Loading state message

    // Data needed for the AI prompt (pulled from the store's static results)
    const analysisData = {
        quiz_results: quizStore.quizQuestions, // Full quiz history for deep analysis
        total_correct: correctCount.value,
        total_answered: totalQuestions.value,
    };

    try {
        const response = await axios.post(
            'http://localhost:5000/api/coaching/suggest',
            analysisData,
            authStore.authHeader // Authenticate the request
        );
        
        coachingText.value = response.data.suggestion_text;
        
    } catch (e) {
        coachingText.value = "Sorry, I am unable to generate a coaching session right now. Please check your API key/quota.";
        console.error("Coaching API Failed:", e);
    } finally {
        isCoachingLoading.value = false;
    }
};

// Handler for the existing Analytics button
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};
</script>

<template>
  <div class="summary-container">
    <div class="summary-header">
        <h1>Quiz Complete! 🎉</h1>
        <p class="final-score">Your Score: 
            <span :class="{'score-high': finalScorePercentage >= 70, 'score-low': finalScorePercentage < 40, 'score-mid': finalScorePercentage >= 40 && finalScorePercentage < 70}">
                {{ finalScorePercentage }}%
            </span>
        </p>
        <p class="summary-count">({{ correctCount }} correct out of {{ totalQuestions }} questions)</p>
    </div>

    <div class="review-section">
        <h2>Detailed Review</h2>
        <div v-for="(q, index) in quizStore.quizQuestions" :key="index" class="question-review-card">
            <div 
                class="review-header"
                :class="{'header-correct': q.isCorrect, 'header-incorrect': !q.isCorrect}"
            >
                <span class="review-status">
                    {{ index + 1 }}. {{ q.isCorrect ? '✅ Correct' : '❌ Incorrect' }} ({{ q.type }})
                </span>
                <span class="subject-tag">{{ q.content_chunk.substring(0, 50) }}...</span> 
            </div>

            <p class="review-question-text">{{ q.question }}</p>
            
            <div class="review-explanation">
                <p><strong>Correct Answer:</strong> <span class="final-answer-text">{{ q.answer }}</span></p>
                <p><strong>Explanation:</strong> {{ q.explanation }}</p>
            </div>
        </div>
    </div>

    <div class="button-group-footer">
        
        <button 
            @click="getCoachingSuggestion" 
            class="new-quiz-btn hear-suggestion-btn" 
            :disabled="isCoachingLoading || totalQuestions === 0"
        >
            {{ isCoachingLoading ? 'Analyzing...' : '🧠 Hear Suggestion' }}
        </button>

        <button @click="viewAnalytics" class="new-quiz-btn view-analytics-btn">
            View Performance Analytics
        </button>

        <button @click="router.push('/quiz')" class="new-quiz-btn start-new-quiz-btn">
            Start New Quiz
        </button>
    </div>

    <div v-if="coachingText && !isCoachingLoading" class="coaching-message-box">
        <h3>AI Coach Suggestion:</h3>
        <p class="coaching-text">{{ coachingText }}</p>
        <audio controls autoplay>
            <source :src="generateTtsUrl(coachingText)" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    </div>
  </div>
</template>

<style scoped>
.summary-container {
    max-width: 900px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}

.summary-header {
    background-color: #3e3e5a;
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 40px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.summary-header h1 {
    color: #fff;
    text-shadow: 0 0 8px #c990ff;
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.final-score {
    font-size: 2.5rem;
    font-weight: 900;
}

.score-high { color: #2ecc71; } /* Green */
.score-mid { color: #f1c40f; } /* Yellow */
.score-low { color: #e74c3c; } /* Red */

.summary-count {
    color: #c0c0c0;
    font-size: 1.1rem;
}

.review-section {
    text-align: left;
    margin-bottom: 40px;
}

.review-section h2 {
    color: #c990ff;
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.question-review-card {
    background-color: #2a2a44;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.review-header {
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #1a1a2e; 
}

.header-correct {
    background-color: #2ecc71; /* Green header for correct */
}

.header-incorrect {
    background-color: #e74c3c; /* Red header for incorrect */
}

.review-question-text {
    padding: 15px 20px 10px;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e0e0e0;
}

.review-explanation {
    background-color: #3e3e5a;
    padding: 15px 20px;
    border-top: 1px solid #444;
    font-size: 0.95rem;
}

.review-explanation strong {
    color: #f1c40f; /* Highlight explanation labels */
    margin-right: 5px;
}

.final-answer-text {
    font-weight: bold;
    color: #b3e0ff; /* Light blue for answer text */
}

/* --- BUTTON GROUP LAYOUT (NEW) --- */
.button-group-footer {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 20px;
}

/* Base button style (for Start New Quiz) */
.new-quiz-btn {
    flex-grow: 1;
    padding: 12px 20px;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    transition: all 0.15s ease;
}

/* Specific button colors */
.start-new-quiz-btn {
    background-color: #3498db;
    box-shadow: 0 6px 0 #2980b9;
}

.view-analytics-btn {
    background-color: #9b59b6; /* Purple color */
    box-shadow: 0 6px 0 #8e44ad;
}

.hear-suggestion-btn {
    background-color: #f1c40f; /* Yellow/Gold color */
    box-shadow: 0 6px 0 #d39d00;
    color: #1a1a2e; /* Dark text on light background */
}

.new-quiz-btn:active {
    box-shadow: 0 2px 0 var(--shadow-color, #2980b9);
    transform: translateY(4px);
}

.hear-suggestion-btn:active {
    box-shadow: 0 2px 0 #d39d00;
}

.view-analytics-btn:active {
    box-shadow: 0 2px 0 #8e44ad;
}

/* --- COACHING MESSAGE BOX --- */
.coaching-message-box {
    text-align: center;
    background-color: #3e3e5a;
    padding: 25px;
    border-radius: 12px;
    margin-top: 30px;
    box-shadow: 0 0 15px rgba(201, 144, 255, 0.3); /* Soft purple glow */
}

.coaching-message-box h3 {
    color: #c990ff;
    margin-bottom: 15px;
    font-size: 1.4rem;
}

.coaching-text {
    font-style: italic;
    color: #fff;
    margin-bottom: 15px;
}
</style> -->









<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'; 
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

const totalQuestions = computed(() => quizStore.quizQuestions.length);
const correctCount = computed(() => 
    quizStore.quizQuestions.filter(q => q.isCorrect === true).length
);
const finalScorePercentage = computed(() => {
    if (totalQuestions.value === 0) return 0;
    return Math.round((correctCount.value / totalQuestions.value) * 100);
});

// --- STATE FOR MODULE 7 (COACHING) ---
const coachingText = ref('');
const isCoachingLoading = ref(false);
// --------------------------------------

// Redirect away if no quiz data is present
onMounted(() => {
    if (totalQuestions.value === 0) {
        router.push('/quiz');
    }
});

// --- NEW FUNCTION: CLIENT-SIDE TTS IMPLEMENTATION (The Fix) ---
const speakSuggestion = (text: string) => {
    // Check if the browser supports the Web Speech API
    if ('speechSynthesis' in window) {
        // Stop any currently speaking speech
        window.speechSynthesis.cancel();
        
        // Create a new speech utterance
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Start speaking the text
        window.speechSynthesis.speak(utterance);
    } else {
        console.warn("Web Speech API not supported. Displaying text only.");
    }
};

// Function to generate and fetch the coaching text (Module 7)
const getCoachingSuggestion = async () => {
    // Prevent re-run if already loading or if text is generated
    if (isCoachingLoading.value || totalQuestions.value === 0 || coachingText.value.length > 50) return; 
    
    isCoachingLoading.value = true;
    coachingText.value = 'Generating personalized suggestion...'; // Loading state message

    // Data needed for the AI prompt
    const analysisData = {
        quiz_results: quizStore.quizQuestions, 
        total_correct: correctCount.value,
        total_answered: totalQuestions.value,
    };

    try {
        const response = await axios.post(
            'http://localhost:5000/api/coaching/suggest',
            analysisData,
            authStore.authHeader 
        );
        
        const finalCoachingText = response.data.suggestion_text;
        
        coachingText.value = finalCoachingText;
        
        // CRITICAL FIX: Play the text immediately after generation
        speakSuggestion(finalCoachingText); 
        
    } catch (e) {
        coachingText.value = "Sorry, I am unable to generate a coaching session right now. Please check your API key/quota.";
        console.error("Coaching API Failed:", e);
    } finally {
        isCoachingLoading.value = false;
    }
};

// Handler for the existing Analytics button
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};
</script>

<template>
  <div class="summary-container">
    <div class="summary-header">
        <h1>Quiz Complete! 🎉</h1>
        <p class="final-score">Your Score: 
            <span :class="{'score-high': finalScorePercentage >= 70, 'score-low': finalScorePercentage < 40, 'score-mid': finalScorePercentage >= 40 && finalScorePercentage < 70}">
                {{ finalScorePercentage }}%
            </span>
        </p>
        <p class="summary-count">({{ correctCount }} correct out of {{ totalQuestions }} questions)</p>
    </div>

    <div class="review-section">
        <h2>Detailed Review</h2>
        <div v-for="(q, index) in quizStore.quizQuestions" :key="index" class="question-review-card">
            <div 
                class="review-header"
                :class="{'header-correct': q.isCorrect, 'header-incorrect': !q.isCorrect}"
            >
                <span class="review-status">
                    {{ index + 1 }}. {{ q.isCorrect ? '✅ Correct' : '❌ Incorrect' }} ({{ q.type }})
                </span>
                <span class="subject-tag">{{ q.content_chunk.substring(0, 50) }}...</span> 
            </div>

            <p class="review-question-text">{{ q.question }}</p>
            
            <div class="review-explanation">
                <p><strong>Correct Answer:</strong> <span class="final-answer-text">{{ q.answer }}</span></p>
                <p><strong>Explanation:</strong> {{ q.explanation }}</p>
            </div>
        </div>
    </div>

    <div class="button-group-footer">
        
        <button 
            @click="getCoachingSuggestion" 
            class="new-quiz-btn hear-suggestion-btn" 
            :disabled="isCoachingLoading || totalQuestions === 0"
        >
            {{ isCoachingLoading ? 'Analyzing...' : '🧠 Hear Suggestion' }}
        </button>

        <button @click="viewAnalytics" class="new-quiz-btn view-analytics-btn">
            View Performance Analytics
        </button>

        <button @click="router.push('/quiz')" class="new-quiz-btn start-new-quiz-btn">
            Start New Quiz
        </button>
    </div>

    <div v-if="coachingText && !isCoachingLoading" class="coaching-message-box">
        <h3>AI Coach Suggestion:</h3>
        <p class="coaching-text">{{ coachingText }}</p>
        
        <button v-if="coachingText" @click="speakSuggestion(coachingText)" class="new-quiz-btn replay-btn">
            &#9654; Replay Voice Suggestion
            
        </button>
    </div>
  </div>
</template>

<style scoped>
.summary-container {
    max-width: 900px;
    margin: 50px auto;
    color: #ffffff;
    text-align: center;
}

.summary-header {
    background-color: #3e3e5a;
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 40px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.summary-header h1 {
    color: #fff;
    text-shadow: 0 0 8px #c990ff;
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.final-score {
    font-size: 2.5rem;
    font-weight: 900;
}

.score-high { color: #2ecc71; } /* Green */
.score-mid { color: #f1c40f; } /* Yellow */
.score-low { color: #e74c3c; } /* Red */

.summary-count {
    color: #c0c0c0;
    font-size: 1.1rem;
}

.review-section {
    text-align: left;
    margin-bottom: 40px;
}

.review-section h2 {
    color: #c990ff;
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.question-review-card {
    background-color: #2a2a44;
    border-radius: 10px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.review-header {
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #1a1a2e; 
}

.header-correct {
    background-color: #2ecc71; /* Green header for correct */
}

.header-incorrect {
    background-color: #e74c3c; /* Red header for incorrect */
}

.review-question-text {
    padding: 15px 20px 10px;
    font-size: 1.1rem;
    font-weight: 500;
    color: #e0e0e0;
}

.review-explanation {
    background-color: #3e3e5a;
    padding: 15px 20px;
    border-top: 1px solid #444;
    font-size: 0.95rem;
}

.review-explanation strong {
    color: #f1c40f; /* Highlight explanation labels */
    margin-right: 5px;
}

.final-answer-text {
    font-weight: bold;
    color: #b3e0ff; /* Light blue for answer text */
}

/* --- BUTTON GROUP LAYOUT (NEW) --- */
.button-group-footer {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 20px;
}

/* Base button style (for Start New Quiz) */
.new-quiz-btn {
    flex-grow: 1;
    padding: 12px 20px;
    color: rgb(255, 255, 255);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    transition: all 0.15s ease;
}

/* Specific button colors */
.start-new-quiz-btn {
    background-color: #3498db;
    box-shadow: 0 6px 0 #2980b9;
}

.view-analytics-btn {
    background-color: #9b59b6; /* Purple color */
    box-shadow: 0 6px 0 #8e44ad;
}

.hear-suggestion-btn {
    background-color: #f1c40f; /* Yellow/Gold color */
    box-shadow: 0 6px 0 #d39d00;
    color: #1a1a2e; /* Dark text on light background */
}

.new-quiz-btn:active {
    box-shadow: 0 2px 0 var(--shadow-color, #2980b9);
    transform: translateY(4px);
}

.hear-suggestion-btn:active {
    box-shadow: 0 2px 0 #d39d00;
}

.view-analytics-btn:active {
    box-shadow: 0 2px 0 #8e44ad;
}

/* --- COACHING MESSAGE BOX --- */
.coaching-message-box {
    text-align: center;
    background-color: #3e3e5a;
    padding: 25px;
    border-radius: 12px;
    margin-top: 30px;
    box-shadow: 0 0 15px rgba(201, 144, 255, 0.3); /* Soft purple glow */
}

.coaching-message-box h3 {
    color: #c990ff;
    margin-bottom: 15px;
    font-size: 1.4rem;
}

.coaching-text {
    font-style: italic;
    color: #dd00ff;
    margin-bottom: 15px;
}
</style>