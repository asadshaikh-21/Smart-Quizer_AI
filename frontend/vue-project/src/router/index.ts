// // D:\SmartQuizzer\frontend\vue-project\src\router\index.ts

// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } else {
//     next()
//   }
// })

// export default router



// D:\SmartQuizzer\frontend\vue-project\src\router\index.ts

// D:\SmartQuizzer\frontend\vue-project\src\router\index.ts

// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Module 3 Step 1)
//     {
//       path: '/quiz',
//       name: 'quiz',
//       // FIX: Use the new QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz',
//       component: () => import('../views/ActiveQuizView.vue'), // You will create this next
//       meta: { requiresAuth: true }
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router




// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
//     {
//       path: '/quiz',
//       name: 'quizConfig', // Renamed from 'quiz' for clarity
//       // FIX: Use the QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz', // This is the route name referenced in the store and components
//       component: () => import('../views/ActiveQuizView.vue'),
//       meta: { requiresAuth: true }
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router








// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
//     {
//       path: '/quiz',
//       name: 'quizConfig', // Renamed from 'quiz' for clarity
//       // FIX: Use the QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz', 
//       component: () => import('../views/ActiveQuizView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ RESULTS SUMMARY (Module 5)
//     {
//       path: '/quiz/results',
//       name: 'quizResults', 
//       component: () => import('../views/ResultSummaryView.vue'), // <-- NEW COMPONENT
//       meta: { requiresAuth: true }
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router






// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
//     {
//       path: '/quiz',
//       name: 'quizConfig', 
//       // FIX: Use the QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz', 
//       component: () => import('../views/ActiveQuizView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ RESULTS SUMMARY (Module 5)
//     {
//       path: '/quiz/results',
//       name: 'quizResults', 
//       component: () => import('../views/ResultSummaryView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: LEARNING ANALYTICS DASHBOARD (Module 6)
//     {
//       path: '/analytics',
//       name: 'analytics', // <--- THE NEW ROUTE NAME
//       component: () => import('../views/AnalyticsView.vue'), 
//       meta: { requiresAuth: true }
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router









// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
//     {
//       path: '/quiz',
//       name: 'quizConfig', 
//       // FIX: Use the QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz', 
//       component: () => import('../views/ActiveQuizView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ RESULTS SUMMARY (Module 5)
//     {
//       path: '/quiz/results',
//       name: 'quizResults', 
//       component: () => import('../views/ResultSummaryView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: LEARNING ANALYTICS DASHBOARD (Module 6)
//     {
//       path: '/analytics',
//       name: 'analytics', 
//       component: () => import('../views/AnalyticsView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ADMIN DASHBOARD (Module 6)
//     {
//       path: '/admin',
//       name: 'adminDashboard', // Use this name for clarity
//       component: () => import('../views/AdminDashboardView.vue'), 
//       meta: { requiresAuth: true } // Protected (though further backend role check is required in production)
//     }
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router







// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth' 

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     // Existing Home route
//     {
//       path: '/',
//       name: 'home',
//       // FIX: Use relative path for component import
//       component: () => import('../views/HomeView.vue')
//     },
//     // New Login Route
//     {
//       path: '/login',
//       name: 'login',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'), 
//       meta: { requiresAuth: false }
//     },
//     // New Register Route
//     {
//       path: '/register',
//       name: 'register',
//       // FIX: Use relative path for component import
//       component: () => import('../views/AuthView.vue'),
//       meta: { requiresAuth: false }
//     },
//     // Protected Profile Route
//     {
//       path: '/profile',
//       name: 'profile',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ProfileView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE FOR CONTENT INGESTION (Module 2)
//     {
//       path: '/content',
//       name: 'content',
//       // FIX: Use relative path for component import
//       component: () => import('../views/ContentView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
//     {
//       path: '/quiz',
//       name: 'quizConfig', 
//       // FIX: Use the QuizConfigView component
//       component: () => import('../views/QuizConfigView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ACTIVE QUIZ RUNNING
//     {
//       path: '/quiz/active',
//       name: 'activeQuiz', 
//       component: () => import('../views/ActiveQuizView.vue'),
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: QUIZ RESULTS SUMMARY (Module 5)
//     {
//       path: '/quiz/results',
//       name: 'quizResults', 
//       component: () => import('../views/ResultSummaryView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: LEARNING ANALYTICS DASHBOARD (Module 6)
//     {
//       path: '/analytics',
//       name: 'analytics', 
//       component: () => import('../views/AnalyticsView.vue'), 
//       meta: { requiresAuth: true }
//     },
//     // NEW ROUTE: ADMIN DASHBOARD (Module 6)
//     {
//       path: '/admin',
//       name: 'adminDashboard',
//       component: () => import('../views/AdminDashboardView.vue'), 
//       meta: { requiresAuth: true } 
//     },
//     // NEW ROUTE: MODERATION QUEUE (Module 6)
//     {
//       path: '/admin/flags',
//       name: 'moderationQueue',
//       component: () => import('../views/ModerationQueueView.vue'), 
//       meta: { requiresAuth: true }
//     },
//   ]
// })

