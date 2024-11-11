<script>
import DynamicForm from "@/components/DynamicForm.vue";
export default {
  components: {
    DynamicForm
  },
  data() {
    return {
      card: null,
      jsonData: {},
      imageCode: "",
      translations: {
        'Surname': 'Nazwisko',
        'Name': 'Imię',
        'Date of birth': 'Data urodzenia',
        'Date': 'Data',
        'Donated blood': 'Ilość oddanej krwi'
      }
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
    GetCard() {
      //here send request for card and json and set
      //local vars card and jsonData as response
      this.card = '/static/test.png'
      this.loadJsonData();
    },
    // temporary func for testing
    async loadJsonData() {
      try {
        const response = await fetch('/test.json');
        const data = await response.json();

        this.image_code = data.image_code;

        this.jsonData = this.parseGtParse(data.gt_parse);
      } catch (error) {
        console.error("Error loading JSON:", error);
      }
    },
    parseGtParse(data) {
      // recursive loading data
      const formattedData = {};
      for (const [key, value] of Object.entries(data)) {
        const tKey = this.translations[key] || key;

        if (typeof value === "object" && value !== null) {
          formattedData[tKey] = this.parseGtParse(value);
        } else {
          formattedData[tKey] = value;
        }
      }
      return formattedData;
    },
  },
  mounted() {
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
  <div class="wrapper vertical">
    <div class="card-wrapper">
      <img :src="card" />
    </div>
    <div class="form-wrapper vertical">
       <form @submit.prevent="handleSubmit" class="form">
         <DynamicForm :value="jsonData" @update:value="jsonData"/>
         <div class="button">WYŚLIJ</div>
       </form>
    </div>
  </div>
</template>
