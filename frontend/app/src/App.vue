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
    <!-- Action buttons - only shown when authenticated -->
    <div v-if="globalState.isAuthenticated" class="action-buttons-container">
      <!-- Finish checking button -->
      <div class="finish-button-wrapper">
        <button 
          class="finish-button" 
          @mouseenter="showFinishTooltip = true" 
          @mouseleave="showFinishTooltip = false"
          @click="finishChecking"
          aria-label="Zakończ sprawdzanie"
        >
          ✕
        </button>
        <div v-if="showFinishTooltip" class="finish-tooltip">
          <p class="mb-0">
            <small>
              Kliknij, aby zakończyć sprawdzanie i wrócić do głównego menu
            </small>
          </p>
        </div>
      </div>
      
      <!-- Help button -->
      <div class="help-button-wrapper">
        <button 
          class="help-button" 
          @mouseenter="showTooltip = true" 
          @mouseleave="showTooltip = false"
          aria-label="Pomoc i kontakt"
        >
          ?
        </button>
        <div v-if="showTooltip" class="help-tooltip">
          <p class="mb-0">
            <small>
              Jeśli masz pytania lub problemy, skontaktuj się z nami pod adresem: 
              <a href="mailto:skany.hdkpck@pck.pomorze.pl" class="text-decoration-none">
                skany.hdkpck@pck.pomorze.pl
              </a>
            </small>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { globalState } from './scripts/store.js'

export default {
  name: 'App',
  data() {
    return {
      globalState,
      showTooltip: false,
      showFinishTooltip: false
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
  methods: {
    finishChecking() {
      // Navigate to the main menu or appropriate route
      this.$router.push('/');
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
  padding-top: 80px; /* Increased padding to account for fixed navbar */
  min-height: calc(100vh - 80px); /* Account for navbar only */
  padding-bottom: 20px; /* Small bottom padding */
}

.content-container-no-navbar {
  padding-top: 0; /* No padding when navbar is hidden */
  min-height: 100vh; /* Use full viewport height */
  padding-bottom: 20px; /* Small bottom padding */
}

.container-fluid {
  max-width: 100%;
}

.action-buttons-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.finish-button-wrapper,
.help-button-wrapper {
  position: relative;
}

.finish-button,
.help-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  color: white;
  border: none;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.finish-button {
  background-color: #dc3545;
}

.finish-button:hover {
  background-color: #c82333;
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.help-button {
  background-color: #007bff;
}

.help-button:hover {
  background-color: #0056b3;
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.finish-tooltip,
.help-tooltip {
  position: absolute;
  bottom: 60px;
  left: 0;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  min-width: 300px;
  max-width: 400px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 1001;
}

.finish-tooltip::after,
.help-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 20px;
  border: 8px solid transparent;
  border-top-color: #f8f9fa;
}

.help-tooltip a {
  color: #007bff;
  text-decoration: none;
}

.help-tooltip a:hover {
  color: #0056b3;
  text-decoration: underline;
}
</style>
