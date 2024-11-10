<script>
export default {
  data() {
    return {
      card: null,
      jsonData: null,
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
    },
  },
  mounted() {
    this.ChangeOrientation()
    this.GetCard()
    window.addEventListener('resize', this.ChangeOrientation)
  },
  beforeDestroy() {
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
      <span class="input vertical">
        <p class="caption">IMIE</p>
        <input type="text" class="text-input" />
      </span>
      <span class="input vertical">
        <p class="caption">NAZWISKO</p>
        <input type="text" class="text-input" />
      </span>
      <span class="input vertical">
        <p class="caption">Cos tam</p>
        <input type="text" class="text-input" />
      </span>
      <span class="input vertical">
        <p class="caption">cos tam</p>
        <input type="text" class="text-input" />
      </span>
      <span class="input vertical">
        <p class="caption">cos tam</p>
        <input type="text" class="text-input" />
      </span>
      <div class="button">WYŚLIJ</div>
    </div>
  </div>
</template>
<style scoped>
.wrapper {
  padding-top: 20px;
}
.card-wrapper {
  width: 100%;
  height: 100%;
}
img {
  width: 100%;
}
.form-wrapper {
  width: 100%;
  height: 100%;
  overflow: scroll;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 20px;
}
</style>
