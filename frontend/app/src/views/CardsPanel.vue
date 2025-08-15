<script>
import axios from "axios";
import {adminCheckSession, getCSRFToken} from "@/scripts/utils.js";
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';

export default {
  components: {
    Vue3EasyDataTable,
  },
  data() {
    return {
      admin: false,
      cards: [],
      loading: false,
      search: '',
      selectedItems: [],
      tableHeaders: [
        { text: 'Image Code', value: 'image_code', sortable: true },
        { text: 'Check Status', value: 'check_status', sortable: true },
        { text: 'Is Green', value: 'is_green', sortable: true },
        { text: 'Current Checks', value: 'current_checks', sortable: true },
        { text: 'Expected Checks', value: 'expected_checks', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      itemsPerPage: 10,
      itemsPerPageOptions: [5, 10, 25, 50, 100],
    }
  },
  computed: {
    filteredCards() {
      console.log('Computing filteredCards, cards:', this.cards);
      const filtered = (this.cards || []).filter(card => {
        console.log('Checking card:', card);
        return card && card.image_code;
      });
      console.log('Filtered result:', filtered);
      
      // Transform data to ensure Vue3EasyDataTable compatibility
      const transformed = filtered.map(card => ({
        ...card,
        // Ensure all required fields are present
        image_code: card.image_code || '',
        check_status: card.check_status || '',
        is_green: Boolean(card.is_green),
        current_checks: card.current_checks || 0,
        expected_checks: card.expected_checks || 0
      }));
      
      console.log('Transformed cards:', transformed);
      return transformed;
    },
    selectedCount() {
      return this.selectedItems.length;
    },
  },
  methods: {
    goToAdminPanel() {
      this.$router.push({name: "admin"});
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
    async fetchCards() {
      this.loading = true;
      try {
        const response = await axios.get('/api/admin/cards')
        console.log('Raw response:', response);
        console.log('Response data:', response.data);
        console.log('Response data type:', typeof response.data);
        console.log('Response data length:', Array.isArray(response.data) ? response.data.length : 'Not an array');
        this.cards = response.data;
        console.log('Fetched cards:', this.cards);
        console.log('Cards length:', this.cards.length);
        if (this.cards.length > 0) {
          console.log('First card:', this.cards[0]);
          console.log('First card keys:', Object.keys(this.cards[0]));
        }
      }
      catch (error) {
        console.error('Error fetching cards:', error);
        alert('Error fetching cards data');
      } finally {
        this.loading = false;
      }
    },
    viewImage(imageCode) {
      this.$router.push(`/card/${imageCode}`);
    },
    async deleteImage(imageCode) {
      if (!confirm('Are you sure you want to delete this card?')) {
        return;
      }
      
      try {
        const response = await axios.delete(
          '/api/admin/card/' + imageCode,
          {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          });
        if (response.status === 200) {
          alert(`Successfully deleted card: ${imageCode}`);
          await this.fetchCards();
        }
      } catch (error) {
        console.error(error);
        alert('Error deleting card');
      }
    },
    async deleteSelected() {
      if (this.selectedItems.length === 0) {
        alert('Please select items to delete');
        return;
      }
      
      if (!confirm(`Are you sure you want to delete ${this.selectedItems.length} selected cards?`)) {
        return;
      }
      
      try {
        const deletePromises = this.selectedItems.map(item => 
          axios.delete(`/api/admin/card/${item.image_code}`, {
            headers: {
              'X-CSRF-TOKEN': getCSRFToken(),
            },
          })
        );
        
        await Promise.all(deletePromises);
        alert(`Successfully deleted ${this.selectedItems.length} cards`);
        this.selectedItems = [];
        await this.fetchCards();
      } catch (error) {
        console.error(error);
        alert('Error deleting selected cards');
      }
    },
    onSelectionChange(items) {
      this.selectedItems = items;
    },
    clearSelection() {
      this.selectedItems = [];
    },
    exportToCSV() {
      if (this.cards.length === 0) {
        alert('No data to export');
        return;
      }
      
      const headers = ['Image Code', 'Check Status', 'Is Green', 'Current Checks', 'Expected Checks'];
      const csvContent = [
        headers.join(','),
        ...this.cards.map(card => [
          card.image_code,
          card.check_status,
          card.is_green ? 'Yes' : 'No',
          card.current_checks,
          card.expected_checks
        ].join(','))
      ].join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cards_export_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    },
  },
  async mounted(){
    this.admin = await adminCheckSession(this.$router);
    await this.fetchCards();
  },
}
</script>

<template>
  <div class="container-fluid mt-4" v-if="admin">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2 class="mb-0">Cards Management</h2>
            <p class="text-muted mb-0">Manage and view all cards in the system</p>
          </div>
          <div class="d-flex gap-2">
            <button @click="goToAdminPanel" class="btn btn-secondary">
              <i class="bi bi-arrow-left"></i> Back to Admin
            </button>
            <button @click="logout" class="btn btn-danger">
              <i class="bi bi-box-arrow-right"></i> Logout
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Total Cards</h5>
            <h3 class="mb-0">{{ cards.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Green Cards</h5>
            <h3 class="mb-0">{{ cards.filter(c => c && c.is_green).length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5 class="card-title">Selected</h5>
            <h3 class="mb-0">{{ selectedCount }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Filtered</h5>
            <h3 class="mb-0">{{ filteredCards.length }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="row mb-3">
      <div class="col-md-6">
        <div class="input-group">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search by image code or status..."
            v-model="search"
          >
        </div>
      </div>
      <div class="col-md-6">
        <div class="d-flex gap-2 justify-content-end">
          <button 
            @click="clearSelection" 
            class="btn btn-outline-secondary"
            :disabled="selectedCount === 0"
          >
            <i class="bi bi-x-circle"></i> Clear Selection
          </button>
          <button 
            @click="deleteSelected" 
            class="btn btn-danger"
            :disabled="selectedCount === 0"
          >
            <i class="bi bi-trash"></i> Delete Selected ({{ selectedCount }})
          </button>
          <button @click="exportToCSV" class="btn btn-success">
            <i class="bi bi-download"></i> Export CSV
          </button>
          <button @click="fetchCards" class="btn btn-primary" :disabled="loading">
            <i class="bi bi-arrow-clockwise" :class="{ 'spinner-border spinner-border-sm': loading }"></i> 
            {{ loading ? 'Loading...' : 'Refresh' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Debug Info -->
    <div class="row mb-3" v-if="cards.length > 0">
      <div class="col-12">
        <div class="card bg-light">
          <div class="card-body">
            <h6>Debug Info:</h6>
            <p>Total cards: {{ cards.length }}</p>
            <p>Filtered cards: {{ filteredCards.length }}</p>
            <p>Search value: "{{ search }}"</p>
            <p>First card: {{ JSON.stringify(cards[0]) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Fallback Table (if Vue3EasyDataTable doesn't work) -->
    <div class="row mb-3" v-if="filteredCards.length > 0">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h6>Cards Data (Fallback View)</h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Image Code</th>
                    <th>Check Status</th>
                    <th>Is Green</th>
                    <th>Current Checks</th>
                    <th>Expected Checks</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="card in filteredCards" :key="card.image_code">
                    <td>{{ card.image_code }}</td>
                    <td>
                      <span :class="card.is_green ? 'badge bg-success' : 'badge bg-secondary'">
                        {{ card.check_status }}
                      </span>
                    </td>
                    <td>
                      <i :class="card.is_green ? 'bi bi-check-circle-fill text-success' : 'bi bi-x-circle-fill text-muted'"></i>
                    </td>
                    <td><span class="badge bg-primary">{{ card.current_checks }}</span></td>
                    <td><span class="badge bg-secondary">{{ card.expected_checks }}</span></td>
                    <td>
                      <div class="d-flex gap-1">
                        <button class="btn btn-sm btn-info text-white" @click="viewImage(card.image_code)" title="View Card">
                          <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" @click="deleteImage(card.image_code)" title="Delete Card">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h6>Vue3EasyDataTable (Main Table)</h6>
          </div>
          <div class="card-body p-0">
            <!-- Minimal Vue3EasyDataTable for testing -->
            <Vue3EasyDataTable
              :headers="tableHeaders"
              :items="filteredCards"
              :loading="loading"
              table-class-name="customize-table"
              :show-index="true"
              theme-color="#007bff"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.customize-table {
  --easy-table-border: 1px solid #dee2e6;
  --easy-table-row-border: 1px solid #dee2e6;
  --easy-table-header-font-size: 14px;
  --easy-table-header-font-color: #495057;
  --easy-table-header-background-color: #f8f9fa;
  --easy-table-body-row-font-size: 14px;
  --easy-table-body-row-font-color: #495057;
  --easy-table-body-row-background-color: #ffffff;
  --easy-table-body-row-hover-background-color: #f8f9fa;
  --easy-table-body-row-hover-font-color: #495057;
  --easy-table-body-row-selected-background-color: #e3f2fd;
  --easy-table-body-row-selected-font-color: #495057;
  --easy-table-footer-font-size: 14px;
  --easy-table-footer-font-color: #495057;
  --easy-table-footer-background-color: #f8f9fa;
  --easy-table-footer-border: 1px solid #dee2e6;
  --easy-table-rows-per-page-selector-width: 70px;
  --easy-table-rows-per-page-selector-option-padding: 10px;
  --easy-table-rows-per-page-selector-z-index: 1;
  --easy-table-scrollbar-track-color: #f1f1f1;
  --easy-table-scrollbar-color: #c1c1c1;
  --easy-table-scrollbar-thumb-color: #a8a8a8;
  --easy-table-scrollbar-corner-color: #f1f1f1;
  --easy-table-loading-mask-background-color: rgba(255, 255, 255, 0.5);
  --easy-table-loading-mask-color: #495057;
  --easy-table-loading-mask-opacity: 0.5;
  --easy-table-loading-mask-z-index: 1;
  --easy-table-loading-mask-background-color: rgba(255, 255, 255, 0.5);
  --easy-table-loading-mask-color: #495057;
  --easy-table-loading-mask-opacity: 0.5;
  --easy-table-loading-mask-z-index: 1;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.bi {
  font-size: 1rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
