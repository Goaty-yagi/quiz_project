<template>
    <div class="quiz-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <div v-if="finishTest==false&&$store.state.isLoading==false">
                <p class="quiz-description title-white">テスト問題</p>
                <div v-if="finishTest" class="finishTest">"finishTest is TRUE"{{ finishTest }}</div>
                <div class='quiz-countainer'>
                    <div
                    class="question-loop"
                    v-for="(question,questionindex) in questions.slice(pagination.a,pagination.b)"
                    v-bind:key="questionindex">
                        <div class='question-wrapper'>
                            <div class="question-header"><i class='q'>Q</i>第{{ questionLengthForHTML }}問</div>
                            <div class='question-body'>{{ getQuestionStatus(question.label,question.status[0]) }}{{ question.quiz_level }}</div>
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
                            <button 
                            class="answer-loop"
                            :class="{'selected-answer':selectedIndexNum==answerindex||
                            answerindex+1 in selectedOrderAnswer,
                            'is-correct-answer':resultHandleDict.isCorrect&&answer.is_correct||
                            resultHandleDict.answerAllTrueType4||
                            resultHandleDict.answerIDType4[answer.answer_id],
                            'isnot-correct-answer':resultHandleDict.isNotCorrect&&resultHandleDict.answerIDType3==answer.id||
                            resultHandleDict.answerIDType5[answer.id]==false||
                            resultHandleDict.answerIDType4[answer.answer_id]==false}"
                            @click="e => result==false && onClick(answerindex,answer,question)"
                            :disabled="maxSelectReach&&answer.id in selectedAnswer==false"
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
                                    <div class="result-answer-order">
                                        <div class="order" v-if="resultHandleDict.questionType4">
                                            {{ answer.answer_id}}
                                        </div>
                                        <div v-if="type3And5CheckResult(resultHandleDict.answerIDType5,resultHandleDict.answerIDType3,answer.id)&&question.question_type!=4">
                                            <i class="fas fa-check"></i>
                                        </div>
                                    </div>
                                    <i v-if="selectedOrderAnswer[answerindex+1]&&question.question_type==5" class="fas fa-check"></i>
                                    <!-- for result -->
                                    <!-- <i v-if="answer.id in resultHandleDict.answerIDType5&&question.question_type==5" class="fas fa-check"></i> -->
                                    <i v-if="resultHandleDict.isCorrect&&answer.is_correct||
                                    resultHandleDict.answerAllTrueType4||
                                    resultHandleDict.answerIDType4[answer.answer_id]" class="far fa-circle"></i>
                                    <i v-if="resultHandleDict.isNotCorrect&&resultHandleDict.answerIDType3==answer.id||
                                    resultHandleDict.answerIDType5[answer.id]==false||
                                    resultHandleDict.answerIDType4[answer.answer_id]==false" class="fas fa-times"></i>
                                </div>
                            </button>
                        </div>
                        <div v-if="showNextOrFinishButton&&
                        result==false" class="button-quiz-container">
                            <!-- <div v-if="questions.length==questionLengthCounter"
                            @click="Finish(question.question_type)" class="btn-tr-white-base-sq">FINSH</div> -->
                            <div
                            @click="nextQuestion(question.question_type,question.id)" class="btn-tr-white-base-sq">
                                NEXT ＞
                            </div>
                        </div>

                        <!-- here for buttun in result -->
                        <div v-if="result" class="buttun-in-result">
                            <div v-if="questionLengthCounter!=1" 
                            @click="resultBack()" class="btn-tr-white-base-sq">＜BACK</div>
                            <div 
                            @click="HandleShowResult()"
                            class="btn-base-black-db-ov">結果画面</div>
                            <div v-if="questions.length!=questionLengthCounter"
                            @click="resultNext()" class="btn-tr-white-base-sq">NEXT＞</div>
                        </div>
                    </div>
                </div>
                <!-- <Result
                v-if="showResult"
                :SelectedAnswerInfo='SelectedAnswerInfo'
                :question_length='questions.length'
                @handlePagination='handlePagination'
                @HandleShowResult='HandleShowResult'
                @resultAnswerHandler='resultAnswerHandler'
                @handleResult='handleResult'
                /> -->
                <!-- <Result
                v-if="showResult"
                :question_length='questions.length'
                :rerultAnswer='rerultAnswer'
                @show='showDetail'/> -->

            </div>
            <TestResult
            v-if="finishTest"
            :finalResult="finalResult"
            :init="init"
            />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {mapGetters,mapActions} from 'vuex'
