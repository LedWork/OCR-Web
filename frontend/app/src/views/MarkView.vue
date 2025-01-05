<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from 'axios'
import {
  changeOrientation,
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
        //console.log(response)
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
        const response = await axios.post('api/card/correct', this.cardData, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        })

        if (response.status === 200) {
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
    window.addEventListener('resize', changeOrientation)
  },
  beforeUnmount() {
    window.removeEventListener('resize', changeOrientation)
  },
}
</script>
<template>
  <div class="wrapper horizontal" v-if="!loading">
    <div class="card-wrapper">
      <img :src="image" />
    </div>
    <div class="form-wrapper vertical">
      <form @submit.prevent="handleSubmit" class="form">
        <DynamicForm :value="jsonData" @update:value="updateJsonData" />
        <div style="text-align: center">
          <button type="submit" class="button upload-btn">NASTĘPNA KARTA</button>
        </div>
      </form>

      <button @click="goToThanks" class="button">ZAKOŃCZ SPRAWDZANIE</button>
    </div>
  </div>
</template>

<style></style>
