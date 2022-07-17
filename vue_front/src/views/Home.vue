<template>
    <section class='home-section'>
        <!-- <ConfettiExplosion 
        :particleCount="150"
        :particleSize="12"
        :duration="3500"
        :force="0.5"
        :stageHeight="800"
        :stageWidth="1600"
        :shouldDestroyAfterDone="true"/> -->
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div v-if="!showCompo" class='home-main-wrapper'>
                <div class="home-hero">
                    <p class="hero-title">楽しく学ぶ最高峰の日本語ラーニングコミュニティ</p>
                    <img @click="testClick" src="@/assets/logo-with-logo.png">
                    <div class="hero-paragraph-wrapper">
                        <div class="paragraph-container">
                            <p class="hero-paragraph">自分のレベルに合った問題をクイズ形式で
                            解き、実力の確認ができるプラットフォーム。</p>
                            <chart
                            class="hero-image"
                            :chart-data="chartData"
                            />
                            <!-- <img @click="testClick" class='hero-image' src="@/assets/status.png"> -->
                        </div>
                        <div class="paragraph-container">
                            <i class="fas fa-comments hero-image"></i>
                            <p class="hero-paragraph">
                            分からないことはコミュニティで質問し、
                            世界中のユーザー同士が助け合い学び合う場。
                            </p>
                        </div>
                        <div v-if="!user" class="test-button-wrapper">
                            <div class='test-button' @click='componentHandler()'>実力テストを始める</div>
                        </div>
                        <div v-if="user" class=registered-user>
                            <div class="hero-title">
                                <p>１日１回実力テストに挑戦できるよ！</p>
                            </div>
                            <div class="paragraph-container">
                                <div class="test-button-wrapper">
                                    <div class='test-button' @click='componentHandler()'>実力テストに挑戦する</div>
                                </div>
                                <div class="done-test">
                                    本日の実力テストは終了しました
                                </div>
                                <i class="fas fa-gamepad  hero-image"></i>
                            </div>
                            <div class="hero-title">
                                <p>運営からのお知らせ</p>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <p @click="unko" class='home-text'>にゃんこ😹日本語ワールド</p>
                <div :class="{'slide-in':slideIn,'slide-out':slideOut}">UNKO</div> -->
                <!-- unko{{$store.getters.getDjangouser.my_quiz[0].my_question}} -->
                <!-- {{$store.getters.gettersReply}}     -->
            </div>   
            <!-- <div class='home-conf' v-if='showCompo'> -->
                <TestConf 
                @close='showCompoHandler'
                v-if='showCompo'/>   
            <!-- </div> -->
            <transition name="notice">
                <NotLogin
                    v-if="tempUserTest&&showNotLogin"
                    @handleShowNotLogin="handleShowNotLogin"
                    />
            </transition>
        </div>
    </section>
</template>

<script>
import ConfettiExplosion from "vue-confetti-explosion";
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Chart from '@/components/account/Chart.vue'
// import Cookies from 'js-cookie'
//  import { uuid } from 'vue-uuid';
export default {
    name: 'Home',
    components: {
        TestConf,
        Notification,
        NotLogin,
        Chart,
        ConfettiExplosion
    },
    data(){
        return{
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
    mounted(){
        // this.test()
        // this.reload()
        // this.aaa()
        this.unko()
        const regionNames = new Intl.DisplayNames(['jp'], { type: 'region' });
        console.log('mounted',regionNames.of('JP'))
        this.scrollTop()
        this.setInitUserStatus()
        // console.log('mounted',this.$store.state.signup.djangoUser)
        // Cookies.set('unko','chinko')
        // this.$store.dispatch("getAnsweredQuestion")
        // this.$store.dispatch("commitHandleOnReplyAndOnAnswer")
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
        }
    },
    methods:{
        // randomBackground(){
        //     this.chartData.datasets.backgroundColor = this.backgroundColorList[Math.floor(Math.random() * this.backgroundColorList.length)];
        //     console.log('RANDOM',this.chartData.datasets.backgroundColor)
        //     this.showChart=true
        // },np,
        unko(){
            // let a = document.getElementById('unko')
            // let b = document.querySelector('#unko')
            // console.log('unko',a,b, typeof a)
            // this.$store.commit('setTempUserNull')
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
        // aaa(){
        //     let b = document.getElementsByClassName('hero-title')
        //     console.log('aaa',b,b.length)
        //     b[2].style.backgroundColor = 'red'
        // }
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

.home-section{
    width:100%;
    // height: 100vh;
    display: flex;
    // justify-content: center;
    align-items: center;
    flex-direction: column;
    .main-wrapper{
        .home-main-wrapper{
            display: flex;
            .home-hero{
                width: 100%;
                margin: 1rem;
                .hero-title{
                    border-top: 6px solid $base-color;
                    border-right: 1px solid $base-color;
                    border-left: 1px solid $base-color;
                    border-bottom: 1px solid $base-color;
                    box-shadow:  1px 1px 18px #888888;
                    // background: rgb(254, 254, 221);
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    padding-right: 0.1rem;
                    padding-left: 0.1rem;
                    margin-top: 1rem;margin-bottom: 1rem;
                    font-weight: bold;
                    font-size: 1.1rem;
                    color: white;

                }
                // img{
                //     width: 100px;
                // }
                
                .hero-paragraph-wrapper{
                    color: $back-white;
                    .paragraph-container{
                        display: flex;
                        align-items: center;
                        background: rgba($color: $back-white, $alpha: 0.1);
                        padding: 0.6rem;
                        margin-bottom: 0.5rem;
                        .hero-paragraph{
                            flex-basis: 50%;
                            font-weight: bold;
                        }
                        .hero-image{
                            flex-basis: 60%;
                            width: 10%;
                        }
                        .fa-comments{
                            font-size: 6rem;
                            color: rgba($color: #a6a6a6, $alpha: 0.6);
                        }
                        .test-button-wrapper{
                            flex-basis: 50%;
                        }
                        .fa-gamepad{
                            font-size: 6rem;
                            color: rgba($color: #a6a6a6, $alpha: 0.6);
                        }
                        .done-test{
                            border: solid $dull-red;
                            padding: 0.1rem 0.5rem 0.1rem 0.5rem;

                        }
                    }
                    .test-button-wrapper{
                        margin: 1rem;
                        .test-button{
                            display: inline-block;
                            border: solid $lite-gray;
                            border-radius: 50vh;
                            padding: 0.1rem 0.8rem 0.1rem 0.8rem;
                            color: $back-white;
                            transition: .5s;
                        }
                        .test-button:hover{
                            background: rgba($color: $back-white, $alpha: 0.1);
                        }
                    }
                    .test-button-wrapper{
                        margin: 1rem;
                        .test-button{
                            display: inline-block;
                            border: solid $lite-gray;
                            border-radius: 50vh;
                            padding: 0.1rem 0.8rem 0.1rem 0.8rem;
                            color: $back-white;
                            transition: .5s;
                        }
                        .test-button:hover{
                            background: rgba($color: $back-white, $alpha: 0.1);
                        }
                    }
                }
            }
        }
        .home-conf{
            // margin-bottom: 200px;
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
