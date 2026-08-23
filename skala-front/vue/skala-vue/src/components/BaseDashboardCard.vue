<script setup></script>

<template>
  <div class="dashboard-grid">
    <div class="panel panel-search">
      <slot name="SearchBar"></slot>
    </div>
    <div class="panel panel-list">
      <slot name="WeatherCard"></slot>
    </div>
  </div>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--space-5);
  align-items: start;
}

.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--space-5);
}

@media (max-width: 720px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
