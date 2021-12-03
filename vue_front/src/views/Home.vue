<template>
  <section class="section">
    <div class="box" style='position:relative'>
      <img class='is-image' src="@/assets/japan.png">
      <div class='title-hero is-overlay'>
        <p class="is-size-6-mobile is-size-1-desktop is-size-3-tablet has-text-weight-bold mb-3">
         日本語試してみよう！
        </p>
        <p class="is-size-6 is-size-4-tablet">
          問題やる？
        </p>
        <button class='button is-outlined'> start </button>
      </div>      
    </div>
  </section>

</template>

<script>

export default {
  name: 'Home',
  components: {
  }
}
</script>
<style lang="scss">
@import "style/_variables.scss";
@media(max-width: 414px){
  .box{
      margin: 0;
      padding:0;
    }
  .section{
      margin: 0;
      padding:0;
    }
  .button{
    padding: 0.5rem;
    // box-sizing: border-box;
    // border: 1px solid $base-color;
    // background: $base-color
  }
  }
  .is-image{
    position:block;
    height: 100%;
    width:100%;
  }
  .title-hero{
    position: absolute;
    top: 50%;
    left: 50%;
    -ms-transform: translate(-50%,-50%);
    -webkit-transform: translate(-50%,-50%);
    transform: translate(-50%,-50%);
    margin:0;
    padding:0;
  }
  
</style>
