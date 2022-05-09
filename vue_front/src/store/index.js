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
        "signup.UID",
      ],  // 保存するモジュール：設定しなければ全部。
      storage: window.sessionStorage
    }),
    createPersistedState({
      key: 'quiz-session',
      paths:[
        "board.answeredQuestion",
        "board.reccomendedQuestion",
        "board.centerTag",
        "quiz.quizNameId",
        "quiz.fieldNameId"],
      storage: window.sessionStorage
    }),
    createPersistedState({
        key: 'tempKey',  // 設定しなければ'vuex'
        paths: [
          "signup.tempUser",
          "signup.userInfo",
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
    quizzes2:(state) => state.quizzes
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
    // deleteTempUser(){
    //     Cookies.remove('tempKey')
    //     console.log("deleted")
    // },
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
    // quizRouter(i,f,n){
    //   state.id = i
    //   state.field = f
    //   state.num = n
    //   return { name: 'Quiz', params:{ id:state.id, field:state.field, num:state.num}}
    // }
  },
  // actions: {
  //   async getquiz2({ state, commit }){
  //     let response = await axios.get(`/api/quizzes/?id=${state.id}`)
  //     .catch(error => {
  //       console.log('error',error.message)
  //                        })
  //     commit('setQuiz',response.data);
  //     console.log('action',response.data)
  //     console.log(state.isLoading)
  //     },
  //   async getquestions2({ state, commit }){
  //     console.log('action2',state.num)
  //     try{
  //       let response2 = await axios.get(`/api/questions/quizzes/?quiz=${state.id}&num=${state.num}`)
  //       commit('getRandomQuestion',response2.data)
  //       commit('setQuestions',response2.data);
  //       // commit('setIsLoading', false)
  //     }
  //     catch{
  //       commit('setIsLoading', false)
  //       router.push({ name: 'Notfound' })
        
  //                        }
      
  //   },
  // },
})
