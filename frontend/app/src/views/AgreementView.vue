<script>
import {checkSession} from "@/scripts/utils.js";
import {getCSRFToken} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true
    }
  },
  async mounted() {
    try {
      this.loading = await checkSession(this.$router);
    } catch (error) {
      console.error("An error occurred while checking agreement status:", error);
      alert("An error occurred. Please reload the page or try again later.");
    }
  },
  methods: {
    async submitAgreement() {
      const response = await fetch("/api/agreement/contract", {
        method: "POST",
        headers: {
          'X-CSRF-TOKEN': getCSRFToken(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agree: "on" }) // Send 'agree' as JSON
      });

      if (response.ok) {
        this.$router.push({ name: "instruction" }); // Navigate to instruction page
      }
    }
  }
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
        <h1 class="text-center">Contract Agreement</h1>
        <p class="text-justify fs-6 text-md-f">
          # Umowa o Zachowaniu Poufności w Procesie Ręcznej Weryfikacji Zdigitalizowanych Honorowych Kart Krwiodawców
          <br>
          ## Sekcja 1: Identyfikacja Stron
          - **Administrator Danych**: Polski Czerwony Krzyż z siedzibą w Warszawie (00-561) przy ul. Mokotowskiej 14, iod@pck.pl
          - **Weryfikator**: [Imię i nazwisko, adres, dane kontaktowe]
          <br>
          ---
          <br>
          ## Sekcja 2: Zakres i Cel
          Weryfikator przyjmuje do wiadomości, że:
          1. Jego zadaniem jest wyłącznie potwierdzenie zgodności zdigitalizowanych danych (numery PESEL, imiona i nazwiska, daty urodzenia, ilość oddanej krwi) z zeskanowanymi honorowymi kartami krwiodawców dostarczonymi przez Administratora Danych.
          2. Weryfikator nie nabywa żadnych praw do przechowywania, kopiowania lub wykorzystywania tych danych w celach innych niż wskazane powyżej.
          <br>
          ---
          <br>
          ## Sekcja 3: Obowiązki
          Weryfikator zobowiązuje się do:
          1. Wykorzystywania udostępnionych danych osobowych wyłącznie w procesie weryfikacji zgodnie z instrukcjami Administratora Danych.
          2. Zachowania danych w ścisłej poufności i nieujawniania ich osobom trzecim.
          3. Nie kopiowania, zapisywania ani przechowywania danych w żadnej formie poza zatwierdzonym procesem weryfikacji.
          4. Zwrócenia lub usunięcia wszystkich danych po zakończeniu weryfikacji, zgodnie z instrukcjami Administratora Danych.
          <br>
          ---
          <br>
          ## Sekcja 4: Zasady RODO
          Weryfikator przyjmuje do wiadomości zasady RODO, w tym:
          1. Przetwarzanie danych zgodnie z prawem, w sposób rzetelny i przejrzysty (**Art. 5 RODO**).
          2. Utrzymanie poufności i integralności danych osobowych (**Art. 32 RODO**).
          <br>
          ---
          <br>
          ## Sekcja 5: Konsekwencje Naruszenia
          Naruszenie warunków niniejszej umowy może skutkować:
          1. Natychmiastowym zakończeniem współpracy w ramach procesu weryfikacji.
          2. Podjęciem działań prawnych na podstawie obowiązujących przepisów dotyczących ochrony danych osobowych, w tym kar wynikających z RODO.
          <br>
          ---
          <br>
          ## Sekcja 6: Potwierdzenie
          Podpisując tę umowę, Weryfikator potwierdza zrozumienie i akceptację opisanych powyżej obowiązków i zobowiązań.
        </p>
      </div>
    </div>

    <div class="m-3 align-items-center w-50 d-flex justify-content-center mt-1 mt-md-5">
      <button class="btn btn-primary w-100 btn-lg" @click="submitAgreement">ZGADZAM SIĘ</button>
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
