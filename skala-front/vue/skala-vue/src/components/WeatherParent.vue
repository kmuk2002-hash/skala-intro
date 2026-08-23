<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'
import { fetchWeatherByCity } from '../api/weatherApi.js'

const router = useRouter()

// 조회할 도시 목록 (한글 이름이면 영문/한글 모두 시도 가능)
const cityNames = ['Seoul', 'Suwon', 'Busan', 'Gwangju', 'Daegu', 'Daejeon']

const weatherList = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

async function loadWeatherData() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const results = await Promise.all(cityNames.map((city) => fetchWeatherByCity(city)))
    weatherList.value = results.map((data) => ({
      id: String(data.id),
      name: data.name,
      temp: Math.round(data.main.temp),
      status: data.weather[0].description,
    }))
  } catch (error) {
    console.error('날씨 데이터를 불러오지 못했습니다:', error)
    errorMessage.value = '날씨 데이터를 불러오는 데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadWeatherData()
})

const searchQuery = ref('')

const filteredWeatherList = computed(() => {
  return weatherList.value.filter((item) => item.name.includes(searchQuery.value))
})

const selectedCityInfo = ref('카드를 클릭하거나 검색해보세요')

const showDetail = (id) => {
  router.push('/weather/' + id)
}
</script>

<template>
  <div class="page-wrapper">
    <p v-if="isLoading">날씨 데이터를 불러오는 중...</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <BaseDashboardCard>
      <template v-slot:SearchBar>
        <SearchBar :search-query="searchQuery" @updateQuery="searchQuery = $event" />
        <div class="search-status">검색중인 도시: {{ searchQuery }}</div>
      </template>
      <template v-slot:WeatherCard>
        <WeatherCard
          :filteredWeatherList="filteredWeatherList"
          @clickCard="selectedCityInfo = $event"
          @clickDetail="showDetail($event.id)"
        />
      </template>
    </BaseDashboardCard>
    <div class="status-bar">{{ selectedCityInfo }}가 선택되었습니다.</div>
  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-status {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.status-bar {
  width: fit-content;
  max-width: 400px;
  background: rgba(17, 209, 46, 0.652);
  border: 1px solid #0aee56;
  border-radius: 8px;
  padding: 14px 16px;
  text-align: center;
  font-weight: 600;
}

.error-message {
  color: #e03131;
  font-weight: 600;
}
</style>
