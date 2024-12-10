import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import InstructionView from '../views/InstructionView.vue'
import MarkView from '../views/MarkView.vue'
import ThanksView from '../views/ThanksView.vue'
import Error404 from '../views/Error404View.vue'
import AdminPanel from '../views/AdminPanel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/instrukcja',
      name: 'instruction',
      component: InstructionView,
    },
    {
      path: '/oznaczanie',
      name: 'marking',
      component: MarkView,
    },
    {
      path: '/podziekowania',
      name: 'thanks',
      component: ThanksView,
    },
    {
      path: '/404',
      name: '404',
      component: Error404,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel,
    },
  ],
})

export default router
