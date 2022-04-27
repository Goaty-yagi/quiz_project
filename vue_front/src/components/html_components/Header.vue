<template>
    <div class="header-wrapper">
        <template v-if='authIsReady' >
            <nav class="navbar-container">
                <div v-if="showBrand" class="nav-brand">
                    <a class="nav-brand-wrapper">
                        <router-link @click="storeReset" to="/" >
                            <img src="@/assets/logo.png">
                        </router-link>
                    </a>
                </div>      
                <div v-if="handleWidthAndHeight" class='nav-menu-flex' :class="{'is-active': showMobileMenu }">
                    <div class="nav-menu" @click="showMobileMenu =false">
                        <div class="space"></div>
                        <router-link :to="{ name: 'Home'}" @click="storeReset" class="nav-item"><i class="fas fa-home" ></i><br>Home</router-link>
                        <router-link :to="{ name: 'QuizHome'}" class="nav-item "><i class="fas fa-lightbulb"></i><br>Quiz</router-link>
                        <router-link :to="{ name: 'Community'}"  class="nav-item"><i class="far fa-comments"></i>Community</router-link>
                        <!-- <router-link to="/test" class="navbar-item has-text-white"><i class="fab fa-aws"></i>Test</router-link> -->
                        <div class="auth" v-if='!user'>
                            <router-link :to="{ name: 'Login'}" class="nav-item"><i class="fas fa-sign-in-alt"></i>Login</router-link>
                            <router-link :to="{ name: 'Signup'}" class="nav-item"><i class="fas fa-user-plus"></i>Signup</router-link>
                        </div>
                        <div class="auth" v-if='user'>
                            <div  @click='getAccount($store.state.signup.user.uid)' class="nav-auth-item"><i class="fas fa-robot"></i>Account</div>
                            <div class="nav-auth-item" @click='logout'><i class="fas fa-sign-out-alt"></i>Logout</div>
                        </div>
                    </div>
                </div>
            </nav>
        </template>
    </div>
</template>

<script>
import {router} from "@/main.js"
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
            handleWidthAndHeight:false,
            showBrand:true,
            width:'',
            Height:'',
            // user: '',
            // authIsReady:'',
        }
    },
    computed:{
    //   user: function(){this.$store.state.signup.user},
    //   authIsReady: function(){this.$store.state.signup.authIsReady}
    // //   authIsReady(() => this.$store.state.signup.authIsReady)
    },
    watch:{
        width:function(v) {
            if(this.width > 427){
                this.handleWidthAndHeight = true
                this.showBrand = false
                console.log(this.handleWidthAndHeight)
                if(this.width > 800){
                this.showBrand = true
                }
            }else{
                this.handleWidthAndHeight = false
                this.showBrand = true
            }
        }
    },
    mounted(){
        this.width = window.innerWidth
        this.height = window.innerHeight;
        window.addEventListener('resize', this.handleResize)
      console.log('mounted-header',this.width,this.height)
    },
    beforeUnmount(){
        window.removeEventListener('resize', this.handleResize)      
    },
    methods:{
    storeReset(){
          this.$store.commit('reset')
    },
    getAccount(id){
        router.push(`/account/${id}` )
    },
    async logout(){
      await this.$store.dispatch('logout')
      // this.$router.push('/')
      // this.$router.go({path: '/', force: true})
    },
    handleResize(){
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        console.log('width:',this.width,'height:',this.height)
    }
  }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.header-wrapper{
    position: sticky;
    // top: 0;
    width: 100vh; 
    height: 100px;
    .navbar-container{
        position: relative;
        // display: flex;
        width: 100%;
        height: 100%;
        img{
            position: absolute;
            width: 3rem;
            height: 3rem;
            left:0;
            top:0;
        }
        .nav-menu-flex{
            display: flex;
            justify-content: center;
            align-items: center;
            // padding:1rem;
            width: 100%;
            // height: 100%;
            .nav-menu{
                display: flex;
                align-items: center;
                padding-top: 1rem;
                // .space{
                //     flex-basis: 50%;
                // }
                .nav-item{
                    color:white;
                    flex-basis: 20%;
                    margin-left: 0.5rem;
                    margin-right: 0.5rem;
                    padding: 0.3rem;
                    transition: 0.5s;
                    border: solid rgba(0, 0, 0, 0);
                }
                .nav-item:hover{
                    color:gray;
                    border: solid gray;
                    box-sizing: inherit;
                }
                .auth{
                    display: flex;
                    flex-basis: 40%;
                    .nav-auth-item{
                        color:white;
                        flex-basis: 50%;
                        margin-left: 0.5rem;
                        margin-right: 0.5rem;
                        padding: 0.3rem;
                        transition: 0.5s;
                        cursor : pointer;
                        border: solid rgba(0, 0, 0, 0);
                    }
                    .nav-auth-item:hover{
                        color:gray;
                        border: solid gray;
                        box-sizing: inherit;
                    }
                }
            }
        }
    }    
}
@media(max-width: 428px){
    .header-wrapper{
        height: 50px;
    }

}

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