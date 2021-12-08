<template>
  <section class="section">
    <div class="box" style='position:relative'>
      <img class='is-image' src="@/assets/japan.png">
      <div class='title-hero is-overlay'>
        <p class="is-size-6-mobile is-size-1-desktop is-size-3-tablet has-text-weight-bold mb-3">
         日本語試してみよう！
        </p>
        <p class="is-size-6 is-size-4-tablet">
          問題やる？
        </p>
        
        <p>{{ this.$store.state.id }}</p>
        <div  @click="onClick()">
          <div>
            <div @click='showCompoHandler'><i class="fas fa-home"></i>quiz</div>
          <!-- <router-link :to="(this.$store.commit('getURLs',4),this.$store.state.randomURL)" class="navbar-item"><i class="fas fa-home"></i>quiz</router-link> -->
          <!-- <router-link :to="(this.$store.commit('getURLs',5),this.$store.state.randomURL)" class="navbar-item"><i class="fas fa-home"></i>中</router-link> -->
          <!-- <router-link :to="(unko())" class="navbar-item"><i class="fas fa-home"></i>unko</router-link> -->
          </div>   
        </div>
      </div>
    </div>
     <div v-if='showCompo'>
        <QuizConf @close='showCompoHandler' />   
      </div>   
    
  </section>

</template>

<script>
import QuizConf from '@/components/QuizConf.vue'
export default {
  name: 'Home',
  components: {
  QuizConf
  },
  data(){
    return{
      manko: '/test/manko',
      // status: 2,
      field:'並び替え',
      // num:3,
      showCompo: false,
      item:{status: 2,num:5}
    }
  },
  methods:{
    unko(){
      return `/quiz/${this.status}`
    },
    onClick(){
      console.log('onclick')
      this.$store.commit('getURLs',this.item)
    },
    showCompoHandler(){
      console.log('handler')
      this.showCompo = !this.showCompo
    }
      
    
  }
}
</script>
<style lang="scss">
@import "style/_variables.scss";
@media(max-width: 414px){  
  .box{
      margin: 0;
      padding:0;
    }
  .section{
      margin: 0;
      padding:0;
    }
  .button{
    padding: 0.5rem;
    // box-sizing: border-box;
    // border: 1px solid $base-color;
    // background: $base-color
  }
  }
  .is-image{
    position:block;
    height: 100%;
    width:100%;
  }
  .title-hero{
    position: absolute;
    top: 50%;
    left: 50%;
    -ms-transform: translate(-50%,-50%);
    -webkit-transform: translate(-50%,-50%);
    transform: translate(-50%,-50%);
    margin:0;
    padding:0;
  }
  
</style>
