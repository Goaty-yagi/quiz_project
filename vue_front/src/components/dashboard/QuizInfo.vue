<template>
    <section class='quiz-info-section'>
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <div class="bar-wrapper">
                <bar
                :chart-data='barChartData'
                :detail="detail"
                @barChartDetail="barChartDetail"/>
            </div>
            <div class="chart-footer">
                <div @click="setBarChartData()" class='all-quizzes' :class="{'selected':!currentTitle}">
                    <p class="all">ALL</p>
                </div>
                <p class="total">Total:{{sumOfAllQuestions}} questions</p>
                <div class="each-title-container">
                    <div class="title-loop"
                        v-for="(quiz,index) in quizNameId"
                        v-bind:key="index">
                        <p class="each-title" 
                            :class="{'selected-title':currentTitle==quiz.name}"
                            @click="barChartDetail(quiz.id-1)">{{ quiz.name }}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import ConfettiExplosion from "vue-confetti-explosion";
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Bar from '@/components/charts/Bar.vue'
import  Chart from '@/components/account/Chart.vue'
import axios from 'axios';

export default {
    name: 'Home',
    components: {
        TestConf,
        Notification,
        NotLogin,
        Bar,
        Chart,
        ConfettiExplosion
    },
    data(){
        return{
            numOfQuestions:'',
            detail: false,
            fixedTitleArray:[],
            currentTitle:'',
            
            field:'並び替え',
            showCompo: false,
            showNotLogin: false,
            item:{status: 1,num:5,test:true},
            test1:"",
            slideIn:true,
            slideOut:false,
            // showChart:false,
            backgroundColorList:[
                'rgba(255, 153, 51, 0.2)',
                'rgba(81, 255, 0, 0.2)',
                'rgba(191, 0, 255, 0.2)',
                'rgba(255, 6, 6, 0.2)',
            ],
            sumOfAllQuestions:'',
            barChartData:{
                labels: [],
                datasets: [{ 
                    label: "",
                    data: [],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(201, 203, 207, 0.2)'
                        ],
                    borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)',
                    'rgb(201, 203, 207)'
                    ],
                }]
            },
            chartData: {
                labels: ["形容詞","文法","動詞","語彙","数字"],
                datasets: [{ 
                    label: "",
                    data: [7,3,8,1,9],
                    borderWidth:1,
                    backgroundColor:'rgba(81, 255, 0, 0.2)',
                    borderColor: ' #ff9933',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'red'
                }],
            },
        }
    },
    created() {
        
    },
    mounted(){
        this.getNumOfQuestions()
        console.log('mounted',this.$store)
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        tempUser(){
            return this.$store.state.signup.tempUser
        },
        reccomendedQuestion(){
            return this.$store.getters.gettersReccomendedQuestion
        },
        emailVerified(){
            return this.$store.getters.getEmailVerified
        },
        tempUserTest(){
            try{
                return this.$store.state.signup.tempUser.test
            }
            catch{
                return false
            }
        },
        questions(){
            return this.$store.getters.questions
        },
        quizNameId(){
                    return this.$store.getters.quizNameId
        },
    },
    methods:{
        async getNumOfQuestions() {
            try{
                const response = await axios.get('/api/questions-dashboard/')
                this.numOfQuestions = response.data[0]
                console.log('data',this.numOfQuestions)
                this.setBarChartData()
            } catch {

            }
        },
        setBarChartData() {
            this.detailFalse()
            this.currentTitle=''
            const tempList = []
            const tempLadelList = []
            for(let i of this.numOfQuestions.get_num_of_question.slice(0,this.numOfQuestions.get_num_of_question.length-1)) {
                let title = Object.keys(i)[0]
                tempLadelList.push(title)
                this.fixedTitleArray = tempLadelList
                this.barChartData.labels = tempLadelList
                tempList.push(i[title].sum)
                this.barChartData.datasets[0].data = tempList
            }
            this.sumOfAllQuestions = this.numOfQuestions.get_num_of_question[this.numOfQuestions.get_num_of_question.length-1].all_questions_num
        },
        barChartDetail(index) {
            for(let i of this.numOfQuestions.get_num_of_question.slice(0,this.numOfQuestions.get_num_of_question.length-1)) {
                if(Object.keys(i)[0]==this.fixedTitleArray[index]){
                    this.currentTitle = this.fixedTitleArray[index]
                    this.barChartData.datasets[0].data= Object.values(i[this.fixedTitleArray[index]])
                    this.barChartData.labels = Object.keys(i[this.fixedTitleArray[index]])
                    this.detail = true
                    
                }
            }
        },
        detailFalse() {
            this.detail = false
        },
        // selectedBarChartDetail(index) {
        // },
        unko(){
            console.log('clicked')
            this.$store.commit('setTempUserNull')
            // window.localStorage.removeItem('quizkey')
            // return `/quiz/${this.status}`
            },
        componentHandler(){
            if(this.tempUserTest){
                this.handleShowNotLogin()
            }
            else{
                this.showCompoHandler()
            }
        },
        showCompoHandler(){
        this.showCompo = !this.showCompo
        },
        handleShowNotLogin(){
            this.showNotLogin = !this.showNotLogin
        },
        // async test(){
        //     await axios
        //     .get("https://ipinfo.io/json?token=32e16159d962c5")
        //     .then(response => {
        //         this.test1 = response.data
        //         console.log(this.test1.city)
        //         })
        //     .catch(error => {
        //         console.log(error)
        //     })      
        // },
        scrollTop(){
            window.scrollTo({
            top: 0,
            // behavior: "smooth"
            });
        },
        async setInitUserStatus(){
            if(this.emailVerified){
                if(this.$store.getters.getTempUser.test){
                    this.$store.commit('setQuizTakerID',this.user.quiz_taker.id)
                    this.$store.commit('setQuizID',this.$store.getters.getTempUser.grade)
                    for(let i of this.$store.getters.getTempUser.statusList){
                        await this.$store.dispatch('userStatusPost',i)
                    }
                }
                this.$store.commit('setTempUserReset')
            }
        },
        testClick(){
            this.slideIn = !this.slideIn
            this.slideOut = !this.slideOut
        },
        aaa(){
            let b = document.getElementsByClassName('hero-title')
            console.log('aaa',b,b.length)
            b[2].style.backgroundColor = 'red'
        }
        // reload(){
        //     console.log('reload_enter',this.$store.state.signup.beingException)
        //     if(this.$store.state.signup.beingException){
        //         console.log('reload_desu')
        //         window.location.reload();
        //     }
        // }
    }
}       
</script>
<style scoped lang="scss">
@import "style/_variables.scss";

