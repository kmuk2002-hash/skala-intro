<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  fetchWeatherByCityId,
  fetchCoordsByCity,
  fetchForecast,
  fetchAirPollution,
} from '../api/weatherApi.js'

const route = useRoute()
const router = useRouter()

const selectedCity = ref(null)
const forecastList = ref([])
const airQuality = ref(null)
const isLoading = ref(false)

// AQI(1~5) 숫자를 텍스트/색상으로 변환
const aqiLabels = {
  1: { text: '좋음', type: 'success' },
  2: { text: '보통', type: 'primary' },
  3: { text: '민감군 주의', type: 'warning' },
  4: { text: '나쁨', type: 'danger' },
  5: { text: '매우 나쁨', type: 'danger' },
}

onMounted(async () => {
  isLoading.value = true
  try {
    // 1. 현재 날씨 (기존 로직)
    const weatherData = await fetchWeatherByCityId(route.params.id)
    selectedCity.value = {
      name: weatherData.name,
      temp: Math.round(weatherData.main.temp),
      status: weatherData.weather[0].description,
    }

    // 2. Geocoding으로 위경도 확보
    const coords = await fetchCoordsByCity(weatherData.name)

    // 3. 예보 + 대기질을 동시에 요청
    const [forecastData, airData] = await Promise.all([
      fetchForecast(coords.lat, coords.lon),
      fetchAirPollution(coords.lat, coords.lon),
    ])

    // 3시간 간격 데이터 중, 하루에 1개씩만 뽑아 5일치로 정리
    forecastList.value = forecastData.list
      .filter((item) => item.dt_txt.includes('12:00:00'))
      .map((item) => ({
        date: item.dt_txt.slice(5, 10),
        temp: Math.round(item.main.temp),
        status: item.weather[0].description,
      }))

    airQuality.value = aqiLabels[airData.list[0].main.aqi]
  } catch (error) {
    console.error(error)
    selectedCity.value = null
  } finally {
    isLoading.value = false
  }
})

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="detail-wrapper">
    <p v-if="isLoading">불러오는 중...</p>

    <div v-else-if="selectedCity" class="detail-card">
      <h2 class="detail-title">{{ selectedCity.name }} ({{ selectedCity.status }})</h2>
      <p class="detail-temp">현재 기온: {{ selectedCity.temp }}°C</p>

      <!-- 대기질 -->
      <el-tag v-if="airQuality" :type="airQuality.type" size="small">
        대기질: {{ airQuality.text }}
      </el-tag>

      <!-- 5일 예보 -->
      <div class="forecast-section" v-if="forecastList.length">
        <h3>5일 예보</h3>
        <div class="forecast-list">
          <div class="forecast-item" v-for="day in forecastList" :key="day.date">
            <div>{{ day.date }}</div>
            <div>{{ day.temp }}°C</div>
            <div>{{ day.status }}</div>
          </div>
        </div>
      </div>

      <button class="back-btn" @click="goBack">목록으로 돌아가기</button>
    </div>

    <div v-else class="not-found">
      <p>해당 도시 정보를 찾을 수 없습니다.</p>
      <button class="back-btn" @click="goBack">목록으로 돌아가기</button>
    </div>
  </div>
</template>

<style scoped>
.detail-wrapper {
  max-width: 400px;
  margin: 20px auto;
}

.detail-card,
.not-found {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.detail-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
}

.detail-temp {
  font-size: 16px;
  color: #444;
  margin-bottom: 12px;
}

.back-btn {
  display: block;
  margin: 16px auto 0;
  padding: 8px 16px;
  border: 1px solid #d4d1d1;
  border-radius: 6px;
  background: #f4f4f4;
  cursor: pointer;
}

.badge-very-hot,
.badge-hot,
.badge-mild,
.badge-cool,
.badge-cold,
.cold {
  display: inline-block;
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
.forecast-section {
  margin-top: 16px;
  text-align: left;
}

.forecast-list {
  display: flex;
  gap: 8px;
  overflow-x: auto;
}

.forecast-item {
  flex-shrink: 0;
  width: 70px;
  padding: 8px;
  background: #f7f8fa;
  border-radius: 6px;
  text-align: center;
  font-size: 12px;
}
</style>
