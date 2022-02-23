<template>
  <div class="account-wrapper">
    <div v-if='emailVerified==false'>
        <div class='main-notification-wrapper'>
            <div class='main-notice-wrapper'>
                <img class='main-image' src="@/assets/logo.png">
                <p class='main-text1'>メール承認が完了していません。</p>
                <p class='main-text1'>メール承認を完了してください。</p>
                <button @click='resent' onclick="disabled = true" class='main-text1'>承認メールを送る。</button>                      
                <!-- <button  @click='addStep' class='button' id='color-button'><p>次へ</p></button> -->
            </div>
        </div>
      </div>
      <Sent v-show='showSent'/>
      <Thumbnail v-if="showThumbnail"/>
      <div class='account'  v-if='this.$store.state.signup.emailVerified'>
        <p>accountdayo</p>
        <div class="cropper-wrapper">
            <img v-bind:src="userData.thumbnail"/>
            <p @click='handleShowThumbnail'>画像を変更する</p>
        </div>
        <p> Username {{ userData.name}}</p>
        <p> grade {{ userData.grade}}</p>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import 'cropperjs/dist/cropper.css';
import  Thumbnail from '@/components/account/Thumbnail.vue'
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
    Thumbnail
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
.main-notification-wrapper{
        top:0;
        position: fixed;
        background:rgba(0,0,0,0.5);
        width:100vw;
        height:100vh;
        flex-direction: column;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .main-notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        position:relative;
        padding-top:1.5rem;
        height:30rem;
        width: 20rem;
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