<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'
import { fetchWeatherByCity } from '../api/weatherApi.js'

const router = useRouter()

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
  <div class="page">
    <section class="page-intro">
      <h1 class="page-title">지역별 실시간 날씨</h1>
      <p class="page-subtitle">도시를 검색하거나 카드를 선택해 상세 정보를 확인하세요.</p>
    </section>

    <p v-if="isLoading" class="loading-text">날씨 데이터를 불러오는 중...</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <BaseDashboardCard>
      <template v-slot:SearchBar>
        <SearchBar :search-query="searchQuery" @updateQuery="searchQuery = $event" />
      </template>
      <template v-slot:WeatherCard>
        <WeatherCard
          :filteredWeatherList="filteredWeatherList"
          @clickCard="selectedCityInfo = $event"
          @clickDetail="showDetail($event.id)"
        />
      </template>
    </BaseDashboardCard>

    <div class="status-toast">
      <span class="status-dot"></span>
      {{ selectedCityInfo }}가 선택되었습니다.
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.page-title {
  font-size: 26px;
  font-weight: 800;
  margin: 0 0 4px;
}

.page-subtitle {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

.loading-text {
  color: var(--color-text-muted);
  font-size: 14px;
}

.error-message {
  color: var(--color-hot);
  font-weight: 600;
  font-size: 14px;
}

.status-toast {
  display: flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 10px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-mild);
  flex-shrink: 0;
}
</style>
