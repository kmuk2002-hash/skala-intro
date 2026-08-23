<script setup>
defineProps({
  cityName: String,
  status: String,
})

const emit = defineEmits(['select-city'])

const handleCardClick = (name) => {
  emit('select-city', name)
}
</script>

<template>
  <div class="weather-card" @click="handleCardClick(cityName)">
    <h4>{{ cityName }} ({{ status }})</h4>
    <p>클릭하면 부모에게 신호를 보냅니다.</p>
  </div>
</template>
