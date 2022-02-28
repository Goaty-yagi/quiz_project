<template>
    <div class="l-wrapper">
        <div class="l-container">
            <div class="reply-wrapper">
                <div class="title-black">
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
                <div class="title-black">
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
                <p @click="$emit('handleShowReplyPage')">キャンセル</p>
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
                this.$emit('handleNotifications','reply')
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
    .title-black{
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
    .title-black{
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
    }
    .form-text:focus{
        outline: none;
    }
}
.button-group{
    // width: 80%;
    display:flex;
    // margin:1rem;
    margin-top: 1rem;
    justify-content: flex-end;
    .btn-tr-black-base-sq{
        margin-left: 0.5rem;
        padding-right: 0.5rem;
        padding-left: 0.5rem;
    }
}
</style>