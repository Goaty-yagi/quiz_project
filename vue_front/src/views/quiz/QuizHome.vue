<template>
    <div class="quiz-home-wrapper">
        <div class="main-wrapper">
            <QuizP
            v-if="componentHandleDict.quiz"
            @backQuizHome="backQuizHome"/>
            <div v-if="componentHandleDict.quiz==false" class="title-white">クイズ</div>
            <!-- <Start
            v-if="componentHandleDict.start"
            @goQuiz="goQuiz"/> -->
            <div v-if="this.componentHandleDict.quizStart==false" class="quiz-home-container">
                <div class="select-container">
                    <div 
                    class="select-loop"
                    v-for="(select,key,selectindex) in quizSelectDict"
                    v-bind:key="selectindex">
                        <div @click="showGrade(select.grade,key)" class="loop-wrapper">
                            <div class="english-title">{{key}}</div>
                            <div v-if="selectindex==0" class="font"><i class="fas fa-dice-one"></i></div>
                            <div v-if="selectindex==1" class="font"><i class="fas fa-dice-two"></i></div>
                            <div v-if="selectindex==2" class="font"><i class="fas fa-dice-three"></i></div>
                            <div v-if="selectindex==3" class="font"><i class="fas fa-dice-four"></i></div>
                            <div class="grade">{{ select.grade }}</div>
                            <div class="description">{{ select.description }}</div>
                        </div>
                    </div>
                </div>
                <div v-if="showEachGrade" class="l-wrapper">
                    <div class="l-container">
                        <div class="close-grade">
                            <div @click="closeGrade()" class="close">
                                <i class="fas fa-times"></i>
                            </div>
                        </div>
                        <div>
                            <img class='is-image' src="@/assets/logo.png">
                        </div>
                        <div class="title-blue">{{ gradeTitle }}</div>
                        <div 
                        class="category-outer-loop"
                        v-for="(selects,key,selectsindex) in quizCategories"
                        v-bind:key="selectsindex">
                            <div v-if="key==receivedKey">
                                <div class="category-inner-loop" v-for="(titles,titlesindex) in selects"
                                v-bind:key="titlesindex">
                                    <div 
                                    class="category-container"
                                    v-for="(options,title,titleindex) in titles"
                                    v-bind:key="titleindex"
                                    >
                                        <div @click="showOptions(titleindex)" class="category-title-container" :class="{
                                            'space':optionDict.showOption&&
                                            optionDict.currentCategory==titleindex,
                                            }">
                                            <div class="category-title">
                                                {{ title }}
                                                <i v-if="options" :class="{
                                                    'lotate':optionDict.showOption&&
                                                    optionDict.currentCategory==titleindex}" 
                                                    class="fas fa-caret-down">
                                                </i>
                                            </div>
                                        </div>
                                        <div class="option-container" v-if="optionDict.showOption&&
                                        optionDict.currentCategory==titleindex">
                                            <div 
                                            class="option-loop"
                                            v-for="(option, optionindex) in options"
                                            v-bind:key="optionindex">
                                                <div @click="goStart()" class="each-option">
                                                    <div class="option-font">
                                                        
                                                        <i v-if="option=='くだもの'" class="fas fa-apple-alt"></i>
                                                        <i v-if="option=='やさい'" class="fas fa-carrot"></i>
                                                        <i v-if="option=='どうぶつ'" class="fas fa-cat"></i>
                                                        <i v-if="option=='のりもの'" class="fas fa-car-side"></i>
                                                        <i v-if="option=='たべもの'" class="fas fa-utensils"></i>
                                                        <i v-if="option=='のみもの'" class="fas fa-mug-hot"></i>
                                                    </div>
                                                    <div class="option-title">
                                                         <p>{{ option }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import QuizP from '@/components/quiz_components/QuizP.vue'

export default {
    components: {
        QuizP,
    },  
    data(){
        return{
            quizSelectDict:{
                beginner:{
                    grade:"超初級",
                    description:"ひらがなやカタカナなど簡単なボキャブラリー"
                },
                basic:{
                    grade:"初級",
                    description:"簡単な文法や一般的な語彙などN５相当"
                },
                intermediate:{
                    grade:"中級",
                    description:"少し難しい文法や表現などN４相当"
                },
                Advanced:{
                    grade:"上級",
                    description:"難しいです"
                }
            },
            quizCategories:{
                beginner:{
                    title:{
                        ひらがな:["50音"], 
                        カタカナ:"", 
                        ボキャブラリー:[
                            "くだもの",
                            "やさい",
                            "どうぶつ",
                            "のりもの",
                            "たべもの",
                            "のみもの"
                        ], 
                        すうじ:""
                    },
                },
                basic:{
                    title:[]
                }
            },
            optionDict:{
                currentCategory:'',
                showOption: false,                
            },
            // quizStart manage after start
            componentHandleDict:{
                quiz: false,
                quizStart: false,
            },
            showEachGrade: false,
            // showEachOptions: false,
            receivedKey: '',
            gradeTitle: '',
        }
    },
    mounted(){
        this.optionDict.currentCategory = ''
    },
    methods:{
        showGrade(grade, key){
            this.showEachGrade = true
            this.gradeTitle = grade
            this.receivedKey = key
        },
        closeGrade(){
            this.showEachGrade = false
        },
        showOptions(index){
            if(this.optionDict.currentCategory==index){
                this.optionDict.showOption = !this.optionDict.showOption
                this.optionDict.currentCategory = ''
            }else{
                this.optionDict.currentCategory = index
                this.optionDict.showOption = true
            }
        },
        getQuizInfo(quizid,quizfield){
            this.$store.commit('getQuizInfo',{})
        },
        allReset(){
            this.optionDict.showOption = false
            this.showEachGrade = false
        },
        goStart(){
            // this.getQuizInfo()
            this.componentHandleDict.quiz = true
            this.componentHandleDict.quizStart = true
            this.allReset()
        },
        backQuizHome(){
            this.componentHandleDict.quizStart = false
            this.componentHandleDict.quiz = false
            this.allReset()
        }
        // goQuiz(){
        //     this.componentHandleDict.start = false
        //     this.componentHandleDict.quiz = true            
        // }
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-home-wrapper{
    display: flex;
    justify-content: center;
    min-height: 80vh;
    width: 100vw;
    .quiz-home-container{
        display: flex;
        flex-direction: column;
        .select-container{
            width:100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            .select-loop{
                width: 90%;
                display: flex;
                justify-content: center;
                position: relative;
                padding: 0.7rem;
                .loop-wrapper{
                    display: flex;
                    align-items: center;
                    width: 100%;
                    border: solid $base-color;
                    border-radius: 0.5rem;
                    margin-top:0.5rem;
                    margin-bottom:0.5rem;
                    background: $back-white;
                    padding: 1rem;
                    .english-title{
                        position: absolute;
                        right: 0;
                        top: 0;
                        margin-right: 0.9rem;
                        padding-right: 0.5rem;
                        padding-left: 0.5rem;
                        color: $back-white;
                        font-weight: bold;
                        border: solid $dark-blue;
                        border-radius: 50vh;
                        background:rgba(252, 75, 175, 0.961);               
                    }
                    .font{
                        font-size: 1.5rem;
                        flex-basis: 10%;
                    }
                    .grade{
                        flex-basis: 30%;
                        font-size: 1.5rem;
                        font-weight: bold;
                    }
                    .description{
                        flex-basis: 60%;
                    }
                }

            }
        }
        .l-wrapper{
            .l-container{
                display: flex;
                flex-direction: column;
                // justify-content: center;
                // nim-height: 75%;
                // min-height: 60%;
                padding-bottom: 2rem;
                .close-grade{
                    // width: inherit;
                    // left:auto;
                    display: flex;
                    justify-content: flex-end;
                    .close{
                        position: fixed;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        border: 0.2rem solid rgb(180, 179, 179);
                        border-radius: 50vh;
                        width: 1.5rem;
                        height: 1.5rem;
                        margin-top: 0.2rem;
                        margin-right: 0.2rem;
                        color: rgb(172, 172, 172);
                    }
                }
                .is-image{
                    width: 8rem;
                    height: auto;
                }
                .category-outer-loop{
                    width: 100%;
                    .category-inner-loop{
                        position: relative;
                        width: 100%;
                        display: flex;
                        align-items: center;
                        flex-direction: column;
                        .category-container{
                            display: flex;
                            position: relative;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            width: 80%;
                            border: solid $base-color;
                            border-radius: 0.5rem;
                            margin-top: 0.5rem;
                            margin-bottom: 0.5rem;
                            min-height: 3rem;
                            background: $background-bottom-right;
                            // transition: 1s;
                            .category-title-container.space{
                                margin-top:0.6rem;
                                margin-bottom: 1rem;
                            }
                            .category-title-container{
                                height: 100%;
                                width: 100%;
                                .category-title{
                                    color: white;
                                    font-weight: bold;
                                    transition: 0.5s;
                                    .fa-caret-down{
                                        position: absolute;
                                        right:0;
                                        margin-top: 0.3rem;
                                        margin-right: 1rem;
                                        transition: 0.5s;
                                    }
                                    .lotate{
                                        transform:rotate(180deg);
                                    }
                                }
                            }
                            .option-container{
                                width: 100%;
                                .option-loop{
                                    width: 100%;
                                    .each-option{
                                        display: flex;
                                        justify-content: center;
                                        margin-bottom: 0.5rem;
                                        .option-font{
                                            flex-basis: 35%;
                                            display: flex;
                                            justify-content: flex-end;
                                            .fa-apple-alt{
                                                color: $dull-red
                                            }
                                            .fa-carrot{
                                                color: rgb(255, 188, 63)
                                            }
                                            .fa-cat{
                                                color: brown;
                                            }
                                            .fa-car-side{
                                                color: rgb(68, 70, 220);
                                            }
                                            .fa-utensils{
                                                color: gray;
                                            }
                                            .fa-mug-hot{
                                                color: rgb(223, 221, 221);
                                            }
                                        }
                                        .option-title{
                                            flex-basis: 65%;
                                            display: flex;
                                            margin-left: 1rem;
                                            p{
                                                color: white;
                                                font-weight: bold;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
</style>