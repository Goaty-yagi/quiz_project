<template>
<!-- this scroll fixed should be change -->
    <div  class="board-detail-wrapper" :class="{'scrll-fixed':showAnswerPage||showReplyPage,'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class="question-wrapper" v-if="question&&relatedQuestion.results&&$store.state.isLoading==false">
                <p class='title-white'>質問板</p>
                <div v-if="$store.state.board.notifications.reply" :class="{'notification-blue':$store.state.board.notifications.reply}">
                    <div class="notification-text">
                        返信しました。
                    </div>
                </div>
                <div v-if="$store.state.board.notifications.answer" :class="{'notification-blue':$store.state.board.notifications.answer}">
                    <div class="notification-text">
                        回答しました。
                    </div>
                </div>
                <div v-if="$store.state.board.notifications.post" :class="{'notification-blue':$store.state.board.notifications.post}">
                    <div class="notification-text">
                        投稿しました。
                    </div>
                </div>
                <div class='question-box'> 
                    <div class="question-box-header">
                        <div class="image">
                            <img class='img' v-bind:src="question.user.thumbnail"/>
                        </div>
                        <div class="username-date">
                            <p> {{ question.user.name}}さん </p>
                            <p> {{ question.created_on }} </p>
                        </div>
                        <div class="question-status-container">
                            <p class="question-status"> {{ handleQuestionStatus(question.solved) }} </p>
                        </div>
                    </div>
                    <div
                     class="tag-container">
                        <div
                         class="tag"
                         v-for="(tag,questionindex) in question.tag"
                         v-bind:key="questionindex">
                            {{ tag.tag }}
                        </div>
                    </div>
                    <div class="title-question">
                        <p class="question-title">  {{ question.title }} </p>        
                        <p class='question-description'> {{ question.description}} </p>
                    </div>
                    <div class="question-box-footer">
                        <div class="like-wrapper">
                            <i v-if="addedLiked==false" @click="addLikedNum" class="far fa-heart" ></i>
                            <i v-if="addedLiked" class="fas fa-heart"></i>
                            <p class="good" v-if="question.liked_num[0]">{{ liked_num }} </p>
                        </div>
                        <div class="viewed-wrapper">
                            <p class="viewed"> viewed {{ question.viewed}} </p>
                        </div>
                        <div class="favorite" @click="handleAddedFavorite()">
                            <i v-if="addedFavorite==false" class="far fa-star"></i>
                            <div  v-if="addedFavorite" class="added-favorite">
                                <i class="far fa-star"></i>
                                <i class="fas fa-star"></i>
                            </div>
                        </div>
                    </div>
                    <div v-if="loginUser">
                        <button v-if="question.user.UID != $store.state.signup.user.uid" class="btn-base-white-db-sq" @click='handleShowAnswerPage'>回答する</button>
                    </div>
                    <!-- <button @click="handleNotifications('reply')" >unko</button> -->
                </div>
                <div class="relative-box">
                    <p>関連した質問</p>
                    <div
                        class="question-wrapper"
                        v-for="(question,questionindex) in slicedRelatedQuestion"
                        v-bind:key="questionindex">
                        <div class='question-list' @click="getRelatedSlug(question.slug)">
                            <div class="tag-wrapper">
                                <div 
                                class="tag"
                                v-for="(tag,tagindex) in question.tag" 
                                v-bind:key="tagindex">{{ tag.tag }}</div>
                            </div>
                            <!-- <div class="question-title">{{ question.title }}</div> -->
                            <div class="question-description">{{ question.description.substr(0,10)+'...' }}</div>
                            <div class='good-like-wrapper'>
                                <i class="far fa-heart"></i>
                                <div class="good" v-if="question.liked_num[0]">{{ question.liked_num[0].liked_num }}</div>
                                <div class="date">投稿日：{{ question.created_on }}</div>
                            </div>
                        </div>        
                    </div>
                    <div class="see-more">
                        <router-link :to="{name:'RelatedQuestion'}">もっと見る></router-link>
                    </div>
                </div>
                <div class="answer-box" v-if='question.answer[0]'>
                    <div class="answer-box-title">
                        <p v-if='question.answer[0]'> 回答</p>
                        ({{ question.answer.length }}件)
                    </div>
                    <div
                     class="under-line"
                     v-for="(answer,answerindex) in question.answer"
                     v-bind:key="answerindex">
                        <div class="answer-box-header">
                            <img class='img' v-bind:src="answer.user.thumbnail"/>
                            <div class="username-date">
                                <p> {{ answer.user.name}}さん </p>
                                <p> {{ answer.created_on }} </p>
                            </div>
                        </div>
                        <p class="answer-description-container">{{ answer.description }} </p>
                        <div class="answer-box-footer">
                            <i v-if="answerDict[answer.id].addedAnswerLiked==false" @click="addAnsweerLikedNum(answer.id)" class="far fa-heart" ></i>
                            <i v-if="answerDict[answer.id].addedAnswerLiked" class="fas fa-heart"></i>
                            <p class="good"> {{ answerDict[answer.id].liked_num }} </p>
                        </div>
                        <div v-if="loginUser">
                            <button v-if="question.user.UID == $store.state.signup.user.uid && answer.reply.length == 0"
                            class='btn-base-white-db-sq' 
                            @click='handleReplyPage(answer.id, answer.description)'>
                            返信する
                            </button>
                        </div>
                        <!-- reply should be appir if post user or replyer -->
                        <div class='reply-wrapper' v-if='answer.reply[0]'>
                            <div>コメント</div>
                            <div class='reply-flex' 
                            v-for="(reply,replyindex) in answer.reply"
                            v-bind:key="replyindex">
                                <div class="reply-wrapper-header">
                                    <img class='img' v-bind:src="reply.user.thumbnail"/>
                                    <div class="username-date">
                                        <p> {{ reply.user.name}}さん </p>
                                        <p> {{ reply.created_on }} </p>
                                    </div>
                                </div>
                                <p class="replay-description">{{ reply.description }}</p>
                                <div v-if="loginUser">
                                    <button v-if='$store.state.signup.user.uid==question.user.UID && answer.reply.slice(-1)[0].id==reply.id && answer.reply.slice(-1)[0].user.UID!=question.user.UID || $store.state.signup.user.uid==answer.user.UID && answer.reply.slice(-1)[0].id==reply.id && answer.reply.slice(-1)[0].user.UID==question.user.UID'
                                    class='btn-base-white-db-sq' 
                                    @click='handleReplyPage(answer.id, reply.description)'>
                                    返信する
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class='line-flex'>
                            <div class="line"></div>
                        </div>
                    </div>
                </div>
            </div>
            <transition name="notice">
                <NotVerified
                    class="components"
                    v-if="showEmailVerified"
                    @handleShowEmailVerified="handleShowEmailVerified"
                />
            </transition>
            <transition name="notice">
                <NotLogin
                    class="components"
                    v-if="showNotLogin"
                    @handleShowNotLogin="handleShowNotLogin"
                />
            </transition>
            <Answer v-if='showAnswerPage'
            class="components"
            @handleShowAnswerPage='handleShowAnswerPage'
            @getDetail="getDetail"
            :questionTitle='questionTitle'
            :questionDescription='questionDescription'
            :questionId='questionId'
            />
            <Reply v-if='showReplyPage'
            class="components"
            @handleShowReplyPage='handleShowReplyPage'
            @getDetail="getDetail"
            :answerId='answerId'
            :reply="reply"
            />
        <!-- {{ questions }} -->
        <!-- <div class=question 
         v-for="(question,questionindex) in questions"
         v-bind:key="questionindex">
            <div class="tag">tag:{{ question.tag }}</div>
            <div class="title">title:{{ question.title }}</div>
            <div class="good">good:{{ question.good }}</div>
            <div class="date">data:{{ remove_T_Z(question.timestamp) }}</div>
        </div>
        <CreateQuestion v-if='showCreateQuestion'
        @handleShowConfirm='handleShowConfirm'/>
        <Confirm v-if='showConfirm'/> -->
         </div>
    </div>
