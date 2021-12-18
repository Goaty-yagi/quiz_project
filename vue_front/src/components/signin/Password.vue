<template>
    <div class="password-wrapper">
        <form class="id-form" @submit.prevent='submitForm' >
            <div class='field-wrapper'>
                <p class='password-text'>パスワード設定</p>
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" type='password' v-model='password' placeholder="Password"></i>
                    </div>      
                </div>
                <div class="field">
                    <div class="input-box">
                        <i class="fas fa-unlock-alt" id='in-font'><input required class="text-box" type='password' v-model='password2' placeholder="Conf Password"></i>
                    </div>          
                </div>
            </div>
            <div class='error-wrapper'>
                <div v-if='passwordError' class='error'>{{ passwordError }}</div> 
            </div>            

            <input class='check-box' required type='checkbox' v-model='accept'>
            <span class='check-box-text'>・利用規約に同意します。</span>
            <!-- <p class='password-text'>{{ accept }}</p> -->
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
            passwordError:''
        }
    },
    mounted(){
        this.$emit('handle')
    },
    updated(){
        console.log('souwb',this.showButton)
        this.showButtonHandler()
    },
    watch:{
        showButton:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
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
            '' : 'your password is not the same'
            if (this.passwordError == ''){
                this.$emit('confHandle')           
            }
        },
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
        align-items: center;
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
    .error-wrapper{
        width: 100%;
        height:5rem;
    }
    .error{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.1rem solid red;
        background:rgb(243, 214, 214);
        width: 100%;
        height:60%;
        margin-top:1rem;
        // margin-left: auto;

        // margin-right: 0;
        }
</style>