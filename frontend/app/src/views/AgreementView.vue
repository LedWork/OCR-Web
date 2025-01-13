<script>
import {adminCheckSession, changeOrientation, checkSession} from "@/scripts/utils.js";
import {getCSRFToken} from "@/scripts/utils.js";
export default {
  data() {
    return {
      loading: true,
      admin: false
    }
  },
  async mounted() {
    try {
      this.loading = await checkSession(this.$router);
      // commenting this out temporarily to avoid errors
      // this.admin = await adminCheckSession();

      // Check if the user has already agreed to the contract
      const response = await fetch("/api/agreement/contract", { method: "GET" });

      if (response.ok) {
        const data = await response.json();
        if (data.message === "You have already agreed to the contract.") {
          // Redirect to the instruction page
          this.$router.push({ name: "instruction" });
          return;
        }
      }

      window.addEventListener("resize", changeOrientation);
    } catch (error) {
      console.error("An error occurred while checking agreement status:", error);
      alert("An error occurred. Please reload the page or try again later.");
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', changeOrientation)
  },
  methods: {
    async submitAgreement() {
      try {
        const response = await fetch("/api/agreement/contract", {
          method: "POST",
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
          body: JSON.stringify({ agree: "on" }) // Send 'agree' as JSON
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data.message); // Optional: Log the success message
          this.$router.push({ name: "instruction" }); // Navigate to instruction page
        } else {
          const errorData = await response.json();
          console.error(errorData.error); // Log the error message
          alert(errorData.error); // Show an alert with the error
        }
      } catch (error) {
        console.error("An error occurred while submitting the agreement:", error);
        alert("An error occurred. Please try again.");
      }
    }
  }
}
</script>
<template>
  <div class="wrapper vertical" v-if="!loading">
    <div v-if="admin" class="button" @click="goToAdmin">ADMIN PANEL</div>
    <div class="text-block">
      <p class="title">Contract Agreement</p>
      <p class="content">
        # Umowa o Zachowaniu Poufności w Procesie Ręcznej Weryfikacji Zdigitalizowanych Honorowych Kart Krwiodawców

        ## Sekcja 1: Identyfikacja Stron
        - **Administrator Danych**: Polski Czerwony Krzyż z siedzibą w Warszawie (00-561) przy ul. Mokotowskiej 14, iod@pck.pl
        - **Weryfikator**: [Imię i nazwisko, adres, dane kontaktowe]  

        ---

        ## Sekcja 2: Zakres i Cel
        Weryfikator przyjmuje do wiadomości, że:
        1. Jego zadaniem jest wyłącznie potwierdzenie zgodności zdigitalizowanych danych (numery PESEL, imiona i nazwiska, daty urodzenia, ilość oddanej krwi) z zeskanowanymi honorowymi kartami krwiodawców dostarczonymi przez Administratora Danych.
        2. Weryfikator nie nabywa żadnych praw do przechowywania, kopiowania lub wykorzystywania tych danych w celach innych niż wskazane powyżej.

        ---

        ## Sekcja 3: Obowiązki
        Weryfikator zobowiązuje się do:
        1. Wykorzystywania udostępnionych danych osobowych wyłącznie w procesie weryfikacji zgodnie z instrukcjami Administratora Danych.
        2. Zachowania danych w ścisłej poufności i nieujawniania ich osobom trzecim.
        3. Nie kopiowania, zapisywania ani przechowywania danych w żadnej formie poza zatwierdzonym procesem weryfikacji.
        4. Zwrócenia lub usunięcia wszystkich danych po zakończeniu weryfikacji, zgodnie z instrukcjami Administratora Danych.

        ---

        ## Sekcja 4: Zasady RODO
        Weryfikator przyjmuje do wiadomości zasady RODO, w tym:
        1. Przetwarzanie danych zgodnie z prawem, w sposób rzetelny i przejrzysty (**Art. 5 RODO**).
        2. Utrzymanie poufności i integralności danych osobowych (**Art. 32 RODO**).

        ---

        ## Sekcja 5: Konsekwencje Naruszenia
        Naruszenie warunków niniejszej umowy może skutkować:
        1. Natychmiastowym zakończeniem współpracy w ramach procesu weryfikacji.
        2. Podjęciem działań prawnych na podstawie obowiązujących przepisów dotyczących ochrony danych osobowych, w tym kar wynikających z RODO.

        ---

        ## Sekcja 6: Potwierdzenie
        Podpisując tę umowę, Weryfikator potwierdza zrozumienie i akceptację opisanych powyżej obowiązków i zobowiązań.
      </p>
    </div>
    <div class="button" @click="submitAgreement">I AGREE</div>
  </div>
</template>
<style></style>
