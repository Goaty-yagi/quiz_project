<template>
    <div class="related-wrapper">
        <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        <div class="main-wrapper">
            <h1 class='title-white'>質問板</h1>
            <div class="related-title">関連した質問</div>
            <div class="question-wrapper">
                <div
                v-for="(question,questionindex) in $store.state.board.relatedQuestion"
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
                            <div class="date">作成日：{{ dateConvert(question.created_on) }}</div>
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
        }
    },
    methods: {
        getDetail(slug){
            console.log('slugdayo',slug)
            // this.$store.commit('getSlug',slug)
            router.push(`/board-detail/${slug}` )
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
    }

}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";

.related-wrapper{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.main-wrapper{
        display: flex;
        flex-direction: column;
        align-items: center;
        .related-title{
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 2rem;
            color: $dark-blue;
            // border-bottom: solid $dark-blue;
        }
        .question-wrapper{
            margin: 1rem;
            width: 85%;
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