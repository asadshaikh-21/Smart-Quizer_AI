// D:\SmartQuizzer\frontend\vue-project\src\stores\quiz_store.ts (Updated for Configuration)

// import { ref } from 'vue';
// import { defineStore } from 'pinia';
// import axios from 'axios';
// import { useAuthStore } from './auth';

// const API_BASE_URL = 'http://localhost:5000/api';

// // Define the shape of a generated question (Now supports all types)
// interface QuizQuestion {
//     type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
//     question: string;
//     options?: string[]; // Only present for MCQ
//     answer: string;
//     explanation: string;
//     content_chunk: string;
//     isCorrect?: boolean;
// }

// // Define the overall quiz configuration
// interface QuizConfig {
//     contentId: string;
//     numQuestions: number;
//     generatedCount: number;
//     questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
// }

// export const useQuizStore = defineStore('quiz', () => {
//     const authStore = useAuthStore();
    
//     // State
//     const quizConfig = ref<QuizConfig | null>(null);
//     const isQuizActive = ref(false);
//     const currentQuestion = ref<QuizQuestion | null>(null);
//     const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
//     const currentQuestionIndex = ref(0);
    
//     // Action to set configuration (called from QuizConfigView)
//     function setConfig(contentId: string, numQuestions: number) {
//         // Set the question types mix (e.g., 25% of each type for a simple implementation)
//         const types: QuizConfig['questionTypes'] = [];
//         const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
//         const numPerType = Math.ceil(numQuestions / 4);

//         for (let i = 0; i < numQuestions; i++) {
//             types.push(typesBase[i % 4] as QuizConfig['questionTypes'][number]);
//         }
        
//         quizConfig.value = {
//             contentId: contentId,
//             numQuestions: numQuestions,
//             generatedCount: 0,
//             questionTypes: types,
//         };
        
//         quizQuestions.value = [];
//         currentQuestionIndex.value = 0;
//         currentQuestion.value = null;
//     }

//     // Main action to generate the next question
//     async function generateNextQuestion(): Promise<boolean> {
//         if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
//             console.log("Quiz generation complete.");
//             return false;
//         }

//         const contentId = quizConfig.value.contentId;
//         const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
//         // Get the specific question type required for the next generation slot
//         const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
//         try {
//             // Call the backend API with the required Content ID and Question Type
//             const response = await axios.post(
//                 `${API_BASE_URL}/quiz/generate/${contentId}`,
//                 {
//                     question_type: questionType,
//                     difficulty: difficulty
//                 },
//                 authStore.authHeader 
//             );

//             const newQuestion = response.data as QuizQuestion;
//             newQuestion.isCorrect = undefined; // Initialize state
            
//             // Add to the list of generated questions
//             quizQuestions.value.push(newQuestion);
//             quizConfig.value.generatedCount += 1;
            
//             // If this is the first question, start the quiz immediately
//             if (quizConfig.value.generatedCount === 1) {
//                 isQuizActive.value = true;
//             }
            
//             // Set the current question to the newly generated one
//             currentQuestion.value = newQuestion;
//             currentQuestionIndex.value = quizQuestions.value.length - 1;
            
//             return true;

//         } catch (error: any) {
//             console.error("Error generating question:", error.response || error);
//             // On API key failure or content exhaustion, stop generation
//             return false; 
//         }
//     }
    
//     // Action to move to the next question in the pre-generated array
//     function moveToNextQuestion() {
//         if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
//             currentQuestionIndex.value += 1;
//             currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
//             return true;
//         }
//         return false;
//     }

//     function endQuiz() {
//         isQuizActive.value = false;
//         quizConfig.value = null;
//         currentQuestion.value = null;
//         // Optionally navigate to a results page here
//     }
    
//     return {
//         quizConfig,
//         isQuizActive,
//         currentQuestion,
//         quizQuestions,
//         currentQuestionIndex,
//         setConfig,
//         generateNextQuestion,
//         moveToNextQuestion,
//         endQuiz,
//     };
// });





