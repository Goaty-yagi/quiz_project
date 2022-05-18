import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Quiz from '../views/Quiz.vue'
import QuizTest from '../views/quiz/QuizTest.vue'
import QuizTestInit from '../views/quiz/QuizTestInit.vue'
import QuizPractice from '../views/quiz/QuizPractice.vue'
import QuizHome from '../views/quiz/QuizHome.vue'
import MyQuiz from '../views/quiz/MyQuiz.vue'
import Test from '../views/Test.vue'
import NotFound from '../views/not-found/NotFound.vue'
import NotFound404 from '../views/not-found/NotFound404.vue'
import ConnectionError from '../views/not-found/ConnectionError.vue'
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
    meta:{login:true,beingException:true}
    
  },
  {
    path: '/quiz-test',
    name: 'QuizTest',
    component: QuizTest,
    meta:{login:true}
  },
  {
    path: '/quiz-test-init',
    name: 'QuizTestInit',
    component: QuizTestInit,
    meta:{emailVerified:true,beingException:true}
  },
  {
    path: '/quiz-practice',
    name: 'QuizPractice',
    component: QuizPractice,
    meta:{login:true,beingException:true}
  },
  {
    path: '/my-quiz',
    name: 'MyQuiz',
    component: MyQuiz,
    meta:{login:true,beingException:true}
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
    meta:{emailVerified:true,beingException:true}
  },
  {
    path: '/account/:uid',
    name: 'Account',
    component: Account,
    meta:{login:true,beingException:true}
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
    meta:{login:true,emailVerified:true,beingException:true}
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
    meta:{emailVerified:true,beingException:true}
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy,
  },
  { 
    path: '/notfound',
    name: 'NotFound',
    component: NotFound,
  },
  { 
    path: '/notfound404',
    name: 'NotFound404',
    component: NotFound404,
  },
  { 
    path: '/connection-error',
    name: 'ConnectionError',
    component: ConnectionError,
  },
  { 
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: NotFound,
    meta:{emailVerified:true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.login) && !store.state.signup.djangoUser) {
    console.log("LOGIN",to.matched)
    next({ name: 'Login' });
    }
    // else if(to.matched.some(record => record.meta.beingException)&&store.state.signup.beingException){
    //   console.log("BeingException",to.matched)
    //   next({ name: 'NotFound404' });
    //   }
    else if(to.matched.some(record => record.meta.apiException==false)&&store.state.signup.apiError.any){
      console.log("BeingException",to.matched)
      next({ name: 'ConnectionError' });
      }
    else if(to.matched.some(record => record.meta.emailVerified)&&!store.state.signup.emailVerified&&store.state.signup.user){
    console.log("NOTFOUND",to.matched)
    next({ name: 'NotFound' });
    }
    else {
    console.log('else',to.matched,'D',store.state.signup.djangoUser,"U",store.state.signup.user)
    next()
  }
})

export default router
