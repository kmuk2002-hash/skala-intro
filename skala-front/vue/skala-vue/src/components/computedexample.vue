<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const dummy = ref(0)

const getMethodResult = () => {
  console.log('일반함수 실행')
  return count.value * 2
}

const doubleCount = computed(() => {
  console.log('computed연산 실행')
  return count.value * 2
})
</script>

<template>
  <div class="practice-section">
    <h2>computed() 캐싱 동작 비교</h2>

    <p>count: {{ count }} | dummy: {{ dummy }}</p>
    <button @click="count++">count 증가</button>
    <button @click="dummy++">dummy 증가</button>
    <p>일반 함수 결과: {{ getMethodResult() }}</p>
    <p>computed 결과: {{ doubleCount }}</p>
  </div>
</template>
