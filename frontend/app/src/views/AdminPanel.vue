<script>
import axios from "axios";
import {adminCheckSession, changeOrientation, getCSRFToken} from "@/scripts/utils.js";

export default {
  data() {
    return {
      uploadedJson: null,
      uploadedImages: [],
      admin: false,
      login: null,
      password: null,
    };
  },
  methods: {
    handleJSONUpload(event) {
      const file = event.target.files[0];
      if (file) {
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
    async logout() {
      const response = await axios.post(
        '/api/auth/break-session',
        {},
        {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        },
      )

      if (response.status === 200) {
        window.location.reload();
      }
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
        <button @click="goToInstruction" class="button">Back</button>
        <button @click="logout" class="button logout-btn">Logout</button>
      </div>

      <div class="uploads">
        <div class="upload-container">
          <h1>
            Uploading JSON data
          </h1>
          <form @submit.prevent="uploadJSON" class="upload-form">
            <label for="jsonUpload" class="button upload-label">Choose JSON file</label>
            <input
              id="jsonUpload"
              type="file"
              accept=".json"
              @change="handleJSONUpload"
              class="file-input"
            />
            <button type="submit" class="button upload-btn">Upload</button>
          </form>
        </div>

        <div class="upload-container">
          <h1>
            Uploading images
          </h1>
          <form @submit.prevent="uploadImages" class="upload-form">
            <label for="imageUpload" class="button upload-label">Choose images</label>
            <input
              id="imageUpload"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              multiple
              class="file-input"
            />
            <button type="submit" class="button upload-btn">Upload</button>
          </form>
        </div>
      </div>

      <div class="upload-container">
        <h1>Adding user</h1>

        <form @submit.prevent="addUser" class="upload-form">
          <input
            id="userUpload"
            type="text"
            class="text-input"
            placeholder="Login"
            v-model="login"
          >
          <button type="submit" class="button upload-btn">Upload</button>
        </form>

        <h3 v-if="password">
          Password: {{ password }}
        </h3>
      </div>

    </div>
  </div>
</template>

<style scoped>

.container {
  max-width: 90%;
  margin: 20px auto;
  padding: 50px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.uploads {
  display: flex;
  flex-wrap: wrap;
  gap: 50px;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.button:hover {
  background-color: #0056b3;
}

.logout-btn {
  background-color: #dc3545;
}

.logout-btn:hover {
  background-color: #c82333;
}

.upload-container {
  flex: 1 1 calc(50% - 50px);
  box-sizing: border-box;

  background-color: #f5f5f5;
  border-radius: 5px;
  margin-top: 20px;
  padding: 30px;
  text-align: center;
}

h1 {
  white-space: nowrap;
  font-size: 24px;
  font-weight: bold;
}

.upload-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.upload-label {
  cursor: pointer;
  font-size: 16px;
}

.file-input {
  display: none;
}

.text-input {
  margin-top: 20px;
}

.upload-btn {
  margin-top: 5px;
  background-color: #28a745;
}

.upload-btn:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .container {
    width: 60%;
    margin: 10px auto;
    padding: 20px;
  }

  .uploads {
    flex-direction: column;
  }

  h1 {
    font-size: 18px;
  }

  .upload-form {
    gap: 5px;
  }

  .button {
    font-size: 10px;
    padding: 6px 12px;
  }

  .upload-container {
    padding: 20px;
    flex: 1 1 100%;
  }

  .text-input {
    margin-top: 10px;
    font-size: 10px;
  }
}
</style>
