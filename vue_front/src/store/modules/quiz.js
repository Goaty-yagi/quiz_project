import store from '..'
import {router} from "@/main.js"
import axios from 'axios'


let getDefaultState = () => {
    return {
        isLoading: false,
        quizID: 1,
        numOfQuiz: 3,
        questionField: [1,2],
        level: 1,
        questions:[],
        quiz:[],
        quizNameId:'',
        fieldNameId:'',
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
        quiz:(state) => state.quiz,
        quizNameId:(state) => state.quizNameId,
        fieldNameId:(state) => state.fieldNameId
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
        setTestQuestions:(state,questions) => (state.questions = questions),
        getQuiz(state, payload){
            state.quiz = payload
            console.log(state.quiz)
        },
        getQuizInfo(state, quizInfo){
            console.log('GQIStore',quizInfo)
            state.questionField = []
            state.quizID = ''
            state.numOfQuiz = ''
            state.quizID = quizInfo.quizId
            if(quizInfo.fieldId){
                state.questionField = quizInfo.fieldId
            }
            state.numOfQuiz = quizInfo.quizNum
            console.log('GQINFOStore',state.quizID,state.questionField)
        },
        getTestQuizInfo(state, quizInfo){
            state.quizID = quizInfo.quizId
            state.level = quizInfo.level
        },
        setQuizNameId(state, payload){
            state.quizNameId = payload
        },
        setFieldNameId(state, payload){
            state.fieldNameId = payload
        },
        // clearQuiz(state, payload){
        //     console.log('in_cleared')
        //     state.questions = []
        //     state.quiz = []
        //     console.log('cleared')
        // }
    },
    actions:{
        async getquestions({ state, commit }){
            console.log('action2',state.num)
            state.questions = []
            state.quiz = []
            commit('setIsLoading', true, {root:true})
            if(state.questionField[0]){
                var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}&field=${state.questionField}`)
            }else{
                var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}`)
            }
            commit('getQuiz',response.data[0])
            response.data.shift()
            commit('getRandomQuestion',response.data)
            commit('setQuestions',response.data);
            commit('setIsLoading', false,{root:true})
        },
        async getQuizNameId({ state, commit }){
            if(state.quizNameId==false){
                commit('setIsLoading', true, {root:true})
                let response = await axios.get("/api/quizzes-name-id/")
                commit('setQuizNameId',response.data)
                console.log(state.quizNameId)
                commit('setIsLoading', false,{root:true})
            }
        },
        async getFieldNameId({ state, commit }){
            if(state.fieldNameId==false){
                commit('setIsLoading', true, {root:true})
                let response = await axios.get("/api/field-list/")
                commit('setFieldNameId',response.data)
                console.log(state.fieldNameId)
                commit('setIsLoading', false,{root:true})
            }
        },
        async getTestQuestions({ state, commit }){
            commit('setIsLoading', true, {root:true})
            let response = await axios.get(`/api/quizzes-tests/?quiz=${state.quizID}&level=${state.level}`)
            commit('getQuiz',response.data[0])
            response.data.shift()
            commit('getRandomQuestion',response.data)
            commit('setTestQuestions',response.data);
            commit('setIsLoading', false,{root:true})
        },
    }
}