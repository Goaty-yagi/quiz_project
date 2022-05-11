<template>
    <div class="signin-wrapper">
        <div class="flex-wrapper">
            <p class='title-white'>ユーザー登録</p>
            <Progress
            v-if='showProgress'
            />
        </div>
        <div :class="{'slide-in':slideIn,'slide-out':slideOut}" id="slide">
        <form v-if='showProgress' @submit.prevent='submitForm' class="field-wrapper">
            <div class="field">
                <div class="input-box" ref='formName'>
                    <i class="fas fa-robot" id='in-font'><input required class="text-box" type='text' v-model='username' id='Username' placeholder="Username"></i>
                </div>       
            </div>
            <div class="field">
                <div class="input-box" ref='formMail'>
                    <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email' id='E-mail' placeholder="E-mail"></i>
                </div>         
            </div>
            <div class="field">
                <div class="input-box">
                    <i class="far fa-envelope" id='in-font'><input required class="text-box" type='email' v-model='email2' id='Confirm' placeholder="Confirm"></i>
                </div>         
            </div>
            <!-- <div class="field">
                <div class="input-box">
                    <i class="fas fa-globe" id='in-font'>
                        <select class="select-box" id='Country' v-model='country' >
                        <option hidden>Country-Name</option>
                        <option>unko</option>
                        </select>
                    </i>
                </div>         
            </div> -->
            <div v-if='mailError||nameError||mailInUseError' class='error-form'>
                <i class="fas fa-exclamation-triangle"></i>
                <div v-if='mailError'>{{ mailError}}</div>
                <div v-if='nameError'>{{ nameError }}</div>
                <div v-if='mailInUseError'>{{ mailInUseError }}</div>
            </div>
            <div>
                <button class='fbottun'  ref='bform' id=''>次へ</button>
            </div>
        </form>
        </div>
        <transition name="slide-in">
            <Password
            class="components"
            v-if='$store.state.step==2&&showPassword&&!showEdit'
            @handle='showProgressHandler'
            @confHandle='showRegiConfHandler'
            @handleAfterPassword='handleAfterPassword'
            />
        </transition>
        <transition name="notice">
            <RegisterConfirm
            v-if='$store.state.step==2&&showRegiConf&&!showEdit&&!showSent'
            @handle='showProgressHandler'
            @edithandle='showEditHandler'
            @sentHandle='showSentHandler'
            @showPasswordFalse='showPasswordFalse'
            />
        </transition>
        <transition name="notice">
          <Sent
            v-if='showSent&&$store.state.step==3'
            @handle='showProgressHandler'
            @sentHandle='showSentHandler'
            />
        </transition>
        <transition name="slide-in">
            <Edit
                v-if='showEdit&&!showPassword'
                @handle='showProgressHandler'
                @confHandle='showRegiConfHandler'
                @edithandle='showEditHandler'
                :showProgress='showProgress'/>
        </transition>
    </div>
</template>

<script>
import Progress from '@/components/signin/Progress.vue'
import Sent from '@/components/signin/Sent.vue'
import ID from '@/components/signin/ID.vue'
import Password from '@/components/signin/Password.vue'
import RegisterConfirm from '@/components/signin/RegisterConfirm.vue'
import Registered from '@/components/signin/Registered.vue'
import Edit from '@/components/signin/Edit.vue'


