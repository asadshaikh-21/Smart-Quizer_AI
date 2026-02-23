<!-- <script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const contentTitle = ref('My Study Notes');
const rawText = ref('');
const statusMessage = ref('');
const isLoading = ref(false);

async function uploadContent() {
    statusMessage.value = '';
    
    if (!rawText.value.trim()) {
        statusMessage.value = '❌ Please paste some learning material.';
        return;
    }

    isLoading.value = true;
    
    try {
        const response = await axios.post(
            'http://localhost:5000/api/content/upload',
            { 
                title: contentTitle.value,
                raw_text: rawText.value 
            },
            authStore.authHeader 
        );

        const data = response.data;
        statusMessage.value = `✅ Success! Content processed into ${data.chunk_count} knowledge chunks.`;
        rawText.value = ''; // Clear the textarea on success

    } catch (error: any) {
        console.error('Content upload failed:', error);
        const msg = error.response?.data?.msg || 'Failed to process content. Check backend logs.';
        statusMessage.value = `❌ Error: ${msg}`;
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
  <div class="content-ingestion-container">
    <h1>📚 Ingest Learning Material</h1>
    <p class="subtitle">Paste text from your notes, book, or article below. Our AI will turn it into quiz chunks.</p>

    <div class="form-card">
        <form @submit.prevent="uploadContent">
            <div class="form-group">
                <label for="title">Title for these Notes:</label>
                <input id="title" type="text" v-model="contentTitle" required>
            </div>

            <div class="form-group">
                <label for="rawText">Paste Study Material Here:</label>
                <textarea 
                    id="rawText" 
                    v-model="rawText" 
                    rows="10" 
                    placeholder="E.g., The kinetic theory of gases describes a gas as a large number of submicroscopic particles..."></textarea>
            </div>

            <p v-if="statusMessage" :class="{'success-message': statusMessage.startsWith('✅'), 'error-message': statusMessage.startsWith('❌') }">
                {{ statusMessage }}
            </p>

            <button type="submit" :disabled="isLoading || !rawText.trim()">
                <span v-if="isLoading">Processing Text...</span>
                <span v-else>Process & Save Chunks</span>
            </button>
        </form>
    </div>
  </div>
</template>

<style scoped>
.content-ingestion-container {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.subtitle {
    margin-bottom: 30px;
    color: #c990ff;
}

.form-card {
    padding: 30px;
    background-color: #2a2a44; /* Darker card background for contrast */
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    text-align: left;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="text"], textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #555;
    border-radius: 8px;
    background-color: #3e3e5a; /* Slightly lighter input background */
    color: #fff;
    box-sizing: border-box;
    resize: vertical;
}

/* Inherit the 3D button styles for consistency */
button {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c; /* Darker shadow */
    transform: translateY(0);
}

button:active:not(:disabled) {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
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
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router'; // <-- NEW IMPORT

// Base URL for the Flask backend API
const API_BASE_URL = 'http://localhost:5000';

const authStore = useAuthStore();
const router = useRouter(); // <-- NEW INSTANCE

// UI State
const ingestionMethod = ref('paste'); // 'paste', 'url', or 'file'

// Form State
const contentTitle = ref('My Study Notes');
const rawText = ref('');
const contentUrl = ref(''); // For URL input
const selectedFile = ref<File | null>(null); // For file upload
const statusMessage = ref('');
const isLoading = ref(false);

// Handle file selection change event
const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        selectedFile.value = target.files[0];
    }
};

async function uploadContent() {
    statusMessage.value = '';
    
    // --- Step 1: Basic Validation based on method ---
    if (ingestionMethod.value === 'paste' && !rawText.value.trim()) {
        statusMessage.value = '❌ Please paste some learning material.';
        return;
    }
    if (ingestionMethod.value === 'url' && !contentUrl.value.trim()) {
        statusMessage.value = '❌ Please enter a valid URL.';
        return;
    }
    if (ingestionMethod.value === 'file' && !selectedFile.value) {
        statusMessage.value = '❌ Please select a file to upload.';
        return;
    }

    isLoading.value = true;
    
    // --- Step 2: Build FormData for API Call ---
    const endpoint = '/api/content/upload';
    const formData = new FormData();
    // All methods require title and method
    formData.append('title', contentTitle.value);
    formData.append('method', ingestionMethod.value);
    
    // Append the specific data based on the chosen method
    if (ingestionMethod.value === 'paste') {
        formData.append('raw_text', rawText.value);
    } else if (ingestionMethod.value === 'url') {
        formData.append('content_url', contentUrl.value);
    } else if (ingestionMethod.value === 'file' && selectedFile.value) {
        formData.append('file', selectedFile.value);
    }

    try {
        const response = await axios.post(
            API_BASE_URL + endpoint,
            formData, 
            {
                headers: {
                    // Include JWT authentication headers
                    ...authStore.authHeader.headers,
                    // Specify content type for file uploads
                    'Content-Type': 'multipart/form-data' 
                }
            } 
        );

        const data = response.data;
        statusMessage.value = `✅ Success! Content processed into ${data.chunk_count} knowledge chunks. Redirecting...`;
        
        // Clear inputs on success
        rawText.value = ''; 
        contentUrl.value = '';
        selectedFile.value = null; 
        
        // --- CRITICAL: ADD REDIRECT LOGIC HERE ---
        setTimeout(() => {
            // Redirect to the new Quiz Configuration Page
            router.push('/quiz'); 
        }, 1500);
        // ------------------------------------------
        
    } catch (error: any) {
        console.error('Content upload failed:', error.response || error);
        const msg = error.response?.data?.msg || 'Failed to process content. Check backend logs.';
        statusMessage.value = `❌ Error: ${msg}`;
    } finally {
        isLoading.value = false;
        // The success redirect already handles clearing the success message.
        // Keep the error timeout logic.
        if (statusMessage.value.startsWith('❌')) {
             setTimeout(() => statusMessage.value = '', 3000);
        }
    }
}
</script>

<template>
  <div class="content-ingestion-container">
    <h1>📚 Ingest Learning Material</h1>
    <p class="subtitle">Select a method to provide your notes. Our AI will turn it into quiz chunks.</p>

    <div class="form-card">
        <form @submit.prevent="uploadContent">
            <div class="form-group">
                <label for="title">Title for these Notes:</label>
                <input id="title" type="text" v-model="contentTitle" required>
            </div>
            
            <div class="form-group ingestion-select">
                <label>Ingestion Method:</label>
                <div class="method-options">
                    <button type="button" :class="{ 'active': ingestionMethod === 'paste' }" @click="ingestionMethod = 'paste'">Paste Text</button>
                    <button type="button" :class="{ 'active': ingestionMethod === 'url' }" @click="ingestionMethod = 'url'">Analyze URL</button>
                    <button type="button" :class="{ 'active': ingestionMethod === 'file' }" @click="ingestionMethod = 'file'">Upload File (PDF)</button>
                </div>
            </div>

            <div class="form-group input-area">
                <label v-if="ingestionMethod === 'paste'" for="rawText">Paste Study Material Here:</label>
                <textarea 
                    v-if="ingestionMethod === 'paste'" 
                    id="rawText" 
                    v-model="rawText" 
                    rows="10" 
                    placeholder="E.g., The kinetic theory of gases describes a gas as a large number of submicroscopic particles..."></textarea>

                <template v-else-if="ingestionMethod === 'url'">
                    <label for="contentUrl">Enter URL to Analyze:</label>
                    <input id="contentUrl" type="url" v-model="contentUrl" placeholder="https://example.com/article">
                </template>

                <template v-else-if="ingestionMethod === 'file'">
                    <label for="fileUpload">Upload PDF/Text File:</label>
                    <input id="fileUpload" type="file" @change="handleFileChange" accept=".pdf,.txt">
                    <p class="file-name" v-if="selectedFile">File selected: {{ selectedFile.name }}</p>
                </template>
            </div>


            <p v-if="statusMessage" :class="{'success-message': statusMessage.startsWith('✅'), 'error-message': statusMessage.startsWith('❌') }">
                {{ statusMessage }}
            </p>

            <button type="submit" :disabled="isLoading || (ingestionMethod === 'paste' && !rawText.trim()) || (ingestionMethod === 'url' && !contentUrl.trim()) || (ingestionMethod === 'file' && !selectedFile)">
                <span v-if="isLoading">Processing Text...</span>
                <span v-else>Process & Save Chunks</span>
            </button>
        </form>
    </div>
  </div>
</template>

<style scoped>
/* Base styles from previous step */
.content-ingestion-container {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.subtitle {
    margin-bottom: 30px;
    color: #c990ff;
}

.form-card {
    padding: 30px;
    background-color: #2a2a44; /* Darker card background for contrast */
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    text-align: left;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #e0e0e0;
}

input[type="text"], input[type="url"], textarea, select, input[type="file"] {
    width: 100%;
    padding: 12px;
    border: 1px solid #555;
    border-radius: 8px;
    background-color: #3e3e5a; 
    color: #fff;
    box-sizing: border-box;
    resize: vertical;
}

/* Specific styling for file input to make it look nice */
input[type="file"] {
    padding: 8px 12px; /* Less padding to fit button text */
    cursor: pointer;
}


.file-name {
    margin-top: 10px;
    font-style: italic;
    color: #9b59b6;
}

/* Ingestion Method Selection Styling */
.method-options {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.method-options button {
    flex-grow: 1;
    padding: 10px;
    background-color: #3e3e5a;
    color: #c0c0c0;
    border: 2px solid #3e3e5a;
    border-radius: 8px;
    cursor: pointer;
    font-weight: normal;
    transition: all 0.2s ease;
    box-shadow: none !important; 
    transform: none !important;
}

.method-options button:hover {
    border-color: #82aaff;
    color: #fff;
}

.method-options button.active {
    background-color: #9b59b6; 
    border-color: #8e44ad;
    color: #fff;
    font-weight: bold;
}

/* Inherit the primary 3D button styles for submit */
button[type="submit"] {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
}

button[type="submit"]:active:not(:disabled) {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}

button[type="submit"]:disabled {
    background-color: #555;
    box-shadow: 0 4px 0 #333;
    cursor: not-allowed;
    transform: translateY(0);
    color: #aaa;
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