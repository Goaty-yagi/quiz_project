import store from '..'
import {router} from "@/main.js"
import axios from 'axios'


let getDefaultState = () => {
    return {
        isLoading: false,
        quizID: 1,
        numOfQuiz: 3,
        questionField: [1,2],
        questions:[],
        quizzes:[],
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
        questions:(state) => state.questions
        // quizzes:(state) => state.quizzes
    },
    mutations:{
        getRandomQuestion(state,array){
            console.log('in randomQ', array)
            for (let i = array.length - 1; i >= 0; i--) {
                let r = Math.floor(Math.random() * (i + 1))
                let tmp = array[i]
                array[i] = array[r]
                array[r] = tmp
            }
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
    },
    actions:{
        async getquestions({ state, commit }){
            console.log('action2',state.num)
            
              let response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}&field=${state.questionField}`)
              console.log('response1',typeof(response.data))
              commit('getRandomQuestion',response.data[1])
              commit('setQuestions',response.data);
              commit('setIsLoading', false)
              console.log('response',response)
            }
            
    }
}