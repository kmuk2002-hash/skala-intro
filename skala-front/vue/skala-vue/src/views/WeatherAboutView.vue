<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
  router.push('/')
}

const features = [
  { icon: '🧩', text: '컴포넌트 단위로 화면을 분리하여 재사용성을 높인 구조' },
  { icon: '🔀', text: '클라이언트 사이드 라우팅을 통한 새로고침 없는 화면 전환' },
  { icon: '📍', text: '동적 라우트를 활용한 도시별 상세 날씨 정보 조회' },
]
</script>

<template>
  <div class="about-page">
    <div class="about-card">
      <h2 class="about-title">서비스 소개</h2>
      <p class="about-desc">
        본 앱은 Vue 3 및 Vue Router 4 기반으로 제작된 실습용 기상 관측 대시보드 시스템입니다.
      </p>

      <ul class="feature-list">
        <li v-for="feature in features" :key="feature.text">
          <span class="feature-icon">{{ feature.icon }}</span>
          {{ feature.text }}
        </li>
      </ul>

      <button class="home-btn" @click="goToHome">대시보드 홈으로 이동</button>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  max-width: 480px;
  margin: 0 auto;
}

.about-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--space-6);
}

.about-title {
  margin: 0 0 var(--space-3);
  font-size: 20px;
  font-weight: 800;
}

.about-desc {
  margin: 0 0 var(--space-5);
  color: var(--color-text-muted);
  font-size: 14px;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.feature-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: var(--color-text);
}

.feature-icon {
  flex-shrink: 0;
}

.home-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: white;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.15s;
}

.home-btn:hover {
  background: var(--color-primary-dark);
}
</style>
