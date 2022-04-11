<template>
    <div class="quiz-wrapper">
        <div class="main-wrapper">
            <!-- {{ typeof(questions) }}
            {{ questions }} -->
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <p class="quiz-description title-white">{{ quiz.description }}</p>
            <div class='quiz-countainer'>
                <div
                class="question-loop"
                v-for="(question,questionindex) in questions.slice(pagination.a,pagination.b)"
                v-bind:key="questionindex">
                    <div class='question-wrapper'>
                        <div class="question-header"><i class='q'>Q</i>第{{  }}問</div>
                        <div class='question-body'>{{ question.label }}</div>
                    </div>
                    
                    <!-- <div :class='showPic(question.image)'> -->
                    <div class="image-container" v-if="question.image">
                        <img class="image" v-bind:src="question.get_image"/>
                    </div>

                    <!-- answer part -->
                    <!-- questiontype 3 is '選択'
                    ４ is '並び替え'
                    5 is '多答' -->
                    <div class='answer-wrapper'>
                        <div 
                        class="answer-loop"
                        :class="{'selected-answer':selectedIndexNum==answerindex||
                        answerindex+1 in selectedOrderAnswer}"
                        @click="onClick(answerindex,answer,question)"
                        v-for="(answer,answerindex) in question.answer"
                        v-bind:key="answerindex">
                            <div class='answer-select-bases'>
                                <div class="answer-select">
                                    <div class="selecter">{{ String.fromCharCode(answerindex+65) }}
                                    </div>
                                </div>
                            </div>
                            <div class="answer-label-bases">
                                <div class="answer-label">
                                    {{ answer.label }}
                                </div>
                            </div>
                            <div class="selected-answer-bases">
                                <div v-if="selectedOrderAnswer[answerindex+1]" class="selected-answer-order">
                                    {{ selectedOrderAnswer[answerindex+1] }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="button-container">
                        <div class="btn-tr-white-base-sq">BACK</div>
                        <div @click="nextQuestion" class="btn-tr-white-base-sq">NEXT ></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'

export default {
    data(){
        return{
            pagination:{
                a: 0,
                b: 1,
            },
            // currentQuestionType:{
            //     select: false,
            //     manySelect: false,
            //     order: false
            // },
            selectedIndexNum: null,
            showSelectNum: true,
            selectedOrderAnswer:{},
            selectAnserCounter:0
        }
    },
    created(){
        console.log("created")
        // this.getquiz()
        this.getquestions()
    },
    mounted(){
        this.currentQuiz
    },
    computed: mapGetters(['questions','quiz']),
        
    methods:{
        ...mapActions(['getquestions']),
        nextQuestion(){
            this.pagination.a += 1
            this.pagination.b += 1
            this.selectedIndexNum= null
        },
        onClick(answerindex, answer, question){
            if(question.question_type == 3){
                if(this.selectedIndexNum==answerindex){
                    this.selectedIndexNum = null
                }else{
                    this.selectedIndexNum = answerindex
                }
            }else if(question.question_type == 4){
                if(this.selectedOrderAnswer[answerindex+1]&&
                this.questions.length>=this.selectAnserCounter){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    this.selectAnserCounter -=1
                }else{
                    this.selectAnserCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnserCounter
                }
            }
        },
        changeOrder(dict, index){
            let orderNum = dict[index]
            delete dict[index]
            if(dict){
                let changeDict = {}
                Object.keys(dict).forEach(key =>{
                    if(dict[key] > orderNum){
                        dict[key] -= 1
                    }
                })
            }
        return dict
        },
        // resetCurrentQuestionType(){
        //     this.currentQuestionType.select = false
        //     this.currentQuestionType.order = false
        //     this.currentQuestionType.manySelect = false
        // },
        // getCurrentQuestionType(currentQuestionType){
        //     this.resetCurrentQuestionType()
        //     if(currentQuestionType == 1){
        //         this.currentQuestionType.select = true
        //     }else if(currentQuestionType == 2){
        //         this.currentQuestionType.order = true
        //     }else if(currentQuestionType == 3){
        //         this.currentQuestionType.manySelect = true
        //     }
        // }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-wrapper{
    width: 100%;
    display: flex;
    justify-content: center;
    .quiz-countainer{
        width: 100%;
        display: flex;
        // align-items: center;
        justify-content: center;
        .question-loop{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            .question-wrapper{
            width: 95%;
            border: solid  rgba(243, 91, 36, 0.808);
            border-radius: 1rem;
            overflow:hidden;
                .question-header{
                background: linear-gradient($base-lite,$base-color);
                color:white;
                padding:0.5rem;
                font-weight:bold;
                position:relative;
                }
                .question-body{
                    background-color: rgb(253, 245, 239);
                    padding:1rem;
                    font-weight:bold;
                }
                .q{
                position:absolute;
                left:5%;
                bottom:2%;
                font-size:1.5rem;  
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
            .answer-wrapper{
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-top: 1rem;
                .answer-loop{
                    width: 95%;
                    height: 3rem;
                    border: solid black;
                    border-radius: 0.5rem;
                    background: white;
                    display: flex;
                    align-items: center;
                    margin-bottom: 0.5rem;
                    transition:0.3s;
                    .answer-select-bases{
                        flex-basis: 15%;
                        .answer-select{
                            border: solid black;
                            border-radius: 50vh;
                            width: 2.5rem;
                            height: 2.5rem;
                            margin-left: 0.5rem;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            transition:0.3s;
                            .selecter{
                                font-weight: bold;
                                font-size: 1.5rem;
                            }
                        }
                    }
                    .answer-label-bases{
                        flex-basis: 70%;
                        .answer-label{

                        }
                    }
                    .selected-answer-bases{
                        flex-basis: 15%;
                        .selected-answer-order{
                            font-size: 1.5rem;
                            font-weight: bold;
                            color: gray;
                        }
                    }
                }
                .selected-answer{
                    background: $base-lite-3;
                    .answer-select{
                        background: $base-color;
                        color: white;
                    }
                }
            }
            .button-container{
                display: flex;
                margin-top: 1rem;
                div{
                    padding-right: 0.3rem;
                    padding-left: 0.3rem;
                }
            }
        }
    }
}
</style>