import Result from '@/components/quiz_components/Result.vue'
import TestResult from '@/components/initial/TestResult.vue'
import { createHydrationRenderer } from '@vue/runtime-core'

export default {
    components: {
    Result,
    TestResult
  },  
    data(){
        return{
            questionLengthForHTML:1,
            questionLengthCounter:1,
            SelectedAnswerInfo:{},
            selectedAnswer: {},
            answerIDAndOrder:{},
            showResult: false,
            showNextOrFinishButton:false,
            result: false,
            countupDict:{
                answerID:'',
                questionID:'',
                questionType:''
            },
            pagination:{
                a: 0,
                b: 1,
            },
            resultHandleDict:{
                isCorrect: false,
                IsNotCorrect: false,
                answerIDType3: '',
                questionType4: false,
                answerAllTrueType4: false,
                answerIDType4: '',
                answerIDType5: '',
            },
            
            maxSelectReach: false,
            // currentQuestionType:{
            //     select: false,
            //     manySelect: false,
            //     order: false
            // },
            selectedIndexNum: null,
            showSelectNum: true,
            selectedOrderAnswer:{},
            selectAnswerCounter:0,
            NumOfIscorrect:0,
            // here for status attribute
            userStatusDict:{
                status:'',
                isCorrect:0,
                isFalse:0
            },
            // from here for test attributes
            quizTestInfo:{
                level:'',
                quizId:4
            },
            LevelCounters:{
                handleLevelUp:0,
                handleLevelDown:0
            },
            finalResult:{
                grade:'',
                level:''
            },
            finishTest:false,
            currentLevel:1,
            currentGrade:"超初級",
            correctAnswer:{},
            tempStatusDict:{
                'status':[],
                'grade':'',
                'level':''
            },
            init: true,
        }
    },
    created(){
        console.log("created")
        // this.getquiz()
        this.getTestQuestions()
    },
    mounted(){
        this.$store.commit('onQuizTrue')
        this.SelectedAnswerInfo = {}
    },
    beforeUnmount(){
        this.$store.commit('onQuizFalse')
    },
    computed: mapGetters(['questions','quiz']),
    methods:{
        ...mapActions(['getTestQuestions']),
        nextQuestion(questionType,questionID){
            this.handleCountUpDict(this.selectedAnswer,questionType,questionID)
            this.pagination.a += 1
            this.pagination.b += 1
            this.selectedIndexNum= null
            this.showNextOrFinishButton = false
            this.selectAnswerHandler(
                questionType,
                )
            this.setTempStatusDict()
            this.questionLengthCounter += 1
            this.questionLengthForHTML += 1
            this.checkConsecutiveResult()
            this.NumOfIscorrect = 0
            this.maxSelectReach = false
            this.selectedOrderAnswer = {}
            this.selectedAnswer = {}
            this.answerIDAndOrder = {}
            this.selectAnswerCounter = 0
            console.log(this.SelectedAnswerInfo,'current',this.currentLevel)
            this.scrollTop()
        },
        // Finish(questionType){
        //     this.showResult = true
        //     this.result = true
        //     this.selectedIndexNum= null
        //     this.selectAnswerHandler(
        //         questionType,
        //         )
        //     this.NumOfIscorrect = 0
        //     this.maxSelectReach = false
        //     this.selectedOrderAnswer = {}
        //     this.selectedAnswer = {}
        //     this.selectAnswerCounter = 0
        //     console.log(this.SelectedAnswerInfo)
        //     this.resultAnswerHandler()
        //     this.scrollTop()
        // },
        onClick(answerindex, answer, question){
            // this is for 2 things,
            // first is for controling CSS return selectedIndexNum
            // which used for questionType 3, and selectedOrderAnswer
            // which used for questionType 4 and 5.
            // second is for selected-answer and is_correct.
            // return selectedAnswer for questionType 3.
            // for questionType 4, use getAnswerIDAndOrder function.
            // for questionType 5, use getIDAndIsCorrect function.
            if(question.question_type == 3){
                if(this.selectedIndexNum==answerindex){
                    this.selectedIndexNum = null
                    this.selectedAnswer = {}
                    this.showNextOrFinishButton = false
                }else{
                    this.selectedIndexNum = answerindex
                    this.selectedAnswer['answerID'] = answer.id
                    this.selectedAnswer['isCorrect'] = answer.is_correct
                    this.handleShowNextOrFinishButton()
                }
            }else if(question.question_type == 4){
                console.log("in No4 DELETE")
                if(this.selectedOrderAnswer[answerindex+1]){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                    this.selectAnswerCounter -= 1
                    this.showNextOrFinishButton = false
                    
                }else{
                    console.log("in No4 ADD")
                    this.selectAnswerCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnswerCounter
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                    console.log("Onclick-No4",Object.keys(this.selectedOrderAnswer).length, question.length)
                    if(Object.keys(this.selectedOrderAnswer).length == question.answer.length){
                    this.handleShowNextOrFinishButton()
                    }
                }
            }else if(question.question_type == 5){
                console.log("on click_type5 question",question)
                this.getNumOfIscorrect(question.answer)
                if(this.selectedOrderAnswer[answerindex+1]){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    // console.log('SOA',this.selectedOrderAnswer)
                    this.getIDAndIsCorrect(answer.id, answer.is_correct)
                    this.selectAnswerCounter -= 1
                    if(question.max_select){
                        if(Object.keys(this.selectedOrderAnswer).length < question.max_select){
                            this.showNextOrFinishButton = false
                            this.maxSelectReach = false
                        }
                    }else if(Object.keys(this.selectedOrderAnswer).length == 0){
                        this.showNextOrFinishButton = false
                    }
                }else{
                    this.selectAnswerCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnswerCounter
                    this.getIDAndIsCorrect(answer.id, answer.is_correct)
                    if(question.max_select){
                        if(Object.keys(this.selectedOrderAnswer).length == question.max_select){
                            this.handleShowNextOrFinishButton()
                            this.maxSelectReach = true
                        }
                    }else{
                        this.handleShowNextOrFinishButton()
                    }
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
            // this is get informations about selected-answer for result component
            // return SelectedAnswerInfo
            if(questionType == 3){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = this.selectedAnswer.isCorrect
                this.handleUserStatus(this.selectedAnswer.isCorrect)
                this.SelectedAnswerInfo[this.questionLengthCounter]['answerID'] = this.selectedAnswer.answerID
            }
            else if(questionType == 4){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                let stringKeys = Object.keys(this.answerIDAndOrder[this.questionLengthCounter]).map(function(a){
                    return Number(a)
                })
                if(JSON.stringify(stringKeys) == JSON.stringify(Object.values(this.answerIDAndOrder[this.questionLengthCounter]))){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = true
                    this.handleUserStatus(true)
                }else{
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = false
                    this.handleUserStatus(false)
                }
                this.makeOrderBoolean()
                this.SelectedAnswerInfo[this.questionLengthCounter]['orderAnswer'] = this.answerIDAndOrder
            }else if(questionType == 5){
                this.SelectedAnswerInfo[this.questionLengthCounter] = {}
                this.SelectedAnswerInfo[this.questionLengthCounter]['questionType'] = questionType
                let isCorrectCounter = 0
                var type5IsCorrect = true
                Object.values(this.selectedAnswer).forEach(value =>{
                    if(value == false){
                        this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = false
                        this.handleUserStatus(false)
                        type5IsCorrect = false
                    }else{
                        isCorrectCounter += 1
                    }
                })
                console.log('SAH',this.NumOfIscorrect, isCorrectCounter)
                if(this.NumOfIscorrect == isCorrectCounter&&
                type5IsCorrect){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = true
                    this.handleUserStatus(true)
                }else if(type5IsCorrect==false&&
                isCorrectCounter > 0){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = null
                    this.handleUserStatus(false)
                }
                // else if(this.maxSelectReach){
                //     this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = null
                // }
                this.SelectedAnswerInfo[this.questionLengthCounter]['selectedAnswer'] = this.selectedAnswer
            }
        },
        getAnswerIDAndOrder(answerID,orderNum){
            // this is for collecting answer from questionType 4
            console.log("GAID")
            if(this.questionLengthCounter in this.answerIDAndOrder){
                console.log("first-IF TRUE",this.questionLengthCounter, this.answerIDAndOrder)
                console.log("sono2daze",orderNum, this.answerIDAndOrder[this.questionLengthCounter])
                if(orderNum in this.answerIDAndOrder[this.questionLengthCounter]){
                    this.answerIDAndOrder[this.questionLengthCounter] =
                    this.changeOrder(this.answerIDAndOrder[this.questionLengthCounter],orderNum)
                }else{
                    this.answerIDAndOrder[this.questionLengthCounter][orderNum] = answerID   
                }
            }else{
                this.answerIDAndOrder[this.questionLengthCounter] = {}
                this.answerIDAndOrder[this.questionLengthCounter][orderNum] = answerID
            }   
        },
        makeOrderBoolean(){
            // this is for AnswerIDAndOrder{1:1} to be {1:true}
            let newDict = {}
            let IntegerKeys = Object.keys(this.answerIDAndOrder[this.questionLengthCounter]).map(function(a){
                    return Number(a)
                })
            for(let i = 0; i < IntegerKeys.length; i++){
                if(IntegerKeys[i] == Object.values(this.answerIDAndOrder[this.questionLengthCounter])[i]){
                    newDict[i+1] = true
                }else{
                    newDict[i+1] = false
                }
            }
            this.answerIDAndOrder = newDict
            // stringKeys.forEach(num =>{
            //     Object.values(this.answerIDAndOrder[this.questionLengthCounter]).forEach(value =>{
            //         if(num == )
            //     })
            // })
        },
        getIDAndIsCorrect(id, isCorrect){
            // this is for questionType 5 
            if(id in this.selectedAnswer){
                delete this.selectedAnswer[id]
                console.log(id,"deleted",this.selectedAnswer)
            }else{
                this.selectedAnswer[id] = isCorrect
                console.log(id,"added",this.selectedAnswer)
            }
        },
        getNumOfIscorrect(answers){
            // this is for questionType 5
            console.log('inGNOI',this.NumOfIscorrect,answers)
            if(this.NumOfIscorrect==false){
                console.log('Gp')
                 Object.values(answers).forEach(value =>{
                    if(value.is_correct){
                        this.NumOfIscorrect += 1
                    }
                })
            }
        },
        handleShowNextOrFinishButton(){
            this.showNextOrFinishButton = true
        },
        resultAnswerHandler(){
            if(this.result){
                this.resultHandleDict.isCorrect = false
                this.resultHandleDict.isNotCorrect = false
                this.resultHandleDict.answerAllTrueType4 = false
                this.resultHandleDict.questionType4 = false
                this.resultHandleDict.answerIDType3 = ''
                this.resultHandleDict.answerIDType4 = ''
                this.resultHandleDict.answerIDType5 = ''
                Object.keys(this.SelectedAnswerInfo).forEach(key =>{
                    if(key==this.questionLengthCounter){
                        console.log("currentType",this.SelectedAnswerInfo[key].questionType,this.SelectedAnswerInfo[key].isCorrect)
                        if(this.SelectedAnswerInfo[key].isCorrect){
                            if(this.SelectedAnswerInfo[key].questionType==4){
                                this.resultHandleDict.answerAllTrueType4 = true
                            }else if(this.SelectedAnswerInfo[key].questionType==5){
                                this.resultHandleDict.answerIDType5 = this.SelectedAnswerInfo[key].selectedAnswer
                            }
                            this.resultHandleDict.isCorrect = true
                        }else if(this.SelectedAnswerInfo[key].isCorrect==false&&
                            this.SelectedAnswerInfo[key].questionType==3){
                                this.resultHandleDict.isCorrect = true
                                this.resultHandleDict.isNotCorrect = true
                                this.resultHandleDict.answerIDType3 = this.SelectedAnswerInfo[key].answerID
                        }else if(this.SelectedAnswerInfo[key].questionType==5){
                            console.log("in type5")
                                this.resultHandleDict.isCorrect = true
                                this.resultHandleDict.isNotCorrect = true
                                this.resultHandleDict.answerIDType5 = this.SelectedAnswerInfo[key].selectedAnswer
                                console.log("type5",this.resultHandleDict.answerIDType5)
                        }else if(this.SelectedAnswerInfo[key].isCorrect==false&&
                            this.SelectedAnswerInfo[key].questionType==4){
                                this.resultHandleDict.questionType4 = true
                                this.resultHandleDict.isCorrect = true
                                this.resultHandleDict.isNotCorrect = true
                                this.resultHandleDict.answerIDType4 = this.SelectedAnswerInfo[key].orderAnswer
                        }
                    }
                })      
            }
        },
        type3And5CheckResult(selectedAnswer5,selectedAnswer3, answerID){
            // console.log(selectedAnswer, answerID)
            if(this.result){
                console.log("type",this.SelectedAnswerInfo[this.questionLengthCounter].questionType,"5",selectedAnswer5, "3",selectedAnswer3,answerID,this.questionLengthCounter)
                if(this.SelectedAnswerInfo[this.questionLengthCounter].questionType==5){
                    console.log("go")
                    if(answerID in selectedAnswer5){
                        return true
                    }else{
                        return false
                    }
                }
                else if(this.SelectedAnswerInfo[this.questionLengthCounter].questionType==3){
                    if(answerID == selectedAnswer3){
                        return true
                    }else{
                        return false
                    }
                }
            }
        },
        handlePagination(a,b){
            // this is for result component
            console.log("HP",a,b)
            this.pagination.a = a
            this.pagination.b = b
            this.questionLengthCounter = b
        },
        handleCountUpDict(selectedAnswer,questionType,questionID){
            this.countupDict.questionType = questionType
            this.countupDict.questionID = questionID
            if(questionType == 5){
                this.countupDict.answerID = Object.keys(selectedAnswer)
            }else if(questionType == 3){
                Object.keys(selectedAnswer).forEach(key => {
                    if(key = "answerID"){
                        this.countupDict.answerID = selectedAnswer[key]
                    }
                })
            }
            this.$store.dispatch('countUpAnswerAndQuestion',this.countupDict)
        },
        HandleShowResult(){
            this.showResult = !this.showResult          
        },
        handleResult(){
            this.result = ! this.result
        },
        handleUserStatus(selectedAnswer){
            // this is for only is_true and is_false
            console.log(selectedAnswer)
            this.userStatusDict.isCorrect = 0
            this.userStatusDict.isFalse = 0
            if(selectedAnswer){
                this.userStatusDict.isCorrect = 1
            }else{
                this.userStatusDict.isFalse = 1
            }
            // this.$store.dispatch('userStatusPost',this.userStatusDict)
            console.log('HUS',this.userStatusDict)
            
        },
        getQuestionStatus(lavel,status){
            this.userStatusDict.status = status
            return lavel
        },
        resultNext(){
            this.pagination.a += 1 
            this.pagination.b += 1
            this.questionLengthCounter += 1
            this.resultAnswerHandler()
            this.scrollTop()
        },
        resultBack(){
            this.pagination.a -= 1 
            this.pagination.b -= 1
            this.questionLengthCounter -= 1
            this.resultAnswerHandler()
            this.scrollTop()
        },
        scrollTop(){
            window.scrollTo({
            top: 0,
            behavior: "smooth"
            });
        },
        setTempStatusDict(){
            console.log('IN-setSD',this.tempStatusDict,this.userStatusDict)
            const _ = require('lodash');
            let copyObject = _.cloneDeep(this.userStatusDict)
            if(!this.tempStatusDict.status[0]){
                this.tempStatusDict.status.push(copyObject)
                console.log('pushed')
            }
            else{
                for(let i in this.tempStatusDict.status){
                    console.log('loop',i,typeof(i),this.tempStatusDict.status[i].status,copyObject.status)
                    if(this.tempStatusDict.status[i].status==copyObject.status){
                        console.log('true',this.tempStatusDict)
                        if(copyObject.isCorrect){
                            console.log('correct')
                            this.tempStatusDict.status[i].isCorrect+=1
                            console.log('correct',this.tempStatusDict)
                            break
                        }else{
                            console.log('notcorrect')
                            this.tempStatusDict.status[i].isFalse+=1
                            console.log('notcorrect',this.tempStatusDict)
                            break
                        }
                    }
                    else{
                        console.log('false',i,this.tempStatusDict.status.length -1)
                        if(Number(i) == this.tempStatusDict.status.length -1){
                            this.tempStatusDict.status.push(copyObject)
                            console.log('pushed2',this.tempStatusDict.status)
                        }
                    }
                }
            }
        },
        
        // from here for test function
        checkConsecutiveResult(){
            var correctCounter = 0
        
            console.log('SS',this.SelectedAnswerInfo)
            if(Object.keys(this.SelectedAnswerInfo).length >= 4){
                if(Object.keys(this.SelectedAnswerInfo).length == 10){
                    let isTrue = 0
                    let isFalse = 0
                    for (let i = 1; i <= 10; i++){
                        if(this.SelectedAnswerInfo[i].isCorrect){
                            isTrue += 1
                        }else{
                            isFalse += 1
                        }
                    }
                    console.log("isT",isTrue)
                    console.log("isF",isFalse)
                    if(isTrue >= 7){
                        this.LevelCounters.handleLevelUp += 1
                        this.currentLevel += 1
                        if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }
                        else{
                            this.quizTestInfo.level = this.currentLevel
                            this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                            this.getTestQuestions()
                            this.pagination.a = 0
                            this.pagination.b = 1
                            this.SelectedAnswerInfo = {}
                            correctCounter = 0
                            this.questionLengthCounter = 1
                        }
                    }
                    else if(isTrue > 4&& isTrue < 7){
                        this.finishTest = true
                        this.getFinalResult()
                        this.LevelCounters.handleLevelUp = 0
                        this.LevelCounters.handleLevelDown = 0
                    }
                    else{
                        this.LevelCounters.handleLevelDown += 1
                        if(this.currentGrade !="超初級"&&this.currentLevel!=1){
                            this.currentLevel -= 1
                            if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelUp = 0
                                this.LevelCounters.handleLevelDown = 0
                            }
                            else{
                                this.quizTestInfo.level = this.currentLevel
                                this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                                this.getTestQuestions()
                                correctCounter = 0
                                this.pagination.a = 0
                                this.pagination.b = 1
                                this.questionLengthCounter = 1
                                this.SelectedAnswerInfo = {}
                            }
                        }
                    }
                    if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown == 3){
                        this.finishTest = true
                        this.getFinalResult()
                        this.LevelCounters.handleLevelUp = 0
                        this.LevelCounters.handleLevelDown = 0
                    }
                }else{
                    console.log("longer than 4")
                    let num4 = 0
                    num4 = Object.keys(this.SelectedAnswerInfo).length - 4
                    for (let i = 1; i <= 4; i++){
                        console.log("forloop",this.SelectedAnswerInfo)
                        if(this.SelectedAnswerInfo[i + num4].isCorrect){
                            correctCounter += 1
                        }
                    }
                    if(correctCounter == 4){
                        console.log("correct4",this.LevelCounters.handleLevelUp,this.LevelCounters.handleLevelDown)
                        this.LevelCounters.handleLevelUp += 1
                        if(this.LevelCounters.handleLevelUp>=3&&this.LevelCounters.handleLevelDown==0){
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                        }else if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown==3){
                            console.log("quiz done", this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown)
                            this.finishTest = true
                            this.getFinalResult()
                            this.LevelCounters.handleLevelUp = 0
                            this.LevelCounters.handleLevelDown = 0
                        }else{
                            console.log('UP')
                            this.quizTestInfo.level = this.currentLevel + 1
                            this.currentLevel += 1
                            this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                            this.getTestQuestions()
                            this.pagination.a = 0
                            this.pagination.b = 1
                            this.SelectedAnswerInfo = {}
                            correctCounter = 0
                            this.questionLengthCounter = 1
                        }                
                    }else if(correctCounter == 0){
                        console.log("zeroCA")
                        if(this.currentLevel==1){
                            console.log("no more low level")
                        }
                        else{
                            this.LevelCounters.handleLevelDown += 1
                            console.log("in down-part",this.LevelCounters.handleLevelUp,this.LevelCounters.handleLevelDown)
                            if(this.LevelCounters.handleLevelDown>=3&&this.LevelCounters.handleLevelUp==0){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelDown = 0
                            }
                            else if(this.LevelCounters.handleLevelUp+this.LevelCounters.handleLevelDown==3){
                                this.finishTest = true
                                this.getFinalResult()
                                this.LevelCounters.handleLevelUp = 0
                                this.LevelCounters.handleLevelDown = 0
                            }else{
                                console.log('down')
                                this.quizTestInfo.level = this.currentLevel -1
                                this.currentLevel -= 1
                                this.$store.commit('getTestQuizInfo',this.quizTestInfo)
                                this.getTestQuestions()
                                correctCounter = 0
                                this.pagination.a = 0
                                this.pagination.b = 1
                                this.questionLengthCounter = 1
                                this.SelectedAnswerInfo = {}
                            }
                        }
                    }
                }
            }
        },
        // async updateQuizTaker(){
        //     console.log('UQT',
        //     this.$store.state.signup.djangoUser.quiz_taker)
        //     this.$store.commit("convertGradeFromIntToID",this.finalResult.grade)
        //     await axios.patch(`api/quiz-taker-test/?quiz_taker=${this.$store.state.signup.djangoUser.quiz_taker[0].id}&grade=${this.$store.state.quiz.gradeForConvert}&level=${this.finalResult.level}`)
        // },
        getFinalResult(){
            console.log("GFR",this.currentGrade)
            this.finalResult.grade = this.currentGrade
            this.finalResult.level = this.currentLevel
            this.tempStatusDict.level = this.currentLevel
            this.$store.dispatch('convertGradeFromIntToIDForNewUser',this.currentGrade)
            this.tempStatusDict.grade = this.$store.getters.gradeForConvert
            this.tempStatusDict.grade = this.$store.state.quiz.gradeForConvert
            if(!this.tempStatusDict.grade){
                // 4 is 超初級. it might be chainge
                this.tempStatusDict.grade = 4
            }
            this.$store.commit('setTempUser',this.tempStatusDict)
            this.$store.commit('tempUserTestTrue')
            // this.updateQuizTaker()
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-wrapper{
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 0.5rem;
    padding-bottom: 2rem;
    // align-items: center;
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
                margin-top: 0.5rem;
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
                .is-correct-answer{
                    background: rgb(148, 255, 235);
                }
                .answer-loop:hover{
                    border: solid $base-color;
                    // background: $base-lite-3;
                    .answer-select{
                        background: $base-lite-2;
                    }
                }
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
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        .selected-answer-order{
                            font-size: 1.5rem;
                            font-weight: bold;
                            color: gray;
                            flex-basis: 50%;
                        }
                        .result-answer-order{
                            flex-basis: 50%;
                            .order{
                                font-size: 1.5rem;
                                font-weight: bold;
                                color: gray;
                                margin-right: 0.5rem;
                            }
                        }
                        .fa-check{
                            color: gray;
                            flex-basis: 50%;
                        }
                        .fa-circle{
                            color: rgba(0, 84, 75, 0.839);
                            font-size: 1.5rem;
                            flex-basis: 50%;
                            margin-right: 0.1rem;
                        }
                        .fa-times{
                            color: rgba(244, 10, 10, 0.839);
                            font-size: 1.5rem;
                            margin-right: 0.1rem;
                            flex-basis: 50%;
                        }
                    }
                }
                .is-correct-answer{
                    background: rgb(177, 243, 231);
                }
                .isnot-correct-answer{
                    background: rgb(255, 147, 147)
                }
                .selected-answer{
                    background: $base-lite-3;
                    .answer-select{
                        background: $base-color;
                        color: white;
                    }
                }
            }
            .button-quiz-container{
                display: flex;
                margin-top: 1rem;
                align-items: center;
                div{
                    padding-top: 0.2rem;
                    padding-bottom: 0.2rem;
                    padding-right: 0.4rem;
                    padding-left: 0.4rem;
                }
            }
            .buttun-in-result{
                display: flex;
                margin-top: 1rem;
                .btn-base-black-db-ov{
                    padding-left: 0.5rem;
                    padding-right: 0.5rem;
                    padding-top: 0.2rem;
                    padding-bottom: 0.2rem;
                    margin-right: 0.5rem;
                    margin-left: 0.5rem;
                    font-weight: bold;                    
                }
                .btn-tr-white-base-sq{
                    padding-left: 0.5rem;
                    padding-right: 0.5rem;
                    padding-top: 0.2rem;
                    padding-bottom: 0.2rem;
                }
            }
        }
    }
}
</style>