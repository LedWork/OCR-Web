<script>
import {checkSession} from "@/scripts/utils.js";
import {getCSRFToken} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true,
      userEmail: ''
    }
  },
  async mounted() {
    try {
      this.loading = await checkSession(this.$router);
      // Fetch user email
      const response = await fetch("/api/auth/session", {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        this.userEmail = data.email || '';
      }
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

    <div class="card border-light-subtle mb-md-3 mb-1 mt-1 mt-md-3"
         style="max-width: 70%; width:auto; max-height:70%; height:auto;">
      <div class="card-body"
           style="height: 70vh; overflow-y: auto;">
        <h1 class="text-center agreement-title">Umowa o zachowaniu poufności</h1>
        <div class="agreement-content">
          <h2 class="section-title">Umowa o zachowaniu poufności w procesie ręcznej weryfikacji kart Zasłużonych Honorowych Dawców Krwi Polskiego Czerwonego Krzyża</h2>
          
          <h3 class="subsection-title">Identyfikacja Stron</h3>
          <div class="agreement-text">
            - <strong class="highlight-text">Administrator Danych</strong>: Polski Czerwony Krzyż z siedzibą w Warszawie (00-561) przy ul. Mokotowskiej 14, iod@pck.pl
            <br>
            - <strong class="highlight-text">Weryfikator</strong>: {{ userEmail }}
          </div>
          
          <h3 class="subsection-title">Zakres i Cel</h3>
          <div class="agreement-text">
            Weryfikator przyjmuje do wiadomości, że: <br>
            1. Administrator Danych udostępnia Weryfikatorowi dane osobowe i upoważnia Weryfikatora do weryfikacji zgodności zdigitalizowanych danych osobowych (m.in. numery PESEL, imiona i nazwiska, daty urodzenia, ilość oddanej krwi, stopnie przyznanych odznak) z zeskanowanymi kartami Zasłużonych Honorowych Dawców Krwi. <br>
            2. Zadadniem Weryfikatora jest wyłącznie potwierdzenie zgodności zdigitalizowanych danych osobowych z zeskanowanymi kartami Zasłużonych Honorowych Dawców Krwi dostarczonymi przez Administratora Danych. <br>
            3. Weryfikator nie nabywa żadnych praw do przechowywania, kopiowania lub wykorzystywania tych danych w celach innych niż wskazane powyżej.
          </div>
          
          <h3 class="subsection-title">Obowiązki Weryfikatora</h3>
          <div class="agreement-text">
            Weryfikator zobowiązuje się do: <br>
            1. Wykorzystywania udostępnionych danych osobowych wyłącznie w procesie weryfikacji zgodnie z instrukcjami Administratora Danych. <br>
            2. Zachowania danych w ścisłej poufności i nieujawniania ich osobom trzecim. <br>
            3. Nie kopiowania, zapisywania, przechowywania, ani wykorzystywania danych w żadnej formie poza zatwierdzonym procesem weryfikacji. <br>
            4. Zwrócenia lub usunięcia wszystkich danych po zakończeniu weryfikacji, zgodnie z instrukcjami Administratora Danych.
          </div>
          
          <h3 class="subsection-title">Zasady RODO</h3>
          <div class="agreement-text">
            Weryfikator przyjmuje do wiadomości zasady <a href="https://uodo.gov.pl/pl/404" target="_blank" rel="noopener noreferrer" class="rodo-link">RODO</a>, w tym: <br>
            1. Dane osobowe udostępnione przez Administratora Danych są poufne i nie mogą być ujawniane osobom trzecim, ani przekazywane do innych podmiotów, kopiowane, zapisywane, przechowywane, ani wykorzystywane poza zatwierdzonym procesem weryfikacji. <br>
            2. Przetwarzanie danych przez Weryfikatora musi być zgodne z prawem, w sposób rzetelny i przejrzysty. <br>
            3. Utrzymanie poufności i integralności danych osobowych.
          </div>
          
          <h3 class="subsection-title">Konsekwencje naruszenia</h3>
          <div class="agreement-text">
            Naruszenie warunków niniejszej umowy może skutkować: <br>
            1. Natychmiastowym zakończeniem współpracy w ramach procesu weryfikacji. <br>
            2. Podjęciem działań prawnych na podstawie obowiązujących przepisów dotyczących ochrony danych osobowych, w tym kar wynikających z RODO. <br>
            3. Żądaniem od Weryfikatora odszkodowania za szkody wynikające z naruszenia umowy.
          </div>
          
          <h3 class="subsection-title">Potwierdzenie</h3>
          <div class="agreement-text">
            Podpisując tę umowę, Weryfikator potwierdza zrozumienie i akceptację opisanych powyżej obowiązków i zobowiązań.
          </div>
        </div>
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

.agreement-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 0.5px;
  margin-bottom: 2rem;
}

.agreement-content {
  line-height: 1.6;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #0d6efd;
  margin-bottom: 1.5rem;
  margin-top: 2rem;
}

.subsection-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
  margin-top: 1.5rem;
}

.agreement-text {
  font-size: 1.1rem;
  font-weight: 400;
  color: #2c3e50;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  text-align: justify;
}

.highlight-text {
  color: #0d6efd;
  font-weight: 600;
  background-color: rgba(13, 110, 253, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
}

.rodo-link {
  color: #0d6efd;
  font-weight: 600;
  text-decoration: underline;
  text-decoration-thickness: 2px;
  text-underline-offset: 2px;
}

.rodo-link:hover {
  color: #0056b3;
  text-decoration-color: #0056b3;
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
  }

  .agreement-title {
    font-size: 1.8rem;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .subsection-title {
    font-size: 1.1rem;
  }

  .agreement-text {
    font-size: 1rem;
  }
}

@media(max-width: 768px) {
  div.card {
    margin-bottom: 0 !important;
  }

  div.card-body {
    height: 60vh !important;
  }

  .agreement-title {
    font-size: 1.6rem;
    margin-bottom: 1.5rem;
  }

  .section-title {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
  }

  .subsection-title {
    font-size: 1rem;
    margin-bottom: 0.8rem;
    margin-top: 1.2rem;
  }

  .agreement-text {
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.2rem;
  }

  button.btn.btn-lg {
    font-size: 1.1rem !important;
    width: 100% !important;
    padding: 0.75rem 1rem;
    font-weight: 600;
  }
}

@media (max-height: 700px) and (max-width: 768px) {
  div.card-body {
    height: 50vh !important;
  }

  .agreement-title {
    font-size: 1.4rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .subsection-title {
    font-size: 0.9rem;
  }

  .agreement-text {
    font-size: 0.9rem;
  }
}
</style>
