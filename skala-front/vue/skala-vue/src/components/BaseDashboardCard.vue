<script setup></script>

<template>
  <div class="dashboard-wrapper">
    <div class="dashboard-box search-box">
      <slot name="SearchBar"></slot>
    </div>
    <div class="dashboard-box list-box">
      <slot name="WeatherCard"></slot>
    </div>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column; /* 위아래로 쌓기 */
  gap: 12px;
}

.dashboard-box {
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: rgb(248, 248, 248);
  border: 3px solid #d4d1d1;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
}

/* 검색 박스: 내용물 크기만큼만, 너무 넓지 않게 상한선만 걸기 */
.search-box {
  width: fit-content;
  max-width: 400px;
}

/* 목록 박스: 카드가 여러 개 들어가니 기존처럼 넓게 */
.list-box {
  max-width: 960px;
}
</style>
