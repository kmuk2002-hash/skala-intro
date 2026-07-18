import { getWeather } from "./weatherAPI.js";

var cityData = {
    seoul: { name: "서울", lat: 37.5665, lon: 126.9780 },
    busan: { name: "부산", lat: 35.1796, lon: 129.0756 },
    incheon: { name: "인천", lat: 37.4563, lon: 126.7052 },
    jeju: { name: "제주", lat: 33.4996, lon: 126.5312 }
};

document.addEventListener("DOMContentLoaded", function () {
    var citySelect = document.getElementById("city-select");
    var weatherBox = document.getElementById("weather-box");

    citySelect.addEventListener("change", async function () {
        var selected = citySelect.value;

        if (selected === "") {
            weatherBox.innerHTML = "";
            return;
        }

        var city = cityData[selected];

        weatherBox.innerHTML =
            "<p>선택한 도시: " + city.name + "</p>" +
            "<p>위도: " + city.lat + ", 경도: " + city.lon + "</p>" +
            "<p>로딩 중... ⏳</p>";

        try {
            var current = await getWeather(city.lat, city.lon);

            weatherBox.innerHTML =
                "<p>선택한 도시: " + city.name + "</p>" +
                "<p>위도: " + city.lat + ", 경도: " + city.lon + "</p>" +
                "<p>현재 온도: " + current.temperature_2m + "°C</p>" +
                "<p>현재 습도: " + current.relative_humidity_2m + "%</p>";
        } catch (error) {
            weatherBox.innerHTML =
                "<p>선택한 도시: " + city.name + "</p>" +
                "<p>날씨 정보를 불러오지 못했습니다.</p>";
        }
    });
});