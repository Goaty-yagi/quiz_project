<template>
    <div  class="board-detail-wrapper">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class="question-wrapper" v-if="question">
                <p class='title-white'>質問板</p>
                <div v-if="notifications.reply" :class="{'notification-blue':notifications.reply}">
                    <div class="notification-text">
                        返信しました。
                    </div>
                </div>
                <div v-if="notifications.answer" :class="{'notification-blue':notifications.answer}">
                    <div class="notification-text">
                        回答しました。
                    </div>
                </div>
                <div class='question-box'> 
                    <div class="question-box-header">
                        <div class="image">
                            <img class='img' v-bind:src="question.user.thumbnail"/>
                        </div>
                        <div class="username-date">
                            <p> {{ question.user.name}}さん </p>
                            <p> {{ question.created_on }} </p>
                        </div>
                        <div class="question-status-container">
                            <p class="question-status"> {{ questionStatus }} </p>
                        </div>
                    </div>
                    <div class="title-question">
                        <p class="question-title">  {{ question.title }} </p>        
                        <p class='question-description'> {{ question.description}} </p>
                    </div>
                    <div class="question-box-footer">
                        <i class="far fa-heart"></i>
                        <p class="good"> {{ question.good}} </p>
                        <p class="viewed"> viewed {{ question.viewed}} </p>
                    </div>
                    <button v-if="question.user.UID != $store.state.signup.user.uid" class="btn-base-white-db-sq" @click='handleShowAnswerPage'>回答する</button>
                    <!-- <button @click="handleNotifications('reply')" >unko</button> -->
                </div>
                <div class="relative-box">
                    <p>関連した質問</p>
                    <p>もっと見る></p>
                </div>
                <div class="answer-box" v-if='question.answer[0]'>
                    <div class="answer-box-title">
                        <p v-if='question.answer[0]'> 回答</p>
                        ({{ question.answer.length }}件)
                    </div>
                    <div
                     class="under-line"
                     v-for="(answer,answerindex) in question.answer"
                     v-bind:key="answerindex">
                        <div class="answer-box-header">
                            <img class='img' v-bind:src="answer.user.thumbnail"/>
                            <div class="username-date">
                                <p> {{ answer.user.name}}さん </p>
                                <p> {{ answer.created_on }} </p>
                            </div>
                        </div>
                        <p class="answer-description-container">{{ answer.description }} </p>
                        <div class="answer-box-footer">
                            <i class="far fa-heart"></i>
                            <p class="good"> {{ answer.good}} </p>
                        </div>
                        <button v-if="question.user.UID == $store.state.signup.user.uid && answer.reply.length == 0"
                         class='btn-base-white-db-sq' 
                         @click='handleReplyPage(answer.id, answer.description)'>
                         返信する
                         </button>
                        <!-- reply should be appir if post user or replyer -->
                        <div class='reply-wrapper' v-if='answer.reply[0]'>
                            <div>コメント</div>
                            <div class='reply-flex' 
                            v-for="(reply,replyindex) in answer.reply"
                            v-bind:key="replyindex">
                                <div class="reply-wrapper-header">
                                    <img class='img' v-bind:src="reply.user.thumbnail"/>
                                    <div class="username-date">
                                        <p> {{ reply.user.name}}さん </p>
                                        <p> {{ reply.created_on }} </p>
                                    </div>
                                </div>
                                <p class="replay-description">{{ reply.description }}</p>
                                <button v-if='$store.state.signup.user.uid==question.user.UID && answer.reply.slice(-1)[0].id==reply.id && answer.reply.slice(-1)[0].user.UID!=question.user.UID || $store.state.signup.user.uid==answer.user.UID && answer.reply.slice(-1)[0].id==reply.id && answer.reply.slice(-1)[0].user.UID==question.user.UID'
                                 class='btn-base-white-db-sq' 
                                 @click='handleReplyPage(answer.id, reply.description)'>
                                 返信する
                                 </button>
                            </div>
                        </div>
                        <div class='line-flex'>
                            <div class="line"></div>
                        </div>
                    </div>
                </div>
            </div>
        <Answer v-if='showAnswerPage'
         @handleShowAnswerPage='handleShowAnswerPage'
         @getDetail="getDetail"
         @handleNotifications="handleNotifications"
         :questionTitle='questionTitle'
         :questionDescription='questionDescription'
         :questionId='questionId'
         />
        <Reply v-if='showReplyPage'
         @handleShowReplyPage='handleShowReplyPage'
         @getDetail="getDetail"
         @handleNotifications="handleNotifications"
         :answerId='answerId'
         :reply="reply"
         />
        <!-- {{ questions }} -->
        <!-- <div class=question 
         v-for="(question,questionindex) in questions"
         v-bind:key="questionindex">
            <div class="tag">tag:{{ question.tag }}</div>
            <div class="title">title:{{ question.title }}</div>
            <div class="good">good:{{ question.good }}</div>
            <div class="date">data:{{ remove_T_Z(question.timestamp) }}</div>
        </div>
        <CreateQuestion v-if='showCreateQuestion'
        @handleShowConfirm='handleShowConfirm'/>
        <Confirm v-if='showConfirm'/> -->
         </div>
    </div>
</template>

