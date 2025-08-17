<script>
import axios from "axios";
import {adminCheckSession, getCSRFToken, logout} from "@/scripts/utils.js";

export default {
  data() {
    return {
      uploadedJson: null,
      uploadedImages: [],
      jsonFileName: "",
      imageFileNames: [],
      admin: false,
      mail: null,
      users: [],
      loadingUsers: false,
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
    goToCardsPanel() {
      this.$router.push({name: "cards"});
    },
    async addUser() {
      try {
        const response = await axios.post(
            '/api/admin/add-user',
            {
              login: this.mail,
            },
            {
              headers: {
                'X-CSRF-TOKEN': getCSRFToken(),
              },
            },
          )
          alert(response.data.message);
          this.mail = ""; // Clear the input
          await this.fetchUsers(); // Refresh the user list
      }
      catch (error) {
        console.error(error);
        alert("Error adding user: " + (error.response?.data?.message || error.message));
      }
    },
    async fetchUsers() {
      this.loadingUsers = true;
      try {
        const response = await axios.get('/api/admin/users', {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        });
        this.users = response.data.users;
      } catch (error) {
        console.error('Error fetching users:', error);
        alert("Error fetching users: " + (error.response?.data?.error || error.message));
      } finally {
        this.loadingUsers = false;
      }
    },

    async revokeUser(login) {
      if (!confirm(`Are you sure you want to revoke user ${login}?`)) {
        return;
      }
      
      try {
        const response = await axios.post(`/api/admin/users/${login}/revoke`, {}, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        });
        alert(response.data.message);
        await this.fetchUsers(); // Refresh the user list
      } catch (error) {
        console.error('Error revoking user:', error);
        alert("Error revoking user: " + (error.response?.data?.error || error.message));
      }
    },
    async unrevokeUser(login) {
      if (!confirm(`Are you sure you want to unrevoke user ${login}?`)) {
        return;
      }
      
      try {
        const response = await axios.post(`/api/admin/users/${login}/unrevoke`, {}, {
          headers: {
            'X-CSRF-TOKEN': getCSRFToken(),
          },
        });
        alert(response.data.message);
        await this.fetchUsers(); // Refresh the user list
      } catch (error) {
        console.error('Error unrevoking user:', error);
        alert("Error unrevoking user: " + (error.response?.data?.error || error.message));
      }
    },
  },
  async mounted(){
    this.admin = await adminCheckSession(this.$router);
    await this.fetchUsers(); // Fetch users on mount
  }
}
</script>
<template>
  <div class="d-flex flex-column justify-content-center align-items-center">
    <div class="card border-light-subtle p-3 mt-5 w-75 h-75" v-if="admin">
      <div class="row mx-3 mb-3">
        <div class="col-12 col-md-auto mb-2 mb-md-0">
          <button @click="goToInstruction" class="btn btn-danger btn-lg w-100">Wróć</button>
        </div>
        <div class="col-12 col-md mb-2 mb-md-0 d-flex justify-content-center gap-2">
          <button @click="goToCardsPanel"
                  class="btn btn-info text-white btn-lg"
                  style="width: auto; max-width: 300px;">
            Panel kart</button>
        </div>
        <div class="col-12 col-md-auto">
          <button @click="logout" class="btn btn-danger btn-lg w-100">Wyloguj</button>
        </div>
      </div>

      <div class="d-flex flex-column flex-md-row mt-5 mb-5 mx-4 gap-3">
        <div class="col-12 col-md-6">
          <h1 class="text-center mb-2">Plik JSON</h1>
          <form @submit.prevent="uploadJSON">
            <label for="jsonUpload" class="text-center">Wybierz plik JSON</label>
            <input
              id="jsonUpload"
              type="file"
              accept=".json"
              @change="handleJSONUpload"
              class="form-control"
            />
            <p v-if="jsonFileName">Selected file: {{ jsonFileName }}</p>
            <div class="d-flex mt-3 justify-content-center align-items-center">
              <button type="submit" class="btn btn-success btn-lg w-100 w-md-25">Wyślij</button>
            </div>
          </form>
        </div>

        <div class="col-12 col-md-6">
          <h1 class="text-center mb-2">Zdjęcia</h1>
          <form @submit.prevent="uploadImages">
            <label for="imageUpload" class="text-center">Wybierz zdjęcia</label>
            <input
              id="imageUpload"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              multiple
              class="form-control"
            />
            <div v-if="imageFileNames.length > 0" class="bg-secondary rounded mt-3 text-white p-2" style="max-height: 100px; overflow-y: auto;">
              <ul class="mb-0">
                <li v-for="(file, index) in imageFileNames" :key="index">{{ file }}</li>
              </ul>
            </div>
            <div class="d-flex mt-3 justify-content-center align-items-center">
              <button type="submit" class="btn btn-success btn-lg w-100 w-md-25">Wyślij</button>
            </div>
          </form>
        </div>
      </div>

      <div class="d-flex justify-content-center align-items-center flex-column mt-3 mb-4">
        <h1 class="text-center">Dodawanie użytkownika</h1>

        <form @submit.prevent="addUser" class="row w-100 d-flex justify-content-center">
          <div class="d-flex flex-column flex-md-row col col-md-6 mx-auto gap-2">
            <input
              id="userUpload"
              type="text"
              class="form-control"
              placeholder="Email"
              v-model="mail"
            >
            <button type="submit" class="btn btn-success">Dodaj</button>
          </div>
        </form>
      </div>

      <div class="d-flex justify-content-center align-items-center flex-column mt-3 mb-4">
        <h1 class="text-center">Lista użytkowników</h1>
        
        <div class="w-100 d-flex justify-content-center">
          <div class="col-12 col-md-8">
            <div v-if="loadingUsers" class="text-center">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            
            <div v-else-if="users.length === 0" class="text-center">
              <p class="text-muted">Brak użytkowników</p>
            </div>
            
            <div v-else class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Email</th>
                    <th>Data utworzenia</th>
                    <th>Typ użytkownika</th>
                    <th>Status</th>
                    <th>Akcje</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.login">
                    <td>{{ user.login }}</td>
                    <td>{{ new Date(user.created_at).toLocaleString('pl-PL') }}</td>
                    <td>
                      <span v-if="user.is_super_user" class="badge bg-danger">Admin</span>
                      <span v-else class="badge bg-primary">Użytkownik</span>
                    </td>
                    <td>
                      <span v-if="user.is_revoked" class="badge bg-warning">Zablokowany</span>
                      <span v-else class="badge bg-success">Aktywny</span>
                    </td>
                    <td>
                      <button 
                        v-if="!user.is_revoked"
                        @click="revokeUser(user.login)" 
                        class="btn btn-warning btn-sm me-1"
                        :disabled="user.is_super_user"
                        :title="user.is_super_user ? 'Nie można zablokować administratora' : 'Zablokuj użytkownika'"
                      >
                        Zablokuj
                      </button>
                      <button 
                        v-else
                        @click="unrevokeUser(user.login)" 
                        class="btn btn-success btn-sm me-1"
                        :disabled="user.is_super_user"
                        :title="user.is_super_user ? 'Nie można odblokować administratora' : 'Odblokuj użytkownika'"
                      >
                        Odblokuj
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
