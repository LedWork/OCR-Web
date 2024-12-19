<script>
import { globalState } from '@/scripts/store'
import axios from 'axios'
const apiUrl = import.meta.env.VITE_API_URL
export default {
  // async created() {
  //   const response = await axios.get(apiUrl + '/csrf-token')
  //   this.csrfToken = response.data.csrf_token
  // },
  data() {
    return {
      login: null,
      password: null,
      csrfToken: null,
    }
  },
  methods: {
    async goToInstruction() {
      const getCSRFToken = () => {
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';')
          for (let cookie of cookies) {
            cookie = cookie.trim()
            let [cookieName, cookieValue] = cookie.split('=')
            if (cookieName == 'csrftoken') return cookieValue
          }
        }
        return null
      }
      try {
        // const response = await axios.post(
        //   apiUrl + '/auth/login',
        //   {
        //     login: this.login,
        //     password: this.password,
        //   },
        //   {
        //     headers: {
        //       'X-CSRF-TOKEN': this.csrfToken,
        //     },
        //   },
        // )
        // if (response.status == 200) {
        //   console.log(response.status)
        //   globalState.isAuthenticated = true
        //   this.$router.push('/instrukcja')
        // }
        const response = fetch(apiUrl + '/auth/login', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          body: JSON.stringify({ Hello: 'World' }),
        })
      } catch (e) {}
    },
  },
}
</script>
<template>
  <div class="wrapper vertical">
    <div class="text-block">
      <p class="title">ZALOGUJ SIĘ ABY KONTUNOWAĆ...</p>
      <input
        placeholder="Login..."
        class="input text-input"
        type="text"
        name="login"
        v-model="login"
      />
      <input
        placeholder="Haslo..."
        class="input text-input"
        type="password"
        name="password"
        v-model="password"
      />
      <div class="btn-wrapper">
        <div class="button" @click="goToInstruction">ZALOGUJ SIĘ</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.title {
  text-align: center;
  font-size: 20px;
}
.button {
  font-size: 20px;
}
@media (min-width: 1024px) {
  .text-block {
    width: 30%;
    padding: 30px;
  }
  .title {
    font-size: 25px;
  }
  .button {
    font-size: 35px;
  }
}
.btn-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
