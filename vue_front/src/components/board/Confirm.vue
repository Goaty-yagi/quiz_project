<template>
    <div class="l-wrapper">
        <div class="main-wrapper">
            <div class="create-question-wrapper">
                <div class="title-black">
                    <p>質問投稿</p>
                </div>
                <div class="form">
                    <div class="question-title-container">
                        <div class='title-flex'>
                            <p>TITLE</p>
                        </div>
                        <div class="question-title">
                            <p> {{ $store.state.title }} </p>
                        </div>
                        <!-- <input class='question-title' type="text" v-model='title' :placeholder="$store.state.title"> -->
                    </div>

                    <div class="line"></div>

                    <div class="question-description">
                        <p class="title-black">質問文</p>
                    </div>
                    <div class='text-field'>
                        <div class='form-text'>
                            {{ $store.state.description }}
                        </div>
                    </div>
                    <div class='confirm-message'>この内容で投稿しますか。
                    </div>
                    <div class="button-group">
                            <div @click="this.$emit('handleShowConfirm')">戻る</div>
                            <button class="btn-tr-black-base-sq" @click='publish'>投稿する</button>
                    </div>            
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { uuid } from 'vue-uuid';
export default {
    data(){
        return{
            title: '',
            discription:'',
            uuid:uuid.v1(),
        }
    },
    mounted(){
        this.title=this.$store.state.title
    },
    methods:{
        async publish(){
            console.log('start add','uuid',this.uuid)
            await axios({
                method: 'post',
                url: '/api/board/question/create',
                data: {
                    title: this.$store.state.title,
                    description: this.$store.state.description,
                    user: this.$store.state.signup.user.uid,
                    slug: this.uuid
                },
                
            })
            // this.$emit('handleNotifications')
            this.$emit('getDetail',this.uuid)
            // this.$emit('handleShowConfirm')
            // this.$router.go({path: this.$router.currentRoute.path, force: true})
        }
        //     axios.post(
        //         '/api/forum/question/',
        //         {title: this.$store.state.title, 
        //         description: this.$store.state.description
        //         },
        //     ).then(response => {
        //         console.log(response)
        //     })
        // },
        // addQuestion(){
        //     console.log('start add')
        //     axios({
        //         method: 'post',
        //         url: '/api/forum/question',
        //         data: {
        //             title: this.$store.state.title,
        //             description: this.$store.state.description
        //         },
        //     })
        // .then((response) =>{
            
        // }

        // )
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
.l-wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
    .create-question-wrapper{
        top:0;
        left:0;
        background: $back-tr-white;
        border: solid $dark-blue;
        width:100%;
        height: auto;
        flex-direction: column;
        display: flex;
        // justify-content: center;
        align-items: center;
        padding: 1.5rem;
        .form{
            width: 100%;
            display: flex;
            flex-direction: column;
            // justify-content: center;
            align-items: center;
            .question-title-container{
                width:90%;
                display: flex;
                flex-direction: column;
                align-items: center;
                .title-flex{
                    display: flex;
                    width: 90%;
                }
                .question-title{
                    display: flex;
                    align-items: center;
                    border: solid $base-color;
                    width: 90%;
                    height: 2.5rem;
                    background: $back-white;
                    padding-left: 0.5rem;
                    text-align: left;
                    font-size: 0.8rem;            
                }
            }
            .line{
                width: 80%;
                border-bottom: 0.2rem solid $dark-blue;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
            .question-description{
                .title-black{
                    margin: 0;
                }
            }
            .text-field{
                width:80%;
                // overflow-y: scroll;
                .form-text{
                    text-align: left;
                    height: 200px;
                    width: 100%;
                    background: $back-white;
                    min-height: 100px;
                    border: 0.1rem solid $base-color;
                    border-radius: 1vh;
                    padding: 1rem;
                    white-space: pre-wrap;
                    overflow-y: scroll;
                }
                .form-text:focus{
                    outline: none;
                }
            }
            .confirm-message{
                margin-top: 1rem;
                color: red;
                font-weight: bold;
            }
            .button-group{
                width: 80%;
                display:flex;
                margin:1rem;
                justify-content: center;
                .btn-tr-black-base-sq{
                    margin-left: 0.5rem;
                    padding-right: 0.5rem;
                    padding-left: 0.5rem;
                }
            }
        }   
    }
}
</style>