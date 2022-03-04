import store from '..'

export default {
    namespace: true,
    state: {
        notifications:{
            reply: false,
            answer: false,
            post: false
        },
    },
    mutations:{
        resetNotifications(state){
            console.log("in_reset")
            state.notifications.answer = false
            state.notifications.reply = false
            state.notifications.post = false
        },        
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