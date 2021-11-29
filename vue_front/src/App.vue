<template>
  <div id="wrapper">
    <div class='box'>
      <nav class="navbar is-dark　is-mobile">
          <div class="navbar-brand">
            <a class="navbar-item">
                <router-link to="/" >何を学ぶ</router-link>
            </a>
            <a class="navbar-burger" @click="showMobileMenu = !showMobileMenu">
              <span></span>
              <span></span>
              <span></span>
            </a>
          </div>
          
          <div class='navbar-menu' :class="{'is-active': showMobileMenu }">
            <div class="navbar-end">
              <div class="navbar-item">
                <router-link to="/" class="button　m-3 is-primary is-outlined">Home</router-link>
                <router-link to="/quiz" class="button m-3 is-primary is-rounded">Quiz</router-link>
              </div>
            </div>

          </div>
      </nav>
      <section class="section is-paddingless pt-4">
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
