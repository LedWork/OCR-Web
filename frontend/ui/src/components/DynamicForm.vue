<template>
  <div v-for="(value, key) in value" :key="key">
    <p class="caption">{{ key }}:</p>

    <div v-if="typeof value === 'object' && value !== null" class="inputs-row">
      <DynamicForm :value="value" @update:value="updateNestedValue(key, $event)" />
    </div>

    <input
      v-else
      :value="value"
      @input="updateValue(key, $event.target.value)"
      :placeholder="key"
      :name="key"
      type="text"
      class="text-input"
    />
  </div>
</template>

<script>
export default {
  name: 'DynamicForm',
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  methods: {
    updateValue(key, newValue) {
      this.$emit('update:value', { ...this.value, [key]: newValue })
    },
    updateNestedValue(key, updatedValue) {
      this.$emit('update:value', { ...this.value, [key]: updatedValue })
    },
  },
}
</script>
