<script setup>
import { useConfigStore } from '../stores/configStore'

const configStore = useConfigStore()
</script>

<template>
  <div class="unit-toggler">
    날씨단위: {{ configStore.unit === 'celsius' ? '섭씨(°C)' : '화씨(°F)' }}
    <el-button type="primary" size="small" @click="configStore.toggleUnit">단위변경</el-button>
  </div>
</template>

<style scoped>
.unit-toggler {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
</style>
