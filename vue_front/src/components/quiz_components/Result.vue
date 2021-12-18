<template>
  <div class='result-compo'>
      <div class='box is-paddingless pb-4'> 
        <div class='button my-5 has-background-info-light is-centered is-static'>
            <p class="title is 3 has-text-danger">結果発表</p>          
        </div>
        <div>
            <p class="mx-5 is-inline-block subtitle is 4">{{ question_length }}問中</p>
            <p class="is-inline-block has-text-danger-dark title is 4">{{ numOfTrue(rerultAnswer) }} 問正解</p>
            <div>
                <p class="subtitle is 5 button is-rounded is-static"> 正解率 {{ getPercentage(numOfTrue(rerultAnswer),question_length) }}%</p>
            </div>
        </div>
    </div>
    <section class="section">
        <div class='result pt-6'>
            <div class="columns is-multiline is-vcentered is-mobile is-centered"
                v-for="(result,resultindex) in rerultAnswer.slice(0,resultDetailslice)"
                v-bind:key="resultindex"
                style='margin-top: -2rem'
                id='result-column'>
                <div class="column">
                    <p class='subtitle'>{{ resultindex+ 1 }} 問目</p>
                </div>
                <div class="column result-all">
                    <div class='result-font' :class='getResultFont(result)'>
                    <i id='result-font' :class='returnFont(result)'></i>
                    </div>
                </div>
                <div class="column" id='resultString'>
                    <p class='subtitle is 4'>{{ getJPResult(result) }}</p>
                </div>
            </div>
            <div style='margin-top: -2rem'>
                <div class='mt-6' v-if='!resultDetail' @click='resultDetailHandler(resultDetailslice)'>
                    <i class="fas fa-chevron-circle-down fa-2x" style='color: lightgray'></i>  
                </div>

                <div v-if='resultDetail' @click='resultDetailHandler(resultDetailslice)'>
                    <i class="fas fa-chevron-circle-up fa-2x" style='color: lightgray'></i> 
                </div>
            </div>
        </div>
        <div>
            <button @click='showDetail' class="button mt-2 is-info is-rounded">詳細を見る</button>
        </div>    
    </section>
    
        <router-link to="/" @click='storeReset' class="mx-2 button is-primary is-outlined">戻る</router-link>
        <div @click='reset' class="mx-2 button is-warning is-light">もう一度</div>
  </div>
</template>

<script>
export default {
    name:"Result",
    props:[
        'question_length',
        'rerultAnswer'
    ],
    data(){
        return{
            resultDetailslice:3,
            resultDetail: false,
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
        getPercentage(answer,question_length){
            return Math.round(answer/question_length * 100)
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
        }
    }
}
</script>

<style>

</style>