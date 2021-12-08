<template>
  <div id="wrapper">
    <div>
      <nav class="navbar is-dark　is-mobile">
          <div class="navbar-brand">
            <a class="navbar-item">
                <router-link to="/" >何を学ぶ</router-link>
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
              <!-- <div  @click="showMobileMenu =false"> -->
                <router-link to="/" class="navbar-item"><i class="fas fa-home"></i>Home</router-link>
                <router-link to="/quiz" class="navbar-item is-spaced"><i class="fas fa-lightbulb"></i>Quiz</router-link>
                <router-link to="/test" class="navbar-item"><i class="fas fa-home"></i>Test</router-link>
              <!-- </div> -->
            </div>

          </div>
      </nav>
      <section class="section">
          <router-view/>
      </section>

      <footer class="footer">
          <p class="has-text-centered">Copyright (c) 2021</p>
      </footer>
    </div>
  </div>
</template>

<script>
export default{
  
  data(){
    return{
      showMobileMenu: false
    }
  }
}
</script>


<style lang="scss">
@import '../node_modules/bulma';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid rgb(214, 9, 9);
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

  // #nav {
  //   padding: 30px;

  //   a {
  //     font-weight: bold;
  //     color: #2c3e50;

  //     &.router-link-exact-active {
  //       color: #42b983;
  //     }
  //   }
  // }
    
  #brand {
    flex-grow: 1;
    flex-direction: column;
    justify-content: center;
  }

</style>
