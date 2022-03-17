<template>
    <div  class="board-account-wrapper">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class='main-container' v-if="user">
                <h1 class='title-white'>質問板</h1>
                <div class="user-info">
                    <div class="header">
                        <img class='img' v-bind:src="user.thumbnail"/>
                        <p>{{ user.name}}</p>
                    </div>
                    <div class="content">
                        <div>質問数 {{ user.question.length }}</div>
                        <div>回答数 {{ user.answer.length }}</div>
                        <div>ベストアンサー数 0</div>
                    </div>
                </div>
                <div class="tag-container">
                    <div>関係するタグ</div>
                    <div v-for="(tag,questionindex) in user.user_tag"
                         v-bind:key="questionindex">
                         <!-- do somethig laler -->
                    </div>
                    <p>編集する></p>
                </div>
                <div class="nav-ber">
                    <div>質問</div>
                    <div>回答</div>
                    <div>おすすめ</div>
                    <div>メッセージ</div>
                </div>
                <div class="selecter">
                    <div class="select-item">解決</div>
                    <div class="select-item">未解決</div>
                    <div class="select-item">投票中</div>
                    <div class="select-item">ベスト</div>
                </div>
                <div
                    class='question-container'
                    v-for="(question,questionindex) in user.question"
                    v-bind:key="questionindex">
                    <div class='question-list' @click="getDetail(question.slug)">
                        <div 
                            class="tag-wrapper">
                            <div 
                                class="tag"
                                v-for="(tag,tagindex) in question.tag" 
                                v-bind:key="tagindex">{{ tag.tag }}</div>
                        </div>
                        <div class="question-title">{{ question.title }}</div>
                        <div class="question-description">{{ question.description.substr(0,10)+'...' }}</div>
                        <div class='good-like-wrapper'>
                            <i class="far fa-heart"></i>
                            <div class="good" v-if="question.liked_num[0]">{{ question.liked_num[0].liked_num }}</div>
                            <div class="date">作成日：{{ question.created_on }}</div>
                        </div>
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

        }
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        }
    },
    mounted(){
        console.log('mounted',this.user)
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.board-account-wrapper{
    display: flex;
    justify-content: center;
    width: 100vw;
    min-height: 80vh;
    // align-items: center;
}
.main-container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    .user-info{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 90%;
        padding:0.5rem;
        .header{
            display: flex;
            justify-content: center;
            align-items: center;
            .img{
                border-radius: 50%; 
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            p{
                flex-basis: 70%;
                font-size: 2rem;
                font-weight: bold;
            }
        }
        .content{
            margin-top: 0.5rem;
            width:100%;
            position: relative;
            text-align: left;
        }
    }
    .tag-container{
        margin-top: 1rem;
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 90%;
        padding:0.5rem;
        p{
            text-align: right;
        }
    }
    .nav-ber{
        width:100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        div{
            font-size:0.8rem;
            color: white;
            border:0.1rem solid white;
            position:flex;
            flex-direction: column;
            flex-basis:20%;
            padding-left:0.1rem;
            padding-right:0.1rem;
            padding: 0.2rem;
            background: linear-gradient(rgba(91, 117, 159, 0.9),rgba(28, 37, 76, 0.9));
            transition:0.5s;
        }
    }
    .selecter{
        width:100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        .select-item{
            font-size:0.8rem;
            color: white;
            border:0.1rem solid $base-color;
            border-radius: 1rem;
            margin:0.3rem;
            min-width: 3rem;
            position:flex;
            // flex-basis:20%;
            padding-left:0.1rem;
            padding-right:0.1rem;
            padding: 0.2rem;
            transition:0.5s;
        }
    }
    .question-container{
        width: 90%;
        .question-list{
        border: solid $base-color;
        margin-bottom: 0.5rem;
        width:100%;
        background: rgb(252, 252, 252);
        display: flex;
        flex-direction: column;
        .tag-wrapper{
            display: flex;
            width: 100%;
            .tag{
                border: solid black;
                border-radius: 50vh;
                background: rgb(230, 230, 230);
                margin-top: 0.5rem;
                margin-left: 0.3rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                min-width: 3rem;
            }
        }
        .good-like-wrapper{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.2rem;
            }
            .date{
                margin-left: 0.5rem;
            }
        }
    }
    }
}

</style>