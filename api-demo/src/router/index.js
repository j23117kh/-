import { createRouter, createWebHistory } from 'vue-router';
import ItemsPage from '../components/ItemsPage.vue';
import ItemDetail from '../components/ItemDetail.vue';

const routes = [
  { path: '/', component: ItemsPage },
  { path: '/items/:id', component: ItemDetail }
];

export default createRouter({
  history: createWebHistory(),
  routes
});