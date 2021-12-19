<template>
    <div class='notification-wrapper'>
        <div class='notice-wrapper'>
            <img class='image' src="@/assets/logo.png">
            <p class='text1'>以下の情報で登録しますか。</p>
            <div class="field">
                <div class="input-box">
                    <div><i class="fas fa-robot" id='in-font'></i></div>
                    <div class="text-box">{{ $store.state.signup.username }}</div>
                </div>         
            </div>
            <div class="field">
                <div class="input-box">
                    <div><i class="far fa-envelope" id='in-font'></i></div>
                    <div class="text-box">{{ $store.state.signup.email }}</div>
                </div>         
            </div>
            <div class="field">
                <div class="input-box">
                    <div><i class="fas fa-globe" id='in-font'></i></div>
                    <div class="text-box">{{ $store.state.signup.country }}</div>
                </div>         
            </div>
            <div class="field">
                <div class="input-box">
                    <i class="fas fa-unlock-alt" id='in-font'></i>
                    <div class="text-box">{{ $store.state.signup.password }}</div>
                </div>         
            </div>
            <div class="buttons">
                <button  @click='goEdit' class='button' id='color-button'><p>編集する</p></button>
                <button  @click='addStep' class='button' id='color-button'><p>登録</p></button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods:{
        addStep(){
            this.$emit('confHandle')
            this.$store.commit('addStep')
            this.$emit('handle')
        },
        goEdit(){
            this.$emit('edithandle')
            this.$emit('handle')
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
        height:30rem;
        width: 20rem;
    }
    .image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .text1{
        font-size:1rem;
        font-weight: bold;
        margin:2rem;
    }
    .input-box{
        border: solid $base-color;
        border-radius: 100Vh;
        // display: flex;
        // justify-content: flex-start;
        // align-items: center;
        margin-left: 1rem;
        margin-right: 1rem;
        height: 3rem;
        position:relative;
    }
    #in-font{
        font-size:1.5rem;
        margin-left: 1rem;
        position:absolute;
        left:0;
        top:0.4rem;
    }
    .text-box{
        position: absolute;
        left:0;
        right:0;
        top:0;
        bottom: 0;
        font-size:1.3rem;
        font-weight: bold;
        margin-top:0.3rem;
    }
    .buttons{
        display: flex;
        justify-content: center;
        align-items: center;

    }
    .button{
        font-weight: bold;
        
    }
</style>