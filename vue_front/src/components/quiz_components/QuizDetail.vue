<template>
    <div class="l-wrapper">
        <div class="main-wrapper">
            <div class='main-quizdetail-wrapper'>
                <div class='l-container'>
                    <div class="close-container">
                        <div @click="close" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <div class="main-detail-container">
                        <div class="question-field">
                            <p class="detail-text">Grade</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.grade }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Status</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.status }}</p>
                        </div>
                        <div class="question-field">
                            <p class="detail-text">Field</p>
                            <p class="center">:</p>
                            <p class="detail-val">{{ questionDetailInfo.field }}</p>
                        </div>
                        <div class="question-label">
                            <p class="question-text">Question</p>
                            <div class="question-container">
                                <p class="question-description">{{ questionDetailInfo.label }}</p>                                
                            </div>
                        </div>
                        <div v-if="questionDetailInfo.image" class="image-container">
                            <img class="image" v-bind:src="questionDetailInfo.image"/>
                        </div>
                    </div>
                    <div @click="questionDelete(questionDetailInfo.id)" class="btn-gray-black-gray-sq">
                        削除しますか
                    </div>                  
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:[
        'questionDetailInfo'
    ],
    mounted(){
        console.log('mounted at detail',this.questionDetailInfo)
    },
    computed:{
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
    },
    methods:{
        addStep(){
            this.$router.push({ name: 'Account' })
            // this.$emit('sentHandle')
            // this.$emit('handle')
            // this.$store.commit('addStep')
        },
        close(){
            this.$emit('handleQuizDetail')
        },
        questionDelete(id){
            console.log("clicked")
            this.$emit('deleteMyQuestion')
            this.close()
        }
    },
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.main-quizdetail-wrapper{
    display: flex;
    justify-content: center;
    width: 100%;
    .l-container{
        .main-detail-container{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 2rem;
            margin-bottom: 2rem;
            .question-field{
                display: flex;
                justify-content: center;
                margin-bottom: 0.4rem;
                border-bottom: 0.2rem solid $lite-gray;
                padding: 0.5rem;
                width: 80%;
                .detail-text{
                    flex-basis: 50%;
                    display: flex;
                    justify-content: flex-end;
                    font-weight: bold;
                    margin-right: 0.5rem;
                }
                .detail-val{
                    flex-basis: 50%;
                    display: flex;
                    font-weight: bold;
                    margin-left: 0.5rem;
                }
                .center{
                    font-weight: bold;
                }
            }
            .question-label{
                display: flex;
                justify-content: center;
                flex-direction: column;
                align-items: center;
                width: 100%;
                .question-text{
                    font-weight: bold;
                    margin-bottom: 0.3rem;
                }
                .question-container{
                    background: $lite-gray;
                    padding:0.5rem;
                    width: 80%;
                }
            }
        }
        .btn-gray-black-gray-sq{
            display: inline-block;
            padding-right: 0.3rem;
            padding-left: 0.3rem;
            margin-bottom: 1rem;
        }

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
</style>