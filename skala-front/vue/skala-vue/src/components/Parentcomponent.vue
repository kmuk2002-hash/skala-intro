<script setup>
import { ref } from 'vue'
import Childcomponent from './Childcomponent.vue'

const selectCityName = ref('수원시 영통구')
const areaCode = ref(103)
</script>

<template>
  <div>
    <Childcomponent :city-name="selectCityName" :area-code="areaCode" />
  </div>
</template>
