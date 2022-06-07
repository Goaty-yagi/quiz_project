import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'
import axios from 'axios'
import {router} from "../main.js"
import  signup  from './modules/signup'
import  board  from './modules/board'
import  quiz  from './modules/quiz'

let getDefaultState = () => {
  return {
    isLoading: false,
    id: 1,
    field:'',
    num:3,
    questions:[],
    quizzes:[],
    randomURL:'',
    test:null,
    notice:false,
    step:1,
    showModal: false,
    fixedScroll: false,
  }}


export default createStore({
  modules: {
    signup,
    board,
    quiz
  },
  state: getDefaultState(),
  plugins: [
    createPersistedState({
      key: 'quizkey',  // 設定しなければ'vuex'
      paths: [
        "signup.djangoUser",
        "signup.emailVerified",
        "signup.apiError",
        "signup.UID",
        "signup.registeredUser",
        "signup.myQuestion",
        "signup.myQuizInfo",
      ],  // 保存するモジュール：設定しなければ全部。
      storage: window.sessionStorage
    }),
    createPersistedState({
      key: 'quiz-session',
      paths:[
        // "board.answeredQuestion",
        // "board.reccomendedQuestion",
        "board.centerTag",
        "quiz.quizNameId",
        "quiz.fieldNameId",
        ],
      storage: window.sessionStorage
    }),
    createPersistedState({
        key: 'tempKey',  // 設定しなければ'vuex'
        paths: [
          "signup.tempUser",
          "signup.userInfo",
          "signup.beingException",
          "signup.reloadForException",
        ],  // 保存するモジュール：設定しなければ全部。
        storage:{
          getItem:(key) => Cookies.get(key),
          setItem:(key,value) =>
            Cookies.set(key,value, {expires: 3, secure: true}),
          removeItem:(key) => Cookies.remove(key),
        }
      })
  ],
  getters:{
    questions2:(state) => state.questions,
    quizzes2:(state) => state.quizzes,
    showModal:(state) => state.showModal,
    fixedScroll:(state) => state.fixedScroll
  },
  mutations: {
    setIsLoading(state, status) {
      state.isLoading = status
    },
    reset(state) {
      console.log('reset')
      Object.assign(state, getDefaultState())
      router.push('/')
    },
    getURLs(state,item){
      state.num = item.num
      // state.field= field
      state.id = item.status
      state.test = item.test
      state.randomURL = `/quiz/${state.id}`
    },
    
    // getRandomQuestion(state,array){
    //   for (let i = array.length - 1; i >= 0; i--) {
    //     let r = Math.floor(Math.random() * (i + 1))
    //     let tmp = array[i]
    //     array[i] = array[r]
    //     array[r] = tmp
    //     }
    //   for ( let k =0; k < array.length; k++){
    //     for (let i = array[k].answer.length - 1; i >= 0; i--) {
    //       let r = Math.floor(Math.random() * (i + 1))
    //       let tmp = array[k].answer[i]
    //       array[k].answer[i] = array[k].answer[r]
    //       array[k].answer[r] = tmp
    //       }}
    //     return array
    // },
    // setQuestions:(state,questions) => (state.questions = questions),
    // setQuiz:(state,quizzes) => (state.quizzes = quizzes),
    // initial
    testHandler(state){
      state.test = false
    },
    noticeHandler(state){
      state.notice = true
      
    },
    noticeOff(state){
      state.notice = false  
    },
    addStep(state){
      state.step += 1
    },
    stepClear(state){
      state.step = 1
    },
    showModalTrue(state){
      state.showModal = true
    },
    showModalFalse(state){
      state.showModal = false
    },
    fixedScrollTrue(state){
      state.fixedScroll = true
    },
    fixedScrollFalse(state){
      state.fixedScroll = false
    },
    handleFixedScroll(state){
      state.fixedScroll = !state.fixedScroll
    }

    // quizRouter(i,f,n){
    //   state.id = i
    //   state.field = f
    //   state.num = n
    //   return { name: 'Quiz', params:{ id:state.id, field:state.field, num:state.num}}
    // }
  },
  // actions: {
  //   }
})
