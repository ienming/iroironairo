import { createApp, defineAsyncComponent } from 'vue'
import App from './App.vue'
// import router from './router';

import './assets/main.css'

// // Global event
// import mitt from 'mitt';
// export const eventBus = mitt();

// Setting routers
import { createRouter, createWebHistory } from "vue-router";
import User from "./views/User.vue";
import OperatorIndex from "./views/Operator/index.vue";
import OperatorEdit from "./views/Operator/edit.vue"

const routes = [
  { path: "/", component: User },
  { path: "/operator", component: OperatorIndex },
  { path: "/operator_edit", component: OperatorEdit },
];

const router = createRouter({
  history: createWebHistory("/iroironairo/"),
  routes,
});

// Mount
const app = createApp(App);
app.use(router);

app.mount('#app')