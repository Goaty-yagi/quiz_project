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
import Dboard from '../views/Dboard.vue'
import Login from '../views/Login.vue'
import Policy from '../views/Policy.vue'
import Community from '../views/Community.vue'
import BoardDetail from '../views/BoardDetail.vue'
import RelatedQuestion from '../views/board/RelatedQuestion.vue'
import BoardAccount from '../views/board/BoardAccount.vue'
import TermsAndConditions from '../views/footer-contents/TermsAndConditions.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
//   {
//     path: '/quiz',
//     // path: '/quiz/:id',
//     name: 'Quiz',
//     component: Quiz
//   },
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
    meta:{quizTook:true,emailVerified:true,compUser:true,beingException:true}
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
    path: '/dboard',
    name: 'Dboard',
    component: Dboard
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    meta:{emailVerified:true,compUser:true,beingException:true}
  },
  {
    path: '/account',
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
    meta:{emailVerified:true,compUser:true,beingException:true}
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy,
  },
  {
    path: '/terms-and-conditions',
    name: 'terms-and-conditions',
    component: TermsAndConditions,
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
    name: 'catchAll',
    component: NotFound,
    // meta:{emailVerified:true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


// there are 6 types of way, 
// 1 is not non registered user 
// => can go community except Caccount and some error or login
// 2 is not registered but took init tes
// => the same as avobe but not include quiz-init
// 3 is registerd firebase but not djangoUser(comes from error)
// => can only go to connection error
// 4 is registered complitely but not emailVerified
// => can't go signup, login, Caccount, quiz-init
// 5 registered user
// => can't go signup,login quiz-init
// 6 can't go quiz-test if took already

router.beforeEach((to, from, next) => {
    // this is for 1
    console.log("router",!store.state.signup.emailVerified&&store.state.signup.registeredUser,store.state.signup.registeredUser)
    if (to.matched.some(record => record.meta.login) && !store.state.signup.djangoUser) {
    console.log("LOGIN",to.matched)
    next({ name: 'Login' });
    }
    // this is for 2
    else if(to.matched.some(record => record.meta.quizTook)&&store.state.signup.tempUser.test){
        console.log("LOGIN",to.matched)
        next({ name: 'Login' });
      }
    //  this is for 3
    else if(to.matched.some(record => record.meta.apiException==false)&&store.state.signup.apiError.any){
      console.log("BeingException",to.matched)
      next({ name: 'ConnectionError' });
      }
    //   this is for 4 next will be chainge to new not found im gonna male later
    else if(to.matched.some(record => record.meta.emailVerified)&&!store.state.signup.emailVerified&&store.state.signup.registeredUser){
    console.log("NOTFOUND",to.matched)
    next({ name: 'NotFound' });
    }
    // this is for 5 next will be chainge to new not found im gonna male later
    else if(to.matched.some(record => record.meta.compUser)&&store.state.signup.emailVerified){
        console.log("NOTFOUND",to.matched)
        next({ name: 'NotFound' });
    }
    else {
    console.log('else',to.matched,'D',store.state.signup.djangoUser,"U",store.state.signup.user)
    next()
  }
})

export default router
