<script setup>
import { computed, ref, onMounted } from 'vue';
import axios from 'axios'
import ColorSwatch from '@/components/ColorSwatch.vue';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';

const data = ref([])
const dataReordered = computed(()=>{
  return data.value.filter(d => d['main_color']).sort(
      (a, b) => {
        return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
    })
})

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
  <div class="bg-silver">
    <main class="container py-5 py-lg-8">
      <div class="row justify-content-center mb-lg-6">
        <div class="ff-serif text-dark col-lg-5">
          <h2 class="fs-4">iroironairo</h2>
          <h1 class="fw-semibold mt-2 mt-md-4 mb-4">色々な色</h1>
          <h3 class="fs-5 d-flex flex-grow align-items-center">
            <span>2022.09.28</span>
            <div style="height: 1px;" class="w-100 bg-dark mx-2"></div>
            <span>2023.03.24</span>
          </h3>
        </div>
        <div class="col-lg-6 d-flex align-items-end justify-content-end">
          <a href="">下載海報</a>
        </div>
      </div>
      <section class="row justify-content-center mb-lg-5">
        <div class="col-lg-11 d-flex justify-content-between">
          <span>{{ dataReordered.length }} 張 / {{ data.length }} 張照片</span>
          <div>Input *2</div>
        </div>
      </section>
      <section class="row justify-content-center">
        <div class="col-lg-11 d-flex flex-wrap gap-1">
          <color-swatch :color-hsl="d.main_color" :label="d.date+' '+d.time"
            v-for="d of dataReordered"></color-swatch>
        </div>
      </section>
    </main>
    <!-- Bookmark -->
    <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
    <!-- Nav -->
    <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
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
</style>