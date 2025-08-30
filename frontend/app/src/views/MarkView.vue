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

export default {
  components: {
    DynamicForm,
    SplitPane,
  },
  data() {
    return {
      loading: true,
      image: null,
      cardData: null,
      jsonData: {},
      imageCode: '',
      showImageModal: false,
      splitPercent: 50, // Default split percentage
      isRequestingCard: false, // Prevent multiple simultaneous card requests
      lastCardRequestTime: null, // Track when we last requested a card
      countdown: 0, // Countdown for the throttle
      countdownInterval: null, // Interval ID for the countdown
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
        console.log('API response:', response)
        const { imageCode, jsonData, cardData } = await loadJsonData(response.data);
        console.log('Parsed data:', { imageCode, jsonData, cardData });
        console.log('Raw response data:', response.data);

        this.imageCode = imageCode;
        this.jsonData = jsonData;
        this.cardData = cardData;
        
        // Update last request time and start countdown
        this.lastCardRequestTime = Date.now();
        this.startCountdown();
        
      } catch (error) {
        console.log(error)
        
        // Check if the error is due to no more cards available
        if (error.response && error.response.status === 400 && 
            error.response.data && error.response.data.error === "No cards available in the database.") {
          // No more cards available, redirect to thanks view
          this.$router.push({name: 'thanks'})
        } else {
          // For other errors (including rate limiting), clear the card data
          // This will show the "Zbyt szybkie żądania" message
          this.cardData = null;
          this.image = null;
          this.imageCode = '';
          this.jsonData = {};
          
          // Ensure countdown is running so users can see remaining time
          this.ensureCountdownRunning();
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
      
      // Start countdown from 21 seconds
      this.countdown = 21;
      console.log('Starting countdown from:', this.countdown);
      
      this.countdownInterval = setInterval(() => {
        this.countdown--;
        console.log('Countdown:', this.countdown);
        
        if (this.countdown <= 0) {
          clearInterval(this.countdownInterval);
          this.countdownInterval = null;
          this.countdown = 0;
          console.log('Countdown finished');
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
    openImageModal() {
      this.showImageModal = true;
    },
    closeImageModal() {
      this.showImageModal = false;
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
      
      console.log('Getting new card...');
      await this.getCard();
      
      console.log('Card data after getCard:', this.cardData);
      console.log('Image code after getCard:', this.imageCode);
      
      // If we successfully got a card, also load the image
      if (this.cardData && this.imageCode) {
        try {
          console.log('Loading image for code:', this.imageCode);
          this.image = await loadImage(this.imageCode);
          console.log('Image loaded successfully:', this.image);
          
          // If image loading failed, try to debug the issue
          if (!this.image) {
            console.log('Image loading returned null/undefined, checking API response...');
            // Make a direct call to see what the image API returns
            const imageResponse = await axios.get(`/api/image/${this.imageCode}`);
            console.log('Direct image API response:', imageResponse.data);
          }
        } catch (error) {
          console.error('Error loading image:', error);
        }
      } else {
        console.log('Cannot load image - missing cardData or imageCode');
      }
    },
    
    ensureCountdownRunning() {
      // If we have a last request time but no countdown running, start it
      if (this.lastCardRequestTime && !this.countdownInterval && this.countdown === 0) {
        console.log('Ensuring countdown is running...');
        this.startCountdown();
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
      }
    } catch (error) {
      console.error('Error in mounted:', error)
    } finally {
      this.loading = false
    }
  },
  
  beforeUnmount() {
    // Clean up countdown interval when component is destroyed
    this.stopCountdown();
  },
  
  watch: {
    // Watch for changes in lastCardRequestTime to ensure countdown is running
    lastCardRequestTime(newVal) {
      if (newVal) {
        // When a new request time is set, ensure countdown is running
        this.$nextTick(() => {
          this.ensureCountdownRunning();
        });
      }
    }
  },
}
</script>
<template>
  <div id="main" class="content-wrapper d-flex flex-column flex-grow-1 pt-2" v-if="shouldShowMainContent">
    <div class="container-fluid d-flex flex-column justify-content-center align-items-center h-100 px-3">
      <div class="row w-100 d-flex justify-content-center mb-2">
        <button
          @click="goToThanks"
          class="btn btn-lg btn-danger w-75">
          ZAKOŃCZ SPRAWDZANIE
        </button>
      </div>

      <split-pane 
        split="vertical" 
        :min-percent="20" 
        :default-percent="splitPercent"
        :percent="splitPercent"
        @resize="handleSplitChange"
        class="split-pane-main"
      >
        <template #paneL>
          <div class="container-img text-center d-flex align-items-center justify-content-center h-100 w-100">
            <img
              class="img-fluid card-image-clickable"
              :src="image"
              alt="Image"
              @click="openImageModal"
              title="Kliknij, aby powiększyć"
            />
          </div>
        </template>
        <template #paneR>
          <div class="card border-light-subtle p-3 d-flex flex-column align-items-center overflow-auto h-100 w-100">
            <form @submit.prevent="handleSubmit" class="w-100">
              <DynamicForm :value="jsonData" @update:value="updateJsonData" />
              <div class="text-center mt-3">
                <button type="submit" class="btn btn-lg btn-success w-100" :disabled="loading || !canRequestCard">
                  <span v-if="loading">ŁADOWANIE...</span>
                  <span v-else-if="!canRequestCard">
                    WYŚLIJ KARTĘ I PRZEJDŹ DO NASTĘPNEJ
                    <span class="ms-2 badge bg-warning text-dark">{{ countdown }}s</span>
                  </span>
                  <span v-else>WYŚLIJ KARTĘ I PRZEJDŹ DO NASTĘPNEJ</span>
                </button>
              </div>
            </form>
          </div>
        </template>
      </split-pane>

      <!-- Modal for image zoom -->
      <div v-if="showImageModal" class="modal-backdrop-custom" @click.self="closeImageModal">
        <div class="modal-dialog-custom">
          <img :src="image" alt="Zoomed Image" class="modal-image" />
          <button class="btn btn-secondary mt-2" @click="closeImageModal">Zamknij</button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Loading indicator -->
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="loading && !shouldShowRateLimitLoading">
    <div class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Ładowanie...</span>
      </div>
      <h3 class="mt-3">Ładowanie karty...</h3>
    </div>
  </div>
  
  <!-- No cards available or rate limit reached -->
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="!loading && !cardData">
    <div class="text-center">
      <h1 class="display-4 text-center mb-3 mt-5">Zbyt szybkie żądania</h1>
      <p class="lead mb-4">Spróbuj ponownie za {{ countdown }} sekund</p>
      
      <div class="d-flex gap-3 justify-content-center">
        <button
          @click="getNewCard"
          :disabled="!canRequestCard"
          class="btn btn-lg btn-primary">
          <span v-if="!canRequestCard">
            Pobierz nową kartę
            <span class="ms-2 badge bg-warning text-dark">{{ countdown }}s</span>
          </span>
          <span v-else>Pobierz nową kartę</span>
        </button>
        
        <button
          @click="goToThanks"
          class="btn btn-lg btn-danger">
          ZAKOŃCZ SPRAWDZANIE
        </button>
      </div>
    </div>
  </div>


</template>

<style scoped>
.split-pane-main {
  height: 75vh;
  min-height: 400px;
  width: 100%;
}

.card {
  height: 75vh;
  overflow-y: auto;
}

.container-img {
  height: 75vh;
  cursor: zoom-in;
}

.card-image-clickable {
  max-width: 100%;
  max-height: 100%;
  height: 75vh;
  object-fit: contain;
  cursor: zoom-in;
  border: 2px solid #eee;
  border-radius: 8px;
  transition: box-shadow 0.2s;
}
.card-image-clickable:hover {
  box-shadow: 0 0 10px #2196f3;
}

/* Modal styles */
.modal-backdrop-custom {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.7);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-dialog-custom {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 90vw;
  max-height: 90vh;
}
.modal-image {
  max-width: 80vw;
  max-height: 70vh;
  border-radius: 8px;
  margin-bottom: 10px;
}

@media (max-width: 768px) and (orientation: portrait) {
  .split-pane-main {
    flex-direction: column;
    height: calc(100vh - 60px);
    min-height: 300px;
  }
  .container-img, .card {
    height: 40vh;
    min-height: 200px;
  }
  .modal-image {
    max-width: 95vw;
    max-height: 60vh;
  }
}
</style>
