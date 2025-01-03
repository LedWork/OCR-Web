<script>
import {adminCheckSession, changeOrientation, checkSession} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true,
      admin: false
    }
  },
  async mounted() {
    this.loading = await checkSession(this.$router);
    this.admin = await adminCheckSession();
    window.addEventListener('resize', changeOrientation)
  },
  beforeUnmount() {
    window.removeEventListener('resize', changeOrientation)
  },
  methods: {
    goToMarking() {
      this.$router.push({name: 'marking'})
    },
    goToAdmin() {
      this.$router.push({name: 'admin'})
    }
  },
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <div v-if="admin" class="button" @click="goToAdmin">ADMIN PANEL</div>
    <div class="text-block">
      <p class="title">Instrukcja</p>
      <p class="content">
        Po kliknięciu przycisku <b>"Przejdź dalej"</b> po lewej stronie zobaczysz zdjęcie karty, a po prawej formularz
        z danymi odczytanymi ze zdjęcia. Nad każdym polem formularza znajduje się etykieta, która odpowiada etykiecie
        na zdjęciu karty. Pola w większości przypadków będą w takiej samej kolejności jak na zdjęciu.
        <br>Jeśli tekst w polu jest zgodny z tym, co widać na zdjęciu, przejdź do kolejnego pola. Jeśli tekst się nie
        zgadza, popraw wpisz w polu poprawny tekst. Po potwierdzeniu wszystkich pól kliknij przycisk
        <b>"Następna karta"</b>, aby przejść do kolejnej karty do wypełnienia!
        <br>Jeśli chcesz zakończyć sprawdzanie, kliknij przycisk <b>"Zakończ sprawdzanie"</b>.
        <br><b>WAŻNE!</b> Po kliknięciu tego
        przycisku sprawdzana karta nie zostanie wysłana do systemu!
      </p>
    </div>
    <div class="button" @click="goToMarking">PRZEJDŹ DALEJ</div>
  </div>
</template>
<style></style>
