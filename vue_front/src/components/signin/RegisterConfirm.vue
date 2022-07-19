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
                    <div class="text-box">{{ viewableCountry }}</div>
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
  props:[
        'viewableCountry',
    ],
    data(){
        return{
            error: null,
            errorMessage:'このメールアドレスはすでに使われています。',
            errorMessage2:'登録できませんでした。もう一度お試しください。',
            userInfo:'',
            gotIP:false,
            IPInfo:[
                {city:"",
                ip:"",
                loc:"",
                org:"",
                postal:"",
                region:"",
                timezone:"",
                country:""
                }
            ],
        }
    },
    mounted(){
        this.$store.commit('fixedScrollTrue')
        this.getCountry()
        console.log('mail',this.$store.state.signup.email, 'password',this.$store.state.signup.password)
        console.log('mounted at confiem',this.$store.getters.fixedScroll)

    },
    beforeUnmount(){
        this.$store.commit('fixedScrollFalse')
    },
    computed:{
        user(){
            try{
                return this.$store.state.signup.djangoUser
            }
            catch{
                return null
            }
        },
    },
    methods:{
        async addStep(){
            await this.$store.dispatch('signup',{
            email: this.$store.state.signup.email,
            password: this.$store.state.signup.password
            })
            this.$emit('confHandle')
            this.$emit('sentHandle')
            this.$store.commit('addStep')
            this.$emit('handle')
            await this.registerUserAndDjango()
        },
        async registerUserAndDjango(){
            if(this.$store.getters.getTempUser.test){
                console.log('YES TEMP')
                this.userInfo={
                    UID: this.$store.state.signup.user.uid,
                    name: this.$store.state.signup.username,
                    email: this.$store.state.signup.email,
                    country: this.$store.state.signup.country,
                    quiz_taker: [
                        {grade: this.$store.getters.getTempUser.grade},
                        {level: this.$store.getters.getTempUser.level},
                        {user_status: this.$store.getters.getTempUser.statusList}
                    ],
                    ip_data: [{
                        city: this.IPInfo.city,
                        ip: this.IPInfo.ip,
                        loc: this.IPInfo.loc,
                        org: this.IPInfo.org,
                        postal: this.IPInfo.postal,
                        region: this.IPInfo.region,
                        timezone: this.IPInfo.timezone,
                        country: this.IPInfo.country
                    }]
                }
            }else{
                console.log('NO TEMP')
                this.userInfo={
                    UID: this.$store.state.signup.user.uid,
                    name: this.$store.state.signup.username,
                    email: this.$store.state.signup.email,
                    country: this.$store.state.signup.country,
                    ip_data: [{
                        city: this.IPInfo.city,
                        ip: this.IPInfo.ip,
                        loc: this.IPInfo.loc,
                        org: this.IPInfo.org,
                        postal: this.IPInfo.postal,
                        region: this.IPInfo.region,
                        timezone: this.IPInfo.timezone,
                        country: this.IPInfo.country
                    }]
                }
            }
            try{
                console.log("try",this.userInfo)
                this.$store.dispatch('signupDjangoUser',this.userInfo)
                // await axios({
                //     method: 'post',
                //     url: '/api/user/',
                //     data: this.userInfo
                    // {
                    //     UID: this.$store.state.signup.user.uid,
                    //     name: this.$store.state.signup.username,
                    //     email: this.$store.state.signup.email,
                    //     quiz_taker: [
                    //         {grade: this.$store.getters.getTempUser.grade},
                    //         {level: this.$store.getters.getTempUser.level}
                    //     ],
                        // ip_data: [{
                        //    city: this.IPInfo.city,
                        //    ip: this.IPInfo.ip,
                        //    loc: this.IPInfo.loc,
                        //    org: this.IPInfo.org,
                        //    postal: this.IPInfo.postal,
                        //    region: this.IPInfo.region,
                        //    timezone: this.IPInfo.timezone,
                        //    country: this.IPInfo.country
                        // }]
                    // },
                // })
            }
            catch(error){
                console.log('error',error.message)
                }
            
        },
        async goEdit(){
            this.$emit('showPasswordFalse')
            this.$emit('handle')
            this.$emit('edithandle')
        },
        async getCountry(){
            if(!this.gotIP){
                await axios
                .get("https://ipinfo.io/json?token=32e16159d962c5")
                // .then(response => {
                //     this.IPInfo = response.data
                //     console.log(this.IPInfo)
                //     })
                .then(response => {
                    let IP = response.data
                    this.IPInfo.city = IP.city
                    this.IPInfo.ip = IP.ip
                    this.IPInfo.loc = IP.loc
                    this.IPInfo.org = IP.org
                    this.IPInfo.postal = IP.postal
                    this.IPInfo.region = IP.region
                    this.IPInfo.timezone = IP.timezone
                    this.IPInfo.country = IP.country
                    console.log(this.IPInfo)
                    })
                .catch((e) => {
                    let logger = {
                        message: "in component/signin/register.getCountry. couldn't get country",
                        name: window.location.pathname,
                        actualErrorName: e.code,
                        actualErrorMessage: e.message,
                    }
                    context.commit('setLogger',logger)
                    router.push({ name: 'ConnectionError' })
                });
                this.gotIP = true
            }
        }    
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
        font-size:1.5rem;
    }
    #in-font{
        // font-size:1rem;
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
        font-size:1.2rem;
        font-weight: bold;
        margin-top:0.5rem;
        margin-left:3rem;
        margin-right:2rem;
    }
    #mail{
        overflow-wrap: break-word;
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