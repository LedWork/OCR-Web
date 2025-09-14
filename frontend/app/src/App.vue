<template>
  <div>
    <nav v-if="!isMarkView" class="navbar navbar-light bg-light fixed-top">
      <div class="container-fluid justify-content-center">
        <img
          src="../public/pck-logo.png"
          alt="PCK Logo"
          class="navbar-logo me-2"
        />
        <p class="navbar-brand mb-0 text-center">PCK-OCR</p>
      </div>
    </nav>
    <div :class="contentContainerClass">
      <RouterView />
    </div>
  </div>
</template>

<script>
import { globalState } from './scripts/store.js'

export default {
  name: 'App',
  data() {
    return {
      globalState
    }
  },
  computed: {
    isMarkView() {
      return this.$route.name === 'marking';
    },
    contentContainerClass() {
      return this.isMarkView ? 'content-container-no-navbar' : 'content-container';
    }
  },
}
</script>

<style>
.navbar-logo {
  height: 60px;
  width: auto;
}

body {
  background-color: #c9c9c9;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
}

.content-container {
  padding-top: 80px; /* Increased padding to account for fixed navbar */
  min-height: calc(100vh - 80px); /* Account for navbar only */
  padding-bottom: 20px; /* Small bottom padding */
}

.content-container-no-navbar {
  padding-top: 0; /* No padding when navbar is hidden */
  height: 100vh; /* Use full viewport height */
  padding-bottom: 0; /* No bottom padding */
}

.container-fluid {
  max-width: 100%;
}

</style>
