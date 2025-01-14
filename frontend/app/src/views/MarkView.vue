<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from 'axios'
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
  },
  data() {
    return {
      loading: true,
      image: null,
      cardData: null,
      jsonData: {},
      imageCode: '',
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
        this.jsonData = parseGtParse(this.jsonData, true)
        this.cardData.gt_parse = this.jsonData
        const response = await axios.post('api/card/correct1', this.cardData, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        })

        if (response.status === 200) {
          this.cardData = null
          window.location.reload()
        } else {
          alert('Error: ' + response.data.error)
        }
      } catch (error) {
        console.error('Error sending data:', error)
        alert('There was an error sending your data.')
      }
    },
    goToThanks() {
      this.$router.push({name: 'thanks'})
    },
  },
  async mounted() {
    this.loading = await checkSession(this.$router)
    await this.getCard()
    this.image = await loadImage(this.imageCode)
  },
}
</script>
<template>
  <div id="main" class="content-wrapper d-flex flex-column flex-grow-1 pt-5" v-if="!loading && cardData">
    <div class="container d-flex flex-column justify-content-center align-items-center h-100">
      <div class="row w-100 d-flex justify-content-center mb-3">
        <button
          @click="goToThanks"
          class="btn btn-lg btn-danger w-75">
          ZAKOŃCZ SPRAWDZANIE
        </button>
      </div>

      <div class="content row w-100 flex-grow-1">
        <div class="container-img col-12 col-md-6 text-center d-flex align-items-center justify-content-center">
          <img
            class="img-fluid"
            :src="image"
            alt="Image"
          />
        </div>
        <div class="col-12 col-md-6 card border-light-subtle p-3 d-flex
         flex-column align-items-center overflow-auto">
          <form @submit.prevent="handleSubmit" class="w-100">
            <DynamicForm :value="jsonData" @update:value="updateJsonData" />
            <div class="text-center mt-3">
              <button type="submit" class="btn btn-lg btn-success w-100">
                WYŚLIJ I PRZEJDŹ DO NASTĘPNEJ KARTY
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="container d-flex flex-column justify-content-center align-items-center mt-5" v-if="!cardData">
    <h1 class="display-4 text-center mb-3 mt-5">KONIEC KART DO WYPEŁNIENIA</h1>
    <button
      @click="goToThanks"
      class="btn btn-lg btn-danger w-auto">
      ZAKOŃCZ SPRAWDZANIE
    </button>
  </div>
</template>

<style scoped>

.card {
  height: 75vh;
  overflow-y: auto;
}

img {
  max-width: 100%;
  max-height: 100%;
  height: 75vh;
  object-fit: contain;
}

@media (max-width: 768px) and (orientation: portrait) {
  .content {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 60px);
  }

  .container-img {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  img {
    max-height: 100%;
    height: auto;
    width: auto;
    object-fit: contain;
  }

  .card {
    flex: 1;
    overflow-y: auto;
  }

  button.btn-danger {
    margin-bottom: 10px;
  }
}
</style>
