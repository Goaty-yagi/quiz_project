<template>
    <div class="account-wrapper" v-if='this.$store.state.signup.emailVerified'>
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class="content-wrapper">
                <h1 class='title-white'>アカウント</h1>
                <div class="cropper-wrapper">
                    <img v-bind:src="userData.thumbnail"/>
                    <p @click='handleShowThumbnail'>画像を<br>変更する</p>
                </div>
                <div class="notification-container">
                    <div class="alert-position-container">
                        <div class="notification-text">
                            お知らせ
                        </div>
                        <div class="notification-alert">
                            Notifications
                        </div>
                    </div>
                </div>
                <div class="user-info-wrapper">
                    <div class="user-name user-container">
                        <div class="left-side">
                            User<br>Name
                        </div>
                        <div class="right-side">
                            {{ userData.name}}
                        </div>
                    </div>
                    <!-- <div class="user-id user-container">
                        <div class="left-side">
                            User<br>ID
                        </div>
                        <div class="right-side">
                            <p>{{ userData.UID }}</p>
                        </div>             
                    </div> -->
                    <div class="current-level user-container">
                        <div class="left-side">
                            Grade
                        </div>
                        <div class="right-side grade-right-side">
                            <div classs="current-level-text">
                                {{ userData.grade}}
                            </div>
                            <div class="max-level">
                                最大レベル　初級Lv,2
                            </div>
                        </div>       
                    </div>
                    <div class="next-level">
                        次は初級レベル７だよ！
                    </div>
                </div>
                <div class="status-wrapper">
                    <chart></chart>
                </div>
                <div class="comunity-account">
                    コミュニティアカウントへ移動
                </div>
            </div>
        </div>
    
      <Sent v-show='showSent'/>
      <Thumbnail v-if="showThumbnail"/>
      <!-- <div v-if='emailVerified==false'>
        <div class='main-notification-wrapper'>
            <div class='main-notice-wrapper'>
                <img class='main-image' src="@/assets/logo.png">
                <p class='main-text1'>メール承認が完了していません。</p>
                <p class='main-text1'>メール承認を完了してください。</p>
                <button @click='resent' onclick="disabled = true" class='main-text1'>承認メールを送る。</button>                      
            </div>
        </div>
      </div> -->
    </div>
</template>

<script>
import axios from 'axios'
import 'cropperjs/dist/cropper.css';
import  Thumbnail from '@/components/account/Thumbnail.vue'
import  Chart from '@/components/account/Chart.vue'
import Sent from '@/components/signin/Sent.vue'
import { computed } from 'vue'
import { useStore } from 'vuex'
export default{
  setup(){
    const store = useStore()
    return{
      user: computed(() => store.state.signup.user),
      email: computed(() => store.state.signup.email),
      password: computed(() => store.state.signup.password),
      emailVerified: computed(() => store.state.signup.emailVerified),
    }
  },
  data(){
    return{
      showSent:false,
      error:'',
      userData:'',
      showThumbnail:false
    }
  },
  components: {
    Sent,
    Thumbnail,
    Chart
  },
  mounted(){
    console.log('account mounted',this.$route.params.uid)
    this.getUserData()
  },
  methods:{
      async getUserData(){
          await axios
            .get(`/api/user/${this.$route.params.uid}`)
            .then(response => {
                this.userData = response.data
                console.log('inGet', this.userData)
                })
            .catch(error => {
                console.log(error)
                })
            },
    async resent(){
          try{
              await this.$store.dispatch('sendEmailVerify')
              this.handleShowSent()
              console.log('showsent:',this.showSent)
          }catch(err){
            this.error = err
            console.log(this.error)
          }
    },
    handleShowSent(){
      this.showSent = true
    },
    handleShowThumbnail(){
        this.showThumbnail = true
    }        
  }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
// @import 'cropperjs/dist/cropper.css';
.account-wrapper{
    display: flex;
    justify-content: center;
    .main-wrapper{
        .content-wrapper{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            .cropper-wrapper{
                display: flex;
                position:relative;
                justify-content: center;
                margin-top: 0.5rem;
                width: 12rem;
                img{
                    border-radius: 50%; 
                    width:  5rem;   
                    height: 5rem;       
                }
                p{
                    position: absolute;
                    right: 0;
                    color: white;
                    font-size: 0.8rem;
                }
            }
            .notification-container{
                position: relative;
                display: flex;
                justify-content: center;
                width: 100%;
                .alert-position-container{
                    width:70%;
                    border: solid $base-color;
                    min-height: 3rem;
                    background: $back-white;
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    .notification-alert{
                    position: absolute;
                    right: 0;
                    top: 0;
                    margin-right: 0.9rem;
                    padding-right: 0.5rem;
                    padding-left: 0.5rem;
                    color: $back-white;
                    font-weight: bold;
                    border: solid $dark-blue;
                    border-radius: 50vh;
                    background:rgba(252, 75, 175, 0.961); 
                    }
                }
            }
            .user-info-wrapper{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                .user-container{
                    display: flex;
                    border: 0.1rem solid $dark-blue;
                    background: $back-white;
                    border-radius: 0.5rem;
                    width: 80%;
                    min-height: 3rem;
                    margin-bottom: 1rem;
                    overflow: hidden;
                    .left-side{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 30%;
                        background: $base-color;
                        border-right: 0.1rem solid $dark-blue;
                        line-height: 0.8rem;
                        color: white;
                        font-weight: bold;
                        font-size: 1.1rem;                      
                    }
                    .right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 70%;
                        width:70%;
                        font-size: 1.2rem;
                        font-weight: bold;
                        // overflow-wrap: break-all;                        
                    }
                    .grade-right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: flex-end;
                        .current-level-text{
                            display: flex;
                            justify-content: center;
                            align-items: flex-end;
                        }
                        .max-level{
                            position: absolute;
                            color: rgba(252, 75, 175, 0.961); 
                            right: 0;
                            top: 0;
                            font-size: 0.7rem;
                            margin-right: 0.2rem;
                        }
                    }
                }
                .next-level{
                    color: white;
                }
            }
            .status-wrapper{
                
            }
            .comunity-account{
                color: white;
            }
        }
    }
}


    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1rem;
        font-weight: bold;
        margin:2rem;
    }
    img {
        border-radius: 50%; 
        width:  5rem;   
        height: 5rem;       
    }
    .cropper-view-box,
    .cropper-face {
      border-radius: 50%;
      cursor: grab;
      outline: initial;
    }
    .cropper-face:active {
      cursor: grabbing;
    }
</style>