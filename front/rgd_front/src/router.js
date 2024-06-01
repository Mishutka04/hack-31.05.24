import { createRouter, createWebHashHistory } from 'vue-router';
import Line from './components/Line.vue';
import Base from './components/Base.vue';
import Google from './components/Google.vue';


export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {name: 'base', path: '', component: Google},
        {name: 'region', path: '/region/:category_id/', component: Line},
        {name: 'division', path: '/region/:category_id/division/:division_id/', component: Base},
        
    ]
})