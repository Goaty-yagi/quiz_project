import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Quiz from '../views/Quiz.vue'
import QuizTest from '../views/quiz/QuizTest.vue'
import QuizPractice from '../views/quiz/QuizPractice.vue'
import QuizHome from '../views/quiz/QuizHome.vue'
import Test from '../views/Test.vue'
import NotFound from '../views/not-found/NotFound.vue'
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
    component: Home,
  },
  {
    path: '/quiz',
    // path: '/quiz/:id',
    name: 'Quiz',
    component: Quiz
  },
  {
    path: '/quiz-home',
    name: 'QuizHome',
    component: QuizHome,
    meta:{login:true}
    
  },
  {
    path: '/quiz-test',
    // path: '/quiz/:id',
    name: 'QuizTest',
    component: QuizTest,
    meta:{login:true}
  },
  {
    path: '/quiz-practice',
    name: 'QuizPractice',
    component: QuizPractice,
    meta:{login:true}
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
    meta:{emailVerified:true}
  },
  {
    path: '/account/:uid',
    name: 'Account',
    component: Account,
    meta:{login:true}
  },
  {
    path: '/board',
    name: 'Community',
    component: Community,
  },
  {
    path: '/board/related',
    name: 'RelatedQuestion',
    component: RelatedQuestion,
  },
  {
    path: '/board/account',
    name: 'BoardAccount',
    component: BoardAccount,
    meta:{login:true,emailVerified:true}
  },
  {
    path: '/board-detail/:slug',
    name: 'BoardDetail',
    component: BoardDetail,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta:{emailVerified:true}
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy,
    meta:{login:true}
  },
  { 
    path: '/notfound',
    name: 'NotFound',
    component: NotFound,
    // 
  },
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
    if (to.matched.some(record => record.meta.login) && !store.state.signup.user) {
    console.log("LOGIN",to.matched)
    next({ name: 'Login' });
    }
    else if(to.matched.some(record => record.meta.emailVerified)&&!store.state.signup.emailVerified&&store.state.signup.user){
    console.log("NOTFOUND",to.matched)
    next({ name: 'NotFound' });
    }
    else {
    console.log('else',to.matched)
    next()
  }
})

export default router
