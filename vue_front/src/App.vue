<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
        <div class="navbar-brand">
          <router-link to="/" class="navbar-item"><strong>何を学ぶ</strong></router-link>
        </div>
        <router-link to="/" class="button　m-3 is-primary is-outlined">Home</router-link>
        <router-link to="/quiz" class="button m-3 is-primary is-rounded">Quiz</router-link>
    </nav>
    <section class="section">
        <router-view/>
    </section>

    <footer class="footer">
        <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>

<style lang="scss">
@import '../node_modules/bulma';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
