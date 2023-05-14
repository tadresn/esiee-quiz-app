import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/user/HomePage.vue'
import quizApiService from '../services/QuizApiService'

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
      component: () => import('../views/user/NewQuizPage.vue')
    },
    {
      path:'/questions',
      name: 'QuestionsManager',
      component: () => import('../views/user/QuestionsManager.vue')
    },
    {
      path:'/score-page',
      name:'ScorePage',
      component: () => import('../views/user/ScorePage.vue')
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('../views/admin/Admin.vue'),
      beforeEnter: (to, from, next) => {
        if(!quizApiService.isAuthorized() && to.name !== 'LoginPage'){
          next({name: 'LoginPage'});
        } else{
          next();
        }
      },
      children: [
        {
          path: 'login-page',
          name: 'LoginPage',
          component: () => import('../views/admin/LoginPage.vue')
        },
        {
          path: '',
          name: 'HomeAdminPage',
          component: () => import('../views/admin/HomeAdminPage.vue')
        },
        {
          path:'add-question',
          name: "AddQuestion",
          component: () => import('../views/admin/AddQuestion.vue')
        }
      ]
    }
  ]
})

export default router
