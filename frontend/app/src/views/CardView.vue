<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from "axios";
import { checkSession, getCSRFToken, loadJsonData, loadImage, parseGtParse} from "@/scripts/utils.js";

export default {
  components: { DynamicForm },
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
      translations: {
        Surname: 'Nazwisko',
        'Name:': 'Imię',
        'Date of birth': 'Data urodzenia',
        Date: 'Data',
        'Donated blood': 'Ilość oddanej krwi',
      },
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
        const response = await axios.post('/api/admin/correct1', this.cardData, {
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
  },
  async mounted() {
    this.loading = await checkSession(this.$router)
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
              <button type="submit" class="btn btn-lg btn-success w-100">ZATWIERDŹ ZMIANY</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.card {
  height: 70vh;
  overflow-y: auto;
}

img {
  max-width: 100%;
  max-height: 100%;
  height: 70vh;
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

