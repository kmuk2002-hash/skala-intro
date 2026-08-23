# skala-vue

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

# 과제(116pg)

### 1. 배열 렌더링

배열을 만든 후 <div v-for="(id, name, temp, status) in weatherList" :key="id">로 배열 랜더링을 진행 -> 하지만 원하는 대로 text interpolation되지 않음
->배열로 만들어 for로 읽었는데 바로 객체의 property를 호출했기 때문이라고 생각->정답
<div v-for="(item, index) in weatherList" :key="id">로 수정 및 text interpoltation시 item.property로 접근

### 2.조건부 렌더링

위의 v-for 형태에 카테고리가 나올 수 있는 부분을 추가함.
<div class="weather-card" v-for="(item, index) in weatherList" :key="id">
{{ item.name }} ({{ item.status }})
<br />
현재 기온: {{ item.temp }}도
<br />
<span v-if="item.temp > 30" class="badge-very-hot">매우 더움(30도 이상)</span>
<span v-else-if="item.temp > 25" class="badge-hot">더움(25~~30도)</span>
<span v-else-if="item.temp > 20" class="badge-mild">선선(20~~25도)</span>
<span v-else-if="item.temp > 10" class="badge-cool">쌀쌀(10~~20도)</span>
<span v-else-if="item.temp > 0" class="badge-cold">추움(0~~10도)</span>
<span v-else="item.temp > 0" class="cold">매우 추움(0도 이하)</span>---->원래 없었다가 영하의 날씨는 style적용이 안되는 걸 보고 추가
</div>

각 조건별로 class를 지정하고 style을 따로 지정해 과제를 구현

### 3.양방향 바인딩 및 한글 처리

초기 구현시 항목만 보고 양방향바인딩이라 v-model로 구현함. 하지만 안내로 v-bind와 @input으로 구현하라고 하는 부분을 확인하고 v-bind와 @input으로 v-model의 기능을 구현함.

### 4.이벤트 및 수식어

- 지역별 날씨 현황 카드를 누르면 상태바에 ~~표기 ->어떻게 할 지 몰라서 수업교재 100pg를 참고해 해결, 다만 달라진 점은 해당 과제에서는 이벤트 객체를 받을 필요가 없으므로 click시 city만 받아 화면에 노출되는 메세지가 달라지도로 작성
  -상세보기 버튼을 for문을 통해 모두 생성하고 해당 버튼에 @click.stop을 걸어 버블링을 방지 및 window.alert로 메세지 등장시킴

마지막에 예시와 style을 맞추기 위해 전체코드를 ai에 넣어 검사를 받아 스타일과 코드를 완성. 또한 해당 과정에서 놓치고 있던 잘못된 점을을 확인 후 수정조치(기능엔 문제가 없었음)

- v-for="(item, index) in weatherList" → v-for="item in weatherList": index를 화면 표시나 로직(순번 표시, 배열 조작 등)에 전혀 쓰지 않으므로 불필요한 index 선언 제거
- :key="id" → :key="item.id": 스코프에 없는 변수 id를 참조하던 오류 수정 (item.id로 바로잡아 key가 정상적으로 각 카드에 매핑되도록 함)

### 5. 본인만의 데이터를 추가하고 이를 기초로 Mockup을 추가한다.

- 데이터를 기존 3개에서 8개로 늘림

# 과제 (145pg)

### 1.반응형 상태 관리

- 기존과 동일

### 2. 검색 도시(computed 활용)

- .filterd를 활용해 computed의 콜백함수를 구현 weatherList는 배열이므로 value로 접근시 객체가 반환됨. 우리는 객체 안의 name과 검색어를 비교해야하므로 아이템을 받아서 아이템의 이름이 weatherlist의 name에 포함될 경우만 반환하여 해당 객체를 담아야 해서 return을 두번 써서 구현함.(잘 모르겠어서 클로드의 도움을 받았음.)

