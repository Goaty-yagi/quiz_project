<template>
    <div class="quiz-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <Start v-if="startQuiz&&questionLength&&$store.state.isLoading==false"
            :questionLength="questionLength"
            :forQuizPageInfo="forQuizPageInfo"
            @closeStart="closeStart"/>
            <div v-if="startQuiz==false">
                <!-- {{userStatusDict.status.status[0]}} -->
                <p class="quiz-description title-white">{{ quiz.description }}</p>
                <div class="progress-wrapper">
                    <div v-if="result==false" class="progress-bar-outer">
                        <div id="progress" style="width:0%" class="progress-bar-inner"></div>
                    </div>
                </div>

                <div v-if="showResult==false" class='quiz-countainer'>
                    <div
                    class="question-loop"
                    v-for="(question,questionindex) in questions.slice(pagination.a,pagination.b)"
                    v-bind:key="questionindex">
                        <div class='question-wrapper'>
                            <div class="question-header"><i class='q'>Q</i>第{{ questionLengthCounter }}問</div>
                            <div class='question-body'>{{ getQuestionStatus(question.label,question.status[0]) }}</div>
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
                            :class="{
                            'selected-answer':selectedIndexNum==answerindex||
                            answerindex+1 in selectedOrderAnswer,
                            'is-correct-answer':resultHandleDict.isCorrect&&answer.is_correct||
                            resultHandleDict.answerAllTrueType4||
                            resultHandleDict.answerIDType4[answer.answer_id],
                            'isnot-correct-answer':resultHandleDict.isNotCorrect&&resultHandleDict.answerIDType3==answer.id||
                            resultHandleDict.answerIDType5[answer.id]==false||
                            resultHandleDict.answerIDType4[answer.answer_id]==false,
                            'answer-hover':!result&&!maxSelectReach}"
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
                        <!-- <div  @click="deleteMyQuestion(question.id)" class="register-container"> -->
                        <div class="quiz-footer" :class="{'quiz-footer-result':result}">
                            <div class="register-container" :class="{'register-container-result':result}">
                                <div v-if="showError" class='error-form'>
                                    <i class="fas fa-exclamation-triangle"></i>
                                    <div>これ以上登録できません</div>
                                    <div>現在、最大で{{ getMyQuizInfo.max }}まで登録できます</div>
                                </div>
                                <button @click="deleteMyQuestion(question)" :disabled="showError" class="register-border-red" v-if="myQuestionIdList.includes(question.id)==false">この問題を<br>登録する</button>
                                <button @click="deleteMyQuestion(question)" class="register-border-blue" v-if="myQuestionIdList.includes(question.id)">この問題を<br>登録解除する</button>
                            </div>
                            <div v-if="showNextOrFinishButton&&
                            result==false" class="button-quiz-container">
                                <div v-if="questions.length==questionLengthCounter"
                                @click="Finish(question.question_type,question.id)" class="btn-tr-white-base-sq">FINSH</div>
                                <div v-if="questions.length!=questionLengthCounter"
                                @click="nextQuestion(question.question_type,question.id)" class="btn-tr-white-base-sq">NEXT ＞</div>
                            </div>

                            <!-- here for buttun in result -->
                            <div v-if="result" class="buttun-in-result">
                                <div class="back-container">
                                    <div v-if="questionLengthCounter!=1" 
                                    @click="resultBack()" class="btn-tr-white-base-sq back">
                                        ＜BACK
                                    </div>
                                </div>
                                <div 
                                @click="HandleShowResult()"
                                class="btn-base-black-db-ov result">結果画面</div>
                                <div class="next-container">
                                    <div v-if="questions.length!=questionLengthCounter"
                                    @click="resultNext()" class="btn-tr-white-base-sq next">
                                        NEXT＞
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <Result
                v-if="showResult"
                :SelectedAnswerInfo='SelectedAnswerInfo'
                :question_length='questions.length'
                @handlePagination='handlePagination'
                @HandleShowResult='HandleShowResult'
                @resultAnswerHandler='resultAnswerHandler'
                @handleResult='handleResult'
                @playAgain="playAgain"
                @backQuizHome="backQuizHome"
                />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {mapGetters,mapActions} from 'vuex'
import Result from '@/components/quiz_components/Result.vue'
import Start from '@/components/quiz_components/Start.vue'

