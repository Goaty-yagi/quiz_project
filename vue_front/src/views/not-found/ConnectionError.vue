<template>
    <div class='not-wrapper'>
        <h1 class='main-title'> {{ scripts.mainTitle }}</h1>
        <p class='sub'> {{ scripts.sub }}</p>
        <p class='sub2'>{{ scripts.sub2 }}</p>
    <div class="error-footer">
        <button class='btn-litegray-black-gray-sq'>{{ scripts.report }}</button>
        <router-link :to="{name:'Home'}" @click='closeConf' class="home"><i class="fas fa-home"></i>{{ scripts.return }}</router-link>
    </div>
</div>

</template>

<script>
import {router} from "/src/main.js"

export default {
    data(){
        return{
            scripts: {
            mainTitle:'500　サーバーエラー',
            sub:'サーバーが混み合っています。しばらく経ってからご利用ください。',
            sub2:'sorry! somethign wired happened',
            report:'エラー報告をする',
            return:'Return to home'
          }

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

<style scoped lang="scss">
@import "style/_variables.scss";
  .not-wrapper{
    /* background: linear-gradient(#5B759F,#1C254C); */
    width: 100%;
    height:100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    .main-title{
        font-size: 2rem;
        font-weight: bold;
        color: $base-white;
    }
    .sub{
        font-weight: bold;
        color: $base-white;
    }
    .sub2{
        font-weight: bold;
        color: $dull-red;
    }
    .error-footer{
        margin-top: 1.5rem;
        display: flex;
        flex-direction: column;
        .btn-litegray-black-gray-sq{
            margin-bottom: 2rem;
        }
        .home{
            border: solid $lite-gray;
            padding: 0 0.6rem;
            transition: .5s;
        }
        .home:hover{
            color: white;
        }
    }
  }
</style>