<template>
    <div class='notification-wrapper'>
        <div class='regist-wrapper'>
            <div class='notice-wrapper'>
                <img class='image' src="@/assets/logo.png">
                <p class='text1'>ユーザー登録が完了しました。</p>
                <p class='text1'>毎日、クイズをしながら日本語スキルを高めよう！</p>
                <router-link to='/account' class='text2'>アカウント画面へ移動</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    mounted(){
        this.$emit('handle')
    },
    props:[
        'p'
    ],
    methods:{
        addStep(){
            this.$emit('sentHandle')
            this.$emit('handle')
            this.$store.commit('addStep')
        }
    },
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
    }
    .regist-wrapper{
        position:relative;
        text-align: center;
        width: 20rem;
        left:0;
        margin:auto;

    }
    .notice-wrapper{
        position:absolute;
        top:13rem;
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        padding-top:1rem;
        height:22rem;
    }
    .image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .text1{
        font-size:1.6rem;
        font-weight: bold;
        margin:0.5rem;
    }
    .text2{
        font-size:0.5rem;
        font-weight: bold;
        margin:2rem;
    }
    
</style>