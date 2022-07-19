<template>
    <div class="enquire-wrapper" :class="{'scroll-fixed':created}">
        <div class="main-wrapper">
            <div class="content-wrapper">
                <div class="title-white">
                    <p>問い合わせ</p>
                </div>
                <form action="">
                    <div class="enquire-container">
                        <div class="enquire-title">名前</div>
                        <input class="enquire-input" type="text" v-model='form.name' placeholder="名前を入力してください">
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">メールアドレス</div>
                        <input class="enquire-input" type="text" v-model='form.mail' placeholder="メールアドレスを入力してください">
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">問い合わせタイプ</div>
                        <div class="enquire-type"
                        @click="showTypeHandle()">
                            <i
                            v-if="!form.type"
                            class="fas fa-angle-down"
                            :class="{'lotate':showType}">
                            </i>
                            <div v-if="form.type">{{ form.type }}</div>
                            <div v-if="showType" class="type-select">
                                <div class="select-loop"
                                v-for="(type,typeindex) in enquireType" 
                                    v-bind:key="typeindex">
                                    <p @click="getSelectType(type)" class="type">・{{type}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="enquire-container">
                        <div class="enquire-title">問い合わせ内容</div>
                        <textarea class="enquire-text" type="text" v-model='form.text' placeholder="20字以上1000字以内で記入してください"></textarea>
                    </div>
                    <div @click="submit()" class="btn-basegra-white-db-sq">送信する</div>
                    <div class="error-container">
                        <div v-if='showError' :class="{'notification-red':showError}">
                            <i class="fas fa-exclamation-triangle"></i>
                            <div v-for="(error,errorindex) in errorArray" 
                                    v-bind:key="errorindex">
                                    <p>{{ error }}</p>
                            </div>
                        </div>
                        <div v-if='created' class="l-wrapper">
                            <div class="l-container">
                                <p class="created-header">問い合わせありがとうございました。</p>
                                <p>内容によっては返信がない<br>場合があります。
                                </p>
                                <div class="button-container">
                                    <div @click="goHome()">ホームに戻る</div>
                                </div>
                            </div>
                        </div>
                        <!-- <div v-if='created' :class="{'notification-blue':created}">
                            <p>送信しました。</p>
                        </div> -->
                    </div>
                </form>
                <div v-if='confirm' class="l-wrapper">
                    <div class="l-container confirm">
                        <p class="confiem-header">以下の内容で問い合わせしますか。</p>
                        <div class="each-container">
                            <p class='each-title'>名前</p>
                            <p class=space>:</p>
                            <p class="content">{{ form.name }}</p>
                        </div>
                        <div class="each-container">
                            <p class='each-title'>メールアドレス</p>
                            <p class=space>:</p>
                            <p class="content">{{ form.mail }}</p>
                        </div>
                        <div class="each-container">
                            <p class='each-title'>問い合わせタイプ</p>
                            <p class=space>:</p>
                            <p class="content">{{ form.type }}</p>
                        </div>
                        <div class="text-container">
                            <p class='text-title'>問い合わせ内容</p>
                            <p class="text-content">{{ form.text }}</p>
                        </div>
                        <!-- <div v-for="(f,formindex) in form" 
                            v-bind:key="formindex">
                            <p>{{ f }}</p>
                        </div> -->
                        <div class="button-container">
                            <div @click="chancelCreate()">キャンセル</div>
                            <div @click="confirmedCreate()">問い合わせる</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {router} from "/src/main.js"

export default {
    data(){
        return{
            alert:false,
            confirm: false,
            showType: false,
            enquireType: [
                '利用規約',
                '個人情報の取り扱い',
                'クイズ',
                'コミュニティ',
                '要望',
                '仕事のお問い合わせ',
                'その他'
            ],
            form:{
                name:'',
                mail:'',
                type:'',
                text:''
            },
            showError: false,
            errorArray:[],
            formError:{
                occurred:false,
                name:'名前を入力してください。',
                longName:'名前は20字以内にしてください。',
                mail:'メールアドレスを入力してください。',
                wrongMail:'正しいアドレスを入力してください。',
                type:'問い合わせタイプを入力してください。',
                text:'問い合わせ内容を入力してください。',
                shortText:'20字以上入力してください。',
                longText:'1000字以内にしてください。'
            },
            created: false,
        }
    },
    beforeUnmount(){
        this.$store.commit('showModalFalse')
        this.resetData()

    },
    methods:{
        async createEnquire() {
            try{
                await axios({
                    method: 'post',
                    url: '/api/enquire/',                            
                    data: {
                        'user_name': this.form.name,
                        'email': this.form.mail,
                        'enquire_type': this.form.type,
                        'enquire_content':this.form.text,
                    },
                })
            } catch(e) {
                console.log('response',e.response.status)
                let logger = {
                    message: this.errorMessage + " enquire" + "couldn't create enquire",
                    path: window.location.pathname,
                    actualErrorName: e.name,
                    actualErrorMessage: e.message,
                }
                this.$store.commit('setLogger',logger)
                this.$store.commit('setIsLoading', false)
                router.push({ name: 'ConnectionError' })
            }
        },
        showTypeHandle() {
            console.log('clicked')
            this.showType = !this.showType
        },
        getSelectType(val){
            this.form.type = val
        },
        submit() {
            console.log(this.form,this.form['name'].length,this.validEmail(this.form['mail']))
            this.errorArray = []
            this.formError.occurred = false
            for(let i of Object.keys(this.form)) {
                console.log(i)
                if(!this.form[i]) {
                    this.errorArray.push(this.formError[i])
                    this.formError.occurred = true
                }
                else if(i == 'text') {
                    if(this.form[i].length < 20) {
                        this.errorArray.push(this.formError["shortText"])
                        this.formError.occurred = true
                    } 
                    else if(this.form[i].length >= 1000) {
                        // this depends on django setting
                        this.errorArray.push(this.formError["LongText"])
                        this.formError.occurred = true

                    }
                }
                else if(i == 'mail') {
                    if(!this.validEmail(this.form[i])) {
                        this.errorArray.push(this.formError["wrongMail"])
                        this.formError.occurred = true
                    }
                }
                else if(i == 'name') {
                    if(this.form[i].length > 20) {
                        console.log('longName')
                        this.errorArray.push(this.formError["longName"])
                        this.formError.occurred = true
                    }
                }

            }
            if(!this.formError.occurred){
                this.confirm = true
                this.$store.commit('showModalTrue')
                // this.setTime(this.createdFalse)
            } else {
                this.showError = true
                this.setTime(this.showErrorFalse)
            }
        },
        validEmail: function (email) {
            var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },
        showErrorFalse(){
            this.showError = false
        },
        confirmedCreate(){
            this.createEnquire()
            console.log('created')
            this.confirm = false
            this.created = true
        },
        chancelCreate() {
            this.confirm = false
        },
        // createdFalse(){
        //     this.created = false
        // },
        setTime(callback){
            setTimeout(callback,3000)
        },
        goHome(){
            router.push("/")
        },
        resetData(){
            this.form.name = ''
            this.form.mail = ''
            this.form.type = ''
            this.form.text = ''
            this.showType = false
            this.showError = false
            this.created = false
            this.formError.occurred = false
        }
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.enquire-wrapper{
    width: 100%;
    display: flex;
    justify-content: center;
    // position: relative;
    .main-wapper{
    }
}
.content-wrapper{
    .title-white{
        margin-bottom: 2rem;
    }
    .enquire-container{
        position: relative;
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 1rem;
        .enquire-title{
            position: absolute;
            left: 0;
            top: 0;
            margin-left: 5%;
            height: 20px;
            color: white;
            font-weight: bold;
            border-bottom: solid $dark-blue;
        }
        .enquire-input{
            width: 90%;
            margin-top: 25px;
            height: 40px;
            padding: 0.3rem;
            font-size: 1.2rem;
            transition: .2s;
        }
        .enquire-input:focus{
            border: solid $base-color;
        }
        .enquire-text{
            width: 90%;
            margin-top: 25px;
            height: 300px;
            padding: 1rem;
            margin-bottom: 1rem;
            resize: none;
            font-size: 1.2rem;
            transition: .2s;

        }
        .enquire-text:focus{
                outline: none;
                border: solid $base-color;
        }
        .enquire-type{
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 90%;
            margin-top: 25px;
            height: 40px;
            padding: 0.3rem;
            font-size: 1.2rem;
            transition: .2s;
            background: white;
            .type-select{
                position: absolute;
                width: 100%;
                min-height: 80px;
                top: 35px;
                background: rgba(252, 252, 252, 0.95);;
                z-index: 1;
                .type{
                    padding: 0.5rem 0;
                    transition: .5s;
                }
                .type:hover{
                    display: block;
                    background: $lite-gray;
                }
                // .type:last-child{
                //     padding-bottom: 0;
                // }
            }
        }
        .fa-angle-down{
            transition: .5s;
        }
        .lotate{
            transform:rotate(180deg);
        }
    }
    .btn-basegra-white-db-sq{
        padding: 0.1rem 0.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .error-container{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        left: 0;
        .notification-red{
            .fa-exclamation-triangle{
                color: red;
            }
            div{
                color: red;
                margin-top: 0.5rem;
                font-weight: bold;
            }
        }
        .l-wrapper{
            z-index: 1; 
        }
        .l-container{
            padding: 1rem;
            font-weight: bold;
            .created-header{
                color: $dull-red;
                margin-bottom: 1rem;
            }
        }
        .button-container div{
            margin-top: 1.5rem;
            padding: 0 1rem;
            border: solid gray;
            display: inline-block;
            transition: .5s;
        }
        .button-container div:hover{
            border: solid $dark-blue;
            color: gray;
        }
        // .notification-blue{
        //     color: blue;
        //     font-weight: bold;
        // }
    }
}
.confirm{
    padding: 1rem;
    .confiem-header{
        font-size: 1.3rem;
        margin: 0.5rem 0;
        color: $dull-red;
    }
    p{
        margin-bottom: 1rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .each-container{
        width: 100%;
        display: flex;
        justify-content: center;
        .each-title{
            flex-basis: 45%;
            width: 50%;
            display: flex;
            justify-content: flex-end;
        }
        .space{
            flex-basis: 5%;
        }
        .content{
            flex-basis: 45%;
            width: 45%;
            display: flex;
        }
    }
    .button-container{
        width: 100%;
        display: flex;
        justify-content: center;
        div{
            margin: 0 0.5rem;
            border: solid gray;
            padding: 0.2rem 0.5rem;
            transition: .5s;
            font-weight: bold;
        }
        div:hover{
            color: gray;
            
        }
        
    }
    .text-container{
        width: 100%;
        display: flex;
        flex-direction: column;
    }
}
</style>