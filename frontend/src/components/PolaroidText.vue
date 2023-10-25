<script setup>
import ColorSwatch from '@/components/ColorSwatch.vue';
import { hsl2Hex } from '@/composable/common';
const props = defineProps(['photo', 'bgStyle'])
</script>

<template>
    <div id="Sec_text">
        <p class="d-flex gap-2 flex-wrap">
          <span v-for="place of photo.places" class="rounded-pill p-2 transition"
          :style="bgStyle">#{{
            place }}</span>
        </p>
        <p class="mb-0 mt-3">{{ photo.description }}</p>
        <div class="d-flex flex-wrap gap-2 mt-5 mt-lg-6 z-1">
            <color-swatch
            :color-hsl="color"
            :label="hsl2Hex(color.h, color.s, color.l)"
            v-for="color of photo.colors"></color-swatch>
        </div>
    </div>
</template>

<style scoped>
#Sec_text{
  width: 80%;
  margin-right: auto;
}

@media screen and (min-width: 992px) {
  #Sec_text{
    width: 30vw;
    margin: unset;
  }
}
</style>