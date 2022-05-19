<template>
    <div class="my-quiz-wrapper">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <!-- <QuizP
            v-if="componentHandleDict.quiz"
            :forQuizPageInfo="forQuizPageInfo"
            @backQuizHome="backQuizHome"/> -->
            <div class="my-quiz-header">
                <p class="title-white">My-Quiz</p>
                <p class="register">登録数{{ length }} / {{myQuiz.max_num}}</p>
                <p class="max">(最大 {{myQuiz.max_num}} 個まで登録できます)</p>
            </div>
            <div class="my-quiz-container" v-if="$store.state.isLoading==false">
                <div class=my-quiz-loop v-for="(question,questionindex) in myQuestion"
                    v-bind:key="questionindex">
                    <div class="each-quiz-container">
                        <div class="question-index-container">
                            <div class="question-index">{{ questionindex+1 }}</div>
                        </div>
                        <div class="question-field">{{ convertFieldIdToInt(question.question.field[0]) }}</div>
                        <div class="question-grade">{{ convertQuizIdToInt(question.question.quiz) }}</div>
                        <div class="question-label">{{ question.question.label.substr(0,10)+'...' }}</div>
                        <div class="close-container">
                
                            <div @click="deleteMyQuestion(question.question.id)" class="close">
                                <i class="fas fa-times"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="btn-basegra-white-db-sq">
                練習
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import NotVerified from '@/components/login/NotVerified.vue'
import QuizP from '@/components/quiz_components/QuizP.vue'

export default {
    components: {
        QuizP,
        NotVerified,
    },
    data(){
        return{
            myQuestion:'',
        }
    },
    mounted(){
        this.myQuestion = this.$store.state.signup.myQuestion
        console.log("mounted",this.myQuestion)
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
        length(){
            // length = this.$store.state.signup.djangoUser.my_quiz[0].my_question
            return this.myQuestion.length
        },
        fieldNameId(){
            return this.$store.getters.fieldNameId
        },
        quizNameId(){
            return this.$store.getters.quizNameId
        }

    },
    methods:{
        convertFieldIdToInt(fieldId){
            for(let i of this.fieldNameId){
                if(i.id==fieldId){
                    return i.name
                }
            }
        },
        convertQuizIdToInt(quizId){
            for(let i of this.quizNameId){
                if(i.id==quizId){
                    return i.name
                }
            }

        },
        deleteMyQuestion(question){
            console.log(question)
            let payload = {
                "question":question,
                "myQuiz":this.myQuiz.id
            }
            console.log('in_delete',this.myQuestion)
            this.myQuestion = this.myQuestion.filter(item =>{
                return (item.question.id !=question)
            })
            console.log(payload,this.myQuestion)
            this.$store.commit("deleteMyQuestion",question)
            this.$store.dispatch("createAndDeleteMyQuiz",payload)
        }
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.my-quiz-wrapper{
    display: flex;
    justify-content: center;
    .main-wrapper{
        display: flex;
        flex-direction: column;
        align-items: center;
        .my-quiz-header{
            margin-bottom: 1rem;
            .register{
                font-size: 1.3rem;
                color: $lite-gray;
                font-weight: bold;
            }
            .max{
                font-size: 0.8rem;
                color: $lite-gray;
            }
        }
        .my-quiz-container{
            width: 95%;
            min-height: 300px;
            border: solid $base-color;
            border-radius: 5px;
            background: $back-white;
            padding-top: 1rem;
            padding-bottom: 1rem;
            .my-quiz-loop{
                .each-quiz-container{
                    display: flex;
                    width: 100%;
                    margin-bottom: 1rem;
                    margin-top: 1rem;
                    padding-bottom: 0.5rem;
                    border-bottom: solid $lite-gray;
                    align-items: center;
                    // justify-content: center;
                    .question-index-container{
                        flex-basis: 10%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        .question-index{
                            border: solid $base-color;
                            border-radius: 50vh;
                            width: 1.7rem;
                            height: 1.7rem;
                            margin-left: 0.4rem;
                            font-weight: bold;
                            background: $dark-blue;
                            color: white;
                        }
                    }
                    .question-field{
                        flex-basis: 20%;

                    }
                    .question-grade{
                        flex-basis: 20%;
                    }
                    .question-label{
                        flex-basis: 40%;
                        font-size: 0.8rem;
                    }
                    .close-container{
                        flex-basis: 5%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-left: 0.7rem;
                        height: 20px;
                        .close{
                            position:relative;
                            border: 0.1rem solid rgb(180, 179, 179);
                            border-radius: 50vh;
                            width: 1rem;
                            height: 1rem;
                            margin-top: auto;
                            margin-right: auto;
                            .fa-times{
                                font-size: 0.8rem;
                            }
                        }
                    }
                }
            }
           
        }
        .btn-basegra-white-db-sq{
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            font-weight: bold;
            font-size: 1.2rem;

        }

    }

}
</style>