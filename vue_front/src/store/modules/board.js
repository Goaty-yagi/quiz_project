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
        reccomendedQuestion:'',
        // favoriteQuestion:'',
        notifications:{
            reply: false,
            answer: false,
            post: false,
        },
    },
    getters:{
        user(state, getters, rootState){
            return rootState.signup.djangoUser
        },
        getUserTags(state, getters){
            let checkDict = {}  
            // let checkedDict = {}
            let checkedList = []
            let checkedlist2 = []
            for(let i of getters.user.user_tag){
                checkDict[i.tag] = i.total_num
                checkedList.push(i.tag)
            }
            console.log("computed",checkDict)
            if(Object.keys(checkDict).length <= 3){
                return checkedList
            }
            if(Object.keys(checkDict).length > 3){
                for(let m=0; m < 3; m++){
                    const aryMax = function (a, b) {return Math.max(a, b);}
                    let max = Object.values(checkDict).reduce(aryMax);
                    const result = Object.keys(checkDict).reduce( (r, key) => { 
                        return checkDict[key] === max ? key : r 
                        }, null);
                    // checkedDict[result] = max
                    delete checkDict[result]
                    checkedlist2.push(result)
                }
                return checkedlist2
            }
        }
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
        async getRelatedQuestion({ state , getters }, payload) {
            // this.$store.commit('setIsLoading', true)
            console.log("ingetRQ in store")
            if(getters.getUserTags.length == 1){
                var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}`
            }
            if(getters.getUserTags.length == 2){
                var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}`
            }
            if(getters.getUserTags.length == 3){
                var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}&tag=${getters.getUserTags[2]}`
            }
            console.log("url:",url)
            try{
                await axios.get(url)
                    .then(response => {
                    state.reccomendedQuestion = response.data
                    console.log(state.reccomendedQuestion.length,state.reccomendedQuestion)
                    })
                }
            catch{(error => {
                    console.log(error)
            })}
            // this.$store.commit('setIsLoading', false)
        },
        // async getFavoriteQuestion({ state , getters }, payload){
        //     const questionId = []
        //     for(let i of getters.user.question){
        //         questionId.push(i.id)
        //     }
        //     await axios
        //     .get(`/api/board/question-favorite?question_id=${questionId}`)
        //     .then(response => {
        //         state.favoriteQuestion = response.data
        //         console.log('GetFQ', state.favoriteQuestion)
        //         })
        //     .catch(error => {
        //         console.log(error)
        //     })
        // },
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