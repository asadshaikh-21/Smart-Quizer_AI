<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// NOTE: In a full version, this would fetch the list of ALL content from the database
// to allow the admin to moderate it.

const router = useRouter();
const contentList = ref([
    { id: 1, title: "Physics Notes - Chunks: 45", status: "Active" },
    { id: 2, title: "User Paste - Chunks: 12", status: "Active" },
    { id: 3, title: "History PDF - Chunks: 88", status: "Active" },
]);

// Handler to go back to the Admin Dashboard
const goBack = () => {
    router.push({ name: 'adminDashboard' });
};
</script>

<template>
  <div class="content-management-container">
    <h1><span class="emoji">📚</span> Content Management</h1>
    <p class="subtitle">Review and manage all user-uploaded study material.</p>

    <div class="content-list-card">
        <div v-if="contentList.length === 0" class="empty-state">
            No active content to display.
        </div>
        <div v-else class="list-wrapper">
            <div v-for="item in contentList" :key="item.id" class="content-item">
                <span class="item-title">{{ item.title }}</span>
                <span :class="['item-status', item.status === 'Active' ? 'status-active' : 'status-pending']">
                    {{ item.status }}
                </span>
                <button class="review-btn">Review Chunks</button>
            </div>
        </div>
        
        <button @click="goBack" class="back-btn">← Back to Dashboard</button>
    </div>
  </div>
</template>

<style scoped>
.content-management-container {
    max-width: 800px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}
.content-list-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.content-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #3e3e5a;
}
.list-wrapper {
    margin-bottom: 20px;
}

.item-title {
    flex-grow: 1;
    font-weight: 600;
    color: #fff;
}
.item-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 15px;
}
.status-active {
    background-color: #2ecc7133;
    color: #2ecc71;
}
.review-btn {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    box-shadow: 0 3px 0 #2980b9;
}
.back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3e3e5a;
    color: #e0e0e0;
    border: 1px solid #555;
    border-radius: 8px;
    cursor: pointer;
}
</style> -->









<!-- 
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // For API calls
import { useAuthStore } from '@/stores/auth'; // To get JWT token

const authStore = useAuthStore();
const router = useRouter();

const contentList = ref<any[]>([]); // <--- CRITICAL: Now an empty reactive array
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List from Backend (Route 7) ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'User not authenticated.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list', // Calls the API that sorts content by date
            authStore.authHeader
        );
        
        // Update the reactive variable with live data
        contentList.value = response.data; 

    } catch (error: any) {
        // A 404/401 indicates a backend/auth error.
        errorMsg.value = 'Failed to load user content. Check backend connection.';
        console.error("Content List Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchContentList);

// Handler to go back to the Admin Dashboard
const goBack = () => {
    router.push({ name: 'adminDashboard' });
};
</script>

<template>
  <div class="content-management-container">
    <h1><span class="emoji">📚</span> Content Management</h1>
    <p class="subtitle">Review and manage all user-uploaded study material.</p>

    <div class="content-list-card">
        <div v-if="errorMsg" class="error-state">
            Error: {{ errorMsg }}
        </div>
        <div v-else-if="isLoading" class="loading-state">
            Fetching content list from database...
        </div>
        <div v-else-if="contentList.length === 0" class="empty-state">
            No active content to display. Please ensure you have uploaded notes.
        </div>
        <div v-else class="list-wrapper">
            <div v-for="item in contentList" :key="item._id" class="content-item">
                <span class="item-title">
                    {{ item.title }} - Chunks: {{ item.chunk_count }}
                </span>
                <span class="item-time">Uploaded: {{ item.created_at }}</span>
                
                <span class="item-status status-active">
                    Active
                </span>
                <button class="review-btn">Review Chunks</button>
            </div>
        </div>
        
        <button @click="goBack" class="back-btn">← Back to Dashboard</button>
    </div>
  </div>
</template>

<style scoped>
.content-management-container {
    max-width: 800px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}
.content-list-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.content-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #3e3e5a;
}
.list-wrapper {
    margin-bottom: 20px;
}

.item-title {
    flex-grow: 1;
    font-weight: 600;
    color: #fff;
    margin-right: 15px; /* Added margin for spacing */
}

.item-time {
    font-size: 0.8rem;
    color: #9b59b6; /* Purple color for time */
    margin-right: 15px;
}

.item-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 15px;
}
.status-active {
    background-color: #2ecc7133;
    color: #2ecc71;
}
.review-btn {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    box-shadow: 0 3px 0 #2980b9;
}
.review-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(2px);
}
.back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3e3e5a;
    color: #e0e0e0;
    border: 1px solid #555;
    border-radius: 8px;
    cursor: pointer;
}
</style> -->