### 3. 반응형 변수 변화 감시 (watch, watchEffect)

- selectedCityInfo 감시: 하나의 변수를 감시하는 watch문을 작성하여 완성
  -searchQuery 감시:

  const searchQuery = ref('')

watchEffect(() => {
console.log(`현재 검색어 ${searchQuery.value}에 매칭되는 API데이터를 필터링했습니다.`)
})

해당 코드로 구현시 너무 많은 로그가 찍혀 다른 유의미한 로그들을 찾기 어려워진다는 단점이 있음 -> lazy를 적용하려고 시도 ->현재 구현된 방식은(과제 요구사항) v-model이 아니라 v-bind와 v-on으로 구현, 때문에 .lazy로 검색이 완료된 후 로그가 남는 방식으로 구현하기 쉽지 않음. 또한 사용자 경험 측면에서도 검색어를 타이핑할 때마다 바로바로 카드가 걸러지는게 좋다(추후 구현될 기능). -> 때문에 debounceTimer를 사용함(.lazy를 쓰려고 시도했으나 막혀서 클로드에 물어보고 이 방식을 알게됨. 예제를 통해 사용방식을 학습한 후 적용)

### 4. 검색 결과 표시

위에서 만들었던 filteredWeatherList를 참고해 v-for로 카드를 만들게 하면 구현되는 기능.

하지만 데이터가 없을 때 검색 결과가 일치하는 도시가 없다는 안내를 하는 기능을 구현되지 않음-> 정확히 어떤 개념을 써야할지는 모르겠어서 가능한 방식과 그 때 우려되는 점을 클로드에 질문

프롬프트:
이걸로 검색어랑 동일한 데이터를 출력하는건 구현했는데 일치하는 검색어가 없을 때, 즉 filteredWeatherList가 비어있을 때 검색 결과가 일치하는 도시가 없다고 안내하는 기능도 구현해야되는데 이건 어떤 기능을 써야되지? v-if 를 통해서 뭔가를 하기엔 조건으로 달 수 있는 변수? 가없는 것 같은데 예를 들어 화면에 표시된 카드가 없을때 어떤 메세지가 떠야한다와 같은

답변: v-if에 filteredWeatherList.length를 조건으로 쓰면 된다.

# 과제 (178pg)

우선 아래와 같이 각 컴포넌트를 새로 만든 후 전체적인 틀을 먼저 만들었다.

최상위 컴포넌트 -> 과제1.vue
┌──────────────────────────────────────────┐
│ WeatherParent.vue │
│ ┌─────────────────────────────────────┐ │
│ │ BaseDashboardCard.vue │ │
│ │ ┌───────────────────────────────┐ │ │
│ │ │ SearchBar.vue │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ └───────────────────────────────┘ │ │
│ │ ┌───────────────────────────────┐ │ │
│ │ │ WeatherCard.vue │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ │ │ │ │
│ │ └───────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘

이후 우선적으로 이전 과제에서 동작한 기능들이 모두 수행되도록 기능을 우선적으로 구현하고 이후 요구사항을 채워가는 식으로 진행함.

WeatherParent.vue -> 모든 반응형 데이터를 관리/자식컴포넌트인 BaseDashboardCard.vue에 전달해야함. 하지만 구조상
<template>
  <div class="BaseDashboardCard">
    베이스 대시보드입니다.
    <BaseDashboardCard></BaseDashboardCard>
    <!--  <BaseDashboardCard></BaseDashboardCard>
  <div class="status-bar">{{ selectedCityInfo }}</div>-->
  </div>
</template>

위와 같이 짜여 props로 두번 주입해야하는 props drillling이 발생-> 요구사항에서 slot으로 구현하라는 이유가 여기서 발생

->BaseDashboardCard에 SearchBar과 WeatherCard를 끼워넣을 슬롯만 이름을 지정하여 구성해놓고 WeatherParent에 BaseDashboardCard, SearchBar, WeatherCard를 모두 임포트한 후

