<template>
    <div class="quiz-wrapper">
        <!-- {{ quizzes }} -->
        {{ typeof(questions) }}
        <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        <div class='quiz-countainer'>
            <div 
            v-for="(question,questionindex) in questions.slice(a,b)"
            v-bind:key="questionindex">
                <div class='question-wrapper'>
                    <div class="question-header"><i class='q'>Q</i>第{{  }}問</div>
                    <div class='question-body'>{{ question.label }}</div>
                </div>
                <!-- <div :class='showPic(question.image)'> -->
                <div v-if="question.image">
                    <img  v-bind:src="question.get_image"/>
                </div>
            </div>
        </div>

    </div>
  
</template>

<script>
import {mapGetters,mapActions} from 'vuex'

export default {
    data(){
        return{
            a: 0,
            b: 1,
        }
    },
    created(){
        console.log("created")
        // this.getquiz()
        this.getquestions()
    },
    computed: mapGetters(['questions']),
    methods:{
        ...mapActions(['getquestions']),
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

</style>