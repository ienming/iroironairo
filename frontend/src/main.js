import './assets/css/custom.css'
import './assets/js/bootstrap.bundle.min.js'
import { createApp } from 'vue'
import App from './App.vue'

// Setting routers
// import router from './router';
import { createRouter, createWebHistory, createWebHashHistory } from "vue-router";
import UserStage from "./views/user/Stage.vue";
import AllPhotos from "./views/user/AllPhotos.vue";
import ColorSearch from "./views/user/ColorSearch.vue";
import SinglePhotoView from "./views/user/SinglePhotoView.vue";
import About from "./views/user/About.vue";
import OperatorIndex from "./views/Operator/index.vue";
import OperatorEdit from "./views/Operator/edit.vue";

const routes = [
  { path: "/", component: UserStage },
  { path: "/all", component: AllPhotos },
  { path: "/color_search", component: ColorSearch },
  { path: "/single_photo_view", component: SinglePhotoView },
  { path: "/about", component: About },
  { path: "/operator", component: OperatorIndex },
  { path: "/operator_edit", component: OperatorEdit },
];

const router = createRouter({
  // history: createWebHistory("/iroironairo/"),
  history: createWebHashHistory("/iroironairo/"),
  routes,
});

// router.beforeEach((to, from) => {
//   console.log(`From ${from.path} to ${to.path}`)
// })

// Mount
const app = createApp(App);
// Router
app.use(router);

app.mount('#app')