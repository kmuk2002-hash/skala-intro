<script setup>
defineProps({
  cityName: String,
  areaCode: Number,
})
</script>

<template>
  <div class="card">
    <p>지역명: {{ cityName }}</p>
    <p>지역 코드: {{ areaCode }}</p>
  </div>
</template>