export default {
    components:{
        Progress,
        Sent,
        ID,
        Password,
        RegisterConfirm,
        Registered,
        Edit
    },
    data(){
        return{
            step:0,
            username:'',
            email:'',
            email2:'',
            // country:'',
            nameError:null,
            mailError:null,
            mailInUseError:null,
            showSent: false,
            showProgress:true,
            showButton:true,
            showRegiConf:false,
            showEdit:false,
            showPassword: false,
            slideIn:true,
            slideOut:false
            // afterPassword:false

        }
    },
    updated(){
        
        this.showButtonHandler()
        console.log(this.$store.state.signup.username)
        // this.getClass()
    },
    mounted(){
        this.$store.commit('handleOnSigningup')
        console.log('mounted',this.$store.getters.onSigningup)
        this.step = this.$store.state.step
    },
    beforeUnmount(){
        this.$store.commit('handleOnSigningup')
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
        nameError:function(v) {if (v != '') { this.$refs.formName.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
        mailError:function(v) {if (v != '') { this.$refs.formMail.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
        mailInUseError:function(v) {if (v != '') { this.$refs.formMail.classList.add('form-error')}
        else{this.$refs.formName.classList.remove('form-error')}},
    },
    methods:{
        async submitForm(){
            // validate email
            // console.log('clicked1')
            this.nameError = this.username.length < 21 ?
            '' : '@name must be less than 20 chars'
            this.mailError = this.email == this.email2 ?
            '' : '@addresses are not the same'
            console.log(this.nameError)
            if (this.nameError == ''&& this.mailError ==''){
                await this.$store.dispatch('checkEmail',this.email)
                console.log(this.$store.state.signup.checkedEmail)
                this.mailInUseError = this.$store.state.signup.checkedEmail ?
                '' : '@address is already in use'
                console.log(this.mailInUseError)
                if (this.$store.state.signup.checkedEmail == true){
                // this.showSentHandler()
                this.handleSlide()
                this.showPasswordTrue()
                this.showProgressHandler()
                this.$store.commit('addStep')
                this.$store.commit('getUsername',this.username)
                this.$store.commit('getEmail',this.email)
                this.$store.commit('getEmail2',this.email2)
                // this.$store.commit('getCountry',this.country)
                }                
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
        showEditHandler(){
            this.showEdit = !this.showEdit
        },
        progressOff(){
            this.showProgress = false
        },
        showButtonHandler(){
            if(this.username!=''&&
                this.email!=''&&
                this.email2!=''
                // &&this.country!=''
                ){
                    this.showButton = false
            }
            else{
                this.showButton = true
            }
        },
        getFilledItems(item){
            if(item == 'Username'){
                if(this.$store.signup.state.username !=''){
                    this.username = this.$store.signup.state.username
                }
            }
            if(item == 'E-mail'){
                if(this.$store.signup.state.email !=''){
                    this.email = this.$store.signup.state.email
                }
            }
            if(item == 'Confirm'){
                if(this.$store.signup.state.email2 !=''){
                    this.email2 = this.$store.signup.state.email2
                }
            }
            // if(item == 'Country'){
            //     if(this.$store.signup.state.country !=''){
            //         this.country = this.$store.signup.state.country
            //     }
            // }
        },
        showPasswordTrue(){
            this.showPassword = true
        },
        showPasswordFalse(){
            this.showPassword = false
        },
        handleSlide(){
            this.slideOut = !this.slideOut
            this.slideIn = !this.slideIn
            // var slide = document.getElementById('slide')
            // slide.setAttribute('style','display:none')
            // console.log('slide',slide)
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .signin-wrapper{
        width:100%;
        position: relative;
        flex-direction: column;
        display: flex;
        padding-top:5rem;
        // justify-content: center;
        align-items: center;
        overflow:scroll;
        .title-white{
            margin-bottom: 1rem;
        }
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
.components{
    display: absolute;
}
#slide{
    display: absolute;
}
// .slide-in{
// 	text-align: center;
// 	opacity: 0;
// 	animation: slide-in-anim 1.5s ease-out forwards;
// }
.slide-out{
    text-align: center;
	opacity: 1;
	animation: slide-out-anim 1.5s ease-out forwards;
}

// @keyframes slide-in-anim {
// 	0% {
// 		opacity: 0;
//         transform: translateX(-20%);
// 	}
// 	// 60% {
// 	// 	transform: translateX(-10%);
// 	// }
// 	// 75% {
// 	// 	transform: translateX(2%);
// 	// }
// 	100% {
// 		opacity: 1;
// 		transform: translateX(0);
// 	}
// }
@keyframes slide-out-anim {
	0% {
		opacity: 1;
        transform: translateX(0);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-60%);
        display: none;
        
	}
}


.slide-in-enter-active {
  animation: slide-in  ease-out 1.5s;
}
.slide-in-leave-active {
  animation: slide-out ease-out 1.5s;
}
@keyframes slide-in {
  0% {
		opacity: 0;
        transform: translateX(5%);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 1;
		transform: translateX(0);
	}
}
@keyframes slide-out {
  0% {
		opacity: 1;
        transform: translateX(0);
	}
	// 60% {
	// 	transform: translateX(-10%);
	// }
	// 75% {
	// 	transform: translateX(2%);
	// }
	100% {
		opacity: 0;
		transform: translateX(-10%);
	}
}
@media(max-width: 629px){
    .signin-wrapper{
        padding-top:1rem;
        
    }
}
</style>