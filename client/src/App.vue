<template>
  <div id="app">
    <router-view v-wechat-title="$route.meta.title"/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  * {
    padding: 0 0;
    margin: 0 0;
  }

  /*html {
    overflow-y: scroll;
    font-size: 16px;
  }

  body {
      width: 100%;
      overflow: hidden;
  }*/
</style>
