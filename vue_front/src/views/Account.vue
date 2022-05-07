<template>
    <div class="account-wrapper" :class="{'laoding-center':$store.state.isLoading}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            
            <div v-if='$store.state.isLoading==false' class="content-wrapper">
                <h1 class='title-white'>アカウント</h1>
                <div class="cropper-wrapper">
                    <img v-bind:src="userData.thumbnail"/>
                    <p @click='handleShowThumbnail'>画像を<br>変更する</p>
                </div>
                <div v-if="showNotification" class="notification-container">
                    <div class="alert-position-container">
                        <div class="notification-text">
                            お知らせ
                        </div>
                        <div class="notification-alert">
                            Notifications
                        </div>
                    </div>
                </div>
                <div class="user-info-wrapper">
                    <div class="user-name user-container">
                        <div class="left-side">
                            User<br>Name
                        </div>
                        <div class="right-side">
                            {{ userData.name}}
                        </div>
                    </div>
                    <!-- <div class="user-id user-container">
                        <div class="left-side">
                            User<br>ID
                        </div>
                        <div class="right-side">
                            <p>{{ userData.UID }}</p>
                        </div>             
                    </div> -->
                    <div class="current-level user-container">
                        <div class="left-side">
                            Grade
                        </div>
                        <div class="right-side grade-right-side">
                            <div classs="current-level-text">
                                {{ getCurrentGradeNmae(quizTaker.grade)}}
                                Lv,{{ quizTaker.level }}
                            </div>
                            <div class="max-level">
                                最大レベル　初級Lv,2
                            </div>
                        </div>       
                    </div>
                    <div class="next-level">
                        次は初級レベル７だよ！
                    </div>
                </div>
                <div class="status-wrapper">
                    <chart
                    v-if="gotInfo"
                    :chart-data="chartData"
                    />
                </div>
                <div @click="goCommunityAccount()" class="comunity-account">
                    コミュニティアカウントへ移動
                </div>
            </div>
        </div>
        <NotVerified
        v-if="!emailVerified&&$store.state.isLoading==false"
        :currentPageName="currentPageName"
        />
        <Sent v-show='showSent'/>
        <Thumbnail v-if="showThumbnail"
        @showThumbnailFalse="showThumbnailFalse"
        @getUserData="getUserData"/>
    </div>
</template>

<script>
import {router} from "../main.js"
import axios from 'axios'
import 'cropperjs/dist/cropper.css';
import  Thumbnail from '@/components/account/Thumbnail.vue'
import  Chart from '@/components/account/Chart.vue'
import Sent from '@/components/signin/Sent.vue'
import NotVerified from '@/components/login/NotVerified.vue'
import { computed } from 'vue'
import { useStore } from 'vuex'
import {mapGetters,mapActions} from 'vuex'

