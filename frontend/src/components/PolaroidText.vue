<script setup>
import { computed, onMounted, inject, watch, ref } from 'vue';
import ColorSwatch from '@/components/ColorSwatch.vue';
import { hsl2Hex } from '@/composable/common';
import { useRouter } from 'vue-router'
const props = defineProps(['photo', 'bgStyle'])

const data = inject('csvData', [])
const dataOrdered = computed(()=>{
  let arr = data.value.filter(d => d['main_color'])
  arr.sort(
    (a, b) => {
      return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
    })
  return arr
})

// 找出靠近這張照片日期前後的照片
const currentIndex = ref(undefined);
const prevIndex = ref(undefined);
const nextIndex = ref(undefined);

const computeRelatingPhotos = (newPhoto) => {
  const findPosition = (el) => el.name === newPhoto.name;
  currentIndex.value = dataOrdered.value.findIndex(findPosition);
  console.log('Current Index: '+currentIndex.value);

  if (currentIndex.value === 0) {
    prevIndex.value = 0
    nextIndex.value = currentIndex.value + 1;
  } else if (currentIndex.value === dataOrdered.value.length - 1) {
    prevIndex.value = currentIndex.value - 1;
    nextIndex.value = currentIndex.value
  } else {
    prevIndex.value = currentIndex.value - 1;
    nextIndex.value = currentIndex.value + 1;
  }
  console.log("Prev index: "+prevIndex.value)
  console.log("Next index: "+nextIndex.value)
};

const prevPhoto = computed(()=>{
  if (prevIndex.value){
    let photo = JSON.parse(JSON.stringify(dataOrdered.value[prevIndex.value]))
    photo.date = photo.date.replace(/:/g, '/')
    photo.time = photo.time.replace(/:[^:]*$/, '')
    return photo
  }
})

const nextPhoto = computed(()=>{
  if (nextIndex.value){
    let photo = JSON.parse(JSON.stringify(dataOrdered.value[nextIndex.value]))
    photo.date = photo.date.replace(/:/g, '/')
    photo.time = photo.time.replace(/:[^:]*$/, '')
    return photo
  }
})

watch(() => props.photo, computeRelatingPhotos);
onMounted(() => {
  computeRelatingPhotos(props.photo);
});

// Router
const router = useRouter()
function searchByPlace(place){
  console.log("Search by place: "+place)
  router.push({
      path: '/all',
      query: {
          place: JSON.stringify(place)
      },
  })
}
</script>

<template>
    <div id="Sec_text" class="z-1">
        <p class="d-flex gap-2 flex-wrap">
          <span v-for="place of photo.places" class="rounded-pill p-2 transition"
          :style="bgStyle" role="button" @click="searchByPlace(place)">#{{
            place }}</span>
        </p>
        <p class="mb-0 mt-3">{{ photo.description }}</p>
        <div class="d-flex flex-wrap gap-2 mt-5 mt-lg-6 z-1">
            <color-swatch
            :color-hsl="color"
            :label="hsl2Hex(color.h, color.s, color.l)"
            v-for="color of photo.colors"></color-swatch>
        </div>
        <div class="mt-5">
          <p class="mb-2 fw-bold opacity-50">靠近這一天</p>
          <div v-if="prevPhoto" class="d-flex align-items-center justify-content-between opacity-50-hover border-top p-3" role="button"
          :style="{'--bs-border-color': bgStyle.backgroundColor}">
            <span>{{ prevPhoto.date+' '+prevPhoto.time }}</span>
            <span class="opacity-75">#{{ prevPhoto.places[0] }}</span>
          </div>
          <div v-if="nextPhoto" class="d-flex align-items-center justify-content-between opacity-50-hover border-top p-3" role="button"
          :style="{'--bs-border-color': bgStyle.backgroundColor}">
            <span>{{ nextPhoto.date+' '+nextPhoto.time }}</span>
            <span class="opacity-75">#{{ nextPhoto.places[0] }}</span>
          </div>
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