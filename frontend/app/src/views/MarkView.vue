<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from 'axios'
import { changeOrientation, checkSession, getCSRFToken } from '@/scripts/utils.js'

export default {
  components: {
    DynamicForm,
  },
  data() {
    return {
      loading: true,
      card: null,
      cardData: null,
      jsonData: {},
      imageCode: '',
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
        const response = await axios.get('/api/card/random')
        console.log(response)
        await this.loadJsonData(response.data)
      } catch (error) {
        console.log(error)
      }
    },
    async loadJsonData(data) {
      try {
        this.image_code = data.image_code
        this.jsonData = this.parseGtParse(data.gt_parse)
        this.cardData = data
      } catch (error) {
        console.error('Error loading JSON:', error)
      }
    },
    async loadImage() {
      try {
        const response = await axios.get(`api/image/${this.image_code}`)
        if (response.data[0].photo) {
          this.card = `data:image/jpeg;base64,${response.data[0].photo}`
        } else {
          console.error('No image found in the response')
        }
      } catch (error) {
        console.error('Error loading image:', error)
      }
    },
    parseGtParse(data, reverse=false) {
      const fieldOrder1 = [
        'Nazwisko',
        'Imię',
        'Data urodzenia',
        'V st.',
        'IV st.',
        'III st.',
        'II st.',
        'I st.',
      ]
      const fieldOrder2 = ['Nr', 'Data', 'ZR', 'Ilość oddanej krwi']

      const formattedData = {}

      const translationsMap = reverse
        ? Object.fromEntries(
          Object.entries(this.translations).map(([key, value]) => [value, key])
        )
        : this.translations;

      for (const [key, value] of Object.entries(data)) {
        const tKey = translationsMap[key] || key

        if (typeof value === 'object' && value !== null) {
          formattedData[tKey] = this.parseGtParse(value, fieldOrder2)
        } else {
          formattedData[tKey] = value
        }
      }

      const reorderFields = (data, order) => {
        const ordered = {}
        order.forEach((field) => {
          if (field in data) {
            ordered[field] = data[field]
          }
        })
        for (const key in data) {
          if (!(key in ordered)) {
            ordered[key] = data[key]
          }
        }
        return ordered
      }
      return reorderFields(formattedData, fieldOrder1)
    },
    async handleSubmit() {
      try {
        this.jsonData = this.parseGtParse(this.jsonData, true)
        this.cardData.gt_parse = this.jsonData
        console.log(this.cardData)
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
  },
  async mounted() {
    this.loading = await checkSession(this.$router)
    await this.getCard()
    await this.loadImage()
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
      <img :src="card" />
    </div>
    <div class="form-wrapper vertical">
      <form @submit.prevent="handleSubmit" class="form">
        <DynamicForm :value="jsonData" @update:value="jsonData" />
        <button type="submit" class="button">WYŚLIJ</button>
      </form>
    </div>
  </div>
</template>

<style></style>
