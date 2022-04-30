<template>
    <div class="header-wrapper">
        <template v-if='authIsReady' >
            <nav class="navbar-container">
                <div class="nav-brand">
                    <a class="nav-brand-wrapper">
                        <router-link @click="storeReset" to="/" >
                            <img src="@/assets/logo.png">
                        </router-link>
                    </a>
                </div>
                <div class="handle-show">
                    <div class='nav-menu-flex'>
                        <div class="nav-menu" @click="showMobileMenu =false">
                            <router-link :to="{ name: 'Home'}" @click="storeReset" class="nav-item"><i class="fas fa-home" ></i>Home</router-link>
                            <router-link :to="{ name: 'QuizHome'}" class="nav-item "><i class="fas fa-lightbulb"></i>Quiz</router-link>
                            <router-link :to="{ name: 'Community'}"  class="nav-item"><i class="far fa-comments fas"></i>Community</router-link>
                            <router-link v-if='!user' :to="{ name: 'Login'}" class="nav-item"><i class="fas fa-sign-in-alt"></i>Login</router-link>
                            <router-link v-if='!user' :to="{ name: 'Signup'}" class="nav-item signup"><i class="fas fa-user-plus"></i>Signup</router-link>
                            <div v-if='user' @click='getAccount($store.state.signup.user.uid)' class="nav-item"><i class="fas fa-robot"></i>Account</div>
                            <div v-if='user' class="nav-item last" @click='logout'><i class="fas fa-sign-out-alt"></i>Logout</div>
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
    // watch:{
    //     width:function(v) {
    //         if(this.width > 427){
    //             this.handleWidthAndHeight = true
    //             this.showBrand = false
    //             console.log(this.handleWidthAndHeight)
    //             if(this.width > 630){
    //             this.showBrand = true
    //             }
    //         }else{
    //             this.handleWidthAndHeight = false
    //             this.showBrand = true
    //         }
    //     }
    // },
    mounted(){
    //     this.width = window.innerWidth
    //     this.height = window.innerHeight;
    //     window.addEventListener('resize', this.handleResize)
    //   console.log('mounted-header',this.width,this.height)
    },
    beforeUnmount(){
        // window.removeEventListener('resize', this.handleResize)      
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
    // handleResize(){
    //     this.width = window.innerWidth;
    //     this.height = window.innerHeight;
    //     console.log('width:',this.width,'height:',this.height)
    // }
  }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.header-wrapper{
    width: 100vh; 
    height: 100px;
    margin-top: 1rem;
    // border-bottom: solid $dark-blue;
    .navbar-container{
        position: relative;
        display: flex;
        justify-content: flex-end;
        width: 100%;
        // height: 100%;
        img{
            position: absolute;
            width: 3rem;
            height: 3rem;
            left:0;
            top:0;
        }
        .nav-menu-flex{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding:1rem;
            width: 100%;
            // height: 100%;
            .nav-menu{
                margin-top: 1.5rem;
                margin-right: 1rem;
                display: flex;
                .fas{
                    margin-right: 0.5rem;
                }
                .nav-item{
                    color:white;
                    // flex:1;
                    border-right: 0.2rem solid $base-color;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    transition: 0.5s;
                }
                .signup{
                    border: solid $base-white;
                    color: rgb(240, 205, 4);
                    margin-left: 0.5rem;
                    padding-right: 1rem;
                    padding-left: 0.5rem;
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    
                }
                .last{
                    border-right: none;
                }
                .nav-item:hover{
                    color:gray;
                    background: $base-white;
                    // border: solid gray;
                    box-sizing: inherit;
                }
                .signup:hover{
                    border: solid $dark-blue;
                    color: $dark-blue;
                    // background: $base-lite-3;
                }
                .auth{
                    display: flex;
                    flex-basis: 40%;
                    margin-left: 0.5rem;
                    margin-right: 0.5rem;
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
@media(min-width: 630px)and(max-width: 660px){
    .nav-brand{
        display: none;
    }
}
@media(max-width: 629px){
    .handle-show{
        display: none;
    }
    // .header-wrapper{
    //     display: none;
    // }
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
  
// @media(max-width:560px){
//     .nav-menu-flex{
//         display: flex;
//         justify-content: flex-end;
//         align-items: center;
//         // padding:1rem;
//         width: 100%;
//         // height: 100%;
//         .nav-menu{
//             margin-top: 1.5rem;
//             margin-right: 1rem;
//             .fas{
//                 margin-right: 0.5rem;
//             }
//             .nav-item{
//                 color:red;
//                 flex:1;
//                 border-right: 0.2rem solid red;
//                 padding-right: 1rem;
//                 padding-left: 1rem;
//                 padding-top: 0.5rem;
//                 padding-bottom: 0.5rem;
//                 transition: 0.5s;
//             }
//             .signup{
//                 border: solid $base-white;
//                 color: rgb(226, 225, 221);
//                 margin-left: 0.5rem;
//                 padding-right: 1rem;
//                 padding-left: 0.5rem;
//                 padding-top: 0.5rem;
//                 padding-bottom: 0.5rem;
                
//             }
//         }
//     }
// }
</style>