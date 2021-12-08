<template>
  <div class="quiz-conf">
    <article class='conf-wrapper'>
        <div class="conf-header">
            <p>初級ークイズに行く？</p>
            <!-- <button class="delete"></button> -->
        </div>
        <div class="conf-body">
            <router-link @click='closeConf' to=/ class="button"><i class="fas fa-home"></i>NO</router-link>
            <router-link :to='this.$store.state.randomURL' class="button"><i class="far fa-hand-point-right"></i>YES</router-link>    
        </div>
    </article>
                
                <!-- <router-link :to="(this.$store.commit('getURLs',4),this.$store.state.randomURL)" class="button"><i class="fas fa-home"></i>YES</router-link> -->
                
           
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
            this.$emit('close')
            this.$store.commit('reset')
        }
    }
}
</script>

<style lang='scss' scoped>
    .quiz-conf{
        top:0;
        position: fixed;
        /* background-color: red; */
        background:rgba(0,0,0,0.5);
        width:100%;
        height:100%;
        
        .conf-wrapper{
            border: solid  rgba(243, 91, 36, 0.808);
            border-radius: 1rem;
            margin-top:10rem;
            overflow:hidden;

        }
        .conf-header{
            box-sizing:inherit;;
            background-color: #ff9933;
            color:white;
            padding:0.5rem;
        }
        .conf-body{
            background-color: rgb(253, 245, 239);
            padding:1rem;
        }
    }
</style>