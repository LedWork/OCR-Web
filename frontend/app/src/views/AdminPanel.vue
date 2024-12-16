<script>
import axios from "axios";
export default {
  data() {
    return {
      uploadedJson: null,
      uploadedImages: [],
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
              "http://localhost:5000/admin/upload-data",
              data,
              {
                headers: {
                  "Content-Type": "application/json",
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
          "http://localhost:5000/admin/upload-images",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        alert("Upload successful.", response.data);
      } catch (error) {
      }
    },
  },
}
</script>
<template>
  <div class="container">
    <div class="logout-container">
      <button class="button logout-btn">Wyloguj</button>
    </div>

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
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.logout-container {
  text-align: right;
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
  background-color: #f5f5f5;
  border-radius: 5px;
  margin-top: 30px;
  padding: 30px;
  text-align: center;
}

h1 {
  font-size: 30px;
  font-weight: bold;
}

.upload-form {
  margin: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-label {
  cursor: pointer;
  font-size: 16px;
}

.file-input {
  display: none;
}

.upload-btn {
  margin: 5px;
  background-color: #28a745;
}

.upload-btn:hover {
  background-color: #218838;
}

</style>
