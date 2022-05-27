import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import withUUID from "vue-uuid";
import vSelect from 'vue-select';
import ConfettiExplosion from "vue-confetti-explosion";

import 'vue-select/dist/vue-select.css';



axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router, axios, withUUID,ConfettiExplosion).component("v-select", vSelect).mount('#app')

export{
    router
}