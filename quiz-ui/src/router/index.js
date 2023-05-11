import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/new-quiz-page',
      name: 'NewQuizPage',
      component: () => import('../views/NewQuizPage.vue')
    },
    {
      path:'/questions',
      name: 'QuestionsManager',
      component: () => import('../views/QuestionsManager.vue')
    },
    {
      path:'/score-page',
      name:'ScorePage',
      component: () => import('../views/ScorePage.vue')
    }
  ]
})

export default router
