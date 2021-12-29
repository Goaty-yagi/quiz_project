<template>
<div class="account-wrapper">
    <!-- <div v-if='emailVerified==false'> -->
        <div class='main-notification-wrapper'>
            <div class='main-notice-wrapper'>
                <img class='main-image' src="@/assets/logo.png">
                <p class='main-text1'>メール承認が完了していません。</p>
                <p class='main-text1'>メール承認を完了してください。</p>
                <button @click='resent' onclick="disabled = true" class='main-text1'>承認メールを送る。</button>                      
                <!-- <button  @click='addStep' class='button' id='color-button'><p>次へ</p></button> -->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods:{
        resent(){
            this.$store.dispatch('sendEmailVerify')
            this.$emit('handleShowSent')
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
.main-notification-wrapper{
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
    .main-notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        position:relative;
        padding-top:1.5rem;
        height:30rem;
        width: 20rem;
        }
    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1rem;
        font-weight: bold;
        margin:2rem;
    }
</style>