// import { ref } from 'vue';
// import { defineStore } from 'pinia';
// import axios from 'axios';
// import { useAuthStore } from './auth';

// const API_BASE_URL = 'http://localhost:5000/api';

// // Define the shape of a generated question (Now supports all types)
// interface QuizQuestion {
//     type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
//     question: string;
//     options?: string[]; // Only present for MCQ
//     answer: string;
//     explanation: string;
//     content_chunk: string;
//     isCorrect?: boolean;
// }

// // Define the overall quiz configuration
// interface QuizConfig {
//     contentId: string;
//     numQuestions: number;
//     generatedCount: number;
//     questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
// }

// export const useQuizStore = defineStore('quiz', () => {
//     const authStore = useAuthStore();
    
//     // State
//     const quizConfig = ref<QuizConfig | null>(null);
//     const isQuizActive = ref(false);
//     const currentQuestion = ref<QuizQuestion | null>(null);
//     const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
//     const currentQuestionIndex = ref(0);
    
//     // Action to set configuration (called from QuizConfigView)
//     function setConfig(contentId: string, numQuestions: number) {
//         // Set the question types mix (e.g., 25% of each type for a simple implementation)
//         const types: QuizConfig['questionTypes'] = [];
//         const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
        
//         // Simple round-robin assignment to ensure even distribution
//         for (let i = 0; i < numQuestions; i++) {
//             types.push(typesBase[i % typesBase.length] as QuizConfig['questionTypes'][number]);
//         }
        
//         quizConfig.value = {
//             contentId: contentId,
//             numQuestions: numQuestions,
//             generatedCount: 0,
//             questionTypes: types,
//         };
        
//         quizQuestions.value = [];
//         currentQuestionIndex.value = 0;
//         currentQuestion.value = null;
//     }

//     // Main action to generate the next question
//     async function generateNextQuestion(): Promise<boolean> {
//         if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
//             console.log("Quiz generation complete.");
//             return false;
//         }

//         const contentId = quizConfig.value.contentId;
//         const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
//         // Get the specific question type required for the next generation slot
//         const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
//         try {
//             // Call the backend API with the required Content ID and Question Type
//             const response = await axios.post(
//                 `${API_BASE_URL}/quiz/generate/${contentId}`,
//                 {
//                     question_type: questionType,
//                     difficulty: difficulty
//                 },
//                 authStore.authHeader 
//             );

//             const newQuestion = response.data as QuizQuestion;
//             newQuestion.isCorrect = undefined; // Initialize state
            
//             // Add to the list of generated questions
//             quizQuestions.value.push(newQuestion);
//             quizConfig.value.generatedCount += 1;
            
//             // If this is the first question, start the quiz immediately
//             if (quizConfig.value.generatedCount === 1) {
//                 isQuizActive.value = true;
//             }
            
//             // Set the current question to the newly generated one
//             currentQuestion.value = newQuestion;
//             currentQuestionIndex.value = quizQuestions.value.length - 1;
            
//             return true;

//         } catch (error: any) {
//             console.error("Error generating question:", error.response || error);
//             // On API key failure or content exhaustion, stop generation
//             return false; 
//         }
//     }
    
//     // Action to move to the next question in the pre-generated array
//     function moveToNextQuestion() {
//         if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
//             currentQuestionIndex.value += 1;
//             currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
//             return true;
//         }
//         return false;
//     }

//     // --- Action to submit the user's answer (The newly added logic) ---
//     function submitAnswer(selectedResponse: string) {
//         if (!currentQuestion.value) return false;
        
//         // 1. Normalize the correct answer and user input for comparison
//         const submitted = selectedResponse.trim().toLowerCase();
//         const correct = currentQuestion.value.answer.trim().toLowerCase();

