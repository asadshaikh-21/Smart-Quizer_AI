<!-- <script setup lang="ts">
import { useQuizStore } from '@/stores/quiz_store';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

onMounted(() => {
    // If the user navigates here directly without configuring, redirect them
    if (!quizStore.quizConfig) {
        router.push('/quiz');
    } else {
        // Start generating the first question when the page loads
        if (quizStore.quizQuestions.length === 0) {
            quizStore.generateNextQuestion();
        }
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <h1>Active Quiz Session</h1>
        <div v-if="!quizStore.isQuizActive">
            <p>Starting quiz or returning to configuration...</p>
        </div>
        <div v-else>
            <p>Loading question {{ quizStore.currentQuestionIndex + 1 }} of {{ quizStore.quizConfig?.numQuestions }}</p>
            
            <div class="question-placeholder">
                <p>Question: {{ quizStore.currentQuestion?.question }}</p>
            </div>
            
            <button @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-btn">Exit Quiz</button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 800px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.question-placeholder {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    margin-top: 20px;
}

.exit-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}
</style> -->




<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; // Wait for selection
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; // Wait for text input
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // Check answer and receive feedback
    const isCorrect = quizStore.submitAnswer(answerToSubmit);
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Getting next question...';
        showExplanation.value = false;
        
        // Wait briefly, then advance to the next question
        setTimeout(async () => {
            await handleAdvance();
        }, 1500);
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
        showExplanation.value = true;
        isProcessing.value = false;
    }
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        // Placeholder redirect for results page
        router.push('/quiz'); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion();

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area">
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default to 2 columns for T/F */
    gap: 15px;
}

/* True/False Specific Styling */
.tf-options {
    grid-template-columns: 1fr 1fr; /* Explicitly set T/F to 2 columns */
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->






<!-- <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; // Wait for selection
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; // Wait for text input
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // Check answer and receive feedback
    const isCorrect = quizStore.submitAnswer(answerToSubmit);
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Getting next question...';
        showExplanation.value = false;
        
        // Wait briefly, then advance to the next question
        setTimeout(async () => {
            await handleAdvance();
        }, 1500);
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
        showExplanation.value = true;
        isProcessing.value = false;
    }
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        // Placeholder redirect for results page
        router.push('/quiz'); 
        return;
    }

    // Attempt to generate the next question
    // Note: In this implementation, the question is generated *after* the previous one is answered.
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area">
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; /* CRITICAL: Allows absolute positioning of the progress bar */
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (NEW) --- */
.score-progress-container {
    position: absolute; 
    top: 0px;
    right: 0px;
    width: 250px; 
    padding: 15px 15px 0 0;
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.5rem;
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 12px;
    background-color: #555; 
    border-radius: 6px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->






<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; // Wait for selection
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; // Wait for text input
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // Check answer and receive feedback
    const isCorrect = quizStore.submitAnswer(answerToSubmit);
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Getting next question...';
        showExplanation.value = false;
        
        // Wait briefly, then advance to the next question
        setTimeout(async () => {
            await handleAdvance();
        }, 1500);
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
        showExplanation.value = true;
        isProcessing.value = false;
    }
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        // Placeholder redirect for results page
        router.push('/quiz'); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion();

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area">
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; /* CRITICAL: Allows absolute positioning of the progress bar */
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    /* FIX: Shifted position left and down */
    top: 5px; 
    right: 20px; 
    width: 180px; /* Reduced width */
    padding: 10px 0 0 0; /* Adjusted padding */
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; /* Reduced size to prevent overlap */
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; /* Reduced height */
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    /* FIX: Added space at the top to clear the progress bar */
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->










<!-- <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const router = useRouter();

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // Check answer and receive feedback
    const isCorrect = quizStore.submitAnswer(answerToSubmit);
    
    // --- START: EXPLANATION FOR ALL ANSWERS FIX ---
    showExplanation.value = true; // CRITICAL: Always show explanation now
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    // --- END: EXPLANATION FOR ALL ANSWERS FIX ---
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        router.push('/quiz'); 
        return;
    }

    // Attempt to generate the next question
    // Note: The move logic is now inside generateNextQuestion() via quizStore
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    /* FIX: Shifted position left and down */
    top: 5px; 
    right: 20px; 
    width: 180px; /* Reduced width */
    padding: 10px 0 0 0; /* Adjusted padding */
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; /* Reduced size to prevent overlap */
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; /* Reduced height */
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    /* FIX: Added space at the top to clear the progress bar */
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->








<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; // <-- NEW IMPORT for logging API call
import { useAuthStore } from '@/stores/auth'; // Ensure AuthStore is imported

// Instantiate the stores
const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); // CRITICAL: Need this to access auth headers for logging

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (which returns logData)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit);
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        // FIX: Use authStore.authHeader for the authentication headers
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log("Answer logged successfully:", logData.is_correct);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        router.push('/quiz'); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->









