<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from "axios";
import {changeOrientation, checkSession, getCSRFToken, loadJsonData, loadImage, parseGtParse} from "@/scripts/utils.js";

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
        const response = await axios.post('/api/admin/correct', this.cardData, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        })

        if (response.status === 200) {
          alert(response.data.message)
          this.goToCardsPanel()
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
    window.addEventListener('resize', changeOrientation)
  },
  beforeUnmount() {
    window.removeEventListener('resize', changeOrientation)
  },
}
</script>

<template>
  <div style="padding:10px;">
    <h1>Card: {{ imageCode }}</h1>
    <div class="button-container">
      <button @click="goToCardsPanel" class="admin-button">Back</button>
      <button @click="logout" class="admin-button logout-btn">Logout</button>
    </div>
  </div>
  <div class="wrapper horizontal" v-if="!loading">
    <div class="card-wrapper">
      <img :src="image" />
    </div>

    <div class="form-wrapper vertical">
      <form @submit.prevent="handleSubmit" class="form">
        <DynamicForm :value="jsonData" @update:value="updateJsonData" />
        <div style="text-align: center">
          <button type="submit" class="button upload-btn">ZATWIERDŹ ZMIANY</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
  .wrapper {
    height: calc(100% - 180px);
  }
</style>
