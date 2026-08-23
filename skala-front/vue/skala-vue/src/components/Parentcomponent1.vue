<script setup>
import { ref } from 'vue'
import Childcomponent from './Childcomponent1.vue'

const handleChildEvent = (message) => {
  console.log('자식으로부터 받은 메세지:', message)
}
</script>

<template>
  <Childcomponent @childEvent="handleChildEvent" />
</template>
