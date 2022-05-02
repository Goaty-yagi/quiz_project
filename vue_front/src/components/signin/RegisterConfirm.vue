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
                        <div class="text-box" id='mail'>{{ $store.state.signup.email }}</div>
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
                <button  @click='goEdit' class='button' :disabled='error' id='color-button'><p>編集する</p></button>
                <button  @click='addStep' class='button' :disabled='error' id='color-button'><p>登録</p></button>
            </div>
            <transition name="notice">
                <div v-if='error' class="error">
                    <p class='error-message' v-if='error'> {{ error }} </p>
                    <button class='fbottun' id='color-button'>戻る</button>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import ID from './ID.vue'
import axios from 'axios'
export default {
  components: { ID },
    data(){
        return{
            error: null,
            errorMessage:'このメールアドレスはすでに使われています。',
            errorMessage2:'登録できませんでした。もう一度お試しください。',
        }
    },
    methods:{
       async addStep(){
            try{
                await this.registerUserOndDjango()
                await this.$store.dispatch('signup',{
                email: this.$store.state.signup.email,
                password: this.$store.state.signup.password
                })
                this.$emit('confHandle')
                this.$emit('sentHandle')
                this.$store.commit('addStep')
                this.$emit('handle')
                console.log('start django add')
            }catch(err){
                this.error = this.errorMessage2
                console.log('catch error',this.error)
            }
        },
        registerUserOndDjango(){
            console.log('start add')
            if(this.$store.getters.getTempUser){
                try{
                    axios({
                        method: 'post',
                        url: '/api/user/',
                        data: {
                            UID: this.$store.state.signup.user.uid,
                            name: this.$store.state.signup.username,
                            email: this.$store.state.signup.email,
                            country: this.$store.state.signup.country,
                            quiz_taker: [
                                {grade: this.$store.getters.getTempUser.grade},
                                {level: this.$store.getters.getTempUser.level}
                            ]
                        },
                    }) 
                }
                catch{

                }
            }
        },
        goEdit(){
            this.$emit('edithandle')
            this.$emit('handle')
        },
        // async handleSubmit(){
        //     try {
        //         await this.$store.dispatch('sentValidation',{
        //             email: this.$store.state.signup.email,
        //             password: this.$store.state.signup.password
        //             })
        //             this.$store.dispatch('')
        //     } catch (err){
        //         this.error = this.errorMessage2
        //         console.log('catch error',this.error)
        //     }
        // },
        // errorMessageHandler(error){
        //     if ( error == 'Firebase: Error (auth/email-already-in-use).'){
        //         this.error = this.errorMessage
        //     }else{
        //         this.error = this.errorMessage2
        //     }
        // }        
    },
    mounted(){
        console.log('mail',this.$store.state.signup.email, 'password',this.$store.state.signup.password)
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
        position:relative;
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
        font-size:0.5rem;
    }
    #in-font{
        font-size:1.5rem;
        margin-left: 1rem;
        position:absolute;
        left:0;
        top:0.6rem;
    }
    .text-box{
        // position: absolute;
        left:0;
        right:0;
        top:0;
        bottom: 0;
        font-size:1.3rem;
        font-weight: bold;
        margin-top:0.5rem;
        margin-left:3rem;
        margin-right:2rem;
    }
    #mail{
        overflow-wrap: break-word;
        font-size:1rem;
        line-height: 0.9rem;
        margin-top:0.8rem;        
    }
    .buttons{
        display: flex;
        justify-content: center;
        align-items: center;

    }
    .button{
        font-weight: bold;
    }
    .error{
        position:absolute;
        border:solid red;
        background: rgb(247, 230, 232);
        border-radius: 1rem;
        height:70%;
        left:0;
        right:0;
        bottom:0;
        top:0;
        margin:auto;
        transition: 0.3s;
        padding:2rem;
        display:flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .error-message{
        font-weight: bold;
    }
</style>