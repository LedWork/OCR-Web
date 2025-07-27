<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from "axios";
import SplitPane from 'vue3-splitpane';
import { checkSession, getCSRFToken, loadJsonData, loadImage, parseGtParse} from "@/scripts/utils.js";

export default {
  components: { DynamicForm, SplitPane },
  props: {
    imageCode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      image: null,
      cardData: null,
      jsonData: {},
      showImageModal: false,
      splitPercent: 50, // Default split percentage
    }
  },
  methods: {
    async getCard() {
      try {
        const response = await axios.get('/api/admin/card/' + this.imageCode);
        //console.log(response)
        const { jsonData, cardData } = await loadJsonData(response.data);

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
        this.jsonData = parseGtParse(this.jsonData, true)
        this.cardData.gt_parse = this.jsonData
        const response = await axios.post('/api/admin/correct', this.cardData, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        })

        if (response.status === 200) {
          this.goToCardsPanel()
          alert(response.data.message)
        } else {
          alert('Error: ' + response.data.error)
        }
      } catch (error) {
        console.error('Error sending data:', error)
        alert('There was an error sending your data.')
      }
    },
    goToCardsPanel() {
      this.$router.push({name: "cards"});
    },
    async logout() {
      const response = await axios.post(
        '/api/auth/break-session',
        {},
        {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        },
      )

      if (response.status === 200) {
        window.location.reload();
      }
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
      sessionStorage.setItem('cardViewSplitPercent', percent.toString());
    },
    loadSplitPercent() {
      const saved = sessionStorage.getItem('cardViewSplitPercent');
      if (saved) {
        this.splitPercent = parseInt(saved);
      }
    }
  },
  async mounted() {
    this.loading = await checkSession(this.$router)
    this.loadSplitPercent(); // Load saved split percentage
    await this.getCard()
    this.image = await loadImage(this.imageCode)
  },
}
</script>

<template>
  <div id="main" class="content-wrapper d-flex flex-column flex-grow-1 pt-5" v-if="!loading">
    <div class="container d-flex flex-column justify-content-center align-items-center h-100">
      <div class="row w-100 mb-3">
        <div class="d-flex justify-content-between">
          <button @click="goToCardsPanel" class="btn btn-danger btn-lg me-2">Wróć</button>
          <h1 class="text-center mb-1">Card: {{ imageCode }}</h1>
          <button @click="logout" class="btn btn-danger btn-lg">Wyloguj</button>
        </div>
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
                <button type="submit" class="btn btn-lg btn-success w-100">ZATWIERDŹ ZMIANY</button>
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

