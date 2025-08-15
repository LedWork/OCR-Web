<template>
  <div>
    <nav class="navbar navbar-light bg-light fixed-top">
      <div class="container-fluid justify-content-center">
        <img
          src="../public/pck-logo.png"
          alt="PCK Logo"
          class="navbar-logo me-2"
        />
        <p class="navbar-brand mb-0 text-center">PCK-OCR</p>
      </div>
    </nav>
    <div class="content-container">
      <RouterView />
    </div>
    <!-- Footer with contact email - only shown when authenticated -->
    <footer v-if="globalState.isAuthenticated" class="footer">
      <div class="container-fluid text-center">
        <p class="mb-0">
          <small>
            Jeśli masz pytania lub problemy, skontaktuj się z nami pod adresem: 
            <a href="mailto:skany.hdkpck@pck.pomorze.pl" class="text-decoration-none">
              skany.hdkpck@pck.pomorze.pl
            </a>
          </small>
        </p>
      </div>
    </footer>
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
  }
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
  padding-top: 50px;
  min-height: calc(100vh - 120px); /* Account for navbar and footer */
  padding-bottom: 60px; /* Add space for footer */
}

.container-fluid {
  max-width: 100%;
}

.footer {
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  padding: 10px 0;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.footer a {
  color: #007bff;
}

.footer a:hover {
  color: #0056b3;
}
</style>
