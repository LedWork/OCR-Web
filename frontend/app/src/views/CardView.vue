<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from "axios";
import {changeOrientation, checkSession, getCSRFToken, loadJsonData, loadImage} from "@/scripts/utils.js";

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
      <form class="form">
        <DynamicForm :value="jsonData" @update:value="jsonData" :readonly="true" />
      </form>
    </div>
  </div>
</template>

<style scoped>
  .wrapper {
    height: calc(100% - 180px);
  }
</style>
