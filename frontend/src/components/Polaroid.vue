<script setup>
import { watch, onMounted, ref } from 'vue';
const props = defineProps(['photoLoaded', 'photo', 'bgStyle'])
const isLoading = ref(true)

watch(() => props.photo, (newPhoto, oldPhoto) => {
  if (newPhoto !== oldPhoto) {
    isLoading.value = true;
  }
});

const imageElement = ref(null)
onMounted(() => {
  imageElement.value.onload = () => {
    // console.log("Image loaded")
    isLoading.value = false;
  };
});
</script>
<template>
    <div class="polaroid hero d-flex flex-column text-dark shadow-lg">
        <div class="ratio ratio-1x1">
          <img
            ref="imageElement"
            :src="photo.url_google"
            alt=""
            class="d-none">
          <div
            v-if="!isLoading"
            class="overflow-hidden">
            <img
              :src="photo.url_google"
              alt=""
              class="w-100 h-100 object-fit-cover"
              style="object-position: center;">
          </div>
          <div
            v-else
            class="d-flex justify-content-center align-items-center">
            <div
              class="spinner-border"
              role="status" />
          </div>
        </div>
        <div>
          <p
            class="d-flex justify-content-between align-items-center border-bottom p-2 ff-serif transition mb-0"
            :style="bgStyle">
            <span class="ps-2">{{ photo.date + ' ' + photo.time }}</span>
          </p>
        </div>
    </div>
</template>