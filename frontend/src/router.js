import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("./views/user/Stage.vue")
  },
  {
    path: "/all",
    component: () => import("./views/user/AllPhotos.vue")
  },
  {
    path: "/color_search",
    component: () => import("./views/user/ColorSearch.vue")
  },
  {
    path: "/single_photo_view",
    component: () => import("./views/user/SinglePhotoView.vue")
  },
  {
    path: "/about",
    component: () => import("./views/user/About.vue")
  },
  {
    path: "/operator",
    component: () => import("./views/Operator/index.vue")
  },
  {
    path: "/operator_edit",
    component: () => import("./views/Operator/edit.vue")
  },
];

const router = createRouter({
  history: createWebHashHistory("/iroironairo/"),
  routes,
});

export default router;