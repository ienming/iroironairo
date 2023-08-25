<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'

const data = ref([])
const heroData = ref(undefined)

// 
const reorderColors = computed(()=>{
  const orderBy = 'h'
  return data.value.filter(d => d['main_color']).sort(
    (a, b) => a.main_color[orderBy] - b.main_color[orderBy])
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
        for (let i=0; i<cols.length; i++){
          if (cols[i] == 'colors' && parts[i]){
            let colorString = parts[i].replace(/'/g, '"')
            parts[i] = JSON.parse(colorString.slice(1, -1))
            obj['main_color'] = parts[i][0]
          }
          if (cols[i] == 'places' && parts[i]){
            let placeString = parts[i].replace(/'/g, '"')
            if (placeString.indexOf(',') !== -1){
              parts[i] = JSON.parse(placeString.slice(1, -1))
            }else{
              parts[i] = JSON.parse(placeString)
            }
          }
          obj[cols[i]] = parts[i]
        }
        data.value.push(obj)
      })
      let randomNum = Math.floor(Math.random() * data.value.length)
      heroData.value = data.value[randomNum]
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
  <div class="my-5 mx-md-5 d-flex justify-content-between">
    <div class="ff-serif">
      <h1 class="fw-bolder">色々な色</h1>
      <h2>iroironairo</h2>
    </div>
    <div v-if="heroData" class="placeholder">
      <img :src="heroData.url_google" alt="" />
      <p>{{ heroData.date }}</p>
      <p>
        <span v-for="place of heroData.places"
        class="me-2">{{ place }}</span>
      </p>
    </div>
  </div>
  <main>
    <section class="d-flex flex-wrap">
      <transition-group name="fade">
        <div v-for="(d, idx) of reorderColors" :key="d.id"
        class="d-flex flex-column justify-content-between"
        :style="{'transition-delay': idx*0.025+'s'}">
          <div class="color-swatch"
          v-if="typeof(d.colors) == 'object'"
          :data-description="d.description.slice(0,7)+'...'"
          :style="{ 'background-color': 'hsl(' + d.main_color.h + ',' + d.main_color.s + '%,' + d.main_color.l + '%)'}"></div>
        </div>
      </transition-group>
    </section>
  </main>
</template>

<style scoped>
.color-swatch{
  --size: 25vw;
  --max-size: 120px;
  width: var(--size);
  height: var(--size);
  max-width: var(--max-size);
  max-height: var(--max-size);
  transition: all .4s cubic-bezier(0.165, 0.84, 0.44, 1);
  cursor: pointer;
  position: relative;
}

.color-swatch::after{
  content: attr(data-description);
  background-color: #fff;
  border-radius: 50px;
  padding: 8px;
  width: max-content;
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: left 50%;
  transform: scale(0);
  transition: all .4s cubic-bezier(0.165, 0.84, 0.44, 1);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175);
  opacity: 0;
  z-index: 1;
}
.color-swatch:hover{
  border-radius: 50%;
}

.color-swatch:hover::after{
  transform: scale(1);
  opacity: 1;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
