<script setup>
import UnitToggler from './components/UnitToggler.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-header-inner">
        <div class="brand">
          <span class="brand-icon">🌤️</span>
          <span class="brand-name">WeatherBoard</span>
        </div>

        <nav class="main-nav">
          <RouterLink to="/" class="nav-link">대시보드</RouterLink>
          <RouterLink to="/about" class="nav-link">서비스 소개</RouterLink>
        </nav>

        <UnitToggler />
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 10;
}

.app-header-inner {
  max-width: 1080px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: 800;
  font-size: 18px;
  margin-right: auto;
}

.brand-icon {
  font-size: 20px;
}

.main-nav {
  display: flex;
  gap: var(--space-5);
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 600;
  padding: 6px 2px;
  border-bottom: 2px solid transparent;
  transition:
    color 0.15s,
    border-color 0.15s;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link.router-link-exact-active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.app-main {
  max-width: 1080px;
  margin: 0 auto;
  padding: var(--space-6) 24px 64px;
}
</style>
