<template>
    <div  class="board-account-wrapper">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': user==false}">
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
                    <div v-for="(tag,questionindex) in handleQuestion"
                         v-bind:key="questionindex">
                         <!-- do somethig laler -->
                    </div>
                    <p>編集する></p>
                </div>
                <div class="nav-ber">
                    <div :class="{'selected': showQuestion.questionType.question}" @click="handleQuestionType('question')">質問</div>
                    <div :class="{'selected': showQuestion.questionType.answered}" @click="handleQuestionType('answered')">回答</div>
                    <div :class="{'selected': showQuestion.questionType.reccomend}" @click="handleQuestionType('reccomend')">おすすめ</div>
                    <div :class="{'selected': showQuestion.questionType.favorite}">お気に入り</div>
                    <div :class="{'selected': showQuestion.questionType.message}">メッセージ</div>
                </div>
                <div class="selecter">
                    <div :class="{'option-selected': showQuestion.questionStatus.all}" @click="handleQuestionStatus('all')" class="select-item">ALL</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.solved}" @click="handleQuestionStatus('solved')" class="select-item">解決</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.unsolved}" @click="handleQuestionStatus('unsolved')" class="select-item">未解決</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.onVoting}" @click="handleQuestionStatus('onVoting')" class="select-item">投票中</div>
                    <div v-if="showQuestion.questionType.answered" :class="{'option-selected': showQuestion.questionStatus.best}" @click="handleQuestionStatus('best')" class="select-item">ベスト</div>
                </div>
                <div
                    class='question-container'
                    v-for="(question,questionindex) in handleQuestion"
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
                        <!-- <div class="question-description">{{ question.description.substr(0,10)+'...' }}</div> -->
                        <div class='good-like-wrapper'>
                            <i class="far fa-heart"></i>
                            <!-- <div class="good" v-if="question.liked_num[0]">{{ question.liked_num[0].liked_num }}</div> -->
                            <div class="date">作成日：{{ question.created_on }}</div>
                        </div>
                    </div>   
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "/src/main.js"
export default {
    data(){
        return{
            showQuestion:{
                reccomendedQuestion:'',
                questionType:{
                    question: true,
                    answered: false,
                    reccomend: false,
                    favorite: false,
                    message:false
                    },
                questionStatus:{
                    all: true,
                    solved: false,
                    unsolved: false,
                    onVoting: false,
                    best: false,
                }
            }
        }
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        handleQuestion(){
            const handledQuestion= []
            console.log("questiontype",this.showQuestion.questionType)
            if(this.showQuestion.questionType.question){
                return this.handleStatus(this.user.question)
            }
            else if(this.showQuestion.questionType.answered){
                const answeredquiz = []
                console.log("in_quiz",this.showQuestion.questionStatus.best )
                if(this.showQuestion.questionStatus.best){
                    console.log('make_best_answered')
                    Object.values(this.user.answer).forEach(value =>{
                        console.log("loop",value)
                        if(value.best == true){
                            answeredquiz.push(value.question)}
                    })
                    console.log(answeredquiz)
                    return answeredquiz
                }
                else{
                    console.log('answered',this.user.answer)
                    Object.values(this.user.answer).forEach(value =>{
                        answeredquiz.push(value.question)
                    })
                    return this.handleStatus(answeredquiz)   
                }
            }else if(this.showQuestion.questionType.reccomend){
                return this.handleStatus(this.$store.state.board.reccomendedQuestion)
            }
        },
    },
    mounted(){
        console.log('mounted',this.user)
        this.reccomendedQuestion = this.$store.dispatch('getRelatedQuestion')
        console.log('mounted',this.reccomendedQuestion)
    },
    methods:{
        getDetail(slug){
            router.push(`/board-detail/${slug}` )
        },
        handleStatus(question){
            console.log("handle",question)
            const handledQuestion= []
            if(this.showQuestion.questionStatus.all){
                console.log('just_return__dayo')
                    return question
                }
                else if(this.showQuestion.questionStatus.solved){
                    console.log('solved_dayo')
                    for(let i of question){
                        if(i.solved){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                }else if(this.showQuestion.questionStatus.unsolved){
                    for(let i of question){
                        console.log(i.title)
                        if(i.solved==false){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                }else if(this.showQuestion.questionStatus.onVoting){
                    console.log('on_going_dayo')
                    for(let i of question){
                        if(i.vote_on_going==true){
                            handledQuestion.push(i)
                        }
                    }
                    return handledQuestion
                }
        },
        // handleQuestion(){
        //     if(this.showQuestion.questionType.question){
        //         // console.log("return_recen:",this.questions)
        //         return this.user.questions
        //     }
        //     else if(this.showQuestion.questionType.answered){
        //         // console.log("return_reco:",this.reccomendedQuestion)
        //         return this.user.answer.question
        //     }
        // },
        handleQuestionStatus(status){
            // handle questionStatus start from here by click.
            // change all status = false then invocation = true
            // then handleQuestion on computed will be triggered
            // which make question from answer to return question to handleStatus
            console.log('status',status)
            if(this.showQuestion.questionStatus[status]){
                console.log('same')
                ;
            }
            else{
                console.log('not the same')
                Object.keys(this.showQuestion.questionStatus).forEach(key =>{
                    this.showQuestion.questionStatus[key] = false
                })
                this.showQuestion.questionStatus[status] = true
                console.log(this.showQuestion.questionStatus)
            }
        },
        handleQuestionType(type){
            if(this.showQuestion.questionType[type]){
                console.log('same')
                ;
            }
            else{
                console.log('not the same')
                Object.keys(this.showQuestion.questionType).forEach(key =>{
                    this.showQuestion.questionType[key] = false
                })
                this.showQuestion.questionType[type] = true
            }
            // if(type == question){
                
                // }
                // for(let i=0; i<Object.keys(this.showQuestion.questionType.length); i++){

                // }
            
        }
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
        .selected{
            background: $base-color;
            font-weight: bold;
            color: black;
        }
    }
    .selecter{
        width:100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        transition: 0.5s;
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
        .option-selected{
            color: black;
            font-weight: bold;
            background: $base-lite;
            border:0.1rem solid $dark-blue;
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