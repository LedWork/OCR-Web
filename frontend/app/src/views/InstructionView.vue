<script>
import {adminCheckSession, checkSession} from "@/scripts/utils.js";
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
  <div id="ins-main"
       class="d-flex flex-column justify-content-between align-items-center mt-1 mt-md-4"
       v-if="!loading">

    <div class="m-3 align-items-center w-50 d-flex justify-content-center">
      <button v-if="admin" class="btn btn-lg w-100 btn-secondary" @click="goToAdmin">ADMIN PANEL</button>
    </div>

    <div class="card border-light-subtle mb-md-5 mb-1"
         style="max-width: 70%; width:auto; max-height:70%; height:auto; overflow-y: auto !important;">
      <div class="card-body">
        <h1 class="text-center">Instrukcja</h1>
        <p class="text-justify fs-6 text-md-f">
          Witamy w systemie ręcznej weryfikacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża.
          <br><br>
          Po kliknięciu przycisku <b>"Przejdź dalej"</b> zostanie wyświetlony skan karty Zasłużonego Honorowego Dawcy Krwi 
          wraz z formularzem zawierającym automatycznie odczytane dane. Każde pole formularza jest oznaczone etykietą odpowiadającą oznaczeniom na karcie, 
          zachowując podobną kolejność jak w oryginale. Prosimy o weryfikację poprawności odczytanych danych we wszystkich polach, zgodnie z poniższymi zasadami:

          <li> W przypadku błędów należy wprowadzić poprawną wartość. </li>
          <li> Wartości w polach powinny odzwierciedlać rzeczywistość, nie powinny być zmieniane. </li>
          <li> Jeśli pole jest puste, należy pozostawić je puste. </li>
          <li> Jeśli pole zawiera znaki np. "-//-", lub "-", należy wpisać dokładnie te znaki. </li>
          <li> Nie wszystkie dane z karty są obecne w formularzu, w takim przypadku pole należy zignorować. </li>
          
          <br>
          Po zweryfikowaniu wszystkich pól, należy kliknąć przycisk <b>"Wyślij kartę i przejdź do następnej"</b>, aby wysłać kartę do systemu i przejść do kolejnego dokumentu.
          <br>
          Aby przerwać proces weryfikacji, należy użyć przycisku <b>"X - Zakończ sprawdzanie"</b>.
          <br>
          <b>Uwaga:</b> Użycie przycisku "Zakończ sprawdzanie" spowoduje, że aktualnie weryfikowana karta nie zostanie zapisana w systemie.
        </p>
      </div>
    </div>

    <div class="m-3 align-items-center w-50 d-flex justify-content-center mt-1 mt-md-5">
      <button class="btn btn-primary w-100 btn-lg" @click="goToMarking">PRZEJDŹ DALEJ</button>
    </div>
  </div>
</template>

<style scoped>
  body {
    overflow: hidden;
  }

  p {
    text-align: justify;
  }

  @media(max-width: 1000px) {
    div.d-flex {
      margin-top: 80px !important;
      justify-content: start !important;
    }

    div.card {
      max-width: 95% !important;
    }
  }

  @media(max-width: 768px) {
    div.card {
      margin-bottom: 0 !important;
    }

    button.btn.btn-lg {
      font-size: 5vw !important;
      width: 100% !important;
    }
  }
</style>
