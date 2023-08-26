<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'

const data = ref([])
const heroData = ref(undefined)
const bodyBgColor = ref(undefined)
const bodyTextColor = ref(undefined)

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
      // position: 'absolute',
      // top: 0
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
  <div v-if="bodyBgColor" :style="backgroundStyle" class="pt-5">
    <div class="container">
      <div class="mb-5 row justify-content-center">
        <div v-if="heroData" class="col-md-6">
          <div class="polaroid hero d-flex flex-column text-dark">
            <div class="placeholder-glow ratio ratio-1x1"
            :style="{
              'background': 'url('+heroData.url_google+')',
              'background-size': 'cover',
              'background-repeat': 'no-repeat',
              }"></div>
            <p class="mb-0 mt-3">{{ heroData.description }}</p>
          </div>
        </div>
        <div class="ff-serif col-md-6">
          <h1 class="fw-bolder">色々な色</h1>
          <h2>iroironairo</h2>
          <p>「色々」（iroiro）在日文裡有「多樣、各式各樣、色彩豐富」的意思，「色々な色」（iroironairo）是我在日本口說課的考試時，無意間脫口而出的句子。這個網站整理了這半年我拍的照片，也作為在日本半年所看見色彩的代表。</p>
          <p>「いろいろな色」は日本語で「多様、多様、豊かな色彩」を意味します。「いろいろな色」は日本語の口述試験中にうっかり口走ってしまった文です。 このウェブサイトは私が半年間に撮った写真を整理するものであり、半年間に日本で見た色の代表でもあります。</p>
        </div>
      </div>
    </div>
    <main class="container text-dark">
      <section class="d-flex flex-wrap gap-3">
        <transition-group name="fade">
          <div v-for="(d, idx) of reorderData" :key="d.id" :style="{ 'transition-delay': idx * 0.025 + 's' }">
            <div class="polaroid color-swatch" v-if="typeof (d.colors) == 'object'">
              <div class="ratio ratio-1x1"
                :style="{ 'background-color': 'hsl(' + d.main_color.h + ',' + d.main_color.s + '%,' + d.main_color.l + '%)' }">
              </div>
              <p class="mb-0 mt-2">{{ d.places[0]||'...' }}</p>
            </div>
          </div>
        </transition-group>
      </section>
    </main>
  </div>
</template>

<style scoped>
.polaroid {
  background-color: #fff;
}

.polaroid.hero {
  padding: 20px;
}

.polaroid.color-swatch {
  padding: 10px;
  border-radius: 4px;
  width: 110px;
  cursor: pointer;
  transition: all .2s ease-in-out;
}

.polaroid.color-swatch:hover{
  transform: translateY(-10px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175);
}

.polaroid.color-swatch>div{
  transition: all .4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.polaroid.color-swatch:hover>div {
  border-radius: 50%;
}
</style>