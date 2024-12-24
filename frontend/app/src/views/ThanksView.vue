<script>
import {checkSession, changeOrientation } from "@/scripts/utils.js";

export default {
  data() {
    return {
      loading: true,
    }
  },
  async mounted() {
    this.loading = await checkSession(this.$router);
    changeOrientation();
  }
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <p class="title">DZIĘKUJEMY ZA UDZIAŁ W PROJEKCIE!</p>
    <p>Zostałes bezpiecznie wylogowany. Możesz zamknąć kartę.</p>
  </div>
</template>
<style scoped>
p {
  text-align: center;
}
</style>
