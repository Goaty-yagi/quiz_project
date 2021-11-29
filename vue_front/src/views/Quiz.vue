<template>
  <div id="wrapper">
    <div class="section is-paddingless" v-if="quizzes[0]&&questions[0]">
      <div class='container-'>
        <div v-if="!showQuiz" @click="handleSHowQuiz">
          <p class="title is 3">{{quizzes[0].name}}問題</p>
          <p class="subtitle is 4">全{{questions.length}}問</p>
          <button>START</button>
        </div>
      <!-- <div v-show="counter > quizzes[0].question.length">
        <p class="title is-3">Result</p>
      </div> -->
      <div v-if="showQuiz && counter < questions.length + 1">
        <div class="i is-size-1-tablet title is-size-3-mobile"> 
          <p>初級</p>
          <p class=" button is-small is-static is-rounded is-active is-size-6-tablet ">第{{ counter }}問</p>
        </div>
        <div v-for="(question,questionindex) in questions.slice(a,b)"
            v-bind:key="questionindex">
          <div>
            <p class='button has-background-link subtitle-4 has-text-link-light is-hovered is-static'>
            {{ question.label }}
            </p>
          </div>
          <div :class='showPic(question.image)'>
            <img  v-bind:src="question.get_image"/>
          </div>
          <!-- answer part -->
          <!-- :class="{'has-background-primary-light has-text-white is-hovered':answer.label == selectedAnswer[0]&&question.field !='並び替え'}" -->
          <div class='columns is-vcentered is-centered is-mobile'    
            v-for="(answer,answerindex) in question.answer"
            v-bind:key="answerindex">
            <div class="py-6 is-three-fifths-tablet button has-background-light is-fullwidth my-4" 
              @click="onClicked(answer,question.field)"
              :class="classHandler(sort,answer.label,selectedAnswer[0],question.field,answer.answer_id,selectedAnswerArray,question.correct_answer,counter)"
              >
              <div class='column'>
                <p class='button is-pulled-left has-background-dark has-text-white is-static is-inline-block'>{{ answerindex+1 }}</p>
              </div>
              <p
              class="column is-overlay mt-5 subtitle is-marginless has-text-centered　has-text-grey-darker"
              >{{ answer.label }}</p>
              <div v-if="question.field=='並び替え'&&showAnswerDetail==false">
                <div class="column-1 is-marginless button is-vcentered is-medium is-rounded has-background-warning-light has-text-warning-dark">
                  <p v-if="sort.includes(answer.answer_id)&&showAnswerDetail==false"
                  class ='is-overlay title is 4 mt-2 has-text-warning-dark'>{{sort.indexOf(answer.answer_id)+1}}</p>
                </div>
              </div>
              <p :class="detailClassHandler(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
              v-if="question.field!='並び替え' && showAnswerDetail">
              {{ getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field) }}
              </p>
              <div :class="detailClassHandler(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
              v-if="question.field=='並び替え' && showAnswerDetail">
              {{ getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field) }}
              </div>
            </div>
              <div class='button is-1 py-6 ml-3 has-background-warning-light has-text-primary-dark is-static'
              v-if="question.field=='並び替え' && showAnswerDetail">
              <p class='is-size-3  has-text-weight-bold	'>{{ question.correct_answer.indexOf(answer.answer_id)+1}}</p> 
              </div>
          </div>
          <button
          class="button is-link is-rounded"
          v-show='selectedAnswer!="" && counter != questions.length && showAnswerDetail==false || sort.length==question.answer.length&&counter != questions.length'
            @click="nextQuestion(sort,selectedAnswer,question.correct_answer,question.field)">Next ></button>
          <button
          class="button is-info is-rounded"
          v-show="selectedAnswer!=''&& counter == questions.length && showAnswerDetail==false ||sort.length==question.answer.length && counter == questions.length"
            @click="showResult(sort,selectedAnswer,question.correct_answer,question.field)">Finish</button>

          <!-- for detail -->
          <button
          class="button is-info is-rounded"
          v-show="counter != questions.length && showAnswerDetail&& counter!=1 ||showAnswerDetail&&counter!=1"
            @click="detailHandler('back')">＜ Back</button>
            <button
          class="button mx-2 has-background-danger-light has-text-danger-dark"
          v-show="showAnswerDetail"
            @click="detailHandler('backToResult',QL=questions.length)">結果に戻る</button>
          <button
          class="button is-link is-rounded"
          v-show='counter != questions.length && showAnswerDetail'
            @click="detailHandler('next')">Next ＞</button>
        </div>
      </div>
      <!-- //result page// -->
      <div v-if="showQuiz && showAnswerDetail==false && counter > questions.length">
        <div class='py-5 my-5 button has-background-info-light is-static'>
          <p class="title is 3 has-text-danger">結果発表</p>          
        </div>
        <div class=box> 
            <div class="mx-5 is-inline-block subtitle is 4">{{ questions.length }}問中</div>
            <div class="is-inline-block has-text-danger-dark title is 4">{{ numOfTrue(rerultAnswer) }} 問正解</div>
            <div>
              <p class="subtitle is 5 button is-rounded is-static"> 正解率 {{ getPercentage(numOfTrue(rerultAnswer),questions.length) }}%</p>
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
              <button @click='showDetail' class="button is-info is-rounded">詳細を見る</button>
        </div>
          <router-link to="/" class="mx-2 button is-primary is-outlined">Home</router-link>
          <a href="/quiz" class="mx-2 button is-warning is-light">もう一度</a>
      </div>
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
      sort: [],
      showQuiz: false,
      a: 0,
      b: 1,
      hover: false,
      percentage:100,
      test:[],
      arreyCounter:-1,
      selectedAnswerArray:[],
      showAnswerDetail: false
      }
  },
  mounted:function() {
    this.getquiz()
    this.getQuestion()
    this.getOneQuestion()
  },
  methods:{
    getquiz(){
    axios
    .get('/api/quizzes/?id=2')
    .then(response => (this.quizzes = response.data))
    },
    getQuestion(){
    axios
    .get('/api/questions/quizzes/?quiz=2&num=7')
    // .get('/api/questions/fields/?field=並び替え&num=3')
    // .get('/api/questions/fields/?field=絵&num=1')
    .then(response => (this.questions = this.getRandomQuestion(response.data)))
    },
    handleSHowQuiz(){
      this.showQuiz = !this.showQuiz
    },
    nextQuestion(sort,selectedAnswer,question_correct_answer,question_field){
      this.a += 1
      this.b += 1
      this.checkCorrectAnswer(sort,selectedAnswer[1],question_correct_answer)
      this.selectedAnswer = ''
      this.counter += 1
      if(question_field !='並び替え'){
        this.selectedAnswerArray.push(selectedAnswer[1])
      }
      else if(question_field =='並び替え'){
        this.selectedAnswerArray.push(this.sort)
        this.sort = []
        this.arreyCounter= -1
      }
      console.log('slevtedID',selectedAnswer[1],'CA',question_correct_answer)
      console.log('resultAnswer',this.rerultAnswer)
      console.log('selectedAnswerArray',this.selectedAnswerArray)
    },
    onClicked(answer,question_field){
      if(this.showAnswerDetail == false)
      if (question_field != '並び替え'){
        this.selectedAnswer = [answer.label,answer.answer_id] 
        console.log('answer_id',answer.answer_id)
      }
      else if(this.sort.includes(answer.answer_id)){
        let tempArray =  this.deleteStringArray(answer.answer_id)
        this.sort = tempArray.slice(0)
        console.log(this.sort)
        
      }
      else{
        this.arreyCounter += 1
        this.sort[this.arreyCounter]=answer.answer_id
        
        console.log('pushed',answer.answer_id,'counter',this.arreyCounter)
        console.log(this.sort)
      }
    },
    showResult(sort,selectedAnswer,question_correct_answer,question_field){
      this.checkCorrectAnswer(sort,selectedAnswer[1],question_correct_answer)
      this.selectedAnswer = ''
      this.counter += 1
      if(question_field !='並び替え'){
        this.selectedAnswerArray.push(selectedAnswer[1])
      }
      else if(question_field =='並び替え'){
        this.selectedAnswerArray.push(this.sort)
        this.sort = []
        this.arreyCounter= -1
      }
    },
    checkCorrectAnswer(sort,answer_id,correct_answer){
      if(this.arrayEqual(sort,correct_answer)||answer_id == correct_answer){
        this.rerultAnswer.push(true)
      }else{
        this.rerultAnswer.push(false)
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
    getPercentage(answer,question_length){
      return Math.round(answer/question_length * 100)
    },
    showPic(pic){
      if (pic){
        return 'my-4 has-background-link-light image is-128x128 is-inline-block'
      }
    },
    arrayEqual(array1,array2){
      if (!Array.isArray(array1))    return false;
      if (!Array.isArray(array2))    return false;
      if (array1.length != array2.length) return false;
      for (var i = 0, n = array1.length; i < n; ++i) {
        if (array1[i] !== array2[i]) return false;
      }
      return true;
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
    },
    deleteStringArray(answer_id){
      let tempArray = this.sort.slice(0)
      if (tempArray.length > 1){
        for (let i of tempArray){
          if (i == answer_id){
            let temp = this.deleteValIndex(tempArray,i)
            this.arreyCounter-=1
            return temp
            }
        }
        // sort has more then 2
      }else{
        let tmp = this.deleteValIndex(tempArray,tempArray[this.arreyCounter])
        this.arreyCounter-=1
        return tmp
        }
    },
    deleteValIndex(array,val){
      let copiedArray = array.slice(0)
      let resultArray = []
      if(array.includes(val)){
        for( let i of copiedArray){
          if (i == val){
            delete copiedArray[copiedArray.indexOf(i)]
            }
          }
        }
        if(copiedArray != []){
          for (let k of copiedArray){
            if (k == null)continue;
            resultArray.push(k)
          }
          return resultArray
      }
      else{
        return console.log('not proper array and val')
      }
    },
    classHandler(sort,answer_label,selectedAnswer,question_field,answer_id,selectedAnswerArray,correct_answer,counter){
      console.log(sort)
      if(this.showAnswerDetail==false){
        if (question_field !='並び替え'&& answer_label == selectedAnswer){
          return 'has-background-primary-light has-text-white is-hovered'
          }
        else if (question_field =='並び替え'&&sort.includes(answer_id)){
          return 'has-background-primary-light has-text-white is-hovered'
          }
        // detail
       }
      else if(this.showAnswerDetail==true && question_field !='並び替え'){
          if (correct_answer == answer_id){
          return 'has-background-primary-light has-text-white is-static is-hovered'
        }
          else if(correct_answer != answer_id && selectedAnswerArray[counter-1] == answer_id){
            return 'has-background-danger-light has-text-white is-static is-hovered'
          }
       }
      else if(question_field =='並び替え'){
          if(selectedAnswerArray[counter-1].indexOf(answer_id) == correct_answer.indexOf(answer_id)){
              return 'has-background-primary-light has-text-white is-static is-hovered'
          }
          else if(selectedAnswerArray[counter-1].indexOf(answer_id) != correct_answer.indexOf(answer_id)){
              return 'has-background-danger-light has-text-white is-static is-hovered'
          }
       }
    },
    // detail
    showDetail(){
      this.a =0
      this.b =1
      this.counter =1
      this.showAnswerDetail = true
      console.log(this.selectedAnswerArray)
    },
    detailHandler(direction,QL=false){
      console.log(direction)
      console.log(this.showAnswerDetail)
      if(direction == 'next'){
        this.a +=1
        this.b +=1
        this.counter +=1
        this.showAnswerDetail = true
        return this.counter
      }
      if(direction == 'back'){
        this.a -=1
        this.b -=1
        this.counter -=1
      }else{
        this.counter = QL+1
        this.showAnswerDetail = false
      }
    },
    getDetailFont(answer_id,correct_answer,selectedAnswerArray,counter,question_field){
      if(question_field !='並び替え'){
        if (answer_id == correct_answer){
          return '○'
        }
        else if(answer_id!=correct_answer && selectedAnswerArray[counter-1] ==answer_id){
          return'×'
        }
      }
      else if(question_field =='並び替え'){
        if(selectedAnswerArray[counter-1].indexOf(answer_id) == correct_answer.indexOf(answer_id)){
          return '○'
        }
        else if(selectedAnswerArray[counter-1].indexOf(answer_id) != correct_answer.indexOf(answer_id))
        return '×'
       }
       else{
         return '    '
       }
    },
    detailClassHandler(a){
      if(a == '○'){
        return'is-size-1 is-marginless has-text-primary-dark'
      }
      else if(a == '×'){
        return'is-size-1 is-marginless has-text-danger-dark'
      }
    },
    getCorrectOrderClass(answer_id,correct_answer,selectedAnswerArray,counter,showAnswerDetail){
      return correct_answer.indexOf(answerid)
    },
    numOfTrue(answered_array){
      let counter = 0
      console.log('innum_resultanswer',this.rerultAnswer)
      console.log('anarray',answered_array)
      for (let t of answered_array){
        if(t == true){
          counter += 1
        }console.log('numcounter',counter)
      }return counter
    },
    getOneQuestion(){
    axios
    // test
    .get('/api/onequestion/?label=並び替え')
    .then(response => (this.test = response))
    },
    consoleTest(i){
    console.log('test',i)
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
<style>
  /* @media(min-width: 480px){
    #wrapper{
      background-color: blueviolet;
    }
  } */

</style>
