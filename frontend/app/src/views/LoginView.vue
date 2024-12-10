<script>
export default {
  methods: {
    goToInstruction() {
      this.$router.push('/instrukcja')
    },
  },
}
</script>
<template>
  <div class="wrapper vertical">
    <div class="text-block">
      <p class="title">ZALOGUJ SIĘ ABY KONTUNOWAĆ...</p>
      <input placeholder="Login..." class="input text-input" type="text" name="login" />
      <input placeholder="Haslo..." class="input text-input" type="password" name="password" />
      <div class="btn-wrapper">
        <div class="button" @click="goToInstruction">ZALOGUJ SIĘ</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.title {
  text-align: center;
  font-size: 20px;
}
.button {
  font-size: 20px;
}
@media (min-width: 1024px) {
  .text-block {
    width: 30%;
    padding: 30px;
  }
  .title {
    font-size: 25px;
  }
  .button {
    font-size: 35px;
  }
}
.btn-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
