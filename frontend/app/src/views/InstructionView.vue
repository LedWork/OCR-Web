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
        Witamy w systemie digitalizacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża.
        <br><br>
        Po kliknięciu przycisku <b>"Przejdź dalej"</b> zostanie wyświetlony skan karty Zasłużonego Honorowego Dawcy Krwi 
        wraz z formularzem zawierającym automatycznie odczytane dane. Każde pole formularza jest oznaczone etykietą odpowiadającą oznaczeniom na karcie, 
        zachowując podobną kolejność jak w oryginale.
        <br><br>
        Prosimy o weryfikację poprawności odczytanych danych we wszystkich polach. W przypadku błędów należy wprowadzić poprawną wartość.
        Po zweryfikowaniu wszystkich pól, należy kliknąć przycisk <b>"Następna karta"</b>, aby wysłać kartę do systemu i przejść do kolejnego dokumentu.
        <br><br>
        Aby przerwać proces weryfikacji, należy użyć przycisku <b>"Zakończ sprawdzanie".</b>.
        <br><br>
        <b>Uwaga:</b> Użycie przycisku "Zakończ sprawdzanie" spowoduje, że aktualnie weryfikowana karta nie zostanie zapisana w systemie.
      </p>
    </div>
    <div class="button" @click="goToMarking">PRZEJDŹ DALEJ</div>
  </div>
</template>
<style></style>
