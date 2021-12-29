<template>
    <div>
        <div class="login-wrapper">
            <div class="flex-wrapper">
                <form class="id-form" @submit.prevent='submitForm' >
                        <p class='login-text'>ログイン</p>
                        <div class="field">
                            <div class="input-box">
                                <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email' id='E-mail' placeholder="E-mail"></i>
                            </div>         
                        </div>
                        <div class="field">
                            <div class="input-box">
                                <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" :type="inputType" v-model='password' placeholder="Password"></i>
                                <i :class="[passType ? 'fas fa-eye':'fas fa-eye-slash']" id='eye' @click='click' ></i>
                            </div>      
                        </div>
                        <div class='error-form'  v-if='userError||passError||manyError'>
                            <i class="fas fa-exclamation-triangle"></i>
                            <div>{{ userError }}</div>
                            <div>{{ passError }}</div>
                            <div>{{ manyError }}</div>
                        </div>
                        <div class='text-wrapper' v-if='passError'>
                            <p>パスワードをお忘れですか。</p>
                            <p  @click='resetPass' class='text'>パスワードの再設定</p>
                        </div>
                        <div class='text-wrapper' v-if='userError'>
                            <p>ユーザー登録しますか。</p>
                            <p @click='goSignup' class='text'>ユーザー登録</p>
                        </div>
                        <div>
                            <button class='fbottun' ref='bform'>ログイン</button>
                        </div>
                </form>
            </div>
        </div>
        <div>
        <SentPassReset v-if='showSentPassReset'/>
        <NotVerified v-if='showNotVerified'
        @handleShowSent = 'handleShowSent'
         />
        <Sent v-show='showSent'/>
  </div>
    </div>
</template>

<script>
import {router} from "../main.js"
import SentPassReset from '@/components/login/SentPassReset.vue'
import NotVerified from '@/components/login/NotVerified.vue'
import Sent from '@/components/signin/Sent.vue'
export default {
    components:{
        SentPassReset,
        Sent,
        NotVerified
    },
    data(){
        return{
            email:'',
            password:'',
            passType:true,
            showButton:true,
            passError:null,
            userError:null,
            manyError:null,
            showSentPassReset:false,
            showSent:false,
            showNotVerified:false,
            store: this.$store.state.signup
        }
    },
    updated(){
        console.log('login check ',this.store.user)
        this.showButtonHandler()
        console.log(this.email,this.password,this.error)
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
    },
    computed: {
        inputType: function () {
        return this.passType ? "password":"text";
            }
        },
    methods:{
        showButtonHandler(){
            if(this.password != '' &&this.email != ''){
                this.showButton = false
            }else{
                this.showButton = true
                }
            },
        click(){
            console.log('click')
            this.passType = !this.passType
        },
        goSignup(){
            this.$router.push({name:'Signup'})
        },
        handleShowSentPassReset(){
            this.showSentPassReset = true
        },
        handleShowNotVerified(){
            this.showNotVerified = true
        },
        async resetPass(){
            await this.$store.dispatch('passwordReset',this.email)
            this.handleShowSentPassReset()

        },
        handleShowSent(){
            this.showSent = true
            console.log('showsent')
        },
        async submitForm(){            
            try{
                await this.$store.dispatch('login',{
                email:this.email,
                password:this.password})
                if(this.store.checkedEmail!=true){
                    this.handleShowNotVerified()
                }else{
                    router.push('/')
                this.$store.commit('reset')
                }
            }catch(err){
                console.log(typeof(err),err.code)
                this.userError = err.code == 'auth/user-not-found'?
                'ユーザーが存在しません。' : '' 
                this.passError = err.code == 'auth/wrong-password'?
                'パスワードが違います。' : ''
                this.manyError = err.code == 'auth/too-many-requests'?
                '短時間にリクエストを複数受けたため一時的にリクエストを停止します。暫く経ってもう一度お試しください。' :''               
            }     
        }
    }
}
</script>


<style scoped lang='scss'>
@import "style/_variables.scss";
    .login-wrapper{
        width:100vw;
        flex-direction: column;
        display: flex;
        padding-top:5rem;
        // justify-content: center;
        align-items: center;
        }
    .login-text{
        color:white;
        font-size:1.2rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
       
    }
    .field-wrapper{
        margin-top:3rem;
    }
    .field{
        display: flex;
        justify-content: flex-start;
        align-items: center;
        align-self: center;
    }
    .label{
        color:white;
        width: 2.7rem;
        overflow-wrap: break-word;
        margin-right:1%;
        line-height:1rem
    }.label:not(:last-child) {
        margin-bottom: initial;
}
    input[type="text"]:focus {
        outline: none;
        }
    input[type="email"]:focus {
        outline: none;
    }
    select:focus {
        outline: none;
        }
    .input-box:focus-within{
        border: solid $base-color;
        
        }
    .input-box{
        border: 0.12rem solid $base-color;
        border-radius: 100vh;
        background: $back-white;
        width: 17rem;
        height: 3rem;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        position:relative;
        
    }#in-font{
        margin-left:0.5rem;
        color:rgb(158, 158, 158); 
        transition:0.3s;
        position:relative;
    }
    #in-font:focus-within{
        color:rgb(92, 92, 92);

    }
    #eye{
        position:absolute;
        right:0;
        margin-right:0.5rem;
        color:rgb(158, 158, 158);
        transition:0.3s;
    }
    #eye:hover{
        color:rgb(92, 92, 92);
    }
    #eye:focus-within{
        color:rgb(92, 92, 92);
    }
    .text-box{
        width: 14rem;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
        position:absolute;
        left:1rem;
    }
    .select-box{
        width: 82%;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
    }
    
    .check-box-text{
        color:white;
        margin-left:1rem;
    }
    .text-wrapper{
        display:flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .text:hover{
        background: grey;
    }
    .text{
        color:white;margin-top:1rem;
        border: 0.1rem solid white;
        border-radius: 0.5rem;
        width: 60%;
        transition:0.5s;
    }
    .error-form{
        width: 17rem;
    }
    p{
        color:white;
        margin-top:1rem;
    }
</style>