<script setup>
import { onMounted, inject, ref, computed, onBeforeUnmount } from 'vue'
import { getReverseColor } from '../../composable/common';
import Controller from '@/components/Controller.vue';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Polaroid from '../../components/Polaroid.vue';
import PolaroidText from '../../components/PolaroidText.vue';

const data = inject('csvData', []);
const nowHeroIndex = ref(0);
const heroData = computed(()=>{
  return orderedData.value[nowHeroIndex.value];
})
const bodyBgColor = computed(()=>{
  if (heroData.value){
    return heroData.value.main_color;
  }
  return {};
})
const bodyTextColor = computed(()=>{
  return getReverseColor(bodyBgColor.value);
})

// 依照時間排列
const orderedData = computed(() => {
  return data.value
    .filter(d => d['main_color'])
    .sort((a, b) => {
      return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1));
    });
})

// 依照照片設定背景色和文字顏色
const backgroundStyle = computed(() => {
  if (bodyBgColor) {
    return {
      backgroundColor: `hsl(${bodyBgColor.value.h},${bodyBgColor.value.s}%,${bodyBgColor.value.l}%)`,
      color: `hsl(${bodyTextColor.value.h},${bodyTextColor.value.s}%,${bodyTextColor.value.l}%)`,
    };
  }
  return {};
})

const backgroundStyleReverse = computed(() => {
  if (bodyBgColor) {
    return {
      backgroundColor: `hsl(${bodyTextColor.value.h},${bodyTextColor.value.s}%,${bodyTextColor.value.l}%)`,
      color: `hsl(${bodyBgColor.value.h},${bodyBgColor.value.s}%,${bodyBgColor.value.l}%)`,
    };
  }
  return {};
})

// 控制
function showNext(){
  if (nowHeroIndex.value == orderedData.value.length - 1){
    nowHeroIndex.value = 0;
  } else {
    nowHeroIndex.value ++;
  }
}

function showPrev(){
  if (nowHeroIndex.value == 0){
    nowHeroIndex.value = orderedData.value.length - 1;
  } else {
    nowHeroIndex.value --;
  }
}

// 自動播放
let timer;
const CHANGE_INTERVAL = 15;
const isAutoPlay = ref(false);
const timeLeft = ref(CHANGE_INTERVAL);

function startPlaying(){
  isAutoPlay.value = true;

  timer = setInterval(() => {
    if (timeLeft.value >= 1){
      timeLeft.value --;
    } else {
      showNext();
      timeLeft.value = CHANGE_INTERVAL;
    }
  }, 1000);
}

function stopPlaying(){
  isAutoPlay.value = false;
  clearInterval(timer);
}

function shuffle() {
  nowHeroIndex.value = Math.round(orderedData.value.length * Math.random());
}

onMounted(() => {
  startPlaying();
})

onBeforeUnmount(() => {
  clearInterval(timer);
})
</script>

<template>
  <main
    v-if="heroData"
    class="transition"
    :style="backgroundStyle">
    <section
      class="container min-vh-100 d-flex flex-column flex-lg-row align-items-center justify-content-start justify-content-lg-center gap-4 gap-lg-5 position-relative pt-5 pb-8 pb-lg-5">
      <polaroid
        :photo="heroData"
        :bg-style="backgroundStyle" />
      <polaroid-text
        :photo="heroData"
        :bg-style="backgroundStyleReverse" />
    </section>
    <!-- Controller -->
    <controller
      :theme="backgroundStyle"
      :is-auto-play="isAutoPlay"
      :time-left="timeLeft"
      @start-playing="startPlaying"
      @stop-playing="stopPlaying"
      @show-next="showNext"
      @show-prev="showPrev"
      @shuffle="shuffle" />
    <!-- Bookmark -->
    <bookmark
      :theme="backgroundStyle"
      class="position-fixed top-0 d-flex align-items-center gap-1" />
    <!-- Nav -->
    <navigator :theme="backgroundStyle" />
  </main>
</template>