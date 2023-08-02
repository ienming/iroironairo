import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import './assets/main.css'

// gloval event
import mitt from 'mitt';
export const eventBus = mitt();

// 使用 Vue Router
const app = createApp(App);
app.use(router);

createApp(app).mount('#app')