<script>
import {changeOrientation, checkSession} from "@/scripts/utils.js";

export default {
  data() {
    return {
      loading: false,
    }
  },
  async mounted() {
    this.loading = await checkSession();
    changeOrientation();
  }
}
</script>
<template>
  <div class="wrapper" v-if="!loading">
    <p>TO JEST 404</p>
  </div>
</template>
