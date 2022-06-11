<template>
    <div v-if="questionTypeId" class="create-question-wrapper" :class="{'scroll-fixed':fixedScroll, 'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="create-question-container" v-if="$store.state.isLoading==false">
                <form @submit.prevent='showConfirmTrue' class="field-wrapper">
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_grade
                                </div>
                            </div>
                            <select required class="text-box" v-model='tempQuiz'>
                                <option
                                    v-for="(id,idindex) in quizNameId" 
                                    v-bind:key="idindex">
                                    <p class="option">{{ id.name }}</p>
                                </option>
                            </select>
                        </div>       
                    </div>
                    <div class="field">
                        <div class="input-box" ref='formMail'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_level
                                </div>
                            </div>
                            <div class="text-box level">
                                <input required type="number" min="1" max="10" step="1" v-model="formQuestionData.quiz_level">
                            </div>
                        </div>         
                    </div>
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_type
                                </div>
                            </div>
                            <select required class="text-box" v-model="formQuestionData.question_type">
                                <option
                                    v-for="(id,idindex) in questionTypeId"
                                    v-bind:key="idindex">
                                    <p class="option">{{ id.name }}</p>
                                </option>
                            </select>
                        </div>       
                    </div>
                    <!-- {{ formQuestionData}} -->
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_field
                                </div>
                            </div>
                            <select required class="text-box" v-model="formQuestionData.field">
                                <option disabled>{{ tempField }}</option>
                                <option
                                    v-for="(id,idindex) in quizFieldList"
                                    v-bind:key="idindex">
                                    <p class="option">{{ id }}</p>
                                </option>
                            </select>
                        </div>       
                    </div>
                    <div class="texarea-field">
                        <div class="texarea-box">
                            <div class="each-title-container">
                                <div class="each-title">
                                    quiz_label
                                </div>
                            </div>
                            <textarea required class="text-box" v-on:focus="onFocus" v-model='formQuestionData.label'>
                            </textarea>
                        </div>       
                    </div>
                    <div class="answer-wrapper" >
                        <div class="answer-title-container">
                            <i @click="subtractAnswer()" class="fas fa-minus"></i>
                            <div class="answer-title">
                                <p>Answer</p>
                            </div>
                            <i @click="addAnswer()" class="fas fa-plus"></i>
                        </div>
                        <div class="answer-container"
                            v-for="(num) of handleAnswerLength" 
                                v-bind:key="num">
                            <div class="num-con">
                                <p class="num">{{ num }}</p>
                            </div>
                            <input required class="answer-label" type="text" placeholder="答え" v-model='formAnswerDataList[num-1].label'>
                            <div class="right-side-answer-container">
                                <div v-if="formQuestionData.question_type!='並び替え'" class="checkbox-container">
                                    <p>true</p>
                                    <input class="checkbox" type="checkbox" v-model='formAnswerDataList[num-1].is_correct'>
                                </div>
                                <div v-if="formQuestionData.question_type=='並び替え'" class="correct-order-container">
                                    <div class="correct-order">
                                        <p>order</p>
                                        <input required input type="number" min="1" :max="handleAnswerLength" step="1" v-model='formAnswerDataList[num-1].answer_id'>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="image-bottun" @click='handleShowThumbnail'>
                            <p v-if="!image">画像を入れますか？</p>
                            <p v-if="image">画像を変更しますか？</p>
                        </div>
                        <div v-if="image" class="image-container">
                            <img class="image" :src="image">
                        </div>
                        <!-- <div v-if="!errorOccurred" class="space-height"></div> -->
                        <div v-if="errorOccurred" :class="{'notification-red':errorOccurred}">
                            <div class="notification-text">
                            {{ errorMessage }}
                            </div>
                        </div>
                        <!-- <input type="file" enctype="multipart/form-data"> -->
                    </div>
                    <!-- <p class="po">{{formAnswerDataList }}</p> -->
                    <div>
                        <button class='fbottun' ref='bform' id=''>作成する</button>
                    </div>
                </form>
            </div>
        </div>
        <Thumbnail v-if="showThumbnail"
        @showThumbnailFalse="showThumbnailFalse"
        @setImageBlob="setImageBlob"/>
        <QuizConfirm
        v-if="showConfirm"
        :questionDetailInfo="questionDetailInfo"
        @submitForm="submitForm"
        @showConfirmFalse="showConfirmFalse"/>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex';
