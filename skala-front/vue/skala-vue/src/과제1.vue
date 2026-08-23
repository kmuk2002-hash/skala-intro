<script setup>
import UnitToggler from './components/UnitToggler.vue'
</script>

<template>
  <div class="app-wrapper">
    <h2 class="app-title">🌤️ 과제 1: 날씨(Mock up)</h2>

    <nav class="main-nav">
      <RouterLink to="/" class="nav-link">Home</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
      <UnitToggler />
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.main-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  padding: 14px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #e5e5e5;
}
</style>
