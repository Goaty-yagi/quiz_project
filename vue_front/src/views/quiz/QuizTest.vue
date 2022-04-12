<template>
    <div class="quiz-wrapper">
        <div class="main-wrapper">
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
                                <div v-if="selectedOrderAnswer[answerindex+1]&&question.question_type==4" class="selected-answer-order">
                                    {{ selectedOrderAnswer[answerindex+1] }}
                                </div>
                                <i v-if="selectedOrderAnswer[answerindex+1]&&question.question_type==5" class="fas fa-check"></i>
                            </div>
                        </div>
                    </div>
                    <div class="button-container">
                        <div v-if="questions.length==questionLengthCounter" class="btn-tr-white-base-sq">FINSH</div>
                        <div v-if="questions.length!=questionLengthCounter" @click="nextQuestion(question.question_type)" class="btn-tr-white-base-sq">NEXT ＞</div>
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
            questionLengthCounter:1,
            SelectedAnswerInfo:{},
            selectedAnswer: {},
            answerIDAndOrder:{},
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
            selectAnswerCounter:0,
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
        nextQuestion(questionType){
            this.pagination.a += 1
            this.pagination.b += 1
            this.selectedIndexNum= null
            this.selectAnswerHandler(
                questionType,
                )
            this.selectedOrderAnswer = {}
            this.selectedAnswer = {}
            this.selectAnswerCounter = 0
            this.questionLengthCounter += 1
            console.log(this.SelectedAnswerInfo)
        },
        Finish(){
            this.SelectedAnswerInfo = {}
        },
        onClick(answerindex, answer, question){
            if(question.question_type == 3){
                if(this.selectedIndexNum==answerindex){
                    this.selectedIndexNum = null
                    this.selectedAnswer = {}
                }else{
                    this.selectedIndexNum = answerindex
                    this.selectedAnswer['answerID'] = answer.id
                    this.selectedAnswer['isCorrect'] = answer.is_correct
                }
            }else if(question.question_type == 4){
                if(this.selectedOrderAnswer[answerindex+1]&&
                this.questions.length>=this.selectAnswerCounter){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                    this.selectAnswerCounter -= 1
                }else{
                    this.selectAnswerCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnswerCounter
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                }
            }else if(question.question_type == 5){
                if(this.selectedOrderAnswer[answerindex+1]&&
                this.questions.length>=this.selectAnswerCounter){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    this.getIDAndIsCorrect(answer.id, answer.is_correct)
                    this.selectAnswerCounter -= 1
                }else{
                    this.selectAnswerCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnswerCounter
                    this.getIDAndIsCorrect(answer.id, answer.is_correct)
                }
            }
        },
        changeOrder(dict, index){
            // if deleted, the num or nums before the deleted items order num
            // change
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
        selectAnswerHandler(questionType){
            if(questionType == 3){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                this.SelectedAnswerInfo[this.questionLengthCounter]['answerID'] = this.selectedAnswer.answerID
                this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = this.selectedAnswer.isCorrect
            }
            else if(questionType == 4){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                this.SelectedAnswerInfo[this.questionLengthCounter]['orderAnswer'] = this.answerIDAndOrder
                let stringKeys = Object.keys(this.answerIDAndOrder[this.questionLengthCounter]).map(function(a){
                    return Number(a)
                })
                if(JSON.stringify(stringKeys) == JSON.stringify(Object.values(this.answerIDAndOrder[this.questionLengthCounter]))){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = true
                }else{
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = false
                }
            }else if(questionType == 5){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                this.SelectedAnswerInfo[this.questionLengthCounter]['selectedAnswer'] = this.selectedAnswer
                Object.values(this.selectedAnswer).forEach(value =>{
                    if(value == false){
                        this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = false
                    }else{
                        this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = true
                    }
                })
            }
        },
        getAnswerIDAndOrder(answerID,orderNum){
            // this is for collecting answer from order questions
            if(this.questionLengthCounter in this.answerIDAndOrder){
                if(orderNum in this.answerIDAndOrder[this.questionLengthCounter]){
                    this.answerIDAndOrder[this.questionLengthCounter] =
                    this.changeOrder(this.answerIDAndOrder[this.questionLengthCounter],orderNum)
                    console.log('removed',this.answerIDAndOrder)
                }else{
                    this.answerIDAndOrder[this.questionLengthCounter][orderNum] = answerID
                    console.log('added',this.answerIDAndOrder)    
                }
            }else{
                this.answerIDAndOrder[this.questionLengthCounter] = {}
                this.answerIDAndOrder[this.questionLengthCounter][orderNum] = answerID
                console.log('added',this.answerIDAndOrder)
            }   
        },
        getIDAndIsCorrect(id, isCorrect){
            if(this.selectedAnswer[id]){
                delete this.selectedAnswer[id]
            }else{
                this.selectedAnswer[id] = isCorrect
            }
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
                        .fa-check{
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