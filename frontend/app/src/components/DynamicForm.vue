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
    }
  }
}
</script>

<template>
  <div v-for="(value, key) in value" :key="key" class="w-100">

    <hr v-if="!$parent || $parent.$options.name !== 'DynamicForm'" />

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
</template>