export default{
    setup(){
        const store = useStore()
        return{
            user: computed(() => store.state.signup.user),
            email: computed(() => store.state.signup.email),
            password: computed(() => store.state.signup.password),
            emailVerified: computed(() => store.state.signup.emailVerified),
        }
    },
    data(){
        return{
            showSent:false,
            error:'',
            userData:'',
            quizTaker:'',
            showThumbnail:false,
            currentPageName:'',
            // showEmailVerified:true,
            gotInfo:false,
            showNotification:false,
            chartAllData:{
                '超初級':{
                    labels:[
                        'ひらがな', 
                        'カタカナ', 
                        'ボキャブラリー', 
                        'すうじ'
                        ],
                },
                '初級':{
                    labels:[
                        '漢字',
                        'な形容詞',
                        'い形容詞',
                        '動詞',
                        '文法',
                        'ボキャブラリー',
                    ],
                },
                '中級':{
                    labels:[],
                },
                '上級':{
                    labels:[],
                }
            },
            chartData: {
                labels: [],
                datasets: [{ 
                    label: "",
                    data: [],
                    borderWidth:1,
                    backgroundColor: 'rgba(255, 153, 51, 0.2)',
                    borderColor: ' #ff9933',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'red'
                }],
            },
        }
    },
    components: {
        Sent,
        Thumbnail,
        Chart,
        NotVerified
    },
    created(){
        this.getQuizNameId()
    },
    watch:{
        userData:function(v) {
            
        this.userData = v
        console.log('hi',v)
        },
    },
    computed: mapGetters(['quizNameId']),
        // returnChartSet(){
        //     if(this.chartData){
        //         this.gotInfo = true
        //         console.log("compu",this.chartData)
        //         return this.chartData
        //     }
        // },
    mounted(){
        console.log('account mounted',this.$route.params.uid)
        this.currentPageName = ''
        this.getUserData()
        this.getCurrentPageName()
        // this.handleShowEmailVerified()
    },
    methods:{
        ...mapActions(['getQuizNameId']),
        async getUserData(){
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/user/${this.$route.params.uid}`)
                .then(response => {
                    this.userData = response.data
                    this.quizTaker = response.data.quiz_taker[0]
                    console.log('inGet', this.userData,this.userStatus)
                    this.handleStatusParameter()
                    this.setInitUserStatus()
                    this.gotInfo = true
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setIsLoading', false)
        },
        async resent(){
            try{
                await this.$store.dispatch('sendEmailVerify')
                this.handleShowSent()
                console.log('showsent:',this.showSent)
            }catch(err){
                this.error = err
                console.log(this.error)
            }
        },
        handleShowSent(){
            this.showSent = true
        },
        handleShowThumbnail(){
            this.showThumbnail = true
        },
        showThumbnailFalse(){
            this.showThumbnail = false
            console.log('inA',this.showThumbnail)
        },
        getCurrentGradeNmae(gradeID){
            for (let i of this.quizNameId){
                if(i.id == gradeID){
                    return i.name
                }
            }
        },
        handleStatusParameter(){
            // this is handling chart view.
            // 1, get quiz_taker from userinfo
            // 2, get current grade from the quizTaker.
            // 3, get chart labels which is locally set.
            // 4, get percentage for each status from user_status from quiz_taker
            // 5, set the labels and the percentages to chartData to invoke data for chart component

            let tempDict = {}
            let tempChartAllData = this.chartAllData[this.getCurrentGradeNmae(this.quizTaker.grade)].labels
            let tempArray = []
            for(let i of this.quizTaker.user_status){
                if(i.grade==this.quizTaker.grade){
                    tempDict[i.status[0]]={"percentage":i.percentage,
                    'order':i.status[1],
                    }
                }
            // var sort = Object.keys(tempDict).map((k)=>({ key: k, value: tempDict[k] }));
            }
            for(let i of tempChartAllData){
                if(i in tempDict){
                    tempArray.push(tempDict[i].percentage / 10)
                }else{
                    tempArray.push(0)
                }
            }
            this.chartData.labels = tempChartAllData
            this.chartData.datasets[0].data = tempArray
            this.gotInfo = true
        },
        getCurrentPageName(){
            let i = this.$route.path
            i = i.split("/")
            this.currentPageName = i[1]
        },
        setInitUserStatus(){
            if(this.emailVerified){
                if(this.$store.getters.getTempUser){
                    this.$store.commit('setQuizTakerID',this.quizTaker.id)
                    this.$store.commit('setQuizID',this.$store.getters.getTempUser.grade)
                    var list = []
                    var counter = 0
                    for(let n of this.$store.getters.getTempUser.statusList){
                        if(counter == 0){
                            list.push(n)
                            counter += 1
                        }else{
                            list.forEach(function(element,index){
                                if(element.status == n.status){
                                    if(n.inCorrect){
                                        list[index].isCorrect +=1
                                    }else{
                                        list[index].isFalse +=1
                                    }
                                }else{
                                    list.push(n)
                                }          
                            })
                        }
                    }
                    console.log("go-loop",list)
                    for(let i of list){
                        this.$store.dispatch('userStatusPost',i)
                    }
                }
                this.$store.commit('setTempUserReset')
            }
        },
        // handleShowEmailVerified(){
        //     if(!this.EmainVerified){}
        //     this.showEmailVerified = false
        //     }
        // },
        goCommunityAccount(){
            router.push("/board/account")
        },      
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
// @import 'cropperjs/dist/cropper.css';
.account-wrapper{
    display: flex;
    justify-content: center;
    // min-height: 10vh;
    // height: 110vh;
    .main-wrapper{
        .content-wrapper{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            .cropper-wrapper{
                display: flex;
                position:relative;
                justify-content: center;
                margin-top: 0.5rem;
                width: 12rem;
                img{
                    border-radius: 50%; 
                    width:  5rem;   
                    height: 5rem;       
                }
                p{
                    position: absolute;
                    right: 0;
                    color: white;
                    font-size: 0.8rem;
                }
            }
            .notification-container{
                position: relative;
                display: flex;
                justify-content: center;
                width: 100%;
                .alert-position-container{
                    width:70%;
                    border: solid $base-color;
                    min-height: 3rem;
                    background: $back-white;
                    margin-top: 1rem;
                    margin-bottom: 1rem;
                    .notification-alert{
                    position: absolute;
                    right: 0;
                    top: 0;
                    margin-right: 0.9rem;
                    padding-right: 0.5rem;
                    padding-left: 0.5rem;
                    color: $back-white;
                    font-weight: bold;
                    border: solid $dark-blue;
                    border-radius: 50vh;
                    background:rgba(252, 75, 175, 0.961); 
                    }
                }
            }
            .user-info-wrapper{
                margin-top: 1rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                .user-container{
                    display: flex;
                    border: 0.1rem solid $dark-blue;
                    background: $back-white;
                    border-radius: 0.5rem;
                    width: 80%;
                    min-height: 3rem;
                    margin-bottom: 1rem;
                    overflow: hidden;
                    .left-side{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 30%;
                        background: $base-color;
                        border-right: 0.1rem solid $dark-blue;
                        line-height: 0.8rem;
                        color: white;
                        font-weight: bold;
                        font-size: 1.1rem;                      
                    }
                    .right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-basis: 70%;
                        width:70%;
                        font-size: 1.2rem;
                        font-weight: bold;
                        // overflow-wrap: break-all;                        
                    }
                    .grade-right-side{
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: flex-end;
                        .current-level-text{
                            display: flex;
                            justify-content: center;
                            align-items: flex-end;
                        }
                        .max-level{
                            position: absolute;
                            color: rgba(252, 75, 175, 0.961); 
                            right: 0;
                            top: 0;
                            font-size: 0.7rem;
                            margin-right: 0.2rem;
                        }
                    }
                }
                .next-level{
                    color: white;
                }
            }
            .status-wrappe{
                // padding-top: 10%;
            }
            .comunity-account{
                color: white;
                cursor : pointer;
                border: solid rgba(0, 0, 0, 0);
                padding: 1rem;
                transition: 0.5s;
                
            }
            .comunity-account:hover{
                border: solid gray;
                color: gray; 
                padding: 1rem;
            }
        }
    }
}


    .main-image{
        width:15%;
        height:auto;
        margin-left: auto;
        margin-right: auto;
    }
    .main-text1{
        font-size:1rem;
        font-weight: bold;
        margin:2rem;
    }
    img {
        border-radius: 50%; 
        width:  5rem;   
        height: 5rem;       
    }
    .cropper-view-box,
    .cropper-face {
      border-radius: 50%;
      cursor: grab;
      outline: initial;
    }
    .cropper-face:active {
      cursor: grabbing;
    }
</style>