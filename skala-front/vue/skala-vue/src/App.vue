<script setup>
import SampleOne from './components/SampleOne.vue'
import SampleTwo from './components/SampleTwo.vue'
import refExample from './components/ref() Example.vue'
import reacExample from './components/reactive() Example.vue'
import computed from './components/computedexample.vue'
import watch from './components/watchexample.vue'
import watch2 from './components/watchexample2.vue'
import lifecycle from './components/lifecyclehookexample.vue'
import parent from './components/Parentcomponent.vue'
import child from './components/Childcomponent.vue'
import parent1 from './components/Parentcomponent1.vue'
import child1 from './components/Childcomponent1.vue'
import parent2 from './components/Parentcomponent2.vue'
import child2 from './components/Childcomponent2.vue'
import parent3 from './components/Parentcomponent3.vue'
import child3 from './components/Childcomponent3.vue'
import slotparent from './components/slotparent.vue'
import slotchild from './components/slotchild.vue'
import slotparent1 from './components/slotparent1.vue'
import slotchild1 from './components/slotchild1.vue'
import slotparent2 from './components/slotparent2.vue'
import slotchild2 from './components/slotchild2.vue'
//첫번째 v-html실습
const rawHtmlData =
  '이 글자는 <span style="color: red; font-weight: bold;">빨간색 굵은 글자</span>이다'
//첫번째 v-html실습 끝
//두번째 v-html실습
import { ref } from 'vue'

const inputValue = ref('')
const message = ref('')

function showMessage() {
  message.value = inputValue.value
}
//두번째 v-html실습 끝
//세번째 v-text 실습
const content = '안녕하세요! <span style = "color: red;"">Skala-Vue</span> 강의입니다.'
//세번째 v-text 실습끝
//네번째 v-bind 실습
const dynamicUrl = 'https://www.naver.com'
const logoImgSrc = 'https://vuejs.org/images/logo.png'
const isButtonDisabled = ref(true)
//네번째 v-bind 실습끝
//다섯번째 v-bind 실습
const isWarning = ref(false)
const themeClass = ref('bg-dark')
//다섯번째 v-bind 실습끝
//여섯번째 v-bind 실습끝
const textColor = ref('purple')
const boxWidth = ref(150)
const baseBoxStyle = ref({
  backgroundColor: '#42b883',
  height: '100px',
  transition: 'all 0.3s ease',
})
//여섯번째 v-bind 실습끝
//일곱번째 v-if 실습끝
const isLogged = ref(false)
const score = ref(85)
//일곱번째 v-if 실습끝
//여덟번째 v-show 실습
const isVisible = ref(true)
//여덟번째 v-show 실습끝
//아홉번째 v-show 실습
const fruits = ref(['사과', '바나나', '딸기'])
const user = ref({
  name: '홍길동',
  age: 25,
  role: '개발자',
})
const items = ref([
  { id: 'prod_101', name: '아이폰' },
  { id: 'prod_102', name: '갤럭시' },
])
//아홉번째 v-show 실습끝
//열번째 v-on 실습끝
const count = ref(0)
const showAlert = () => {
  alert('함수가 성공적으로 호출되었습니다.')
}
//열번째 v-on 실습끝
//열한번째 v-on 실습
const position = ref('')
const tagName = ref('')
const getOnlyEvent = (e) => {
  position.value = `좌표: X=${e.clientX} Y=${e.clientY}`
}
const getWidthParam = (name, e) => {
  tagName.value = `대상: ${name} / 클릭된 태그: ${e.target.tagName}`
}
//열한번째 v-on 실습끝
//열두번째 event modifier 실습
const handleLink = () => {
  alert('수식어 덕분에 네이버로 이동하지 않고 함수만 실행됩니다.')
}

const handleBox = () => {
  alert('부모 박스가 클릭되었습니다.')
}

const handleChild1 = () => {
  alert('1번 자식 클릭')
}

const handleChild2 = () => {
  alert('2번 자식(나만 켜짐) 클릭')
}
//열두번째 event modifier 실습끝
//열세번째 event modifier 실습
const comment = ref('')
const isAgreed = ref(false)
const favoriteFruits = ref([])
const gender = ref('')
const selectedCar = ref('')
//열세번째 event modifier 실습끝
//열네번째 v-model modifiers 실습
const lazyText = ref('')
const age = ref('')
const userEmail = ref('')
const price = ref('')
//열네번째 v-model modifiers 실습끝
</script>

