// D:\SmartQuizzer\frontend\vue-project\src\main.ts

import './assets/main.css'

import { createApp } from 'vue'
// Ensure Pinia is imported from the pinia package
import { createPinia } from 'pinia' 
import App from './App.vue'
// Ensure router is imported from the local router file
import router from './router' 

const app = createApp(App)
const pinia = createPinia() 

app.use(pinia) 
app.use(router)

app.mount('#app')