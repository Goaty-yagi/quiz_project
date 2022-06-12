<template>
    <div class="l-wrapper">
        <div class="main-wrapper">
            <div class='main-quizdetail-wrapper'>
                <div class='l-container'>
                    <!-- <div class="close-container">
                        <div @click="close" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div> -->
                    <div class="main-detail-container">
                        <div class="question-field">
                            <p class="detail-text">Grade</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.grade }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Level</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.level }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Question-type</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.question_type }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Field</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.field }}</p>
                        </div>
                        <div class="question-label">
                            <p class="question-text">Question</p>
                            <div class="question-container">
                                <p class="question-description">{{ questionDetailInfo.label }}</p>                                
                            </div>
                        </div>
                        <div v-if="questionDetailInfo.image" class="image-container">
                            <img class="image" v-bind:src="questionDetailInfo.image"/>
                        </div>
                        <div class="question-label">
                            <p class="question-text">Answer</p>
                            <div class="question-container"
                                v-for="(answer,answerindex) in  questionDetailInfo.answers"
                                v-bind:key="answerindex">
                                <div class="answer-detail">
                                    <p class="index">{{ answerindex + 1 }}</p>
                                    <p class="iabel">{{ answer.label }}</p>
                                    <div class="answer-detail-right">
                                        <p v-if="!answer.answer_id" class="correct">{{ answer.is_correct }}</p>
                                        <p v-if="answer.answer_id" class="answer-id">{{ answer.answer_id }}</p>
                                    </div>    
                                </div>                         
                            </div>
                        </div>
                    </div>
                    <p class="main-title">この内容で作成しますか？</p>
                    <div @click="showConfirmFalse()" class="btn-gray-black-gray-sq">
                        戻る
                    </div>   
                    <div @click="submitForm()" class="btn-gray-black-gray-sq">
                        作成する
                    </div>                  
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:[
        'questionDetailInfo',
        'myQuestion',
        'showButtonAndNoQuizFalse'

    ],
    mounted(){
        this.$store.commit('showModalTrue')
        console.log('mounted at detail',this.questionDetailInfo)
    },
    beforeUnmount(){
        this.$store.commit('showModalFalse')
        this.$store.commit('fixedScrollFalse')
    },
    computed:{
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
    },
    methods:{
        addStep(){
            this.$router.push({ name: 'Account' })
            // this.$emit('sentHandle')
            // this.$emit('handle')
            // this.$store.commit('addStep')
        },
        close(){
            this.$emit('handleQuizDetail')
        },
        submitForm(){
            this.$emit('submitForm')
        },
        // questionDelete(id){
        //     console.log("clicked")
        //     this.$store.dispatch("handleNotifications", 'reply')
        //     this.deleteMyQuestion(id)
        //     this.close()
        // },
        deleteMyQuestion(question){
            console.log("INDE",question,this.myQuestion.length)
            let payload = {
                "question":question,
                "myQuiz":this.myQuiz.id
            }
            this.$emit('deleteQuestionFunForDetailPage',question)
            console.log(payload,this.myQuestion)
            this.$store.commit("deleteMyQuestion",question)
            this.$store.dispatch("createAndDeleteMyQuiz",payload)
        },
        showConfirmFalse(){
            this.$emit('showConfirmFalse')
            this.$emit('chancelAction')
        }
    },
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.main-quizdetail-wrapper{
    display: flex;
    justify-content: center;
    width: 100%;
    // overflow: scroll;
    .l-container{
        // height: auto;
        max-height: 70vh;
        overflow: scroll;
        .main-detail-container{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            .question-field{
                display: flex;
                justify-content: center;
                margin-bottom: 0.4rem;
                border-bottom: 0.2rem solid $lite-gray;
                padding: 0.5rem;
                width: 80%;
                .detail-text{
                    flex-basis: 50%;
                    display: flex;
                    justify-content: flex-end;
                    font-weight: bold;
                    margin-right: 0.5rem;
                }
                .detail-val{
                    flex-basis: 50%;
                    display: flex;
                    font-weight: bold;
                    margin-left: 0.5rem;
                }
                .center{
                    font-weight: bold;
                }
            }
            .question-label{
                display: flex;
                justify-content: center;
                flex-direction: column;
                align-items: center;
                width: 100%;
                .question-text{
                    font-weight: bold;
                    margin-bottom: 0.3rem;
                }
                .question-container{
                    background: $lite-gray;
                    padding:0.5rem;
                    margin-bottom: 0.5rem;
                    width: 80%;
                    .answer-detail{
                        position: relative;
                        display: flex;
                        justify-content: space-between;
                        .index{
                            // flex-basis: 10%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            border: solid $base-color;
                            border-radius: 50vh;
                            width: 1.5rem;
                            height: 1.5rem;
                            background: $dark-blue;
                            color: white;
                            margin-right: 1rem;
                        }
                        .iabel{
                            position: absolute;
                            right: 0;
                            left: 0;
                            margin: 0 auto;
                            // margin-right: 0.5rem;
                            // margin-left: 0.5rem;
                        }
                        .answer-detail-right{
                            display: flex;
                            justify-content: flex-end;
                            width: 50%;
                            .correct{

                            }
                        }
                    }
                }
            }
        }
        .main-title{
            font-weight: bold;
            margin-bottom: 0.2rem;
            color: $dull-red;
        }
        .btn-gray-black-gray-sq{
            display: inline-block;
            border: solid $base-color;
            padding-right: 0.3rem;
            padding-left: 0.3rem;
            margin-bottom: 1rem;
            margin-right: 0.5rem;
            margin-left: 0.5rem;
        }

    }
}
.image-container{
    display: flex;
    justify-content: center;
    width: 100%;
    .image{
        width: 40%;
    }
}
</style>