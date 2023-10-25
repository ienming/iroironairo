<script setup>
import { computed, inject, ref } from 'vue';
import { hsl2Hex } from '@/composable/common';
import ColorSwatch from '@/components/ColorSwatch.vue';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Selection from '../../components/Selection.vue';
import Polaroid from '../../components/Polaroid.vue';
import PolaroidText from '../../components/PolaroidText.vue';
import ButtonCheckbox from '@/components/ButtonCheckbox.vue'

const data = inject('csvData', [])
const dataFiltered = computed(() => {
  let arr = data.value.filter(d => d['main_color'])
    // 根據地點篩選
    if (filterByPlaces.value.length < places.value.length){
      let result = []
      filterByPlaces.value.forEach(filterPlace => {
        result = result.concat(arr.filter(d => d.places.includes(filterPlace)))
      })
      const set = new Set(result)
      arr = Array.from(set)
    }
    // 根據月份篩選  
    if (filterByMonth.value.key !== "0") {
      arr = arr.filter(d => d.date.split(":")[1] == filterByMonth.value.key)
    }
    // 根據時間篩選
    if (filterByHour.value.key !== "全部") {
      arr = arr.filter(d => d.time.split(":")[0] == filterByHour.value.key)
    }
  // 篩選完畢後重新排序
  arr = arr.sort(
    (a, b) => {
      return new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
    })
  // 插入月份標誌
  let newArr = []
  for (let i = 0; i < arr.length; i++) {
    const currentMonth = arr[i].date.split(":")[1]
    // 第一個資料前先塞
    if (i == 0){
      let obj = {
          type: "monthTag",
          value: currentMonth,
        }
        const monthTxtObj = month2Txt(currentMonth)
        obj['zh'] = monthTxtObj.zh
        obj['jp'] = monthTxtObj.jp
        newArr.push(obj)
    }
    newArr.push(arr[i])
    // 判斷是否換月份
    if (i < arr.length - 1) {
      const nextDateMonth = arr[i + 1].date.split(":")[1]
      if (currentMonth !== nextDateMonth) {
        let obj = {
          type: "monthTag",
          value: nextDateMonth,
        }
        const monthTxtObj = month2Txt(nextDateMonth)
        obj['zh'] = monthTxtObj.zh
        obj['jp'] = monthTxtObj.jp
        newArr.push(obj)
      }
    }
  }
  return newArr
})

// 月份中日文對照表
function month2Txt(month) {
  let obj = {}
  switch (month) {
    case '09':
      obj['zh'] = '九月',
        obj['jp'] = 'Kugatsu'
      break;
    case '10':
      obj['zh'] = '十月',
        obj['jp'] = 'Jyuugatsu'
      break;
    case '11':
      obj['zh'] = '十一月',
        obj['jp'] = 'Jyuuichigatsu'
      break;
    case '12':
      obj['zh'] = '十二月',
        obj['jp'] = 'Jyuunigatsu'
      break;
    case '01':
      obj['zh'] = '一月',
        obj['jp'] = 'Ichigatsu'
      break;
    case '02':
      obj['zh'] = '二月',
        obj['jp'] = 'Nigatsu'
      break;
    case '03':
      obj['zh'] = '三月',
        obj['jp'] = 'Sangatsu'
      break;
  }
  return obj
}

