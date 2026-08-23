<script setup>
const props = defineProps({
  searchQuery: String,
})

const emit = defineEmits(['updateQuery'])

const sendToParent = (value) => {
  emit('updateQuery', value)
}
</script>

<template>
  <div class="searchcity">
    🔍 도시검색 <br />
    도시검색창입니다.
    <el-input
      :model-value="searchQuery"
      @input="sendToParent"
      placeholder="궁금한 도시를 입력하시오"
      clearable
    />
    <br />
  </div>
</template>

<style scoped>
.searchcity {
  background: rgba(210, 208, 208, 0.652);
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 14px 16px;
}
</style>
