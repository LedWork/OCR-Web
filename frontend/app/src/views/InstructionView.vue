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

    <div class="card border-light-subtle mb-md-5 mb-1 instruction-card"
         style="max-width: 70%; width:auto; max-height:70%; height:auto; overflow-y: auto !important;">
      <div class="card-body p-4">
        <h1 class="text-center mb-4">Instrukcja</h1>
        <div class="instruction-content">
          <p class="text-justify fs-6 mb-4">
            Witamy w systemie ręcznej weryfikacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża.
          </p>
          
          <p class="text-justify fs-6 mb-3">
            Po kliknięciu przycisku <b>"Przejdź dalej"</b> zostanie wyświetlony skan karty Zasłużonego Honorowego Dawcy Krwi 
            wraz z formularzem zawierającym automatycznie odczytane dane. Każde pole formularza jest oznaczone etykietą odpowiadającą oznaczeniom na karcie, 
            zachowując podobną kolejność jak w oryginale. Prosimy o weryfikację poprawności odczytanych danych we wszystkich polach, zgodnie z poniższymi zasadami:
          </p>

          <div class="rules-section mb-4">
            <h5 class="mb-3 text-primary">Zasady weryfikacji:</h5>
            <ul class="rules-list">
              <li>W przypadku błędów należy wprowadzić poprawną wartość.</li>
              <li>Wartości w polach powinny odzwierciedlać rzeczywistość, nie powinny być zmieniane.</li>
              <li>Jeśli pole jest puste, należy pozostawić je puste.</li>
              <li>Jeśli pole zawiera znaki np. "-//-", lub "-", należy wpisać dokładnie te znaki.</li>
              <li>Nie wszystkie dane z karty są obecne w formularzu, w takim przypadku pole należy zignorować.</li>
            </ul>
          </div>
          
          <div class="action-section">
            <p class="text-justify fs-6 mb-3">
              Po zweryfikowaniu wszystkich pól, należy kliknąć przycisk <b>"Wyślij kartę i przejdź do następnej"</b>, 
              aby wysłać kartę do systemu i przejść do kolejnego dokumentu.
            </p>
            
            <p class="text-justify fs-6 mb-3">
              Aby przerwać proces weryfikacji, należy użyć przycisku <b>"X - Zakończ sprawdzanie"</b>.
            </p>
            
            <div class="alert alert-warning mt-3" role="alert">
              <strong>Uwaga:</strong> Użycie przycisku "Zakończ sprawdzanie" spowoduje, że aktualnie weryfikowana karta nie zostanie zapisana w systemie.
            </div>
          </div>
        </div>
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

  .instruction-card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
  }

  .instruction-content {
    line-height: 1.6;
  }

  .rules-section {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    border-left: 4px solid #0d6efd;
  }

  .rules-list {
    margin: 0;
    padding-left: 1.5rem;
    list-style-type: disc;
  }

  .rules-list li {
    margin-bottom: 0.75rem;
    padding-left: 0.5rem;
    line-height: 1.5;
  }

  .rules-list li:last-child {
    margin-bottom: 0;
  }

  .action-section {
    background-color: #fff;
    border-radius: 8px;
    padding: 1rem 0;
  }

  .alert {
    border-radius: 8px;
    border: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

    .rules-section {
      padding: 1rem;
    }
  }

  @media(max-width: 768px) {
    div.card {
      margin-bottom: 0 !important;
    }

    .card-body {
      padding: 1.5rem !important;
    }

    .rules-section {
      padding: 0.75rem;
    }

    .rules-list {
      padding-left: 1rem;
    }

    button.btn.btn-lg {
      font-size: 5vw !important;
      width: 100% !important;
    }
  }
</style>
