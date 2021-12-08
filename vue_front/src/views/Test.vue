<template>
  <div class="home">
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>
    <div>
      Hello!
      <router-link :to="(quizRouter('a','s','8'))">Quiz</router-link>
      <!-- <p> {{ this.$store.commit('unko') }}</p> -->
      <!-- {{st}} -->
      <p>{{ this.$store.state.unko }}</p>
      <!-- {{ this.$store.commit('ko','manko')}} -->
      <p>{{ questions}}</p>
      
    </div>
  </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
export default {
  name:'questions',
  data(){
    return{
      st:'o',
      id: 5
    }
  },
  methods:{
    quizRouter(i,f,n){
      return { name: 'Quiz', params:{ id:i, field:f, num:n}}
    },
    ...mapActions(['getquiz','getquestions'])
    // unko(){
    //   this.$store.commit('unko',)
    // }
    },
    created(){
      this.$store.commit('setNum',this.id)
      this.getquiz()
      this.getquestions()
    },
  // mounted(){
  //     this.st = this.$store.commit('unko')
  //     console.log(this.st)
  // }
  computed: mapGetters(['questions','quizzes'])

}
</script>

<style>

</style>