//         // 2. Determine if the answer is correct
//         const isCorrect = submitted === correct;
        
//         // 3. Log the result back into the current question object
//         currentQuestion.value.isCorrect = isCorrect; 
        
//         // In a real adaptive app, this is where we would call a backend route to log performance for ML.
        
//         return isCorrect;
//     }
    
//     function endQuiz() {
//         isQuizActive.value = false;
//         quizConfig.value = null;
//         currentQuestion.value = null;
//         // Optionally navigate to a results page here
//     }
    
//     return {
//         quizConfig,
//         isQuizActive,
//         currentQuestion,
//         quizQuestions,
//         currentQuestionIndex,
//         setConfig,
//         generateNextQuestion,
//         moveToNextQuestion,
//         submitAnswer, // <-- CRITICAL: Now correctly returned
//         endQuiz,
//     };
// });








// import { ref, computed } from 'vue'; // <-- Ensure 'computed' is imported
// import { defineStore } from 'pinia';
// import axios from 'axios';
// import { useAuthStore } from './auth';

// const API_BASE_URL = 'http://localhost:5000/api';

// // Define the shape of a generated question (Now supports all types)
// interface QuizQuestion {
//     type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
//     question: string;
//     options?: string[]; // Only present for MCQ
//     answer: string;
//     explanation: string;
//     content_chunk: string;
//     isCorrect?: boolean;
// }

// // Define the overall quiz configuration
// interface QuizConfig {
//     contentId: string;
//     numQuestions: number;
//     generatedCount: number;
//     questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
// }

// export const useQuizStore = defineStore('quiz', () => {
//     const authStore = useAuthStore();
    
//     // State
//     const quizConfig = ref<QuizConfig | null>(null);
//     const isQuizActive = ref(false);
//     const currentQuestion = ref<QuizQuestion | null>(null);
//     const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
//     const currentQuestionIndex = ref(0);
    
//     // Action to set configuration (called from QuizConfigView)
//     function setConfig(contentId: string, numQuestions: number) {
//         // Set the question types mix (e.g., 25% of each type for a simple implementation)
//         const types: QuizConfig['questionTypes'] = [];
//         const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
        
//         // Simple round-robin assignment to ensure even distribution
//         for (let i = 0; i < numQuestions; i++) {
//             types.push(typesBase[i % typesBase.length] as QuizConfig['questionTypes'][number]);
//         }
        
//         quizConfig.value = {
//             contentId: contentId,
//             numQuestions: numQuestions,
//             generatedCount: 0,
//             questionTypes: types,
//         };
        
//         quizQuestions.value = [];
//         currentQuestionIndex.value = 0;
//         currentQuestion.value = null;
//     }

//     // Main action to generate the next question
//     async function generateNextQuestion(): Promise<boolean> {
//         if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
//             console.log("Quiz generation complete.");
//             return false;
//         }

//         const contentId = quizConfig.value.contentId;
//         const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
//         // Get the specific question type required for the next generation slot
//         const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
//         try {
//             // Call the backend API with the required Content ID and Question Type
//             const response = await axios.post(
//                 `${API_BASE_URL}/quiz/generate/${contentId}`,
//                 {
//                     question_type: questionType,
//                     difficulty: difficulty
//                 },
//                 authStore.authHeader 
//             );

//             const newQuestion = response.data as QuizQuestion;
//             newQuestion.isCorrect = undefined; // Initialize state
            
//             // Add to the list of generated questions
//             quizQuestions.value.push(newQuestion);
//             quizConfig.value.generatedCount += 1;
            
//             // If this is the first question, start the quiz immediately
//             if (quizConfig.value.generatedCount === 1) {
//                 isQuizActive.value = true;
//             }
            
//             // Set the current question to the newly generated one
//             currentQuestion.value = newQuestion;
//             currentQuestionIndex.value = quizQuestions.value.length - 1;
            
//             return true;