<template>
  <BaseDashboardCard>
    <template v-slot:SearchBar>
      <SearchBar />
    </template>
    <template v-slot:WeatherCard>
      <WeatherCard />
    </template>
  </BaseDashboardCard>
</template>

이런 식으로 처리하면 props를 두번 주입할 필요 없이 바로 Parent에서 SearchBar과 WeatherCard에 데이터를 넘길 수 있음.

## 이후 props&emit를 설정하며 발생한 트러블슈팅 요약

## 1. "emit에 부모 데이터를 인자로 넣어서 업데이트하면, 그걸로 부모 데이터가 바뀌나?"

**직접 세우신 가설**: emit 함수 인자에 값을 넣어서 호출하면 그 자체로 부모 데이터가 갱신될 것이다.

**결과**: 틀린 가설이었어요. `emit`은 "이벤트 발생 신호"만 쏘는 것이고, 실제 데이터 갱신은 부모가 `@이벤트명="변수 = $event"`처럼 **별도로 받아서 처리하는 코드를 써놔야만** 일어난다는 걸 확인하셨습니다.

## 2. "searchQuery를 받아서, input 이벤트 시 새 값으로 바뀌고 그걸 돌려주는 거 아니야?"

**직접 세우신 가설**: `props.searchQuery`가 사용자의 타이핑에 따라 자동으로 최신값으로 갱신될 것이고, 그걸 그대로 emit하면 된다.

**결과**: 절반만 맞고 절반은 틀렸던 케이스예요. "새 값을 부모에게 돌려준다"는 흐름 자체는 정확했지만, **`props.searchQuery`는 부모가 마지막으로 내려준 값에 머물러 있을 뿐, 사용자가 타이핑한다고 자동으로 안 바뀐다**는 걸 발견하셨고, 실제 최신 입력값은 `event.target.value`(이벤트 객체)에서 꺼내야 한다는 결론에 스스로 도달하셨습니다.

## 3. "input으로 받은 값은 자동으로 value로 바뀌는 거야?"

**직접 하신 질문**: `$event.target.value`라는 문법이 어디서 그 값을 가져오는지 원리를 궁금해하심.

**확인된 내용**: 이건 Vue가 아니라 **브라우저(HTML `<input>` 태그) 자체의 기본 동작**이라는 걸 짚어드렸고, `.value`가 사용자 입력을 자동으로 담고 있다는 브라우저 레벨의 동작 원리를 정확히 이해하셨습니다.

## 4. "emit로 데이터를 올리면 부모에서는 아무 일도 안 일어나고, $event로 부모가 추가 실행해야 갱신되는 거지?"

**직접 세우신 결론**: 여러 번의 시행착오(1번 항목) 끝에, "emit은 신호만 보내고, 실제 갱신은 부모의 몫"이라는 정확한 인과관계를 스스로 재구성해서 질문하셨어요.

**결과**: 정확히 맞았습니다. 처음 1번 질문에서는 "emit이 곧 갱신"이라고 생각하셨다가, 여러 트러블슈팅을 거치며 "emit=신호, 부모의 리스너 코드=실제 갱신"이라는 올바른 모델로 스스로 수정하신 과정이었어요.

## 5. "그 카드의 도시 이름을 반환하려면 지금처럼 쓰는 게 맞겠네? 이벤트 객체로는 도시 이름에 접근할 방법이 없고?"

**직접 세우신 가설**: `@click="clickCard(item.name)"`처럼 데이터를 직접 넘기는 지금 방식이 맞고, 이벤트 객체(`MouseEvent`) 안에는 애초에 "도시 이름" 같은 애플리케이션 데이터가 들어있지 않을 것이다.

