<template>
  <h1>課題管理アプリ</h1>

  <div id="app-container">
    <RouterView /> 
  </div>
</template>

<script setup>
// このコンポーネントは、RouterViewを介してページを表示する枠組みになりました。
// 従来のタスク管理ロジック（tasks, handleSave, computedなど）は、
// 依存するコンポーネント（ItemsPage.vue）に移動させます。
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#app-container {
    display: flex;
    justify-content: space-around;
    padding: 20px;
}
</style>