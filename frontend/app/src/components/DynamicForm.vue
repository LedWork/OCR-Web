<script>
export default {
  name: 'DynamicForm',
  props: {
    value: {
      type: Object,
      required: true,
    },
    readonly: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    renderBlocks() {
      // Build a list of renderable blocks describing desired layout
      const data = this.value || {}
      const processed = new Set()
      const blocks = []

      // Personal info block: Nazwisko, Imię, PESEL, Data urodzenia
      const personalInfoFields = ['Nazwisko', 'Imię', 'PESEL', 'Data urodzenia']
      const availablePersonalFields = personalInfoFields.filter(field => data[field] !== undefined)
      if (availablePersonalFields.length > 0) {
        blocks.push({ type: 'personal-info', keys: availablePersonalFields })
        availablePersonalFields.forEach(field => processed.add(field))
      }

      // Stage sections in order
      const stageOrder = ['III st.', 'II st.', 'I st.']
      stageOrder.forEach((stageKey) => {
        if (data[stageKey] !== undefined && typeof data[stageKey] === 'object') {
          blocks.push({ type: 'stage', key: stageKey, value: data[stageKey] })
          processed.add(stageKey)
        }
      })

      // Any remaining fields (fallback)
      Object.keys(data).forEach((key) => {
        if (!processed.has(key)) {
          blocks.push({ type: 'field', key })
        }
      })

      return blocks
    }
  },
  mounted() {
    // Initialize Bootstrap tooltips
    this.initializeTooltips();
  },
  updated() {
    // Re-initialize tooltips after updates
    this.initializeTooltips();
  },
  methods: {
    updateValue(key, newValue) {
      this.$emit('update:value', { ...this.value, [key]: newValue })
    },
    updateNestedValue(key, updatedValue) {
      this.$emit('update:value', { ...this.value, [key]: updatedValue })
    },
    handleKeyDown(event, currentKey, isNested = false, parentKey = null) {
      if (event.key === 'Enter') {
        event.preventDefault();
        this.focusNextField(event.target, currentKey, isNested, parentKey);
      }
    },
    focusNextField(currentInput, currentKey, isNested = false, parentKey = null) {
      const allInputs = Array.from(this.$el.querySelectorAll('input[type="text"]'));
      const currentIndex = allInputs.indexOf(currentInput);
      
      if (currentIndex < allInputs.length - 1) {
        const nextInput = allInputs[currentIndex + 1];
        nextInput.focus();
        nextInput.select(); // Select all text for easy replacement
      }
    },
    getSectionClass(key) {
      if (key === 'III st.') return 'section-iii'
      if (key === 'II st.') return 'section-ii'
      if (key === 'I st.') return 'section-i'
      return ''
    },
    getTooltipText(key) {
      const tooltips = {
        'PESEL': 'PESEL może znajdować się w różnych miejscach na karcie. Sprawdź czy PESEL ma dokładnie 11 cyfr',
        'Data': 'Sprawdź poprawność daty w formacie DD.MM.RRRR lub DD.MM.RR',
        'Na wniosek ZR': 'Wpisz miejscowość dokładnie tak, jak jest na karcie, np. Gdansk, Starog-Gd., również "-//-" lub "\'\'"',
        'Ilość oddanej krwi (bez ml)': 'Wpisz ilość oddanej krwi bez ml i bez dodatkowych znaków, np. 12000',
        'Nazwisko': 'Wpisz nazwisko tak, jak jest na karcie, np. ĆWIKLIŃSKI',
        'Imię': 'Wpisz imię tak, jak jest na karcie, np. MARIUSZ',
        'Data urodzenia': 'Wpisz datę urodzenia tak, jak jest na karcie, np. 22.10.1975',
        'Nr': 'Wpisz numer tak, jak jest na karcie, np. 2986/Gd',
        'Dodatkowe informacje (np. duplikaty)': 'Wpisz dodatkowe informacje wpisane poza wyznaczonymi polami (ale nie PESEL), np. wydane duplikaty',
      }
      return tooltips[key] || `Sprawdź poprawność pola: ${key}`
    },
    initializeTooltips() {
      // Use Bootstrap's tooltip API if available
      this.$nextTick(() => {
        const tooltipTriggerList = this.$el.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(el => {
          if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            new bootstrap.Tooltip(el);
          }
        });
      });
    }
  }
}
</script>

