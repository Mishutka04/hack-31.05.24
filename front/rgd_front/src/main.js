import './assets/main.css';
import router from './router';
import { createApp } from 'vue';
import App from './App.vue';
const app = createApp(App);
app.config.globalProperties.$globalUrl = 'https://rzd.firecalculation.ru/'
app.use(router);
app.mount('#app');