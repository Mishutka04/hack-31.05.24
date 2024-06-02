import { createRouter, createWebHashHistory } from 'vue-router';
import Region from './components/Region.vue';
import Division from './components/Division.vue';
import Base from './components/Base.vue';


export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {name: 'base', path: '', component: Base},
        {name: 'region', path: '/region/:category_id/', component: Region},
        {name: 'division', path: '/region/:category_id/division/:division_id/', component: Division},
        
    ]
})