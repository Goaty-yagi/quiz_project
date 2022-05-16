<template>
    <div class="l-wrapper">
        <div class="l-container">
            <div class="reply-wrapper">
                <div class="title-blue">
                    <p>コメント</p>
                </div>
                <div class="comment-wrapper">
                    <p>{{ reply }}</p>
                </div>
                <!-- <div class="question-discription">
                    <p>description: {{ questionDescription }}</p>
                </div> -->
            </div>

            <div class="answer-wrapper">
                <div class="title-blue">
                    <p>返信文</p>
                </div>
                <textarea class='form-text' v-model='description' placeholder="回答"/>
            </div>
            <div v-if="alert" :class="{'notification-red':alert}">
                <div class="notification-text">
                    文章を入力してください。
                </div>
            </div>
            <div class="button-group">
                <p class="cancel" @click="$emit('handleShowReplyPage')">キャンセル</p>
                <button class="btn-tr-black-base-sq"
                 @click="addAnswer" 
                 :disabled='alert'>回答する</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data(){
        return{
            description:'',
            alert: false,
        }
    },
    props:[
        'answerId',
        'reply',
        'handleNotifications'
    ],
    mounted(){
        console.log('answerMounted',this.reply)
        this.$store.commit('showModalTrue')
    },
    beforeUnmount(){
        this.$store.commit('showModalFalse')        
    },
    methods:{
        // addAnswer(){
        //     console.log('start add')
        //     axios({
        //         method: 'post',
        //         url: '/api/board/reply/create/',
        //         data: {
        //             description: this.description,
        //             user: this.$store.state.signup.user.uid,
        //             answer: this.answerId
        //         }
        //       })
        //       console.log('end add')
        //       this.$emit('handleNotifications','reply')
        //       this.$emit('getDetail')
        //       this.$emit('handleShowReplyPage')
        //     //   this.$emit('handleshowAnswerPage')
        //     //   this.$router.go({path: this.$router.currentRoute.path, force: true})
        //  },
        resetNotifications(){
            this.alert = false
        },
        descriptionCheck(){
            if(this.description==''){
                this.alert = true
                setTimeout(this.resetNotifications, 3000)
            }
        },
        async replyPost(){
            await axios({
                method: 'post',
                url: '/api/board/reply/create/',
                data: {
                    description: this.description,
                    user: this.$store.state.signup.user.uid,
                    answer: this.answerId
                }
            })
        },
        addAnswer(){
            console.log('start add')
            this.descriptionCheck()
            if(this.alert==false){
                this.replyPost()
                this.$store.dispatch("handleNotifications", 'reply')
                // this.$emit('handleNotifications','reply')
                this.$emit('getDetail')
                this.$emit('handleShowReplyPage')
                console.log('end-reply')
            }
            //   this.$emit('handleshowAnswerPage')
            //   this.$router.go({path: this.$router.currentRoute.path, force: true})
         },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    animation: l-container 3s;
    padding:1rem;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.reply-wrapper{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    .title-blue{
        margin: 1rem;
    }
    .comment-wrapper{
        background: rgb(235, 235, 235);
        padding: 0.5rem;
        width: 90%;
        // margin:0.5rem;
        text-align: left;
        white-space: pre-wrap;
    }
}
.answer-wrapper{
    width: 90%;
    .title-blue{
        margin: 1rem;
    }
    .form-text{
        width: 100%;
        background: $back-white;
        height: auto;
        min-height: 100px;
        border: 0.1rem solid $base-color;
        border-radius: 1vh;
        padding: 1rem;
        resize: none;
        transition: .5s;
    }
    .form-text:focus{
        outline: none;
        border: solid $dark-blue;
    }
}
.button-group{
    width: 80%;
    display:flex;
    margin:1rem;
    justify-content: flex-end;
    .cancel{
        background: rgb(234, 234, 234);
        padding: 0.5rem;
        transition: 0.5s;
    }
    .cancel:hover{
        background: rgb(196, 195, 195);
    }
    .btn-tr-black-base-sq{
        margin-left: 0.8rem;
        padding-right: 0.7rem;
        padding-left: 0.7rem;
        transition: 0.5s;
    }
    .btn-tr-black-base-sq:hover{
        background: $base-color;
        color: white;
        font-weight: bold;
    }
}
</style>