**결과**: 정확했습니다. 이벤트 객체는 브라우저 차원의 "어디를 클릭했는지" 정보만 담고, `item.name` 같은 Vue 데이터는 별도로 함수 인자에 직접 넘겨야 한다는 걸 정확히 짚으셨어요. `event.target.dataset`을 통한 우회 방법이 이론상 있긴 하지만, Vue에서는 지금 방식이 표준이라는 것도 확인하셨습니다.

## 6. "item을 통째로 부모로 올리고, 부모에서 `$event.value.name`으로 접근 가능한지?"

**직접 세우신 가설**: emit으로 객체 전체를 올리면, 부모에서 `$event`를 통해 그 객체 속성에 접근할 수 있을 것이다.

**결과**: 흐름 자체(item 전체를 emit해서 부모가 `$event`로 접근)는 정확했지만, `.value`를 붙이신 부분만 수정이 필요했어요. `$event`는 `ref`가 아니라 emit이 넘긴 값 그 자체라서 `.value` 없이 `$event.name`으로 바로 접근해야 한다는 걸 확인하셨습니다.

## 전체적으로 보이는 학습 패턴

질문들을 순서대로 보면, **"emit이 곧 데이터 변경이다"라는 초기 오해(1번)에서 출발해서, 여러 시행착오를 거치며 "emit=신호, 실제 처리=부모의 리스너 코드"라는 정확한 모델로 스스로 수정해나가신 과정**이 뚜렷하게 보여요. 특히 4번, 5번, 6번 질문에서는 이미 스스로 정확한 답에 근접한 가설을 세우고 "이게 맞는지" 확인받는 식으로 질문 패턴이 바뀌셨는데, 이건 emit의 "신호 전달"이라는 본질과 `.value`가 필요한 대상(ref)과 필요 없는 대상(순수 값)을 구분하는 감각을 꽤 탄탄하게 잡으신 것으로 보입니다.

### 4번 요구사항까지 기능을 구현 후 style만 클로드의 도움으로 코드를 작성함.

# 과제 (196pg)

router의 index.js에 views에 존재하는 4개의 파일을 경로로 지정, 이 중 notfoundview는 지정되지 않은 경로로 접근 시 라우팅해야하는 파일이므로 와일드카드(_)를 이용해 설정->Router4에서 유효하지 않은 문법이라 /:pathMatch(._)*로 다시 설정->*만 사용했을 땐 어떤 경로로 적든 다 빈 화면이였지만 문법 수정 후 정해진 경로로 접근시 원하는 page가 노출되었고 정의되지 않은 경로로 접근 시 모두 NotFoundView화면으로 라우팅됨을 확인함.

다음으로 라우터를 임포트해 네비게이션 바를 추가하였고 기존 코드에서 RouterView를 이용해 의도에 맞게끔 라우팅 될 수 있도록 설정함. 이후 상세보기 버튼 클릭시 router.push로 개별 상세페이지를 만드려고 진행 중 경로로 푸시했지만 정의되지 않은 url로 notfoundview로 이동하는 현상을 확인함->만들어낸 url에 맞게 라우터 경로를 지정해줘야하는데 문제는 mock객체가 현재는 6개로 6개의 경로를 수동으로 지정해야한다는 점, 이후 mock객체가 많아지거나 database와 연동된다면 모든 url을 라우터의 경로로 지정할 수 없음을 깨달음->과제 요구사항에 작성되어있던 동적라우팅의 필요성이 체감되는 순감임.

## 동적라우팅을 이해하기 위한 클로드와의 대화

### 1. 기본 개념

- **동적 라우팅**: URL의 특정 부분을 고정된 문자열이 아니라 "변할 수 있는 값(변수)"으로 취급해서, 그 값에 따라 하나의 컴포넌트가 서로 다른 내용을 보여주게 만드는 방식
- 라우트 정의 예시: `{ path: '/weather/:id', component: WeatherDetailView }`
  - `:id`는 "가변 자리" — 실제 URL에서 무엇이 오든(`city_01`, `city_02` 등) 이 라우트 하나가 전부 받아냄
