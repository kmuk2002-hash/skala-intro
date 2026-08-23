import axios from 'axios'

const API_KEY = import.meta.env.VITE_WEATHER_API_KEY
const WEATHER_BASE = 'https://api.openweathermap.org/data/2.5'
const GEO_BASE = 'https://api.openweathermap.org/geo/1.0'

export async function fetchWeatherByCity(cityName) {
  const response = await axios.get(`${WEATHER_BASE}/weather`, {
    params: { q: cityName, appid: API_KEY, units: 'metric', lang: 'kr' },
  })
  return response.data
}

export async function fetchWeatherByCityId(cityId) {
  const response = await axios.get(`${WEATHER_BASE}/weather`, {
    params: { id: cityId, appid: API_KEY, units: 'metric', lang: 'kr' },
  })
  return response.data
}

// 1. Geocoding — 도시 이름 → 위경도
export async function fetchCoordsByCity(cityName) {
  const response = await axios.get(`${GEO_BASE}/direct`, {
    params: { q: cityName, limit: 1, appid: API_KEY },
  })
  return response.data[0] // { lat, lon, name, country, ... }
}

// 2. 5일/3시간 예보
export async function fetchForecast(lat, lon) {
  const response = await axios.get(`${WEATHER_BASE}/forecast`, {
    params: { lat, lon, appid: API_KEY, units: 'metric', lang: 'kr' },
  })
  return response.data
}

// 3. 대기오염
export async function fetchAirPollution(lat, lon) {
  const response = await axios.get(`${WEATHER_BASE}/air_pollution`, {
    params: { lat, lon, appid: API_KEY },
  })
  return response.data
}