.quiz-info-section{
    width:100%;
    // height: 100vh;
    display: flex;
    // justify-content: center;
    align-items: center;
    flex-direction: column;
    .main-wrapper{
        // display: flex;
        .bar-wrapper{

        }
        .chart-footer{
            display: flex;
            flex-direction: column;
            align-items: center;
            .all-quizzes{
                color: white;
                padding: 0 1rem;
                margin: 0.5rem 0;
                font-size: 1.2rem;
                font-weight: bold;
                border: solid $base-color;
                border-radius: 50vh;
                transition: .5s;
                .all{

                }                
            }
            .selected{
                color: $dark-blue;
                background: $base-color-tr;
                border: solid white;
            }
            .total{
            color: white;
            font-weight: bold;
            margin-bottom: 0.5rem;
            }
            .each-title-container{
                display: flex;
                justify-content: center;
                width: 100%;
                .title-loop{
                    .each-title{
                        color: white;
                        margin-left: 0.5rem;
                        margin-right: 0.5rem;
                        padding: 0 0.4rem;
                        font-weight: bold;
                        border: solid $base-color;
                        transition: .5s;
                    }.selected-title{
                        color: $dark-blue;
                        background: $base-color-tr;
                        border: solid white;
                    }
                }

            }
        }
    }
}
.hero-title{
    border-top: 6px solid $base-color;
    border-right: 1px solid $base-color;
    border-left: 1px solid $base-color;
    border-bottom: 1px solid $base-color;
    // background: rgb(254, 254, 221);
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-right: 0.1rem;
    padding-left: 0.1rem;
    font-weight: bold;
    font-size: 1.1rem;
    color: white;

}



// @media(max-width: 1024px){

//   }
//   .home-section{
//     width:100%;
//     height: 100vh;
//     // height:100%;
//   }.wrapper{
//     flex-direction: column;
//     display: flex;
//     justify-content: center;
//     align-items: center;
//     width:100%;
//     // height:100%;
//     // bottom:10%;
//   }
//   .is-image{
//     width: 8rem;
//     height: auto;
//   }
//   .home-text{
//     font-size:2rem;
//     color:white;
//     font-weight: bold;
//   }
//   #or-button{
//     border-radius: 100vh;
//     border: 2px solid $base-color;
//     margin:1rem;
//     padding:0.4rem;
//     background: transparent;
//     color: $base-color;
//     font-weight:bold;
//     font-size: 1rem;
//     transition:0.5s;
//     }
//     #or-button:hover{
//       background: $base-color;
//       color:white;
//     }
//     .home-conf{
//       position:absolute;
//       left:0;
//     }
.slide-in{
	text-align: center;
	opacity: 0;
	animation: slide-in-anim 1.5s ease-out forwards;
}
.slide-out{
    text-align: center;
	opacity: 1;
	animation: slide-out-anim 1.5s ease-out forwards;
}

@keyframes slide-in-anim {
	20% {
		opacity: 0;
        transform: translateX(-20%);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 1;
		transform: translateX(0);
	}
}
@keyframes slide-out-anim {
	20% {
		opacity: 1;
        transform: translateX(0);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-20%);
        display: none;
	}
}
</style>
