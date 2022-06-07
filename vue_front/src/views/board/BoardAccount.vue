<template>
    <div  class="board-account-wrapper scroll_area" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading}">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div v-if="$store.state.isLoading==false" class='main-container'>
                <div v-if="onNotification.show" :class="{'notification-blue':onNotification.show}">
                    <div class="notification-text" v-if="onNotification.onAnswer">
                        新しい回答があります。
                    </div>
                    <div class="notification-text" v-if="onNotification.onReply">
                        新しい返信があります。
                    </div>
                </div>
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
                    <div class="tag-text">関連するタグ</div>
                    <div class="tag-wrapper">
                        <div v-if="!getThreeUsertag">
                            <p>現在表示できるタグはありません。</p>
                        </div>
                        <div 
                            @click="handleTag(questionindex,tag.tag.id,'tag')"
                            class="tag"
                            :class="{'animation-tag':active==questionindex}" 
                            v-for="(tag,questionindex) in getThreeUsertag"
                            v-bind:key="questionindex"
                            >
                            {{ tag.tag.tag }}
                        </div>
                        
                    </div>
                        <!-- <p>編集する></p> -->
                </div>
                <div class="nav-ber" v-if="tag==false">
                    <div :class="{'selected': showQuestion.questionType.question}" @click="handleQuestionType('question')">質問</div>
                    <div :class="{'selected': showQuestion.questionType.answered}" @click="handleQuestionType('answered')">回答</div>
                    <div :class="{'selected': showQuestion.questionType.reccomend}" @click="handleQuestionType('reccomend')">おすすめ</div>
                    <div :class="{'selected': showQuestion.questionType.favorite}" @click="handleQuestionType('favorite')">お気に入り</div>
                    <!-- <div :class="{'selected': showQuestion.questionType.message}">メッセージ</div> -->
                </div>
                <div class="selecter">
                    <div :class="{'option-selected': showQuestion.questionStatus.all}" @click="handleQuestionStatus('all')" class="select-item">ALL</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.solved}" @click="handleQuestionStatus('solved')" class="select-item">解決</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.unsolved}" @click="handleQuestionStatus('unsolved')" class="select-item">未解決</div>
                    <div :class="{'option-selected': showQuestion.questionStatus.onVoting}" @click="handleQuestionStatus('onVoting')" class="select-item">投票中</div>
                    <div v-if="showQuestion.questionType.answered" :class="{'option-selected': showQuestion.questionStatus.best}" @click="handleQuestionStatus('best')" class="select-item">ベスト</div>
                </div>
                <div class="is-loading-bar has-text-centered middle-loading" v-bind:class="{'is-loading': spinner }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class="no-question" v-if="!handleQuestion[0]&&tag==false">
                <div v-if="showQuestion.questionType.question">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">質問をするとここに表示されます。</p>
                </div>
                <div v-if="showQuestion.questionType.answered">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">質問に回答するとここに表示されます。</p>
                </div>
                <div v-if="showQuestion.questionType.favorite">
                    <p>表示できる質問はありません。</p>
                    <p v-if="showQuestion.questionStatus.all">お気に入りに登録するとここに表示されます。</p>
                </div>
            </div>
                <div
                    class='question-container'
                    v-for="(question,questionindex) in handleQuestion"
                    v-bind:key="questionindex">
                    
                    <div class='question-list' v-if="spinner==false" @click="getDetail(question.slug)">
                        <div class="tag-wrapper">
                            <div 
                                class="tag"
                                v-for="(tag,tagindex) in question.tag" 
                                v-bind:key="tagindex">{{ tag.tag }}
                            </div>
                            <div class="on-answer-wrapper">
                                <div class="on-answer" v-if="handleOnAnswer(question)||handleOnReply2(question)">
                                        <div class="on-answer-container" v-if="handleOnAnswer(question)">
                                            <span class="span1"> NEW</span><span class="span2">ANSWER</span>
                                        </div>
                                        <div class="on-answer-container" v-if="handleOnReply2(question)">
                                            <span class="span1"> NEW</span><span class="span2">Reply</span>
                                        </div>
                                </div>
                                <div class="on-answer" v-if="onReplayCheck(question.answer)">
                                    <div class="on-answer-container">
                                        <span class="span1"> NEW</span><span class="span2">REPLY</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="question-title">{{ question.title }}</div>
                        <div class="question-description" v-if="question.description">{{ question.description.substr(0,10)+'...' }}</div>
                        <div class='good-like-wrapper'>
                            <i class="far fa-heart"></i>
                            <div class="good" v-if="question">{{ viewedNum(question.liked_num) }}</div>
                            <div class="date">作成日：{{ dateConvert(question.created_on) }}</div>
                        </div>
                    </div>   
                </div>
                <!-- v-if="scrollBottom&&questions.next" -->
                <div v-if="questions.next&&scrollBottom" class="question-list-dammy shine">
                    <div class="tag-wrapper-dammy">
                        <div class="tag-dammy"></div>
                    </div>
                    <div class="question-title-dammy"></div>
                    <div class="questiondescroption-dammy"></div>
                    <div class="footer-dammy"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {router} from "/src/main.js"
