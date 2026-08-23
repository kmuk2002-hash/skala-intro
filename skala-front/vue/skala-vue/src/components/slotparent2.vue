<script setup>
import slotchild from './slotchild2.vue'
</script>

<template>
  <div class="practice-section">
    <h2>scoped slot 주입 실습</h2>
    <h3>상위 컴포넌트(parent)</h3>
    <slotchild v-slot="slotBag">
      <div class="display-panel">
        <p>알림메세지: {{ slotBag.text }}</p>
        <p>접속자 수: {{ slotBag.count }}</p>
      </div>
    </slotchild>
    <slotchild></slotchild>
  </div>
</template>
