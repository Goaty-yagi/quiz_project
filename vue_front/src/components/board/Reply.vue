<template>
    <div class="create-question-wrapper">
        <div class="innner-wrapper">
            <div class="question-wrapper">
                <div class="title">
                    <p>質問文</p>
                </div>
                <div class="question-title">
                    <p>title: {{ questionTitle }}</p>
                </div>
                <div class="question-discription">
                    <p>description: {{ questionDescription }}</p>
                </div>
            </div>

            <div class="answer-wraper">
                <div class="title">
                    <p>返信文</p>
                </div>
                <input type="text" v-model='description' placeholder="回答">
                {{ description }}
            </div>
            <div class="image">

            </div>
            <div class="button-group">
                <p>キャンセル</p>
                <button @click="addAnswer">回答する</button>
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
        }
    },
    props:[
        'answerId',
    ],
    mounted(){
        console.log('answerMounted',this.questionId)
    },
    methods:{
        addAnswer(){
            console.log('start add')
            axios({
                method: 'post',
                url: '/api/board/reply/create/',
                data: {
                    description: this.description,
                    user: this.$store.state.signup.user.uid,
                    answer: this.answerId
                }
              })
            //   this.$emit('handleshowAnswerPage')
              this.$router.go({path: this.$router.currentRoute.path, force: true})
         },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .create-question-wrapper{
        top:0;
        position: fixed;
        background:rgba(0,0,0,0.5);
        width:100vw;
        height:100vh;
        flex-direction: column;
        display: flex;
        justify-content: center;
        align-items: center;       
    }
    .innner-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;
        display:inline-block;        
    }
</style>