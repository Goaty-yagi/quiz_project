import store from '..'
import {router} from "@/main.js"
import axios from 'axios'


let getDefaultState = () => {
    return {
        isLoading: false,
        quizID: 1,
        countUpDict:{
            questionID: '',
            answerID: '',
            questionType:''
        },
        userStatusDict:{
            status:'',
            grade:'',
            quizTaker:'',
            isCorrect:0,
            isFalse:0
        },
        currentQuizMode:{
            myQuiz: false,
            practice: false,
            test: false
        },
        gradeForConvert:'',
        numOfQuiz: 3,
        questionField: [1,2],
        level: 1,
        questions:[],
        quiz:[],
        quizNameId:'',
        fieldNameId:'',
        questionTypeId:'',
        statusNameId:'',
        randomURL:'',
        test:null,
        notice:false,
        step:1,
        // onQuiz is for footer view 
        onQuiz: false,
        // myQuestion: ''
    }
}

export default {
    namespace: true,
    state: getDefaultState(),
    getters:{
        questions:(state) => state.questions,
        quiz:(state) => state.quiz,
        quizNameId:(state) => state.quizNameId,
        fieldNameId:(state) => state.fieldNameId,
        statusNameId:(state) => state.statusNameId,
        gradeForConvert:(state) => state.gradeForConvert,
        currentQuizMode:(state) => state.currentQuizMode,
        questionTypeId:(state) => state.questionTypeId,
        quizTaker(state, getters, rootState){
            try{
                return rootState.signup.djangoUser.quiz_taker[0].id
            }catch{
                return null
            }
        },
        quizTakerObject(state, getters, rootState){
            try{
                return rootState.signup.djangoUser.quiz_taker[0]
            }catch{
                return null
            }
        },
        quizID(state, getters, rootState){
            try{
                return rootState.signup.djangoUser.quiz_taker[0].grade
            }catch{
                return null
            }
        },
        // myQuestion(state, getters, rootState){
        //     state.myQuestion = rootState.signup.djangoUser.my_quiz[0].my_question
        //     console.log("myquestion",state.myQuestion)
        // }
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
        setAnswerAndQuestionID(state,IDs){
            state.countUpDict.questionID = IDs.questionID
            state.countUpDict.answerID = IDs.answerID
            state.countUpDict.questionType = IDs.questionType
        },
        getQuizInfo(state, quizInfo){
            state.questionField = []
            state.quizID = ''
            state.numOfQuiz = ''
            state.quizID = quizInfo.quizId
            if(quizInfo.fieldId){
                state.questionField = quizInfo.fieldId
            }
            state.numOfQuiz = quizInfo.quizNum
        },
        getTestQuizInfo(state, quizInfo){
            console.log('in',quizInfo)
            state.quizID = quizInfo.quizId
            state.level = quizInfo.level
            console.log('setQ-quiz id and level',state.quizID,state.level)
        },
        setQuizId(state){
        },
        setQuizNameId(state, payload){
            state.quizNameId = payload
        },
        setFieldNameId(state, payload){
            state.fieldNameId = payload
        },
        setStatusNameId(state, payload){
            state.statusNameId = payload
        },
        setQuestionTypeId(state, payload){
            state.questionTypeId = payload
        },
        getUserStatusInfo(state, payload){
            state.userStatusDict.status = payload.status
            // state.userStatusDict.grade = payload.grade
            // state.userStatusDict.quiz_taker = payload.quiz_taker
            state.userStatusDict.isCorrect = payload.isCorrect
            state.userStatusDict.isFalse = payload.isFalse
            console.log("GUSI",state.userStatusDict)
        },
        // getUserStatusInfoForInit(state, payload){
        //     state.userStatusDict.status = payload.status
        //     // state.userStatusDict.grade = payload.grade
        //     // state.userStatusDict.quiz_taker = payload.quiz_taker
        //     state.userStatusDict.isCorrect = payload.isCorrect
        //     state.userStatusDict.isFalse = payload.isFalse
        //     console.log("GUSI",state.userStatusDict)
        // },
        setQuizID(state, payload){
            state.userStatusDict.grade = payload
            console.log('setQuizID',state.userStatusDict.grade)
        },
        setQuizTakerID(state, payload){
            state.userStatusDict.quizTaker = payload
        },
        convertGradeFromIntToID(state, payload){
            for(let i of state.quizNameId){
                if(i.name == payload){
                    state.gradeForConvert = i.id
                }
            }
        },
        convertGradeFromIDToInt(state, payload){
            for(let i of state.quizNameId){
                if(i.id == payload){
                    state.gradeForConvert = i.name
                }
            }
        },
        onQuizTrue(state){
            state.onQuiz = true
        },
        onQuizFalse(state){
            state.onQuiz = false
        },
        handleCurrentQuizMode(state,payload){
            for (let i of state.currentQuizMode){
                console.log('CQM',i)
                if(i == payload){
                    state.currentQuizMode[i] = true
                }
            }
        },
        setQuizIdAndlevel(state, getters){
            console.log('GEETERS',getters)
            state.quizID = getters.grade
            state.level = getters.level
            console.log("SQIAL",state.level,state.quizID)
        }
    },
    actions:{
        async getquestions({ state, commit,getters }){
            console.log('action2',state.quizID,state.level)
            state.questions = []
            state.quiz = []
            commit('setIsLoading', true, {root:true})
            if(state.questionField[0]){
                var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}&field=${state.questionField}`)
            }else{
                var response = await axios.get(`/api/quizzes-questions/?quiz=${state.quizID}&num=${state.numOfQuiz}`)
            }
            console.log(getters.quizTaker)
            commit('setQuizTakerID',getters.quizTaker)
            commit('getQuiz',response.data[0])
            commit('setQuizID',response.data[0].name)
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
        async getStatusNameId({ state, commit }){
            if(state.statusNameId==false){
                commit('setIsLoading', true, {root:true})
                let response = await axios.get("/api/status-list/")
                commit('setStatusNameId',response.data)
                commit('setIsLoading', false,{root:true})
            }
        },
        async getQuestionTypeId({ state, commit }){
            console.log('question-type1')
            if(state.questionTypeId==false){
                console.log('question-type')
                commit('setIsLoading', true, {root:true})
                let response = await axios.get("/api/question-types")
                commit('setQuestionTypeId',response.data)
                commit('setIsLoading', false,{root:true})
                console.log('inGet',state.questionTypeId)
            }
        },
        async getTestQuestions({ state, commit, getters }){
            // need things for non login
            console.log('getquestioninfo',state.que)
            if(getters.quizID!=null){
                // quiz_taker exist
                console.log('true')
                commit('setIsLoading', true, {root:true})
                let response = await axios.get(`/api/quizzes-tests/?quiz=${state.quizID}&level=${state.level}`)
                commit('getQuiz',response.data[0])
                commit('setQuizTakerID',getters.quizTaker)
                commit('setQuizID',response.data[0].name)
                response.data.shift()
                commit('getRandomQuestion',response.data)
                commit('setTestQuestions',response.data);
                commit('setIsLoading', false,{root:true})
            }else{
                // first questions in init
                commit('setIsLoading', true, {root:true})
                let response = await axios.get(`/api/quizzes-tests/?quiz=4&level=${state.level}`)
                commit('getQuiz',response.data[0])
                response.data.shift()
                commit('getRandomQuestion',response.data)
                commit('setTestQuestions',response.data);
                commit('setIsLoading', false,{root:true})
            }
        },
        async countUpAnswerAndQuestion({ state , commit }, payload){
            // commit('setIsLoading', true, {root:true})
            commit('setAnswerAndQuestionID',payload)
            if(state.countUpDict.questionType!=4){
                await axios.patch(`/api/answers-count/?answer=${state.countUpDict.answerID}&question=${state.countUpDict.questionID}`)
            }
            // commit('setIsLoading', false,{root:true})
            
        },
        async userStatusPost({ state , commit }, payload){
            console.log("userStatusPost",state.userStatusDict)
            commit('getUserStatusInfo',payload)
            await axios({
                method: 'post',
                url: '/api/user-status/',
                data: {
                    status: state.userStatusDict.status,
                    grade: state.userStatusDict.grade,
                    quiz_taker: state.userStatusDict.quizTaker,
                    is_correct: state.userStatusDict.isCorrect,
                    is_false: state.userStatusDict.isFalse,
                }
            })
        },
        async createAndDeleteMyQuiz({ state , commit }, payload){
            console.log("inMY",payload)
            await axios({
                method: 'post',
                url: '/api/my-question/',
                data: {
                    my_quiz: payload.myQuiz,
                    question: payload.question
                }
            })
        },
        async convertGradeFromIntToIDForNewUser({ state , dispatch, commit }, payload){
            if(!state.quizNameId){
                await dispatch('getQuizNameId')
            }
            commit('convertGradeFromIntToID', payload)
            console.log('done convert')
        },
        setQuizIdAndlevelAction({ state , commit, getters }){
            commit('setQuizIdAndlevel', getters.quizTakerObject)
            console.log('donene')
        },
    }
}