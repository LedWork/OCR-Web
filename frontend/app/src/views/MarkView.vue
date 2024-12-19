<script>
import DynamicForm from '@/components/DynamicForm.vue'
import axios from 'axios'
export default {
  components: {
    DynamicForm,
  },
  data() {
    return {
      loading: true,
      card: null,
      jsonData: {},
      imageCode: '',
      translations: {
        Surname: 'Nazwisko',
        Name: 'Imię',
        'Date of birth': 'Data urodzenia',
        Date: 'Data',
        'Donated blood': 'Ilość oddanej krwi',
      },
    }
  },
  methods: {
    ChangeOrientation() {
      if (window.screen.width > 768) {
        document.querySelector('.wrapper').classList.add('horizontal')
        document.querySelector('.wrapper').classList.remove('vertical')
      } else {
        document.querySelector('.wrapper').classList.remove('horizontal')
        document.querySelector('.wrapper').classList.add('vertical')
      }
    },
    async GetCard() {
      try {
        const response = await axios.get('http://localhost:5000/card/random')
        console.log(response.data)
        await this.loadJsonData(response.data)
      } catch (error) {
        console.log(error)
      }
    },
    async loadJsonData(data) {
      try {
        this.image_code = data.image_code
        this.jsonData = this.parseGtParse(data.gt_parse)
      } catch (error) {
        console.error('Error loading JSON:', error)
      }
    },
    async loadImage() {
      try {
        const response = await axios.get(`http://localhost:5000/image/${this.image_code}`)

        if (response.data.photo) {
          this.card = `data:image/jpeg;base64,${response.data.photo}`
        } else {
          console.error('No image found in the response')
        }
      } catch (error) {
        console.error('Error loading image:', error)
      }
    },
    parseGtParse(data) {
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

      for (const [key, value] of Object.entries(data)) {
        const tKey = this.translations[key] || key

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
  },
  async mounted() {
    try {
      const response = await axios.get(apiUrl + '/auth/session', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      console.log(response)
      if (!response.ok) {
        this.$router.push('/')
      } else this.loading = false
    } catch (e) {
      this.$router.push('/')
    }
    this.ChangeOrientation()
    this.GetCard()
    window.addEventListener('resize', this.ChangeOrientation)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.ChangeOrientation)
  },
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <div class="card-wrapper">
      <img :src="card" />
    </div>
    <div class="form-wrapper vertical">
      <form @submit.prevent="handleSubmit" class="form">
        <DynamicForm :value="jsonData" @update:value="jsonData" />
        <div class="button">WYŚLIJ</div>
      </form>
    </div>
  </div>
</template>
