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
    }
  }
}
</script>

<template>
  <div v-for="(value, key) in value" :key="key" class="w-100">

    <hr v-if="!$parent || $parent.$options.name !== 'DynamicForm'" />

    <div :class="getSectionClass(key)">
      <label class="form-label">
        {{ key }}:
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
</style>
