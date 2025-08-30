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
  <div v-for="(value, key) in value" :key="key" class="w-100">

    <hr v-if="!$parent || $parent.$options.name !== 'DynamicForm'" />

    <div :class="getSectionClass(key)">
      <label class="form-label" :title="getTooltipText(key)" data-bs-toggle="tooltip" data-bs-placement="top">
        {{ key }}:
        <span class="tooltip-indicator">?</span>
      </label>

      <div v-if="typeof value === 'object' && value !== null" class="inputs-row">
        <DynamicForm :value="value" @update:value="updateNestedValue(key, $event)" />
      </div>

      <input
        v-else
        :value="value"
        @input="updateValue(key, $event.target.value)"
        :placeholder="key"
        :name="key"
        :readonly="readonly"
        type="text"
        class="form-control"
      />
    </div>
  </div>
</template>

<style scoped>
.section-iii {
  background-color: #e3f2fd;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  border-left: 4px solid #2196f3;
}

.section-ii {
  background-color: #f3e5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  border-left: 4px solid #9c27b0;
}

.section-i {
  background-color: #e8f5e8;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  border-left: 4px solid #4caf50;
}

.inputs-row {
  margin-top: 10px;
}

.form-label {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  cursor: help;
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
</style>
