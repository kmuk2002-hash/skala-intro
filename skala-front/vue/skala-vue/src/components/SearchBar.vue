<script setup>
defineProps({
  searchQuery: String,
})

const emit = defineEmits(['updateQuery'])

const sendToParent = (value) => {
  emit('updateQuery', value)
}
</script>

<template>
  <div class="search-block">
    <h3 class="panel-title">도시 검색</h3>
    <el-input
      :model-value="searchQuery"
      @input="sendToParent"
      placeholder="궁금한 도시를 입력하시오"
      clearable
    />
    <p class="search-hint">
      <template v-if="searchQuery">"{{ searchQuery }}" 검색 중</template>
      <template v-else>전체 도시가 표시됩니다</template>
    </p>
  </div>
</template>

<style scoped>
.panel-title {
  margin: 0 0 var(--space-4);
  font-size: 15px;
  font-weight: 700;
}

.search-hint {
  margin: 10px 2px 0;
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>
