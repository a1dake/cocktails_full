import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "simplebar/dist/simplebar.css";
import "simplebar";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import "vue-multiselect/dist/vue-multiselect.css";

import "@vuepic/vue-datepicker/dist/main.css";
import vuetify from "@/plugins/vuetify";

createApp(App).use(store).use(router).use(vuetify).mount("#app");
