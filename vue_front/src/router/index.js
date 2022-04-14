import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Quiz from '../views/Quiz.vue'
import QuizTest from '../views/quiz/QuizTest.vue'
import QuizPractice from '../views/quiz/QuizPractice.vue'
import Test from '../views/Test.vue'
import NotFound from '../views/NotFound.vue'
import Signup from '../views/Signup.vue'
import Account from '../views/Account.vue'
import Login from '../views/Login.vue'
import Policy from '../views/Policy.vue'
import Community from '../views/Community.vue'
import BoardDetail from '../views/BoardDetail.vue'
import RelatedQuestion from '../views/board/RelatedQuestion.vue'
import BoardAccount from '../views/board/BoardAccount.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/quiz',
    // path: '/quiz/:id',
    name: 'Quiz',
    component: Quiz
  },
  {
    path: '/quiz-test',
    // path: '/quiz/:id',
    name: 'QuizTest',
    component: QuizTest
  },
  {
    path: '/quiz-practice',
    // path: '/quiz/:id',
    name: 'QuizPractice',
    component: QuizPractice
  },
  {
    path: '/test',
    name: 'Test',
    component: Test
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/account/:uid',
    name: 'Account',
    component: Account,
    // meta:{requireLogin: true}
  },
  {
    path: '/board',
    name: 'Community',
    component: Community
  },
  {
    path: '/board/related',
    name: 'RelatedQuestion',
    component: RelatedQuestion
  },
  {
    path: '/board/account',
    name: 'BoardAccount',
    component: BoardAccount
  },
  {
    path: '/board-detail/:slug',
    name: 'BoardDetail',
    component: BoardDetail
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy
  },
  // { 
  //   path: '/norfound',
  //   name: 'Notfound',
  //   component: NotFound 
  // },
  // { 
  //   path: '/:catchAll(.*)',
  //   name: 'NotFound',
  //   component: NotFound 
  // }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.signup.user) {
    next({ name: 'Login' });
  } else {
    next()
  }
})

export default router
