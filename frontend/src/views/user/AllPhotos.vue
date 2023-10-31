<script setup>
import { computed, inject, onBeforeMount, onMounted, watch, ref, reactive, nextTick } from 'vue';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import { hsl2Hex } from '@/composable/common';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import Selection from '@/components/Selection.vue';
import Polaroid from '@/components/Polaroid.vue';
import PolaroidText from '@/components/PolaroidText.vue';
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
      arr = arr.filter(d => d.date.split("/")[1] == filterByMonth.value.key)
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
    const currentMonth = arr[i].date.split("/")[1]
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
      const nextDateMonth = arr[i + 1].date.split("/")[1]
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

// 顯示模式
const displayMode = ref(false)

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

// 從其他頁面點選地點過來
onBeforeMount(()=>{
  const route = useRoute()
  if (JSON.stringify(route.query) !== '{}'){
    const placeArg = JSON.parse(route.query.place);
    filterByPlaces.value = []
    filterByPlaces.value.push(placeArg)
  }
})

// 同一頁點選地點時也要觸發 filter
onBeforeRouteUpdate((to, form) =>{
  const placeArg = JSON.parse(to.query.place);
  filterByPlaces.value = []
  filterByPlaces.value.push(placeArg)
  polaroidShown.value = false
})

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
  console.log(key)
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
const density = ref(10)

// 控制項
const controllerShown = ref(false)

// Polaroid
const polaroidShown = ref(false)
const nowPolaroid = ref(null)
function showPolaroid(data){
  nowPolaroid.value = data
  polaroidShown.value = true
}
function showPrev(){
  const findingFunction = (d) => d.name === nowPolaroid.value.name
  const currentPhotoIndex = dataFiltered.value.findIndex(findingFunction)
  if (dataFiltered.value[currentPhotoIndex-1]['main_color']){
    nowPolaroid.value = dataFiltered.value[currentPhotoIndex-1]
  }else{
    if (currentPhotoIndex == 1){
      nowPolaroid.value = dataFiltered.value[dataFiltered.value.length-1]
    }else{
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex-2]
    }
  }
}
function showNext(){
  const findingFunction = (d) => d.name === nowPolaroid.value.name
  const currentPhotoIndex = dataFiltered.value.findIndex(findingFunction)
  if (currentPhotoIndex == dataFiltered.value.length-1){
    nowPolaroid.value = dataFiltered.value[1]
  }else{
    if (dataFiltered.value[currentPhotoIndex+1]['main_color']){
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex+1]
    }else{
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex+2]
    }
  }
}

// Random photo
const randomIndexes = ref([])
const randomPhotoStatus = reactive({})
const [randomPhoto_1, randomPhoto_2, randomPhoto_3] = [ref(null), ref(null), ref(null)]
const randomPhotoEls = [randomPhoto_1, randomPhoto_2, randomPhoto_3]

const randomPhotos = computed(()=>{
  let photos = []
  const cleanData = JSON.parse(JSON.stringify(dataFiltered.value)).filter(d => d.type !== 'monthTag')
  randomIndexes.value.forEach(idx => {
    photos.push(cleanData[idx])
  })
  return photos
})

function lotteryPhoto(){
  randomIndexes.value = []
  for (const key in randomPhotoStatus){
    randomPhotoStatus[key] = false
  }

  const cleanData = JSON.parse(JSON.stringify(dataFiltered.value)).filter(d => d.type !== 'monthTag')
  const maxIndex = cleanData.length - 1;
  if (cleanData.length > 3){
    while (randomIndexes.value.length < 3) {
      const randomIndex = Math.floor(Math.random() * (maxIndex + 1));
      
      if (!randomIndexes.value.includes(randomIndex)) {
        randomIndexes.value.push(randomIndex);
      }
    }
  }else{
    while (randomIndexes.value.length <= cleanData.length - 1){
      const randomIndex = Math.floor(Math.random() * (maxIndex + 1));
      
      if (!randomIndexes.value.includes(randomIndex)) {
        randomIndexes.value.push(randomIndex);
      }
    }
  }
  console.log("Get new random photos: "+randomIndexes.value)
}

function randomPhotoLoaded(num){
  randomPhotoStatus[num] = true
}

// 滾動 Show Case（for 滑鼠）
const showCaseDiv = ref(null)
function scrollShowCase(type){
  const dom = showCaseDiv.value
  const currentChild = Array.from( dom.children ).find(child => {
    return child.offsetLeft >= dom.scrollLeft + window.innerWidth / 2;
  });
  switch (type){
    case 'next':
      dom.scrollTo({
        left: currentChild.offsetLeft,
        behavior: "smooth"
      })
    break;
    case 'prev':
      dom.scrollTo({
        left: dom.scrollLeft - window.innerWidth/2,
        behavior: "smooth"
      })
  }
}

