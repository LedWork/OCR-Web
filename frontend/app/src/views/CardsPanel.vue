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
      // Advanced filters
      filters: {
        checkStatus: '',
        isGreen: '',
        currentChecks: '',
        expectedChecks: '',
        dateRange: {
          start: '',
          end: ''
        }
      },
      // Sort configuration
      sortBy: 'image_code',
      sortDesc: false,
      tableHeaders: [
        { text: 'Image Code', value: 'image_code', sortable: true },
        { text: 'Check Status', value: 'check_status', sortable: true },
        { text: 'Is Green', value: 'is_green', sortable: true },
        { text: 'Current Checks', value: 'current_checks', sortable: true },
        { text: 'Expected Checks', value: 'expected_checks', sortable: true },
        { text: 'Created Date', value: 'created_at', sortable: true },
        { text: 'Updated Date', value: 'updated_at', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false, width: 150 },
      ],
      itemsPerPage: 10,
      itemsPerPageOptions: [5, 10, 25, 50, 100],
      // Filter options
      checkStatusOptions: ['pending', 'in_progress', 'completed', 'verified', 'rejected'],
      booleanOptions: [
        { text: 'All', value: '' },
        { text: 'Yes', value: 'true' },
        { text: 'No', value: 'false' }
      ],
      showAdvancedFilters: false,
    }
  },
  computed: {
    filteredCards() {
      let filtered = (this.cards || []).filter(card => {
        if (!card || !card.image_code) return false;
        
        // Apply search filter
        if (this.search) {
          const searchLower = this.search.toLowerCase();
          const imageCode = (card.image_code || '').toLowerCase();
          const checkStatus = (card.check_status || '').toLowerCase();
          const currentChecks = (card.current_checks || '').toString();
          const expectedChecks = (card.expected_checks || '').toString();
          
          return imageCode.includes(searchLower) || 
                 checkStatus.includes(searchLower) ||
                 currentChecks.includes(searchLower) ||
                 expectedChecks.includes(searchLower);
        }
        
        return true;
      });
      
      // Apply advanced filters
      if (this.filters.checkStatus) {
        filtered = filtered.filter(card => card.check_status === this.filters.checkStatus);
      }
      
      if (this.filters.isGreen !== '') {
        const isGreen = this.filters.isGreen === 'true';
        filtered = filtered.filter(card => card.is_green === isGreen);
      }
      
      if (this.filters.currentChecks) {
        const currentChecks = parseInt(this.filters.currentChecks);
        filtered = filtered.filter(card => parseInt(card.current_checks) === currentChecks);
      }
      
      if (this.filters.expectedChecks) {
        const expectedChecks = parseInt(this.filters.expectedChecks);
        filtered = filtered.filter(card => parseInt(card.expected_checks) === expectedChecks);
      }
      
      // Apply date range filter if dates are set
      if (this.filters.dateRange.start || this.filters.dateRange.end) {
        filtered = filtered.filter(card => {
          if (!card.created_at) return true;
          
          const cardDate = new Date(card.created_at);
          const startDate = this.filters.dateRange.start ? new Date(this.filters.dateRange.start) : null;
          const endDate = this.filters.dateRange.end ? new Date(this.filters.dateRange.end) : null;
          
          if (startDate && endDate) {
            return cardDate >= startDate && cardDate <= endDate;
          } else if (startDate) {
            return cardDate >= startDate;
          } else if (endDate) {
            return cardDate <= endDate;
          }
          
          return true;
        });
      }
      
      // Transform data to ensure Vue3EasyDataTable compatibility
      const transformed = filtered.map(card => {
        if (!card) return null;
        
        return {
          ...card,
          // Ensure all required fields are present with safe defaults
          image_code: card.image_code || '',
          check_status: card.check_status || '',
          is_green: card.is_green ? 'Yes' : 'No',
          current_checks: parseInt(card.current_checks) || 0,
          expected_checks: parseInt(card.expected_checks) || 0,
          created_at: card.created_at ? this.formatDate(card.created_at) : '',
          updated_at: card.updated_at ? this.formatDate(card.updated_at) : '',
        };
      }).filter(Boolean); // Remove any null items
      
      return transformed;
    },
    selectedCount() {
      return this.selectedItems.length;
    },
    // Get unique values for filter options
    uniqueCheckStatuses() {
      const statuses = [...new Set(this.cards.map(card => card.check_status).filter(Boolean))];
      return statuses.sort();
    },
    // Filter summary
    activeFiltersCount() {
      let count = 0;
      if (this.search) count++;
      if (this.filters.checkStatus) count++;
      if (this.filters.isGreen !== '') count++;
      if (this.filters.currentChecks) count++;
      if (this.filters.expectedChecks) count++;
      if (this.filters.dateRange.start || this.filters.dateRange.end) count++;
      return count;
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
        this.cards = response.data;
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
    clearSelection() {
      this.selectedItems = [];
    },
    // Clear all filters
    clearAllFilters() {
      this.search = '';
      this.filters = {
        checkStatus: '',
        isGreen: '',
        currentChecks: '',
        expectedChecks: '',
        dateRange: {
          start: '',
          end: ''
        }
      };
      this.sortBy = 'image_code';
      this.sortDesc = false;
    },
    // Toggle advanced filters
    toggleAdvancedFilters() {
      this.showAdvancedFilters = !this.showAdvancedFilters;
    },
    // Handle sorting
    handleSort(column, direction) {
      this.sortBy = column;
      this.sortDesc = direction === 'desc';
    },
    exportToCSV() {
      if (this.cards.length === 0) {
        alert('No data to export');
        return;
      }
      
      const headers = ['Image Code', 'Check Status', 'Is Green', 'Current Checks', 'Expected Checks', 'Created Date', 'Updated Date'];
      const csvContent = [
        headers.join(','),
        ...this.filteredCards.map(card => [
          card.image_code,
          card.check_status,
          card.is_green ? 'Yes' : 'No',
          card.current_checks,
          card.expected_checks,
          card.created_at,
          card.updated_at
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
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString; // Handle invalid dates
      return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    }
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
            placeholder="Search by image code, status, or numbers..."
            v-model="search"
          >
          <button 
            @click="toggleAdvancedFilters" 
            class="btn btn-outline-secondary"
            type="button"
          >
            <i class="bi bi-funnel"></i>
            Filters {{ activeFiltersCount > 0 ? `(${activeFiltersCount})` : '' }}
          </button>
        </div>
      </div>
      <div class="col-md-6">
        <div class="d-flex gap-2 justify-content-end">
          <button 
            @click="clearAllFilters" 
            class="btn btn-outline-warning"
            :disabled="activeFiltersCount === 0"
          >
            <i class="bi bi-x-circle"></i> Clear Filters
          </button>
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

    <!-- Advanced Filters -->
    <div v-if="showAdvancedFilters" class="row mb-3">
      <div class="col-12">
        <div class="card filters-card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="bi bi-funnel"></i> Advanced Filters
            </h6>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <!-- Check Status Filter -->
              <div class="col-md-3">
                <label class="form-label">Check Status</label>
                <select v-model="filters.checkStatus" class="form-select">
                  <option value="">All Statuses</option>
                  <option v-for="status in uniqueCheckStatuses" :key="status" :value="status">
                    {{ status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ') }}
                  </option>
                </select>
              </div>
              
              <!-- Is Green Filter -->
              <div class="col-md-3">
                <label class="form-label">Is Green</label>
                <select v-model="filters.isGreen" class="form-select">
                  <option v-for="option in booleanOptions" :key="option.value" :value="option.value">
                    {{ option.text }}
                  </option>
                </select>
              </div>
              
              <!-- Current Checks Filter -->
              <div class="col-md-3">
                <label class="form-label">Current Checks</label>
                <input 
                  type="number" 
                  v-model="filters.currentChecks" 
                  class="form-control" 
                  placeholder="Exact number"
                  min="0"
                >
              </div>
              
              <!-- Expected Checks Filter -->
              <div class="col-md-3">
                <label class="form-label">Expected Checks</label>
                <input 
                  type="number" 
                  v-model="filters.expectedChecks" 
                  class="form-control" 
                  placeholder="Exact number"
                  min="0"
                >
              </div>
              
              <!-- Date Range Filters -->
              <div class="col-md-6">
                <label class="form-label">Date Range</label>
                <div class="input-group">
                  <input 
                    type="date" 
                    v-model="filters.dateRange.start" 
                    class="form-control"
                    placeholder="Start date"
                  >
                  <span class="input-group-text">to</span>
                  <input 
                    type="date" 
                    v-model="filters.dateRange.end" 
                    class="form-control"
                    placeholder="End date"
                  >
                </div>
              </div>
              
              <!-- Filter Summary -->
              <div class="col-md-6 d-flex align-items-end">
                <div class="text-muted">
                  <small>
                    Showing {{ filteredCards.length }} of {{ cards.length }} cards
                    <span v-if="activeFiltersCount > 0" class="filters-indicator">
                      {{ activeFiltersCount }}
                    </span>
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h6 class="mb-0">Cards Data</h6>
            <div class="d-flex gap-2 align-items-center">
              <small class="text-muted">
                Sorted by: <strong>{{ sortBy }}</strong> 
                <i :class="sortDesc ? 'bi bi-sort-down' : 'bi bi-sort-up'"></i>
              </small>
            </div>
          </div>
          <div class="card-body p-0">
            <Vue3EasyDataTable
              :headers="tableHeaders"
              :items="filteredCards"
              :loading="loading"
              table-class-name="customize-table"
              :show-index="true"
              theme-color="#007bff"
              :rows-per-page="itemsPerPage"
              :rows-per-page-options="itemsPerPageOptions"
              v-model:items-selected="selectedItems"
              :select-options="{
                enable: true,
                selectOnCheckboxOnly: true,
                selectAllByGroup: true
              }"
              @sort="handleSort"
              :sort-by="sortBy"
              :sort-type="sortDesc ? 'desc' : 'asc'"
            >
              <template #item-actions="{ item, index }">
                <div class="d-flex gap-2">
                  <button 
                    class="btn btn-sm btn-info text-white" 
                    @click="viewImage(filteredCards[index-1].image_code)" 
                    title="View Card"
                  >
                    <i class="bi bi-eye"></i> View
                  </button>
                  <button 
                    class="btn btn-sm btn-danger" 
                    @click="deleteImage(filteredCards[index-1].image_code)" 
                    title="Delete Card"
                  >
                    <i class="bi bi-trash"></i> Delete
                  </button>
                </div>
              </template>
            </Vue3EasyDataTable>
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

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.form-check-input {
  cursor: pointer;
}

/* Filter styles */
.filters-card {
  border-left: 4px solid #007bff;
}

.filters-card .card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-select, .form-control {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-select:focus, .form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Filter toggle button */
.btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}

/* Active filter indicator */
.filters-indicator {
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: bold;
}

/* Table header improvements */
.card-header small {
  font-size: 0.875rem;
}

.card-header .bi {
  margin-left: 0.25rem;
}

/* Responsive improvements */
@media (max-width: 768px) {
  .col-md-3, .col-md-6 {
    margin-bottom: 1rem;
  }
  
  .d-flex.gap-2 {
    flex-wrap: wrap;
  }
  
  .btn {
    margin-bottom: 0.5rem;
  }
}

/* Loading states */
.loading-overlay {
  position: relative;
  opacity: 0.6;
  pointer-events: none;
}

/* Filter summary styling */
.filter-summary {
  background-color: #e9ecef;
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-size: 0.875rem;
}

/* Sort indicator */
.sort-indicator {
  color: #007bff;
  font-weight: bold;
}

.sort-indicator .bi {
  margin-left: 0.25rem;
}
</style>
