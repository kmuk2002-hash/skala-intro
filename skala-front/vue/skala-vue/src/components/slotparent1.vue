<script setup>
import slotchild1 from './slotchild1.vue'
</script>

<template>
  <div class="parctice-section">
    <h2>Named Slot 주입 실습</h2>
    <slotchild1>
      <template v-slot:header>
        <h3>여긴 named헤더 영역</h3>
      </template>
      <p>dfadsf</p>
    </slotchild1>
  </div>
</template>
