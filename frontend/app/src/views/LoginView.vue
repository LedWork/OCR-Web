<script>
import { globalState } from '@/scripts/store'
import axios from 'axios'
import {getCSRFToken} from "@/scripts/utils.js";
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
      try {
         /*const addUser = await axios.post(
           '/api/admin/add-user',
           {
             login: this.login,
             password: this.password,
           },
           {
             headers: {
               'X-CSRF-TOKEN': getCSRFToken(),
             },
           },
         )*/
        const response = await axios.post(
          '/api/auth/login',
          {
            login: this.login,
            password: this.password,
          },
          {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          },
        )
        if (response.status === 200) {
          console.log(response.status)
          globalState.isAuthenticated = true
          this.$router.push('/instrukcja')
        }
      } catch {}
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