<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // For API calls
import { useAuthStore } from '@/stores/auth'; // To get JWT token

const authStore = useAuthStore();
const router = useRouter();

const contentList = ref<any[]>([]); // Reactive array for fetched content
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List from Backend (Route 7) ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'User not authenticated.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list', // Calls the API that sorts content by date
            authStore.authHeader
        );
        
        // Update the reactive variable with live data
        contentList.value = response.data; 

    } catch (error: any) {
        // A 404/401 indicates a backend/auth error.
        errorMsg.value = 'Failed to load user content. Check backend connection.';
        console.error("Content List Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchContentList);

// Handler to go back to the Admin Dashboard
const goBack = () => {
    router.push({ name: 'adminDashboard' });
};

// --- NEW HANDLER: Review Chunks Functionality (Module 6) ---
const reviewChunks = (item: any) => {
    // Check if the item has chunks to review
    if (item.chunks && item.chunks.length > 0) {
        // Prepare a summary of the first few chunks
        const chunkSummary = item.chunks.slice(0, 5).map((chunk: string, index: number) => 
            `Chunk ${index + 1}: ${chunk.substring(0, 50)}...`
        ).join('\n\n');
        
        alert(`--- Content Review: ${item.title} ---\n\n` + 
              `Total Chunks: ${item.chunk_count}\n\n` +
              `First 5 Chunks for Inspection:\n${chunkSummary}\n\n` +
              `Action: In a full app, this would open a dedicated chunk viewer.`);
    } else {
        alert(`Content ID ${item._id} has no valid chunks.`);
    }
};
</script>

<template>
  <div class="content-management-container">
    <h1><span class="emoji">📚</span> Content Management</h1>
    <p class="subtitle">Review and manage all user-uploaded study material.</p>

    <div class="content-list-card">
        <div v-if="errorMsg" class="error-state">
            Error: {{ errorMsg }}
        </div>
        <div v-else-if="isLoading" class="loading-state">
            Fetching content list from database...
        </div>
        <div v-else-if="contentList.length === 0" class="empty-state">
            No active content to display. Please ensure you have uploaded notes.
        </div>
        <div v-else class="list-wrapper">
            <div v-for="item in contentList" :key="item._id" class="content-item">
                <span class="item-title">
                    {{ item.title }} - Chunks: {{ item.chunk_count }}
                </span>
                <span class="item-time">Uploaded: {{ item.created_at }}</span>
                
                <span class="item-status status-active">
                    Active
                </span>
                <button @click="reviewChunks(item)" class="review-btn">Review Chunks</button>
            </div>
        </div>
        
        <button @click="goBack" class="back-btn">← Back to Dashboard</button>
    </div>
  </div>
</template>

<style scoped>
.content-management-container {
    max-width: 800px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}
.content-list-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.content-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #3e3e5a;
}
.list-wrapper {
    margin-bottom: 20px;
}

.item-title {
    flex-grow: 1;
    font-weight: 600;
    color: #fff;
    margin-right: 15px; /* Added margin for spacing */
}

.item-time {
    font-size: 0.8rem;
    color: #9b59b6; /* Purple color for time */
    margin-right: 15px;
}

.item-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 15px;
}
.status-active {
    background-color: #2ecc7133;
    color: #2ecc71;
}
.review-btn {
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    box-shadow: 0 3px 0 #2980b9;
}
.review-btn:active {
    box-shadow: 0 1px 0 #2980b9;
    transform: translateY(2px);
}
.back-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3e3e5a;
    color: #e0e0e0;
    border: 1px solid #555;
    border-radius: 8px;
    cursor: pointer;
}
</style>