const controllerContainer = ref(null)
function initTooltip(){
  nextTick(()=>{
    const tooltipTriggerList = controllerContainer.value.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  })
}

onMounted(()=>{
  window.setInterval(()=>{
    lotteryPhoto()
  }, 15000)

  watch(dataFiltered, () => {
    lotteryPhoto();
  });

  lotteryPhoto()
  initTooltip()
})
</script>

<template>
  <div class="min-vh-100 bg-silver">
    <section>
      <div class="d-flex">
        <div v-if="randomPhotos.length > 2" id="randomPhoto_3">
          <img ref="randomPhoto_3" :src="randomPhotos[2].url_google" class="d-none" @load="randomPhotoLoaded('3')"/>
          <transition name="fade" mode="out-in">
            <img v-if="randomPhotoStatus['3']" :src="randomPhotos[2].url_google" alt="" style="width: auto; height: 25vh;" class="random-photo">
            <div v-else style="height: 25vh; width: 18.75vh;" :style="{'background-color': hsl2Hex(randomPhotos[2].colors[0].h, randomPhotos[2].colors[0].s, randomPhotos[2].colors[0].l)}"></div>
          </transition>
        </div>
        <div v-if="randomPhotos.length > 0" id="randomPhoto_1">
          <img ref="randomPhoto_1" :src="randomPhotos[0].url_google" class="d-none" @load="randomPhotoLoaded('1')"/>
          <transition name="fade" mode="out-in">
            <img v-if="randomPhotoStatus['1']" :src="randomPhotos[0].url_google" alt="" style="width: auto; height: 25vh;" class="random-photo">
            <div v-else style="height: 25vh; width: 18.75vh;" :style="{'background-color': hsl2Hex(randomPhotos[0].colors[0].h, randomPhotos[0].colors[0].s, randomPhotos[0].colors[0].l)}"></div>
          </transition>
        </div>
      </div>
    </section>
    <main class="row justify-content-center">
      <section v-if="!displayMode" class="pt-6 ps-6 d-flex justify-content-start overflow-scroll" ref="showCaseDiv">
        <transition-group name="fade">
          <div v-for="(d,id) of dataFiltered" :key="id">
            <div v-if="d.type == 'monthTag'" style="height: 25vh;" class="ff-serif position-relative">
              <p class="bg-silver p-1 m-0 position-absolute" style="top: -60px;">
                <span class="mb-1 fw-bold d-block">{{ d.zh }}</span>
                <span>{{ d.jp }}</span>
              </p>
            </div>
            <div v-else style="height: 25vh;"
            :style="{'background-color': hsl2Hex(d.main_color.h, d.main_color.s, d.main_color.l), 'width': density+'px'}"
            role="button" class="position-relative color-data"
            :data-place="d.places.length > 0 ? d.places : '無'"
            @click="showPolaroid(d)"></div>
          </div>
        </transition-group>
      </section>
      <section v-else class="ps-6">
        <section v-for="month of months.filter(m => m.label !== '全部')" class="mb-3">
          <div class="mb-1 d-flex align-items-center">
            <p class="ff-serif mb-0"><strong>{{ month.label }}</strong> {{ month2Txt(month.key).jp }}</p>
            <div class="d-flex align-items-center">
              <div class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="往前移動">
                  <i class="fa-solid fa-arrow-left"></i>
              </div>
              <div class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="往後移動">
                  <i class="fa-solid fa-arrow-right"></i>
              </div>
            </div>
          </div>
          <div class="d-flex overflow-scroll">
            <div v-for="(d,id) of dataFiltered.filter(d => d.type !== 'monthTag').filter(d => d.date.split('/')[1] == month.key)">
              <div style="height: 25vh;"
                  :style="{'background-color': hsl2Hex(d.main_color.h, d.main_color.s, d.main_color.l), 'width': density+'px'}"
                  role="button" class="position-relative color-data"
                  :data-place="d.places.length > 0 ? d.places : '無'"
                  @click="showPolaroid(d)"></div>
            </div>
          </div>
        </section>
      </section>
    </main>
    <section class="position-relative">
      <div class="d-flex">
        <div class="row ff-serif text-dark col-lg-5 me-auto ps-6 pt-3 d-flex">
          <div class="col-lg-8">
            <h2 class="fs-6">iroironairo</h2>
            <h1 class="fw-semibold mt-2 mb-3">色々な色</h1>
            <h3 class="d-flex flex-grow align-items-center opacity-50" style="font-size: 14px;">
              <span>2022.09.28</span>
              <div style="height: 1px;" class="w-100 bg-dark mx-2"></div>
              <span>2023.03.24</span>
            </h3>
          </div>
          <div class="col-lg-4 d-flex align-items-start gap-2" ref="controllerContainer">
            <div class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="切換顯示模式" @click="displayMode = !displayMode">
              Switch mode
            </div>
            <div class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="篩選照片" @click="controllerShown = !controllerShown">
              <i class="fa-solid fa-sliders"></i>
            </div>
            <div v-if="!displayMode" class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="往前移動" @click="scrollShowCase('prev')">
              <i class="fa-solid fa-arrow-left"></i>
            </div>
            <div v-if="!displayMode" class="luc-controller opacity-50 opacity-100-hover" role="button" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="往後移動" @click="scrollShowCase('next')">
                <i class="fa-solid fa-arrow-right"></i>
            </div>
          </div>
        </div>
        <div v-if="randomPhotos.length > 1" class="ms-auto pe-8 pt-3" id="randomPhoto_2">
          <img ref="randomPhoto_2" :src="randomPhotos[1].url_google" class="d-none" @load="randomPhotoLoaded('2')"/>
          <transition name="fade" mode="out-in">
            <img v-if="randomPhotoStatus['2']" :src="randomPhotos[1].url_google" alt="" style="width: auto; height: 25vh;" class="random-photo">
            <div v-else style="height: 25vh; width: 18.75vh;" :style="{'background-color': hsl2Hex(randomPhotos[1].colors[0].h, randomPhotos[1].colors[0].s, randomPhotos[1].colors[0].l)}"></div>
          </transition>
        </div>
      </div>
    </section>
    <!-- 控制項 -->
    <transition name="fade" mode="out-in">
      <section class="p-4 position-fixed top-0 end-0 w-25 bg-silver h-100 overflow-scroll z-1 shadow-lg"
      v-show="controllerShown">
        <span class="pb-2 d-block">{{ dataFiltered.filter(d => d['_id']).length }} 張 / {{ data.length }} 張照片</span>
        <div class="d-flex flex-wrap gap-3">
          <selection class="w-100" label="拍攝月份" :options="months" :current-label="filterByMonth.label" @change-value="filterMonth">
          </selection>
          <selection class="w-100" label="拍攝時間" :options="hours" :current-label="filterByHour.label" @change-value="filterHour">
          </selection>
          <div>
            <label for="dataDensity" class="form-label">Example range</label>
            <input type="range" min="3" max="30" class="form-range" id="dataDensity" v-model="density">
          </div>
        </div>
        <div class="pb-3">
          <div class="mt-2 d-flex gap-2 flex-wrap">
            <button-checkbox v-for="place of places" :label="place.label" :value="place.key" :checked="filterByPlaces.includes(place.key)"
            @change-value="filterPlace"></button-checkbox>
          </div>
        </div>
      </section>
    </transition>
    <!-- Modal Polaroid -->
    <transition name="fade" mode="out-in">
      <section class="vh-100 bg-silver fixed-top d-flex justify-content-center align-items-center gap-5"
      v-if="polaroidShown">
        <polaroid :photo="nowPolaroid"></polaroid>
        <polaroid-text :photo="nowPolaroid" :bg-style="{'background-color': '#232323', 'color': '#f6f6f6'}"></polaroid-text>
        <i class="fa-solid fa-xmark fa-xl position-absolute top-0 end-0 p-5 opacity-50-hover"
        role="button" @click="polaroidShown = false"></i>
        <div class="position-absolute end-0 d-flex flex-column px-3 pb-3 pb-lg-0 gap-3">
          <button class="luc-controller" @click="showPrev">
              <i class="fa-solid fa-arrow-left"></i>
          </button>
          <button class="luc-controller" @click="showNext">
              <i class="fa-solid fa-arrow-right"></i>
          </button>
        </div>
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
  font-size: 36px;
}

.anim-line-h {
  display: block;
  width: 80%;
  height: 1px;
  flex: auto;
  margin: 0 4px;
}

.random-photo{
  width: 105px;
  overflow: hidden;
}

#randomPhoto_1{
  padding-left: 30vw;
}

#randomPhoto_3{
  padding: 50px;
  padding-left: 100px;
}
</style>