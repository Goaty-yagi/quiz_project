<template>
  <section class='home-section'>
    <!-- <Notification/> -->
    <!-- <p class='has-text-white'>{{ this.$store.state.id }}</p> -->
    <div class='wrapper'>
      <img class='is-image' src="@/assets/logo.png">
      <p class='home-text'>日本語クイズ</p>
      <!-- {{ $store.state.signup.user.uid }} -->
      <div  @click="onClick()">
          <button id='or-button' @click='showCompoHandler'>SRART</button>
      </div>
      <div>
      </div>
    </div>   
     <div class='home-conf' v-if='showCompo'>
        <TestConf @close='showCompoHandler' />   
      </div>   
    
  </section>

</template>

<script>
import TestConf from '@/components/initial/TestConf.vue'
import Notification from '@/components/initial/Notification.vue'
export default {
  name: 'Home',
  components: {
    TestConf,
    Notification
  },
  data(){
    return{
      // status: 2,
      field:'並び替え',
      // num:3,
      showCompo: false,
      item:{status: 2,num:5,test:true},
      // a:window.innerWidth
    }
  },
  methods:{
    unko(){
      return `/quiz/${this.status}`
    },
    onClick(){
      this.$store.commit('getURLs',this.item)
    },
    showCompoHandler(){
      this.showCompo = !this.showCompo
    }   
  }
}
</script>
<style scoped lang="scss">
@import "style/_variables.scss";
@media(max-width: 1024px){

  }
  .home-section{
    width:100%;
    // height:100%;
  }.wrapper{
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
    width:100%;
    height:100%;
    // bottom:10%;
  }
  .is-image{
    width: 8rem;
    height: auto;
  }
  .home-text{
    font-size:2rem;
    color:white;
    font-weight: bold;
  }
  #or-button{
    border-radius: 100vh;
    border: 2px solid $base-color;
    margin:1rem;
    padding:0.4rem;
    background: transparent;
    color: $base-color;
    font-weight:bold;
    font-size: 1rem;
    transition:0.5s;
    }
    #or-button:hover{
      background: $base-color;
      color:white;
    }
    .home-conf{
      position:absolute;
      left:0;
    }
</style>
