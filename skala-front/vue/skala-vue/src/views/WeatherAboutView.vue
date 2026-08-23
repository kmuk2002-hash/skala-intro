<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="about-wrapper">
    <div class="about-card">
      <h2 class="about-title">ℹ️ 서비스 소개</h2>
      <p class="about-desc">
        본 앱은 Vue 3 및 Vue Router 4 기반으로 제작된 실습용 기상 관측 대시보드 시스템입니다.
      </p>
      <ul class="about-list">
        <li>컴포넌트 단위로 화면을 분리하여 재사용성을 높인 구조</li>
        <li>클라이언트 사이드 라우팅을 통한 새로고침 없는 화면 전환</li>
        <li>동적 라우트를 활용한 도시별 상세 날씨 정보 조회</li>
      </ul>

      <button class="home-btn" @click="goToHome">대시보드 홈으로 이동</button>
    </div>
  </div>
</template>

<style scoped>
.about-wrapper {
  max-width: 480px;
  margin: 20px auto;
}

.about-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 20px;
}

.about-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.about-desc {
  font-size: 14px;
  color: #444;
  line-height: 1.6;
  margin-bottom: 12px;
}

.about-list {
  list-style: disc;
  padding-left: 20px;
  font-size: 14px;
  color: #444;
  line-height: 1.8;
  margin-bottom: 20px;
}

.home-btn {
  display: block;
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  background: #4096ff;
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.home-btn:hover {
  background: #1c7ed6;
}
</style>
