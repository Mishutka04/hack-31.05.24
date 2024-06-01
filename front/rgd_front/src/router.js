import { createRouter, createWebHashHistory } from 'vue-router';
import Line from './components/Line.vue';
import Base from './components/Base.vue';
import Google from './components/Google.vue';


export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {name: 'base', path: '', component: Google},
        {name: 'line', path: '/route/:category_id/', component: Line},
        {name: 'google', path: '/google/', component: Google},
        
    ]
})