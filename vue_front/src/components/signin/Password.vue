<template>
    <div class="password-wrapper">
        <form class="id-form" @submit.prevent='submitForm' >
            <div class='field-wrapper'>
                <p class='password-text'>パスワード設定</p>
                <div class="field">
                    <div class="input-box" ref='pass'>
                        <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" :type="inputType" v-model='password' placeholder="Password"></i>
                        <i :class="[passType ? 'fas fa-eye':'fas fa-eye-slash']" id='eye' @click='click' ></i>
                    </div>      
                </div>
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" :type="inputType2" v-model='password2' placeholder="Conf Password"></i>
                        <i :class="[passType2 ? 'fas fa-eye':'fas fa-eye-slash']" id='eye' @click='click2' ></i>
                    </div>          
                </div>
            </div>
            <div class='check-box-wrapper'>
                <input class='check-box' required type='checkbox' v-model='accept'>
                <span @click='goPolicy' class='check-box-text'>・利用規約に同意します。</span>
            </div>
            <div class='error-form' v-if='passwordError||passwordError2'>
                <i class="fas fa-exclamation-triangle"></i>
                <div v-if='passwordError' >{{ passwordError }}</div> 
                <div v-if='passwordError2'>{{ passwordError2 }}</div>
            </div>    
            <div>
                <button class='fbottun' ref='bform'>次へ</button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return{
            password:'',
            password2:'',
            accept:'',
            showButton:true,
            passwordError:'',
            passwordError2:'',
            passType:true,
            passType2:true,
        }
    },
    mounted(){
        this.$emit('handle')
    },
    updated(){
        this.showButtonHandler()
    },
    computed: {
    inputType: function () {
      return this.passType ? "password":"text";
        },
    inputType2: function () {
      return this.passType2 ? "password":"text";
        }
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
        passwordError:function(v) {if (v != '') { this.$refs.pass.classList.add('form-error')}
        else{this.$refs.pass.classList.remove('form-error')}},
    },
    methods:{
        showButtonHandler(){
            if(this.password!=''&&this.password2!=''&&this.accept==true){
                this.showButton = false
                }
            else{
                this.showButton = true
                }
            },
        submitForm(){
            // validate password
            console.log('clicked')
            this.passwordError = this.password == this.password2?
            '' : '@passwords are not the same'
            this.passwordError2 = this.password.length > 7?
            '' : '@password is less than 8 char'
            if (this.passwordError == ''&&this.passwordError2 == ''){
                this.$emit('confHandle')
                this.$emit('handleAfterPassword')
                this.$store.commit('getPassword',this.password)         
            }
        },
        click(){
            this.passType = !this.passType
        },
        click2(){
            this.passType2 = !this.passType2
        },
        goPolicy(){
            this.$router.push({name:'Policy'})
        }
    }
        
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .password-wrapper{
        width:100vw;
        flex-direction: column;
        align-items: flex-start;;
        display: flex;
        position: absolute;
        align-items: center;
        margin-top: 100px;
        }
    .password-text{
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
    input[type="password"]:focus {
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
    .form-error{
        border: solid red;
      }
    .text-box{
        width: 14rem;
        border:none;
        background: $back-white;
        margin-left:0.5rem;
        position:absolute;
        left:1rem;
    }
    .check-box-wrapper{
        margin-top: 1.5rem;
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
    .error-wrapper{
        width: 100%;
        height:5rem;
    }
</style>