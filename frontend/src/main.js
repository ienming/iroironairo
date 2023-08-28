import { createApp, defineAsyncComponent } from 'vue'
import App from './App.vue'

// Setting routers
// import router from './router';
import { createRouter, createWebHashHistory } from "vue-router";
import UserIndex from "./views/user/Index.vue";
import OperatorIndex from "./views/Operator/index.vue";
import OperatorEdit from "./views/Operator/edit.vue"

const routes = [
  { path: "/", component: UserIndex },
  { path: "/operator", component: OperatorIndex },
  { path: "/operator_edit", component: OperatorEdit },
];

const router = createRouter({
  history: createWebHashHistory("/iroironairo/"),
  routes,
});

// Mount
const app = createApp(App);
app.use(router);

app.mount('#app')