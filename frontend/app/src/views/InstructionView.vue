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
        <h1 class="text-center mb-4 instruction-title">Instrukcja</h1>
        <div class="instruction-content">
          <p class="text-justify instruction-text mb-4">
            Witamy w systemie ręcznej weryfikacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża.
          </p>
          
          <p class="text-justify instruction-text mb-3">
            Po kliknięciu przycisku <strong class="highlight-text">"Przejdź dalej"</strong> zostanie wyświetlony skan karty Zasłużonego Honorowego Dawcy Krwi 
            wraz z formularzem zawierającym automatycznie odczytane dane. Każde pole formularza jest oznaczone etykietą odpowiadającą oznaczeniom na karcie, 
            zachowując podobną kolejność jak w oryginale. Prosimy o weryfikację poprawności odczytanych danych we wszystkich polach, zgodnie z poniższymi zasadami:
          </p>

          <div class="rules-section mb-4">
            <h3 class="mb-3 rules-title">Zasady weryfikacji:</h3>
            <ul class="rules-list">
              <li>W przypadku błędów należy wprowadzić poprawną wartość.</li>
              <li>Wartości w polach powinny odzwierciedlać rzeczywistość, nie powinny być zmieniane.</li>
              <li>Jeśli pole jest puste, należy pozostawić je puste.</li>
              <li>Jeśli pole zawiera znaki np. "-//-", lub "-", należy wpisać dokładnie te znaki.</li>
              <li>Nie wszystkie dane z karty są obecne w formularzu, w takim przypadku pole należy zignorować.</li>
            </ul>
          </div>
          
          <div class="action-section">
            <p class="text-justify instruction-text mb-3">
              Po zweryfikowaniu wszystkich pól, należy kliknąć przycisk <strong class="highlight-text">"Wyślij kartę i przejdź do następnej"</strong>, 
              aby wysłać kartę do systemu i przejść do kolejnego dokumentu.
            </p>
            
            <p class="text-justify instruction-text mb-3">
              Aby przerwać proces weryfikacji, należy użyć przycisku <strong class="highlight-text">"X - Zakończ sprawdzanie"</strong>.
            </p>
            
            <div class="alert alert-warning mt-3 warning-alert" role="alert">
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
    line-height: 1.6;
  }

  .instruction-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #2c3e50;
    letter-spacing: 0.5px;
  }

  .instruction-text {
    font-size: 1.1rem;
    font-weight: 400;
    color: #2c3e50;
    line-height: 1.7;
  }

  .highlight-text {
    color: #0d6efd;
    font-weight: 600;
    background-color: rgba(13, 110, 253, 0.1);
    padding: 2px 4px;
    border-radius: 3px;
  }

  .rules-section {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1.2rem;
    border-left: 4px solid #0d6efd;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .rules-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #0d6efd;
    margin-bottom: 1rem;
  }

  .rules-list {
    margin: 0;
    padding-left: 1.5rem;
    list-style-type: disc;
  }

  .rules-list li {
    margin-bottom: 0.8rem;
    padding-left: 0.5rem;
    line-height: 1.6;
    font-size: 1rem;
    font-weight: 400;
    color: #2c3e50;
  }

  .rules-list li:last-child {
    margin-bottom: 0;
  }

  .action-section {
    background-color: #fff;
    border-radius: 8px;
    padding: 0.8rem 0;
  }

  .warning-alert {
    font-size: 1rem;
    font-weight: 500;
    border-left: 4px solid #ffc107;
    background-color: #fff3cd;
    color: #856404;
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

    .instruction-title {
      font-size: 1.8rem;
    }

    .instruction-text {
      font-size: 1rem;
    }

    .rules-title {
      font-size: 1.2rem;
    }

    .rules-section {
      padding: 1rem;
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

    .instruction-title {
      font-size: 1.6rem;
      margin-bottom: 1rem;
    }

    .instruction-text {
      font-size: 0.95rem;
      line-height: 1.6;
    }

    .rules-title {
      font-size: 1.1rem;
    }

    .rules-section {
      padding: 0.8rem;
    }

    .rules-list {
      padding-left: 1.2rem;
    }

    .rules-list li {
      font-size: 0.9rem;
      margin-bottom: 0.6rem;
      line-height: 1.5;
    }

    .warning-alert {
      font-size: 0.9rem;
    }

    button.btn.btn-lg {
      font-size: 1.1rem !important;
      width: 100% !important;
      padding: 0.75rem 1rem;
    }
  }
</style>
