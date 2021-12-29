<template>
  <div class="header-wrapper">
    <template v-if='authIsReady' >
      <nav class="navbar is-transparent">
          <div class="navbar-brand">
            <a class="navbar-item is-paddingless">
                <router-link @click="storeReset" to="/" >
                    <img src="@/assets/logo.png">
                </router-link>
            </a>
            <!-- mobile menu -->
            <!-- <a class="navbar-burger" @click="showMobileMenu = !showMobileMenu">
              <button v-if='showMobileMenu==true' class="delete mt-3 is-large"></button>
                <div v-if='showMobileMenu==false'>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
            </a> -->
          </div>      
          <div class='navbar-menu' :class="{'is-active': showMobileMenu }">
            <div class="navbar-end is-expanded" @click="showMobileMenu =false">
                <router-link to="/" @click="storeReset" class="navbar-item has-text-white"><i class="fas fa-home" ></i>Home</router-link>
                <router-link to="/quiz" class="navbar-item is-spaced has-text-white"><i class="fas fa-lightbulb"></i>Quiz</router-link>
                <router-link to="/test" class="navbar-item has-text-white"><i class="fab fa-aws"></i>Test</router-link>
                <div v-if='!user'>
                  <router-link to="/login" class="navbar-item has-text-white"><i class="fas fa-sign-in-alt"></i>Login</router-link>
                  <router-link to="/signup" class="navbar-item has-text-white"><i class="fas fa-user-plus"></i>Signup</router-link>
                </div>
                <div v-if='user'>
                  <router-link v-if='emailVerified' to="/account" class="navbar-item has-text-white"><i class="fas fa-robot"></i>account</router-link>
                  <div class="navbar-item has-text-white" @click='logout'><i class="fas fa-sign-out-alt"></i>Logout</div>
                </div>
            </div>
          </div>
      </nav>
    </template>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
// import {router} from "../main.js"
export default {
  setup(){
    const store = useStore()
    return{
      user: computed(() => store.state.signup.user),
      emailVerified: computed(() => store.state.signup.emailVerified),
      authIsReady: computed(() => store.state.signup.authIsReady)
    }
  },
    data(){
        return{
            showMobileMenu: false,
            // user: '',
            // authIsReady:'',
        }
    },
    // computed:{
    //   user: function(){this.$store.state.signup.user},
    //   authIsReady: function(){this.$store.state.signup.authIsReady}
    // //   authIsReady(() => this.$store.state.signup.authIsReady)
    // },
    mounted(){
      // console.log(this.user,this.authIsReady)
      // this.user = this.$store.state.signup.user,
      // this.authIsReady = this.$store.state.signup.authIsReady
      // console.log('user',this.user,'auth',this.authIsReady)
    },
    beforeMount(){
      
    },
    methods:{
    storeReset(){
          this.$store.commit('reset')
    },
    async logout(){
      await this.$store.dispatch('logout')
      // this.$router.push('/')
      // this.$router.go({path: '/', force: true})
    }
  }
}
</script>

<style scoped lang=scss>
  .header-wrapper{
    width:100vw;
    /* height:100Vh; */
    position:relative;

  }
  .navbar {
    &.is-transparent {
      background-color: transparent;
      background-image: none;
      }
    }
  .navbar-end{
    color:white;
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
    background:rgba(255, 255, 255, 0.3);
  }
  .nav-mobile-item:hover{
    background:rgba(255, 255, 255, 0.3);
  }

</style>