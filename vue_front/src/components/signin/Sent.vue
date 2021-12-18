<template>
    <div class='notification-wrapper'>
        <div class='notice-wrapper'>
            <img class='image' src="@/assets/logo.png">
            <p class='text1'>IDを送信しました。</p>
            <p class='text1'>登録したアドレスで確認してください。</p>
            <button  @click='addStep' class='button' id='color-button'><p>次へ</p></button>
        </div>
    </div>
</template>

<script>
export default {
    props:[
    ],
    methods:{
        addStep(){
            this.$emit('sentHandle')
            this.$emit('handle')
            this.$store.commit('addStep')
        }
    },
    mounted(){
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .notification-wrapper{
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
    .notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        display:inline-block;
        padding-top:1.5rem;
    }
    .image{
        width:15%;
        height:15%;
        margin-left: auto;
        margin-right: auto;
    }
    .text1{
        font-size:7vw;
        font-weight: bold;
        margin:2rem;
    }

    .button{
        font-weight: bold;
        margin:3rem;
    }
    #register-button{
        width: auto;
        font-size:5vw;
        padding:1.5%;
        
    }
@media(min-width: 660px) and (max-width: 1024px){
    .notice-wrapper{
        margin-top:10%;
        width:80%;
    }
    #font{
        font-size:35vw;
    }
    .text{
        font-size:3vw;
    }
    #register-button{
        font-size:3vw;
    }
  }
@media(min-width: 1025px){
    .text1{
        font-size:3vw;
    }
    .notice-wrapper{
        margin-top:10%;
        width:40%;
        height:50vw;
    }
    .block{
        margin:1.5vw;
    }
    #font{
        font-size:13vw;
    }
    .circle{
        height: 10vw;
        width: 10vw;
    }
    .text{
        font-size:1.1vw;
    }
    #register-button{
        font-size:3vw;
    }
    #in-font{
        font-size:3vw;
    }
    #register-button{
        font-size:1.5vw;
  }
}
</style>