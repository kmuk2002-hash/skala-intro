<script setup>
import { ref, watch } from 'vue'

const currentCity = ref('서울')
const logMessage = ref('아직 감시 시스템이 작동하지 않았습니다.')

watch(currentCity, (newone, oldone) => {
  logMessage.value = `감시자 발동 ${oldone}가 ${newone} 로 변경`
  console.log(`기상청 서버에서 ${newone}의 날씨 api를 다시 조회합니다.`)
})
</script>

<template>
  <div class="practice-section">
    <h2>감시자 watch()의 원리와 실무 활용</h2>
    <h3>지역 선택 제어판</h3>
    <button @click="currentCity = '서울'">서울 선택</button>
    <button @click="currentCity = '부산'">부산 선택</button>
    <button @click="currentCity = '대구'">대구 선택</button>
    <div class="monitor">
      <h3>모니터링 시스템</h3>
      <p>{{ logMessage }}</p>
    </div>
  </div>
</template>
