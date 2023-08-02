import { createRouter, createWebHistory } from "vue-router";
import Frontend from "./views/Frontend.vue";
import Backend from "./views/Backend.vue";

const routes = [
  { path: "/", component: Frontend },
  { path: "/backend", component: Backend },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;