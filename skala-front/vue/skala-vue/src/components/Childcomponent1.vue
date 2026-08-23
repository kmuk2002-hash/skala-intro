<script setup>
const emit = defineEmits(['childEvent'])

const sendToParent = () => {
  emit('childEvent', '안녕하세요, 부모 컴포넌트!')
}
</script>

<template>
  <button @click="sendToParent">부모에게 메세지 보내기</button>
</template>
