<template>
<div class='not-wrapper'>
  <div class="main-wrapper">
      <h1 class='title is-1 mt-4'> お探しのページは見つかりませんでした。</h1>
      <h1 class='subtitle is-3'> Page not found</h1>
  </div>
  <div class="router">
    <router-link :to="{name:'Home'}" @click='closeConf' class="return"><i class="fas fa-home"></i>Return to Home</router-link>
  </div>
</div>

</template>

<script>
export default {
  data(){
    return{

    }
  },
  methods:{
    closeConf(){
        this.$store.commit('reset')
    }
  }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
  .not-wrapper{
    /* background: linear-gradient(#5B759F,#1C254C); */
    width: 100vw;
    height:100vh;
    padding-top:25vh;
    padding-bottom: 25vh;
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    align-items: center;
  }
  .main-wrapper{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 100%;
  }
  .router{
      margin-top: 1.5rem;
  }
  .return{
      padding: 1rem;
      border: solid rgba(0,0,0,0);
      font-size: 1.5rem;
      transition: 0.5s;
  }
  .return:hover{
      border: solid $dark-blue;
  }
</style>