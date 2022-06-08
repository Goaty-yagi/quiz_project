<template>
    <div v-if="questionTypeId" class="create-question-wrapper">
        <div class="main-wrapper">
            <div class="create-question-container" v-if="$store.state.isLoading==false">
                <form @submit.prevent='submitForm' class="field-wrapper">
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_grade
                                </div>
                            </div>
                            <select required class="text-box" v-model='formQuestionData.quiz'>
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
                                <input required type="number" min="1" max="10" step="1" v-model="formQuestionData.level">
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
                    <!-- <div class="additional-field-wrapper">
                        <div class="additional-field">
                            <div class="input-box">
                                <div class='each-title-container'>
                                    <div class="each-title">
                                        quiz_field
                                    </div>
                                </div>
                                <div class="text-box">
                                    <input required input type="number" value="1" min="1" max="10" step="1">
                                </div>
                            </div>
                            <div class="input-box" ref='formName'>
                                <div class='each-title-container'>
                                    <div class="each-title">
                                        quiz_field
                                    </div>
                                </div>
                                <select required class="text-box" >
                                    <option
                                        v-for="(id,idindex) in quizNameId" 
                                        v-bind:key="idindex">
                                        <p class="option">{{ id.name }}</p>
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div> -->
                    {{ formQuestionData}}
                    <div class="field">
                        <div class="input-box" ref='formName'>
                            <div class='each-title-container'>
                                <div class="each-title">
                                    quiz_field
                                </div>
                            </div>
                            <select required class="text-box" v-model="formQuestionData.field">
                                <option
                                    v-for="(id,idindex) in fieldNameId" 
                                    v-bind:key="idindex">
                                    <p class="option">{{ id.name }}</p>
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
                            <div class="num">
                                <p>{{ num }}</p>
                            </div>
                            <input class="answer-label" type="text" placeholder="答え" v-model='formAnswerDataList[num-1].label'>
                            <div class="checkbox-container">
                                <p>true?</p>
                                <input class="checkbox" type="checkbox" v-model='formAnswerDataList[num-1].is_correct'>
                            </div>
                            <div v-if="formQuestionData.questionType=='並び替え'" class="correct-order-container">
                                <div class="correct-order">
                                    <p>order?</p>
                                    <input required input type="number" min="1" max="10" step="1" v-model='formAnswerDataList[num-1].answer_id'>
                                </div>
                            </div>
                            <!-- unko{{ formAnswerDataList[num-1] }} -->
                        </div>
                    </div>
                    <!-- <div v-if='mailError||nameError||mailInUseError' class='error-form'>
                        <i class="fas fa-exclamation-triangle"></i>
                        <div v-if='mailError'>{{ mailError}}</div>
                        <div v-if='nameError'>{{ nameError }}</div>
                        <div v-if='mailInUseError'>{{ mailInUseError }}</div>
                    </div> -->
                    <div>
                        <button class='fbottun' ref='bform' id=''>作成する</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
export default {
    components: {
        
    },
    data(){
        return{
            showSideBar: true,
            formQuestionData:{
                quiz:'初級',
                quiz_level:1,
                question_type:'選択',
                field:'ひらがな',
                label:'',
                status:'',
                max_select:'',
                image:''
            },
            formAnswerDataList:[{
                label:'',
                is_correct:'',
                answer_id:'',
            },],
            formAnswerData:{
                label:'',
                is_correct:'',
                answer_id:'',
            },
            answerNum: 1,
            handleAnswerLength: 1,
        }
    },
    created(){
        this.$store.dispatch('getQuestionTypeId')
    },
    beforeMount(){
        // this.$store.dispatch('getQuestionTypeId')
    },
    mounted(){
        console.log('mounted at create-question',this.formAnswerDataList)
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
        }
    },
    computed: mapGetters(['quizNameId','fieldNameId','questionTypeId']),
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
            console.log('start add')
            this.setAllFormData()
            // await axios({
            //     method: 'post',
            //     url: '/api/questions-create/',
            //     data: {
            //         title: this.$store.state.board.title,
            //         description: this.$store.state.board.description,
            //         user: this.$store.state.signup.user.uid,
            //         slug: this.uuid,
            //         liked_num:{},
            //         tag: this.getTagId()
            //     },
                
            // })
        },
        setAllFormData(){
            // need to think about status part regarding of field
            if(this.formQuestionData.question_type == "多答") {
                let counter = 0
                for(let i of this.formAnswerDataList){
                    if(i.is_correct) {
                        counter += 1
                    }
                }
                if(counter >= 1){
                    console.log('error more than 2')
                } else if(this.formAnswerDataList.length == counter) {
                    console.log('error all ture')
                } else {
                    this.formQuestionData.max_select = counter
                }
            }
            this.formQuestionData.question_type = this.convertQuizTypeToId(this.formQuestionData.question_type)
            this.formQuestionData.quiz = this.convertQuizGradeToId(this.formQuestionData.quiz)
            this.formQuestionData.field = this.convertQuizFieldToId(this.formQuestionData.field)
            console.log("set", this.formQuestionData)
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
        }
    },
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";



.create-question-wrapper{
    width: 100%;
    margin: 0;margin-top: 2rem;
    display: flex;
    justify-content: center;
}
.field-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    .field{
        display: flex;
        justify-content: center;
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
        display: flex;
        align-items: center;
        flex-direction: column;
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
            width: 80%;
            border: solid $base-color;
            border-radius: 0.5rem;
            background: $back-white;
            margin-bottom: 0.4rem;
            .num{
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
            .answer-label{
                width: 50%;
                height: 2rem;
                padding: 0 0.5rem;
            }
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