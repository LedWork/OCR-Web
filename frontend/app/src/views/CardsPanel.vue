<script>
import axios from "axios";
import {adminCheckSession, changeOrientation, getCSRFToken} from "@/scripts/utils.js";

export default {
  data() {
    return {
      admin: false,
      cards: [],
    }
  },
  methods: {
    goToAdminPanel() {
      this.$router.push({name: "admin"});
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
    async fetchCards() {
      try {
        const response = await axios.get('/api/admin/cards')
        this.cards = response.data;
        console.log(this.cards);
      }
      catch (error) {
        console.error(error);
      }
    },
    viewImage(imageCode) {
      this.$router.push(`/card/${imageCode}`);
    },
    async deleteImage(imageCode) {
      const response = await axios.delete(
        '/api/admin/card/' + imageCode,
        {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        });
      if (response.status === 200) {
        alert(`Successfully deleted`);
        await this.fetchCards();
      }
    },
  },
  async mounted(){
    this.admin = await adminCheckSession(this.$router);
    await this.fetchCards();
    changeOrientation();
    window.addEventListener("resize", changeOrientation);
  },
  beforeunload() {
    window.removeEventListener("resize", changeOrientation);
  }
}
</script>

<template>
  <div class="wrapper">
    <div class="container" v-if="admin">
      <div class="button-container">
        <button @click="goToAdminPanel" class="admin-button">Back</button>
        <button @click="logout" class="admin-button logout-btn">Logout</button>
      </div>

      <div class="image-table">
        <table>
          <thead>
          <tr>
            <th>Image Code</th>
            <th>View</th>
            <th>Delete</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(card, index) in cards" :key="index">
            <td>{{ card }}</td>
            <td>
              <button @click="viewImage(card)">View</button>
            </td>
            <td>
              <button @click="deleteImage(card)">Delete</button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
