<script setup>
import { computed, inject, ref, onBeforeMount } from 'vue';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Polaroid from '@/components/Polaroid.vue';
import PolaroidText from '@/components/PolaroidText.vue';

const data = inject('csvData', [])
const nowPhoto = ref(undefined)

// const route = useRoute()
onBeforeRouteUpdate((to, form) =>{
    const nowPhotoName = JSON.parse(to.query.photo)
    nowPhoto.value = data.value.find((d) => d.name === nowPhotoName);
})

onBeforeMount(()=>{
  const route = useRoute()
  if (JSON.stringify(route.query) !== '{}'){
    const nowPhotoName = JSON.parse(route.query.photo)
    nowPhoto.value = data.value.find((d) => d.name === nowPhotoName);
  }
})

</script>
<template>
    <div>
        <section class="vh-100 bg-silver fixed-top d-flex justify-content-center align-items-center gap-5"
        v-if="nowPhoto">
            <polaroid :photo="nowPhoto"></polaroid>
            <polaroid-text :photo="nowPhoto" :bg-style="{'background-color': '#232323', 'color': '#f6f6f6'}"></polaroid-text>
        </section>
        <!-- Bookmark -->
        <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
        <!-- Nav -->
        <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
    </div>
</template>