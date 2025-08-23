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
      // Upload progress tracking
      uploadProgress: 0,
      isUploading: false,
      uploadStatus: "",
      currentChunk: 0,
      totalChunks: 0,
      uploadStartTime: null,
      estimatedTimeRemaining: null,
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
        // Validate file types and sizes
        const validFiles = [];
        const invalidFiles = [];
        
        for (const file of files) {
          // Check file type
          if (!file.type.startsWith('image/')) {
            invalidFiles.push(`${file.name} (not an image)`);
            continue;
          }
          
          // Check individual file size (max 5MB per file)
          if (file.size > 5 * 1024 * 1024) {
            invalidFiles.push(`${file.name} (too large: ${(file.size / 1024 / 1024).toFixed(2)}MB)`);
            continue;
          }
          
          validFiles.push(file);
        }
        
        if (invalidFiles.length > 0) {
          alert(`Some files were rejected:\n${invalidFiles.join('\n')}`);
        }
        
        if (validFiles.length > 0) {
          this.imageFileNames = validFiles.map((file) => file.name);
          this.uploadedImages = validFiles;
          
          // Show total size info
          const totalSize = validFiles.reduce((sum, file) => sum + file.size, 0);
          console.log(`Selected ${validFiles.length} images, total size: ${(totalSize / 1024 / 1024).toFixed(2)}MB`);
        } else {
          alert("No valid image files selected");
          event.target.value = '';
        }
      } else {
        alert("Please upload valid image files");
      }
    },
    async uploadImages() {
      if (this.uploadedImages.length === 0) {
        alert("Please upload at least one image file.");
        return;
      }

      // Calculate total size and determine if chunking is needed
      const totalSize = this.uploadedImages.reduce((sum, image) => sum + image.size, 0);
      const maxChunkSize = 8 * 1024 * 1024; // 8MB per chunk (staying under 10MB limit)
      
      if (totalSize <= maxChunkSize) {
        // Small upload - use original method
        await this.uploadImagesSingleBatch();
      } else {
        // Large upload - show summary and confirm
        const totalSizeMB = (totalSize / 1024 / 1024).toFixed(2);
        const estimatedChunks = Math.ceil(totalSize / maxChunkSize);
        
        const confirmMessage = `Large upload detected:\n` +
          `• Total size: ${totalSizeMB}MB\n` +
          `• Estimated chunks: ${estimatedChunks}\n` +
          `• This will be automatically split into smaller uploads\n\n` +
          `Do you want to continue?`;
        
        if (confirm(confirmMessage)) {
          await this.uploadImagesChunked(maxChunkSize);
        }
      }
    },

    async uploadImagesSingleBatch() {
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
        alert("Upload failed: " + (error.response?.data?.error || error.message));
      }
    },

    async uploadImagesChunked(maxChunkSize) {
      this.isUploading = true;
      this.uploadProgress = 0;
      this.uploadStatus = "Preparing upload...";
      this.uploadStartTime = Date.now();
      
      try {
        // Group images into chunks
        const chunks = this.createImageChunks(maxChunkSize);
        this.totalChunks = chunks.length;
        this.currentChunk = 0;
        
        this.uploadStatus = `Uploading ${chunks.length} chunks...`;
        
        for (let i = 0; i < chunks.length; i++) {
          this.currentChunk = i + 1;
          this.uploadStatus = `Uploading chunk ${i + 1} of ${chunks.length}...`;
          
          const chunk = chunks[i];
          const formData = new FormData();
          
          // Add chunk metadata
          formData.append("chunk_index", i.toString());
          formData.append("total_chunks", chunks.length.toString());
          formData.append("is_chunked", "true");
          
          // Add files for this chunk
          chunk.forEach((image) => {
            formData.append("files", image);
          });

          // Retry logic for failed chunks
          let retryCount = 0;
          const maxRetries = 3;
          let chunkUploaded = false;
          
          while (!chunkUploaded && retryCount < maxRetries) {
            try {
              if (retryCount > 0) {
                this.uploadStatus = `Retrying chunk ${i + 1} (attempt ${retryCount + 1}/${maxRetries})...`;
              }
              
              const response = await axios.post(
                "/api/admin/upload-images-chunked",
                formData,
                {
                  headers: {
                    "Content-Type": "multipart/form-data",
                    'X-CSRF-TOKEN': getCSRFToken(),
                  },
                  timeout: 60000, // 60 second timeout for large chunks
                }
              );
              
              // Update progress
              this.uploadProgress = ((i + 1) / chunks.length) * 100;
              
              // Calculate estimated time remaining
              this.calculateEstimatedTime(i + 1, chunks.length);
              
              console.log(`Chunk ${i + 1} uploaded successfully:`, response.data);
              chunkUploaded = true;
              
            } catch (error) {
              retryCount++;
              console.error(`Error uploading chunk ${i + 1} (attempt ${retryCount}):`, error);
              
              if (retryCount >= maxRetries) {
                throw new Error(`Failed to upload chunk ${i + 1} after ${maxRetries} attempts: ${error.response?.data?.error || error.message}`);
              }
              
              // Wait before retry (exponential backoff)
              await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
            }
          }
        }
        
        this.uploadStatus = "Upload completed successfully!";
        alert("All images uploaded successfully!");
        
      } catch (error) {
        this.uploadStatus = "Upload failed: " + error.message;
        alert("Upload failed: " + error.message);
      } finally {
        this.isUploading = false;
        this.uploadProgress = 0;
        this.currentChunk = 0;
        this.totalChunks = 0;
        this.uploadStartTime = null;
        this.estimatedTimeRemaining = null;
      }
    },

    calculateEstimatedTime(completedChunks, totalChunks) {
      if (completedChunks <= 1 || !this.uploadStartTime) return;
      
      const elapsed = Date.now() - this.uploadStartTime;
      const avgTimePerChunk = elapsed / completedChunks;
      const remainingChunks = totalChunks - completedChunks;
      const estimatedRemaining = avgTimePerChunk * remainingChunks;
      
      if (estimatedRemaining > 0) {
        const minutes = Math.floor(estimatedRemaining / 60000);
        const seconds = Math.floor((estimatedRemaining % 60000) / 1000);
        
        if (minutes > 0) {
          this.estimatedTimeRemaining = `${minutes}m ${seconds}s remaining`;
        } else {
          this.estimatedTimeRemaining = `${seconds}s remaining`;
        }
      }
    },

    createImageChunks(maxChunkSize) {
      const chunks = [];
      let currentChunk = [];
      let currentChunkSize = 0;
      
      for (const image of this.uploadedImages) {
        if (currentChunkSize + image.size > maxChunkSize && currentChunk.length > 0) {
          // Current chunk is full, start a new one
          chunks.push(currentChunk);
          currentChunk = [image];
          currentChunkSize = image.size;
        } else {
          // Add to current chunk
          currentChunk.push(image);
          currentChunkSize += image.size;
        }
      }
      
      // Add the last chunk if it has files
      if (currentChunk.length > 0) {
        chunks.push(currentChunk);
      }
      
      return chunks;
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
            <i class="bi bi-table"></i> Panel kart
          </button>
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
            
            <!-- Upload Progress Section -->
            <div v-if="isUploading" class="mt-3">
              <div class="progress mb-2" style="height: 25px;">
                <div 
                  class="progress-bar progress-bar-striped progress-bar-animated" 
                  role="progressbar" 
                  :style="{ width: uploadProgress + '%' }"
                  :aria-valuenow="uploadProgress" 
                  aria-valuemin="0" 
                  aria-valuemax="100"
                >
                  {{ Math.round(uploadProgress) }}%
                </div>
              </div>
              <div class="text-center">
                <small class="text-muted">{{ uploadStatus }}</small>
                <div v-if="totalChunks > 1" class="mt-1">
                  <small class="text-muted">Chunk {{ currentChunk }} of {{ totalChunks }}</small>
                </div>
                <div v-if="estimatedTimeRemaining" class="mt-1">
                  <small class="text-info">{{ estimatedTimeRemaining }}</small>
                </div>
              </div>
            </div>
            
            <div class="d-flex mt-3 justify-content-center align-items-center">
              <button 
                type="submit" 
                class="btn btn-success btn-lg w-100 w-md-25"
                :disabled="isUploading"
              >
                <span v-if="isUploading">Uploading...</span>
                <span v-else>Wyślij</span>
              </button>
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
