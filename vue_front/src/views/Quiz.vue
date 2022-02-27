<template>
  <div class="quiz-wrapper">
    
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>
      <div class='quiz-countainer'>
        <div  v-if="quizzes[0]&&questions[0]&&$store.state.isLoading==false">
          <div>
            <Start
            v-show='!this.$store.state.test'
            :showQuiz='showQuiz'
            :quizzes='quizzes'
            :questions='questions'
            @handle="handleSHowQuiz"/>
    
            <div v-if="showQuiz && counter < questions.length + 1">
              <progress v-if="showAnswerDetail==false" class="progress" :value="progress(counter,questions.length)" max="100"/>
              <div class=question-grade> 
                <p v-show="!this.$store.state.test" class='quiz-title'>初級</p>
                <p v-show="this.$store.state.test" class='quiz-title'>実力テスト</p>
              </div>              
              <div v-for="(question,questionindex) in questions.slice(a,b)"
                  v-bind:key="questionindex">
                <div class='question-wrapper'>
                  <div class="question-header"><i class='q'>Q</i>第{{ counter }}問</div>
                  <div class='question-body'>{{ question.label }}</div>
                </div>
              <div>
            </div>
            <div :class='showPic(question.image)'>
              <img  v-bind:src="question.get_image"/>
            </div>

                <!-- answer part -->
                
            <div class='answer-flex'    
              v-for="(answer,answerindex) in question.answer"
              v-bind:key="answerindex">
              <div class='answer-container' 
                @click="onClicked(answer,question.field)"
                :class="classHandler(sort,answer.label,selectedAnswer[0],question.field,answer.answer_id,selectedAnswerArray,question.correct_answer,counter)"
                >
                <div class='order-container'>
                  <p class="answer-index">{{ String.fromCharCode(answerindex+65) }}</p>
                </div>
                <p class="answer-label">{{ answer.label }}</p>
                <div class="order-space" v-if="question.field=='並び替え'&&showAnswerDetail==false">        
                    <p v-if="sort.includes(answer.answer_id)&&showAnswerDetail==false"
                    class ='order-num'
                    >{{sort.indexOf(answer.answer_id)+1}}</p>
                </div>

                <div class='' >
                  <div class="">
                    <div class='result-font' :class="getResultFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
                      v-if="question.field!='並び替え' && showAnswerDetail">
                      <i id='result-font' :class='returnFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))'></i>
                    </div>
                    <div class='result-font' :class="getResultFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))"
                      v-if="question.field=='並び替え' && showAnswerDetail">
                      <i id='result-font' :class='returnFont(getDetailFont(answer.answer_id,question.correct_answer,selectedAnswerArray,counter,question.field))'></i>
                    </div>
                </div>
                <div class=''
                  id='result-order-num'
                  v-if="question.field=='並び替え' && showAnswerDetail">
                  <p id='result-num' class='has-text-weight-bold	'>{{ question.correct_answer.indexOf(answer.answer_id)+1}}</p> 
                </div>
              </div>
            </div>

                  </div>
                  
                <button
                  class="button"
                  id='color-button'
                  v-show='selectedAnswer!="" && counter != questions.length && showAnswerDetail==false || sort.length==question.answer.length&&counter != questions.length'
                  @click="nextQuestion(sort,selectedAnswer,question.correct_answer,question.field)">Next ></button>
                <button
                class="button"
                id='color-button'
                v-show="selectedAnswer!=''&& counter == questions.length && showAnswerDetail==false ||sort.length==question.answer.length && counter == questions.length"
                  @click="showResult(sort,selectedAnswer,question.correct_answer,question.field)">Finish</button>

              <!-- detail part -->
              
              <div class="">
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
                  class=""
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
            <Result
              v-show='!this.$store.state.test'
              :question_length='questions.length'
              :rerultAnswer='rerultAnswer'
              @show='showDetail'/>
          </div>
       </div>
      </div>
    </div>
      <TestResult
        v-if='this.$store.state.test&&counter-1 == questions.length&&$store.state.isLoading==false'/>
      <transition name="notice">
        <Notification
          v-if='this.$store.state.notice&&counter-1 == questions.length'
          />
      </transition>
  </div>
</template>

