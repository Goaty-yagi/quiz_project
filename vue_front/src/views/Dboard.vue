<template>
    <div class="dashboard-wrapper" >
        <div class="">
            <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
                <div class="lds-dual-ring"></div>
            </div>
            <div class="dashboard-container" v-if="$store.state.isLoading==false">
                <div class="header-flex">
                    <h1 class='title-white'>ダッシュボード</h1>
                </div>
                <div class="side-bar" :class="{'less-side-bar':showSideBar==false}">
                    <i @click="handleShowSideBar()" class="fas fa-backspace"></i>
                </div>
            </div>
        </div>
        <CreateQuizQuestion/>
    </div>
</template>

<script>
import CreateQuizQuestion from '@/components/dashboard/CreateQuizQuestion.vue'

export default {
    components: {
        CreateQuizQuestion
    },
    data(){
        return{
            showSideBar: true,
        }
    },
    mounted(){
        console.log('mounted at dashboard',this.showSideBar)
    },
    methods:{
        handleShowSideBar(){
            console.log(this.showSideBar)
            this.showSideBar = !this.showSideBar 
            console.log(this.showSideBar)
        }
    }
}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";



.dashboard-wrapper{
    width: 100%;
    margin: 0;
    // display: flex;
    // justify-content: center;
    .side-bar{
        position: absolute;
        left: 0;
        margin-top: 1rem;
        background: $dark-tr-blue;
        width: 20%;
        height: 75vh;
        transition: .5s;
        .fa-backspace{
            position: absolute;
            right: 0;
            color: $lite-gray;
            padding-top: 0.5rem;
            padding-right: 0.5rem;
        }
    }
    .less-side-bar{
        width: 5%;
    }
    .main-wrapper{
        .dashboard-container{
            // flex-direction: column;
            // justify-content: center;
            // align-items: center;
            margin: 0;
            width: 100%;
        }
    }
}
</style>