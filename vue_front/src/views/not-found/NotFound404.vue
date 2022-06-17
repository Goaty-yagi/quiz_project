<template>
    <div class='not-wrapper'>
        <div v-if="$store.state.board.notifications.reply" :class="{'notification-blue':$store.state.board.notifications.reply}">
            <div class="notification-text">
                {{ scripts.errorNoteText }}
            </div>
        </div>
        <h1 class='main-title'> {{ scripts.mainTitle }}</h1>
        <p class='sub'> {{ scripts.sub }}</p>
        <p class='sub2'>{{ scripts.sub2 }}</p>
    <div class="error-footer">
        <button v-if="this.$store.getters.logger.exist" @click="createLog()" class='btn-litegray-black-gray-sq'>{{ scripts.report }}</button>
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
                errorNoteText:'報告しました。ご協力ありがとうございました。',
                mainTitle:'404　サーバーエラー',
                sub:'404 Server Error',
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
        createLog(){
            console.log('in not 404 got log')
            this.$store.dispatch('createLog',this.$store.getters.logger)
            this.showDelete()
        },
        showDelete(){
            console.log("clicked")
            this.$store.dispatch("handleNotifications", 'reply')
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