export default {
    components: {
    Result,
    Start
    },
    props:[
        "forQuizPageInfo"
    ],
    data(){
        return{
            questionLengthCounter:1,
            questionLength:'',
            SelectedAnswerInfo:{},
            selectedAnswer: {},
            answerIDAndOrder:{},
            showResult: false,
            showNextOrFinishButton:false,
            result: false,
            startQuiz: false,
            progressBarSwitch: false,
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
            countupDict:{
                answerID:'',
                questionID:'',
                questionType:''
            },
            userStatusDict:{
                status:'',
                isCorrect:0,
                isFalse:0
            },
            maxSelectReach: false,
            selectedIndexNum: null,
            showSelectNum: true,
            selectedOrderAnswer:{},
            selectAnswerCounter:0,
            NumOfIscorrect:0,
            showError: false,
            myQuestionIdList:[]
        }
    },
    created(){
        // this.getquiz()
        this.getquestions()
    },
    mounted(){
        console.log("mounted QuizP",this.getMyQuestion)
        this.getMyQuestionIds(this.getMyQuestion)
        this.questionLength = this.questions.length
        this.startQuiz = true
        this.SelectedAnswerInfo = {}
        
    },
    watch:{
        questions:function(v) {
            if(this.questions){
                this.questionLength = this.questions.length
                // this.userStatusDict.status = this.questions[0]
            }
        },
        // startQuiz:function(v) {
        //     if(v == false){
        //         let percentage = this.questionLengthCounter/(this.questions.length) * 100 
        //         let a = document.getElementById('progress')
        //         a.setAttribute('style',`width:${percentage}%`)}
        // }
    },
    computed: mapGetters(['questions','quiz','getMyQuestion','getMyQuizInfo']),
        // myQuestion(){
        //     return this.$store.state.signup.myQuestion
        // },
    methods:{
        ...mapActions(['getquestions']),
        nextQuestion(questionType,questionID){
            this.handleCounyUpDict(this.selectedAnswer,questionType,questionID)
            this.pagination.a += 1
            this.pagination.b += 1
            this.selectedIndexNum= null
            this.showNextOrFinishButton = false
            this.selectAnswerHandler(
                questionType,
                )
            this.NumOfIscorrect = 0
            this.maxSelectReach = false
            this.selectedOrderAnswer = {}
            this.selectedAnswer = {}
            this.selectAnswerCounter = 0
            this.questionLengthCounter += 1
            this.answerIDAndOrder = {}
            // this. progressBar()
            this.scrollTop()
        },
        Finish(questionType,questionID){
            this.handleCounyUpDict(this.selectedAnswer,questionType,questionID)
            this.updateQuizTaker()
            this.showResult = true
            this.result = true
            this.selectedIndexNum= null
            this.selectAnswerHandler(
                questionType,
                )
            this.NumOfIscorrect = 0
            this.maxSelectReach = false
            this.selectedOrderAnswer = {}
            this.selectedAnswer = {}
            this.selectAnswerCounter = 0
            this.answerIDAndOrder = {}
            this.resultAnswerHandler()
            this.scrollTop()
        },
        onClick(answerindex, answer, question){
            // this is for 2 things,
            // first is for controling CSS return selectedIndexNum
            // which used for questionType 3, and selectedOrderAnswer
            // which used for questionType 4 and 5.
            // second is for selected-answer and is_correct.
            // return selectedAnswer for questionType 3.
            // for questionType 4, use getAnswerIDAndOrder function.
            // for questionType 5, use getIDAndIsCorrect function.
            this.progressBar()
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
                if(this.selectedOrderAnswer[answerindex+1]&&
                this.questions.length>=this.selectAnswerCounter){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                    this.selectAnswerCounter -= 1
                    this.showNextOrFinishButton = false
                    
                }else{
                    this.selectAnswerCounter += 1
                    this.selectedOrderAnswer[answerindex+1] = this.selectAnswerCounter
                    this.getAnswerIDAndOrder(answer.answer_id,this.selectAnswerCounter)
                    if(Object.keys(this.selectedOrderAnswer).length == question.answer.length){
                    this.handleShowNextOrFinishButton()
                    }
                }
            }else if(question.question_type == 5){
                this.getNumOfIscorrect(question.answer)
                if(this.selectedOrderAnswer[answerindex+1]){
                    this.selectedOrderAnswer = 
                    this.changeOrder(this.selectedOrderAnswer,answerindex+1)
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
                if(this.NumOfIscorrect == isCorrectCounter&&
                type5IsCorrect){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = true
                    this.handleUserStatus(true)
                }else if(type5IsCorrect==false&&
                isCorrectCounter > 0){
                    this.SelectedAnswerInfo[this.questionLengthCounter]['isCorrect'] = null
                    this.handleUserStatus(false)
                }
                this.SelectedAnswerInfo[this.questionLengthCounter]['selectedAnswer'] = this.selectedAnswer
            }
        },
        getAnswerIDAndOrder(answerID,orderNum){
            // this is for collecting answer from questionType 4
            if(this.questionLengthCounter in this.answerIDAndOrder){
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
        },
        getIDAndIsCorrect(id, isCorrect){
            // this is for questionType 5 
            if(id in this.selectedAnswer){
                delete this.selectedAnswer[id]
            }else{
                this.selectedAnswer[id] = isCorrect
            }
        },
        getNumOfIscorrect(answers){
            // this is for questionType 5
            if(this.NumOfIscorrect==false){
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
                                this.resultHandleDict.isCorrect = true
                                this.resultHandleDict.isNotCorrect = true
                                this.resultHandleDict.answerIDType5 = this.SelectedAnswerInfo[key].selectedAnswer
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
            if(this.result){
                if(this.SelectedAnswerInfo[this.questionLengthCounter].questionType==5){
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
        handleCounyUpDict(selectedAnswer,questionType,questionID){
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
            console.log("HCUD",this.countupDict)
            this.$store.dispatch('countUpAnswerAndQuestion',this.countupDict)
        },
        handlePagination(a,b){
            // this is for result component
            this.pagination.a = a
            this.pagination.b = b
            this.questionLengthCounter = b
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
            this.$store.dispatch('userStatusPost',this.userStatusDict)
            console.log('HUS',this.userStatusDict)
            
        },
        getQuestionStatus(lavel,status){
            this.userStatusDict.status = status
            return lavel
        },
        async updateQuizTaker(){
            await axios
            .patch(`api/quiz-taker-practice/?quiz_taker=${this.$store.state.signup.djangoUser.quiz_taker[0].id}`)
            .catch(e => {
                    let logger = {
                        message: "in components/quiz_components/QuizP/updateQuizTaker. couldn't update QuizTaker",
                        path: window.location.pathname,
                        actualErrorName: e.name,
                        actualErrorMessage: e.message,
                    }
                    this.$store.commit('setLogger',logger)
                    this.$store.commit('setIsLoading', false)
                    router.push({ name: 'ConnectionError' })
                })
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
        closeStart(){
            console.log("clicked")
            this.startQuiz = false
        },
        playAgain(){
            console.log('clicked play again')
            this.startQuiz = true
            this.attributeReset()
        },
        attributeReset(){
            this.result = false
            this.showResult = false
            this.pagination.a = 0
            this.pagination.b = 1
            this.selectedIndexNum= null
            this.showNextOrFinishButton = false
            this.SelectedAnswerInfo = {}
            this.NumOfIscorrect = 0
            this.maxSelectReach = false
            this.selectedOrderAnswer = {}
            this.selectedAnswer = {}
            this.selectAnswerCounter = 0
            this.questionLengthCounter = 1
            this.resultHandleDict.isCorrect = false,
            this.resultHandleDict.IsNotCorrect =false,
            this.resultHandleDict.answerIDType3 = '',
            this.resultHandleDict.questionType4 = false,
            this.resultHandleDict.answerAllTrueType4 =false,
            this.resultHandleDict.answerIDType4 ='',
            this.resultHandleDict.answerIDType5 = ''
            this.answerIDAndOrder = {}
            this.getquestions()
        },
        backQuizHome(){
            this.$emit('backQuizHome')
            this.attributeReset()
        },
        progressBar(){
            if(this.startQuiz == false){
                this.progressBarSwitch = true
                console.log(this.questionLengthCounter,(this.questions.length))
                let percentage = this.questionLengthCounter/(this.questions.length) * 100 
                let a = document.getElementById('progress')
                a.setAttribute('style',`width:${percentage}%`)
            }
        },
        deleteMyQuestion(question){
            console.log("INDELETE",question,this.myQuestionIdList)
            let payload = {
                "question":question.id,
                "myQuiz":this.getMyQuizInfo.id
            }
            if(!this.myQuestionIdList.includes(question.id)){
                if(this.myQuestionIdList.length >=this.getMyQuizInfo.max){
                    this.showError = true
                    setTimeout(this.showErrorFalse, 3000)  
                }
                else{
                    this.myQuestionIdList.push(question.id)
                    console.log("added",this.myQuestionIdList)
                    this.$store.commit("addMyQuestion",{'question':question})
                    this.$store.dispatch("createAndDeleteMyQuiz",payload)
                }
            }
            else{
                this.myQuestionIdList = this.myQuestionIdList.filter(item =>item != question.id )
                console.log("deleted",this.myQuestionIdList)
                this.$store.commit("deleteMyQuestion",question.id)
                this.$store.dispatch("createAndDeleteMyQuiz",payload)
            }
        },
        getMyQuestionIds(myQuestion){
            for(let i of myQuestion){
                this.myQuestionIdList.push(i.question.id)
            }
            console.log('GMQI',this.myQuestionIdList)
        },
        showErrorFalse(){
            this.showError = false
        }
        // setTimeout(context.commit, 3000,"resetNotifications")     
        // handleShowRegister(questionId){
        //     console.log(this.getMyQuestion)
        //     try{
        //         for(let i of this.getMyQuestion){
        //             console.log("HSR",i.question.id,questionId)

        //             if(i.question.id==questionId){
        //                 this.showRegister= false
        //                 return false
        //             }
        //         }
        //         this.showRegister= true
        //         return true
        //     }
        //     catch{
        //         // this.showRegister= true
        //         // return true
        //     }
        // }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.progress-wrapper{
    display: flex;
    justify-content: center;
    min-height: 80%;
    .progress-bar-outer{
        position: relative;
        border: solid black;
        border-radius: 50vh;
        width:80%;
        height: 2rem;
        background: rgb(238, 238, 238);
        margin-bottom: 1.5rem;
        margin-top: 0.5rem;
        overflow: hidden;
        .progress-bar-inner{
            position:absolute;
            top:0;
            left:0;
            box-sizing: inherit;
            height: 1.8rem;
            transform:skewX(-10deg);
            transition: 1s;
            background: linear-gradient(to bottom right,#F6F3E4 1%,#ffc890);       
        }
    }
}
.quiz-wrapper{
    width: 100%;
    min-height: 80vh;
    padding-bottom: 1rem;
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
                margin-top: 0.5rem;
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
                .answer-hover:hover{
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
            .quiz-footer{
                width: 100%;
                display: flex;
                justify-content: center;
                position: relative;
                margin-bottom: 1rem;
                height: 3rem;
                .register-container{
                    position: absolute;
                    display: flex;
                    width: 100%;
                    justify-content: flex-end;
                    margin-top: 0.5rem;
                    margin-right: 1rem;
                    .error-form{
                        animation: notification 3s;
                        animation-fill-mode: forwards;
                        position: absolute;
                        left: 0;
                        right: 0;
                        top: 0;
                        padding-bottom: 0.7rem;
                        margin: auto;
                        width: 80%;
                        background: rgba(252, 252, 252, 0.85);
                        z-index: 2;

                    }
                    .register-border-red{
                        border:0.3rem solid $dull-red;
                        border-radius: 5px;
                        padding: 0.2rem;
                        font-size: 0.8rem;
                        background: $back-white;
                        color: $dark-blue;
                        font-weight: bold;
                        transition: .5s;
                    }
                    .register-border-red:hover{
                        background: white;
                        border:0.3rem solid $lite-dull-red;
                    }
                    .register-border-blue{
                        border:0.3rem solid $dull-blue;
                        border-radius: 5px;
                        padding: 0.2rem;
                        font-size: 0.8rem;
                        background: $back-white;
                        color: $dark-blue;
                        font-weight: bold;
                        transition: .5s;
                    }
                    .register-border-blue:hover{
                        background: white;
                        border:0.3rem solid $lite-dull-blue;
                    }
                    
                }
                .button-quiz-container{
                    display: flex;
                    margin-top: 1rem;
                    z-index: 1;
                    div{
                        padding-right: 0.3rem;
                        padding-left: 0.3rem;
                    }
                }
                .buttun-in-result{
                    display: flex;
                    margin-top: 1rem;
                    width: 100%;
                    z-index: 1;
                    .back-container{
                        flex-basis: 45%;
                        display: flex;
                        justify-content: flex-end;
                        .back{
                            display: inline-block;
                            padding-left: 0.5rem;
                            padding-right: 0.5rem;
                            padding-top: 0.2rem;
                            padding-bottom: 0.2rem;
                        }
                    }
                    .result{
                        flex-basis: 20%;
                        width: auto;
                        padding-left: 0.5rem;
                        padding-right: 0.5rem;
                        padding-top: 0.2rem;
                        padding-bottom: 0.2rem;
                        margin-right: 0.5rem;
                        margin-left: 0.5rem;
                        font-weight: bold;                    
                    }
                    .next-container{
                         flex-basis: 45%;
                         display: flex;
                        .next{
                            display: inline-block;
                            padding-left: 0.5rem;
                            padding-right: 0.5rem;
                            padding-top: 0.2rem;
                            padding-bottom: 0.2rem;
                            // margin-bottom: 0.5rem;
                        }
                    }
                }
            }
        }
    }
}
@media(max-width: 480px){
    .progress-bar-outer{
        margin-bottom: 0.5rem!important;
        margin-top: 0!important;
    }
    .result{
        flex-basis: 33%!important;
    }
    .register-container-result{
    margin-top: 4rem!important;
    }
}
@media(max-height: 960px){
    .quiz-footer-result{
        margin-bottom: 5rem!important;
    }
}
</style>