// stores/configStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useConfigStore = defineStore('config', () => {
  // state
  const unit = ref('celsius')

  // getters
  const unitSymbol = computed(() => (unit.value === 'fahrenheit' ? '°F' : '°C'))

  // actions
  const toggleUnit = () => {
    unit.value = unit.value === 'celsius' ? 'fahrenheit' : 'celsius'
  }

  return { unit, unitSymbol, toggleUnit }
})
