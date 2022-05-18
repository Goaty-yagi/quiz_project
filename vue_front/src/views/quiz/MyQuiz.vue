<template>
    <div class="my-quiz-wrapper" :class="{'scroll-fixed':fixedScroll}">
        <div class="main-wrapper">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <!-- <i class="fas fa-cog"></i> -->
                <div class="lds-dual-ring"></div>
            </div>
            <!-- <QuizP
            v-if="componentHandleDict.quiz"
            :forQuizPageInfo="forQuizPageInfo"
            @backQuizHome="backQuizHome"/> -->
            <div class="my-quiz-header">
                <p class="title-white">My-Quiz</p>
                <p class="register">登録数３\５</p>
                <p class="max">(最大５個まで登録できます)</p>
            </div>
            
            <div class="my-quiz-container l-container" v-if="$store.state.isLoading==false">
            </div>
            <div class="btn-basegra-white-db-sq">
                練習
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters,mapActions} from 'vuex'
import NotVerified from '@/components/login/NotVerified.vue'
import QuizP from '@/components/quiz_components/QuizP.vue'

export default {
    components: {
        QuizP,
        NotVerified,
    }, 

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.my-quiz-wrapper{
    .main-wrapper{
        .my-quiz-header{
            margin-bottom: 1rem;
            .register{
                font-size: 1.3rem;
                color: $lite-gray;
                font-weight: bold;
            }
            .max{
                font-size: 0.8rem;
                color: $lite-gray;
            }
        }
        .my-quiz-container{
            width: 100%;
            min-height: 400px;
           
        }
        .btn-basegra-white-db-sq{
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-top: 0.2rem;
            padding-bottom: 0.2rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            font-weight: bold;
            font-size: 1.2rem;

        }

    }

}
</style>