<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; // For logging API call
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref(''); 
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (which returns logData)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit);
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log("Answer logged successfully:", logData.is_correct);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        // CRITICAL CHANGE: Navigate to the new Results Summary Page
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    // If navigated directly without configuration, redirect
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->











<!-- <script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'; // Added watch
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; // For logging API call
import { useAuthStore } from '@/stores/auth'; // Ensure AuthStore is imported

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref(''); // Used for Fill-up and Short Answer
const selectedOption = ref<string | null>(null); // Used for MCQ and True/False
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- NEW FEATURE 2: TIMER STATE ---
const timerStart = ref(0); 

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Start timer when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now();
    }
}, { immediate: true }); // Start immediately when the component mounts
// ------------------------------------


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    // --- NEW FEATURE 2: CALCULATE TIME ---
    const timeTaken = Date.now() - timerStart.value; // Time in milliseconds
    // ------------------------------------

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (which now returns logData)
    // CRITICAL: Passing timeTaken to the store
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        // Quiz is finished (reached the configured number of questions)
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
        // Timer automatically resets via the watch handler when currentQuestion updates
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->



















<!-- 

<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; // CRITICAL: Added onUnmounted
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null);
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- NEW FEATURE 2: TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); // Time in seconds for display
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now(); // Reset submission start time
    elapsedTime.value = 0; // Reset visual counter
    
    // Start counting up every second
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; // Type casting for clearInterval compatibility
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};
// ------------------------------------


// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); // Start submission timer
        startVisualTimer(); // Start visual timer
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    // --- NEW FEATURE 2: CALCULATE TIME ---
    const timeTaken = Date.now() - timerStart.value; // Time in milliseconds
    // ------------------------------------

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (CRITICAL: Passing timeTaken to the store)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
        // Timer automatically restarts via the watch handler when currentQuestion updates
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats"> 
                    <span class="timer">{{ elapsedTime }}s</span> 
                    <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">End Quiz and Return to Config</button>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

/* NEW: Style for the header stats container */
.header-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; /* Orange/Yellow for time */
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}
</style> -->















<!-- 
<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; // All necessary imports from vue
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- NEW FEATURE 2: TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); // Time in seconds for display
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now(); // Reset submission start time
    elapsedTime.value = 0; // Reset visual counter
    
    // Start counting up every second
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; 
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};
// ------------------------------------


// --- Computed Properties (Restored) ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); // Start submission timer
        startVisualTimer(); // Start visual timer
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    // --- NEW FEATURE 2: CALCULATE TIME ---
    const timeTaken = Date.now() - timerStart.value; // Time in milliseconds
    // ------------------------------------

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (passing timeTaken)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
        // Timer automatically restarts via the watch handler when currentQuestion updates
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- NEW NAVIGATION HANDLER (Backward Button Logic) ---
const goToPreviousQuestion = () => {
    // Only allow navigation if we are not at the first question
    if (quizStore.currentQuestionIndex > 0) {
        stopVisualTimer();
        // Move to the previous question object in the quizQuestions array
        quizStore.moveToPreviousQuestion();
        
        // Ensure the answer state for the previous question is displayed
        showExplanation.value = true;
        
        // Clear local inputs but keep the feedback based on the stored result
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = `Reviewing Question ${quizStore.currentQuestionIndex + 1}`;
    }
};


// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats"> 
                    <span class="timer">{{ elapsedTime }}s</span> 
                    <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="navigation-footer">
            <button 
                v-if="quizStore.currentQuestionIndex > 0 && !isProcessing" 
                @click="goToPreviousQuestion" 
                class="nav-arrow-btn prev-btn"
            >
                &#9664; Previous Question
            </button>
            
            <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">
                End Quiz and Return to Config
            </button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

/* NEW: Style for the header stats container */
.header-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; /* Orange/Yellow for time */
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}

/* --- NEW NAVIGATION FOOTER STYLES --- */
.navigation-footer {
    display: flex;
    justify-content: space-between; /* Space out the two buttons */
    align-items: center;
    margin-top: 30px;
}

.nav-arrow-btn {
    padding: 10px 20px;
    background-color: #3498db; /* Blue color for navigation */
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.15s ease;
    
    /* 3D EFFECT */
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.nav-arrow-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}
</style> -->









<!-- 
<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; 
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); 
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now();
    elapsedTime.value = 0; 
    
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; 
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};

// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); 
        startVisualTimer(); 
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    const timeTaken = Date.now() - timerStart.value; 

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (passing timeTaken)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
        // Timer automatically restarts via the watch handler when currentQuestion updates
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- NEW NAVIGATION HANDLER (Backward Button Logic) ---
const goToPreviousQuestion = () => {
    // Only allow navigation if we are not at the first question
    if (quizStore.currentQuestionIndex > 0) {
        stopVisualTimer();
        quizStore.moveToPreviousQuestion();
        
        // Ensure the answer state for the previous question is displayed
        showExplanation.value = true;
        
        // Clear local inputs but keep the feedback based on the stored result
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = `Reviewing Question ${quizStore.currentQuestionIndex + 1}`;
    }
};


// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats"> 
                    <span class="timer">{{ elapsedTime }}s</span> 
                    <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="navigation-footer">
            <button 
                v-if="quizStore.currentQuestionIndex > 0 && !isProcessing" 
                @click="goToPreviousQuestion" 
                class="nav-arrow-btn prev-btn"
            >
                &#9664; Previous Question
            </button>
            
            <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">
                End Quiz and Return to Config
            </button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

/* NEW: Style for the header stats container */
.header-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; /* Orange/Yellow for time */
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}

/* --- NEW NAVIGATION FOOTER STYLES --- */
.navigation-footer {
    display: flex;
    justify-content: space-between; /* Space out the two buttons */
    align-items: center;
    margin-top: 30px;
}

.nav-arrow-btn {
    padding: 10px 20px;
    background-color: #3498db; /* Blue color for navigation */
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.15s ease;
    
    /* 3D EFFECT */
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.nav-arrow-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}
</style> -->








<!-- 



<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; 
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); // Time in seconds for display
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now();
    elapsedTime.value = 0; 
    
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; 
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};
// ------------------------------------


// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); 
        startVisualTimer(); 
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    const timeTaken = Date.now() - timerStart.value; 

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (passing timeTaken)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- NEW NAVIGATION HANDLER (Backward Button Logic) ---
const goToPreviousQuestion = () => {
    // Only allow navigation if we are not at the first question
    if (quizStore.currentQuestionIndex > 0) {
        stopVisualTimer();
        quizStore.moveToPreviousQuestion();
        
        // Ensure the answer state for the previous question is displayed
        showExplanation.value = true;
        
        // Clear local inputs but keep the feedback based on the stored result
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = `Reviewing Question ${quizStore.currentQuestionIndex + 1}`;
    }
};

// --- NEW HANDLER FOR MODULE 6 FEEDBACK ---
const flagQuestion = async () => {
    if (!currentQuestion.value) return;

    const reason = prompt("Please briefly state why you are flagging this question (e.g., inaccurate answer, inappropriate content):");

    if (!reason) return; 

    try {
        await axios.post(
            'http://localhost:5000/api/feedback/flag', // Route 13
            {
                question_id: currentQuestion.value.content_id, // The ID of the content chunk
                reason: reason // The user's input reason
            },
            authStore.authHeader
        );
        alert("Thank you. The question has been flagged for administrator review.");
    } catch (e) {
        alert("Failed to flag question. Please try again later.");
        console.error("Flagging failed:", e);
    }
};


// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats"> 
                    <span class="timer">{{ elapsedTime }}s</span> 
                    <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
                
                <button 
                    @click="flagQuestion" 
                    :disabled="isProcessing || showExplanation"
                    class="flag-btn"
                >
                    ⚠️ Flag Question for Review
                </button>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="navigation-footer">
            <button 
                v-if="quizStore.currentQuestionIndex > 0 && !isProcessing" 
                @click="goToPreviousQuestion" 
                class="nav-arrow-btn prev-btn"
            >
                &#9664; Previous Question
            </button>
            
            <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">
                End Quiz and Return to Config
            </button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

/* NEW: Style for the header stats container */
.header-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; /* Orange/Yellow for time */
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}

/* --- NEW NAVIGATION FOOTER STYLES --- */
.navigation-footer {
    display: flex;
    justify-content: space-between; /* Space out the two buttons */
    align-items: center;
    margin-top: 30px;
}

.nav-arrow-btn {
    padding: 10px 20px;
    background-color: #3498db; /* Blue color for navigation */
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.15s ease;
    
    /* 3D EFFECT */
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.nav-arrow-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}

/* --- FLAG BUTTON STYLING --- */
.flag-btn {
    background-color: #8e44ad; /* Purple */
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 8px 15px;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 0 3px 0 #6c3483;
    transition: all 0.1s ease;
    margin-top: 15px;
    display: block;
    width: fit-content;
}

.flag-btn:active {
    box-shadow: 0 1px 0 #6c3483;
    transform: translateY(2px);
}
</style> -->





////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
















<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; // CRITICAL: onUnmounted added
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); // Time in seconds for display
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now(); // Reset submission start time
    elapsedTime.value = 0; // Reset visual counter
    
    // Start counting up every second
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; 
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};
// ------------------------------------


// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); 
        startVisualTimer(); 
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    // --- NEW FEATURE 2: CALCULATE TIME ---
    const timeTaken = Date.now() - timerStart.value; // Time in milliseconds
    // ------------------------------------

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (passing timeTaken)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
        // Timer automatically restarts via the watch handler when currentQuestion updates
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- NEW NAVIGATION HANDLER (Backward Button Logic) ---
const goToPreviousQuestion = () => {
    // Only allow navigation if we are not at the first question
    if (quizStore.currentQuestionIndex > 0) {
        stopVisualTimer();
        quizStore.moveToPreviousQuestion();
        
        // Ensure the answer state for the previous question is displayed
        showExplanation.value = true;
        
        // Clear local inputs but keep the feedback based on the stored result
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = `Reviewing Question ${quizStore.currentQuestionIndex + 1}`;
    }
};

// --- NEW HANDLER FOR MODULE 6 FEEDBACK ---
const flagQuestion = async () => {
    if (!currentQuestion.value) return;

    const reason = prompt("Please briefly state why you are flagging this question (e.g., inaccurate answer, inappropriate content):");

    if (!reason) return; 

    try {
        await axios.post(
            'http://localhost:5000/api/feedback/flag', // Route 13
            {
                question_id: currentQuestion.value.content_id, // The ID of the content chunk
                reason: reason // The user's input reason
            },
            authStore.authHeader
        );
        alert("Thank you. The question has been flagged for administrator review.");
    } catch (e) {
        alert("Failed to flag question. Please try again later.");
        console.error("Flagging failed:", e);
    }
};


// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    // Start question generation if the quiz is not already loaded
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats"> 
                    <span class="timer">{{ elapsedTime }}s</span> 
                    <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                <p class="question-text">{{ currentQuestion.question }}</p>
                
                <button 
                    @click="flagQuestion" 
                    :disabled="isProcessing || showExplanation"
                    class="flag-btn"
                >
                    ⚠️ Flag Question for Review
                </button>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="navigation-footer">
            <button 
                v-if="quizStore.currentQuestionIndex > 0 && !isProcessing" 
                @click="goToPreviousQuestion" 
                class="nav-arrow-btn prev-btn"
            >
                &#9664; Previous Question
            </button>
            
            <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">
                End Quiz and Return to Config
            </button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: #fff;
    text-align: center;
}

.quiz-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
}

.loading-state h1 {
    color: #c990ff;
    text-shadow: 0 0 5px #82aaff;
}

/* --- DYNAMIC PROGRESS BAR STYLING (FIXED POSITION) --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f;
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: #555; 
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}

/* --- Color Change Logic (using attribute selector for simplicity) --- */
/* High Score (70%+) */
.progress-fill[data-score^="7"], 
.progress-fill[data-score^="8"], 
.progress-fill[data-score^="9"],
.progress-fill[data-score="100"] {
    background-color: #2ecc71; /* Green */
}

/* Low Score (0%-30%) */
.progress-fill[data-score^="0"],
.progress-fill[data-score^="1"],
.progress-fill[data-score^="2"],
.progress-fill[data-score^="30"] {
    background-color: #e74c3c; /* Red */
}
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}

.quiz-header h2 {
    color: #fff;
    font-size: 1.5rem;
}

/* NEW: Style for the header stats container */
.header-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; /* Orange/Yellow for time */
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: #5d496a;
    color: #fff;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Default for T/F */
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: #3e3e5a;
    border: 2px solid transparent;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 #333;
}

.option-btn:hover:not(:disabled) {
    background-color: #4c4c70;
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important;
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #3e3e5a;
    color: #fff;
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: #2ecc71;
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: #e74c3c;
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #444;
    text-align: left;
    color: #ccc;
}

.explanation-area strong {
    color: #fff;
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

.next-question-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #d39d00;
    transition: all 0.15s ease;
}

.exit-quiz-btn {
    margin-top: 30px;
    padding: 10px 20px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 0 #c0392b;
}

/* --- NEW NAVIGATION FOOTER STYLES --- */
.navigation-footer {
    display: flex;
    justify-content: space-between; /* Space out the two buttons */
    align-items: center;
    margin-top: 30px;
}

.nav-arrow-btn {
    padding: 10px 20px;
    background-color: #3498db; /* Blue color for navigation */
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    font-size: 1rem;
    transition: all 0.15s ease;
    
    /* 3D EFFECT */
    box-shadow: 0 4px 0 #2980b9; 
    transform: translateY(0);
}

.nav-arrow-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(3px);
}

/* --- FLAG BUTTON STYLING --- */
.flag-btn {
    background-color: #8e44ad; /* Purple */
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 8px 15px;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 0 3px 0 #6c3483;
    transition: all 0.1s ease;
    margin-top: 15px;
    display: block;
    width: fit-content;
}

.flag-btn:active {
    box-shadow: 0 1px 0 #6c3483;
    transform: translateY(2px);
}
</style>