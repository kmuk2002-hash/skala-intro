<script setup>
import slotchild from './slotchild.vue'
</script>

<template>
  <div class="practice-section">
    <h2>Default Slot 레이아웃 주입 실습</h2>
    <slotchild>
      <p>단순한 텍스트 문장을 주입합니다.</p>
    </slotchild>
    <slotchild>
      <h2 style="color: #e74c3c">🔥 경고 상태</h2>
      <button>확인</button>
    </slotchild>
    <slotchild></slotchild>
  </div>
</template>
