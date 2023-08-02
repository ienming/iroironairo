import { createApp, defineAsyncComponent } from 'vue'
import App from './App.vue'
// import router from './router';

import './assets/main.css'

// gloval event
import mitt from 'mitt';
export const eventBus = mitt();


import { createRouter, createWebHistory } from "vue-router";
import Frontend from "./views/Frontend.vue";
import Backend from "./views/Backend.vue";

const routes = [
  { path: "/", component: Frontend },
  { path: "/backend", component: Backend },
];

const router = createRouter({
  history: createWebHistory("/iroironairo/"),
  routes,
});

const app = createApp(App);
app.use(router);

app.mount('#app')