//         } catch (error: any) {
//             console.error("Error generating question:", error.response || error);
//             // On API key failure or content exhaustion, stop generation
//             return false; 
//         }
//     }
    
//     // Action to move to the next question in the pre-generated array
//     function moveToNextQuestion() {
//         if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
//             currentQuestionIndex.value += 1;
//             currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
//             return true;
//         }
//         return false;
//     }

//     // --- Action to submit the user's answer ---
//     function submitAnswer(selectedResponse: string) {
//         if (!currentQuestion.value) return false;
        
//         // 1. Normalize the correct answer and user input for comparison
//         const submitted = selectedResponse.trim().toLowerCase();
//         const correct = currentQuestion.value.answer.trim().toLowerCase();

//         // 2. Determine if the answer is correct
//         const isCorrect = submitted === correct;
        
//         // 3. Log the result back into the current question object
//         currentQuestion.value.isCorrect = isCorrect; 
        
//         // In a full adaptive app, this is where we would call a backend route to log performance for ML.
        
//         return isCorrect;
//     }
    
//     function endQuiz() {
//         isQuizActive.value = false;
//         quizConfig.value = null;
//         currentQuestion.value = null;
//         // Optionally navigate to a results page here
//     }
    
//     // --- NEW GETTER: Calculates the live score percentage ---
//     const currentScorePercentage = computed(() => {
//         if (quizQuestions.value.length === 0) return 0;
        
//         // Filter questions that have been answered (where isCorrect is defined)
//         const answeredQuestions = quizQuestions.value.filter(q => q.isCorrect !== undefined);
        
//         if (answeredQuestions.length === 0) return 0;

//         const correctCount = answeredQuestions.filter(q => q.isCorrect === true).length;
        
//         // Calculate and round the percentage
//         return Math.round((correctCount / answeredQuestions.length) * 100);
//     });

//     return {
//         quizConfig,
//         isQuizActive,
//         currentQuestion,
//         quizQuestions,
//         currentQuestionIndex,
//         setConfig,
//         generateNextQuestion,
//         moveToNextQuestion,
//         submitAnswer,
//         endQuiz,
//         currentScorePercentage, // <-- NEW GETTER EXPORTED
//     };
// });







// import { ref, computed } from 'vue'; // <-- Ensure 'computed' is imported
// import { defineStore } from 'pinia';
// import axios from 'axios';
// import { useAuthStore } from './auth';

// const API_BASE_URL = 'http://localhost:5000/api';

// // Define the shape of a generated question (Now supports all types)
// interface QuizQuestion {
//     type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
//     question: string;
//     options?: string[]; // Only present for MCQ
//     answer: string;
//     explanation: string;
//     content_chunk: string;
//     isCorrect?: boolean;
// }

// // Define the overall quiz configuration
// interface QuizConfig {
//     contentId: string;
//     numQuestions: number;
//     generatedCount: number;
//     questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
// }

// export const useQuizStore = defineStore('quiz', () => {
//     const authStore = useAuthStore();
    
//     // State
//     const quizConfig = ref<QuizConfig | null>(null);
//     const isQuizActive = ref(false);
//     const currentQuestion = ref<QuizQuestion | null>(null);
//     const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
//     const currentQuestionIndex = ref(0);
    
//     // Action to set configuration (called from QuizConfigView)
//     function setConfig(contentId: string, numQuestions: number) {
//         // Set the question types mix (e.g., 25% of each type for a simple implementation)
//         const types: QuizConfig['questionTypes'] = [];
//         const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
        
//         // Simple round-robin assignment to ensure even distribution
//         for (let i = 0; i < numQuestions; i++) {
//             types.push(typesBase[i % typesBase.length] as QuizConfig['questionTypes'][number]);
//         }
        
//         quizConfig.value = {
//             contentId: contentId,
//             numQuestions: numQuestions,
//             generatedCount: 0,
//             questionTypes: types,
//         };
        
