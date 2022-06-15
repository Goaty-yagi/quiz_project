<template>
    <div class="dashboard-wrapper" >
        <div class="">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <div class="dashboard-container" v-if="$store.state.isLoading==false">
                <div class="header-flex">
                    <h1 class='title-white'>ダッシュボード</h1>
                </div>
                <div class="side-bar" :class="{'less-side-bar':showSideBar==false}">
                    <i @click="handleShowSideBar()" 
                        class="fas fa-angle-double-left"></i>
                    <div class='space'></div>
                    <div class="option-loop" v-for="(val, key, index) in options"
                        :key="index">
                        <div v-if="showSideBar" class="each-option" :class="{'select-option':selectOption(key)}" @click="handleEachPage(key)">
                            {{ key }}   
                        </div>       
                    </div>
                </div>
            </div>
        </div>
        <CreateQuizQuestion
        v-if="options.createQuiz"/>
        <QuizInfo
        v-if="options.quizInfo"/>
    </div>
</template>

<script>
import CreateQuizQuestion from '@/components/dashboard/CreateQuizQuestion.vue'
import QuizInfo from '@/components/dashboard/QuizInfo.vue'

export default {
    components: {
        CreateQuizQuestion,
        QuizInfo
    },
    data(){
        return{
            showSideBar: true,
            currentOption:'quizInfo',
            options:{
                'quizInfo':true,
                'createQuiz':false,
                }
                
        }
    },
    mounted(){
        console.log('mounted at dashboard',this.showSideBar)
    },
    conoputed:{

    },
    methods:{
        handleShowSideBar(){
            console.log(this.showSideBar)
            this.showSideBar = !this.showSideBar 
            console.log(this.showSideBar)
        },
        handleEachPage(key) {
            console.log('OP',key,this.options[key])
            if(this.options[key] == false){
                this.options[key] = true
                this.options[this.currentOption] = false
                this.currentOption = key
            }
        },
        selectOption(key){
            if(this.currentOption == key){
                return true
            } else {
                return false
            }
        },
        
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";



.dashboard-wrapper{
    width: 100%;
    margin: 0;
    position: relative;
    // display: flex;
    // justify-content: center;
    .side-bar{
        position: fixed;
        left: 0;
        bottom: 0;
        margin-top: 1rem;
        background: $dark-tr-blue;
        width: 200px;
        height: 100%;
        transition: .5s;
        z-index: 1;
        .fa-angle-double-left{
            position: absolute;
            right: 0;
            color: $lite-gray;
            margin-top: 0.5rem;
            margin-right: 0.5rem;
            transition: .5s;
        }
        .space {
            height: 1rem;
        }
        .option-loop{
            color: white;
            margin-top: 0.5rem;
            .each-option{
                margin-top: 1rem;
                transition: .5s;
                font-weight: bold;
            }
            .each-option:hover {
                background: $lite-gray;
                color: $lite-blue;
            }
            .select-option{
                background: $lite-gray;
                transition: .5s;
                color: $dark-blue;
            }
        }
    }
    .less-side-bar{
        width: 50px;
        .fa-angle-double-left{
            transform: rotate(180deg);
           
        }
    }
    .main-wrapper{
        .dashboard-container{
            // flex-direction: column;
            // justify-content: center;
            // align-items: center;
            margin: 0;
            width: 100%;
        }
    }
}
// @media(max-width: 629px){
//     .side-bar{
//         width: 100%;
//         // margin-bottom: 20%;
//     }
//     .less-side-bar{
//         width: 0px;
//     }
// }
</style>