<template>
<!-- this scroll fixed should be change -->
    <div class="community-wrapper scroll_area" :class="{'scroll-fixed':showCreateQuestion, 'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <div class="community-container" v-if="$store.state.isLoading==false">
                <div class="header-flex">
                    <h1 class='title-white'>質問板</h1>
                    <i v-if="emailVerified" @click="goAccount()" class="fas fa-user user-font"></i>
                    <i v-if="handleOnReplyAndOnAnswer" class="fas fa-exclamation"></i>
                    <!-- <i @click="goAccount()" class="fas fa-address-book user-font"></i> -->
                </div>
                <!-- <div v-if="notifications" :class="{'notification-blue':notifications}">
                        <div class="notification-text">
                            投稿しました。
                        </div>
                    </div> -->
                <form class='search-wrapper' @submit.prevent='splitSearch()'>
                    <i class="fas fa-search"><input class='search' v-model='search' type="text"></i>
                </form>
            
                
                <div class="question-box" v-if='showQuestionStatus.search==false' >
                    <p class='word'>わからない事があったら質問してみよう。</p>
                    <button class='btn-base-white-db-sq' 
                    @click='handleShowCreateQuestion'>質問する</button>
                </div>
                <!-- <button @click="handleNotifications">unko</button> -->

                <div class=select-wrapper v-if='showQuestionStatus.search==false'>
                    <button
                    @click="questionHandler('recent')"
                    :class="{'btn-tr-white-base-cir':showQuestionStatus.recent==false,'btn-tr-black-baselite-cir':showQuestionStatus.recent}"
                    >最近の投稿</button>
                    <button
                    @click="questionHandler('reccomend')"
                    :class="{'btn-tr-white-base-cir':showQuestionStatus.reccomend==false,'btn-tr-black-baselite-cir':showQuestionStatus.reccomend}">おすすめの<wbr>投稿</button>
                </div>
                <div class="question-wrapper">
                    <CreateQuestion
                        v-if='showCreateQuestion'
                        :parentTagDict="parentTagDict"
                        @handleShowConfirm='handleShowConfirm'
                        @handleShowCreateQuestion='handleShowCreateQuestion'/>
                    <transition name="notice">
                    <NotVerified
                        v-if="showEmailVerified"
                        @handleShowEmailVerified="handleShowEmailVerified"
                        />
                    </transition>
                    <transition name="notice">
                    <NotLogin
                        v-if="showNotLogin"
                        @handleShowNotLogin="handleShowNotLogin"
                        />
                    </transition>
                    <Confirm
                        v-if='showConfirm'
                        @handleShowConfirm='handleShowConfirm'
                        @getDetail='getDetail'
                        @handleNotifications='handleNotifications'
                    />

                    <!-- here is for searched questions -->
                    <div v-if='showQuestionStatus.search'>
                        <div class="search-title title-blue">検索結果</div>
                        <div class="no-found" v-if="questions.results==false">
                            <p>お探しの質問は見つかりませんでした。</p>
                            <div class="route">
                                <div @click="goHome()"><i class="fas fa-home" ></i><p>ホームへ戻る</p></div>
                                <div @click="handleShowQuestionStatusSearch()"><i class="far fa-comments"></i><p>質問板へ戻る</p></div>
                            </div>
                        </div>
                        <div
                        v-for="(question,questionindex) in questions.results"
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
                    </div
                    >
                    <!-- here for general questions -->
                    <div
                    v-for="(question,questionindex) in handleQuestions"
                    v-bind:key="questionindex"
                    >
                        <div class='question-list' v-if='showQuestionStatus.search==false' @click="getDetail(question.slug)">
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
                    <div v-if="scrollBottom&&questions.next" class="question-list-dammy shine">
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
    </div>
</template>