//         quizQuestions.value = [];
//         currentQuestionIndex.value = 0;
//         currentQuestion.value = null;
//     }

//     // Main action to generate the next question
//     async function generateNextQuestion(): Promise<boolean> {
//         if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
//             console.log("Quiz generation complete.");
//             return false;
//         }

//         const contentId = quizConfig.value.contentId;
//         const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
//         // Get the specific question type required for the next generation slot
//         const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
//         try {
//             // Call the backend API with the required Content ID and Question Type
//             const response = await axios.post(
//                 `${API_BASE_URL}/quiz/generate/${contentId}`,
//                 {
//                     question_type: questionType,
//                     difficulty: difficulty
//                 },
//                 authStore.authHeader 
//             );

//             const newQuestion = response.data as QuizQuestion;
//             newQuestion.isCorrect = undefined; // Initialize state
            
//             // Add to the list of generated questions
//             quizQuestions.value.push(newQuestion);
//             quizConfig.value.generatedCount += 1;
            
//             // If this is the first question, start the quiz immediately
//             if (quizConfig.value.generatedCount === 1) {
//                 isQuizActive.value = true;
//             }
            
//             // Set the current question to the newly generated one
//             currentQuestion.value = newQuestion;
//             currentQuestionIndex.value = quizQuestions.value.length - 1;
            
//             return true;

//         } catch (error: any) {
//             console.error("Error generating question:", error.response || error);
//             // On API key failure or content exhaustion, stop generation
//             return false; 
//         }
//     }
    
//     // Action to move to the next question in the pre-generated array
//     function moveToNextQuestion() {
//         if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
//             currentQuestionIndex.value += 1;
//             currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
//             return true;
//         }
//         return false;
//     }

//     // --- Action to submit the user's answer (UPDATED FOR LOGGING) ---
//     function submitAnswer(selectedResponse: string) {
//         if (!currentQuestion.value || !quizConfig.value) return { isCorrect: false, logData: null };
        
//         // 1. Determine if the answer is correct
//         const submitted = selectedResponse.trim().toLowerCase();
//         const correct = currentQuestion.value.answer.trim().toLowerCase();
//         const isCorrect = submitted === correct;
        
//         // 2. Log the result back into the current question object
//         currentQuestion.value.isCorrect = isCorrect; 
        
//         // 3. Prepare data for backend logging (Module 4)
//         const logData = {
//             content_id: quizConfig.value.contentId,
//             content_chunk: currentQuestion.value.content_chunk,
//             is_correct: isCorrect, // Boolean value
//             question_type: currentQuestion.value.type,
//         };
        
//         // Function now returns the result and the data object
//         return { isCorrect, logData };
//     }
    
//     function endQuiz() {
//         isQuizActive.value = false;
//         quizConfig.value = null;
//         currentQuestion.value = null;
//         // Optionally navigate to a results page here
//     }
    
//     // --- GETTER: Calculates the live score percentage (Progress Bar) ---
//     const currentScorePercentage = computed(() => {
//         if (quizQuestions.value.length === 0) return 0;
        
//         // Filter questions that have been answered (where isCorrect is defined)
//         const answeredQuestions = quizQuestions.value.filter(q => q.isCorrect !== undefined);
        
//         if (answeredQuestions.length === 0) return 0;

//         const correctCount = answeredQuestions.filter(q => q.isCorrect === true).length;
        
//         // Calculate and round the percentage
//         return Math.round((correctCount / answeredQuestions.length) * 100);
//     });

//     return {
//         quizConfig,
//         isQuizActive,
//         currentQuestion,
//         quizQuestions,
//         currentQuestionIndex,
//         setConfig,
//         generateNextQuestion,
//         moveToNextQuestion,
//         submitAnswer, // Function now returns { isCorrect, logData }
//         endQuiz,
//         currentScorePercentage,
//     };
// });







