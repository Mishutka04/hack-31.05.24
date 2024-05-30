import './assets/main.css';
import router from './router';
import { createApp } from 'vue';
import App from './App.vue';
const app = createApp(App);
app.config.globalProperties.$globalUrl = 'http://127.0.0.1:8000/'
app.use(router);
app.mount('#app');