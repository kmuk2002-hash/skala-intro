<script setup>
import { ref, watch } from 'vue'
const city = ref('서울')
const dateType = ref('오늘')
const apiStatus = ref('대기 중...')

watch([city, dateType], ([newcity, newdate], [oldcity, olddate]) => {
  apiStatus.value = `변경감지 ${oldcity}(${olddate})가 ${newcity}(${newdate})`
  console.log(`${newcity}의 ${newdate} 날씨를 불러옵니다..`)
})
</script>

<template>
  <div class="practice-section">
    <h2>여러 개의 변수 동시 감시</h2>
    <h3>날씨 조건 설정</h3>
    <label>도시:</label>
    <select v-model="city">
      <option value="서울">서울</option>
      <option value="수원">수원</option>
      <option value="부산">부산</option>
    </select>
    <label>날짜:</label>
    <label><input type="radio" value="오늘" v-model="dateType" />오늘</label>
    <label><input type="radio" value="내일" v-model="dateType" />내일</label>
    <label><input type="radio" value="주간예보" v-model="dateType" />주간예보</label>
    <div class="monitor">
      <h3>통합 모니터링 로그</h3>
      <p>현재 상태: {{ apiStatus }}</p>
    </div>
  </div>
</template>
