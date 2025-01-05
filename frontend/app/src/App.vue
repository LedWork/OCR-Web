<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="main-wrapper">
    <nav>
      <p class="tekst">PCK-OCR</p>
    </nav>
    <RouterView />
  </div>
</template>

<style>
.main-wrapper {
  width: 100%;
  height: 100%;
}
nav {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 60px;
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
  background-color: #dbdbdb;
}
.tekst {
  font-family: 'Red Hat Display', sans-serif;
  font-weight: 700;
  font-size: 30px;
}
body {
  background-color: #c9c9c9;
  width: 100%;
  height: 100%;
}
#app {
  width: 100%;
  height: 100%;
}
html {
  width: 100%;
  height: 100%;
}
</style>