import axios from 'axios'
import Thumbnail from '@/components/account/Thumbnail.vue'
import QuizConfirm from '@/components/dashboard/QuizConfirm.vue'

function initialData() {
    return{
        showThumbnail: false,
        showSideBar: true,
        showConfirm: false,
        tempQuiz:'初級',
        tempField:'フィールドを選択してください。',
        // tempQuizType: '選択',
        questionDetailInfo:{},
        formQuestionData:{
            quiz:'初級',
            quiz_level:1,
            question_type:'選択',
            field:'フィールドを選択してください。',
            label:'',
            status:'',
            max_select:'',
            image:''
        },
        formAnswerDataList:[{
            label:'',
            is_correct:false,
            answer_id:0,
        },
        {
            label:'',
            is_correct:false,
            answer_id:0,
        },
        {
            label:'',
            is_correct:false,
            answer_id:0,
        },
        {
            label:'',
            is_correct:false,
            answer_id:0,
        },
        ],
        formAnswerData:{
            label:'',
            is_correct:false,
            answer_id:0,
        },
        formDataError:{
            noFieldError: "クイズフィールドを選んでください。",
            // highLevelError: "レベルは１０以内の数字を入力してください。",
            noSetAnswerIdError: "答えの順番を指定してください。",
            wrongNumOrderError:"答えの順番に間違いがあります。",
            notSelectOneError: "正解を一つ選んでください。",
            noMoreThanThreeError: "多答問題は答えを３つ以上指定してください。",
            moreThanTwoError:"多答問題は正解を２つ以上指定してください。",
            AllTrueError:"全ての答えが正解になっています。"
            },
        errorOccurred: false,
        errorMessage:'',
        answerNum: 4,
        handleAnswerLength: 4,
        formDataReady: false,
        image: '',
    }
}

