<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from 'axios'
import SplitPane from 'vue3-splitpane';
import {
  checkSession,
  getCSRFToken,
  loadJsonData,
  loadImage,
  parseGtParse
} from '@/scripts/utils.js'
import { globalState } from '@/scripts/store.js'

export default {
  components: {
    DynamicForm,
    SplitPane,
  },
  data() {
    return {
      globalState,
      loading: true,
      image: null,
      cardData: null,
      jsonData: {},
      imageCode: '',
      splitPercent: 50, // Default split percentage
      isRequestingCard: false, // Prevent multiple simultaneous card requests
      lastCardRequestTime: null, // Track when we last requested a card
      countdown: 0, // Countdown for the throttle
      countdownInterval: null, // Interval ID for the countdown
      isRateLimited: false, // Track if we're rate limited vs no cards available
      showTooltip: false,
      showFinishTooltip: false,
      // Zoom functionality
      zoomLevel: 1,
      zoomMin: 0.5,
      zoomMax: 3,
      zoomStep: 0.1,
      imagePosition: { x: 0, y: 0 },
      isDragging: false,
      dragStart: { x: 0, y: 0 },
    }
  },
  computed: {
    canRequestCard() {
      // Allow request if no last request time or if the countdown has finished
      return !this.lastCardRequestTime || this.countdown === 0;
    },
    
    remainingThrottleTime() {
      // Directly use the reactive countdown for display
      return this.countdown;
    },
    
    shouldShowMainContent() {
      return !this.loading && this.cardData;
    },
    
    shouldShowRateLimitLoading() {
      return this.isRateLimited && this.countdown > 0;
    }
  },
  methods: {
    async getCard() {
      // Check if we can request a card (throttling)
      if (!this.canRequestCard) {
        console.log('Throttling active, cannot request card yet');
        return;
      }
      
      // Prevent multiple simultaneous requests
      if (this.isRequestingCard) {
        console.log('Card request already in progress, skipping...');
        return;
      }
      
      try {
        this.isRequestingCard = true;
        
        const response = await axios.get('/api/card/random')
        const { imageCode, jsonData, cardData } = await loadJsonData(response.data);

        this.imageCode = imageCode;
        this.jsonData = jsonData;
        this.cardData = cardData;
        
        // Reset rate limit flag since we successfully got a card
        this.isRateLimited = false;
        
        // Update last request time and start countdown
        this.lastCardRequestTime = Date.now();
        this.startCountdown();
        
      } catch (error) {
        console.log(error)
        
        // Check if the error is due to no more cards available
        if (error.response && error.response.status === 400 && 
            error.response.data && error.response.data.error === "No cards available in the database.") {
          // No more cards available, set flag and clear data
          this.isRateLimited = false;
          this.cardData = null;
          this.image = null;
          this.imageCode = '';
          this.jsonData = {};
        } else if (error.response && error.response.status === 429) {
          // Rate limit exceeded, set flag and clear data
          this.isRateLimited = true;
          this.cardData = null;
          this.image = null;
          this.imageCode = '';
          this.jsonData = {};
          
          // If we have a last request time but no countdown running, start it
          // This ensures users can see the remaining time
          if (this.lastCardRequestTime && !this.countdownInterval) {
            this.startCountdown();
          }
        } else {
          // For other errors, assume rate limiting and clear the card data
          this.isRateLimited = true;
          this.cardData = null;
          this.image = null;
          this.imageCode = '';
          this.jsonData = {};
          
          // If we have a last request time but no countdown running, start it
          // This ensures users can see the remaining time
          if (this.lastCardRequestTime && !this.countdownInterval) {
            this.startCountdown();
          }
        }
      } finally {
        this.isRequestingCard = false;
      }
    },
    
    startCountdown() {
      // Clear any existing countdown
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
      }
      
      // Calculate how much time has passed since the last request
      if (this.lastCardRequestTime) {
        const elapsed = Date.now() - this.lastCardRequestTime;
        const remaining = Math.max(0, 16 - Math.floor(elapsed / 1000));
        this.countdown = remaining;
      } else {
        // If no last request time, start from 16
        this.countdown = 16;
      }
      
      this.countdownInterval = setInterval(() => {
        this.countdown--;
        
        if (this.countdown <= 0) {
          clearInterval(this.countdownInterval);
          this.countdownInterval = null;
          this.countdown = 0;
        }
      }, 1000);
    },
    
    stopCountdown() {
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
        this.countdown = 0;
      }
    },
    updateJsonData(updatedValue) {
      this.jsonData = updatedValue;
    },
    async handleSubmit() {
      try {
        this.loading = true
        this.jsonData = parseGtParse(this.jsonData, true)
        this.cardData.gt_parse = this.jsonData
        const response = await axios.post('api/card/correct', this.cardData, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        })

        if (response.status === 200) {
          // Load the next card instead of reloading the page
          await this.getCard()
          // Only try to load image if we still have a card (getCard didn't redirect)
          if (this.cardData) {
            this.image = await loadImage(this.imageCode)
            // Focus on first form field after submitting and loading next card
            this.focusFirstFormField();
          }
        } else {
          alert('Error: ' + response.data.error)
        }
      } catch (error) {
        console.error('Error sending data:', error)
        alert('There was an error sending your data.')
      } finally {
        this.loading = false
      }
    },
    goToThanks() {
      this.$router.push({name: 'thanks'})
    },
    handleSplitChange(percent) {
      this.splitPercent = percent;
      // Save to session storage
      sessionStorage.setItem('markViewSplitPercent', percent.toString());
    },
    loadSplitPercent() {
      const saved = sessionStorage.getItem('markViewSplitPercent');
      if (saved) {
        this.splitPercent = parseInt(saved);
      }
    },
    
    async getNewCard() {
      // Reset the countdown and get a new card
      this.stopCountdown();
      this.lastCardRequestTime = null;
      this.isRateLimited = false; // Reset rate limit flag
      await this.getCard();
      
      // If we successfully got a card, also load the image
      if (this.cardData && this.imageCode) {
        try {
          this.image = await loadImage(this.imageCode);
          // Focus on first form field after loading new card
          this.focusFirstFormField();
        } catch (error) {
          console.error('Error loading image:', error);
        }
      }
    },
    
    focusFirstFormField() {
      // Focus on the first form field (Nazwisko) after a short delay to ensure DOM is updated
      this.$nextTick(() => {
        setTimeout(() => {
          const firstInput = this.$el.querySelector('input[type="text"]');
          if (firstInput) {
            firstInput.focus();
          }
        }, 100);
      });
    },
    
    // Zoom functionality methods
    handleWheel(event) {
      event.preventDefault();
      
      const delta = event.deltaY > 0 ? -this.zoomStep : this.zoomStep;
      const newZoom = Math.max(this.zoomMin, Math.min(this.zoomMax, this.zoomLevel + delta));
      
      if (newZoom !== this.zoomLevel) {
        const rect = event.currentTarget.getBoundingClientRect();
        const containerCenterX = rect.width / 2;
        const containerCenterY = rect.height / 2;
        
        // Get mouse position relative to the container
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        
        // Calculate the zoom factor
        const zoomFactor = newZoom / this.zoomLevel;
        
        // Calculate the point on the image that the mouse is pointing to
        // This is the point that should remain under the mouse after zoom
        const imagePointX = (mouseX - containerCenterX - this.imagePosition.x) / this.zoomLevel;
        const imagePointY = (mouseY - containerCenterY - this.imagePosition.y) / this.zoomLevel;
        
        // Update zoom level
        this.zoomLevel = newZoom;
        
        // Calculate new position so the same image point stays under the mouse
        this.imagePosition.x = mouseX - containerCenterX - imagePointX * this.zoomLevel;
        this.imagePosition.y = mouseY - containerCenterY - imagePointY * this.zoomLevel;
      }
    },
    
    handleMouseDown(event) {
      if (this.zoomLevel > 1) {
        this.isDragging = true;
        this.dragStart = { x: event.clientX - this.imagePosition.x, y: event.clientY - this.imagePosition.y };
        event.preventDefault();
      }
    },
    
    handleMouseMove(event) {
      if (this.isDragging && this.zoomLevel > 1) {
        this.imagePosition.x = event.clientX - this.dragStart.x;
        this.imagePosition.y = event.clientY - this.dragStart.y;
        event.preventDefault();
      }
    },
    
    handleMouseUp() {
      this.isDragging = false;
    },
    
    resetZoom() {
      this.zoomLevel = 1;
      this.imagePosition = { x: 0, y: 0 };
    },
    
    handleKeyDown(event) {
      // Reset zoom with 'R' key only when not typing in form inputs and not using Ctrl+R
      if ((event.key === 'r' || event.key === 'R') && 
          !event.ctrlKey && 
          !event.metaKey && 
          !event.target.matches('input, textarea, select')) {
        this.resetZoom();
        event.preventDefault();
      }
    }
  },
  async mounted() {
    try {
      await checkSession(this.$router)
      this.loadSplitPercent(); // Load saved split percentage
      // If we reach here, session is valid (checkSession would redirect if invalid)
      await this.getCard()
      // Only try to load image if we have a card
      if (this.cardData) {
        this.image = await loadImage(this.imageCode)
        // Focus on first form field after initial load
        this.focusFirstFormField();
      }
      
      // Add event listeners for zoom functionality
      document.addEventListener('mousemove', this.handleMouseMove);
      document.addEventListener('mouseup', this.handleMouseUp);
      document.addEventListener('keydown', this.handleKeyDown);
    } catch (error) {
      console.error('Error in mounted:', error)
    } finally {
      this.loading = false
    }
  },
  
  beforeUnmount() {
    // Clean up countdown interval when component is destroyed
    this.stopCountdown();
    
    // Clean up event listeners
    document.removeEventListener('mousemove', this.handleMouseMove);
    document.removeEventListener('mouseup', this.handleMouseUp);
    document.removeEventListener('keydown', this.handleKeyDown);
  },
  

}
</script>
<template>
  <div id="main" class="content-wrapper d-flex flex-column flex-grow-1 pt-2" v-if="shouldShowMainContent">
    <!-- PCK Logo in top left corner -->
    <div class="pck-logo-container">
      <img src="../../public/pck-logo.png" alt="Polski Czerwony Krzyż" class="pck-logo" />
    </div>
    
    <div class="container-fluid d-flex flex-column align-items-center h-100 px-3">

      <split-pane 
        split="vertical" 
        :min-percent="20" 
        :default-percent="splitPercent"
        :percent="splitPercent"
        @resize="handleSplitChange"
        class="split-pane-main"
      >
        <template #paneL>
          <div 
            class="container-img text-center d-flex align-items-start justify-content-center h-100 w-100"
            @wheel="handleWheel"
            @mousedown="handleMouseDown"
            :class="{ dragging: isDragging }"
          >
            <img
              class="img-fluid card-image-clickable"
              :src="image"
              alt="Image"
              :style="{
                transform: `scale(${zoomLevel}) translate(${imagePosition.x}px, ${imagePosition.y}px)`,
                transformOrigin: 'center center',
                transition: isDragging ? 'none' : 'transform 0.1s ease-out'
              }"
              :title="zoomLevel > 1 ? 'Przewiń, aby przybliżyć/oddalić | Przeciągnij, aby przesunąć | R - reset' : 'Przewiń, aby przybliżyć/oddalić'"
            />
            
            <!-- Zoom controls -->
            <div v-if="zoomLevel > 1" class="zoom-controls">
              <div class="zoom-indicator">
                {{ Math.round(zoomLevel * 100) }}%
              </div>
              <button 
                class="btn btn-sm btn-outline-secondary zoom-reset-btn"
                @click="resetZoom"
                title="Resetuj powiększenie (R)"
              >
                Reset
              </button>
            </div>
          </div>
        </template>
        <template #paneR>
          <div class="card border-light-subtle p-3 d-flex flex-column h-100 w-100">
            <!-- Scrollable form content -->
            <div class="form-content-scrollable flex-grow-1 overflow-auto">
              <form @submit.prevent="handleSubmit" class="w-100">
                <DynamicForm :value="jsonData" @update:value="updateJsonData" />
              </form>
            </div>
            
            <!-- Fixed button at bottom -->
            <div class="button-container mt-3">
              <button type="submit" class="btn btn-success w-100 submit-button" :disabled="loading || !canRequestCard" @click="handleSubmit" tabindex="-1">
                <span v-if="loading">ŁADOWANIE...</span>
                <span v-else-if="!canRequestCard">
                  WYŚLIJ KARTĘ I PRZEJDŹ DO NASTĘPNEJ
                  <span class="ms-2 badge bg-warning text-dark">{{ countdown }}s</span>
                </span>
                <span v-else>WYŚLIJ KARTĘ I PRZEJDŹ DO NASTĘPNEJ</span>
              </button>
            </div>
          </div>
        </template>
      </split-pane>

    </div>
  </div>
  
  <!-- Loading indicator -->
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="loading && !shouldShowRateLimitLoading">
    <!-- PCK Logo in top left corner -->
    <div class="pck-logo-container">
      <img src="/pck-logo.png" alt="Polski Czerwony Krzyż" class="pck-logo" />
    </div>
    
    <div class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Ładowanie...</span>
      </div>
      <h3 class="mt-3">Ładowanie karty...</h3>
    </div>
  </div>
  
  <!-- No cards available or rate limit reached -->
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="!loading && !cardData">
    <!-- PCK Logo in top left corner -->
    <div class="pck-logo-container">
      <img src="/pck-logo.png" alt="Polski Czerwony Krzyż" class="pck-logo" />
    </div>
    
    <!-- Rate limit message -->
    <div class="text-center" v-if="isRateLimited">
      <h1 class="display-4 text-center mb-3 mt-5">Zbyt szybkie żądania</h1>
      <p class="lead mb-4">Spróbuj ponownie za kilka sekund</p>
      
      <div class="d-flex gap-3 justify-content-center">
        <button
          @click="getNewCard"
          :disabled="!canRequestCard"
          class="btn btn-lg btn-primary"
          tabindex="-1">
          <span v-if="!canRequestCard">
            Pobierz nową kartę
          </span>
          <span v-else>Pobierz nową kartę</span>
        </button>
        
        <button
          @click="goToThanks"
          class="btn btn-lg btn-danger"
          tabindex="-1">
          ZAKOŃCZ SPRAWDZANIE
        </button>
      </div>
    </div>
    
    <!-- No more cards message -->
    <div class="text-center" v-else>
      <h1 class="display-4 text-center mb-3 mt-5">KONIEC KART DO WYPEŁNIENIA</h1>
      <div class="d-flex gap-3 justify-content-center">
        <button
          @click="goToThanks"
          class="btn btn-lg btn-danger w-auto"
          tabindex="-1">
          ZAKOŃCZ SPRAWDZANIE
        </button>
      </div>
    </div>
  </div>
  
  <!-- Action buttons - only shown when authenticated and on marking page -->
  <div v-if="globalState.isAuthenticated && $route.name === 'marking'" class="action-buttons-container">
    <!-- Finish checking button -->
    <div class="finish-button-wrapper">
      <button 
        class="finish-button" 
        @mouseenter="showFinishTooltip = true" 
        @mouseleave="showFinishTooltip = false"
        @click="goToThanks"
        aria-label="Zakończ sprawdzanie"
        tabindex="-1"
      >
        ✕
      </button>
      <div v-if="showFinishTooltip" class="finish-tooltip">
        <p class="mb-0">
          <small>
            Kliknij, aby zakończyć sprawdzanie bez wysyłania obecnej karty
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
        tabindex="-1"
      >
        ?
      </button>
      <div v-if="showTooltip" class="help-tooltip">
        <p class="mb-0">
          <small>
            Przewiń, aby przybliżyć/oddalić | Przeciągnij, aby przesunąć | R - reset
            <br><br>
            Jeśli masz pytania lub problemy, skontaktuj się z nami pod adresem: 
            <a href="mailto:skany.hdkpck@pck.pomorze.pl" class="text-decoration-none">
              skany.hdkpck@pck.pomorze.pl
            </a>
          </small>
        </p>
      </div>
    </div>
  </div>
  

