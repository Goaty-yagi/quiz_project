<template>
    <div class="start-wrapper">
        <div class="main-wrapper">
            <div class="quiz-title-container">
                <div v-if="forQuizPageInfo.all==false" class="not-all">
                    <div class="start-grade">
                        <p>{{ forQuizPageInfo.grade }}</p>
                    </div>
                    <p class="field-and-option">{{ forQuizPageInfo.field }}</p>
                    <p class="field-and-option"> {{forQuizPageInfo.option}}問題</p>
                </div>
                <div v-if="forQuizPageInfo.all" class="dojo">{{ forQuizPageInfo.grade }}道場</div>
                <p class="start-length">全{{ questionLength }}問</p>
            </div>
            <div class="button-container">
                <div @click="closeStart()" class="btn-base-white-db-sq">
                    START
                </div>
            </div>
            <div class="start-notification">
                ・クイズはランダムに作成されるので
                毎回問題が異なります。
                何回も挑戦してみてね。
            </div>
        </div>
      
    </div>
</template>

<script>
export default {
    props:[
        'questionLength',
        'forQuizPageInfo'
        // 'questions',
        // 'showQuiz'
    ],
    data(){
        return{
        }
    },
    mounted(){
        this.questionLength
        this.scrollTop()
    },
    methods:{
        goQuiz(){
            this.$emit('goQuiz')
        },
        closeStart(){
            this.$emit('closeStart')
            // this.progressBar()
        },
        scrollTop(){
            window.scrollTo({
            top: 0,
            // behavior: "smooth"
            });
        },
        // progressBar(){
        //     this.$emit('progressBar')
        // }
        // handleSHowQuiz(){
        //     this.$emit('handle')
        // },
    }
    }
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.start-wrapper{
    .main-wrapper{
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        // justify-content: center;
        .quiz-title-container{
            width: 80%;
            border: solid $base-color;
            border-radius: 0.5rem;
            background: $back-white;
            margin-top: 3rem;
            // padding: 1rem;
            overflow: hidden;
            .not-all{
                width: 100%;
                .start-grade{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 60px;
                    font-size: 1.5rem;
                    font-weight: bold;
                    background: $background-bottom-right;
                    border-bottom: solid $base-color;
                    color: white; 
                }
                .field-and-option{
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                    font-weight: bold;
                }
            }
            .start-length{
                border: solid $middle-blue;
                border-radius: 50vh;
                padding-right: 0.5rem;
                padding-left: 0.5rem;
                margin-bottom: 1rem;
                display: inline-block;
                font-size: 1.5rem;
                font-weight: bold;
            }
        }
        .dojo{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px;
            font-size: 1.5rem;
            font-weight: bold;
            background: $background-bottom-right;
            border-bottom: solid $base-color;
            color: white; 
        }
        .button-container{
            margin-top: 2rem;
            margin-bottom: 2rem;
            .btn-base-white-db-sq{
                padding-top: 0.3rem;
                padding-bottom: 0.3rem;
                padding-right: 0.8rem;
                padding-left: 0.8rem;
                font-size: 1.5rem;
                font-weight: bold;
            }
        }
        .start-notification{
            width: 80%;
            color: white;
            margin-top: 2rem;
        }
    }
}

</style>