<script>
import axios from 'axios'
// import { computed } from 'vue'
// import { useStore } from 'vuex'
import NotVerified from '@/components/login/NotVerified.vue'
import NotLogin from '@/components/login/NotLogin.vue'
import {router} from "../main.js"
import  CreateQuestion from '@/components/board/CreateQuestion.vue'
import  Confirm from '@/components/board/Confirm.vue'
import  Search from '@/components/board/Search.vue'
export default {
    // setup(){
    //     const store = useStore()
    //     return{
    //         user: computed(() => store.state.signup.user),
    //         email: computed(() => store.state.signup.email),
    //         password: computed(() => store.state.signup.password),
    //         emailVerified: computed(() => store.state.signup.emailVerified),
    //     }
    // },
    components: {
        CreateQuestion,
        Confirm,
        Search,
        NotVerified,
        NotLogin
  },
    data(){
        return{
            questions:'',
            temporaryQuestion:'',
            search:'',
            wordList: [],
            parentTagDict:{},       
            showCreateQuestion: false,
            showEmailVerified: false,
            showNotLogin: false,
            showConfirm: false,
            scrollFixed: false,
            scroll_position: '100',
            userTagList: [],
            // reccomendedQuestion: [],
            searchedQuestion:'',
            onAnswerOrReply:false,
            scrollY: 0,
            scrollHeight:'',
            scrollBottom: false, 
            bottomScrollActionHandler:true,
            // notifications:false,
            next: '',
            showQuestionStatus:{
                recent: true,
                reccomend: false,
                search: false
            },
            styles:{
                position:'',
                top:'',
            }
        }
    },
    created(){
        console.log('created')
        this.$store.dispatch('getDjangoUser')
        this.$store.dispatch('getAnsweredQuestion')
    },
    beforeMount(){
        // this.getQuestion()
        console.log('before-mounted')
    },
    mounted() {
        window.addEventListener('scroll', this.handleScroll)
        window.addEventListener('scroll', this.getScrollY)
        this.bottomScrollActionHandler = true
        this.scrollBottom = false, 
        this.scrollTop()
        this.handleOnAnswerOrReply()
        this.$store.dispatch('getRelatedQuestion')
        this.getQuestion()
        this.showEmailVerified = false
    },
    beforeUnmount(){
        window.removeEventListener('scroll', this.handleScroll)
        window.removeEventListener('scroll', this.getScrollY)
    },
    // unmounted(){
    //     console.log("DSTROY")
    //     window.removeEventListener('scroll', this.handleScroll)
    //     window.removeEventListener('scroll', this.getScrollY)
    // },
    // watch:{
    //     scrollY:function(v) {this.scrollY = window.scrollY }
    //     },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        roginUser(){
            return this.$store.state.signup.user
        },
        notification(){
            return 
        },
        reccomendedQuestion(){
            return this.$store.getters.gettersReccomendedQuestion
        },
        emailVerified(){
            return this.$store.getters.getEmailVerified
        },
        handleOnReplyAndOnAnswer(){
            // this is for community_page to display if user have notifications
            if(this.roginUser){
                for(let question2 of this.user.question){
                    if(question2.on_answer==true&&question2.user.UID==this.user.UID){
                        console.log("onAnswer_dayo")
                        return true
                    }
                }
                console.log("answercheck start", this.$store.getters.gettersAnsweredQuestions)
                let answeredQuestion = this.$store.getters.gettersAnsweredQuestions.results
                for(let question of answeredQuestion){
                    for(let answer of question.answer){
                        if(answer.on_reply==true&&answer.user.UID==this.user.UID){
                            return  true
                        }
                    }
                }return false
            }
            // Object.keys(answeredQuestion).forEach(key =>{
            //     console.log(key)
            //     for(let answer of answeredQuestion[key].answer){
            //         if(answer.on_reply==true){
            //             return true
            //         }
            //     }
            //     // this.showQuestion.questionStatus[key] = false
            // })
            // for(let question of getters.gettersAnsweredQuestions){
            //     console.log(question)
            //     for(let answer of question.answer){
            //         console.log(answer.id)
            //         if(answer.on_reply==true&&answer.user.UID==getters.user.UID){
            //             return  true
            //         }
            //     for(let question2 of getters.user.question){
            //             if(question2.on_answer==true&&question2.user.UID==getters.user.UID){
            //                 return true
            //             }else{
            //                 return false
            //             }
            //         }
            //     }
                
            // }
        },
        // getUserTags(){
        //     let checkDict = {}  
        //     // let checkedDict = {}
        //     let checkedList = []
        //     let checkedlist2 = []
        //     for(let i of this.user.user_tag){
        //         checkDict[i.tag] = i.total_num
        //         checkedList.push(i.tag)
        //     }
        //     console.log("computed",checkDict)
        //     if(Object.keys(checkDict).length <= 3){
        //         return checkedList
        //     }
        //     if(Object.keys(checkDict).length > 3){
        //         for(let m=0; m < 3; m++){
        //             const aryMax = function (a, b) {return Math.max(a, b);}
        //             let max = Object.values(checkDict).reduce(aryMax);
        //             const result = Object.keys(checkDict).reduce( (r, key) => { 
        //                 return checkDict[key] === max ? key : r 
        //                 }, null);
        //             // checkedDict[result] = max
        //             delete checkDict[result]
        //             checkedlist2.push(result)
        //         }
        //         return checkedlist2
        //     }
        // },
        handleQuestions(){
            console.log("in handlequestion")
            if(this.showQuestionStatus.recent){
                this.questions = this.temporaryQuestion
                return this.questions.results
            }
            else if(this.showQuestionStatus.reccomend){
                console.log('RECCOMEND',this.reccomendedQuestion)
                this.questions = this.reccomendedQuestion
                return this.questions.results
            }
            else if(this.showQuestionStatus.search){
                this.questions = this.searchedQuestion
                return this.questions.results
            }
        }
    },
    methods: {
        async getQuestion() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/board/question/list')
                .then(response => {
                    this.temporaryQuestion = response.data
                    // this.next = response.data.next
                    // document.title = this.product.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
            this.getParentTag()
        },
        async getAdditionalQuestion(next){
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
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        async getParentTag(){
            await axios
                .get('/api/board/parent-tag')
                .then(response => {
                    let parentTags = response.data
                    console.log('parentTags',parentTags)
                    this.getParentTagDict(parentTags)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        handleOnAnswerOrReply(){
            if(this.$store.getters.handleOnAnswer||this.$store.getters.handleOnReply){
                this.onAnswerOrReply = true
            }
        },
        // async getRelatedQuestion() {
        //     // this.$store.commit('setIsLoading', true)
        //     console.log("ingetRQ",this.getUserTags)
        //     if(this.getUserTags.length == 1){
        //         var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}`
        //     }
        //     if(this.getUserTags.length == 2){
        //         var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}&tag=${this.getUserTags[1]}`
        //     }
        //     if(this.getUserTags.length == 3){
        //         var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}&tag=${this.getUserTags[1]}&tag=${this.getUserTags[2]}`
        //     }
        //     console.log("url:",url)
        //     try{
        //         await axios.get(url)
        //             .then(response => {
        //             this.reccomendedQuestion = response.data
        //             console.log(this.reccomendedQuestion.length,this.reccomendedQuestion)
        //             })
        //         }
        //     catch{(error => {
        //             console.log(error)
        //     })}
        //     // this.$store.commit('setIsLoading', false)
        // },
        async getSearchQuestion(){
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/board/question/search/?keyword=${this.wordList}`)
                .then(response => {
                    this.searchedQuestion = response.data
                    console.log("SQ", this.searchedQuestion)
                    this.questionHandler("search")
                    console.log("status changed to :",this.showQuestionStatus.search)
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },          
        async splitSearch(){
            if(this.search){
                this.wordList = []
                let letterList = []
                this.search = this.search.trim()
                this.search = this.search.split('')
                for(let i of this.search){
                    console.log(i === ' ')
                    if(i === ' '&&letterList[0] || i === '　'&&letterList[0]){
                        this.wordList.push(letterList.join(''))
                        letterList = []
                    }
                    else if(i === ' ' || i === '　'){
                        ;
                    }             
                    else{
                        letterList.push(i)
                    }
                }
                this.wordList.push(letterList.join(''))
                letterList = []
                this.search = ''
                await this.getSearchQuestion()
            }
        },
        getParentTagDict(parentTags){
            for (let i of parentTags){
                this.parentTagDict[i.parent_tag] = i.center_tag
            }
        },
        handleShowCreateQuestion(){
            console.log('showCreate')
            if(this.emailVerified&&this.roginUser){
                this.showCreateQuestion = !this.showCreateQuestion
                this.handleScrollFixed()
                this.a()
            }else if(!this.emailVerified&&this.roginUser){
                this.handleShowEmailVerified()
            }else{
                this.handleShowNotLogin()        
            }
        },
        handleShowEmailVerified(){
            this.showEmailVerified = !this.showEmailVerified
        },
        handleShowNotLogin(){
            this.showNotLogin = !this.showNotLogin
        },
        handleShowConfirm(){
            this.showConfirm = !this.showConfirm
        },
        getDetail(slug){
            console.log('slugdayo',slug)
            // this.$store.commit('getSlug',slug)
            router.push(`/board-detail/${slug}` )
        },
        // nextHandlar(next){
        //     return next
        // },
        questionHandler(key){
            // recieve "recent" or "reccomend" to change status
            this.bottomScrollActionHandler = true
            for(let i of Object.keys(this.showQuestionStatus)){
                if(i == key){
                    this.showQuestionStatus[i] = true                    
                }else{
                    this.showQuestionStatus[i] = false
                }
            }
            // this.showQuestionStatus[key] = true
        },
        handleScrollFixed(){
            this.scrollFixed = !this.scrollFixed
        },
        handleShowQuestionStatusSearch(){
            showQuestionStatus.search = false
        },
        goHome(){
            router.push("/")
            this.$store.commit('reset')
        },
        goAccount(){
            router.push("/board/account")
        },
        scrollTop(){
            window.scrollTo({
                top: 0,
            });
        },
        getScrollY(){
            this.scrollY = window.scrollY
        },
        handleScroll(){
            var doch = document.querySelector('.scroll_area').scrollHeight
            var winh = window.innerHeight; //ウィンドウの高さ
            var bottom = doch - winh; //ページ全体の高さ - ウィンドウの高さ = ページの最下部位置
            if (bottom+100 <= this.scrollY&&this.bottomScrollActionHandler) {
                this.bottomScrollActionHandler = false
                this.scrollBottom = true
                console.log("shitadayo",this.scrollBottom,this.questions.next)
                this.getAdditionalQuestion(this.questions.next)
                // this.scrollBottom = false
                // this.next==null
                if(this.next==null){
                    this.scrollBottom = false
                }
            }
        },
        // dammySetTime(){
        //     this.scrollBottom = false
        // },
        // resetNotifications(){
        //     this.notifications = false
            
        // },
        // handleNotifications(){
        //         this.notifications = true
        //         setTimeout(this.resetNotifications, 3000)    
        // },
        a(){
            this.scroll_position = window.pageYOffset;
            this.styles.top = this.scroll_position
            console.log(this.scroll_position,)
        
        // const elem = document.getElementById('scroll');
        // elem.style.top = scroll_position
        // console.log('scroll', scroll_position)
        // window.scrollTo({
        //     top: scroll_position,
        //     behavior: "smooth"
        //     });
        //     console.log("unko")
        }
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
.scroll{
    position:fixed;
}
.community-wrapper{
    // background: linear-gradient(#5B759F,#1C254C);
    display: flex;
    flex-direction: column;
    // justify-content: center;
    height: auto;
    min-height: 80vh;
    width: 100vw;
    align-items: center;
    .main-wrapper{
        .community-container{
            display: flex;
            flex-direction: column;
            align-items: center;
            .header-flex{
                display: flex;
                justify-content: center;
                position:relative;
                width:100%;
                .user-font{
                    position:absolute;
                    right:0;
                    margin-right: 1rem;
                    margin-top: 1rem;
                    font-size: 2rem;
                    color: $dark-blue
                }
                .fa-exclamation{
                    position:absolute;
                    right:0;
                    margin-right: 0.6rem;
                    margin-top: 0.5rem;
                    font-size: 0.2rem;
                    border: solid red;
                    border-radius: 50vh;
                    // padding: 0.3rem;
                    padding-top: 0.1rem;
                    padding-bottom: 0.1rem;
                    padding-left: 0.3rem;
                    padding-right: 0.3rem;
                    color: red;
                    background: $back-white;
                }
            }
            .search-wrapper{
                border: solid $base-color;
                border-radius: 50vh;
                width: 70%;
                height: 2.5rem;
                background: $back-white;
                display: flex;
                align-items: center;       
                .fa-search{
                    width:100%;
                    margin-left: 1rem;
                    padding-right: 1rem;
                    transition: 0.5s;
                    color: rgb(165, 165, 165);
                    .search{
                    border: none;
                    padding-left: 0.5rem;
                    background: $back-white;
                    width: 90%;
                    }
                }
                .fa-search:focus-within{
                    color:rgb(80, 80, 80);
                }
            }
            .question-box{
                border: solid $base-color;
                border-radius: 0.5rem;
                width: 90%;
                height: 10rem;
                background: rgb(252, 252, 252);
                margin: 1rem;
                .word{
                    margin: 1rem;
                    font-size: 1.5rem;
                }
                .btn-base-white-db-sq{
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                    font-size: 1rem;
                    font-weight: bold;
                }
            }
            .select-wrapper{
                .btn-tr-black-baselite-cir{
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    font-size: 0.8rem;
                    margin-right: 0.1rem;
                }
                .btn-tr-white-base-cir{
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    font-size: 0.8rem;
                    margin-left: 0.1rem;
                }
            }
            .question-wrapper{
                margin: 1rem;
                width: 85%;
                .search-title{
                    margin-top: 2rem;
                }
                .no-found{
                    p{
                        margin-top:0.5rem;
                    }
                    .route{
                        display:flex;
                        align-items: center;
                        justify-content: center;
                        padding: 1rem;
                        color: gray;
                        div{
                            margin:1rem;
                        }
                        div:hover{
                            color:rgb(221, 221, 221);
                            transition:0.3s;
                        }
                    }
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
                .question-list-dammy{
                    background: gray;
                    display: flex;
                    width: 100%;
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
        }
    }
}
</style>