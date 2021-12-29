<template>
    <div class='mobile-header-wrapper'>
        <div class="mobilemenu-wrapper">
            <router-link to="/" @click="storeReset" class="nav-mobile-item"><i class="fas fa-home" ></i><p>Home</p></router-link>
            <router-link to="/"  class="nav-mobile-item"><i class="fas fa-robot"></i><p>Account</p></router-link>
            <router-link to="/"  class="nav-mobile-item"><i class="far fa-comments"></i><p>Comunity</p></router-link>
            <router-link to="/"  class="nav-mobile-item"><i class="far fa-lightbulb"></i><p>Quiz</p></router-link>
            <router-link to="/"  class="nav-mobile-item"><i class="fas fa-cog"></i><p>その他</p></router-link>
        </div>
    </div>
</template>

<script>
export default {
    methods:{
    storeReset(){
          this.$store.commit('reset')
        },
    }
}
</script>

<style scoped>
.mobilemenu-wrapper{
    position:absolute;
    width:100%;
    display: flex;
    justify-content: center;
    bottom:0;
  }
.nav-mobile-item{
    font-size:0.8rem;
    color: white;
    border:0.1rem solid white;
    position:flex;
    flex-direction: column;
    flex-basis:20%;
    padding-left:0.1rem;
    padding-right:0.1rem;
    background:rgba(255, 255, 255, 0.3);
    transition:0.5s;
  }
  .nav-mobile-item:hover{
    background:rgba(255, 255, 255, 0.5);
  }
</style>