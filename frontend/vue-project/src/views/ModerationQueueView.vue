<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const flaggedQuestions = ref<any[]>([]);
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Flagged Questions ---
const fetchFlags = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        // NOTE: This API endpoint is NOT yet created in app.py. We will create it now (Route 14).
        const response = await axios.get(
            'http://localhost:5000/api/admin/moderation/queue',
            authStore.authHeader
        );
        flaggedQuestions.value = response.data;
    } catch (error: any) {
        errorMsg.value = 'Failed to load Flagging Queue: Unauthorized or API missing.';
        console.error("Moderation Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

// --- Handler to perform the action and refresh ---
const handleReviewAction = (flagId: string, action: 'resolve' | 'delete') => {
    alert(`Action: ${action} on Flag ID: ${flagId}. (No backend logic implemented yet.)`);
    // In a real app, this would call a PATCH/DELETE endpoint: /api/admin/moderation/{flagId}
};

onMounted(fetchFlags);
</script>

<template>
  <div class="moderation-container">
    <h1>🚨 Question Moderation Queue</h1>
    <p class="subtitle">Reviewing flagged content submissions from users.</p>

    <div v-if="isLoading" class="loading-state">Loading flagged items...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else-if="flaggedQuestions.length === 0" class="empty-queue">
        <p>✅ The moderation queue is clear! All quiet on the platform.</p>
        <button @click="router.push('/admin')" class="return-btn">Back to Dashboard</button>
    </div>
    
    <div v-else class="moderation-list">
        <div v-for="flag in flaggedQuestions" :key="flag._id" class="flag-card">
            <div class="flag-header">
                <span class="flag-reason">Reason: {{ flag.reason }}</span>
                <span class="flag-status status-pending">{{ flag.status }}</span>
            </div>
            
            <p class="flagged-question"><strong>Question Content ID:</strong> {{ flag.question_content_id }}</p>
            <p class="flagged-user">Flagged by User: {{ flag.user_id.substring(0, 8) }}...</p>
            <p class="flagged-time">Time: {{ new Date(flag.timestamp).toLocaleString() }}</p>

            <div class="flag-actions">
                <button @click="handleReviewAction(flag._id, 'resolve')" class="action-resolve">Resolve Flag</button>
                <button @click="handleReviewAction(flag._id, 'delete')" class="action-delete">Delete/Ignore</button>
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.moderation-container {
    max-width: 900px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}

.loading-state, .error-state, .empty-queue {
    padding: 30px;
    background-color: #2a2a44;
    border-radius: 12px;
    margin-top: 30px;
}

.empty-queue p {
    font-size: 1.2rem;
    color: #2ecc71;
}
.return-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

/* --- FLAG CARD STYLES --- */
.flag-card {
    background-color: #3e3e5a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 5px solid #e74c3c; /* Red warning border */
    text-align: left;
}

.flag-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #555;
    padding-bottom: 10px;
    margin-bottom: 10px;
}

.flag-reason {
    font-weight: bold;
    color: #e74c3c;
}

.flagged-question, .flagged-user, .flagged-time {
    font-size: 0.9rem;
    color: #c0c0c0;
}

.flag-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}

.flag-actions button {
    padding: 8px 15px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}

.action-resolve {
    background-color: #2ecc71;
    color: #1a1a2e;
}

.action-delete {
    background-color: #f39c12;
    color: #1a1a2e;
}
</style> -->














<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const flaggedQuestions = ref<any[]>([]);
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Flagged Questions (Route 14) ---
const fetchFlags = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/moderation/queue', // Route 14
            authStore.authHeader
        );
        flaggedQuestions.value = response.data;
    } catch (error: any) {
        errorMsg.value = 'Failed to load Flagging Queue: Unauthorized or API missing.';
        console.error("Moderation Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

// --- Handler to perform the action and refresh (Routes 15 & 16) ---
const handleReviewAction = async (flagId: string, action: 'resolve' | 'delete') => {
    
    if (!confirm(`Are you sure you want to ${action} flag ${flagId}? This action cannot be undone.`)) return;

    let method = action === 'resolve' ? 'patch' : 'delete';
    let endpoint = `/api/admin/moderation/${action}/${flagId}`;

    try {
        // Send the request (PATCH for resolve, DELETE for delete)
        await axios({
            method: method,
            url: `http://localhost:5000${endpoint}`,
            headers: authStore.authHeader.headers
        });
        
        // Success: Refresh the list immediately
        alert(`${action.charAt(0).toUpperCase() + action.slice(1)} successful! Queue will refresh.`);
        await fetchFlags(); // Reloads the queue to show the updated state
        
    } catch (error: any) {
        alert(`Error during ${action}: ${error.response?.data?.msg || 'Network failed.'}`);
        console.error(`Error during ${action}:`, error);
    }
};

onMounted(fetchFlags);
</script>

<template>
  <div class="moderation-container">
    <h1>🚨 Question Moderation Queue</h1>
    <p class="subtitle">Reviewing flagged content submissions from users.</p>

    <div v-if="isLoading" class="loading-state">Loading flagged items...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else-if="flaggedQuestions.length === 0" class="empty-queue">
        <p>✅ The moderation queue is clear! All quiet on the platform.</p>
        <button @click="router.push({ name: 'adminDashboard' })" class="return-btn">Back to Dashboard</button>
    </div>
    
    <div v-else class="moderation-list">
        <div v-for="flag in flaggedQuestions" :key="flag._id" class="flag-card">
            <div class="flag-header">
                <span class="flag-reason">Reason: {{ flag.reason }}</span>
                <span class="flag-status status-pending">{{ flag.status }}</span>
            </div>
            
            <p class="flagged-question"><strong>Question Content ID:</strong> {{ flag.question_content_id }}</p>
            <p class="flagged-user">Flagged by User: {{ flag.user_id.substring(0, 8) }}...</p>
            <p class="flagged-time">Time: {{ flag.timestamp }}</p>

            <div class="flag-actions">
                <button @click="handleReviewAction(flag._id, 'resolve')" class="action-resolve">Resolve Flag</button>
                <button @click="handleReviewAction(flag._id, 'delete')" class="action-delete">Delete/Ignore</button>
            </div>
        </div>
        <button @click="router.push({ name: 'adminDashboard' })" class="back-btn">← Back to Dashboard</button>
    </div>
  </div>
</template>

<style scoped>
.moderation-container {
    max-width: 900px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}

.loading-state, .error-state, .empty-queue {
    padding: 30px;
    background-color: #2a2a44;
    border-radius: 12px;
    margin-top: 30px;
}

.error-state {
    color: #e74c3c;
}

.empty-queue p {
    font-size: 1.2rem;
    color: #2ecc71;
}
.return-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

/* --- FLAG CARD STYLES --- */
.flag-card {
    background-color: #3e3e5a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 5px solid #e74c3c; /* Red warning border */
    text-align: left;
}

.flag-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #555;
    padding-bottom: 10px;
    margin-bottom: 10px;
}

.flag-reason {
    font-weight: bold;
    color: #e74c3c;
}

.flagged-question, .flagged-user, .flagged-time {
    font-size: 0.9rem;
    color: #c0c0c0;
}

.flag-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}

.flag-actions button {
    padding: 8px 15px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}

.action-resolve {
    background-color: #2ecc71;
    color: #1a1a2e;
}

.action-delete {
    background-color: #f39c12;
    color: #1a1a2e;
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