// import { ref, computed } from 'vue'; 
// import { defineStore } from 'pinia';
// import axios from 'axios';
// import { useAuthStore } from './auth';

// const API_BASE_URL = 'http://localhost:5000/api';

// // Define the shape of a generated question (Now supports all types)
// interface QuizQuestion {
//     type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
//     question: string;
//     options?: string[]; // Only present for MCQ
//     answer: string;
//     explanation: string;
//     content_chunk: string;
//     isCorrect?: boolean;
// }

// // Define the overall quiz configuration
// interface QuizConfig {
//     contentId: string;
//     numQuestions: number;
//     generatedCount: number;
//     questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
// }

// export const useQuizStore = defineStore('quiz', () => {
//     const authStore = useAuthStore();
    
//     // State
//     const quizConfig = ref<QuizConfig | null>(null);
//     const isQuizActive = ref(false);
//     const currentQuestion = ref<QuizQuestion | null>(null);
//     const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
//     const currentQuestionIndex = ref(0);
    
//     // Action to set configuration (called from QuizConfigView)
//     function setConfig(contentId: string, numQuestions: number) {
//         // Set the question types mix (e.g., 25% of each type for a simple implementation)
//         const types: QuizConfig['questionTypes'] = [];
//         const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
        
//         // Simple round-robin assignment to ensure even distribution
//         for (let i = 0; i < numQuestions; i++) {
//             types.push(typesBase[i % typesBase.length] as QuizConfig['questionTypes'][number]);
//         }
        
//         quizConfig.value = {
//             contentId: contentId,
//             numQuestions: numQuestions,
//             generatedCount: 0,
//             questionTypes: types,
//         };
        
//         quizQuestions.value = [];
//         currentQuestionIndex.value = 0;
//         currentQuestion.value = null;
//     }

//     // Main action to generate the next question
//     async function generateNextQuestion(): Promise<boolean> {
//         if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
//             console.log("Quiz generation complete.");
//             return false;
//         }

//         const contentId = quizConfig.value.contentId;
//         const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
//         // Get the specific question type required for the next generation slot
//         const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
//         try {
//             // Call the backend API with the required Content ID and Question Type
//             const response = await axios.post(
//                 `${API_BASE_URL}/quiz/generate/${contentId}`,
//                 {
//                     question_type: questionType,
//                     difficulty: difficulty
//                 },
//                 authStore.authHeader 
//             );

//             const newQuestion = response.data as QuizQuestion;
//             newQuestion.isCorrect = undefined; // Initialize state
            
//             // Add to the list of generated questions
//             quizQuestions.value.push(newQuestion);
//             quizConfig.value.generatedCount += 1;
            
//             // If this is the first question, start the quiz immediately
//             if (quizConfig.value.generatedCount === 1) {
//                 isQuizActive.value = true;
//             }
            
//             // Set the current question to the newly generated one
//             currentQuestion.value = newQuestion;
//             currentQuestionIndex.value = quizQuestions.value.length - 1;
            
//             return true;

//         } catch (error: any) {
//             console.error("Error generating question:", error.response || error);
//             // On API key failure or content exhaustion, stop generation
//             return false; 
//         }
//     }
    
//     // Action to move to the next question in the pre-generated array
//     function moveToNextQuestion() {
//         if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
//             currentQuestionIndex.value += 1;
//             currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
//             return true;
//         }
//         return false;
//     }

//     // --- Action to submit the user's answer (FINAL LOGGING DATA RETURN) ---
//     function submitAnswer(selectedResponse: string, timeTaken: number) { // <-- TIME TAKEN ACCEPTED
//         if (!currentQuestion.value || !quizConfig.value) return { isCorrect: false, logData: null };
        
//         // 1. Determine if the answer is correct
//         const submitted = selectedResponse.trim().toLowerCase();
//         const correct = currentQuestion.value.answer.trim().toLowerCase();
//         const isCorrect = submitted === correct;
        
