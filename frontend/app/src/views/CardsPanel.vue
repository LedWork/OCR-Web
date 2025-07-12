<script>
import axios from "axios";
import {adminCheckSession, getCSRFToken} from "@/scripts/utils.js";

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
  },
}
</script>

<template>
  <div class="container mt-5" v-if="admin">
    <div class="d-flex justify-content-between mb-4">
      <button @click="goToAdminPanel" class="btn btn-danger btn-lg">Wróć</button>
      <button @click="logout" class="btn btn-danger btn-lg">Wyloguj</button>
    </div>

    <div class="table-responsive w-75 mx-auto">
      <table class="table table-striped table-bordered">
        <thead class="table-dark">
        <tr class="text-center">
          <th class="w-50">Image Code</th>
          <th class="w-25">Check Status</th>
          <th class="w-25">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(card, index) in cards" :key="index">
          <td>{{ card.image_code }}</td>
          <td class="text-center">
            <span 
              :class="card.is_green ? 'text-success fw-bold' : 'text-muted'"
              :style="card.is_green ? 'color: #28a745 !important;' : ''"
            >
              {{ card.check_status }}
            </span>
          </td>
          <td class="d-flex gap-2 justify-content-center">
            <button class="btn btn-info text-white btn-sm" @click="viewImage(card.image_code)">Pokaż</button>
            <button class="btn btn-danger btn-sm" @click="deleteImage(card.image_code)">Usuń</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>

</style>
