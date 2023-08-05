import { createApp, defineAsyncComponent } from 'vue'
import App from './App.vue'

// Setting routers
// import router from './router';
import { createRouter, createWebHashHistory } from "vue-router";
import User from "./views/User.vue";
import OperatorIndex from "./views/Operator/index.vue";
import OperatorEdit from "./views/Operator/edit.vue"

const routes = [
  { path: "/", component: User },
  { path: "/operator", component: OperatorIndex },
  { path: "/operator_edit", component: OperatorEdit },
];

const router = createRouter({
  history: createWebHashHistory("/iroironairo/"),
  routes,
});

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

// Mount
const app = createApp(App);
app.use(router);
app.use(vuetify)

app.mount('#app')