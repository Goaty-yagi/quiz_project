<template>
<div class='not-wrapper'>
  <h1 class='title is-1 mt-4'> 404　サーバーエラー</h1>
  <h1 class='subtitle is-3'> 404 Server Error</h1>
  <div>
    <button>エラー報告をする</button>
    <router-link :to="{name:'Home'}" @click='closeConf'  class="is-centered mt-6"><i class="fas fa-home"></i>Return to Home</router-link>
  </div>
</div>

</template>

<script>
import {router} from "/src/main.js"

export default {
    data(){
        return{

        }
    },
    mounted(){
        console.log('mounted',this.$store.getters.logger)
        this.checkBeingException()
        setTimeout(this.reload, 3000)  
    },
    methods:{
        closeConf(){
            this.$store.commit('reset')
        },
        checkBeingException(){
            this.$store.commit('checkBeingException')
            this.$store.commit('reloadForExceptionTrue')
        },
        reload(){
            console.log('reload_enter',this.$store.state.signup.beingException)
            if(this.$store.state.signup.reloadForException){
                console.log('reload_desu')
                this.$store.commit('reloadForExceptionFalse')
                // this.goHome()
                console.log('start-reload')
                window.location.reload();
            }
        },
        goHome(){
            router.push('/' )
        }
    }
}
</script>

<style scoped>
  .not-wrapper{
    /* background: linear-gradient(#5B759F,#1C254C); */
    width: 100vw;
    height:100vh;
    padding-top:25vh;
    padding-bottom: 25vh;
  }
</style>