import axios from 'axios'
export default {
    data(){
        return{
            questions:'',
            reccomendedQuestion:'',
            answeredQuestion:'',
            userQuestion:'',
            tagQuestion:'',
            bottomScrollActionHandler: true,
            scrollBottom: false,
            tag:false,
            active: null,
            spinner:false,
            showOnes:false,
            onNotification:{
                onReply:false,
                onAnswer:false,
                show: false
            },
            showNotifications: false,
            temporaryStatus:'',
            showQuestion:{
                questionType:{
                    question: true,
                    answered: false,
                    reccomend: false,
                    favorite: false,
                    tag:false,

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
    watch:{
        showOnes:function(v) {if (v == true){
            console.log('go set',this.showOnes)
            this.setTime()
        }}
    },
    computed:{
        user(){
            return this.$store.getters.getDjangouser
        },
        // notifications(){
        //     return this.$store.getters.notifications
        // },
        getThreeUsertag(){
            const _ = require('lodash');
            let used_num_list = []
            let userTag = _.cloneDeep(this.user.user_tag)
            console.log('UT',userTag)
            if(userTag){
                if(userTag.length == 1){
                    return userTag
                }
                else if(userTag.length == 2){
                    
                    used_num_list.push(userTag.reduce((a,b)=>a.used_num>b.used_num?a:b))
                    used_num_list.push(userTag.reduce((a,b)=>a.used_num<b.used_num?a:b))
                    if(used_num_list[0].id == used_num_list[1].id){
                        return userTag
                    }
                    else{
                        return used_num_list
                    }
                }
                else if(userTag.length >= 3){
                    while (used_num_list.length < 3){
                        used_num_list.push(userTag.reduce((a,b)=>a.used_num>b.used_num?a:b))
                        Object.values(userTag).forEach(value =>{
                            if(value.id == used_num_list.slice(-1)[0].id)                   
                                delete userTag[userTag.indexOf(value)]
                        })
                    }
                    return used_num_list
                }
            }else{
                
            }
            // console.log("GT",this.user.user_tag.reduce((a,b)=>a.used_num>b.used_num?a:b));
            // let used_num_temp_list = []
            // let used_num_list = []
            // let counter = 0
            // for(let i of this.user.user_tag){
            //     if(counter == 0){
            //         used_num_temp_list.push(i)
            //         counter += 1
            //     }else{

            //     }
            // }
        },
        getAnsweredQuestion(){
            console.log("getdazeAQ")
            return this.$store.getters.gettersAnsweredQuestions
        },
        handleQuestion(){
            const handledQuestion= []
            console.log("questiontype",this.showQuestion.questionType)
            if(this.showQuestion.questionType.question){
                try{
                    this.questions = this.userQuestion
                    console.log("UQR",this.questions.results)
                    return this.handleStatus(this.HandleQuestionOnanswerOrder(this.questions.results))
                }catch{
                }
            }
            else if(this.showQuestion.questionType.answered){
                const answeredquiz = []
                console.log('AQ',this.getAnsweredQuestion)
                this.questions = this.getAnsweredQuestion
                console.log("best",this.showQuestion.questionStatus.best)
                if(this.showQuestion.questionStatus.best){
                    Object.values(this.questions.results).forEach(value =>{
                        console.log("loop",value.answer)
                        for(let answer of value.answer){
                            if(answer.best==true&&answer.user.UID==this.user.UID){
                                answeredquiz.push(value)
                            }
                        }
                    })
                    console.log("best list",answeredquiz)
                    return answeredquiz
                }
                else{
                    console.log("not best")
                    var answeredquiz2 = []
                    // for(let i of this.answeredQuestion){
                        Object.values(this.questions.results).forEach(value =>{
                            console.log("value",value.answer)
                            if(value.answer[0].on_reply==true&&value.answer[0].user.UID==this.user.UID){
                                answeredquiz.push(value)
                            }else{
                                answeredquiz2.push(value)
                            }
                        })
                        console.log(answeredquiz,answeredquiz2)
                        if(answeredquiz){
                            for(let i of answeredquiz2){
                                answeredquiz.push(i)
                            }
                            return this.handleStatus(answeredquiz)
                        }
                    return this.handleStatus(this.getAnsweredQuestion.results)   
                }
            }else if(this.showQuestion.questionType.reccomend){
                this.questions = this.$store.state.board.reccomendedQuestion
                return this.handleStatus(this.questions.results)
            }else if(this.showQuestion.questionType.favorite){
                if(this.$store.state.signup.favoriteQuestion){
                     this.questions = this.$store.state.signup.favoriteQuestion
                    return this.handleStatus(this.questions.results)
                }else{
                    this.questions = ''
                    return this.handleStatus(this.questions)
                }
            }else if(this.showQuestion.questionType.tag){
                this.questions = this.tagQuestion
                return this.handleStatus(this.questions.results)
            }
            
        },
    },
    beforeMount(){
        console.log("beforeMounted")
        this.getUserQuestion()
        this.scrollTop()
        this.$store.dispatch("getAnsweredQuestion")
        this.$store.dispatch("getFavoriteQuestion")
    },
    mounted(){
        console.log('THREE',this.getThreeUsertag)
        console.log('mounted')
        this.getUserQuestion()
        window.addEventListener('scroll', this.handleScroll)
        window.addEventListener('scroll', this.getScrollY)
        this.bottomScrollActionHandler = true
        this.scrollBottom = false, 
        this.handleOnReply()
        this.$store.dispatch('getRelatedQuestion')
        this.reccomendedQuestion = this.$store.state.board.reccomendedQuestion
        // this.setTime()
    },
    beforeUnmount(){
        window.removeEventListener('scroll', this.handleScroll)
        window.removeEventListener('scroll', this.getScrollY)
    },
    methods:{
        getDetail(slug){
            router.push(`/board-detail/${slug}` )
        },
        async getAdditionalQuestion(next){
            console.log("addQ",next)
            if(next!=null){
                await axios
                .get(next)
                .then(response => {
                    for(let i of response.data.results){
                        this.questions.results.push(i)
                    }
                    this.questions.next= response.data.next
                    this.bottomScrollActionHandler = true
                    if(this.questions.next==null){
                        this.bottomScrollActionHandler = false
                        this.scrollBottom = false
                        // window.removeEventListener('scroll', this.handleScroll)
                        // window.removeEventListener('scroll', this.getScrollY)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        async getUserQuestion(){
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/board/question-user-question?uid=${this.user.UID}`)
                .then(response => {
                    this.userQuestion = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async getTagQuestion(tagID, tag){
            this.spinner = true
            await axios
                .get(`/api/board/tag-question?tag=${tagID}`)
                .then(response => {
                    this.tagQuestion = response.data
                    console.log("GTQ",this.tagQuestion,tagID,tag)
                    this.handleQuestionType(tag)
                })
                .catch(error => {
                    console.log(error)
                })
            this.spinner = false
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
        HandleQuestionOnanswerOrder(question){
            const questionList = []
            var questionList2 = []
            for(let i of question){
                if(i.on_answer==true){
                    questionList.push(i)
                }else{
                    questionList2.push(i)
                }
            }
            if(questionList){
                for(let o of questionList2){
                    questionList.push(o)
                }
                return questionList
            }
            return question

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
                this.scrollTop()
            }
        },
        handleQuestionType(type){
            console.log('got type', type)
            this.bottomScrollActionHandler = true
            if(this.showQuestion.questionType[type]){
                console.log('same',this.showQuestion.questionType)
                ;
            }
            else{
                console.log('not the same')
                Object.keys(this.showQuestion.questionType).forEach(key =>{
                    this.showQuestion.questionType[key] = false
                })
                this.showQuestion.questionType[type] = true
                console.log('after true',this.showQuestion.questionType)
                this.scrollTop()
                if(this.showQuestion.questionStatus.best==true){
                    this.showQuestion.questionStatus.best==false
                    this.handleQuestionStatus('all')
                }
            }
            // if(type == question){
                
                // }
                // for(let i=0; i<Object.keys(this.showQuestion.questionType.length); i++){

                // }
            
        },
        resetNotifications(){
            this.onNotification.show = false
            console.log('reset is done',this.onNotification.showReplyNotify)
        },
        setTime(){
            console.log('insettime')
            if(this.onNotification.onReply||this.onNotification.onAnswer){
                this.onNotification.show = true
                setTimeout(this.resetNotifications, 4500) 
            }
        },
        handleOnReply(){
            try{
                console.log("handleOnREPLY", this.getAnsweredQuestion)
                for(let question of this.getAnsweredQuestion.results){
                    console.log("first loop",question.answer)
                    for(let answer of question.answer){
                        console.log("second loop",answer)
                        if(answer.on_reply==true&&answer.user.UID==this.user.UID){
                            this.onNotification.onReply = true
                            this.showOnes = true
                        }
                    }
                }
                console.log("end")
            }
            catch{

            }
        },
        handleOnAnswer(question){
            if(question.on_answer&&question.user.UID==this.user.UID){
                this.onNotification.onAnswer = true
                this.showOnes = true
                return true      
            }else{
                return false
            }
        },
        handleOnReply2(question){
            if(question.on_reply&&question.user.UID==this.user.UID){
                this.onNotification.onReply = true
                this.showOnes = true
                return true      
            }else{
                return false
            }
        },
        onReplayCheck(questionAnswer){
            for(let answer of questionAnswer){
                if(answer.on_reply==true){
                    if(answer.user.UID==this.user.UID){
                        this.showOnes = true
                    return true
                    }
                }
            }
            return false
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        },
        getScrollY(){
            this.scrollY = window.scrollY
        },
        handleScroll(){
            console.log("inSCROLL")
            var doch = document.querySelector('.scroll_area').scrollHeight
            var winh = window.innerHeight; //ウィンドウの高さ
            var bottom = doch - winh; //ページ全体の高さ - ウィンドウの高さ = ページの最下部位置
            console.log("inSCROLL2","doch",doch,"winh",winh,'bottom',bottom,'scTOP',this.scrollY,this.bottomScrollActionHandler)
            if (bottom+100 <= this.scrollY&&this.bottomScrollActionHandler) {
                this.bottomScrollActionHandler = false
                this.scrollBottom = true
                console.log("shitadayo",this.scrollBottom,this.questions.next)
                this.getAdditionalQuestion(this.questions.next)
                // if(this.next==null){
                //     this.scrollBottom = false
                // }
            }
        },
        handleTag(indexNum, tagID, tag){
            this.tag = !this.tag
            console.log('inHT',this.showQuestion.questionType)
            if(this.showQuestion.questionType.tag == false){
                for(let i of Object.keys(this.showQuestion.questionType)){
                    if(this.showQuestion.questionType[i]==true){
                        this.temporaryStatus = i
                        console.log('TMK',this.temporaryStatus)
                    }
                }
            }
            console.log('TMK2',this.temporaryStatus)
            if(this.active == indexNum){
                this.active = null
                this.tag = false
                this.showQuestion.questionType.tag = false
                console.log("before",this.showQuestion.questionType,this.temporaryStatus)
                this.handleQuestionType(this.temporaryStatus)
            }else{
                this.active = indexNum
                this.tag = true
                this.getTagQuestion(tagID, tag)
            }
        },
        dateConvert(date){
            var date = date
            var time = ''
            var newDate = ''
            var dt = new Date(date)
            if(dt.getHours() > 11){
                time = " PM"
                dt = dt.setHours(dt.getHours()-12)
                date = new Date(dt)
            }else{
                time = " AM"
            }
            newDate = date + time + " UTC"
            dt = new Date(newDate)
            var stringDT = dt.toLocaleString([], {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'})
            return stringDT.replace(/\//g,'-')
        },
        viewedNum(likedNum){
            console.log('in_liked',likedNum)
            try{
                if(likedNum){
                    return likedNum[0].liked_num
                }
                else{
                    return 0
                }
            }
            catch{
                return 0
            }
        }
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";

.animation-tag{
    color: white;
    background: $dark-blue;
    animation-name: tag;
    animation-timing-function:linear;
    animation-duration:1s;
    animation-iteration-count:1;
    animation:tag  forwards;
}
@keyframes tag {
  from   { opacity: 1;
        } 
  100% { 
      color:white;
      background: $dark-blue;
      border: 0.1rem solid $base-color;
      
  }
}

.board-account-wrapper{
    display: flex;
    height: auto;
    min-height: 80vh;
    width: 100vw;
    margin-bottom: 1rem;
    flex-direction: column;
    align-items: center;
}
.main-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    .notification-blue{
        display: flex;
        display: flex;
        flex-direction: column;
        .notification-text{
            margin-top: 1rem;
        }
    }
    
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
        .tag-text{
            font-size: 1.2rem;
            margin: 0.5rem;
        }
        .tag-wrapper{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
            .tag{
                border: solid $dark-blue;
                border-radius: 50vh;
                background: $base-lite-2;
                margin-top: 0.5rem;
                margin-left: 0.5rem;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                min-width: 5rem;
                font-size: 1rem;
                font-weight: bold;
                color:$dark-blue;
                transition: 0.5s;
            }
            .tag:hover{
                color: gray
            }
        }
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
        div:hover{
            font-weight: bold;
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
        .select-item:hover{
            font-weight: bold;
        }
        .option-selected{
            color: black;
            font-weight: bold;
            background: $base-lite;
            border:0.1rem solid $dark-blue;
        }
    }
    .middle-loading{
        margin-top: 2rem;
    }
    .question-container{
        width: 90%;
        .question-list:hover{
            background: $base-lite-3;
        }
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
                .on-answer-wrapper{
                    position:relative;
                    width:100%;
                    .on-answer{
                        position: absolute;
                        right: 0;
                        flex-direction: column;
                        width:3.7rem;
                        margin-top: 0.5rem;
                        margin-right: 0.3rem;
                        padding-right:0.2rem;
                        padding-left:0.2rem; 
                        .on-answer-container{
                            display: flex;
                            flex-direction: column;
                            color: red;
                            border: solid red;
                            border-radius: 0.5rem;
                            margin-bottom: 0.3rem;     
                        }
                        .span1{
                            font-weight: bold;
                        }
                        .span2{
                            margin-top: -0.5rem;
                            font-size: 0.6rem;
                            font-weight: bold;             
                        }
                    }
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
    .question-list-dammy{
        background: gray;
        display: flex;
        width: 90%;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        .tag-wrapper-dammy{
            display: flex;
            width: 100%;
            .tag-dammy{
                border-radius: 50vh;
                background: rgb(92, 92, 92);
                margin-top: 0.5rem;
                margin-left: 0.3rem;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                min-width: 3rem;
                min-height: 1.5rem;
            }
        }
        .question-title-dammy{
            background: rgb(92, 92, 92);
            padding: 0.5rem;
            width: 80%;
        }
        .questiondescroption-dammy{
            background: rgb(92, 92, 92);
            padding: 0.5rem;
            width: 80%;
            margin-top: 0.5rem;
        }
        .footer-dammy{
            background: rgb(92, 92, 92);
            padding: 0.5rem;
            width: 80%;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }
    }
}
.no-question{
    border: solid $dull-red;
    background: $back-gra-white;
    width: 80%;
    padding: 1rem 0;
    font-weight: bold;
}

</style>