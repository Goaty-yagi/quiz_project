import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Quiz from '../views/Quiz.vue'
import Test from '../views/Test.vue'
import NotFound from '../views/NotFound.vue'
import Signin from '../views/Signin.vue'
import Account from '../views/Account.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/quiz/:id',
    name: 'Quiz',
    component: Quiz
  },
  {
    path: '/test/:slug',
    name: 'Test',
    component: Test
  },
  { 
    path: '/norfound',
    name: 'Notfound',
    component: NotFound 
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/account',
    name: 'Account',
    component: Account
  },
  { 
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: NotFound 
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