</template>

<script>
import axios from 'axios'
import {router} from "../main.js"
import NotVerified from '@/components/login/NotVerified.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import  Answer from '@/components/board/Answer.vue'
import  Reply from '@/components/board/Reply.vue'
export default {
    components: {
        Answer,
        Reply,
        NotVerified,
        NotLogin
  },
    data(){
        return{
            currentUserId:'',
            question:'',
            showAnswerPage: false,
            showReplyPage: false,
            questionTitle:'',
            questionDescription:'',
            questionSlug:'',
            questionId:'',
            answerId:'',
            allAnswer:'',
            answerDict:{},
            addedAnswerLiked:{},
            viewed:0,
            questionStatus:['回答受付中','解決済み'],
            reply:'',
            questionUser: '',
            questionUserBoolean: false,
            liked_num: '',
            addedLiked: false,
            addedFavorite: false,
            likedUserIdList:'',
            checkedLikedUserList:[],
            relatedQuestion:'',
            slicedRelatedQuestion:'',
            questionTags:[],
            showEmailVerified:false,
            showNotLogin: false,
        }
    },
    mounted() {
        this.getDetail()
        console.log("mounted_detail",this.$route.params.slug)
    },
    beforeUnmount(){
        console.log('beforeUNMOUNT')
        this.$store.dispatch('getDjangoUser')
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        loginUser(){
            return this.$store.state.signup.user
        },
        emailVerified(){
            return this.$store.getters.getEmailVerified
        },
    },
    methods: {
        async getDetail(slug="") {
            this.$store.commit('setIsLoading', true)
            this.scrollTop()
            console.log('inthegetdetail')
            if(slug==""){
                var url = `/api/board/question/${this.$route.params.slug}`
            }else{
                var url = `/api/board/question/${slug}`
            }
            await axios
                .get(url)
                .then(response => {
                    this.question = response.data
                    this.questionTitle = this.question.title
                    this.questionDescription = this.question.description
                    this.questionSlug = this.question.slug
                    this.questionId = this.question.id
                    this.liked_num = this.question.liked_num[0].liked_num
                    this.likedUserIdList = this.question.liked_num[0].user
                    this.questionUser = this.question.user.UID
                    this.allAnswer = this.question.answer
                    this.viewed = this.question.viewed
                    this.patchOnReply()
                    // this.patchOnAnswer()
                    this.questionPatch()
                    this.makeAnswerDict()
                    this.getQuestionTagList(this.question.tag)
                    this.getRelatedQuestion()
                    this.countViewedNumUp()
                    this.favoriteCheck()
                    if(!this.loginUser){
                        this.$store.commit('setIsLoading', false)
                    }
                })
                .catch(error => {
                    console.log(error)
            })
            // this.$store.commit('setIsLoading', false)
        },
        // async patchOnAnswer(slug=""){
        //     if(slug==""){
        //         var url = `/api/board/question/${this.$route.params.slug}`
        //     }else{
        //         var url = `/api/board/question/${slug}`
        //     }
        //     console.log("gonna if patch answer",this.question.on_answer==true&&this.question.user.UID==this.user.UID)
        //     if(this.question.on_answer==true&&this.question.user.UID==this.user.UID){
        //         console.log('PatchAnswer url',url)
        //         axios.patch(
        //             url,
        //             { on_answer: false }) 
        //         console.log("go store AQ and DU")
        //         await this.$store.dispatch('getDjangoUser')
        //         await this.$store.dispatch('getAnsweredQuestion')
        //     }
        // },
        async patchOnReply(){
            console.log("patchOnReply",this.allAnswer)
            for(let answer of this.allAnswer){
                console.log("answer",answer)
                if(answer.on_reply==true&&answer.user.UID==this.$store.getters.user.UID){
                    var url = `/api/board/answer-detail/${answer.id}`
                    await axios({
                        method: 'patch',
                        url: url,
                        data: {
                            on_reply: false,
                        },
                    })
                    this.$store.dispatch('getDjangoUser')
                    this.$store.dispatch('getAnsweredQuestion')
                }
            }
        },
        async getRelatedQuestion() {
            // relatedQuestion.results Start from here.
            // => deleteSameQuestion to delete the same question in RQ as detail Q.
            // => makeRandomSlicedArray to make random sliced RQ array
            if(this.loginUser){
                this.$store.commit('setIsLoading', true)
                if(this.questionTags.length == 1){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&uid=${this.user.UID}`
                }
                if(this.questionTags.length == 2){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&uid=${this.user.UID}`
                }
                if(this.questionTags.length == 3){
                    var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&tag=${this.questionTags[2]}&uid=${this.user.UID}`
                }
                console.log("url:",url)
                try{
                    await axios.get(url)
                        .then(response => {
                        this.relatedQuestion = response.data
                        })
                    }
                catch{(error => {
                        console.log(error)
                })}
                console.log('after-try',this.relatedQuestion)
                this.$store.commit('setRelatedQuestion', this.relatedQuestion.results)
                this.deleteSameQuestion()
                this.makeRandomSlicedArray()
                this.$store.commit('setIsLoading', false)
                    
            }
            else{
                this.relatedQuestion = {}
                this.relatedQuestion.results = 'unko'

            }
        },
        async createFavorite(){
            await axios({
                method: 'post',
                url: '/api/board/favorite-question-create/',
                data: {
                    user: this.$store.state.signup.user.uid,
                    question: [this.question.id]
                },
            })
        },
        handleAddedFavorite(){
            if(this.user){
                this.addedFavorite=!this.addedFavorite
                this.createFavorite()
            }else{
                this.handleShowNotLogin()
            }
        },
        async countViewedNumUp(){
            if(this.loginUser){
                for (let i =0; i < this.question.tag.length; i++){
                    await axios({
                    method: 'post',
                    url: '/api/board/user-tag/create/',
                    data: {
                        user: this.$store.state.signup.user.uid,
                        tag: this.question.tag[i].id
                        },  
                    })
                }
            }
        },
        handleShowAnswerPage(){
            console.log('clicked')
            if(this.emailVerified){
                this.showAnswerPage = !this.showAnswerPage
            }else{
                this.handleShowEmailVerified()
            }
            // this.handleScrollFixed()
        },
        getReply(reply){
            this.reply = reply
        },
        handleShowReplyPage(){
            this.showReplyPage = !this.showReplyPage
        },
        handleReplyPage(id, reply=''){
            this.getAnswerId(id)
            this.showReplyPage = !this.showReplyPage
            this.getReply(reply)
        },
        getAnswerId(id){
            this.answerId = id
        },
        getReplyUserAndQuestionUser(reply, question){
            this.questionAnswerUser.push(reply)
            this.questionAnswerUser.push(question)
        },
        handleQuestionStatus(status){
            if(status==true){
                return this.questionStatus[1]
            }
            else{
                return this.questionStatus[0]
            }
        },
        getQuestionTagList(questionTags){
            this.questionTags = []
            for(let tag of questionTags){
                this.questionTags.push(tag.id)
            }
        },
        // G-method return a value from array invoked
        // RandArray(array){
        //     var rand = Math.random()*array.length | 0;
        //     var rValue = array[rand];
        //     console.log("RAndA", rValue)
        //     return rValue;
        // },
        makeRandomSlicedArray(){
            if(this.loginUser){
                let num = 3
                console.log("MRSA")
                if (this.relatedQuestion.results.lendth < 3){
                    num = this.relatedQuestion.results.lendth
                }
                console.log("MRSA2")
                this.getRandomQuestion(this.relatedQuestion.results)
                this.slicedRelatedQuestion = this.relatedQuestion.results.slice(0,num)
                console.log(this.slicedRelatedQuestion)
            }
        },
        deleteSameQuestion(){
            if(this.loginUser){
                for(let q of this.relatedQuestion.results){
                    if (q.id == this.question.id){
                        this.relatedQuestion.results.splice(this.relatedQuestion.results.indexOf(q),1)
                        break
                    }
                }
            }
        },
        getRandomQuestion(array){
            for (let i = array.length - 1; i >= 0; i--) {
                let r = Math.floor(Math.random() * (i + 1))
                let tmp = array[i]
                array[i] = array[r]
                array[r] = tmp
                }
            for ( let k =0; k < array.length; k++){
                for (let i = array[k].answer.length - 1; i >= 0; i--) {
                let r = Math.floor(Math.random() * (i + 1))
                let tmp = array[k].answer[i]
                array[k].answer[i] = array[k].answer[r]
                array[k].answer[r] = tmp
                }}
                return array
            },
        // resetNotifications(){
        //     this.notifications.answer = false
        //     this.notifications.reply = false
        // },
        // handleNotifications(elem){
        //     if(elem == "reply"){
        //         this.notifications.reply = true
        //         setTimeout(this.resetNotifications, 3000)
                
        //     }
        //     if(elem == "answer"){
        //         console.log("in answer")
        //         this.notifications.answer = true
        //         setTimeout(this.resetNotifications, 3000)
        //     }            
        // },
        // getLikedNum(liked_num){
        //     this.liked_num = liked_num
        //     return this.liked_num
        // },
        getRelatedSlug(slug){
            this.getDetail(slug)
            this.$forceUpdate();
        },
        addLikedNum(){
            if(this.loginUser){
                this.liked_num += 1
                this.addedLiked = true
                for(let i=0; i<this.likedUserIdList.length; i++){
                    this.checkedLikedUserList.push(this.likedUserIdList[i].UID)
                }
                this.checkedLikedUserList.push(this.$store.state.signup.user.uid)
                this.countUpLiked()
            }else{
                this.handleShowNotLogin()
            }
        },
        clearAllLiked(){
            this.addedLiked = false
            for(let i in this.answerDict){
                this.answerDict[i].addedAnswerLiked = false
            }
        },
        checkUserLiked(){
            // this is for question like
            if(this.loginUser){
                this.clearAllLiked()
                for(let i of this.likedUserIdList){
                    if(i.UID == this.$store.state.signup.user.uid){
                    this.addedLiked = true
                    }
                }
                console.log("likedhere",this.addedLiked)
                // this is for answer like
                for(let answerId in this.answerDict){
                    // console.log(Array.isArray(this.answerDict[answerId].likedUsers))
                    for( let user of this.answerDict[answerId].likedUsers[0]){
                        if(user == this.$store.state.signup.user.uid){
                            this.answerDict[answerId].addedAnswerLiked = true
                        }
                    }
                }   
            }
        },
        favoriteCheck(){
            if(this.user){
                this.addedFavorite = false
                for(let i of this.$store.state.signup.djangoUser.favorite_question[0].question){
                    console.log('loop',this.addedFavorite,i,this.question.id)
                    if(this.question.id==i){
                        this.addedFavorite = true
                        console.log(this.addedFavorite)
                        break
                    }
                }
            }
        },
        countUpLiked(){
            // console.log('in countUPLiked',this.question.liked_num[0].id ,this.addedLiked)
            if(this.addedLiked){
                axios.patch(`/api/board/question-liked/${this.question.liked_num[0].id}/`,
                {
                    user: this.checkedLikedUserList,
                    liked_num: this.liked_num
                })
                console.log('done')
            }
        },
        async questionPatch(){
            // patch view count_up and on_answer
            if(this.questionUserBoolean == false&&this.question.on_answer==true&&this.question.user.UID==this.user.UID){
                console.log('count', this.questionSlug)
                await axios.patch(`/api/board/question/${this.questionSlug}`,{
                    viewed: this.viewed + 1,
                    on_answer: false
                })
                this.$store.dispatch('getDjangoUser')
                this.$store.dispatch('getAnsweredQuestion')
            }else if(this.questionUserBoolean == false){
                axios.patch(`/api/board/question/${this.questionSlug}`,{
                    viewed: this.viewed + 1
                })
            }
        },
        // setAnswerBoolean(){
        //     for(let answer of this.allAnswer){
        //         this.addedAnswerLiked[answer.id] = false
        //     }
        //     console.log('boo',this.addedAnswerLiked)
        // },
        makeAnswerDict(){
            // liked_answer start from here to make each answer dict
            // to hold information
            console.log("in make dict",this.allAnswer)
            for(let answer of this.allAnswer){
                console.log(answer)
                this.answerDict[answer.id] = {
                    "liked_id":answer.liked_answer[0].id,
                    "liked_num":answer.liked_answer[0].liked_num,
                    "addedAnswerLiked":false,
                    "likedUsers":[answer.liked_answer[0].user]
                }
            }
            console.log('answer-dict',this.answerDict)
            this.checkUserLiked()
        },
        addAnsweerLikedNum(answerId){
            // add answer id start from here. answerDict has each answers liked num.
            // invoke answerId to att liked num, then addedAnswerLiked = true  
            this.answerDict[answerId].liked_num += 1
            this.answerDict[answerId].addedAnswerLiked = true
            // for(let i=0; i<this.likedUserIdList.length; i++){
            //     this.checkedLikedUserList.push(this.likedUserIdList[i].UID)
            // }
            this.answerDict[answerId].likedUsers[0].push(this.$store.state.signup.user.uid)
            console.log("is addliked",this.answerDict)
            this.countUpLikedAnswer(answerId)
        },
        countUpLikedAnswer(answerId){
            console.log("countUpLikedAnswer")
                axios.patch(`/api/board/answer-liked/${this.answerDict[answerId].liked_id}/`,
                {
                    user: this.answerDict[answerId].likedUsers[0],
                    liked_num: this.answerDict[answerId].liked_num
                })
                console.log('done')
        },
        handleShowEmailVerified(){
            console.log('V')
            this.showEmailVerified = !this.showEmailVerified
            console.log('V',this.showEmailVerified)
        },
        handleShowNotLogin(){
            this.showNotLogin = !this.showNotLogin
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
                // behavior: "smooth"
            });
        },
        // falseNotifications(elem){
        //     if(elem == "answer"){
        //         this.notifications.answer = false
        //     }
        //     if(elem == "reply"){
        //         this.notifications.reply = false
        //     }
        // },
        // handleScrollFixed(){
        //     this.scrollFixed = !this.scrollFixed
        // },
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
@import "style/_board.scss";
.scroll{
    position:fixed;
}
.components{
    z-index: 3;
}

.board-detail-wrapper{
    display: flex;
    justify-content: center;
    width: 100vw;
    min-height: 80vh;
    margin-bottom: 1rem;
    // align-items: center;
}
.question-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    .question-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        .question-box-header{
            display: flex;
            .image{
                .img{
                border-radius: 50%; 
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
                width:40%;
            }
            .question-status-container{
                display: flex;
                justify-content: flex-end;
                width: 50%;
                position: relative;
                .question-status{
                    position: absolute;
                    right:0;
                    top: 0.5rem;
                    color: rgb(255, 43, 209);
                    margin-right: 1rem;
                }
            }
        }
        .tag-container{
            display: flex;
            width: 100%;
            padding-left: 1rem;
            .tag{
                margin-right: 0.5rem;
                border: solid gray;
                border-radius: 1rem;
                padding:0.5rem; 
            }
        }
        .title-question{
            padding:1rem;
            .question-title{
                text-align: center;
                margin-bottom: 1rem;
                border-bottom: solid $dark-blue;
                display: inline-block;
                padding-bottom: 1rem;
            }
            .question-description{
                text-align: left;
                padding: 1rem; 
                background: rgb(236, 236, 236);
                white-space: pre-wrap;
            }
        }
        .question-box-footer{
            display: flex;
            margin-bottom: 0.5rem;
            width:100%;
            .like-wrapper{
                flex-basis: 10%;
                display: flex;
                .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 0.5rem;
                margin-right: 0.3rem;
                margin-top: 0.1rem;
                // flex-basis: 10%;
                }
            }
            .viewed-wrapper{
                flex-basis: 40%;
                .viewed{
                margin-left: 1rem;
                margin-right: 0.5rem;
                }
            }
            .favorite{
                display: flex;
                position:relative;
                justify-content:flex-end;
                flex-basis: 50%;
                margin-top: 0.1rem;
                margin-right: 1rem;
                box-sizing: border-box;
                position:relative;
                .far{
                    position: absolute;
                    right: 0.1rem;
                }
                .added-favorite{
                    position: relative;
                    .far{
                        position: absolute;
                        z-index:2;
                        right: 0.1rem;
                    }
                    .fas{
                        position: absolute;
                        color: yellow;
                        right: 0.1rem;
                        z-index:1;
                    }
                }
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
    }
    .relative-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        display: flex;
        flex-direction: column;
        P{
            margin-bottom: 0.5rem;
        }
        .question-wrapper{
            width: 100%;
            display: flex;
            .question-list{
                border-bottom: solid rgb(236, 234, 234);
                margin-bottom: 0.5rem;
                width:100%;
                padding: 0.2rem;
                // background: rgb(236, 234, 234);
                display: flex;
                flex-direction: column;
                .tag-wrapper{
                    display: flex;
                    width: 100%;
                    .tag{
                        border: solid rgb(230, 230, 230);
                        margin-left: 0.3rem;
                        min-width: 2rem;
                    }
                }
                .good-like-wrapper{
                    display: flex;
                    font-size: 0.7rem;
                    .fa-heart{
                        // color: rgb(221, 36, 221);
                        margin-left: 0.5rem;
                        margin-right: 0.3rem;
                        margin-top: 0.2rem;
                    }
                    .date{
                        margin-left: 0.5rem;
                    }
                }
            }
            .question-list:hover{
                background: rgb(230, 230, 230);
            }
        }
        .see-more{
            display: flex;
            justify-content: flex-end;
            margin-right: 0.5rem;
            margin-top: 0.5rem;

        }
    }
    .answer-box{
        border: solid $base-color;
        border-radius: 0.5rem;
        background: $back-lite-white;
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        .answer-box-title{
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        }
        .under-line{
            width: 90%;
            border-bottom: 0.2rem solid rgb(236, 236, 236);
            margin-top: 2rem;
            margin-bottom: 1rem;
            &:last-child{
                border-bottom: none;
            }
        }
        .answer-box-header{
            display: flex;
            .img{
                border-radius: 50%; 
                width:  3rem;   
                height: 3rem;
                margin: 0.5rem; 
            }
            .username-date{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.5rem;
            }
        }
        .answer-description-container{
            margin: 1rem;
            background: rgb(236, 236, 236);
            padding: 1rem;
            text-align: left;
        }
        .answer-box-footer{
            display: flex;
            .fa-heart{
                color: rgb(221, 36, 221);
                margin-left: 1rem;
                margin-right: 0.3rem;
                margin-top: 0.1rem;
            }
        }
        .btn-base-white-db-sq{
            margin: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            font-size: 1rem;
            font-weight: bold;
        }
        .reply-wrapper{
            // display: flex;
            // flex-direction: column;
            // justify-content: center;
            // align-items: center;
            .reply-flex{
                width: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-bottom: 1rem;
                .reply-wrapper-header{
                    width: 80%;
                    height: 100%;
                    display: flex;              
                    .img{
                        border-radius: 50%; 
                        width:  3rem;   
                        height: 3rem;
                        margin: 0.5rem; 
                    }
                    .username-date{
                        display: flex;
                        flex-direction: column;
                        align-items: flex-start;
                        margin-top: 0.5rem;
                    }
                
                }
                .replay-description{
                    width: 63%;
                    // border-left: solid $dark-blue;
                    background: rgb(236, 236, 236);
                    text-align: left;
                    padding: 0.5rem;
                }
            }
        }
        .line-flex{
            display: flex;
            width: 100%;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            // .line-flex:last-of-type{
            //     border-bottom: none;
            // }
            &.line{
                width: 90%;
                border-bottom: 0.2rem solid rgb(236, 236, 236);
                margin-top: 2rem;
                margin-bottom: 1rem;
                &:last-child{
                    border-bottom: none;
                }
            }
        }
    }
}
</style>