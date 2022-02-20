<template>
    <div class="board-detail-wrapper" v-if="question">
        <div class="main-wrapper">
            <div class="question-wrapper">
                <p class='title-white'>質問板</p>
                <div class='question-box'>
                    <div class="question-box-header">
                        <img class='img' v-bind:src="question.user.thumbnail"/>
                        <div class="username-date">
                            <p> {{ question.user.name}}さん </p>
                            <p> {{ question.created_on }} </p>
                        </div>
                        <div class="question-status-container">
                            <p class="question-status"> {{ questionStatus }} </p>
                        </div>
                    </div>
                    <p>  {{ question.title }} </p>        
                    <p> {{ question.description}} </p>
                    <div class="question-box-footer">
                        <i class="far fa-heart"></i>
                        <p class="good"> {{ question.good}} </p>
                        <p class="viewed"> viewed {{ question.viewed}} </p>
                    </div>
                    <button class="btn-base-white-db-sq" @click='handleShowAnswerPage'>回答する</button>
                </div>
                <div class="relative-box">
                    <p>関連した質問</p>
                    <p>もっと見る></p>
                </div>
                <div class="answer-box">
                    <div class="answer-box-title">
                        <p v-if='question.answer[0]'> 回答</p>
                        ({{ question.answer.length }}件)
                    </div>
                    <div
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
                        <button v-if='answer.reply==false' class='btn-base-white-db-sq' @click='handleShowReplyPage(answer.id)'>返信する</button>
                        <!-- reply should be appir if post user or replyer -->
                        <div class='reply-wrapper' v-if='answer.reply[0]'>
                            <div class='reply-flex' 
                            v-for="(reply,replyindex) in answer.reply"
                            v-bind:key="replyindex">
                                <div class="reply-wrapper-header">
                                    <img class='img' v-bind:src="reply.user.thumbnail"/>
                                    <div class="username-date">
                                        <p> {{ question.user.name}}さん </p>
                                        <p> {{ question.created_on }} </p>
                                    </div>
                                </div>
                                <p class="replay-description">返信{{ reply.description }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <Answer v-if='showAnswerPage'
        @handleShowAnswerPage='handleShowAnswerPage'
        :questionTitle='questionTitle'
        :questionDescription='questionDescription'
        :questionId='questionId
        '/>
        <Reply v-if='showReplyPage'
        @handleShowReplyPage='handleShowReplyPage'
        :answerId='answerId'
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
            question:'',
            showAnswerPage: false,
            showReplyPage: false,
            questionTitle:'',
            questionDescription:'',
            questionId:'',
            answerId:'',
            questionStatus:'未解決'
        }
    },
    beforeMount(){
    },
    mounted() {
        console.log('mounted at detail') 
        this.getDetail() 
    },
    methods: {
        async getDetail() {
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
        },
        handleShowAnswerPage(){
            this.showAnswerPage = !this.showAnswerPage
        },
        handleShowReplyPage(id){
            this.getAnswerId(id)
            this.showReplyPage = !this.showReplyPage
        },
        getAnswerId(id){
            this.answerId = id
        }
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";

.board-detail-wrapper{
    display: flex;
    justify-content: center;
}
.question-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .question-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        .question-box-header{
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
            .question-status-container{
                width: 40%;
                position: relative;
                .question-status{
                    position: absolute;
                    right:0;
                    top: 0.5rem;
                    color: rgb(255, 43, 209);
                }
            }
        }
        .question-box-footer{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 0.5rem;
                margin-right: 0.3rem;
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
        .answer-box-title{
            display: flex;
            justify-content: center;
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
            display: flex;
            flex-direction: column;
            // justify-content: center;
            align-items: center;
            .reply-flex{
                width: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
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
                    border-left: solid $dark-blue;
                }
            }
        }
    }
}

</style>