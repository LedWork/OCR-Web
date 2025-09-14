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
       class="d-flex flex-column justify-content-between align-items-center mt-1"
       v-if="!loading">

    <div class="m-2 align-items-center w-50 d-flex justify-content-center">
      <button v-if="admin" class="btn btn-sm w-100 btn-secondary" @click="goToAdmin">ADMIN PANEL</button>
    </div>

    <div class="card border-light-subtle mb-2 instruction-card"
         style="max-width: 80%; width:auto; max-height:75vh; height:auto; overflow-y: auto !important;">
      <div class="card-body p-3">
        <h2 class="text-center mb-3">Instrukcja</h2>
        <div class="instruction-content">
          <p class="text-justify fs-6 mb-3">
            Witamy w systemie ręcznej weryfikacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża.
          </p>
          
          <p class="text-justify fs-6 mb-2">
            Po kliknięciu przycisku <b>"Przejdź dalej"</b> zostanie wyświetlony skan karty Zasłużonego Honorowego Dawcy Krwi 
            wraz z formularzem zawierającym automatycznie odczytane dane. Każde pole formularza jest oznaczone etykietą odpowiadającą oznaczeniom na karcie, 
            zachowując podobną kolejność jak w oryginale. Prosimy o weryfikację poprawności odczytanych danych we wszystkich polach, zgodnie z poniższymi zasadami:
          </p>

          <div class="rules-section mb-3">
            <h6 class="mb-2 text-primary">Zasady weryfikacji:</h6>
            <ul class="rules-list">
              <li>W przypadku błędów należy wprowadzić poprawną wartość.</li>
              <li>Wartości w polach powinny odzwierciedlać rzeczywistość, nie powinny być zmieniane.</li>
              <li>Jeśli pole jest puste, należy pozostawić je puste.</li>
              <li>Jeśli pole zawiera znaki np. "-//-", lub "-", należy wpisać dokładnie te znaki.</li>
              <li>Nie wszystkie dane z karty są obecne w formularzu, w takim przypadku pole należy zignorować.</li>
            </ul>
          </div>
          
          <div class="action-section">
            <p class="text-justify fs-6 mb-2">
              Po zweryfikowaniu wszystkich pól, należy kliknąć przycisk <b>"Wyślij kartę i przejdź do następnej"</b>, 
              aby wysłać kartę do systemu i przejść do kolejnego dokumentu.
            </p>
            
            <p class="text-justify fs-6 mb-2">
              Aby przerwać proces weryfikacji, należy użyć przycisku <b>"X - Zakończ sprawdzanie"</b>.
            </p>
            
            <div class="alert alert-warning mt-2" role="alert">
              <strong>Uwaga:</strong> Użycie przycisku "Zakończ sprawdzanie" spowoduje, że aktualnie weryfikowana karta nie zostanie zapisana w systemie.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="m-2 align-items-center w-50 d-flex justify-content-center">
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
    line-height: 1.4;
  }

  .rules-section {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1rem;
    border-left: 3px solid #0d6efd;
  }

  .rules-list {
    margin: 0;
    padding-left: 1.2rem;
    list-style-type: disc;
  }

  .rules-list li {
    margin-bottom: 0.4rem;
    padding-left: 0.3rem;
    line-height: 1.3;
    font-size: 0.9rem;
  }

  .rules-list li:last-child {
    margin-bottom: 0;
  }

  .action-section {
    background-color: #fff;
    border-radius: 6px;
    padding: 0.5rem 0;
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
      margin-top: 60px !important;
      justify-content: start !important;
    }

    div.card {
      max-width: 95% !important;
      max-height: 70vh !important;
    }

    .rules-section {
      padding: 0.8rem;
    }
  }

  @media(max-width: 768px) {
    div.card {
      margin-bottom: 0 !important;
      max-height: 65vh !important;
    }

    .card-body {
      padding: 1rem !important;
    }

    .rules-section {
      padding: 0.6rem;
    }

    .rules-list {
      padding-left: 0.8rem;
    }

    .rules-list li {
      font-size: 0.85rem;
      margin-bottom: 0.3rem;
    }

    button.btn.btn-lg {
      font-size: 4vw !important;
      width: 100% !important;
    }
  }
</style>
