<template>
  <div id="wrapper">
    <div class="box" v-if="quizzes[0]&&questions[0]">
      <div v-if="!showQuiz" @click="handleSHowQuiz">
        <p class="title is 3">{{quizzes[0].name}}問題</p>
        <p class="subtitle is 4">全{{questions.length}}問</p>
        <button>START</button>
      </div>
      <!-- <div v-show="counter > quizzes[0].question.length">
        <p class="title is-3">Result</p>
      </div> -->
      <div v-if="showQuiz && counter < questions.length + 1">
        <div class="title is-1"> 
          <h1>初級</h1>
          <p class=" button is-static is-rounded is-active subtitle is-6">第{{ counter }}問</p>
        </div>
        <div>
          <div  v-for="(question,questionindex) in questions.slice(a,b)"
              v-bind:key="questionindex">
            <p>
              {{ question.label }}
            </p>
            <div
            class="section button is-fullwidth my-4 has-text-grey-darker"       
              v-for="(answer,answerindex) in question.answer"
              v-bind:key="answerindex"
              @click="onClicked(answer)"
              :class="{'has-background-primary-light has-text-white is-hovered':answer.label == selectedAnswer[0]}"
              >
                <p class='button has-background-dark has-text-white is-static'>{{ answerindex+1 }}</p>
                <p
                class="column"
                >{{ answer.label }}</p>
            </div>
            </div>
          <button
          class="button is-link is-rounded"
          v-show='selectedAnswer!="" && counter != questions.length'
            @click="nextQuestion">next ></button>
          <button
          class="button is-info is-rounded"
          v-show="selectedAnswer!='' && counter == questions.length"
            @click="showResult">Finish</button>
        </div>
      </div>
      <!-- //result page// -->
      <div v-if="showQuiz && counter > questions.length">
        <div class='py-5 my-5 button has-background-info-light is-static'>
          <p class="title is 3 has-text-danger">結果発表</p>          
        </div>
        <div class=box> 
            <div class="mx-5 is-inline-block subtitle is 4">{{ questions.length }}問中</div>
            <div class="is-inline-block has-text-danger-dark title is 4">{{ trueAnswer }} 問正解</div>
            <div>
              <p class="subtitle is 5 button is-rounded is-static"> 正解率 {{ percentage }}%</p>
            </div>
            <table class='is my-5 table is-fullwidth is-hoverable' v-for="(result,resultindex) in rerultAnswer"
              v-bind:key="resultindex">
              <tr>
                <td> 
                  <p class='mx-5 is-inline-block subtitle is 4'>{{ resultindex+ 1 }}問目</p>
                  <p class='mx-6 title is-1 has-text-link is-inline-block subtitle is 4'
                  :class="{'has-text-danger':result==true}">{{ getFont(result) }}</p>
                  <p class='is-inline-block subtitle is 4'>{{  getJPResult(result) }}</p>
                </td>
              </tr>
            </table>
              <button class="button is-info is-rounded">詳細を見る</button>
        </div>
          <button class="mx-2 button is-primary is-outlined">HOME</button>
          <button class="mx-2 button is-warning is-light">もう一度</button>   
      </div>
    </div>
  </div>
</template>

<script> 
import axios from 'axios'
export default {
  name: 'Quiz',
  data(){
    return{
      counter: 1,
      selectedAnswer:'',
      rerultAnswer:[],
      quizzes: [],
      questions: [],
      showQuiz: false,
      a: 0,
      b: 1,
      hover: false,
      trueAnswer: 0,
      falseAnswer:0,
      percentage:100
      }
  },
  mounted:function() {
    this.getquiz()
    this.getQuestion()
    // this.getPercentage(this.trueAnswer)
  },
  methods:{
    getquiz(){
    axios
    .get('/api/quizzes/?id=2')
    .then(response => (this.quizzes = response.data))
    },
    getQuestion(){
    axios
    .get('/api/questions/quizzes/?quiz=2&num=12')
    .then(response => (this.questions = this.getRandomQuestion(response.data)))
    },
    handleSHowQuiz(){
      this.showQuiz = !this.showQuiz
    },
    nextQuestion(){
      this.a += 1
      this.b += 1
      this.getResult()
      this.rerultAnswer.push(this.selectedAnswer[1])
      this.selectedAnswer = ''
      console.log(this.trueAnswer)
      this.counter += 1
    },
    onClicked(i){
      this.selectedAnswer = [i.label,i.is_correct]
      // if(this.selectedAnswer == true){
      //   this.selectedAnswer = 'a'
      // }else{
      //   this.selectedAnswer ='b'
      // }
      console.log(this.selectedAnswer,this.trueAnswer)    
    },
    showResult(){
      // this.correctAnswer.push(this.selectedAnswer[1])
      this.getResult()
      this.rerultAnswer.push(this.selectedAnswer[1])
      this.selectedAnswer = ''
      this.counter += 1
      console.log(this.trueAnswer)
      this.getPercentage(this.trueAnswer)
    },
    getResult(){
      if (this.selectedAnswer[1] == true){
        this.trueAnswer +=1
      }else{
        this.falseAnswer +=1
      }
    },
    getJPResult(result){
      if (result == true){
        return '正解'
      }else{
        return'不正解'
      }

    },
    getFont(result){
      if (result == true){
        return '○'
      }else{
        return'×'
      }
    },
    getPercentage(answer){
      this.percentage = Math.round(answer/this.questions.length * 100)
      
    },
    getRandomQuestion:function(array){
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
    }        
  },
  // getTrue(){
  //     for(i in this.correctAnswe){
  //       if(i == true){
  //         this.True += 1
  //       }
  //     }
  //     return this.True 
  //   },
  // computed:{
  //   trueAnswer: function(){
  //     for(i in this.correctAnswe){
  //       if(i == true){
  //         this.True += 1
  //       }
        
  //     } return this.True
  //   }
  // }
}
</script> 