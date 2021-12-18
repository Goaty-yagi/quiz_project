<template>
  <div class="quiz-conf">
    <article class='conf-wrapper'>
        <div class="conf-header">
            <p>初級ークイズに行く？</p>
            <!-- <button class="delete"></button> -->
        </div>
        <div class="conf-body">
            <router-link @click='closeConf' to=/ class="button m-2"><i class="fas fa-home"></i>NO</router-link>
            <router-link :to='this.$store.state.randomURL' class="button m-2" id='or-button'>START</router-link>
            <!-- <button id='or-button' @click='showCompoHandler'>SRART</button>    -->
        </div>
    </article>                     
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
    @media(max-width: 414px){
        .quiz-conf{
            width:100%;
            height:100%;
            .conf-wrapper{
                margin-top:12rem;
               
            }
        }
    }
    @media(min-width: 415px) and (max-width: 767px){
        .quiz-conf{
            width:50%;
            height:50%;
            .conf-wrapper{
                margin-top:15rem;
                width:80%;
            }
        }
    }
    @media(min-width: 767px){
        .quiz-conf{
            width:50%;
            height:50%;
            .conf-wrapper{
                margin-top:15rem;
                width:60%;
                
            }
        }
    }
    .quiz-conf{
        top:0;
        position: fixed;
        background:rgba(0,0,0,0.5);
        width:100%;
        height:100%;        
        
        .conf-wrapper{
            border: solid  rgba(243, 91, 36, 0.808);
            border-radius: 1rem;
            overflow:hidden;
            margin-left: auto;
            margin-right: auto;
            
            

        }
        .conf-header{
            background-color: #ff9933;
            color:white;
            padding:0.5rem;
            font-weight:bold;
        }
        .conf-body{
            background-color: rgb(253, 245, 239);
            padding:1rem;
        }
    }
</style>