<template>
     <div class="l-wrapper">
        <div class='l-container'>
            <div class="title-blue">
                 <p>質問文</p>
            </div>
            
            <form class="form" @submit.prevent='addAnswer'>
                <div class="question-title">
                    <p>{{ questionTitle }}</p>
                </div>
                <div class="question-discription">
                    <p>{{ questionDescription }}</p>
                </div>

                <div class="line"></div>

                <div class="answer-wraper">
                    <p class="title-blue">回答文</p>
                    <textarea class='form-text' type="text" v-model='description' placeholder="回答"></textarea>
                </div>
                <!-- <div class="image">
                    <i class="fas fa-camera"></i>
                    <p>写真を添付</p>
                </div> -->
                <div class="button-group">
                    <p class="cancel" @click="$emit('handleShowAnswerPage')">キャンセル</p>
                    <button class="btn-tr-black-base-sq" 
                    :disabled="alert">回答する</button>
                </div>
            </form>
            <div v-if="alert" :class="{'notification-red':alert}">
                <div class="notification-text">
                    文章を入力してください。
                </div>
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
            alert: false
        }
    },
    props:[
        'questionDescription',
        'questionTitle',
        'questionId',
        'handleNotifications'
    ],
    mounted(){
        console.log('answerMounted',this.questionId)
        this.$store.commit('showModalTrue')
    },
    beforeUnmount(){
        this.$store.commit('showModalFalse')
    },
    methods:{
        resetNotifications(){
            this.alert = false
        },
        descriptionCheck(){
             if(this.description==''){
                 this.alert = true
                 setTimeout(this.resetNotifications, 3000)
             }
         },
        async answerPost(){
            console.log("this.questionId",this.questionId)
            await axios({
                method: 'post',
                url: '/api/board/answer/create',
                data: {
                    description: this.description,
                    user: this.$store.state.signup.user.uid,
                    question: this.questionId,
                    liked_answer:[]
                }
            })
        },
        async addAnswer(){
            this.descriptionCheck()
            console.log('start add')
            if(this.alert==false){
               await this.answerPost()
                this.$emit('getDetail')
                this.$store.dispatch("handleNotifications", 'answer')
                this.$emit('handleShowAnswerPage')
                console.log("end_answer",this.$store.state.board.notifications)
            }
            //   this.$router.go({path: this.$router.currentRoute.path, force: true})
         },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    animation: l-container 3s;
    display: flex;
    flex-direction: column;
    // justify-content: center;
    align-items: center;
    position:relative;
    .title-blue{
        margin: 2rem;
    }
    .form{
        width: 100%;
        display: flex;
        flex-direction: column;
        // justify-content: center;
        align-items: center;
        .question-discription{
            width:90%;
            height: 100px;
            background: rgb(228, 228, 228);
            margin-top: 1rem;
            padding: 0.5rem;
            text-align: left;
            white-space: pre-wrap;
            overflow-y: scroll;

        }
        .line{
            width: 80%;
            border-bottom: 0.2rem solid $dark-blue;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        .answer-wraper{
            width: 100%;
            .title-blue{
                margin: 0;
            }
            .form-text{
                background: $back-white;
                padding: 1rem;
                width: 80%;
                height:10rem;
                border: 0.1rem solid $base-color;
                border-radius: 1vh;
                resize: none;
                transition: .5s;
            }
            .form-text:focus{
                outline: none;
                border: solid $middle-blue;
            }
        }
        .image{
            width:80%;
            display:flex;
            // align-items: left;  
            margin:1rem;
            // justify-content: flex-start;
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
    }
}
</style>