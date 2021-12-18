<template>
  <div>
      <div v-if="!showQuiz">
        <p class="title is 3 has-text-white">{{quizzes[0].name}}問題</p>
        <p class="subtitle is 4 has-text-white">全{{questions.length}}問</p>
        <button @click="handleSHowQuiz">START</button>
    </div>
  </div>
</template>

<script>
export default {
    props:[
        'quizzes',
        'questions',
        'showQuiz'
    ],
    data(){
        return{
        }
    },
    methods:{
        handleSHowQuiz(){
            this.$emit('handle')
        },
    }
    }
</script>

<style>

</style>