<template>
  <div style="padding: 20px">
    <SampleOne />
    <br />
    <SampleTwo />
    <br />
    <!--첫번째 v-html 실습-->
    <div class="practice-section">
      <h2>v-html 디렉티브 학습</h2>
      <h3>일반 보간법 {{}} 사용 결과:</h3>
      <p>{{ rawHtmlData }}</p>
      <br />
      <h3>v-html 디렉티브 사용 결과:</h3>
      <p v-html="rawHtmlData"></p>
      <br />
    </div>
  </div>
  <!--첫번째 v-html 실습끝-->
  <!--두번째 v-html 실습-->
  <div class="practice-section">
    <h2>v-html XSS 학습</h2>
    <input v-model="inputValue" placeholder="내용을 입력하세요" />
    <button @click="showMessage">확인</button>
    <div v-html="message"></div>
  </div>
  <!--두번째 v-html 실습끝-->
  <!--세번째 v-text 실습-->
  <div class="practice-section">
    <h2>v-text 디렉티브 실습</h2>
    <h3>1)일반 보간법{{}}결과</h3>
    <p>cnffur: {{ content }}</p>
    <br />

    <h3>2) v-text 디렉티브 결과:</h3>
    <p v-text="'출력:' + content"></p>
    <br />

    <h3>v-html 결과 비교:</h3>
    <p v-html="content"></p>
  </div>

  <!--세번째 v-text 실습끝-->
  <!--네번째 v-bind 실습-->
  <div class="practice-section">
    <h2>v-bind 디렉티브 기본 (축약형: 콜론)</h2>
    <h3>1)동적 링크 연결</h3>
    <a :href="dynamicUrl">여기를 클릭하면 네이버로 이동합니다.</a>
    <br />

    <h3>2)동적 이미지 연결</h3>
    <img :src="logoImgSrc" alt="Vue 로고" style="sidth: 100px" />
    <br />

    <h3>3)버튼 비활성화 제어</h3>
    <p>현재 버튼 사용 불가능 상태: {{ isButtonDisabled }}</p>
    <button :disabled="isButtonDisabled">동의해야 클릭할 수 있는 버튼</button>
    <button @click="isButtonDisabled = !isButtonDisabled">위 버튼 잠금 해제/토글하기</button>
    <br />
  </div>
  <!--네번째 v-bind 실습끝-->
  <!--다섯번째 v-bind 실습-->
  <div class="practice-section">
    <h2>v-bind 디렉티브 고급 (클래스 바인딩)</h2>
    <h3>클래스 바인딩 (객체 형식)</h3>
    <p :class="{ 'text-danger': isWarning }">현재 경고 상태: {{ isWarning }}</p>
    <button @click="isWarning = !isWarning">경고 상태 토글</button>
    <br />
    <h3>클래스 바인딩</h3>
    <div :class="[themeClass, isWarning ? 'border-red' : 'border-gray']">
      다중 클래스가 조립된 박스 구역입니다.
    </div>
  </div>

  <!--다섯번째 v-bind 실습끝-->
  <!--여섯번째 v-bind 실습-->
  <div class="practice-section">
    <h2>v-bind 디렉티브 고급(스타일 바인딩)</h2>
    <h3>1)인라인 스타일 변수 조작 (객체 형식)</h3>
    <p :style="{ color: textColor, fontWeight: 'bold' }">이 글자의 색상은 실시간으로 바뀝니다.</p>
    <button @click="textColor = textColor === 'purple' ? 'blue' : 'purple'">글자 색상 토글</button>
    <br />

    <h3>2) 다중 스타일 객체 조립 (배열 형식)</h3>
    <label>박스 가로 크기(px):</label>
    <input type="number" v-model="boxWidth" step="50" />
    <br />
    <div :style="[baseBoxStyle, { width: boxWidth + 'px' }]">
      <p style="color: white; padding: 10px; text-align: center">
        가로 크기: {{ boxWidth }}px 박스
      </p>
    </div>
  </div>
  <!--여섯번째 v-bind 실습끝-->
  <!--일곱번째 v-if 실습-->
  <div class="parctice-section">
    <h2>v-if 디렉티브 학습</h2>
    <h3>1) 기본 로그인 상태 스위치</h3>
    <p v-if="isLogged">환영합니다! 회원 전용 화면입니다.</p>
    <p v-else>로그인이 필요합니다. 먼저 로그인해 주세요.</p>
    <button @click="isLogged = !isLogged">{{ isLogged ? '로그아웃하기' : '로그인하기' }}</button>
    <br />
    <h3>2)성적별 학점 등급 측정 (다중 조건문)</h3>
    <label>현재 점수 입력:</label>
    <input type="number" v-model="score" min="0" max="100" step="5" />
    <br />
    <div v-if="score >= 90" style="color: green; font-weight: bold">
      합격 등급: A학점 (훌륭합니다!)
    </div>
    <div v-else-if="score >= 80" style="color: blue">합격 등급: B학점 (양호합니다.)</div>
    <div v-else-if="score >= 70" style="color: orange">합격 등급: C학점 (조금 더 분발하세요.)</div>
    <div v-else style="color: red; font-weight: bold">합격 등급: F학점 (재시험 대상입니다.)</div>
  </div>
  <!--일곱번째 v-if 실습끝-->
  <!--여덟번째 v-show 실습끝-->
  <div class="practice-section">
    <h2>v-show 디렉티브 학습</h2>
    <button @click="isVisible = !isVisible">화면 토글하기</button>
    <br />
    <div v-show="isVisible" class="box">
      <p>v-show 상자</p>
      <p>조건이 false가 되면 CSS display: none이 붙습니다.</p>
    </div>
  </div>
  <!--여덟번째 v-show 실습끝-->
  <!--아홉번째 v-for 실습-->
  <div class="practice-section">
    <h2>v-for 디렉티브 학습</h2>
    <h3>1) 배열 랜더링</h3>
    <ul>
      <li v-for="(fruit, index) in fruits" :key="index">{{ index + 1 }}번 과일:{{ fruit }}</li>
    </ul>
    <h3>2)객체 렌더링</h3>
    <ul>
      <li v-for="(value, key, index) in user" :key="key">[{{ index }}] {{ key }}:{{ value }}</li>
    </ul>
    <h3>3) 배열 내 객체 렌더링</h3>
    <ul>
      <li v-for="(item, index) in items" :key="item.id">[{{ index }}] {{ item.name }}</li>
    </ul>
  </div>
  <!--아홉번째 v-for 실습끝-->
  <!--열번째 v-on 실습-->
  <div class="practice-section">
    <h2>v-on 이벤트 핸들링 기초</h2>
    <h3>1) 인라인 연산 처리</h3>
    <p>현재 카운트: {{ count }}</p>
    <button @click="count++">1씩 증가</button>
    <br />
    <h3>2) 스크립트 함수 호출</h3>
    <button @click="showAlert">알림창 띄우기</button>
  </div>
  <!--열번째 v-on 실습끝-->
  <!--열한번째 v-on 실습-->
  <div class="practice-section">
    <h2>v-on 이벤트 객체($event) 활용</h2>
    <p>좌표: {{ position }}</p>
    <p>태그: {{ tagName }}</p>
    <button @click="getOnlyEvent">클릭 좌표 알아내기</button>
    <button @click="getWidthParam('회원A', $event)">회원 정보와 태그 확인</button>
  </div>
  <!--열한번째 v-on 실습끝-->
  <!--열두번째 event modifier 실습끝-->
  <div class="practice-section">
    <h2>이벤트 수식어(Modifiers) 학습</h2>
    <h3>1) .prevent (기본 동작 막기)</h3>
    <a href="https://www.naver.com" @click.prevent="handleLink">네이버 링크</a>
    <br />

    <h3>2) .stop (이벤트 버블링 막기)</h3>
    <div @click="handleBox" style="padding: 20px; background-color: #eee">
      <p>부모 영역 (클릭 시 alert 발동)</p>
      <button @click="handleChild1">버블링 발생 버튼</button>
      <button @click.stop="handleChild2">버블링 차단 버튼</button>
    </div>
  </div>
  <!--열두번째 event modifier 실습끝-->
  <!--열세번째 event modifier 실습-->
  <div class="practice-section">
    <h2>모든 HTML Form 요소와 c-model 매핑</h2>
    <div>
      <h3>1)Textarea (장문 텍스트)</h3>
      <textarea v-model="comment" placeholder="의견을 남겨주세요"></textarea>
      <p>
        데이터 상태: <span>{{ comment }}</span>
      </p>
    </div>
    <div>
      <h3>2)단일 Checkbox (동의 여부)</h3>
      <label> <input type="checkbox" v-model="isAgreed" /> 약관에 동의합니다. </label>
      <p>
        데이터 상태: <span>{{ isAgreed }}</span>
      </p>
    </div>
    <div>
      <h3>3)다중 Checkbox (복수 선택 -> 배열에 저장)</h3>
      <label> <input type="checkbox" value="사과" v-model="favoriteFruits" /> 사과 </label>
      <label> <input type="checkbox" value="바나나" v-model="favoriteFruits" /> 바나나 </label>
      <label> <input type="checkbox" value="딸기" v-model="favoriteFruits" /> 딸기 </label>
      <p>
        데이터 상태 (배열): <span>{{ favoriteFruits }}</span>
      </p>
    </div>
    <div>
      <h3>4)Radio (단일 선택)</h3>
      <label><input type="radio" value="남성" v-model="gender" /> 남성 </label>
      <label><input type="radio" value="여성" v-model="gender" /> 여성 </label>
      <p>
        데이터 상태 (배열): <span>{{ gender }}</span>
      </p>
    </div>
    <div>
      <h3>5) Select (드롭다운 선택)</h3>
      <select v-model="selectedCar">
        <option value="">-- 선택하세요 --</option>
        <option value="tesla">테슬라</option>
        <option value="hyundai">현대자동차</option>
        <option value="bmw">BMW</option>
      </select>
      <p>
        데이터 상태 (배열): <span>{{ selectedCar }}</span>
      </p>
    </div>
  </div>
  <!--열세번째 event modifier 실습끝-->
  <!--열네번째 v-model modifier 실습끝-->
  <div class="practice-section">
    <h2>v-model 수식어ㅓ (Modifiers) 활용</h2>
    <section style="margin-bottom: 20px">
      <h3>1) .lazy수식어 (change 이벤트 시점 반영)</h3>
      <input type="text" v-model.lazy="lazyText" placeholder="입력 후 Enter 또는 외부 클릭" />
      <p>
        실시간이 아닌 확정된 값: <strong>{{ lazyText }}</strong>
      </p>
    </section>

    <section style="margin-bottom: 20px">
      <h3>2) .number 수식어 (Number 타입 자동 형변환)</h3>
      <input type="text" v-model.number="age" placeholder="나이를 입력하세요" />
      <p>
        입력된 값: <strong>{{ age }}</strong>
      </p>
      <p>
        데이터 타입: <strong>{{ typeof age }}</strong>
      </p>
    </section>

    <section style="margin-bottom: 20px">
      <h3>3) .trim 수식어 (양끝 공백 자동 제거)</h3>
      <input type="text" v-model.trim="userEmail" placeholder="앞뒤 공백을 포함해 입력해 보세요" />
      <p>
        공백 제거된 값: <strong>{{ userEmail }}</strong>
      </p>
      <p>
        문자열 길이: <strong>{{ userEmail.length }}</strong>
      </p>
    </section>

    <section style="margin-bottom: 20px">
      <h3>4) .Chaining (수식어 체이닝: .trim.number)</h3>
      <input
        type="text"
        v-model.trim.number="price"
        placeholder="공백과 숫자를 섞어 입력해 보세요"
      />
      <p>
        처리된 값: <strong>{{ price }}</strong>
      </p>
      <p>
        데이터 타입: <strong>{{ typeof price }}</strong>
      </p>
    </section>
  </div>
  <!--열네번째 v-model modifier 실습끝-->
  <div>
    <refExample />
  </div>
  <div>
    <reacExample />
  </div>
  <div><computed /></div>
  <div><watch /></div>
  <div><watch2 /></div>
  <div><lifecycle /></div>
  <div><parent /></div>
  <div><parent1 /></div>
  <div><parent2 /></div>
  <div><parent3 /></div>
  <div><slotparent /></div>
  <div><slotparent1 /></div>
  <div><slotparent2 /></div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
s @media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }

  .text-danger {
    color: red;
    font-weight: bold;
  }
  .bg-dark {
    background-color: #333;
    color: white;
    padding: 15px;
  }
  .border-red {
    border: 3px solid red;
  }
  .border-gray {
    border: 3px solid #ccc;
  }
}
.box {
  padding: 10px;
  margin-top: 5px;
  color: white;
  border-radius: 5px;
  background-color: #3498db; /* 파란색 */
}
</style>
