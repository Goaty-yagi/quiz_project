import store from '..'
import axios from 'axios'
import { extractIdentifiers } from '@vue/compiler-core'

export default {
    namespace: true,
    state: {
        title:'',
        description:'',
        selectedTagList:'',
        relatedQuestion:'',
        searchedQuestions:'',
        reccomendedQuestion:'',
        answeredQuestion:'',
        // favoriteQuestion:'',
        notificationApi:'',
        showNoticeOnAcount:{
            answer:false,
            reply:false,
        },
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
        gettersAnsweredQuestions(state){
            return state.answeredQuestion
        },
        gettersReccomendedQuestion(state){
            return state.reccomendedQuestion
        },
        gettersAnswer(state){
            return state.showNoticeOnAcount.answer
        },
        gettersReply(state){
            return state.showNoticeOnAcount.reply
        },
        // notificationApi(state){
        //     return state.notificationApi
        // },
        getUserTags(state, getters){
            if(getters.user){
                let checkDict = {}  
                // let checkedDict = {}
                let checkedList = []
                let checkedlist2 = []
                for(let i of getters.user.user_tag){
                    checkDict[i.tag.id] = i.total_num
                    checkedList.push(i.tag)
                    // console.log('loop',Object.keys(checkDict).length,checkDict)
                }
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
        notificationApi(state){
            console.log('NAPI',state.notificationApi.length)
            var noty = state.notificationApi
            if(noty.length==0){
                return false
            }
            else if(noty.length==1){
                for(let i of noty.length[0]){
                    console.log(i)
                    if(i.on_answer||i.on_reply){
                        return true
                    }else{
                        return false
                    }
                }
            }
            else if(noty.length==2){
                console.log("d2desu",noty[0])
                for(let o of noty[0]){
                    console.log(o)
                    if(o.on_answer||o.on_reply){
                        return true
                    }else{
                        for(let k of noty[1]){
                            if(k.on_reply){
                                return true
                            }
                            else{
                                return false
                            }
                        }
                    }
                }
            }
        },        
        // handleOnReplyAndOnAnswer(state, getters, rootState){
        //     console.log("handleOnREPLY")
        //     for(let question of getters.gettersAnsweredQuestions){
        //         for(let answer of question.answer){
        //             if(answer.on_reply==true&&answer.user.UID==getters.user.UID){
        //                 return  true
        //             }else{
        //                 return false
        //             }
        //         }
        //     }
        //     console.log("end")
        // },
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
        setReccomendedQuestion(state, payload){
            state.reccomendedQuestion = payload
            console.log('set-reccomendedQuestion')
        },
        setRelatedQuestion(state, payload){
            state.relatedQuestion = payload
            console.log("commited relatedQ",state.relatedQuestion )
        },
        getTagList(state, payload){
                state.selectedTagList = payload
                console.log('Got tagID',state.selectedTagList)
        },
        // handleOnReplyAndOnAnswer(state, getters){
        //     // this is for community_page to display if user have notifications
        //     console.log('inHandleAR in store')
        //     for(let question2 of getters.question){
        //         if(question2.on_answer==true&&question2.user.UID==getters.UID){
        //             console.log("onAnswer_dayo")
        //             state.showNoticeOnAcount.answer = true
        //         }else{
        //             state.showNoticeOnAcount.answer = false
        //         }
        //     }
        //     console.log("answercheck start")
        //     let answeredQuestion = getters.question
        //     for(let question of answeredQuestion){
        //         console.log(question)
        //         for(let answer of question.answer){
        //             console.log(answer.id)
        //             if(answer.on_reply==true&&answer.user.UID==getters.UID){
        //                 console.log("onreply_dayo")
        //                 state.showNoticeOnAcount.reply = true
        //             }
        //         }
        //     }
        // },
    },
    
    actions:{
        commitHandleOnReplyAndOnAnswer({commit,getters}){
            commit('handleOnReplyAndOnAnswer', getters.user)
        },
        handleNotifications(context, payload){
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
            await axios
                .get(`/api/board/question/search/?keyword=${payload}`)
                .then(response => {
                    state.searchedQuestions = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async getRelatedQuestion({ state , getters, commit }, payload) {
            // for reccomended-question, if user and user.user_tag exist, get reccomended-question.
            // else, get question-viewed-order.
            
            if(getters.user){
                try{
                    if(getters.getUserTags.length == 1){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&uid=${getters.user.UID}`
                    }
                    if(getters.getUserTags.length == 2){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}&uid=${getters.user.UID}`
                    }
                    if(getters.getUserTags.length == 3){
                        var url = `/api/board/question/filter-list?tag=${getters.getUserTags[0]}&tag=${getters.getUserTags[1]}&tag=${getters.getUserTags[2]}&uid=${getters.user.UID}`
                    }
                    else{
                        var url = '/api/board/question-viewed-order'
                    }
                }
                catch{
                    var url = '/api/board/question-viewed-order'  
                }
            }else{
                var url = '/api/board/question-viewed-order'
            }
            try{
                console.log("try2",url)
                await axios.get(url)
                    .then(response => {
                        commit('setReccomendedQuestion', response.data)
                    // state.reccomendedQuestion = response.data
                    })
                }
            catch{(error => {
                    console.log(error)
            })}
            // this.$store.commit('setIsLoading', false)
        },
        async getAnsweredQuestion({ state , getters,rootState,rootGetters}, payload) {
            // this.$store.commit('setIsLoading', true)
            console.log("INGAQ")
            var url = `/api/board/question-answered?user=${rootGetters.getUID}`
            try{
                await axios.get(url)
                    .then(response => {
                    state.answeredQuestion = response.data
                    console.log('A',state.answeredQuestion)
                    })                    
                }
            catch{(error => {
                    console.log("error",error)
            })}
            // this.$store.commit('setIsLoading', false)
        },
        async getNotificationApi({ state , getters,rootState,rootGetters}, payload) {
            // this.$store.commit('setIsLoading', true)
            console.log("INGNAPI")
            var url = `/api/board/user-question-answer-notification?user=${rootGetters.getUID}`
            try{
                await axios.get(url)
                    .then(response => {
                    state.notificationApi = response.data
                    console.log('gotAPI',state.answeredQuestion)
                    })                    
                }
            catch{(error => {
                    console.log("error",error)
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