<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// Handler for the moderation button (Future implementation)
const goToModeration = () => {
    alert("Navigating to Question Moderation Queue (Feature placeholder).");
    // router.push({ name: 'moderationQueue' }); // Future route
};

// Handler for the moderation button (Future implementation)
const goToContentReview = () => {
    alert("Navigating to Content Review (Feature placeholder).");
};

</script>

<template>
  <div class="admin-container">
    <h1><span class="emoji">👑</span> Admin Dashboard</h1>
    <p class="subtitle">Platform Health and Performance Overview</p>

    <div v-if="isLoading" class="loading-state">Loading system metrics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else class="dashboard-grid">
        
        <div class="stat-card stat-primary">
            <p class="card-label">Overall Accuracy</p>
            <span class="card-value">{{ stats.overall_accuracy_percent }}%</span>
            <p class="card-detail">System average across all quizzes.</p>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Users</p>
            <span class="card-value">{{ stats.total_users }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Quizzes Taken</p>
            <span class="card-value">{{ stats.total_interactions }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Content Items Uploaded</p>
            <span class="card-value">{{ stats.total_content_items }}</span>
        </div>

    </div>

    <div class="admin-actions">
        <h2>Content Quality & Feedback Management</h2>
        
        <button @click="goToModeration" class="action-btn-moderation">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </button>
        
        <button @click="goToContentReview" class="action-btn-secondary">
             <span class="emoji">📚</span> Manage User Content
        </button>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
    border-radius: 10px;
}

/* --- DASHBOARD GRID --- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
}

.stat-card {
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
}

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style> -->







<!-- 

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; // CRITICAL: Import RouterLink

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// Handler for content review (still an alert, but kept separate for structure)
const goToContentReview = () => {
    alert("Navigating to Content Review (Feature placeholder).");
};
</script>

<template>
  <div class="admin-container">
    <h1><span class="emoji">👑</span> Admin Dashboard</h1>
    <p class="subtitle">Platform Health and Performance Overview</p>

    <div v-if="isLoading" class="loading-state">Loading system metrics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else class="dashboard-grid">
        
        <div class="stat-card stat-primary">
            <p class="card-label">Overall Accuracy</p>
            <span class="card-value">{{ stats.overall_accuracy_percent }}%</span>
            <p class="card-detail">System average across all quizzes.</p>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Users</p>
            <span class="card-value">{{ stats.total_users }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Quizzes Taken</p>
            <span class="card-value">{{ stats.total_interactions }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Content Items Uploaded</p>
            <span class="card-value">{{ stats.total_content_items }}</span>
        </div>

    </div>

    <div class="admin-actions">
        <h2>Content Quality & Feedback Management</h2>
        
        <RouterLink :to="{ name: 'moderationQueue' }" class="action-btn-moderation router-link">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </RouterLink>
        
        <button @click="goToContentReview" class="action-btn-secondary">
             <span class="emoji">📚</span> Manage User Content
        </button>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
    border-radius: 10px;
}

/* --- DASHBOARD GRID --- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
}

.stat-card {
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
}

/* Ensure RouterLink inherits button styling */
.router-link {
    display: block; 
    text-decoration: none;
    text-align: center;
    color: white !important; /* Forces link text color */
}

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style> -->









<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; // CRITICAL: Import RouterLink

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// The goToContentReview alert handler has been DELETED, replaced by the RouterLink.
</script>

<template>
  <div class="admin-container">
    <h1><span class="emoji">👑</span> Admin Dashboard</h1>
    <p class="subtitle">Platform Health and Performance Overview</p>

    <div v-if="isLoading" class="loading-state">Loading system metrics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else class="dashboard-grid">
        
        <div class="stat-card stat-primary">
            <p class="card-label">Overall Accuracy</p>
            <span class="card-value">{{ stats.overall_accuracy_percent }}%</span>
            <p class="card-detail">System average across all quizzes.</p>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Users</p>
            <span class="card-value">{{ stats.total_users }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Total Quizzes Taken</p>
            <span class="card-value">{{ stats.total_interactions }}</span>
        </div>

        <div class="stat-card">
            <p class="card-label">Content Items Uploaded</p>
            <span class="card-value">{{ stats.total_content_items }}</span>
        </div>

    </div>

    <div class="admin-actions">
        <h2>Content Quality & Feedback Management</h2>
        
        <RouterLink :to="{ name: 'moderationQueue' }" class="action-btn-moderation router-link">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </RouterLink>
        
        <RouterLink :to="{ name: 'contentManagement' }" class="action-btn-secondary router-link">
             <span class="emoji">📚</span> Manage User Content
        </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
    border-radius: 10px;
}

/* --- DASHBOARD GRID --- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
}

.stat-card {
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
}

/* Ensure RouterLink inherits button styling */
.router-link {
    display: block; 
    text-decoration: none;
    text-align: center;
    color: white !important; /* Forces link text color */
}

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style>