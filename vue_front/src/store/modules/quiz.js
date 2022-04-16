import store from '..'
import {router} from "@/main.js"
import axios from 'axios'


let getDefaultState = () => {
    return {
        isLoading: false,
        quizID: 1,
        numOfQuiz: 5,
        questionField: [1,2],
        questions:[],
        quiz:[],
        randomURL:'',
        test:null,
        notice:false,
        step:1,
    }
}

export default {
    namespace: true,
    state: getDefaultState(),
    getters:{
        questions:(state) => state.questions,
        quiz:(state) => state.quiz
    },
    mutations:{
        getRandomQuestion(state,array){
            console.log('in randomQ', array)
            // for (let i = array.length - 1; i >= 0; i--) {
            //     let r = Math.floor(Math.random() * (i + 1))
            //     let tmp = array[i]
            //     array[i] = array[r]
            //     array[r] = tmp
            // }
            for ( let k =0; k < array.length; k++){
                for (let i = array[k].answer.length - 1; i >= 0; i--) {
                    let r = Math.floor(Math.random() * (i + 1))
                    let tmp = array[k].answer[i]
                    array[k].answer[i] = array[k].answer[r]
                    array[k].answer[r] = tmp
                }
            }
            return array
        },
        setQuestions:(state,questions) => (state.questions = questions),
        getQuiz(state, payload){
            state.quiz = payload
            console.log(state.quiz)
        },
        getQuizInfo(state, {quizid,questionfield}){
            state.questionField = []
            state.quizID = quizid
            state.questionField = questionfield
            console.log('',state.quizID,state.questionField)
        }
    },
    actions:{
        async getquestions({ state, commit }){
            console.log('action2',state.num)
            commit('setIsLoading', true, {root:true})
            
              let response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}&field=${state.questionField}`)
              commit('getQuiz',response.data[0])
              response.data.shift()
              commit('getRandomQuestion',response.data)
              commit('setQuestions',response.data);
              commit('setIsLoading', false,{root:true})
            }
    }
}