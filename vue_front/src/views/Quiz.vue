<template>
  <div id="wrapper">
    <!-- <div v-show='$store.state.isLoading'>
           <div class="fas fa-spinner fa-pulse">{{}}</div>
    </div> -->
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>
      <div class="section is-paddingless" v-if="quizzes[0]&&questions[0]">
        <div id="wrapper-quiz">
        <div class='container'>
          
          <div v-if="!showQuiz" @click="handleSHowQuiz">
            <p class="title is 3">{{quizzes[0].name}}問題</p>
            <p class="subtitle is 4">全{{questions.length}}問</p>
            <button id='ko'>START</button>
          </div>
          <div v-if="showQuiz && counter < questions.length + 1">
            <progress v-if="showAnswerDetail==false" class="progress is-warning is-marginless mb-1" :value="progress(counter,questions.length)" max="100"/>
            <div class="is-size-1-tablet  title is-size-4-mobile"> 
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
              
              <div class='columns is-mobile is-vcentered'    
                v-for="(answer,answerindex) in question.answer"
                v-bind:key="answerindex">
                <div class="py-5 is-three-fifths-tablet button is-paddingless has-background-light is-fullwidth my-2" 
                  @click="onClicked(answer,question.field)"
                  :class="classHandler(sort,answer.label,selectedAnswer[0],question.field,answer.answer_id,selectedAnswerArray,question.correct_answer,counter)"
                  id='answer-container'>
                  <div class='column'>
                    <div id ='order-container' class='button is-pulled-left is-small  px-4 is-rounded has-background-dark has-text-white has-text-weight-bold is-size-6-mobile is-static'>
                      <p id="answer-index">{{ answerindex+1 }}</p>
                    </div>
                  </div>
                  <p
                  class="is-overlay mt-4  has-text-grey-darker"
                    id='answer-label'>{{ answer.label }}
                  </p>
                  <div v-if="question.field=='並び替え'&&showAnswerDetail==false">
                    <div class='column' >
                      <div id='order-space' class="button is-small is-rounded has-background-warning-light has-text-warning-dark">
                        <p v-if="sort.includes(answer.answer_id)&&showAnswerDetail==false"
                        class ='is-size-4-mobile mt-1 has-text-warning-dark'
                        id='order-num'
                        style='position:absolute'>{{sort.indexOf(answer.answer_id)+1}}</p>
                      </div>
                    </div>  
                  </div>

                
                  <div class='columns is-mobile is-vcentered' id='result'>
                    <div class="column result-all">
                      <div class='result-font' :class="getResultFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
                        v-if="question.field!='並び替え' && showAnswerDetail">
                        <i id='result-font' :class='returnFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))'></i>
                      </div>
                      <div class='result-font' :class="getResultFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
                        v-if="question.field=='並び替え' && showAnswerDetail">
                        <i id='result-font' :class='returnFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))'></i>
                      </div>
                  </div>
                  <div class='button px-2 is-paddingless ml-1 has-background-warning-light has-text-primary-dark is-static'
                    id='result-order-num'
                    v-if="question.field=='並び替え' && showAnswerDetail">
                    <p id='result-num' class='has-text-weight-bold	'>{{ question.correct_answer.indexOf(answer.answer_id)+1}}</p> 
                  </div>
                </div>
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

            <!-- detail part -->
            
            <div class="buttons has-addons is-centered">
              <p class="control">
                <button
                  class="button"
                  v-show="counter != questions.length && showAnswerDetail&& counter!=1 ||showAnswerDetail&&counter!=1"
                    @click="detailHandler('back')">
                    ＜ Back
                </button>
              </p>
              <p class="control">
                <button
                class="button has-background-danger-light is-paddingless px-2 has-text-danger-dark"
                v-show="showAnswerDetail"
                  @click="detailHandler('backToResult',QL=questions.length)">結果に戻る
                </button>
              </p>
              <p class="control">
                <button
                class="button"
                v-show='counter != questions.length && showAnswerDetail'
                  @click="detailHandler('next')">Next ＞</button>
              </p>
            </div>
          </div>
        </div>
        <!-- //result page// -->
        
        <div v-if="showQuiz && showAnswerDetail==false && counter > questions.length">
          <div class='box is-paddingless pb-4'> 
            <div class='button my-5 has-background-info-light is-centered is-static'>
              <p class="title is 3 has-text-danger">結果発表</p>          
            </div>
            <div>
              <p class="mx-5 is-inline-block subtitle is 4">{{ questions.length }}問中</p>
              <p class="is-inline-block has-text-danger-dark title is 4">{{ numOfTrue(rerultAnswer) }} 問正解</p>
              <div>
                <p class="subtitle is 5 button is-rounded is-static"> 正解率 {{ getPercentage(numOfTrue(rerultAnswer),questions.length) }}%</p>
              </div>
            </div>
          </div>
          <section class="section">
            <div class='result pt-6'>
              <div class="columns is-multiline is-vcentered is-mobile is-centered"
                v-for="(result,resultindex) in rerultAnswer.slice(0,resultDetailslice)"
                v-bind:key="resultindex"
                style='margin-top: -2rem'
                id='result-column'>
                <div class="column">
                  <p class='subtitle'>{{ resultindex+ 1 }} 問目</p>
                </div>
                <div class="column result-all">
                  <div class='result-font' :class='getResultFont(result)'>
                    <i id='result-font' :class='returnFont(result)'></i>
                  </div>
                </div>
                <div class="column" id='resultString'>
                  <p class='subtitle is 4'>{{ getJPResult(result) }}</p>
                </div>
              </div>
              <div style='margin-top: -2rem'>
                <div class='mt-6' v-if='!resultDetail' @click='resultDetailHandler(resultDetailslice)'>
                  <i class="fas fa-chevron-circle-down fa-2x" style='color: lightgray'></i>  
                </div>

                <div v-if='resultDetail' @click='resultDetailHandler(resultDetailslice)'>
                  <i class="fas fa-chevron-circle-up fa-2x" style='color: lightgray'></i> 
                </div>
              </div>
            </div>
            <div>
                <button @click='showDetail' class="button mt-2 is-info is-rounded">詳細を見る</button>
            </div>    
          </section>
        
            <!-- <table class='is my-5 table is-fullwidth is-hoverable' v-for="(result,resultindex) in rerultAnswer"
              v-bind:key="resultindex">
              <tr>
                <td> 
                  <p class='mx-5 is-inline-block subtitle is 4'>{{ resultindex+ 1 }}問目</p>
                  <p class='mx-6 title is-1 has-text-link is-inline-block subtitle is 4'
                  :class="{'has-text-danger':result==true}">{{ getFont(result) }}</p>
                  <p class='is-inline-block subtitle is 4'>{{  getJPResult(result) }}</p>
                </td>
              </tr>
            </table> -->
           
          <router-link to="/" class="mx-2 button is-primary is-outlined">戻る</router-link>
          <a href="/quiz" class="mx-2 button is-warning is-light">もう一度</a>
        </div>
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
      showAnswerDetail: false,
      resultDetailslice:3,
      resultDetail: false
      }
  },
  mounted:function() {
    this.getquiz()
    this.getQuestion()
    this.getOneQuestion()
  },
  methods:{
    async getquiz(){
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/quizzes/?id=2')
        .then(response => (this.quizzes = response.data))
        .catch(error => {
                      console.log(error)
                  })
      },
    async　getQuestion(){
    await　axios
      .get('/api/questions/quizzes/?quiz=2&num=3')
      // .get('/api/questions/fields/?field=並び替え&num=3')
      // .get('/api/questions/fields/?field=絵&num=1')
      .then(response => (this.questions = this.getRandomQuestion(response.data)))
      this.$store.commit('setIsLoading', false)
    },
    progress(counter,question_length){
      console.log(counter / question_length *100)
      return counter / question_length *100

    },
    handleSHowQuiz(){
      this.showQuiz = !this.showQuiz
    },
    nextQuestion(sort,selectedAnswer,question_correct_answer,question_field){
      this.scrollTop()
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
    scrollTop(){
      window.scrollTo({
        top: 0,
        behavior: "auto"
      });
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
        return 'my-4 has-background-link-light image is-96x96 is-inline-block'
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
    resultDetailHandler(slice){
      if(slice <= 5){
        console.log(this.resultDetailslice)
        this.resultDetailslice = 100
        this.resultDetail = true
      }
      else{
        this.resultDetailslice = 3
        this.resultDetail = false
      }
    },
    
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
      this.scrollTop()
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
          return true
        }
        else if(answer_id!=correct_answer && selectedAnswerArray[counter-1] ==answer_id){
          return false
        }
        else{console.log('none')}
      }
      else if(question_field =='並び替え'){
        if(selectedAnswerArray[counter-1].indexOf(answer_id) == correct_answer.indexOf(answer_id)){
          return true
        }
        else if(selectedAnswerArray[counter-1].indexOf(answer_id) != correct_answer.indexOf(answer_id))
        return false
       }
       
    },
    // detailClassHandler(a){
    //   if(a == '○'){
    //     return'is-size-1 is-marginless has-text-primary-dark'
    //   }
    //   else if(a == '×'){
    //     return'iis-size-1 s-marginless has-text-danger-dark'
    //   }
    // },
    getCorrectOrderClass(answer_id,correct_answer,selectedAnswerArray,counter,showAnswerDetail){
      return correct_answer.indexOf(answer_id)
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
    returnFont(boolean){
      if(boolean == true){
        return "far fa-circle"
      }
      else if(boolean == false){
        return "fas fa-times"
      }
    },
    getResultFont(result){
      if(result == true){
        return "result-font-green"
      }
      else if(result == false){
        return "result-font-red"
      }
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
<style lang="scss">
@import "style/_variables.scss";
/* this is for Iphone */
  @media(max-width: 767px){
  #resultString{
      display: none ;
    }
  #answer-label{
    font-weight:bold;
     }
  #result-order-num{
    height: 3rem;
    }
  #result-num{
    font-size: 2rem;
    }
  .result-all{
    font-size: 1.5rem;
    }
  }
  /* between Iphone and Ipad*/
  @media(min-width: 415px) and (max-width: 767px){

  }
  // wider than ipad include ipad
  @media(min-width: 768px){
  #wrapper-quiz{
    border: solid lighten( $base-color, 30% );
    border-radius: 3rem;
    margin-left: 3rem;
    margin-right: 3rem;
  }
  #answer-container{
    // width: 300px;
    height: 5rem;
  }
  #answer-label{
    position: absolute;
    // padding-top:0.5rem;
    font-size: 2rem;  
    }
  #answer-index{
    font-size: 1.7rem;
    position: absolute;
  }
  #order-container{
    width: 3rem;
    height: 3rem;
  }
  #order-space{
    padding: 1.5rem;
    margin-right: 0.5rem;
  }
  #order-num{
    font-size: 2rem;
    font-weight:bold;
  }
  #result-order-num{
    width: 3rem;
    height: 5rem;
    font-size: 2rem;
  }
  .detailClassHandler{
    font-size: 10rem
  }
  .result-all{
    font-size: 2rem;
  }
  
  }
  // for desktop include ipadpro
  @media(min-width: 1024px){

  }
  #wrapper-quiz{
    padding: 2rem;
    }
  .result{
    border: solid lighten( $base-color, 30% );
  }
  #result-column{
    border-bottom: solid rgb(231, 221, 221);
    margin-right: 2rem;
    margin-left: 2rem;
    margin-bottom: 2rem;
  }
  .result-all{
    margin-right:1rem;
    .result-font-green{
      color: green;
    }
    .result-font-red{
      color:red;
    }
  }
  #order-space{
    text-align: right;
    
  }
  // #result{
  //   .result-all{
  //     text-align: right;
  //   }
  // }
 
</style>
