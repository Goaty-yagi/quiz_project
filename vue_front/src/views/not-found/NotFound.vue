<template>
<div class='not-wrapper'>
  <h1 class='title is-1 mt-4'> 404</h1>
  <h1 class='subtitle is-3'> Page not found</h1>
  <div>
    <router-link :to="{name:'Home'}" @click='closeConf'  class="is-centered mt-6"><i class="fas fa-home"></i>Return to Home</router-link>
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

<style scoped>
  .not-wrapper{
    /* background: linear-gradient(#5B759F,#1C254C); */
    width: 100vw;
    height:100vh;
    padding-top:25vh;
    padding-bottom: 25vh;
  }
</style>