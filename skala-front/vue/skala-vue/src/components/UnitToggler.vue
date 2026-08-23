<script setup>
import { useConfigStore } from '../stores/configStore'

const configStore = useConfigStore()
</script>

<template>
  <button class="unit-toggle" @click="configStore.toggleUnit">
    <span class="unit-current">{{ configStore.unit === 'celsius' ? '°C' : '°F' }}</span>
    <span class="unit-switch-icon">⇄</span>
    <span class="unit-target">{{ configStore.unit === 'celsius' ? '°F' : '°C' }}</span>
  </button>
</template>

<style scoped>
.unit-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: var(--color-surface);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition:
    border-color 0.15s,
    box-shadow 0.15s;
}

.unit-toggle:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.unit-current {
  color: var(--color-primary);
}

.unit-switch-icon {
  color: var(--color-text-muted);
  font-size: 12px;
}

.unit-target {
  color: var(--color-text-muted);
}
</style>
