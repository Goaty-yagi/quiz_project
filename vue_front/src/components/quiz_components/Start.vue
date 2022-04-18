<template>
    <div class="start-wrapper">
        <div class="main-wrapper">
            <div class="quiz-title-container">
                <p v-if="forQuizPageInfo==false" class="start-title">{{ forQuizPageInfo.grade }}・{{ forQuizPageInfo.field }}問題</p>
                <p v-if="forQuizPageInfo" class="start-title">{{ forQuizPageInfo.grade }}道場</p>
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
    },
    methods:{
        goQuiz(){
            this.$emit('goQuiz')
        },
        closeStart(){
            this.$emit('closeStart')
            // this.progressBar()
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
            padding: 1rem;
            .start-title{
                font-size: 1.5rem;
                font-weight: bold;
            }
            .start-length{
                font-size: 1.5rem;
                font-weight: bold;
            }
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