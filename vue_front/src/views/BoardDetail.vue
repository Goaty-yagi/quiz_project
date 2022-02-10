<template>
    <div class="community-wrapper" v-if="question">
        <h1>質問板</h1>
        <p> タイトル {{ question.title }} </p>
        <p> ユーザー名{{ question.user.name}} </p>
        <p> 作成日{{ question.created_on }} </p>
        <p> 質問{{ question.description}} </p>
        <div>
            <button @click='handleShowAnswerPage'>回答する</button>
        </div>
        <p v-if='question.answer[0]'> 回答</p>
        <div
            v-for="(answer,answerindex) in question.answer"
            v-bind:key="answerindex">
            <p> ユーザー名 {{ answer.user.name }} </p>
            <p>回答 {{ answer.description }} </p>
            <p> 作成日{{ answer.created_on }} </p>
             <button @click='handleShowReplyPage(answer.id)'>返信する</button>
            <!-- reply should be appir if post user or replyer -->
            <div v-if='answer.reply[0]'>
                <p>返信a</p>
                <div v-for="(reply,replyindex) in answer.reply"
                     v-bind:key="replyindex">
                     <p>返信{{ reply.description }}</p>
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
            answerId:''
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

<style scoped>
.question{
    color:white;    
}
p{
    color:white;
}
</style>