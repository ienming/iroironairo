<script setup>
import { watch, onMounted, ref } from 'vue';
const props = defineProps(['photo', 'bgStyle']);

const isLoading = ref(true);

watch(() => props.photo, (newPhoto, oldPhoto) => {
  if (newPhoto !== oldPhoto) {
    isLoading.value = true;
  }
});

function hi() {
  isLoading.value = false;
}
</script>

<template>
    <div class="polaroid hero d-flex flex-column text-dark shadow-lg">
        <div class="ratio ratio-1x1">
          <div
            v-show="isLoading"
            class="d-flex justify-content-center align-items-center">
            <div
              class="spinner-border"
              role="status" />
          </div>
          <div
            v-show="!isLoading"
            class="overflow-hidden">
            <img
              :src="photo.url_google"
              :onload="isLoading = false"
              class="w-100 h-100 object-fit-cover"
              style="object-position: center;">
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