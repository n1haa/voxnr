import { createRouter, createWebHistory } from 'vue-router'
import Welcome from '../welcome.vue'
import CompanyRegistration from '../CompanyRegistration.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: Welcome,
    },
    {
      path: '/register-company',
      name: 'register-company',
      component: CompanyRegistration,
    },
    {
      path: '/employee-auth',
      name: 'employee-auth',
      component: { render: () => null },
    },
  ],
})

export default router