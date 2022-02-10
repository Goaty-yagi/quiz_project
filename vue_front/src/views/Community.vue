<template>
    <div class="community-wrapper" v-if="questions">
        <h1>質問板</h1>
        <div class='search-wrapper'>
            <p>分からないことがあったら質問してみよう。</p>
        </div>
        <div class="ask-box" @click='handleShowCreateQuestion'>
            <button>質問する</button>
        </div>
        <div class=select-wrapper>
            <button>最近の投稿</button>
            <button>オススメの投稿</button>
        </div>
        <!-- {{ questions }} -->
        <div class=question 
         v-for="(question,questionindex) in questions"
         v-bind:key="questionindex">
            <div @click="getDetail(question.slug)">
                {{ question.slug }}
                <div class="tag">tag:{{ question.tag }}</div>
                <div class="title">title:{{ question.title }}</div>
                <div class="good">good:{{ question.good }}</div>
                <div class="date">data:{{ remove_T_Z(question.created_on) }}</div>
            </div>        
        </div>
        <CreateQuestion v-if='showCreateQuestion'
        @handleShowConfirm='handleShowConfirm'/>
        <Confirm v-if='showConfirm'/>
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
            questions:[],
            showCreateQuestion: false,
            showConfirm: false,
        }
    },
    beforeMount(){
        this.getQuestion() 
    },
    mounted() {
        this.getQuestion()
        console.log('mounted at community') 
    },
    methods: {
        async getQuestion() {
            this.$store.commit('setIsLoading', true)

            // const category_slug = this.$route.params.category_slug
            // const product_slug = this.$route.params.product_slug
            await axios
                .get('/api/board/question/')
                .then(response => {
                    this.questions = response.data
                    // document.title = this.product.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
        handleShowCreateQuestion(){
            this.showCreateQuestion = true
        },
        handleShowConfirm(){
            this.showConfirm = true
            console.log('confurm',this.showConfirm)
        },
        remove_T_Z(datatime){
            const time = datatime.replace(/T|Z/g,' ')
            return time
        },
        getDetail(slug){
            console.log(slug)
            // this.$store.commit('getSlug',slug)
            router.push(`/board-detail/${slug}` )
        }
    }
}
</script>

<style scoped>
.question{
    color:white;    
}
</style>