- **정적 라우팅과의 차이**
  - 정적 라우팅: URL이 완전히 고정, 한 URL엔 딱 하나의 고정된 화면만 연결 (`/about` → `AboutView`)
  - 동적 라우팅: 경로의 "패턴"만 맞으면, 그 안의 실제 값이 무엇이든 같은 컴포넌트로 연결
- **필요성**
  - 정적 라우팅만 쓰면 데이터 개수(도시 수 등)만큼 라우트와 컴포넌트 파일을 전부 따로 만들어야 함 → 데이터가 많아지면 물리적으로 불가능하고 심각한 중복 발생
  - 동적 라우팅을 쓰면 컴포넌트 파일이 하나만 있어도, 그 안에서 URL의 `:id` 값을 읽어와 대응하는 데이터를 찾아 보여주는 방식으로 전부 처리 가능
  - 부가 효과: URL 자체가 "지금 보여줄 대상이 무엇인지"를 담는 정보 전달 수단이 되어, 새로고침이나 링크 공유 시에도 동일한 화면 재현 가능

### 2. 내가 했던 오해와 그에 대한 대답

#### 오해: "URL마다 각각 다른 Vue 파일이 있어야 하는 것 아니야?"

- **오해의 내용**: 동적 라우팅으로 URL이 여러 갈래로 나뉘면(`/weather/city_01`, `/weather/city_02` 등), 그 URL 개수만큼 각각 대응하는 Vue 파일이 따로 있어야 한다고 생각함
- **대답**: 이 전제는 정적 라우팅에서만 성립함. 동적 라우팅에서는 URL이 몇 개로 갈리든 Vue 파일은 정확히 하나만 있으면 됨
  - 라우터가 하는 일: "이 패턴에 맞는 URL이면, 정해진 컴포넌트 하나를 화면에 그려라"까지만 담당 (구체적인 `id` 값 자체는 신경 쓰지 않음)
  - 컴포넌트가 하는 일: 자기 자신이 렌더링된 후, `useRoute()`로 "지금 나를 그리게 만든 URL에 실제로 뭐가 들어있었는지"를 스스로 조회하고, 그 값에 맞는 데이터를 찾아 화면에 표시
  - 즉 라우터(패턴 매칭 → 컴포넌트 선택)와 컴포넌트(구체적 값 조회 → 데이터 매칭)의 역할이 두 단계로 분리되어 있음

## 3. 내가 스스로 정의한 동적 라우팅의 개념

: "약간 함수 같은 개념이네?"

> 동적 라우팅은 URL을 함수 호출처럼, `:id` 부분을 함수의 매개변수처럼 취급해서, 하나의 컴포넌트(=함수 코드)가 넘어오는 값에 따라 다른 결과(화면)를 보여주게 만드는 구조다.

해당 이해를 바탕으로 index.js에 새로운 동적라우팅을 설정하였고 이 라우팅시 연결될 WeatherDetialView를 작성함
초기 버전: {path: '/detail',name: 'detail',component: DetailView,},
수정 버전: { path: '/weather/:id', name: 'weather-detail', component: WeatherDetailView },
->다음과 같이 :id로 매핑될 수 있도록 경로설정 및 해당 패턴을 가지는 모든 url을 WeatherDetailView와 연결

라우팅 관련 기능(동적 라우트, Catch all, Programmatic Navigation, active 클래스 활용)이 서로 독립적인 게 아니라 하나의 라우터 설정을 중심으로 여러 곳에서 재사용되는 구조라는 걸 체감함. 특히 router.push를 상세보기 이동과 "홈으로 돌아가기" 양쪽에 동일한 패턴으로 재사용한 부분에서, 함수(라우트 이동 로직)를 한 번 정확히 이해하고 나면 유사한 상황에 반복 적용이 쉬워진다는 걸 느낌.

#과제 (212pg)

