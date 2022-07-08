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
                    <div class="log-index">{{ DetailTagIndex+1 }}</div>
                    <div class="main-detail-container" :class="{'noShow':noShow(logindex)}" v-for="(value, key ,logindex) in loggers.results[DetailTagIndex]"
                        v-bind:key="logindex">
                        <div v-if="logindex!=0&&logindex!=5" class="question-field">
                            <p class="detail-text">{{ key }}</p>
                            <p class="detail-val">{{ value }}</p>
                        </div>
                    </div>
                    <div class="angle-container">                        
                        <!-- @click="e => result==false && onClick(answerindex,answer,question)" -->
                        <i @click="e => DetailTagIndex!=0&& back()" :class="DetailTagIndex==0 ? 'space-left':'fas fa-angle-double-left'"></i>
                        <i @click="e => !nextUrl&&DetailTagIndex!=loggers.results.length-1&& next(e)||typeof nextUrl=='string' && next()" :class="!nextUrl&&DetailTagIndex==loggers.results.length-1 ? 'space-right':'fas fa-angle-double-right'"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props:[
        'loggers',
        'currentTagIndex',
        'nextUrl',
        'noMoreUrl',
        'patchUrl',
    ],
    data(){
        return{
            errorMessage:"components/dashboard/LoggerDetail",
            DetailTagIndex: this.currentTagIndex,
            logIdList: []
        }
    },
    mounted(){
        this.ckeckedTrue()
        this.$store.commit('showModalTrue')
        console.log('mounted at detail',this.nextUrl)
    },
    beforeUnmount(){
        console.log('BU')
        this.patchLogger()
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
        next(e) {
            console.log('clicked',e)
            if(this.DetailTagIndex!=this.loggers.results.length-1){
                this.DetailTagIndex += 1
                this.ckeckedTrue()
            } else if (this.nextUrl&&this.DetailTagIndex==this.loggers.results.length-1){
                this.getNextLogger(this.ckeckedTrue())
                this.DetailTagIndex += 1
                
            }
        },
        ckeckedTrue() {
            console.log('checkedTrue',this.loggers.results,this.DetailTagIndex)
            if(!this.loggers.results[this.DetailTagIndex].checked) {
                this.loggers.results[this.DetailTagIndex].checked = true
                this.logIdList.push(this.loggers.results[this.DetailTagIndex].id)
            }
            console.log('true',this.loggers.results,this.logIdList)
        },
        back() {
            this.DetailTagIndex -= 1
            this.ckeckedTrue()
        },
        getNextLogger() {
            this.$emit('getNextLogger')
        },
        noShow(index) {
            if(index==0||index==5) {
                console.log('true',index)
                return true
            } else {
                return false
            }
        },
        async patchLogger(){
            this.$store.commit('setIsLoading', true)
            console.log(this.logIdList)
            if(this.logIdList.length) {
                // let a = '/api/loggers-patch?logList='
                await axios
                .patch(`/api/loggers-patch?logList=${this.logIdList}`)
                .catch(e => {
                    let logger = {
                    message: this.errorMessage + 'patchLogger',
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit("checkDjangoError",e.message)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
                })
            }
            this.$store.commit('setIsLoading', false)
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
        .log-index{
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid $base-color;
            border-radius: 50vh;
            width: 1.5rem;
            height: 1.5rem;
            margin-left: 0.6rem;
            margin-top: 0.3rem;
            font-weight: bold;
            background: $dark-blue;
            color: $lite-gray;
        }
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
                    color: rgb(167, 167, 167);
                }
                .detail-val{
                    font-weight: bold;
                    margin-left: 0.5rem;
                    font-size: 0.9rem;
                    width: 90%;
                    max-width: 90%;
                    // margin: 0 1rem;
                    overflow-wrap: break-word;
                }
            }
        }
        .noShow{
            display: none;
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
                transition: .5s;
            }
            .fa-angle-double-left:hover{
                color: $lite-blue;
            }
            .space-left{
                margin-right: 2rem;
                width: 1.2rem;
            }
            .fa-angle-double-right{
                margin-left: 2rem;
                font-size: 1.2rem;
                color: gray;
                transition: .5s;
            }
            .fa-angle-double-right:hover {
                color: $lite-blue;
            }
            .space-right{
                margin-left: 2rem;
                width: 1.2rem;
            }
        }
    }
}

</style>