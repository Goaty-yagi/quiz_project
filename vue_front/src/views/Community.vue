<template>
    <div class="community-wrapper">
        <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <!-- <i class="fas fa-cog"></i> -->
            <div class="lds-dual-ring"></div>
        </div>
        <div class="main-wrapper"  v-if="questions">
            <h1 class='title-white'>質問板</h1>
            {{ getUserTags }}
            <!-- <div v-if="notifications" :class="{'notification-blue':notifications}">
                    <div class="notification-text">
                        投稿しました。
                    </div>
                </div> -->
            <div class='search-wrapper'>
                <i class="fas fa-search"></i>
                <input class='search' type="text">
            </div>
            <div class="question-box">
                <p class='word'>わからない事があったら質問してみよう。</p>
                <button class='btn-base-white-db-sq' 
                 @click='handleShowCreateQuestion'>質問する</button>
            </div>
            <!-- <button @click="handleNotifications">unko</button> -->
            <div class=select-wrapper>
                <button class='btn-tr-black-baselite-cir'>最近の投稿</button>
                <button class='btn-tr-white-base-cir'>おすすめの<wbr>投稿</button>
            </div>
            <div class="question-wrapper">
                <div
                v-for="(question,questionindex) in questions"
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
                            <div class="date">作成日：{{ remove_T_Z(question.created_on) }}</div>
                        </div>
                    </div>        
                </div>
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
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {router} from "../main.js"
import  CreateQuestion from '@/components/board/CreateQuestion.vue'
import  Confirm from '@/components/board/Confirm.vue'
export default {
    components: {
        CreateQuestion,
        Confirm,
  },
    data(){
        return{
            questions:'',
            parentTagDict:{},       
            showCreateQuestion: false,
            showConfirm: false,
            scrollFixed: false,
            scroll_position: '100',
            userTagList: [],
            // notifications:false,
            fixed: '',
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
    },
    mounted() {
        
        this.getQuestion() 
        // this.getQuestion()
        console.log('mounted at community',typeof []) 
    },
    computed:{
        getUserTags(){
            let checkDict = {}  
            // let checkedDict = {}
            let checkedList = []
            let checkedlist2 = []
            for(let i of this.$store.state.signup.djangoUser.user_tag){
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
            // this.userTags = this.$store.state.signup.djangoUser.user_tag
            // console.log("this.userTags",this.userTags)
            // return this.userTags
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
        // async getRelatedQuestion() {
        //     // relatedQuestion Start from here.
        //     // => deleteSameQuestion to delete the same question in RQ as detail Q.
        //     // => makeRandomSlicedArray to make random sliced RQ array
        //     this.$store.commit('setIsLoading', true)
        //     console.log("ingetRQ", this.questionTags.length)
        //     if(this.questionTags.length == 1){
        //         var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}`
        //     }
        //     if(this.questionTags.length == 2){
        //         var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}`
        //     }
        //     if(this.questionTags.length == 3){
        //         var url = `/api/board/question/filter-list?tag=${this.questionTags[0]}&tag=${this.questionTags[1]}&tag=${this.questionTags[2]}`
        //     }
        //     console.log("url:",url)
        //     try{
        //         await axios.get(url)
        //             .then(response => {
        //             this.relatedQuestion = response.data
        //             console.log(this.relatedQuestion.length,this.relatedQuestion)
        //             })
        //         }
        //     catch{(error => {
        //             console.log(error)
        //     })}
        //     this.$store.commit('getRelatedQuestion', this.relatedQuestion)
        //     this.deleteSameQuestion()
        //     this.makeRandomSlicedArray()
        //     console.log("relatedquestion",this.relatedQuestion)
        //     this.$store.commit('setIsLoading', false)
        // },
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
         handleScrollFixed(){
            this.scrollFixed = !this.scrollFixed
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
    width: 100vw;
    align-items: center;
    .main-wrapper{
        display: flex;
        flex-direction: column;
        align-items: center;
        .search-wrapper{
            border: solid $base-color;
            border-radius: 50vh;
            width: 70%;
            height: 2.5rem;
            background: $back-white;
            display: flex;
            align-items: center;        
            .fa-search{
                margin-left: 1rem;
            }
            .search{
                border: none;
                background: $back-white;
                width: 85%;
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