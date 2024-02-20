import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from "../views/LoginPage.vue";
import PollView from "@/views/PollView.vue";


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  { path: "/signin", component: LoginPage },
  { path: "/poll/:id", component: PollView },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
