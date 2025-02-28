<script>
import {logout} from "@/scripts/utils.js";

export default {
  async mounted() {
    await logout(false);
  },
}
</script>
<template>
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5">
    <h1 class="display-4 text-center mb-3 mt-5">DZIĘKUJEMY ZA UDZIAŁ W PROJEKCIE!</h1>
    <p class="lead text-center mt-5">Zostałes bezpiecznie wylogowany. Możesz zamknąć kartę.</p>
  </div>
</template>
<style scoped>
p {
  text-align: center;
}
</style>