<script>
import Result from '@/components/quiz_components/Result.vue'
import TestResult from '@/components/initial/TestResult.vue'
import Notification from '@/components/initial/Notification.vue'
import Start from '@/components/quiz_components/Start.vue'
import {mapGetters,mapActions} from 'vuex'
// import axios from 'axios'
export default {
  name: 'Quiz',
  components: {
    Result,
    Start,
    TestResult,
    Notification
  },  
  data(){
    return{
      counter: 1,
      selectedAnswer:'',
      rerultAnswer:[],
      sort: [],
      showQuiz: false,
      a: 0,
      b: 1,
      percentage:100,
      arreyCounter:-1,
      selectedAnswerArray:[],
      showAnswerDetail: false,
      }
  },
  created(){
    this.$store.commit('setIsLoading', true)
    this.getquiz()
    this.getquestions()
    this.testHandler()
    //   setTimeout(() =>{
    //   this.$store.commit('setIsLoading', false);
    // },2000)
    },
    beforeMount(){
    },
    mounted(){
      window.addEventListener('beforeunload', () => {
      this.$store.commit('reset')
    })
    },
    beforeDestroyed(){
      this.$store.commit('reset')
      console.log('beforDeth')
    },
  computed: mapGetters(['questions','quizzes']),

  methods:{
    ...mapActions(['getquiz','getquestions']),
    
    progress(counter,question_length){
      console.log(counter / question_length *100)
      return counter / question_length *100

    },
    testHandler(){
      if (this.$store.state.test==true){
        this.showQuiz=true}
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
        behavior: "smooth"
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
      this.scrollTop()
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
    getFont(result){
      if (result == true){
        return '○'
      }else{
        return'×'
      }
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
          return 'clicked'
          }
        else if (question_field =='並び替え'&&sort.includes(answer_id)){
          return 'clicked'
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
    showDetail(){
      this.scrollTop()
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
    getCorrectOrderClass(answer_id,correct_answer,selectedAnswerArray,counter,showAnswerDetail){
      return correct_answer.indexOf(answer_id)
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
  },
}
</script>
<style scoped lang="scss">
@import "style/_variables.scss";
  .quiz-wrapper{
    width:100vw;
    height:100vh;
  }
  .quiz-countainer{
    width:19rem;
    margin-left:auto;
    margin-right:auto;
    text-align: center;
  }
  .progress{
    margin-top:3rem;
  }
  .quiz-title{
    color:white;
    font-size: 1.5rem;
  }
  .question-wrapper{
            border: solid  rgba(243, 91, 36, 0.808);
            border-radius: 1rem;
            overflow:hidden;
        }
        .question-header{
            background: linear-gradient($base-lite,$base-color);
            color:white;
            padding:0.5rem;
            font-weight:bold;
            position:relative;
        }
        .q{
          position:absolute;
          left:5%;
          bottom:2%;
          font-size:1.5rem;
          
        }
        .question-body{
            background-color: rgb(253, 245, 239);
            padding:1rem;
            font-weight:bold;
        }

  .answer-container{
    border: 0.2rem solid rgb(110, 109, 108);
    border-radius: 50vh;
    background: white;
    margin-bottom:0.5rem;
    display:flex;
    position:relative;
    transition: 0.3s
    }
    .answer-container:hover{
      border: 0.2rem solid lighten($base-color,20%);
      }
    .answer-container.clicked{
      border: 0.2rem solid $base-color;
      .order-container{
        border: 0.2rem solid rgb(93, 93, 93);
        background:$base-color;
        color:white;
        .answer-index{
          color:white;
        }
      }
    }
      .order-container{
        height: 2.5rem;
        width: 2.5rem;
        border: 0.2rem solid $base-color;
        border-radius: 50%;
        margin-left:0.5rem;
        position:relative;
        color:grey;
        transition: 0.3s
      }
      .answer-index{
        font-size:1.5rem;
        position:absolute;
        left:0;
        right:0;
        top:0;
        color:grey;
        font-weight: bold;
  }
  .answer-label{
    position:absolute;
    height: 50%;
    left:0;
    right:0;
    bottom:0;
    top:0;
    margin:auto;
    color:rgb(48, 48, 48);
  }
  .order-space{
    position:absolute;
    right:0;
    top:0;
    bottom:0;
    // border: 0.1rem solid black;
    // border-radius: 10%;
    box-sizing: content-box;
    margin-right:1rem;
    display:flex;
    justify-content: center;
    align-items: center;
    // height: 90%;
    // width: inherit;
  }
  .order-num{
    text-align: center;
    font-size: 1.5rem;
    font-weight:bold;
    color:rgb(93, 93, 93);
  }
  .button{
    margin-bottom: 1rem;
  }
// @import "style/_variables.scss";
//   #quiz-wrapper{
//     width: 100vw;
//     height: 100vh;
//   }
// /* this is for Iphone */
//   @media(max-width: 767px){
//   // #quiz-wrapper{
//   //   padding-top:5vw;
//   // }
//   #resultString{
//       display: none ;
//     }
//   #answer-label{
//     font-weight:bold;
//      }
//   #result-order-num{
//     height: 3rem;
//     }
//   #result-num{
//     font-size: 2rem;
//     }
//   .result-all{
//     font-size: 1.5rem;
//     }
//   }
//   /* between Iphone and Ipad*/
//   @media(min-width: 415px) and (max-width: 767px){

//   }
//   // wider than ipad include ipad
//   @media(min-width: 768px) and (max-width: 1024px){
//   #wrapper-quiz{
//     // border: solid lighten( $base-color, 30% );
//     // border-radius: 3rem;

//     margin-left: 8rem;
//     margin-right: 8rem;
//   }
//   #answer-container{
//     // width: 300px;
//     height: 5rem;
//   }
//   #answer-label{
//     position: absolute;
//     // padding-top:0.5rem;
//     font-size: 2rem;  
//     }
//   #answer-index{
//     font-size: 1.7rem;
//     position: absolute;
//   }
//   #order-container{
//     width: 3rem;
//     height: 3rem;
//   }
//   #order-space{
//     padding: 1.5rem;
//     margin-right: 0.5rem;
//   }
//   #order-num{
//     font-size: 2rem;
//     font-weight:bold;
//   }
//   #result-order-num{
//     width: 3rem;
//     height: 5rem;
//     font-size: 2rem;
//   }
//   .detailClassHandler{
//     font-size: 10rem
//   }
//   .result-all{
//     font-size: 2rem;
//   }
  
//   }
//   // for desktop include ipadpro
//   @media(min-width: 1024px){
//     #wrapper-quiz{
//     margin-left: 16rem;
//     margin-right: 16rem;
//     }
//   }
//   #wrapper-quiz{
//     padding: 2rem;

//     }
//   .result{
//     border: solid lighten( $base-color, 30% );
//   }
//   #result-column{
//     border-bottom: solid rgb(231, 221, 221);
//     margin-right: 2rem;
//     margin-left: 2rem;
//     margin-bottom: 2rem;
//   }
//   .result-all{
//     margin-right:1rem;
//     .result-font-green{
//       color: green;
//     }
//     .result-font-red{
//       color:red;
//     }
//   }
//   #order-space{
//     text-align: right;
    
//   }
//   .question-wrapper{
//             border: solid  rgba(243, 91, 36, 0.808);
//             border-radius: 1rem;
//             overflow:hidden;
//             margin-top: -1rem;
//             // margin-left: auto;
//             // margin-right: auto;
//         }
//         .question-header{
//             background: linear-gradient($base-lite,$base-color);
//             color:white;
//             padding:0.5rem;
//             font-weight:bold;
//             position:relative;
//         }
//         .q{
//           position:absolute;
//           left:5%;
//           bottom:2%;
//           font-size:1.5rem;
          
//         }
//         .question-body{
//             background-color: rgb(253, 245, 239);
//             padding:1rem;
//             font-weight:bold;
//         }
//   #answer-container{
//     transition:0.3s;
//     border-radius: 2vh;
//     border: 0.1rem solid black;
//   }
//   #order-container{
//     background: transparent;
//     color:black;
//     border: 0.1rem solid black;
//     transition:0.3s;
//     }
//   #answer-index{
//     transition:0.3s;
//     color:white;
//   }
//   #answer-container:hover{
//     border:0.1rem solid $base-color;
//     }
//   #answer-container:hover #order-container{
//     border:0.1rem solid $base-color;
//     }
//   #answer-container:hover #order-container #answer-index{
//     color: $base-color;
//   }
//   #answer-button{
//     background: none;
//     color:white;
//     border: 0.1rem solid  $base-color;
//     transition:0.3s;
//   }
//   #answer-button:hover{
//     background: $base-color;
//     color:white;
//     font-weight: bold;
//     border: 0.1rem solid  darken($base-color,10%);
//   }
  
  // .notice-enter-from{
  //   opacity: 0;
  // }
  // .notice-enter-to{
  //   opacity: 1 ;
  // }
  // .notice-enter-active, .notice-leave-active {
  // transition: opacity .5s;
  // }
</style>
