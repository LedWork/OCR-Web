<script>
export default {
  methods: {
    goToMarking() {
      this.$router.push('/oznaczanie')
    },
  },
}
</script>
<template>
  <div class="wrapper vertical">
    <div class="text-block">
      <p class="title">Instrukcja</p>
      <p class="content">
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quas earum dignissimos ipsum
        assumenda ratione explicabo consequatur quo cupiditate mollitia quibusdam eveniet eum,
        tempore fugit. Magni itaque doloremque ea! Distinctio, possimus.
      </p>
    </div>
    <div class="button" @click="goToMarking">PRZEJDŹ DALEJ</div>
  </div>
</template>
<style></style>
