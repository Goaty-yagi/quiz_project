<template>
    <div class="logger-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div  :class="{'notification-blue':$store.state.board.notifications.reply}">
            <div class="notification-text">
                
            </div>
        </div>
        <div class="main-wrapper">
            <div class="main-container" >
                <div class="logger-header">
                    <p>新しいログ{{  }}件</p>
                    <!-- <p class="title-white">My-Quiz</p>
                    <p class="register">登録数{{ length }} / {{myQuiz.max_num}}</p>
                    <p class="max">(最大 {{myQuiz.max_num}} 個まで登録できます)</p> -->
                </div>
                <!-- {{ loggers }} -->
                <div class="logger-container" v-if="$store.state.isLoading==false">
                    <div class="no-my-quiz" v-if="!loggers.results">
                        <div class="no-quiz">
                            ログはありません。<br>
                        </div>
                    </div>
                    <div class=logger-loop @click="logDetailTrue(logindex)" v-for="(log,logindex) in loggers.results"
                        v-bind:key="logindex">
                        <div class="each-log-container">
                            <div class="question-index-container">
                                <div class="question-index">{{ logindex+1 }}</div>
                            </div>
                            <!-- <div class="log-time">{{ log.created_on }}</div> -->
                            <div class="log-time">{{ log.created_on }}</div>
                            <!-- <div class="log-message">{{ log.actualErrorMessage.substr(0,15)+'...'  }}</div> -->
                            <div v-if="!log.checked" class="log-checked" >{{ ckeckedToString(log.checked) }}</div>
                        </div>
                    </div>
                    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': loading }">
                        <div class="lds-dual-ring"></div>
                    </div>
                    <i v-if="this.nextUrl" @click="getNextLogger()" class="fas fa-angle-down"></i>
                    <LogDetail
                    v-if="logDetail"
                    :loggers="loggers"
                    :currentTagIndex="currentTagIndex"
                    :nextUrl="nextUrl"
                    :noMoreUrl="noMoreUrl"
                    @logDetailFalse="logDetailFalse"
                    @getNextLogger="getNextLogger"             
                    />
                </div>
                <!-- <div @click="handleQuizOpen()" v-if="showButtonAndNoQuiz" class="btn-basegra-white-db-sq">
                    練習
                </div> -->
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import LogDetail from '@/components/dashboard/LogDetail.vue'
import axios from 'axios';

export default {
    components: {
        LogDetail,
    },
    data(){
        return{
            errorMessage:"components/dashboard/Logger",
            loggers: "",
            logDetail: false,
            currentTagIndex:'',
            nextUrl: '',
            loading: false,
            noMoreUrl: false,
        }
    },
    mounted(){
        this.getLogger()
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        myQuiz(){
            return this.$store.state.signup.djangoUser.my_quiz[0]
        },
        fieldNameId(){
            return this.$store.getters.fieldNameId
        },
        quizNameId(){
            return this.$store.getters.quizNameId
        },
        statusNameId(){
            this.$store.dispatch("getStatusNameId")
            return this.$store.getters.statusNameId
        }

    },
    methods:{
        async getLogger(){
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/enquire-list')
                .then(response => {
                    this.loggers = response.data
                    if(response.data.next){
                        this.nextUrl = response.data.next
                    } else {
                        this.noMoreUrl = true
                    }
                    console.log('getlog', this.loggers)
                    })
                .catch(e => {
                    let logger = {
                    message: this.errorMessage + 'getLogger',
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit("checkDjangoError",e.message)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
                })
            this.$store.commit('setIsLoading', false)
        },
        async getNextLogger() {
            console.log('next')
            this.loading = true
            await axios
                .get(this.nextUrl)
                .then(response => {
                    console.log(response.data.results)
                    this.loggers.results.push(response.data.results[0])
                    console.log('n',response.data.next)
                    this.nextUrl = response.data.next
                    })
                .catch(e => {
                    let logger = {
                    message: this.errorMessage + 'getLogger',
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit("checkDjangoError",e.message)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
                })
            this.loading = false

        },
        ckeckedToString(checked) {
            if(checked){
                return ''
            } else {
                return '未確認'
            }
        },
        logDetailFalse() {
            this.logDetail = false
        },
        logDetailTrue(index) {
            this.currentTagIndex = index
            this.logDetail = true
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.main-container{
        display: flex;
        flex-direction: column;
        align-items: center;
        }

.logger-wrapper{
    display: flex;
    justify-content: center;
    .main-wrapper{
        .logger-header{
            margin-bottom: 1rem;
            .register{
                font-size: 1.3rem;
                color: $lite-gray;
                font-weight: bold;
            }
            .max{
                font-size: 0.8rem;
                color: $lite-gray;
            }
        }
        .logger-container{
            width: 95%;
            min-height: 300px;
            max-height: 350px;
            border: solid $base-color;
            border-radius: 5px;
            background: $back-white;
            padding-top: 1rem;
            padding-bottom: 1rem;
            overflow: scroll;
            .no-my-quiz{
                margin:2rem;
                .no-quiz{
                    color: $dark-blue;
                    font-weight: bold;
                    margin-bottom: 2rem;
                }
            
            }
            .logger-loop:hover{
                background: $back-lite-white;
                border-bottom: solid $lite-gray;
            }
            .logger-loop{
                position: relative;
                display: flex;
                align-items: center;
                border-bottom: solid $lite-gray;
                transition: .5s;
                .each-log-container{
                    position: relative;
                    display: flex;
                    width: 100%;
                    margin-bottom: 1rem;
                    margin-top: 1rem;
                    // padding-bottom: 0.5rem;
                    align-items: center;
                    // justify-content: center;
                    .question-index-container{
                        flex-basis: 10%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        .question-index{
                            border: solid $base-color;
                            border-radius: 50vh;
                            width: 1.7rem;
                            height: 1.7rem;
                            margin-left: 0.4rem;
                            font-weight: bold;
                            background: $dark-blue;
                            color: white;
                        }
                    }
                    .log-time{
                        flex-basis: 30%;

                    }
                    .log-message{
                        flex-basis: 50%;
                    }
                    .log-checked{
                        position: absolute;
                        flex-basis: 10%;
                        right: 0;
                        color: red;
                        margin-right: 0.5rem;
                        border: solid $dull-red;
                    }
                }
            }
            .fa-angle-down{
                margin-top: 1rem;
            }
        }
        .btn-basegra-white-db-sq{
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            font-weight: bold;
            font-size: 1.2rem;

        }

    }

}
</style>