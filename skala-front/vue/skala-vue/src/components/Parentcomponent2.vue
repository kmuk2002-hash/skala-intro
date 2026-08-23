<script setup>
import { ref } from 'vue'
import Child from './Childcomponent2.vue'
const selectedCityInfo = ref('카드를 클릭해 보세요.')

const receiveCitySignal = (cityName) => {
  selectedCityInfo.value = `${cityName}이 성공적으로 선택되었습니다.`
}
</script>

<template>
  <div class="parent-box">
    <h2>부모관제탑</h2>
    <hr />

    <Child cityName="서울" status="맑음" @select-city="receiveCitySignal" />
    <Child cityName="수원" status="비" @select-city="receiveCitySignal" />

    <div class="status-bar">
      {{ selectedCityInfo }}
    </div>
  </div>
</template>
