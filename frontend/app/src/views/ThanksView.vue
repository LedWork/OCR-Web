<script>
import {changeOrientation, logout} from "@/scripts/utils.js";

export default {
  async mounted() {
    await logout(false);
    window.addEventListener('resize', changeOrientation)
  },
  beforeUnmount() {
    window.removeEventListener('resize', changeOrientation)
  },
}
</script>
<template>
  <div class="wrapper vertical">
    <h1 class="title">DZIĘKUJEMY ZA UDZIAŁ W PROJEKCIE!</h1>
    <p>Zostałes bezpiecznie wylogowany. Możesz zamknąć kartę.</p>
  </div>
</template>
<style scoped>
p {
  text-align: center;
}
</style>
