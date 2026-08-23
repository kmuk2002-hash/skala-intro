<script setup>
import { ref } from 'vue'
import child from './Childcomponent3.vue'

const message = ref('Parent 초기 메세지')
const handleUpdateReqjuest = (newValue) => {
  message.value = newValue
}
</script>

<template>
  <div class="practice-section">
    <h2>Props & Emits</h2>
    <div class="parent-container">
      <h2>상위 컴포넌트(Parent)</h2>
      <p>현재 로컬 데이터(state): {{ message }}</p>
      <br />
      <child :parent-data="message" @update-request="handleUpdateReqjuest" />
    </div>
  </div>
</template>
