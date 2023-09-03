import { createApp, defineAsyncComponent } from 'vue'
import App from './App.vue'

// Setting routers
// import router from './router';
import { createRouter, createWebHashHistory } from "vue-router";
import UserStage from "./views/user/Stage.vue";
import AllPhotos from "./views/user/AllPhotos.vue";
import About from "./views/user/About.vue";
import OperatorIndex from "./views/Operator/index.vue";
import OperatorEdit from "./views/Operator/edit.vue"

const routes = [
  { path: "/", component: UserStage },
  { path: "/all", component: AllPhotos },
  { path: "/about", component: About },
  { path: "/operator", component: OperatorIndex },
  { path: "/operator_edit", component: OperatorEdit },
];

const router = createRouter({
  history: createWebHashHistory("/iroironairo/"),
  routes,
});

// Mount
const app = createApp(App);
// Router
app.use(router);

app.mount('#app')