<script setup>
import { onMounted, ref, computed, onBeforeUnmount } from 'vue'
import axios from 'axios'
import colorSwatch from '../../components/colorSwatch.vue';
import controllerManual from '../../components/controllerManual.vue';
import controllerAuto from '../../components/controllerAuto.vue';

const data = ref([])
const heroData = ref(undefined)
const bodyBgColor = ref(undefined)
const bodyTextColor = ref(undefined)
const imgLoaded = ref(false)
let timer

// HSL to Hex
function hsl2Hex(h, s, l) {
  l /= 100;
  const a = s * Math.min(l, 1 - l) / 100;
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
  };
  let result = `#${f(0)}${f(8)}${f(4)}`
  return result.toUpperCase();
}

// 重設圖片載入狀態，已顯示 spinner
function resetImgLoaded(){
  imgLoaded.value = false
}

// 把色票依照彩度排列
const reorderData = computed(() => {
  const orderBy = 'h'
  // 測試時先篩選出確定有顏色的
  return data.value.filter(d => d['main_color']).sort(
    (a, b) => a.main_color[orderBy] - b.main_color[orderBy])
})

// 隨機取得一張照片做主角
function randomHero() {
  let randomNum = Math.floor(Math.random() * reorderData.value.length)
  heroData.value = reorderData.value[randomNum]
  bodyBgColor.value = heroData.value.main_color
  if (33 < bodyBgColor.value.l && bodyBgColor.value.l < 67) {
    bodyTextColor.value = {
      'h': 360,
      's': 0,
      'l': 100,
    }
  } else {
    bodyTextColor.value = {
      'h': bodyBgColor.value.h,
      's': bodyBgColor.value.s,
      'l': 100 - bodyBgColor.value.l,
    }
  }
}

// 依照隨機選出的照片設定背景色和文字顏色
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

// Test reading from CSV without backend
const CSV_URL = "/src/assets/data.csv"
function readFromCSV() {
  axios.get(CSV_URL)
    .then((response) => {
      let raw_d = response.data.replace("\r", "").split("\n")
      let cols = raw_d[0].split(",")
      raw_d.shift()
      raw_d.forEach(d => {
        const parts = [];
        let currentPart = '';
        let withinBracket = false;

        for (const char of d) {
          if (char === '[') {
            withinBracket = true;
          } else if (char === ']') {
            withinBracket = false;
          }

          if (char === ',' && !withinBracket) {
            parts.push(currentPart.trim());
            currentPart = '';
          } else {
            currentPart += char;
          }
        }

        if (currentPart) {
          parts.push(currentPart.trim());
        }

        let obj = {}
        for (let i = 0; i < cols.length; i++) {
          if (cols[i] == 'colors' && parts[i]) {
            let colorString = parts[i].replace(/'/g, '"')
            parts[i] = JSON.parse(colorString.slice(1, -1))
            obj['main_color'] = parts[i][0]
          }
          if (cols[i] == 'places' && parts[i]) {
            let placeString = parts[i].replace(/'/g, '"')
            if (placeString.indexOf(',') !== -1) {
              parts[i] = JSON.parse(placeString.slice(1, -1))
            } else {
              parts[i] = JSON.parse(placeString)
            }
          }
          obj[cols[i]] = parts[i]
        }
        data.value.push(obj)
      })
      randomHero()
      console.log("讀取本地 CSV 成功")
    })
    .catch((error) => {
      console.error(error);
    });
}

onMounted(() => {
  readFromCSV()

  // 定時隨機抽選
  timer = window.setInterval(() => {
    resetImgLoaded()
    randomHero()
  }, 10000)
})

onBeforeUnmount(() => {
  clearInterval(timer)
})
</script>

<template>
  <main v-if="bodyBgColor" :style="backgroundStyle" class="transition">
    <div class="container vh-100 d-flex flex-column flex-md-row align-items-center justify-content-center gap-5">
      <div class="polaroid hero d-flex flex-column text-dark">
        <div class="ratio ratio-1x1">
          <img :src="heroData.url_google" alt="" class="d-none" @load="imgLoaded = true">
          <div v-if="imgLoaded" class="overflow-hidden">
            <img :src="heroData.url_google" alt="" class="w-100 h-100 object-fit-cover"
            style="object-position: center;">
          </div>
          <div v-else class="d-flex justify-content-center align-items-center">
            <div class="spinner-border" role="status"></div>
          </div>
        </div>
        <div>
          <p class="d-flex justify-content-between align-items-center border-bottom p-2 ff-serif transition mb-0"
            :style="backgroundStyle">
            <i class="fa-solid fa-camera fa-xl"></i>
            <span class="ps-2">{{ heroData.date + ' ' + heroData.time }}</span>
          </p>
        </div>
      </div>
      <div id="Sec_text">
        <p class="d-flex gap-2 flex-wrap">
          <span v-for="place of heroData.places" class="rounded-pill p-2 transition" :style="backgroundStyleReverse">#{{
            place }}</span>
        </p>
        <p class="mb-0 mt-3">{{ heroData.description }}</p>
        <div class="d-flex flex-wrap gap-2 mt-8">
            <color-swatch :color-hsl="color"
            v-for="color of heroData.colors"></color-swatch>
        </div>
      </div>
    </div>
    <!-- Controller -->
    <controller-manual></controller-manual>
    <controller-auto></controller-auto>
  </main>
</template>

<style scoped>
#Sec_text{
  width: 30vw;
}
</style>