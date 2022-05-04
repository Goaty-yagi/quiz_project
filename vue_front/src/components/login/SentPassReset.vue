<template>
    <div class='l-wrapper'>
        <div class='l-container'>
            <img class='image' src="@/assets/logo.png">
            <p class='text1'>パスワード再登録メールを送信しました。</p>
            <p class='text1'>登録したアドレスで確認してください。</p>
        </div>
    </div>
</template>

<script>
export default {
    props:[
    ],
    methods:{
        addStep(){
            this.$router.push({ name: 'Account' })
            // this.$emit('sentHandle')
            // this.$emit('handle')
            // this.$store.commit('addStep')
        }
    },
    mounted(){
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-container{
    min-height: 40%;
}
    .image{
        width:15%;
        height:15%;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 4rem;
    }
    .text1{
        font-size:1.5rem;
        font-weight: bold;
        margin:2rem;
    }
</style>