먼저 main.js를 확인했다(pinia임포트 됐는지) -> stores/configStore.js를 먼저 작성했다.(computed로 화씨 섭씨 변환될 수 있게 구현) -> 다음으로 실제 토글러파일을 작성했다.configStore를 useConfigStore()를 통해 생성한 후 메서드를 사용해 진행->최상위에 작성한 토글러 파일을 사용할 수 있도록 작성->단위변환이 필요한 파일에서 store를 이용할 수 있도록 코드 수정
결론적으로 Pinia는 props/emit(부모-자식 관계)로는 전달이 어려운, 서로 관계없는 여러 컴포넌트가 공유해야 하는 상태를 한 곳(store)에 모아 관리하는 도구였다. 사용하려면 `main.js`에 `app.use(createPinia())`로 등록한 뒤, 각 컴포넌트에서 `useXxxStore()`를 호출해 인스턴스를 받아 써야 한다.
해당 과제에선 state는 store.속성명으로 바로 읽었고, 구조분해할 땐 반응성이 끊기지 않게 `storeToRefs()`를 써야 하며, 변경은 가급적 actions를 통해서만 한다.
getters/변환 로직 사용 시 판정 기준(원본 값)과 화면 표시용 변환 값을 혼동하지 않아야 하고, store 파일 생성과 import는 별개 작업이므로 경로·파일 존재 여부를 항상 확인해야 한다.

#과제 (230pg)

먼저 axios를 설치한 후 OpenWeatherMap에 가입하여 API Key를 발급받았다. -> .env파일을 생성해 api키를 보호하며 명시해 두었다. ->src의 하위컴포넌트로 api를 통해 데이터를 불러오는 컴포넌트를 하나 새로 생성했다.(weatherApi/js) -> WeatherParent.vue/WeatherDetailView.vue에서 mock data를 실제 api 응답으로 교체했다.

## 추가로 적용한 것

3시간, 5일 단위의 날씨 예측, 대기질 확인 배지를 추가했다. 때문에 기존 weatherApi.js에 3개의 함수를 추가했다(기간 예보 관련, 대기질 관련, 도시를 위경도로 반환하는 함수)

주의할 점->.env를 통해 api 보안을 진행할 때 api키는 ""로 감싸지 않고 앞뒤 공백도 없이 key만 입력해야한다.(따옴표나 공백도 키로 인식하기 때문)/따옴표로 감싸서 오류가 발생했다

#과제 (249pg)
먼저 element-plus를 설치한 후 main.js에 사용할 라이브러리로 임포트한다. ->우리가 사용한 건 Element Plus이고 해당 사이트에서 사용할 요소와 코드문법을 확인할 수 있다. ->나는 SearchBar에 el-input을, WeatherCard.vue에 el-card, el-tag, el-button을, UnitToggler에 el-button을 적용했다.->이 과정에서 WeatherCard.vue에 적용한 el-tag는 원래 코드에서처럼 status를 클래스로 나누어 클래스별로 표현하는 형식이 아니라 미리 정해둔 5가지의 상태(success, warning, danger, info, primary)에 맞게 스타일이 달라지는 형태기때문에 기존 v-if로 판정과 표현할 클래스를 동시에 구분하던 형태에서 판정 후 타입을 반환하는 함수를 정의하고 그 함수를 통해 상태를 결정하는 방식으로 로직이 분리되었다.

#과제 (274pg)
우선 npm run lint를 이용해 에러를 잡았다. 총 34개의 에러가 발생했고 이는 모두 코드챌린지과정에서 생긴 오류였다.(파일이름을 한 단어로 지은 것, 사용하지 않는 변수를 임포트 한 것) -> 이는 실습과제와는 무관하고 전부 고치는데 드는 시간 소요가 컸기에 그냥 무시하고 과제를 진행했다.

실제 배포 전 클로드의 도움으로 전체적인 코드의 스타일을 더 전문적으로 보일 수 있게 수정했다.
