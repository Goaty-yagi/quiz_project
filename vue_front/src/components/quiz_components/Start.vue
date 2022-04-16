<template>
    <div class="start-wrapper">
        <div class="main-wrapper">
            <div class="quiz-title-container">
                <p class="start-title">初級・くだもの問題</p>
                <p class="start-length">全{{ questionLength }}問</p>
            </div>
            <div class="button-container">
                <div @click="closeStart()" class="btn-base-black-db-ov">
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
        'questionLength'
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
            margin-top: 1rem;
            padding: 0.5rem;
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
            margin-top: 1rem;
            margin-bottom: 1rem;
            .btn-base-black-db-ov{
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