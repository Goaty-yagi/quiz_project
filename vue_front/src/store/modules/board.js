import store from '..'

export default {
    namespace: true,
    state: {
        notifications:{
            reply: false,
            answer: false,
            post: false,
            title:'',
            description:'',
            selectedTagList:''
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
        getSelectedTagList(state, payload){
            state.selectedTagList = payload
        }
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
        }           
    }


}