<template>
    <div class="signin-wrapper">
        <div class="flex-wrapper">
            <p class='signin-text'>ユーザー登録</p>
            <Progress
            v-if='showProgress'
            />
        </div>
        <form v-if='$store.state.step==1&&showProgress' @submit.prevent='submitForm' class="field-wrapper">
            <div class="field">
                <!-- <label class="label">Username</label> -->
                <div class="input-box">
                    <i class="fas fa-robot" id='in-font'><input required class="text-box" type='text' v-model='username' placeholder="Username"></i>
                </div>       
            </div>
            <div v-if='nameError' class='error'>{{ nameError }}</div>  
            <div class="field">
                <!-- <label class="label">E-mail</label> -->
                <div class="input-box">
                    <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email' placeholder="E-mail"></i>
                </div>         
            </div>
            <div class="field">
                <!-- <label class="label">Confirm</label> -->
                <div class="input-box">
                    <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email2' placeholder="Confirm"></i>
                </div>         
            </div>
            <div v-if='mailError' class='error'>{{ mailError }}</div>
            <div class="field">
                <!-- <label class="label">Country</label> -->
                <div class="input-box">
                    <i class="fas fa-globe" id='in-font'>
                        <select class="select-box" v-model='country' >
                        <option hidden>Country-Name</option>
                        <option>unko</option>
                        </select>
                    </i>
                </div>         
            </div>
            <input class='check-box' required type='checkbox' v-model='robotConf'>
            <span class='check-box-text'>私はロボットではありません。</span>
            <div>
                <button class='fbottun'  ref='bform' id=''>送信</button>
            </div>
        </form>
        <transition name="notice">
          <Sent
            v-if='showSent&&$store.state.step==1'
            @handle='showProgressHandler'
            @sentHandle='showSentHandler'
            />
        </transition>
        <Password
          v-if='$store.state.step==3'
          @handle='showProgressHandler'
          @confHandle='showRegiConfHandler'/>

        <ID
            v-if='$store.state.step==2'
            @handle='showProgressHandler'/>
        <RegisterConfirm
           v-if='$store.state.step==3&&showRegiConf'
           @handle='showProgressHandler'
           />
        <Registered
            v-if='$store.state.step==4'
            @handle='showProgressHandler'
            />
    </div>
</template>

<script>
import Progress from '@/components/signin/Progress.vue'
import Sent from '@/components/signin/Sent.vue'
import ID from '@/components/signin/ID.vue'
import Password from '@/components/signin/Password.vue'
import RegisterConfirm from '@/components/signin/RegisterConfirm.vue'
import Registered from '@/components/signin/Registered.vue'
export default {
    components:{
        Progress,
        Sent,
        ID,
        Password,
        RegisterConfirm,
        Registered
    },
    data(){
        return{
            step:0,
            username:'',
            email:'',
            email2:'',
            country:'',
            robotConf:'',
            nameError:'',
            mailError:'',
            showSent: false,
            showProgress:true,
            showButton:true,
            showRegiConf:false,

        }
    },
    updated(){
        
        this.showButtonHandler()
        // this.getClass()
    },
    mounted(){
        this.step = this.$store.state.step
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
    },
    methods:{
        submitForm(){
            // validate email
            // console.log('clicked1')
            this.nameError = this.username.length < 6 ?
            '' : 'username must be less than 5 chars'
            this.mailError = this.email == this.email2 ?
            '' : 'your mail adrress is not the same'
            if (this.nameError == ''&& this.mailError ==''){
                this.showSentHandler()
                this.showProgressHandler()
            }
        },
        showSentHandler(){
            this.showSent = !this.showSent
        },
        showProgressHandler(){
            this.showProgress = !this.showProgress
        },
        showRegiConfHandler(){
            this.showRegiConf = !this.showRegiConf
        },
        showButtonHandler(){
            if(this.username!=''&&
                this.email!=''&&
                this.email2!=''&&
                this.country!=''&&
                this.robotConf!=''){
                    this.showButton = false
            }
            else{
                this.showButton = true
            }
        },
        // getClass(){
        //     if(this.showSent == false){
        //         if (this.showButton == false){
        //         this.$refs.bform.classList.add('button-hover')
        //         }else{
        //             this.$refs.bform.classList.remove('button-hover')
        //     }   
        //     }
        // },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .signin-wrapper{
        height: 100vh;
        width:100vw;
        flex-direction: column;
        align-items: flex-start;;
        display: flex;
        padding-top:5rem;
        // justify-content: center;
        align-items: center;
        }
    .signin-text{
        color:white;
        font-size:2rem;
       
    }
    .field-wrapper{
        margin-top:3rem;
    }
    .field-wrapper{

    }
    .field{
        display: flex;
        justify-content: flex-start;
        align-items: center;
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
        
    }#in-font{
        margin-left:0.5rem;
        color:rgb(158, 158, 158); 
        transition:0.3s;
        position:relative;
    }
    #in-font:focus-within{
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
    .error{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.1rem solid red;
        background:rgb(243, 214, 214);
        width: 90%;
        margin-left: auto;
        margin-right: 0;
        }
</style>