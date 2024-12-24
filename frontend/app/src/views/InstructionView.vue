<script>
import {adminCheckSession, changeOrientation, checkSession} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true,
      admin: false
    }
  },
  async mounted() {
    this.loading = await checkSession(this.$router);
    this.admin = await adminCheckSession();
    changeOrientation();
  },
  methods: {
    goToMarking() {
      this.$router.push({name: 'marking'})
    },
    goToAdmin() {
      this.$router.push({name: 'admin'})
    }
  },
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <div v-if="admin" class="button" @click="goToAdmin">ADMIN PANEL</div>
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
