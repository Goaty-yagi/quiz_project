<template>
    <div class="community-wrapper">
        <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <!-- <i class="fas fa-cog"></i> -->
            <div class="lds-dual-ring"></div>
        </div>
        <div class="main-wrapper"  v-if="questions">
            <div class="header-flex">
                <h1 class='title-white'>質問板</h1>
                <i @click="goAccount()" class="fas fa-user user-font"></i>
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
           
            
            <div class="question-box" v-if='showSearch==false' >
                <p class='word'>わからない事があったら質問してみよう。</p>
                <button class='btn-base-white-db-sq' 
                 @click='handleShowCreateQuestion'>質問する</button>
            </div>
            <!-- <button @click="handleNotifications">unko</button> -->

            <div class=select-wrapper v-if='showSearch==false'>
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
                <Confirm
                    v-if='showConfirm'
                    @handleShowConfirm='handleShowConfirm'
                    @getDetail='getDetail'
                    @handleNotifications='handleNotifications'
                />

                <!-- here is for searched questions -->
                <div v-if='showSearch'>
                    <div class="search-title title-blue">検索結果</div>
                    <div class="no-found" v-if="searchedQuestion==false">
                        <p>お探しの質問は見つかりませんでした。</p>
                        <div class="route">
                            <div @click="goHome()"><i class="fas fa-home" ></i><p>ホームへ戻る</p></div>
                            <div @click="showSearcheFalse()"><i class="far fa-comments"></i><p>質問板へ戻る</p></div>
                        </div>
                    </div>
                    <div
                    v-for="(question,questionindex) in searchedQuestion"
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
                    <div class='question-list' v-if='showSearch==false' @click="getDetail(question.slug)">
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
                            <div class="date">作成日：{{ remove_T_Z(question.created_on) }}</div>
                        </div>
                    </div>        
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {router} from "../main.js"
import  CreateQuestion from '@/components/board/CreateQuestion.vue'
import  Confirm from '@/components/board/Confirm.vue'
import  Search from '@/components/board/Search.vue'
export default {
    components: {
        CreateQuestion,
        Confirm,
        Search
  },
    data(){
        return{
            questions:'',
            search:'',
            wordList: [],
            parentTagDict:{},       
            showCreateQuestion: false,
            showConfirm: false,
            showSearch: false,
            scrollFixed: false,
            scroll_position: '100',
            userTagList: [],
            reccomendedQuestion: [],
            searchedQuestion:'',
            // notifications:false,
            fixed: '',
            showQuestionStatus:{
                recent: true,
                reccomend: false
            },
            styles:{
                position:'',
                top:'',
            }
        }
    },
    created(){
    },
    beforeMount(){
        // this.getQuestion()
        console.log('mounted',this.user)
    },
    mounted() {
        this.getQuestion()
        this.getRelatedQuestion()
        // this.getQuestion()
        console.log('mounted at community',typeof []) 
    },
    computed:{
        user(){
            return this.$store.state.signup.djangoUser
        },
        getUserTags(){
            let checkDict = {}  
            // let checkedDict = {}
            let checkedList = []
            let checkedlist2 = []
            for(let i of this.user.user_tag){
                checkDict[i.tag] = i.total_num
                checkedList.push(i.tag)
            }
            console.log("computed",checkDict)
            if(Object.keys(checkDict).length <= 3){
                return checkedList
            }
            if(Object.keys(checkDict).length > 3){
                for(let m=0; m < 3; m++){
                    const aryMax = function (a, b) {return Math.max(a, b);}
                    let max = Object.values(checkDict).reduce(aryMax);
                    const result = Object.keys(checkDict).reduce( (r, key) => { 
                        return checkDict[key] === max ? key : r 
                        }, null);
                    // checkedDict[result] = max
                    delete checkDict[result]
                    checkedlist2.push(result)
                }
                return checkedlist2
            }
        },
        handleQuestions(){
            console.log("in handlequestion")
            if(this.showQuestionStatus.recent){
                console.log("return_recen:",this.questions)
                return this.questions
            }
            if(this.showQuestionStatus.reccomend){
                console.log("return_reco:",this.reccomendedQuestion)
                return this.reccomendedQuestion
            }
        }
    },
    methods: {
        async getQuestion() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/board/question/list')
                .then(response => {
                    this.questions = response.data
                    // document.title = this.product.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)
                })
            this.getParentTag()
            this.$store.commit('setIsLoading', false)
        },
        async getParentTag(){
            console.log('in_get_parentTag')
            await axios
                .get('/api/board/parent-tag')
                .then(response => {
                    let parentTags = response.data
                    this.getParentTagDict(parentTags)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async getRelatedQuestion() {
            // this.$store.commit('setIsLoading', true)
            console.log("ingetRQ",this.getUserTags)
            if(this.getUserTags.length == 1){
                var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}`
            }
            if(this.getUserTags.length == 2){
                var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}&tag=${this.getUserTags[1]}`
            }
            if(this.getUserTags.length == 3){
                var url = `/api/board/question/filter-list?tag=${this.getUserTags[0]}&tag=${this.getUserTags[1]}&tag=${this.getUserTags[2]}`
            }
            console.log("url:",url)
            try{
                await axios.get(url)
                    .then(response => {
                    this.reccomendedQuestion = response.data
                    console.log(this.reccomendedQuestion.length,this.reccomendedQuestion)
                    })
                }
            catch{(error => {
                    console.log(error)
            })}
            // this.$store.commit('setIsLoading', false)
        },
        async getSearchQuestion(){
            console.log('Gsearch')
            await axios
                .get(`/api/board/question/search/?keyword=${this.wordList}`)
                .then(response => {
                    this.searchedQuestion = response.data
                    console.log('gotserchedQQ',this.searchedQuestion)
                })
                .catch(error => {
                    console.log(error)
                })
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
                this.showSearch = true
            }
        },
        getParentTagDict(parentTags){
            for (let i of parentTags){
                this.parentTagDict[i.parent_tag] = i.center_tag
            }
        },
        handleShowCreateQuestion(){
            console.log('showCreate')
            this.showCreateQuestion = !this.showCreateQuestion
            this.handleScrollFixed()
            this.a()
        },
        handleShowConfirm(){
            this.showConfirm = !this.showConfirm
            console.log('confurm',this.showConfirm)
        },
        remove_T_Z(datatime){
            const time = datatime.replace(/T|Z/g,' ')
            return time
        },
        getDetail(slug){
            console.log('slugdayo',slug)
            // this.$store.commit('getSlug',slug)
            router.push(`/board-detail/${slug}` )
        },
        questionHandler(key){
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
        showSearcheFalse(){
            this.showSearch = false
        },
        goHome(){
            router.push("/")
            this.$store.commit('reset')
        },
        goAccount(){
            router.push("/board/account")
        },
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
    min-height: 100vh;
    width: 100vw;
    align-items: center;
    .main-wrapper{
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
        }
    }
}
</style>