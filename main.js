import './assets/css/custom.css'
import './assets/js/bootstrap.bundle.min.js'
import { createApp } from 'vue'
import router from './router';
import App from './App.vue'

const app = createApp(App);
app.use(router);

app.mount('#app')