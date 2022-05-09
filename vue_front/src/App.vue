<template>
    <div id="wrapper">
        <div class="wrapper2">
            <Header
            id="header"/>
            <section class="main-section" :class="{'scroll-fixed':$store.state.isLoading}">
                <router-view
                id='router'/>
                <Footer
                id="footer"
                v-if="!$store.state.isLoading&&!$store.state.quiz.onQuiz"/>
            </section>
            <div class='mobile-header'
            v-if="!$store.state.quiz.onQuiz">
                <MobileHeader/>
            </div>
        </div>
    </div>
</template>

<script>
import Footer from '@/components/html_components/Footer.vue'
import Header from '@/components/html_components/Header.vue'
import MobileHeader from '@/components/html_components/MobileHeader.vue'
import Sent from '@/components/signin/Sent.vue'
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
export default{
  setup(){
    const store = useStore()
    // const m = ref(window.matchMedia("(max-width: 896px)"));
    // const mediaQuery = () =>  window.matchMedia("(max-width: 896px)")
    return{
      user: computed(() => store.state.signup.user),
      djangoUser: computed(() => store.state.signup.djangoUser),
      email: computed(() => store.state.signup.email),
      password: computed(() => store.state.signup.password),
      emailVerified: computed(() => store.state.signup.emailVerified),
      // mobileChecker:computed(() => window.innerWidth)
    }
  },
  data(){
    return{
      quizurl:'/quiz/2',
      showSent:false
    }
  },
  components: {
    Footer,
    Sent,
    Header,
    MobileHeader
  },
  methods:{
    storeReset(){
          this.$store.commit('reset')
    },
  async resent(){
        // try{
            await this.$store.dispatch('sendEmailVerify')
            this.handleShowSent()
    },
    handleShowSent(){
      this.showsent = true
    }
  }
}
</script>


<style lang="scss">
@import '../node_modules/bulma';
@import "style/_variables.scss";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#wrapper{
  // background: linear-gradient(#5B759F,#1C254C);
  // background: red;
  // height: 100%;
  // position: relative;
  // min-height: 100%;
}
#wrapper:after{
  background: linear-gradient(#5B759F,#1C254C);
  position: fixed;/*固定配置*/
  top: 0; left: 0;/*左上に固定*/
  width: 100%; height: 100%;/*画面全体を覆う*/
  content: "";
  z-index: -1;/*背景にするため*/
}
 .wrapper2{
   position:absolute;

}
#header{
    position: fixed;
    top: 0;
    left: 0;
    // height: 100px;
    // z-index: 100;
}
#router{
  min-height: 80vh;
//   padding-bottom: 5rem;
}
#footer{
    // z-index: -1;
}
.main-header{
  position:relative;
  bottom:0;
}
.main-section{
  // background: linear-gradient(#5B759F,#1C254C);
  margin-top: 60px;
  width: 100vw;
  min-height:100vh;
}

// .router{
//   border:solid green;
//   width: 60%;
//   margin: 0 auto;
//   max-width: 50%
// }
.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid rgb(214, 9, 9);
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}    
  // here intend to be pablic css
  
  #color-button{
    background: linear-gradient($base-lite,$base-color);
    color:white;
    border: 0.1rem solid  $base-color;
    transition:0.3s;
  }
  #color-button:hover{
    background: $base-color;
    color:white;
    font-weight: bold;
    border: 0.1rem solid  darken($base-color,10%);
  }
  // form button
  .fbottun{
        margin-top:1rem;
        border-radius: 100vh;
        border: 2px solid $base-color;
        margin:1rem;
        padding-top:0.3rem;
        padding-bottom:0.3rem;
        padding-left:1rem;
        padding-right:1rem;        
        background: transparent;
        color: white;
        font-size: 1rem;
        transition:0.5s;
    }
    .fbottun.button-hover{
        background: $base-color;
        color:white;
        font-weight:bold;
        border: 2px solid darken($base-color,10%);
    }
    .fbottun.button-hover:hover{
        background: transparent;
        color:$base-color;
    }
    // formerror
    .error-form{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.2rem solid red;
        border-radius: 1rem;
        background:rgb(252, 252, 252);
        width: 100%;
        padding-top:0.5rem;
        padding-bottom:0.5rem;
        transition:0.5s;
        align-self: center;
      }
      .form-error{
        border: solid red;
      }
@media(min-width: 630px){
  .mobile-header{
    display:none;
  }
  .wrapper{
    position:relative
  }.main-section{
    margin-top: 120px;
    // background: linear-gradient(#5B759F,#1C254C);
    // width: 100vw;
    // height:100vh;
    // box-sizing: border-box;
  }
  // .wrapper2{
  //   border: solid white;
  //   height: 90%;
  //   width: 80%;
  //   position: absolute;
  // }
  // .main-section{
  //   width: 50%;
  //   height: 70%;
  //   border: solid yellow;
  //   position: absolute;
  // }
}
// mailvalidation notice
// .main-notification-wrapper{
//         top:0;
//         position: fixed;
//         background:rgba(0,0,0,0.5);
//         width:100vw;
//         height:100vh;
//         flex-direction: column;
//         display: flex;
//         justify-content: center;
//         align-items: center;
//     }
//     .main-notice-wrapper{
//         border: solid $base-color;
//         border-radius: 2vh;
//         background:$back-white;
//         text-align: center;       
//         position:relative;
//         padding-top:1.5rem;
//         height:30rem;
//         width: 20rem;
//         }
//     .main-image{
//         width:15%;
//         height:auto;
//         margin-left: auto;
//         margin-right: auto;
//     }
//     .main-text1{
//         font-size:1rem;
//         font-weight: bold;
//         margin:2rem;
//     }

    
// animation for name'notice'
.notice-enter-from{
    opacity: 0;
  }
  .notice-enter-to{
    opacity: 1 ;
  }
  .notice-enter-active, .notice-leave-active {
  transition: opacity .5s;
  }
</style>
