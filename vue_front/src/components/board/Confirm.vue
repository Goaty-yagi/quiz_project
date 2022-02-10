<template>
    <div class="create-question-wrapper">
        <div class="title">
            <p>質問投稿</p>
        </div>
        <form class="form" @submit.prevent='submitForm'>
            <div class="question-title-container">
                <p>タイトル</p>
                {{ title }}
            </div>
            <input class='question-title' type="text" v-model='title' :placeholder="$store.state.title">
            <div class="question-description">
                <p>質問文</p>
                {{ discription }}
            </div>
            <input class='form-text' type="text" v-model='discription' :placeholder="$store.state.description">
        </form>
        <div class="image">
            <i class="fas fa-camera"></i>
            <p>写真を添付</p>
        </div>
        <div class="button-group">
            <p>キャンセル</p>
            <button @click='publish'>投稿する</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data(){
        return{
            title: '',
            discription:'',
        }
    },
    mounted(){
        this.title=this.$store.state.title
    },
    methods:{
        publish(){
            console.log('start add')
            axios({
                method: 'post',
                url: '/api/board/question/',
                data: {
                    title: this.$store.state.title,
                    description: this.$store.state.description,
                    user: this.$store.state.signup.user.uid,
                },
                
            })
            this.$router.go({path: this.$router.currentRoute.path, force: true})
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
    .create-question-wrapper{
        top:0;
        position: fixed;
        background: linear-gradient(#5B759F,#1C254C);
        width:100vw;
        height:100vh;
        flex-direction: column;
        display: flex;
        // justify-content: center;
        align-items: center;       
    }
    .title{
        color:white;
        margin-top: 5rem;
        border-bottom: solid rgb(5, 5, 105);

    }
    .question-description{
        color: white;
    }
    .form{
        width: inherit;
        // height: inherit;
    }
    .form-text{
        width: 80%;
        height:10rem;
        border: 0.1rem solid $base-color;
        border-radius: 1vh;
        // text-align:left;
    }
    .image{
        display:flex;
        align-items: left;  
        margin:1rem;
    }
    .button-group{
        display:flex;
        align-items: left;  
        margin:1rem;
    }
</style>