// // Navigation Guard (Required for protected routes)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Protect routes that require login
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login' }) 
//   } 
//   // Redirect logged-in users away from login/register pages
//   else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
//     next({ name: 'profile' })
//   } 
//   // Allow navigation
//   else {
//     next()
//   }
// })

// export default router










import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Existing Home route
    {
      path: '/',
      name: 'home',
      // FIX: Use relative path for component import
      component: () => import('../views/HomeView.vue')
    },
    // New Login Route
    {
      path: '/login',
      name: 'login',
      // FIX: Use relative path for component import
      component: () => import('../views/AuthView.vue'), 
      meta: { requiresAuth: false }
    },
    // New Register Route
    {
      path: '/register',
      name: 'register',
      // FIX: Use relative path for component import
      component: () => import('../views/AuthView.vue'),
      meta: { requiresAuth: false }
    },
    // Protected Profile Route
    {
      path: '/profile',
      name: 'profile',
      // FIX: Use relative path for component import
      component: () => import('../views/ProfileView.vue'), 
      meta: { requiresAuth: true } 
    },
    // NEW ROUTE FOR CONTENT INGESTION (Module 2)
    {
      path: '/content',
      name: 'content',
      // FIX: Use relative path for component import
      component: () => import('../views/ContentView.vue'),
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: QUIZ CONFIGURATION (Updated Name: quizConfig)
    {
      path: '/quiz',
      name: 'quizConfig', 
      // FIX: Use the QuizConfigView component
      component: () => import('../views/QuizConfigView.vue'), 
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: ACTIVE QUIZ RUNNING
    {
      path: '/quiz/active',
      name: 'activeQuiz', 
      component: () => import('../views/ActiveQuizView.vue'),
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: QUIZ RESULTS SUMMARY (Module 5)
    {
      path: '/quiz/results',
      name: 'quizResults', 
      component: () => import('../views/ResultSummaryView.vue'), 
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: LEARNING ANALYTICS DASHBOARD (Module 6)
    {
      path: '/analytics',
      name: 'analytics', 
      component: () => import('../views/AnalyticsView.vue'), 
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: ADMIN DASHBOARD (Module 6)
    {
      path: '/admin',
      name: 'adminDashboard',
      component: () => import('../views/AdminDashboardView.vue'), 
      meta: { requiresAuth: true } 
    },
    // NEW ROUTE: MODERATION QUEUE (Module 6)
    {
      path: '/admin/flags',
      name: 'moderationQueue',
      component: () => import('../views/ModerationQueueView.vue'), 
      meta: { requiresAuth: true }
    },
    // NEW ROUTE: CONTENT MANAGEMENT (Module 6)
    {
      path: '/admin/content',
      name: 'contentManagement', 
      component: () => import('../views/ContentManagementView.vue'), 
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation Guard (Required for protected routes)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Protect routes that require login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' }) 
  } 
  // Redirect logged-in users away from login/register pages
  else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'profile' })
  } 
  // Allow navigation
  else {
    next()
  }
})

export default router