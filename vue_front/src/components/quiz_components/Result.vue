<template>
    <div class="result_compo">
        <div class="result-title">
            <p class="result">-結果-</p>
            <p class="percentage">{{ getPercentage }}%正解</p>
        </div>
        <div class="result-scroll">
            <div class="result-scroll-header">
                <p class="question-length">全{{ question_length }}問</p>
            </div>

            <div class="result-contents">
                <div 
                class="result-loop"
                v-for="(value,key,index) in SelectedAnswerInfo" 
                v-bind:key="index">
                    <div class="loop-contnts">
                        <div class="question-num">{{ key }}問目</div>
                        <div v-if="value.isCorrect" class="results"><i class="far fa-circle"></i></div>
                        <div v-if="value.isCorrect==false" class="results"><i class="fas fa-times"></i></div>
                        <div v-if="value.isCorrect==null" class="results tri"><i class="fas fa-exclamation-triangle"></i></div>
                        <div @click="HandleResultPage(index,index+1)" class="detail">
                            <p>
                                詳細 =>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="buttons">
            <div @click="reset()" class="btn-tr-white-base-cir">戻る</div>
            <div @click="playAgain()" class="btn-tr-black-baselite-cir">もう一度</div>
        </div>
    </div>
</template>

<script>
export default {
    name:"Result",
    props:[
        'question_length',
        'SelectedAnswerInfo'
    ],
    data(){
        return{
            resultDetailslice:3,
            resultDetail: false,
        }
    },
    mounted(){
        console.log('mounted on result',this.currentQuizMode)
    },
    computed:{
        getPercentage(){
            let trueNum = 0
            Object.values(this.SelectedAnswerInfo).forEach(value => {
                if(value.isCorrect){
                    trueNum += 1
                }
            })
            return Math.round(trueNum/this.question_length * 100)
        },
        currentQuizMode(){
            return this.$store.getters.currentQuizMode
        }
    },
    methods:{
        numOfTrue(answered_array){
            let counter = 0
            for (let t of answered_array){
                if(t == true){
                counter += 1
                }
            }return counter
        },
        HandleResultPage(a,b){
            this.$emit('HandleShowResult')
            this.$emit('handlePagination',a,b)
            this.$emit('resultAnswerHandler')
        },
        getResultFont(result){
            if(result == true){
                return "result-font-green"
            }
            else if(result == false){
                return "result-font-red"
            }
        },
        returnFont(boolean){
            if(boolean == true){
                return "far fa-circle"
            }
            else if(boolean == false){
                return "fas fa-times"
            }
        },
        getJPResult(result){
            if (result == true){
                return '正解'
            }else{
                return'不正解'
            }
        },
        resultDetailHandler(slice){
            if(slice <= 5){
                console.log(this.resultDetailslice)
                this.resultDetailslice = 100
                this.resultDetail = true
            }
            else{
                this.resultDetailslice = 3
                this.resultDetail = false
            }
        },
        storeReset(){
            this.$store.commit('reset')
        },
        reset: function () {
            location.reload()
        },
        showDetail(){
            this.$emit('show')
        },
        playAgain(){
            this.$emit('playAgain')
        },
        backQuizHome(){
            this.$emit('backQuizHome')
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.result_compo{  
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: auto;
    overflow: scroll;
    // min-height:90vh;
    .result-title{
        .result{
            font-size: 2rem;
            color: rgb(255, 81, 81);
            font-weight: bold;
        }
        .percentage{
            color: $back-white;
            font-size: 1.5rem;
            font-weight: bold;
        }
    }
    .result-scroll{
        display: flex;
        flex-direction: column;
        background: $back-tr-white;
        border: solid $base-color;
        border-radius: 0.5rem;
        width: 90%;
        height: 350px;
        overflow: scroll;
        .result-scroll-header{
            margin-top: 0.5rem;
            .question-length{
                font-size: 1.3rem;
            }
        }
        .result-contents{
            .result-loop{
                display: flex;
                justify-content: center;
                width: 100%;
                margin-top: 0.5rem;
                margin-bottom: 0.5rem;
                .loop-contnts{
                    display: flex;
                    justify-content: center;
                    width: 80%;
                    margin-top: 0.5rem;
                    // margin-bottom: 0.5rem;
                    padding-bottom: 0.5rem;
                    border-bottom: solid rgb(203, 203, 203);
                    .question-num{
                        flex-basis: 40%;
                    }
                    .results{
                        flex-basis: 20%;
                        font-size: 1.2rem;
                    }
                    .tri{
                        color: rgb(204, 204, 7);
                        font-size: 1.2rem;
                    }
                    .fa-circle{
                        color:rgb(39, 187, 39);
                    }
                    .fa-times{
                        color: $dull-red;
                    }
                    .detail{
                        flex-basis: 40%;
                        p{
                            transition: .5S;
                            
                        }
                        p:hover{
                            display: inline-block;
                            border: solid $lite-gray;
                            padding-right: 0.5rem;
                            padding-left: 0.5rem;
                            background: $back-white;
                            transition: .5S;
                        }
                    }
                }
            }
        }
    }
    .buttons{
        padding: 1rem;
        .btn-tr-white-base-cir{
            padding-right: 0.8rem;
            padding-left: 0.8rem;
            margin-right: 0.5rem;
        }
        .btn-tr-black-baselite-cir{
            padding-right: 0.8rem;
            padding-left: 0.8rem;
        }        
    }
}
</style>