<script setup>
import { useConfigStore } from '../stores/configStore'

const props = defineProps({
  filteredWeatherList: Array,
})

const emit = defineEmits(['clickCard', 'clickDetail'])
const configStore = useConfigStore()

const clickcard = (item) => {
  emit('clickCard', item.name)
}
const clickdetail = (item) => {
  emit('clickDetail', item)
}

const displayTemp = (rawTemp) => {
  if (configStore.unit === 'fahrenheit') {
    return Math.round((rawTemp * 9) / 5 + 32)
  }
  return rawTemp
}

// 원본 섭씨 기준으로 배지 타입/텍스트를 결정
const getBadge = (temp) => {
  if (temp > 30) return { text: '매우 더움(30도 이상)', type: 'danger' }
  if (temp > 25) return { text: '더움(25~30도)', type: 'warning' }
  if (temp > 20) return { text: '선선(20~25도)', type: 'success' }
  if (temp > 10) return { text: '쌀쌀(10~20도)', type: 'info' }
  if (temp > 0) return { text: '추움(0~10도)', type: 'primary' }
  return { text: '매우 추움(0도 이하)', type: '' }
}
</script>

<template>
  날씨카드입니다.
  <div class="weather-section">
    <h2>🗺️ 지역별 날씨 현황</h2>

    <el-card
      class="weather-card"
      shadow="hover"
      v-for="item in props.filteredWeatherList"
      :key="item.id"
      @click="clickcard(item)"
    >
      <div class="card-body">
        <div class="weather-info">
          <div class="weather-title">{{ item.name }} ({{ item.status }})</div>
          <div class="weather-temp">
            현재 기온: {{ displayTemp(item.temp) }}{{ configStore.unitSymbol }}
          </div>
          <el-tag :type="getBadge(item.temp).type" size="small">
            {{ getBadge(item.temp).text }}
          </el-tag>
        </div>
        <el-button size="small" @click.stop="clickdetail(item)">상세보기</el-button>
      </div>
    </el-card>

    <div class="weather-info no-result" v-if="props.filteredWeatherList.length === 0">
      검색 결과가 일치하는 도시가 없습니다.
    </div>
  </div>
</template>

<style scoped>
.weather-section {
  background: rgba(210, 208, 208, 0.652);
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 14px 16px;
}

.weather-section h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

.weather-card {
  margin-bottom: 12px;
  cursor: pointer;
}

.weather-card:last-child {
  margin-bottom: 0;
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weather-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.weather-title {
  font-weight: 700;
}

.no-result {
  text-align: center;
  padding: 20px;
  color: #888;
}
</style>
