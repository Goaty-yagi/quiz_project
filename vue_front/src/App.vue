<template>
  <div id="wrapper">
    <div class="wrapper2">
      <div class="main-header">
       <Header/>
      </div>
        <section class="main-section">
            <router-view
            id='router'/>
        </section>
      <Footer
      v-if='!this.$router.path==quizurl'
      />
    </div>
  </div>
</template>

<script>
import Footer from '@/components/html_components/Footer.vue'
import Header from '@/components/html_components/Header.vue'
export default{
  data(){
    return{
      quizurl:'/quiz/2'
    }
  },
  components: {
    Footer,
    Header
  },
  methods:{
    storeReset(){
          this.$store.commit('reset')
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
  background: linear-gradient(#5B759F,#1C254C);
  width: 100vw;
  height:100vh;  
}
 .wrapper2{
   position:relative;
}
.main-header{
  position:absolute;
}
.main-section{
  // background: linear-gradient(#5B759F,#1C254C);
  width: 100vw;
  height:90vh;

  // border:solid orange;
  // width: 80%;
  // margin: 0 auto;
  // max-width: 90%
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
  #register-button{
    background: none;
    color:black;
    border: 0.1rem solid  $base-color;
    transition:0.3s;
  }
  #register-button:hover{
    background: $base-color;
    color:white;
    font-weight: bold;
    border: 0.1rem solid  darken($base-color,10%);
  }
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
@media(min-width: 1024px){
  .wrapper{
    position:relative
  }.main-section{
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
