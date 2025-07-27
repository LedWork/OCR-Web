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
    }
  },
  methods: {
    async getCard() {
      try {
        const response = await axios.get('/api/card/random')
        console.log(response)
        const { imageCode, jsonData, cardData } = await loadJsonData(response.data);

        this.imageCode = imageCode;
        this.jsonData = jsonData;
        this.cardData = cardData;
      } catch (error) {
        console.log(error)
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
          this.image = await loadImage(this.imageCode)
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
    }
  },
  async mounted() {
    try {
      await checkSession(this.$router)
      this.loadSplitPercent(); // Load saved split percentage
      // If we reach here, session is valid (checkSession would redirect if invalid)
      await this.getCard()
      this.image = await loadImage(this.imageCode)
    } catch (error) {
      console.error('Error in mounted:', error)
    } finally {
      this.loading = false
    }
  },
}
</script>
<template>
  <div id="main" class="content-wrapper d-flex flex-column flex-grow-1 pt-2" v-if="!loading && cardData">
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
                <button type="submit" class="btn btn-lg btn-success w-100" :disabled="loading">
                  <span v-if="loading">ŁADOWANIE...</span>
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
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="loading">
    <div class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Ładowanie...</span>
      </div>
      <h3 class="mt-3">Ładowanie karty...</h3>
    </div>
  </div>
  
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="!loading && !cardData">
    <h1 class="display-4 text-center mb-3 mt-5">KONIEC KART DO WYPEŁNIENIA</h1>
    <button
      @click="goToThanks"
      class="btn btn-lg btn-danger w-auto">
      ZAKOŃCZ SPRAWDZANIE
    </button>
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