</template>

<style scoped>
.split-pane-main {
  height: 100vh;
  min-height: 400px;
  width: 100%;
}

.card {
  height: 100vh;
}

.form-content-scrollable {
  min-height: 0; /* Important for flexbox scrolling */
}

.button-container {
  flex-shrink: 0; /* Prevent button from shrinking */
}

.submit-button {
  padding: 0.75rem 1.5rem; /* Increased padding for better accessibility */
  font-size: 1.1rem; /* Larger font size for better readability */
  font-weight: 600; /* Bold text for better visibility */
  color: #fff; /* Ensure high contrast */
}

.container-img {
  height: 100vh;
  cursor: zoom-in;
  overflow: hidden;
  position: relative;
}

.card-image-clickable {
  max-width: 100%;
  max-height: 100%;
  height: auto;
  object-fit: contain;
  cursor: zoom-in;
  border: 2px solid #eee;
  border-radius: 8px;
  transition: box-shadow 0.2s;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  align-self: flex-start;
}

.container-img:active .card-image-clickable {
  cursor: grabbing;
}

.container-img.dragging .card-image-clickable {
  cursor: grabbing;
}

/* Zoom controls */
.zoom-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.zoom-indicator {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
  min-width: 60px;
  text-align: center;
}

.zoom-reset-btn {
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
}
.card-image-clickable:hover {
  box-shadow: 0 0 10px #2196f3;
}