<template>
  <div class="w-100">
    <div v-for="(block, idx) in renderBlocks" :key="idx" class="w-100">
      <!-- Personal info block (all in one row on wide screens) -->
      <div v-if="block.type === 'personal-info'" class="personal-info-block mb-2">
        <div class="personal-info-grid">
          <div v-for="k in block.keys" :key="k" class="personal-info-field">
            <label class="form-label" :title="getTooltipText(k)" data-bs-toggle="tooltip" data-bs-placement="top">
              {{ k }}:
              <span class="tooltip-indicator">?</span>
            </label>
            <input
              :value="value[k]"
              @input="updateValue(k, $event.target.value)"
              @keydown="handleKeyDown($event, k)"
              :name="k"
              :readonly="readonly"
              type="text"
              class="form-control personal-info-input"
            />
          </div>
        </div>
      </div>

      <!-- Pair rows (two inputs in one row) -->
      <div v-else-if="block.type === 'pair'" class="row g-2 mb-1">
        <div v-for="k in block.keys" :key="k" class="col-auto">
          <div class="form-field-wrapper">
            <label class="form-label" :title="getTooltipText(k)" data-bs-toggle="tooltip" data-bs-placement="top">
              {{ k }}:
              <span class="tooltip-indicator">?</span>
            </label>
            <input
              :value="value[k]"
              @input="updateValue(k, $event.target.value)"
              @keydown="handleKeyDown($event, k)"
              :name="k"
              :readonly="readonly"
              type="text"
              class="form-control form-control-compact"
            />
          </div>
        </div>
      </div>

      <!-- Stage sections (compact layout) -->
      <div v-else-if="block.type === 'stage'" :class="getSectionClass(block.key)" class="mb-2">
        <div class="stage-header">
          <label class="form-label stage-title" :title="getTooltipText(block.key)" data-bs-toggle="tooltip" data-bs-placement="top">
            {{ block.key }}:
            <span class="tooltip-indicator">?</span>
          </label>
        </div>
        <div class="stage-inputs-grid">
          <div v-for="(v, k) in block.value" :key="k" class="stage-input-group">
            <label class="stage-field-label" :title="getTooltipText(k)" data-bs-toggle="tooltip" data-bs-placement="top">
              {{ k }}:
              <span class="tooltip-indicator">?</span>
            </label>
            <input
              :value="value[block.key][k]"
              @input="updateNestedValue(block.key, { ...value[block.key], [k]: $event.target.value })"
              @keydown="handleKeyDown($event, k, true, block.key)"
              :name="k"
              :readonly="readonly"
              type="text"
              class="form-control stage-input stage-input-compact"
            />
          </div>
        </div>
      </div>

      <!-- Fallback single fields -->
      <div v-else-if="block.type === 'field'" class="mb-1">
        <label class="form-label" :title="getTooltipText(block.key)" data-bs-toggle="tooltip" data-bs-placement="top">
          {{ block.key }}:
          <span class="tooltip-indicator">?</span>
        </label>
        <input
          :value="value[block.key]"
          @input="updateValue(block.key, $event.target.value)"
          @keydown="handleKeyDown($event, block.key)"
          :name="block.key"
          :readonly="readonly"
          type="text"
          class="form-control"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.section-iii {
  background-color: #e3f2fd;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 8px;
  border-left: 3px solid #2196f3;
}

.section-ii {
  background-color: #f3e5f5;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 8px;
  border-left: 3px solid #9c27b0;
}

.section-i {
  background-color: #e8f5e8;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 8px;
  border-left: 3px solid #4caf50;
}

.stage-header {
  margin-bottom: 6px;
}

.stage-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0;
  color: #333;
}

.stage-inputs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 6px 12px;
  align-items: start;
  justify-content: start;
}

@media (max-width: 768px) {
  .personal-info-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .stage-inputs-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }
}

.stage-input-group {
  display: flex;
  flex-direction: column;
  min-width: 0;
  width: 100%;
}

.stage-field-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #555;
  margin-bottom: 3px;
  display: flex;
  align-items: center;
  cursor: help;
}

.stage-input {
  font-size: 0.95rem;
  padding: 6px 10px;
  height: 38px;
  border-radius: 4px;
}

.form-field-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.form-control-compact {
  width: 100%;
  min-width: 100px;
  font-size: 1rem;
  padding: 8px 12px;
  height: 42px;
}

.stage-input-compact {
  width: 100%;
  min-width: 90px;
  font-size: 0.95rem;
  padding: 6px 10px;
  height: 38px;
}

.personal-info-block {
  background-color: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 4px solid #6c757d;
  margin-bottom: 12px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.personal-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px 16px;
  align-items: flex-start;
  width: 100%;
  max-width: 100%;
}

.personal-info-field {
  display: flex;
  flex-direction: column;
  min-width: 0;
  width: 100%;
}

.personal-info-input {
  width: 100%;
  font-size: 1rem;
  padding: 8px 12px;
  height: 42px;
  box-sizing: border-box;
}

.form-label {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  cursor: help;
  font-size: 0.85rem;
}

.tooltip-indicator {
  display: inline-flex;
  align-items: center;
  margin-left: 6px;
  cursor: help;
  transition: all 0.2s ease;
}

.tooltip-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  margin-left: 6px;
  cursor: help;
  transition: all 0.2s ease;
  border-radius: 50%;
  background-color: #e9ecef;
  color: #6c757d;
  font-size: 12px;
  font-weight: bold;
  line-height: 1;
  animation: subtle-glow 3s ease-in-out infinite;
}

@keyframes subtle-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.1);
  }
  50% {
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2);
  }
}

.tooltip-indicator:hover {
  background-color: #007bff;
  color: white;
  transform: scale(1.05);
}

/* Custom tooltip styling */
:deep(.tooltip) {
  font-size: 0.875rem;
}

:deep(.tooltip-inner) {
  max-width: 300px;
  text-align: left;
  padding: 8px 12px;
  background-color: #333;
  border-radius: 6px;
}

/* Enhanced focus styles for form inputs */
.personal-info-input:focus,
.stage-input:focus,
.form-control:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Ensure proper tab order - handled by HTML tabindex attribute */
</style>