// 地點篩選
const places = computed(() => {
  let arr = data.value.map(d => d.places).filter(d => Array.isArray(d))
  let temp = ['全部']
  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr[i].length; j++) {
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
const filterByPlaces = ref([])
for (let i=0; i<places.value.length; i++){
  filterByPlaces.value.push(places.value[i].key)
}
function filterPlace(checkedStatus){
  console.log(checkedStatus)
  if (checkedStatus.key === '全部'){
    if (checkedStatus.value){
      filterByPlaces.value = []
      for (let i=0; i<places.value.length; i++){
        filterByPlaces.value.push(places.value[i].key)
      }
    }else{
      filterByPlaces.value = []
    }
  }else{
    if (checkedStatus.value){
      filterByPlaces.value.push(checkedStatus.key)
    }else{
      filterByPlaces.value = filterByPlaces.value.filter(p => p !== checkedStatus.key)
    }
  }
  console.log(filterByPlaces.value)
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
  filterByMonth.value = months.find(month => month.key == key)
}

// 時間篩選
const hours = computed(()=>{
  let arr = data.value.map(d => d.time).filter(d => d)
  let temp = []
  for (let i = 0; i < arr.length; i++) {
      temp.push(arr[i].split(":")[0])
  }
  temp.sort((a,b) => {return a - b})
  temp.unshift("全部")
  temp = new Set(temp)
  let output = [...temp].map(d => {
    let obj = {
      key: d,
      label: d
    }
    if (d !== '全部'){
      if (d < 10){
        obj['label'] = "早上"+d.slice(-1)+"點"
      }
      if (d >= 10 && d < 12){
        obj['label'] = "早上"+d+"點"
      }
      if (d == 12){
        obj['label'] = "中午12點"
      }
      if (d > 12 && d < 18){
        obj['label'] = "下午"+(d*1-12)+"點"
      }
      if (d >= 18){
        obj['label'] = "晚上"+(d*1-12)+"點"
      }
    }
    return obj
  })
  return output
})
const filterByHour = ref(hours.value[0])
function filterHour(key) {
  filterByHour.value = hours.value.find(hour => hour.key == key)
}

// 資料密度
const density = ref(7)

// Polaroid
const polaroidShown = ref(false)
const nowPolaroid = ref(null)
function showPolaroid(data){
  nowPolaroid.value = data
  polaroidShown.value = true
}
</script>

<template>
  <div class="min-vh-100 bg-silver">
    <section class="container pt-5 position-relative">
      <div class="row justify-content-center mt-6 mb-4 mb-lg-6">
        <div class="ff-serif text-dark col-lg-5">
          <h2 class="fs-4">iroironairo</h2>
          <h1 class="fw-semibold mt-2 mt-md-4 mb-4">色々な色</h1>
          <h3 class="fs-5 d-flex flex-grow align-items-center">
            <span>2022.09.28</span>
            <div style="height: 1px;" class="w-100 bg-dark mx-2"></div>
            <span>2023.03.24</span>
          </h3>
        </div>
        <div class="col-lg-6 mt-4 mt-lg-0 d-flex align-items-end justify-content-end">
          <a href="" class="text-dark link-offset-2 link-offset-3-hover link-underline-dark link-underline-opacity-0 link-underline-opacity-75-hover txt-lang-hover">
            <i class="fa-solid fa-arrow-down fa-lg"></i>
            <div class="ms-1 d-inline-block">
              <span>下載海報</span>
              <span>下載海報</span>
            </div>
          </a>
        </div>
      </div>
      <section class="row justify-content-center mb-5">
        <div class="col-lg-11 d-flex gap-3 flex-wrap justify-content-between">
          <span>{{ dataFiltered.filter(d => d['_id']).length }} 張 / {{ data.length }} 張照片</span>
          <div class="d-flex flex-wrap gap-3">
            <selection label="拍攝月份" :options="months" :current-value="filterByMonth.label" @change-value="filterMonth">
            </selection>
            <selection label="拍攝時間" :options="hours" :current-value="filterByHour.label" @change-value="filterHour">
            </selection>
            <input type="range" min="3" max="30" v-model="density">
          </div>
          <div class="d-flex gap-1 overflow-scroll">
            <button-checkbox v-for="place of places" :label="place.label" :value="place.key" :checked="filterByPlaces.includes(place.key)"
            @change-value="filterPlace"></button-checkbox>
          </div>
        </div>
      </section>
    </section>
    <main class="row justify-content-center">
      <div class="pt-6 ps-5 d-flex justify-content-start overflow-scroll">
        <transition-group name="fade">
          <div v-for="(d,id) of dataFiltered" :key="id">
            <div v-if="d.type == 'monthTag'" style="height: 40vh;" class="ff-serif position-relative">
              <p class="bg-silver p-1 m-0 position-absolute" style="top: -60px;">
                <span class="mb-1 fw-bold d-block">{{ d.zh }}</span>
                <span>{{ d.jp }}</span>
              </p>
            </div>
            <div v-else style="height: 40vh;"
            :style="{'background-color': hsl2Hex(d.main_color.h, d.main_color.s, d.main_color.l), 'width': density+'px'}"
            role="button" class="position-relative color-data"
            :data-place="d.places"
            @click="showPolaroid(d)"></div>
          </div>
        </transition-group>
      </div>
    </main>
    <!-- Modal Polaroid -->
    <transition name="fade" mode="out-in">
      <section class="vh-100 bg-silver fixed-top d-flex justify-content-center align-items-center gap-5"
      v-if="polaroidShown">
        <polaroid :photo="nowPolaroid"></polaroid>
        <polaroid-text :photo="nowPolaroid"></polaroid-text>
        <i class="fa-solid fa-xmark fa-xl position-absolute end-0 p-5 opacity-50-hover"
        role="button" @click="polaroidShown = false"></i>
      </section>
    </transition>
    <!-- Bookmark -->
    <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
    <!-- Nav -->
    <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
  </div>
</template>

<style scoped>
h1 {
  font-size: 52px;
}

@media screen and (min-width: 992px) {
  h1{
    font-size: 86px;
  }
}

.anim-line-h {
  display: block;
  width: 80%;
  height: 1px;
  flex: auto;
  margin: 0 4px;
}

.color-data:hover{
  width: 90px !important;
}
.color-data:hover::after{
  transform: scale(1);
}
.color-data::after {
  display: block;
  content: attr(data-place);
  position: absolute;
  top: 12px;
  padding: 8px;
  border-radius: 25px;
  font-size: 14px;
  width: max-content;
  z-index: 99;
  transform-origin: center;
  transform: scale(0);
  /* transition: .1s ease-in-out; */
  background-color: #fff;
}
</style>