/* PCK Logo styles */
.pck-logo-container {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

.pck-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid #dc3545;
  background-color: white;
  padding: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.pck-logo:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

/* Action buttons styles */
.action-buttons-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 9999;
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
  width: 55px;
  height: 55px;
  border-radius: 50%;
  color: white;
  border: none;
  font-size: 22px;
  font-weight: 700;
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
  bottom: 65px;
  left: 0;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 18px;
  min-width: 320px;
  max-width: 420px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 10000;
  font-size: 1rem;
  line-height: 1.5;
  color: #2c3e50;
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

/* Focus management styles */
button:focus {
  outline: none !important;
  box-shadow: none !important;
}

button[tabindex="-1"]:focus {
  outline: none !important;
  box-shadow: none !important;
}

/* Ensure form inputs have clear focus styles */
input[type="text"]:focus {
  outline: 3px solid #007bff;
  outline-offset: 3px;
  border-color: #007bff;
  box-shadow: 0 0 0 0.3rem rgba(0, 123, 255, 0.3);
  font-size: 1.1rem;
  font-weight: 400;
}

/* General form styling for better accessibility */
input[type="text"] {
  font-size: 1rem;
  font-weight: 400;
  color: #2c3e50;
  line-height: 1.5;
}

@media (max-width: 768px) and (orientation: portrait) {
  .split-pane-main {
    flex-direction: column;
    height: calc(100vh - 60px);
    min-height: 300px;
  }
  .container-img, .card {
    height: calc(50vh - 30px);
    min-height: 200px;
  }
  .card-image-clickable {
    height: calc(50vh - 30px);
  }
  
  .submit-button {
    font-size: 1rem;
    padding: 0.6rem 1.2rem;
  }
  
  .finish-button,
  .help-button {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .finish-tooltip,
  .help-tooltip {
    font-size: 0.9rem;
    min-width: 280px;
    max-width: 350px;
    padding: 15px;
  }
  
  input[type="text"] {
    font-size: 0.95rem;
  }
  
  input[type="text"]:focus {
    font-size: 1rem;
  }
}
</style>
