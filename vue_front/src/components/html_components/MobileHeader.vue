<template>
    <div class='mobile-header-wrapper'>
        <div class="mobilemenu-wrapper">
            <router-link to="/" @click="storeReset" class="nav-mobile-item"><i class="fas fa-home" ></i><p>Home</p></router-link>
            <div @click='getAccount($store.state.signup.user.uid)' class="nav-mobile-item"><i class="fas fa-robot"></i><p>Account</p></div>
            <router-link to="/board"  class="nav-mobile-item"><i class="far fa-comments"></i><p>Community</p></router-link>
            <router-link to="quiz-home"  class="nav-mobile-item"><i class="far fa-lightbulb"></i><p>Quiz</p></router-link>
            <router-link to="/"  class="nav-mobile-item"><i class="fas fa-cog"></i><p>その他</p></router-link>
        </div>
    </div>
</template>

<script>
import {router} from "@/main.js"
export default {
    methods:{
    storeReset(){
          this.$store.commit('reset')
        },
    getAccount(id){
            console.log(id)
            // this.$store.commit('getSlug',slug)
            router.push(`/account/${id}` )
        }
    }
}
</script>

<style  lang='scss' scoped>
.mobilemenu-wrapper{
    
    position:fixed;
    width:100%;
    display: flex;
    justify-content: center;
    bottom:0;
  }
.nav-mobile-item{
    font-size:0.8rem;
    color: white;
    border:0.1rem solid white;
    position:flex;
    flex-direction: column;
    flex-basis:20%;
    padding-left:0.1rem;
    padding-right:0.1rem;
    background: linear-gradient(rgba(91, 117, 159, 0.9),rgba(28, 37, 76, 0.9));
    transition:0.5s;
  }
  .nav-mobile-item:hover{
    background: linear-gradient(rgba(0,0,0,0),rgba(0,0,0,1));
  }
</style>