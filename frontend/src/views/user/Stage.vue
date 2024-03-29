<script setup>
import { onMounted, inject, ref, computed, onBeforeUnmount } from 'vue'
import { getReverseColor } from '../../composable/common';
import Controller from '@/components/Controller.vue';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Polaroid from '../../components/Polaroid.vue';
import PolaroidText from '../../components/PolaroidText.vue';

const imgLoaded = ref(false)
const data = inject('csvData', [])
const nowHeroIndex = ref(0)
const heroData = computed(()=>{
  return reorderData.value[nowHeroIndex.value]
})
const bodyBgColor = computed(()=>{
  if (heroData.value){
    return heroData.value.main_color
  }
  return {}
})
const bodyTextColor = computed(()=>{
  return getReverseColor(bodyBgColor.value)
})

// 重設圖片載入狀態，已顯示 spinner
function resetImgLoaded(){
  imgLoaded.value = false
}

// 依照時間排列
const reorderData = computed(() => {
  // 測試時先篩選出確定有顏色的
  if (shuffleNum.value){
    return data.value.filter(d => d['main_color']).sort(() => Math.random() - shuffleNum.value)
  }else{
    return data.value.filter(d => d['main_color']).sort(
      (a, b) => {
        return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
      })
  }
})

// 依照照片設定背景色和文字顏色
const backgroundStyle = computed(() => {
  if (bodyBgColor) {
    return {
      backgroundColor: `hsl(${bodyBgColor.value.h},${bodyBgColor.value.s}%,${bodyBgColor.value.l}%)`,
      color: `hsl(${bodyTextColor.value.h},${bodyTextColor.value.s}%,${bodyTextColor.value.l}%)`,
    };
  }
  return {}
})

const backgroundStyleReverse = computed(() => {
  if (bodyBgColor) {
    return {
      backgroundColor: `hsl(${bodyTextColor.value.h},${bodyTextColor.value.s}%,${bodyTextColor.value.l}%)`,
      color: `hsl(${bodyBgColor.value.h},${bodyBgColor.value.s}%,${bodyBgColor.value.l}%)`,
    };
  }
  return {}
})

// 控制
function showNext(){
  resetImgLoaded()
  if (nowHeroIndex.value == reorderData.value.length-1){
    nowHeroIndex.value = 0
  }else{
    nowHeroIndex.value++
  }
}

function showPrev(){
  resetImgLoaded()
  if (nowHeroIndex.value == 0){
    nowHeroIndex.value = reorderData.value.length-1
  }else{
    nowHeroIndex.value --
  }
}

// 自動播放
let timer
const autoPlaying = ref(false)
const timeLeft = ref(10)

function startPlaying(){
  autoPlaying.value = true
  timer = window.setInterval(()=>{
    if (timeLeft.value >= 1){
      timeLeft.value --
    }else{
      showNext()
      timeLeft.value = 10
    }
  }, 1000)
}

function stopPlaying(){
  autoPlaying.value = false
  timeLeft.value = 10
  clearInterval(timer)
}

// 隨機排序
const shuffleNum = ref(undefined)
function shuffle() {
  resetImgLoaded()
  shuffleNum.value = Math.random()
}

onMounted(() => {
  startPlaying()
})

onBeforeUnmount(() => {
  clearInterval(timer)
})
</script>

<template>
  <main v-if="heroData" :style="backgroundStyle" class="transition">
    <section class="container min-vh-100 d-flex flex-column flex-lg-row align-items-center justify-content-start justify-content-lg-center gap-4 gap-lg-5 position-relative pt-5 pb-8 pb-lg-5">
      <polaroid :photo="heroData" :photo-loaded="imgLoaded" :bg-style="backgroundStyle"></polaroid>
      <polaroid-text :photo="heroData" :bg-style="backgroundStyleReverse"></polaroid-text>
    </section>
    <!-- Controller -->
    <controller :theme="backgroundStyle"
      :auto-playing="autoPlaying"
      :time-left="timeLeft"
      @start-playing="startPlaying"
      @stop-playing="stopPlaying"
      @show-next="showNext"
      @show-prev="showPrev"
      @shuffle="shuffle"></controller>
    <!-- Bookmark -->
    <bookmark :theme="backgroundStyle"
    class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
    <!-- Nav -->
    <navigator :theme="backgroundStyle"></navigator>
  </main>
</template>