<script>
import axios from 'axios'
import  Answer from '@/components/board/Answer.vue'
import  Reply from '@/components/board/Reply.vue'
export default {
    components: {
        Answer,
        Reply
  },
    data(){
        return{
            currentUserId:'',
            question:'',
            showAnswerPage: false,
            showReplyPage: false,
            questionTitle:'',
            questionDescription:'',
            questionId:'',
            answerId:'',
            questionStatus:'未解決',
            reply:'',
            notifications:{
                reply: false,
                answer: false,
            },
            questionAnswerUser:[
            ]
        }
    },
    beforeMount(){
        // this.currentUserId = this.$store.state.signup.user.uid
    },
    mounted() {
        // this.currentUserId = this.$store.state.signup.user.uid
        console.log(this.currentUserId)
        // console.log('mounted at detail', this.$store.state.signup.user.uid) 
        this.getDetail() 
    },
    methods: {
        async getDetail() {
            this.$store.commit('setIsLoading', true)
            console.log('inthegetdetail')
            await axios
                .get(`/api/board/question/${this.$route.params.slug}`)
                .then(response => {
                    this.question = response.data
                    this.questionTitle = this.question.title
                    this.questionDescription = this.question.description
                    this.questionId = this.question.id})
                .catch(error => {
                    console.log(error)
            })
            this.$store.commit('setIsLoading', false)
        },
        handleShowAnswerPage(){
            this.showAnswerPage = !this.showAnswerPage
            // this.handleScrollFixed()
        },
        getReply(reply){
            this.reply = reply
        },
        handleShowReplyPage(){
            this.showReplyPage = !this.showReplyPage
        },
        handleReplyPage(id, reply=''){
            this.getAnswerId(id)
            this.showReplyPage = !this.showReplyPage
            this.getReply(reply)
        },
        getAnswerId(id){
            this.answerId = id
        },
        getReplyUserAndQuestionUser(reply, question){
            this.questionAnswerUser.push(reply)
            this.questionAnswerUser.push(question)
        },
        resetNotifications(){
            this.notifications.answer = false
            this.notifications.reply = false
        },
        handleNotifications(elem){
            // this.notifications.reply = false
            // this.notifications.answer = false
            // console.log('inhanglenotu',elem)
            // console.log(this.notifications.answer)
            if(elem == "reply"){
                this.notifications.reply = true
                setTimeout(this.resetNotifications, 3000)
                
            }
            if(elem == "answer"){
                console.log("in answer")
                this.notifications.answer = true
                setTimeout(this.resetNotifications, 3000)
                console.log(this.notifications.answer)
            }            
        },
        // falseNotifications(elem){
        //     if(elem == "answer"){
        //         this.notifications.answer = false
        //     }
        //     if(elem == "reply"){
        //         this.notifications.reply = false
        //     }
        // },
        // handleScrollFixed(){
        //     this.scrollFixed = !this.scrollFixed
        // },
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.scroll{
    position:fixed;
}

.board-detail-wrapper{
    display: flex;
    justify-content: center;
    width: 100vw;
    align-items: center;
}
.question-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    .question-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        .question-box-header{
            display: flex;
            .image{
                .img{
                border-radius: 50%; 
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
                width:40%;
            }
            .question-status-container{
                display: flex;
                justify-content: flex-end;
                width: 50%;
                position: relative;
                .question-status{
                    position: absolute;
                    right:0;
                    top: 0.5rem;
                    color: rgb(255, 43, 209);
                    margin-right: 1rem;
                }
            }
        }
        .title-question{
            padding:1rem;
            .question-title{
                text-align: center;
                margin-bottom: 1rem;
                border-bottom: solid $dark-blue;
                display: inline-block;
                padding-bottom: 1rem;
            }
            .question-description{
                text-align: left;
                padding: 1rem; 
                background: rgb(236, 236, 236);
            }
        }
        .question-box-footer{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.1rem;
            }
            .viewed{
                margin-left: 1rem;
                margin-right: 0.5rem;
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
    }
    .relative-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .answer-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        .answer-box-title{
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        }
        .under-line{
            width: 90%;
            border-bottom: 0.2rem solid rgb(236, 236, 236);
            margin-top: 2rem;
            margin-bottom: 1rem;
            &:last-child{
                border-bottom: none;
            }
        }
        .answer-box-header{
            display: flex;
            .img{
                border-radius: 50%; 
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
            }
        }
        .answer-description-container{
            margin: 1rem;
            background: rgb(236, 236, 236);
            padding: 1rem;
            text-align: left;
        }
        .answer-box-footer{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 1rem;
                margin-right: 0.3rem;
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
        .reply-wrapper{
            // display: flex;
            // flex-direction: column;
            // justify-content: center;
            // align-items: center;
            .reply-flex{
                width: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-bottom: 1rem;
                .reply-wrapper-header{
                    width: 80%;
                    height: 100%;
                    display: flex;              
                    .img{
                        border-radius: 50%; 
                        width:  3rem;   
                        height: 3rem;
                        margin: 0.5rem; 
                    }
                    .username-date{
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start;
                        margin-top: 0.5rem;
                    }
                
                }
                .replay-description{
                    width: 63%;
                    // border-left: solid $dark-blue;
                    background: rgb(236, 236, 236);
                    text-align: left;
                    padding: 0.5rem;
                }
            }
        }
        .line-flex{
            display: flex;
            width: 100%;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            // .line-flex:last-of-type{
            //     border-bottom: none;
            // }
            &.line{
                width: 90%;
                border-bottom: 0.2rem solid rgb(236, 236, 236);
                margin-top: 2rem;
                margin-bottom: 1rem;
                &:last-child{
                    border-bottom: none;
                }
            }
        }
    }
}
</style>