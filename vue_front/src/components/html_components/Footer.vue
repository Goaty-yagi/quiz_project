<template>
    <footer class="footer-wrapper">
        <router-link class="img" to="/" >
            <img src="@/assets/logo.png">
        </router-link>
        <div class="footer-container">
            <div class="footer-contents"
            v-for="(contents,key,index) in footerContents"
            v-bind:key="index">
                <div class="content-box">
                    <div class="content-title" >
                        {{key}}
                    </div>
                    <div class="content-loop"
                    v-for="(content,key,contentIndex) in contents"
                    v-bind:key="contentIndex">
                        {{ content }}
                    </div>
                </div>                
            </div>
        </div>
        <div class="social-link">
            <div class="space">
            </div>
            <img @click="twitter" class="social-img" src="@/assets/twitter.png">
        </div>
        <p class="copy-right">Copyright (c) 2022</p>
    </footer>
</template>

<script>
import {router} from "/src/main.js"
export default {
    data(){
        return{
            tweetUrl:'',
            footerContents:{
                'ガイドとヘルプ':[
                    'About',
                    '利用規約',
                    'ガイドライン',
                    '問い合わせ',
                    'ヘルプ'
                ],
                'コンテンツ':[
                    'Quiz',
                    'Community'
                ],
                '運営':[
                    '運営会社'
                ]
            }
        }
    },
    methods:{
        twitter(){
            var shareURL = 'https://twitter.com/intent/tweet?text=' + "ねこJapanese" + "%20%23ねこサンプルコード集" + '&url=' + "URL";  
            window.open(shareURL)
        },
    },
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.footer-wrapper{
    background-color: transparent;
    background-image: none;
    border-top: solid $dark-blue;
    height: 10rem;
    position: relative;
    .img{
        position: absolute;
        flex-basis: 50%;
        display: flex;
        img{
            width: 5rem;
            height: 5rem;
            margin-left: 1rem;
        }
    }
    .footer-container{
        display: flex;
        justify-content: flex-end;
        margin-right: 2rem;
        .footer-contents{
            display: flex;
            justify-content: flex-end;
            .content-box{
                margin-top: 1rem;
                margin-right: 0.5rem;
                margin-left: 0.5rem;
                .content-title{
                    color: $base-white;
                    font-weight: bold;
                    font-size: 1.2rem;
                    border-bottom: solid gray;
                }
                .content-loop{
                        color: $base-white;
                        margin-top: 0.5rem;
                    }
             }
         }
    }
    .copy-right{
        color: $base-white;
        padding: 1rem;
        
    }
    .social-link{
        .social-img{
            width: 3rem;
            transition: .5s;
        }
        .social-img:hover{
            box-shadow: 0.5px 0.5px 10px 2.5px #cbfaed;
            border-radius: 7px;
        }
    }
}
@media(max-width: 480px){
    .footer-wrapper{
        // display: flex;
        // flex-direction: column;
        // justify-content: center;
        .img{
            position: absolute;
            flex-basis: 50%;
            display: flex;
            img{
                width: 5rem;
                height: 5rem;
                margin-left: 1rem;
            }
        }
        .footer-container{
            display: flex;
            justify-content: center;
            flex-direction: column;
            width: 100%;
            .footer-contents{
                display: flex;
                justify-content: center;
                .content-box{
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    .content-title{
                        color: $base-white;
                        font-weight: bold;
                        font-size: 1.2rem;
                        border-bottom: solid gray;
                    }
                    .content-loop{
                            color: $base-white;
                            margin-top: 0.5rem;
                        }
                }
            }
        }
        .copy-right{
            color: $base-white;
            margin-top: 1rem;
            padding: 4rem;
            
        }
    }
}
</style>