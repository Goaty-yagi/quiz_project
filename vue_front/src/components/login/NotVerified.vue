<template>
    <div class="account-wrapper l-wrapper">
        <div class="main-wrapper">
            <div class='main-notification-wrapper'>
                <div class='main-notice-wrapper'>
                    <div class="close-container">
                        <div v-if="!currentPageName" @click="unShow()" class="close">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                    <img @click="backHome()" class='main-image' src="@/assets/logo.png">
                    <div v-if="sent">
                        <p class='main-text1'>パスワード再登録メールを送信しました。</p>
                        <p class='main-text1'>登録したアドレスで確認してください。</p>
                    </div>
                    <div v-if="!sent">
                        <p class='main-text1'>メール承認が完了していません。</p>
                        <p class='main-text1'>メール承認を完了してください。</p>
                    </div>
                    <button v-if="!sent" @click='resent' onclick="disabled = true" class='btn-gray-black-gray-sq'>承認メールを送る</button>                      
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "@/main.js"
export default {
    props:[
        'currentPageName',
    ],
    data(){
        return{
            sent: false
        }
    },
    mounted(){
        this.sent = false
        console.log('NV',this.$options)
    },
    methods:{
        resent(){
            this.sent = true
            this.$store.dispatch('sendEmailVerify')
            this.$emit('handleShowSent')
        },
        backHome(){
            router.push('/' )
        },
        unShow(){
            this.$emit('handleShowEmailVerified')
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.account-wrapper{
    // height: 100%;
    width: 100%;
    .main-wrapper{
        display: flex;
        justify-content: center;
    }
}
.btn-gray-black-gray-sq{
    margin-bottom: 2rem;
    font-size: 1.2rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
}
img{
    margin-top: 1.5rem;
    cursor: pointer;
}
.main-notification-wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
    // min-height: 100%;
    width: 100%;
}
    .main-notice-wrapper{
        border: solid $base-color;
        border-radius: 2vh;
        background:$back-white;
        text-align: center;       
        position:relative;
        // padding-top:1.5rem;
        width: 80%;
        min-height: 120%;
    }
    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1.4rem;
        font-weight: bold;
        margin:2rem;
    }
</style>