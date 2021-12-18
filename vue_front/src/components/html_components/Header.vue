<template>
  <div class="header-wrapper">
      <nav class="navbar is-transparent">
          <div class="navbar-brand">
            <a class="navbar-item is-paddingless">
                <router-link @click="storeReset" to="/" >
                    <img src="@/assets/logo.png">
                </router-link>
            </a>
            <a class="navbar-burger" @click="showMobileMenu = !showMobileMenu">
              <button v-if='showMobileMenu==true' class="delete mt-3 is-large"></button>
                <div v-if='showMobileMenu==false'>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
            </a>
          </div>      
          <div class='navbar-menu' :class="{'is-active': showMobileMenu }">
            <div class="navbar-end is-expanded" @click="showMobileMenu =false">
                <router-link to="/" @click="storeReset" class="navbar-item has-text-white"><i class="fas fa-home" ></i>Home</router-link>
                <router-link to="/quiz" class="navbar-item is-spaced has-text-white"><i class="fas fa-lightbulb"></i>Quiz</router-link>
                <router-link to="/test" class="navbar-item has-text-white"><i class="fab fa-aws"></i>Test</router-link>
            </div>
          </div>
      </nav>
  </div>
</template>

<script scoped>
export default {
    data(){
        return{
            showMobileMenu: false
        }
    },
    methods:{
    storeReset(){
          this.$store.commit('reset')
    }
  }
}
</script>

<style lang=scss>
  .navbar {
    &.is-transparent {
      background-color: transparent;
      background-image: none;
      }
    }
  .navbar-end{
    color:white;
  }

</style>