//         // 2. Log the result back into the current question object
//         currentQuestion.value.isCorrect = isCorrect; 
        
//         // 3. Prepare data for backend logging (Module 4)
//         const logData = {
//             content_id: quizConfig.value.contentId,
//             content_chunk: currentQuestion.value.content_chunk,
//             is_correct: isCorrect,
//             question_type: currentQuestion.value.type,
//             time_taken_ms: timeTaken, // <-- NEW DATA POINT SAVED
//         };
        
//         return { isCorrect, logData };
//     }
    
//     function endQuiz() {
//         isQuizActive.value = false;
//         quizConfig.value = null;
//         currentQuestion.value = null;
//         // Optionally navigate to a results page here
//     }
    
//     // --- GETTER: Calculates the live score percentage (Progress Bar) ---
//     const currentScorePercentage = computed(() => {
//         if (quizQuestions.value.length === 0) return 0;
        
//         // Filter questions that have been answered (where isCorrect is defined)
//         const answeredQuestions = quizQuestions.value.filter(q => q.isCorrect !== undefined);
        
//         if (answeredQuestions.length === 0) return 0;

//         const correctCount = answeredQuestions.filter(q => q.isCorrect === true).length;
        
//         // Calculate and round the percentage
//         return Math.round((correctCount / answeredQuestions.length) * 100);
//     });

//     return {
//         quizConfig,
//         isQuizActive,
//         currentQuestion,
//         quizQuestions,
//         currentQuestionIndex,
//         setConfig,
//         generateNextQuestion,
//         moveToNextQuestion,
//         submitAnswer, // Function now returns { isCorrect, logData }
//         endQuiz,
//         currentScorePercentage,
//     };
// });







import { ref, computed } from 'vue'; 
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthStore } from './auth';

const API_BASE_URL = 'http://localhost:5000/api';

// Define the shape of a generated question (Now supports all types)
interface QuizQuestion {
    type: "MCQ" | "True/False" | "Fill-up" | "Short Answer";
    question: string;
    options?: string[]; // Only present for MCQ
    answer: string;
    explanation: string;
    content_chunk: string;
    content_id: string;
    isCorrect?: boolean;
}

// Define the overall quiz configuration
interface QuizConfig {
    contentId: string;
    numQuestions: number;
    generatedCount: number;
    questionTypes: ("MCQ" | "True/False" | "Fill-up" | "Short Answer")[];
}

