<template>
    <div class="enquire-wrapper">
        <div class="main-wrapper">
            <div class="content-wrapper">
                <div class="title-white">
                    <p>問い合わせ</p>
                </div>
                <div class="enquire-container">
                    <div class="enquire-title">名前</div>
                    <input class="enquire-input" type="text" v-model='form.name'>
                </div>
                <div class="enquire-container">
                    <div class="enquire-title">メールアドレス</div>
                    <input class="enquire-input" type="text" v-model='form.mail'>
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
                    <textarea class="enquire-text" type="text" v-model='form.text'></textarea>
                </div>
                <div @click="submit()" class="btn-basegra-white-db-sq">送信する</div>
                <div class="error-container">
                    <div v-if='formError.occurred' :class="{'notification-red':formError.occurred}">
                        <i class="fas fa-exclamation-triangle"></i>
                        <div v-if='!form.name'>{{ formError.name}}</div>
                        <div v-if='!form.mail'>{{ formError.mail }}</div>
                        <div v-if='!form.type'>{{ formError.type}}</div>
                        <div v-if='!form.text'>{{ formError.text }}</div>
                        <div v-if='form.text.length < 20 &&form.text'>{{ formError.lessText }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            description:'',
            alert:false,
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
            formError:{
                occurred:false,
                name:'名前を入力してください。',
                mail:'メールアドレスを入力してください。',
                wrongMail:'正しいアドレスを入力してください。',
                type:'問い合わせタイプを入力してください。',
                text:'問い合わせ内容を入力してください。',
                lessText:'20字以上入力してください。'
            }
        }
    },
    methods:{
        showTypeHandle() {
            console.log('clicked')
            this.showType = !this.showType
        },
        getSelectType(val){
            this.form.type = val
        },
        submit() {
            for(let i of Object.keys(this.form)) {
                console.log(i)
                if(i == 'text') {
                    if(this.form[i].length < 20) {
                        this.formError.occurred = true
                        this.setTime()
                        break
                    }
                }
                // else if(i == 'mail') {
                //     if(this.form[i].search(/'@'/)==-1) {
                //         console.log('not@')
                //         this.formError.occurred = true
                //         this.setTime()
                //         break
                //     }
                // }
                else if(!this.form[i]) {
                    this.formError.occurred = true
                    this.setTime()
                    break
                } else {
                    this.formError.occurred = false
                }
            }
            console.log(this.form,this.form.text.length)
        },
        formErrorFalse(){
            this.formError.occurred = false
        },
        setTime(){
            setTimeout(this.formErrorFalse,3000)
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
    position: relative;
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
    }
}
</style>