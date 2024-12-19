<script>
import axios from 'axios'
const apiUrl = import.meta.env.VITE_API_URL
export default {
  data() {
    return {
      loading: true,
    }
  },
  async mounted() {
    try {
      this.csrfToken = this.getCookie('CSRF-TOKEN')
      const response = await axios.get(apiUrl + '/auth/session', {
        headers: {
          'X-CSRF-TOKEN': this.csrfToken,
        },
        withCredentials: true,
      })
      console.log(response)
      if (response.status != 200) {
        this.$router.push('/')
      } else this.loading = false
    } catch (e) {
      this.$router.push('/')
    }
  },
  methods: {
    goToMarking() {
      this.$router.push('/oznaczanie')
    },
  },
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <div class="text-block">
      <p class="title">Instrukcja</p>
      <p class="content">
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quas earum dignissimos ipsum
        assumenda ratione explicabo consequatur quo cupiditate mollitia quibusdam eveniet eum,
        tempore fugit. Magni itaque doloremque ea! Distinctio, possimus.
      </p>
    </div>
    <div class="button" @click="goToMarking">PRZEJDŹ DALEJ</div>
  </div>
</template>
<style></style>
