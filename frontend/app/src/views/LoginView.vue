<script>
import { globalState } from '@/scripts/store'
import axios from 'axios'
import {getCSRFToken} from "@/scripts/utils.js";
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
      error: null,
    }
  },
  methods: {
    async goToAgreement() {
      try {
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
          globalState.isAuthenticated = true
          this.$router.push({name: 'agreement'})
        }
      } catch(error) {
        console.error(error)
        this.error = error.response.data.message
      }
    },
    async goToInstruction() {
      try {
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
          globalState.isAuthenticated = true
          this.$router.push({name: 'instruction'})
        }
      } catch(error) {
        console.error(error)
        this.error = error.response.data.message
      }
    },
    // TEMPORARY FOR TESTING, WILL BE DELETED IN PROD VERSION
    async makeAdmin() {
      const response = await axios.post(
        '/api/admin/temp-admin',
        {},
        {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        },
      )

      if (response.status === 200) {
        alert(response.data.message);
      }
    }
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

      <p v-if="error" class="error">{{ error }}</p>

      <div class="btn-wrapper">
        <div class="button" @click="goToAgreement">ZALOGUJ SIĘ</div>
      </div>

      <div class="btn-wrapper">
        <div class="button" @click="makeAdmin">CREATE ADMIN </div>
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
