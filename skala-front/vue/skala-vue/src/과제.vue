<script setup>
import { ref, computed, watch, watchEffect } from 'vue'

const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
  { id: 'city_04', name: '광주', temp: 34, status: '맑음' },
  { id: 'city_05', name: '대구', temp: 28, status: '흐림' },
  { id: 'city_06', name: '대전', temp: 25, status: '비' },
  { id: 'city_07', name: '추운도시1', temp: 10, status: '비' },
  { id: 'city_08', name: '추운도시2', temp: -1, status: '눈' },
])

const selectedCityInfo = ref('카드를 클릭하거나 검색해보세요')

watch(selectedCityInfo, (newValue, oldValue) => {
  console.log(`상태바 문구가 변경되었습니다: ${newValue}`)
})

const getCity = (city) => {
  selectedCityInfo.value = `${city}가 선택되었습니다.`
}

const searchQuery = ref('')

let debounceTimer = null
watch(searchQuery, (newValue) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    console.log(`현재 검색어 ${newValue}에 매칭되는 API데이터를 필터링했습니다.`)
  }, 300)
})
const showDetail = (cityName, status) => {
  window.alert(`${cityName}의 현재 날씨는 ${status}상태입니다.`)
}

const filteredWeatherList = computed(() => {
  return weatherList.value.filter((item) => {
    return item.name.includes(searchQuery.value)
  })
})
</script>

<template>
  <div class="box">
    <h2>🌤️ 과제 1: 날씨(Mock up)</h2>
    <div class="searchcity">
      🔍 도시검색
      <input
        type="text"
        :value="searchQuery"
        @input="searchQuery = $event.target.value"
        placeholder="궁금한 도시를 입력하시오"
      />
      <br />
      검색중인 도시: {{ searchQuery }}
    </div>

    <div class="weather-section">
      <h2>🗺️ 지역별 날씨 현황</h2>
      <div
        class="weather-card"
        @click="getCity(item.name)"
        v-for="item in filteredWeatherList"
        :key="item.id"
      >
        <div class="weather-info">
          <div class="weather-title">{{ item.name }} ({{ item.status }})</div>
          <div class="weather-temp">현재 기온: {{ item.temp }}°C</div>
          <span v-if="item.temp > 30" class="badge-very-hot">매우 더움(30도 이상)</span>
          <span v-else-if="item.temp > 25" class="badge-hot">더움(25~30도)</span>
          <span v-else-if="item.temp > 20" class="badge-mild">선선(20~25도)</span>
          <span v-else-if="item.temp > 10" class="badge-cool">쌀쌀(10~20도)</span>
          <span v-else-if="item.temp > 0" class="badge-cold">추움(0~10도)</span>
          <span v-else class="cold">매우 추움(0도 이하)</span>
        </div>
        <button @click.stop="showDetail(item.name, item.status)">상세보기</button>
      </div>
      <div class="weather-info" v-if="filteredWeatherList.length === 0">
        검색 결과가 일치하는 도시가 없습니다.
      </div>
    </div>

    <div class="status-bar">{{ selectedCityInfo }}</div>
  </div>
</template>

<style scoped>
.box {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: rgb(248, 248, 248);
  border: 3px solid #d4d1d1;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
}

.box > h2 {
  padding-bottom: 12px;
  margin-bottom: 16px;
  border-bottom: 1px solid #e5e5e5;
}

.searchcity {
  background: rgba(210, 208, 208, 0.652);
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 12px;
}

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
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.6;
  cursor: pointer;
}

.weather-card:last-child {
  margin-bottom: 0;
}

.weather-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.weather-title {
  font-weight: 700;
}

.weather-card button {
  flex-shrink: 0;
  padding: 6px 12px;
  border: 1px solid #d4d1d1;
  border-radius: 6px;
  background: #f4f4f4;
  cursor: pointer;
}

.status-bar {
  background: rgba(17, 209, 46, 0.652);
  border: 1px solid #0aee56;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 12px;
  text-align: center;
  font-weight: 600;
}

.badge-very-hot,
.badge-hot,
.badge-mild,
.badge-cool,
.badge-cold,
.cold {
  display: inline-block;
  width: fit-content;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
}

.badge-very-hot {
  background: #ff8787;
  color: white;
}
.badge-hot {
  background: #ffe1e1;
  color: #e03131;
}
.badge-mild {
  background: #fff9db;
  color: #f08c00;
}
.badge-cool {
  background: #e3f0ff;
  color: #1c7ed6;
}
.badge-cold {
  background: #d0ebff;
  color: #1864ab;
}
.cold {
  background: #0a71bf;
  color: #79abd9;
}
</style>
