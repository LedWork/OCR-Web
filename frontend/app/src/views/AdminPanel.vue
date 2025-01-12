<script>
import axios from "axios";
import {adminCheckSession, changeOrientation, getCSRFToken, logout} from "@/scripts/utils.js";
import "@/assets/admin.css"

export default {
  data() {
    return {
      uploadedJson: null,
      uploadedImages: [],
      jsonFileName: "",
      imageFileNames: [],
      admin: false,
      login: null,
      password: null,
    };
  },
  methods: {
    logout,
    handleJSONUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.jsonFileName = file.name;
        if (file.type === "application/json") {
          this.uploadedFile = file;
        }
        else {
          alert("Please upload JSON file.");
        }
      }
    },
    async uploadJSON() {
      if (!this.uploadedFile) {
        alert("Please upload a valid JSON file.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.uploadedFile);
      try {
        const reader = new FileReader();
        reader.onload = async () => {
          try {
            const fileContent = reader.result;
            const data = JSON.parse(fileContent);

            const response = await axios.post(
              "/api/admin/upload-data",
              data,
              {
                headers: {
                  "Content-Type": "application/json",
                  'X-CSRF-TOKEN': getCSRFToken(),
                }
              }
            );
            console.log(response);
            alert("Upload successful.", response.data);
        } catch (error) {
          alert("Error during file processing or upload: ", error);
        }
      };
      reader.readAsText(this.uploadedFile);
    } catch (error) {
      console.error("Error: ", error);
    }
  },
    handleImageUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.imageFileNames = Array.from(files).map((file) => file.name);
        this.uploadedImages = Array.from(files);
      }
      else {
        alert("Please upload valid image files");
      }
    },
    async uploadImages() {
      if (this.uploadedImages.length === 0) {
        alert("Please upload at least one image file.");
        return;
      }

      const formData = new FormData();
      this.uploadedImages.forEach((image) => {
        formData.append("files", image);
      });

      try {
        const response = await axios.post(
          "/api/admin/upload-images",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          }
        );
        alert("Upload successful.", response.data);
      } catch (error) {
        console.error(error);
      }
    },
    goToInstruction() {
      this.$router.push({name: "instruction"});
    },
    goToAgreement() {
      this.$router.push({name: "agreement"});
    },
    goToCardsPanel() {
      this.$router.push({name: "cards"});
    },
    async addUser() {
      try {
        const response = await axios.post(
          '/api/admin/add-user',
          {
            login: this.login,
          },
          {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          },
        )
        console.log(response)
        this.password = response.data.password;
      }
      catch (error) {
        console.error(error);
      }

    }
  },
  async mounted(){
    this.admin = await adminCheckSession(this.$router);
    changeOrientation();
    window.addEventListener("resize", changeOrientation);
  },
  beforeunload() {
    window.removeEventListener("resize", changeOrientation);
  }
}
</script>
<template>
  <div class="wrapper">
    <div class="container" v-if="admin">
      <div class="button-container">
        <button @click="goToInstruction" class="admin-button">Wróć</button>
        <button @click="goToCardsPanel" class="admin-button">Panel kart</button>
        <button @click="logout" class="admin-button logout-btn">Wyloguj</button>
      </div>

      <div class="uploads">
        <div class="upload-container">
          <h1>
            Plik JSON
          </h1>
          <form @submit.prevent="uploadJSON" class="upload-form">
            <label for="jsonUpload" class="admin-button upload-label">Wybierz plik JSON</label>
            <input
              id="jsonUpload"
              type="file"
              accept=".json"
              @change="handleJSONUpload"
              class="file-input"
            />
            <p v-if="jsonFileName">Selected file: {{ jsonFileName }}</p>
            <button type="submit" class="admin-button upload-btn">Wyślij</button>
          </form>
        </div>

        <div class="upload-container">
          <h1>
            Zdjęcia
          </h1>
          <form @submit.prevent="uploadImages" class="upload-form">
            <label for="imageUpload" class="admin-button upload-label">Wybierz zdjęcia</label>
            <input
              id="imageUpload"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              multiple
              class="file-input"
            />
            <div v-if="imageFileNames.length > 0" class="images-names">
              <ul>
                <li v-for="(file, index) in imageFileNames" :key="index">{{ file }}</li>
              </ul>
            </div>
            <button type="submit" class="admin-button upload-btn">Wyślij</button>
          </form>
        </div>
      </div>

      <div class="upload-container">
        <h1>Dodawanie użytkownika</h1>

        <form @submit.prevent="addUser" class="upload-form">
          <input
            id="userUpload"
            type="text"
            class="text-input"
            placeholder="Login"
            v-model="login"
          >
          <button type="submit" class="admin-button upload-btn">Dodaj</button>
        </form>

        <h3 v-if="password">
          Hasło: {{ password }}
        </h3>
      </div>

    </div>
  </div>
</template>
