<template>
    <section class='home-section'>
        <div class='wrapper'>
            <img @click="unko" class='is-image' src="@/assets/logo.png">
            <p @click="unko" class='home-text'>日本語クイズ</p>
            <!-- unko{{$store.getters.getDjangouser.quiz_taker}} -->
            <!-- {{$store.getters.gettersReply}}     -->
            <div v-if="!user">
                <button id='or-button' @click='componentHandler()'>SRART</button>
            </div>
        </div>   
        <div class='home-conf' v-if='showCompo'>
            <TestConf @close='showCompoHandler' />   
        </div>
        <transition name="notice">
            <NotLogin
                v-if="tempUserTest&&showNotLogin"
                @handleShowNotLogin="handleShowNotLogin"
                />
        </transition>
    </section>
</template>

<script>
import axios from 'axios'
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
import NotLogin from '@/components/login/NotLogin.vue'
// import Cookies from 'js-cookie'
//  import { uuid } from 'vue-uuid';
export default {
    name: 'Home',
    components: {
        TestConf,
        Notification,
        NotLogin,
    },
    data(){
        return{
            field:'並び替え',
            showCompo: false,
            showNotLogin: false,
            item:{status: 1,num:5,test:true},
            test1:""
        }
    },
    mounted(){
        // this.test()
        this.scrollTop()
        this.setInitUserStatus()
        console.log('mounted',this.$store.state.signup.djangoUser)
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
                if(this.$store.getters.getTempUser){
                    this.$store.commit('setQuizTakerID',this.quizTaker.id)
                    this.$store.commit('setQuizID',this.$store.getters.getTempUser.grade)
                    for(let i of this.$store.getters.getTempUser.statusList){
                        await this.$store.dispatch('userStatusPost',i)
                    }
                }
                this.$store.commit('setTempUserReset')
            }
        },
    }
}
</script>
<style scoped lang="scss">
@import "style/_variables.scss";
@media(max-width: 1024px){

  }
  .home-section{
    width:100%;
    height: 100vh;
    // height:100%;
  }.wrapper{
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
    width:100%;
    // height:100%;
    // bottom:10%;
  }
  .is-image{
    width: 8rem;
    height: auto;
  }
  .home-text{
    font-size:2rem;
    color:white;
    font-weight: bold;
  }
  #or-button{
    border-radius: 100vh;
    border: 2px solid $base-color;
    margin:1rem;
    padding:0.4rem;
    background: transparent;
    color: $base-color;
    font-weight:bold;
    font-size: 1rem;
    transition:0.5s;
    }
    #or-button:hover{
      background: $base-color;
      color:white;
    }
    .home-conf{
      position:absolute;
      left:0;
    }
</style>