export default {
    components: {
        Thumbnail,
        QuizConfirm
    },
    data(){
        return initialData()
        
    },
    created(){
        this.$store.dispatch('getQuestionTypeId')
    },
    beforeMount(){
        // this.$store.dispatch('getQuestionTypeId')
    },
    mounted(){
        console.log('mounted at create-question',this.quizNameId,this.fieldNameId)
    },
    watch:{
        answerNum:function(v) {
            console.log('v',v)
            if (this.handleAnswerLength > v){
                this.handleAnswerLength = v
                this.formAnswerDataList.pop()   
            } else {
                const _ = require('lodash');
                let copyObject = _.cloneDeep(this.formAnswerData)
                this.formAnswerDataList.push(copyObject)
                this.handleAnswerLength = v
            }
        },
        tempQuiz:function(v) {
            console.log('T',v)
            this.formQuestionData.quiz = v
            this.formQuestionData.field = this.tempField
        },
        // tempQuizType:function(v) {
        //     this.formQuestionData.question_type = v
        //     for(let i of this.formAnswerDataList) {
        //         i.is_correct = ''
        //     }
        // }
    },
    computed:{
        quizNameId() {
            return this.$store.getters.quizNameId
        },
        fieldNameId() {
            return this.$store.getters.fieldNameId
        },
        questionTypeId() {
            return this.$store.getters.questionTypeId
        },
        quizFieldList() {
            let list = [];
            for (let i of this.fieldNameId) {
                if (this.convertQuizGradeToId(this.tempQuiz) == i.grade) {
                    list.push(i.name)
                }
            }
            return list
        },
        fixedScroll(){
            return this.$store.getters.fixedScroll
        },
    },
    // mapGetters(['quizNameId','fieldNameId','questionTypeId']),
    methods:{
        // ...mapActions(['getQuestionTypeId']),
        handleShowSideBar(){
            console.log(this.showSideBar)
            this.showSideBar = !this.showSideBar 
            console.log(this.showSideBar)
        },
        addAnswer(){
            this.answerNum += 1
        },
        subtractAnswer(){
            if(this.answerNum > 1){
                this.answerNum -= 1
            }
        },
        async submitForm(){
            await this.setAllFormData()
            let response =''
            try{
                console.log('GO',this.formQuestionData.field)
                if(this.formDataReady){
                    response = await axios({
                        method: 'post',
                        url: '/api/questions-create/',                            
                        data: {
                            'quiz': this.formQuestionData.quiz,
                            'label': this.formQuestionData.label,
                            'field': [this.formQuestionData.field],
                            'question_type':this.formQuestionData.question_type,
                            'quiz_level': this.formQuestionData.quiz_level,
                            'answer': this.formAnswerDataList
                        },
                    })
                }
                if(this.formQuestionData.image){
                    console.log(response.data)
                    const formdata = new FormData
                    formdata.append('image',this.formQuestionData.image,`${this.formQuestionData.image}.png`)
                    axios
                    .patch(
                        `/api/questions-image-dispatch/${response.data.id}`,formdata)
                }
            } catch(e) {
                console.log('error',e)
            }
            this.allResetVars()
        },
        setAllFormData(){
            // need to think about status part regarding of field
            if (this.formQuestionData.field == this.tempField) {
                this.errorMessage = this.formDataError.noFieldError
                this.setTimeForNotification()
                return 
            }
            if(this.formQuestionData.question_type == "並び替え") {
                this.formAnswerDataList.forEach((elem, index) => {
                    this.formAnswerDataList[index].is_correct = false
                })
                let answerIdList = []
                this.formAnswerDataList.forEach((elem, index) => {
                    answerIdList.push(elem.answer_id)
                    if(!this.formAnswerDataList[index].answer_id) {
                        this.errorMessage = this.formDataError.noSetAnswerIdError
                        this.setTimeForNotification()
                        return 
                    } 
                })
                const answerIdListSet = [... new Set(answerIdList)];
                if(answerIdListSet.length == answerIdList.length){
                    this.formDataReady = true
                } else {
                    this.errorMessage = this.formDataError.wrongNumOrderError
                    this.setTimeForNotification()
                    return 
                }
            } else {
                let counter = 0
                for(let i of this.formAnswerDataList){
                    if(i.is_correct) {
                        counter += 1
                    }
                }
                if(this.formQuestionData.question_type == "選択") {
                    if(counter !=1) {
                        this.errorMessage = this.formDataError.notSelectOneError
                        this.setTimeForNotification()
                        return 
                    } else {
                        this.formAnswerDataList.forEach((elem,index) =>{
                            if(elem.answer_id) {
                                this.formAnswerDataList[index].answer_id = 0
                            }
                        })
                        this.formDataReady = true
                    }
                }
                else if(this.formQuestionData.question_type == "多答") {
                    if(this.formAnswerDataList.length < 3) {
                        this.errorMessage = this.formDataError.noMoreThanThreeError
                        this.setTimeForNotification()
                        return
                    } else if(counter == 1) {
                        this.errorMessage = this.formDataError.moreThanTwoError
                        this.setTimeForNotification()
                        return
                    } else if(this.formAnswerDataList.length == counter) {
                        this.errorMessage = this.formDataError.AllTrueError
                        this.setTimeForNotification()
                        return
                    } else {
                        this.formQuestionData.max_select = counter
                        this.formAnswerDataList.forEach((elem,index) =>{
                            if(elem.answer_id) {
                                this.formAnswerDataList[index].answer_id = 0
                            }
                        })
                        this.formDataReady = true
                    }
                }
            }
            this.formQuestionData.question_type = this.convertQuizTypeToId(this.formQuestionData.question_type)
            this.formQuestionData.quiz = this.convertQuizGradeToId(this.formQuestionData.quiz)
            this.formQuestionData.field = this.convertQuizFieldToId(this.formQuestionData.field)
            console.log("set", this.formQuestionData)
        },
        setTimeForNotification(){
            this.errorOccurred = true
            setTimeout(this.errorOccurredFalse, 3000);
        },
        errorOccurredFalse(){
            this.errorOccurred = false
        },
        convertQuizGradeToId(grade) {
            for (let i of this.quizNameId){
                if (i.name == grade){
                    return i.id
                }
            }
        },
        convertQuizTypeToId(type) {
            for (let i of this.questionTypeId){
                if (i.name == type){
                    return i.id
                }
            }
        },
        convertQuizFieldToId(field) {
            for (let i of this.fieldNameId){
                if (i.name == field){
                    return i.id
                }
            }
        },
        handleShowThumbnail(){
            this.showThumbnail = true
        },
        showThumbnailFalse(){
            this.showThumbnail = false
        },
        setImageBlob(blob,url) {
            console.log('set-blob',blob)
            this.image = url
            this.questionDetailInfo.image = url
            this.formQuestionData.image = blob
        },
        showConfirmTrue(){
            this.setQuestionDetailInfo()
            this.setAllFormData()
            if(this.formDataReady){
                this.$store.commit('fixedScrollTrue')
                this.showConfirm = true
            }
        },
        showConfirmFalse() {
            this.showConfirm = false
            this.$store.commit('fixedScrollFalse')
        },
        allResetVars() {
            Object.assign(this.$data, initialData())
        },
        setQuestionDetailInfo() {
            console.log('info')
            this.questionDetailInfo.grade = this.formQuestionData.quiz
            this.questionDetailInfo.level = this.formQuestionData.quiz_level
            this.questionDetailInfo.question_type = this.formQuestionData.question_type
            this.questionDetailInfo.field = this.formQuestionData.field
            this.questionDetailInfo.label = this.formQuestionData.label
            this.questionDetailInfo.answers = this.formAnswerDataList
            console.log('doneinfo')
        }
    },
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";


.po{
    color: white;
}
.create-question-wrapper{
    width: 100%;
    margin: 0;margin-top: 2rem;
    display: flex;
    justify-content: center;
    .create-question-container{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
.field-wrapper{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    .field{
        display: flex;
        justify-content: center;
        width: 100%;
        // border: solid red;
        .input-box{
            display: flex;
            font-size: 1.2rem;
            width: 80%;
            justify-content: center;
            border: solid $base-color;
            border-radius: 0.5rem;
            min-height: 40px;
            background: $back-white;
            // padding: 0.2rem 0.5rem;
            overflow:hidden;
            .each-title-container{
                flex-basis: 30%;
                min-width: 40%;
                display: flex;
                align-items: center;
                justify-content: center;
                border-right: solid $base-color;
                background: $dark-blue;                
                .each-title{
                    color: $base-white;
                    width: 100px;
                    font-weight: bold;
                    // font-size: 1rem;
                    margin: 0.2rem 0.5rem;
                }
            }
            .text-box{
                flex-basis: 70%;
                width: 30%;
                height: auto;
                background: transparent;
                border: none;
                margin-right: 1rem;
                margin-left: 1rem;
                font-size: 1rem;
                background: $back-white;
                .option{
                    font-weight: bold;
                }
            }
            .text-box:focus{
                outline: none;
            }
            .level{
                display: flex;
            }
        }
    }
    .texarea-field{
        width: 100%;
        display: flex;
        justify-content: center;
        .texarea-box{
            width: 80%;
            .each-title-container{
                display: flex;
                justify-content: center;
                .each-title{
                    width: 40%;
                    border-top: solid $base-color;
                    border-right: solid $base-color;
                    border-left: solid $base-color;
                    background: $dark-blue;
                    color: $base-white;
                    font-weight: bold;
                    border-radius: 0.5rem 0.5rem 0 0;
                }
            }
             .text-box{
                width: 100%;
                background: $back-white;
                height: auto;
                min-height: 100px;
                border: 0.1rem solid $base-color;
                border-radius: 1vh;
                padding: 1rem;
                resize: none;
                transition: 0.5s;
            }
            .text-box:focus{
                outline: none;
                border: solid $middle-blue;
            }
        }
    }
    .answer-wrapper{
        position: relative;
        display: flex;
        align-items: center;
        flex-direction: column;
        width: 100%;
        .answer-title-container{
            display: flex;
            align-items: center;
            .fa-minus{
                margin-right: 0.5rem;
                border: solid gray;
                border-radius: 50vh;
                padding: 0.1rem;
                background: $lite-gray;
                font-size: 0.8rem;
                transition: .5s;
            }
            .fa-minus:hover{
                border: solid $dark-blue;
                color: $base-color;
            }
            .answer-title{
                border: solid $base-color;
                border-radius: 0.5rem;
                padding-right: 0.5rem;
                padding-left: 0.5rem;
                background: $dark-blue;
                margin-bottom: 0.2rem;
                color: $base-white;
                font-weight: bold;
            }
            .fa-plus{
                margin-left: 0.5rem;
                border: solid gray;
                border-radius: 50vh;
                padding: 0.1rem;
                background: $lite-gray;
                font-size: 0.8rem;
                transition: .5s;
            }
            .fa-plus:hover{
                border: solid $dark-blue;
                color: $base-color;
            }
        }
        .answer-container{
            display: flex;
            align-items: center;
            // justify-content: center;
            min-width: 80%;
            border: solid $base-color;
            border-radius: 0.5rem;
            background: $back-white;
            margin-bottom: 0.4rem;
            .num-con{
                flex-basis: 10%;
                .num {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 2rem;
                    height: 2rem;
                    background: $dark-blue;
                    border-radius: 50vh;
                    border: solid $base-color;
                    color: $base-white;
                    font-weight: bold;
                    margin: 0.2rem 0.5rem;
                }
            }
            .answer-label{
                height: 2rem;
                flex-basis: 70%;
                padding: 0 0.5rem;
            }
            .right-side-answer-container{
                flex-basis: 16%;
                display: flex;
                justify-content: flex-end;
                width: 10%;
                padding-right: 0.1rem;
                // margin-right: 1rem;
                .checkbox-container{
                    margin-left: 1rem;
                    .checkbox{
                    }
                }
                .correct-order-container{
                    margin-left: 0.5rem;
                }
            }
        }
        .image-bottun{
            margin-top: 1rem;
            color: $lite-gray;
            border: solid gray;
            padding: 0.1rem 0.7rem;
            transition: .5s;
        }
        .image-bottun:hover {
            border: solid $base-color;
        }
        .image-container{
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 1rem;
            .image{
                width: 40%;
                // height: 40%;
            }
        }
    }
    .space-height{
        min-height: 3rem;
    }
    // .additional-field-wrapper{
    //     width: 100%;
    //     display: flex;
    //     justify-content: center;
    //     flex-direction: column;
    //     align-items: center;
    //     .additional-field{
    //         display: flex;
    //         flex-direction: column;
    //         align-items: flex-end;
    //         width: 80%;
    //         .input-box{
    //             display: flex;
    //             font-size: 1.2rem;
    //             width: 80%;
    //             justify-content: center;
    //             border: solid $base-color;
    //             border-radius: 0.5rem;
    //             min-height: 20px;
    //             background: $back-white;
    //             // padding: 0.2rem 0.5rem;
    //             overflow:hidden;
    //             .each-title-container{
    //                 flex-basis: 30%;
    //                 display: flex;
    //                 align-items: center;
    //                 justify-content: center;
    //                 border-right: solid $base-color;
    //                 background: $dark-blue;                
    //                 .each-title{
    //                     color: $base-white;
    //                     width: 100px;
    //                     font-weight: bold;
    //                     margin: 0.2rem 0.5rem;
    //                 }
    //             }
    //             .text-box{
    //                 flex-basis: 70%;
    //                 background: transparent;
    //                 border: none;
    //                 margin-right: 1rem;
    //                 margin-left: 1rem;
    //                 font-size: 1rem;
    //                 background: $back-white;
    //                 .option{
    //                     font-weight: bold;
    //                 }
    //             }
    //             .text-box:focus{
    //                 outline: none;
    //             }
    //             .level{
    //                 display: flex;
    //             }
    //         }
    //     }
    // }
}
</style>