import store from '..'
import axios from 'axios'

export default {
    namespace: true,
    state: {
        title:'',
        description:'',
        selectedTagList:'',
        relatedQuestion:'',
        searchedQuestions:'',
        notifications:{
            reply: false,
            answer: false,
            post: false,
        },
    },
    mutations:{
        resetNotifications(state){
            console.log("in_reset")
            state.notifications.answer = false
            state.notifications.reply = false
            state.notifications.post = false
        },
        getTitle(state,payload){
            state.title = payload
            console.log('Got title',state.title)
        },
        getDescription(state, payload){
            state.description = payload
            console.log('Got description',state.description)
        },
        // getSelectedTagList(state, payload){
        //     state.selectedTagList = payload
        // },
        getRelatedQuestion(state, payload){
            state.relatedQuestion = payload
            console.log("commited relatedQ",state.relatedQuestion )
        },
        getTagList(state, payload){
                state.selectedTagList = payload
                console.log('Got tagID',state.selectedTagList)
        },
        // getWordList(state, payload){
        //     state.wordList = payload
        // }
    },
    
    actions:{
        handleNotifications(context, payload){
            console.log("in_handle",payload)
            if(payload == "reply"){
                context.state.notifications.reply = true
                setTimeout(context.commit, 3000,"resetNotifications")      
            }
            if(payload == "answer"){
                context.state.notifications.answer = true
                setTimeout(context.commit, 3000,"resetNotifications")
            }
            if(payload == "post"){
                context.state.notifications.post = true
                setTimeout(context.commit, 3000,"resetNotifications")
            }
        },
        async getSearchQuestion(state,payload){
            console.log('Gsearch',payload)
            
            await axios
                .get(`/api/board/question/search/?keyword=${payload}`)
                .then(response => {
                    state.searchedQuestions = response.data
                    console.log("response_searched",state.searchedQuestions)
                })
                .catch(error => {
                    console.log(error)
                })
        },          
        // async getSearchQuestion({ state, commit }){
        //     await axios({
        //         method: 'get',
        //         url: `/api/board/question/search/`,
        //         data: {
        //             keyword: state.searchKeywords
        //         },
        //     })
        //     .then()
        //     .catch(error => {
        //         console.log(error)
        //     })
        // },          
    }


}