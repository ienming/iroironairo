<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'

const data = ref([])
const heroData = ref(undefined)
const bodyBgColor = ref(undefined)
const bodyTextColor = ref(undefined)

const polaroidPlaceShown = ref(true)

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
})
</script>

<template>
  <div v-if="bodyBgColor" :style="backgroundStyle" class="pt-3 pt-md-7">
    <div class="container">
      <div class="mb-5 row flex-column-revrese flex-md-row justify-content-center">
        <div v-if="heroData" class="col-md-6">
          <div class="polaroid hero d-flex flex-column text-dark">
            <div class="placeholder-glow ratio ratio-1x1"
            :style="{
              'background': 'url('+heroData.url_google+')',
              'background-size': 'cover',
              'background-repeat': 'no-repeat',
              }"></div>
            <div>
              <p class="d-flex justify-content-between align-items-center border-bottom p-2 ff-serif"
              :style="backgroundStyle">
                <i class="fa-solid fa-camera fa-xl"></i>
                <span class="ps-2">{{ heroData.date + ' ' + heroData.time }}</span>
              </p>
              <p>
                <span v-for="place of heroData.places" class="me-2 rounded-pill p-2 border"
                :style="backgroundStyleReverse"
                >#{{ place }}</span>
              </p>
              <p class="mb-0 mt-3">{{ heroData.description }}</p>
            </div>
          </div>
        </div>
        <div class="ff-serif col-md-6 mt-5 mt-md-0 px-md-5 px-lg-7 pt-md-9">
          <h2 class="fs-4">iroironairo</h2>
          <h1 class="fw-semibold my-4">色々な色</h1>
          <h3 class="fs-5 d-flex align-items-center">
            <span>2022.09.28</span>
            <span class="anim-line-h"
            :style="{'background-color': `hsl(${bodyTextColor.h},${bodyTextColor.s}%,${bodyTextColor.l}%)`}"></span>
            <span>2023.03.24</span>
          </h3>
          <div class="abstract">
            <p class="mb-4">「色々」（iroiro）在日文裡有「多樣、各式各樣、色彩豐富」的意思，「色々な色」（iroironairo）是我在日本口說課的考試時，無意間脫口而出的句子。這個網站整理了這半年我拍的照片，也作為在日本半年所看見色彩的代表。</p>
            <p>「いろいろな色」は日本語で「多様、多様、豊かな色彩」を意味します。「いろいろな色」は日本語の会話試験中にうっかり口走ってしまった文です。 このウェブサイトは私が半年間に撮った写真を整理するものであり、半年間に日本で見た色の代表でもあります。</p>
          </div>
        </div>
      </div>
    </div>
    <section class="p-4 my-4 bg-white bg-opacity-25">
      <div class="container">
        <div class="row no-wrap align-items-center gap-3">
          <div class="form-check w-auto">
            <input class="form-check-input" type="checkbox" v-model="polaroidPlaceShown" id="polaroid_place">
            <label class="form-check-label" for="polaroid_place">
              顯示拍攝地點
            </label>
          </div>
          <div class="d-flex align-items-center w-auto">
            <span class="pe-2">拍攝地點</span>
            <select class="form-select w-auto" aria-label="Default select example">
              <option value="1">顏色</option>
            </select>
          </div>
        </div>
      </div>
    </section>
    <main class="container text-dark">
      <section class="d-flex flex-wrap gap-3">
        <transition-group name="fade">
          <div v-for="(d, idx) of reorderData" :key="d.id"
            :style="{ 'transition-delay': idx * 0.025 + 's' }"
            class="col-3 col-md-1 flex-grow-1">
            <div class="polaroid color-swatch">
              <div class="ratio ratio-1x1"
                :style="{ 'background-color': 'hsl(' + d.main_color.h + ',' + d.main_color.s + '%,' + d.main_color.l + '%)' }">
              </div>
              <transition name="fade" mode="out-in">
                <p class="mb-0 mt-1" v-show="polaroidPlaceShown">{{ d.places[0]||'...' }}</p>
              </transition>
            </div>
          </div>
        </transition-group>
      </section>
    </main>
  </div>
</template>

<style scoped>
h1{
  font-size: 86px;
}

.anim-line-h{
  display: block;
  width: 80%;
  height: 1px;
  flex: auto;
  margin: 0 4px;
}

@media screen and (min-width: 768px) {
  .abstract{
    margin-top: 267px;
  }
}
</style>