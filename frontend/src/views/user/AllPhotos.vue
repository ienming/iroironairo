<script setup>
import { computed } from 'vue';
import { usePhotoStore } from '@/stores/PhotoStore'
const photoStore = usePhotoStore()
const data = photoStore.photos //data is a Reactive object

const dataReordered = computed(()=>{
    return data.filter(d=>d['main_color'])
})
</script>

<template>
    All photos
    <p v-for="d of dataReordered">{{ d }}</p>
</template>