export const useQuizStore = defineStore('quiz', () => {
    const authStore = useAuthStore();
    
    // State
    const quizConfig = ref<QuizConfig | null>(null);
    const isQuizActive = ref(false);
    const currentQuestion = ref<QuizQuestion | null>(null);
    const quizQuestions = ref<QuizQuestion[]>([]); // Array to hold all generated questions
    const currentQuestionIndex = ref(0);
    
    // Action to set configuration (called from QuizConfigView)
    function setConfig(contentId: string, numQuestions: number) {
        // Set the question types mix (e.g., 25% of each type for a simple implementation)
        const types: QuizConfig['questionTypes'] = [];
        const typesBase = ["MCQ", "True/False", "Fill-up", "Short Answer"];
        
        // Simple round-robin assignment to ensure even distribution
        for (let i = 0; i < numQuestions; i++) {
            types.push(typesBase[i % typesBase.length] as QuizConfig['questionTypes'][number]);
        }
        
        quizConfig.value = {
            contentId: contentId,
            numQuestions: numQuestions,
            generatedCount: 0,
            questionTypes: types,
        };
        
        quizQuestions.value = [];
        currentQuestionIndex.value = 0;
        currentQuestion.value = null;
    }

    // Main action to generate the next question
    async function generateNextQuestion(): Promise<boolean> {
        if (!quizConfig.value || quizConfig.value.generatedCount >= quizConfig.value.numQuestions) {
            console.log("Quiz generation complete.");
            return false;
        }

        const contentId = quizConfig.value.contentId;
        const difficulty = authStore.userProfile?.difficulty_level || 'Intermediate';
        
        // Get the specific question type required for the next generation slot
        const questionType = quizConfig.value.questionTypes[quizConfig.value.generatedCount];
        
        try {
            // Call the backend API with the required Content ID and Question Type
            const response = await axios.post(
                `${API_BASE_URL}/quiz/generate/${contentId}`,
                {
                    question_type: questionType,
                    difficulty: difficulty
                },
                authStore.authHeader 
            );

            const newQuestion = response.data as QuizQuestion;
            newQuestion.isCorrect = undefined; // Initialize state
            
            // Add to the list of generated questions
            quizQuestions.value.push(newQuestion);
            quizConfig.value.generatedCount += 1;
            
            // If this is the first question, start the quiz immediately
            if (quizConfig.value.generatedCount === 1) {
                isQuizActive.value = true;
            }
            
            // Set the current question to the newly generated one
            currentQuestion.value = newQuestion;
            currentQuestionIndex.value = quizQuestions.value.length - 1;
            
            return true;

        } catch (error: any) {
            console.error("Error generating question:", error.response || error);
            // On API key failure or content exhaustion, stop generation
            return false; 
        }
    }
    
    // --- NEW ACTION: Move back to the previous question ---
    function moveToPreviousQuestion() {
        if (currentQuestionIndex.value > 0) {
            currentQuestionIndex.value -= 1;
            currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
            return true;
        }
        return false;
    }

    // Action to move to the next question in the pre-generated array (Used when skipping back/reviewing)
    function moveToNextQuestion() {
        if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
            currentQuestionIndex.value += 1;
            currentQuestion.value = quizQuestions.value[currentQuestionIndex.value];
            return true;
        }
        return false;
    }


    // --- Action to submit the user's answer (FINAL LOGGING DATA RETURN) ---
    function submitAnswer(selectedResponse: string, timeTaken: number) { 
        if (!currentQuestion.value || !quizConfig.value) return { isCorrect: false, logData: null };
        
        // 1. Determine if the answer is correct
        const submitted = selectedResponse.trim().toLowerCase();
        const correct = currentQuestion.value.answer.trim().toLowerCase();
        const isCorrect = submitted === correct;
        
        // 2. Log the result back into the current question object
        currentQuestion.value.isCorrect = isCorrect; 
        
        // 3. Prepare data for backend logging (Module 4)
        const logData = {
            content_id: quizConfig.value.contentId,
            content_chunk: currentQuestion.value.content_chunk,
            is_correct: isCorrect,
            question_type: currentQuestion.value.type,
            time_taken_ms: timeTaken, // <-- NEW DATA POINT SAVED
        };
        
        return { isCorrect, logData };
    }
    
    function endQuiz() {
        isQuizActive.value = false;
        quizConfig.value = null;
        currentQuestion.value = null;
        // Optionally navigate to a results page here
    }
    
    // --- GETTER: Calculates the live score percentage (Progress Bar) ---
    const currentScorePercentage = computed(() => {
        if (quizQuestions.value.length === 0) return 0;
        
        // Filter questions that have been answered (where isCorrect is defined)
        const answeredQuestions = quizQuestions.value.filter(q => q.isCorrect !== undefined);
        
        if (answeredQuestions.length === 0) return 0;

        const correctCount = answeredQuestions.filter(q => q.isCorrect === true).length;
        
        // Calculate and round the percentage
        return Math.round((correctCount / answeredQuestions.length) * 100);
    });

    return {
        quizConfig,
        isQuizActive,
        currentQuestion,
        quizQuestions,
        currentQuestionIndex,
        setConfig,
        generateNextQuestion,
        moveToNextQuestion,
        moveToPreviousQuestion, // <-- NEW EXPORT
        submitAnswer, 
        endQuiz,
        currentScorePercentage,
    };
});