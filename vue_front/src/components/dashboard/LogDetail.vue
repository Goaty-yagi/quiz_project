<template>
    <div class="l-wrapper">
        <div class="main-wrapper">
            <div class='main-quizdetail-wrapper'>
                <div class='l-container'>
                    <div class="close-container">
                        <div @click="close()" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <div class="main-detail-container" :class="{'noShow':noShow}" v-for="(value, key ,logindex) in loggers.results[DetailTagIndex]"
                        v-bind:key="logindex">
                        <div v-if="logindex!=0&&logindex!=5" class="question-field">
                            <p  class="detail-text">{{ key }}</p>
                            <p class="detail-val">{{ value }}</p>
                        </div>
                        <!-- <div class="question-field">
                            <p class="detail-text">Message</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{  }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Path</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{  }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">ActualErrorName</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{  }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">ActualErrorMessage</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{  }}</p>
                        </div> -->
                        <!-- <div class="question-label">
                            <p class="question-text">Question</p>
                            <div class="question-container">
                                <p class="question-description">{{  }}</p>                                
                            </div>
                        </div> -->
                        <!-- <div v-if="questionDetailInfo.image" class="image-container">
                            <img class="image" v-bind:src="questionDetailInfo.image"/>
                        </div> -->
                    </div>
                    <div class="angle-container">
                        <i class="fas fa-angle-double-left"></i>
                        <i class="fas fa-angle-double-right"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:[
        'loggers',
        'currentTagIndex'
    ],
    data(){
        return{
            DetailTagIndex: this.currentTagIndex,
        }
    },
    mounted(){
        this.$store.commit('showModalTrue')
        console.log('mounted at detail',this.questionDetailInfo)
    },
    beforeUnmount(){
        this.$store.commit('showModalFalse')
    },
    computed:{
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
    },
    methods:{
        close(){
            this.$emit('logDetailFalse')
        },
    },
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.main-quizdetail-wrapper{
    display: flex;
    justify-content: center;
    position: relative;
    width: 100%;
    .l-container{
        position: relative;
        width: 90%;
        .main-detail-container{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 1rem;
            margin-bottom: 1rem;
            .question-field{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                border-bottom: 0.2rem solid $lite-gray;
                width: 90%;
                .detail-text{
                    display: flex;
                    font-weight: bold;
                    font-size: 1.2rem;
                }
                .detail-val{
                    display: flex;
                    font-weight: bold;
                    margin-left: 0.5rem;
                    font-size: 0.9rem;
                }
            }
        }
        .angle-container{
            display: flex;
            justify-content: center;
            width: 100%;
            margin-bottom: 1rem;
            .fa-angle-double-left{
                margin-right: 2rem;
                font-size: 1.2rem;
                color: gray;
            }
            .fa-angle-double-right{
                margin-left: 2rem;
                font-size: 1.2rem;
                color: gray;
            }
        }
    }
}

</style>