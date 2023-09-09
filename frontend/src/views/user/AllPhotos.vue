<script setup>
import { computed, ref, onMounted } from 'vue';
import axios from 'axios'
import ColorSwatch from '@/components/ColorSwatch.vue';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Selection from '../../components/Selection.vue';

const data = ref([])
const dataFiltered = computed(() => {
  let arr = data.value.filter(d => d['main_color']).sort(
    (a, b) => {
      return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
    })
  // 根據月份篩選  
  if (filterByMonth.value.key !== "0") {
    arr = arr.filter(d => d.date.split(":")[1] == filterByMonth.value.key)
  }
  // 根據地點篩選
  if (filterByPlace.value.key !== "全部"){
    arr = arr.filter(d => d.places.includes(filterByPlace.value.key))
  }
  return arr
})

// 地點篩選
const places = computed(()=>{
  let arr = data.value.map(d => d.places).filter(d => Array.isArray(d))
  let temp = ['全部']
  for (let i=0; i<arr.length; i++){
    for (let j=0; j<arr[i].length; j++){
      temp.push(arr[i][j])
    }
  }
  temp = new Set(temp)
  let output = [...temp].map(d => {
    let obj = {
      key: d,
      label: d
    }
    return obj
  })
  return output
})
const filterByPlace = ref(places.value[0])
function filterPlace(key) {
  console.log('filter by place: ' + key)
  filterByPlace.value = places.value.find(place => place.key == key)
}

// 月份篩選
const months = [
  {
    label: '全部',
    key: '0'
  },
  {
    label: '九月',
    key: '09'
  },
  {
    label: '十月',
    key: '10'
  },
  {
    label: '十一月',
    key: '11'
  },
  {
    label: '十二月',
    key: '12'
  },
  {
    label: '一月',
    key: '01'
  },
  {
    label: '二月',
    key: '02'
  },
  {
    label: '三月',
    key: '03'
  }
]
const filterByMonth = ref(months[0])
function filterMonth(key) {
  console.log('filter by month: ' + key)
  filterByMonth.value = months.find(month => month.key == key)
}

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
  <div class="min-vh-100 bg-silver">
    <section class="container py-5 py-lg-8 position-relative">
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
          <span>{{ dataFiltered.length }} 張 / {{ data.length }} 張照片</span>
          <div class="d-flex gap-4">
            <selection label="拍攝地點" :options="places" :current-value="filterByPlace.label" @change-value="filterPlace"></selection>
            <selection label="拍攝月份" :options="months" :current-value="filterByMonth.label" @change-value="filterMonth">
            </selection>
          </div>
        </div>
      </section>
      <main class="row justify-content-center">
        <div class="col-lg-11 d-flex flex-wrap justify-content-start gap-2">
          <color-swatch class="flex-grow-1"
          :label="d.date+' '+d.places"
          :view-photo="true" :color-hsl="d.main_color"
            v-for="d of dataFiltered"></color-swatch>
        </div>
      </main>
      <!-- Fade out clip -->
      <div class="fade-clip fixed-bottom"></div>
    </section>
    <!-- Bookmark -->
    <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
    <!-- Nav -->
    <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
  </div>
</template>

<style scoped>
h1 {
  font-size: 86px;
}

.anim-line-h {
  display: block;
  width: 80%;
  height: 1px;
  flex: auto;
  margin: 0 4px;
}
</style>