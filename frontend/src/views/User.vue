<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const data = ref([])

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
          if (cols[i] == 'colors' && parts[i]!==''){
            let colorString = parts[i].replace(/'/g, '"')
            parts[i] = JSON.parse(colorString.slice(1, -1))
            obj['main_color'] = parts[i][0]
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
</script>

<template>
  <div class="my-5 mx-md-5">
    <h1 class="ff-serif fw-bolder">色々な色</h1>
    <h2 class="mb-3 ff-serif">
      iroironairo
    </h2>
    <button class="btn btn-outline-dark" @click="readFromCSV">私が見た日本を観る！</button>
  </div>
  <main>
    <section class="d-flex flex-wrap">
      <transition-group name="fade">
        <div v-for="(d, idx) of reorderColors" :key="d.id"
        :style="{'transition-delay': idx*0.025+'s'}">
          <!-- <p>{{ d.name }}</p>
          <p>{{ d.colors }}</p> -->
          <div class="color-swatch"
          v-if="typeof(d.colors) == 'object'"
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
}
.color-swatch:hover{
  border-radius: 50%;
}

img {
  max-width: 500px;
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

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
