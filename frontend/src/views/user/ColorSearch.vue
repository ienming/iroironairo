<script setup>
import { computed, inject, ref, reactive, onMounted, nextTick } from "vue";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";
import { hsl2Hex, hex2Rgb } from "@/composable/common";
import { diff } from "color-diff";
import Bookmark from "@/components/Bookmark.vue";
import Navigator from "@/components/Navigator.vue";
import Polaroid from "@/components/Polaroid.vue";
import PolaroidText from "@/components/PolaroidText.vue";

const route = useRoute();
const data = inject("csvData", []);

const colorHsl = computed(() => {
  if (route.query.color){
    return JSON.parse(route.query.color);
  }else return
});
const colorHex = computed(() => {
  return hsl2Hex(colorHsl.value.h, colorHsl.value.s, colorHsl.value.l);
});
const colorRgb = computed(() => {
  return hex2Rgb(colorHex.value);
});

function colorDifference(color1, color2) {
  let result = diff(color1, color2);
  return result;
}

const threshold = 10;
const dataFiltered = computed(() => {
  let arr = [...data.value];
  arr = arr.filter((d) => d["main_color"]);
  let output = [];
  for (let i = 0; i < arr.length; i++) {
    // 只找最多的顏色
    const currentHsl = arr[i].colors[0];
    const currentHex = hsl2Hex(currentHsl.h, currentHsl.s, currentHsl.l);
    const currentRgb = hex2Rgb(currentHex);

    if (colorDifference(colorRgb.value, currentRgb) < threshold) {
      output.push(arr[i]);
    }
    // 用所有顏色下去找
    // for (let j=0; j<arr[i].colors.length; j++){
    //     const currentHsl = arr[i].colors[j]
    //     const currentHex = hsl2Hex(currentHsl.h, currentHsl.s, currentHsl.l)
    //     const currentRgb = hex2Rgb(currentHex)

    //     if (colorDifference(colorRgb.value, currentRgb) < threshold){
    //         output.push(arr[i])
    //     }
    // }
  }
  output = Array.from(new Set(output));
  output = output.sort((a, b) => {
    return (
      new Date(a.iso_date.slice(0, -1)) - new Date(b.iso_date.slice(0, -1))
    );
  });
  return output;
});

const hasData = computed(()=>{
  if (dataFiltered.value.length > 0){
    return true
  }else return false
})

// Random photo
const randomPhotoLoaded = ref(false)
const randomIndex = ref(0)
const randomPhoto = computed(()=>{
  if (hasData.value){
    return dataFiltered.value[randomIndex.value]
  }
})
const randomPhotoColor = computed(()=>{
  if (randomPhoto.value){
    return hsl2Hex(
      randomPhoto.value.colors[0].h,
      randomPhoto.value.colors[0].s,
      randomPhoto.value.colors[0].l
    )
  }
})
function lotteryPhoto(){
  if (hasData.value){
    randomPhotoLoaded.value = false
    const maxIndex = dataFiltered.value.length - 1;
    randomIndex.value = Math.floor(Math.random() * (maxIndex + 1));
  }
}
const randomPhotoEl = ref(null)
const randomPhotoOffsetY = ref('')
function loadRandomPhoto(){
  randomPhotoLoaded.value = true
  nextTick(()=>{
    const imgEl = randomPhotoEl.value
    // console.log(randomPhotoEl)
    // console.log(randomPhotoEl.value)
    // console.log(imgEl.clientHeight)
    if (imgEl){
      randomPhotoOffsetY.value = `-${(imgEl.clientHeight-300)/2}px`
    }
  })
}

// 月份分群
const months = [
  {
    label: "九月 Kugatsu",
    key: "09",
  },
  {
    label: "十月 Jyuugatsu",
    key: "10",
  },
  {
    label: "十一月 Jyuuichigatsu",
    key: "11",
  },
  {
    label: "十二月 Jyuunigatsu",
    key: "12",
  },
  {
    label: "一月 Ichigatsu",
    key: "01",
  },
  {
    label: "二月 Nigatsu",
    key: "02",
  },
  {
    label: "三月 Sangatsu",
    key: "03",
  },
];

// Polaroid
const polaroidShown = ref(false);
const nowPolaroid = ref(null);
function showPolaroid(data) {
  nowPolaroid.value = data;
  polaroidShown.value = true;
}
function showPrev() {
  const findingFunction = (d) => d.name === nowPolaroid.value.name;
  const currentPhotoIndex = dataFiltered.value.findIndex(findingFunction);
  if (currentPhotoIndex > 0) {
    if (dataFiltered.value[currentPhotoIndex - 1]["main_color"]) {
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex - 1];
    }
  } else {
    nowPolaroid.value = dataFiltered.value[dataFiltered.value.length - 1];
  }
}
function showNext() {
  const findingFunction = (d) => d.name === nowPolaroid.value.name;
  const currentPhotoIndex = dataFiltered.value.findIndex(findingFunction);
  if (currentPhotoIndex == dataFiltered.value.length - 1) {
    nowPolaroid.value = dataFiltered.value[0];
  } else {
    if (dataFiltered.value[currentPhotoIndex + 1]["main_color"]) {
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex + 1];
    }
  }
}

// 推薦顏色
const recommends = computed(()=>{
  let arr = []
  const clearData = JSON.parse(JSON.stringify(data.value.filter(d => d['main_color'])))
  if(clearData){
    const maxIndex = clearData.length - 1;
    for (let i=0; i<4; i++){
      let randomIndex = Math.floor(Math.random() * (maxIndex + 1));
      arr.push(clearData[randomIndex]['main_color'])
    }
    return arr
  }
})
const router = useRouter()
function reSearch(recColor) {
    // randomPhotoLoaded.value = false
    router.push({
        path: '/color_search',
        query: {
            color: JSON.stringify(recColor)
        },
    })
}

// 同一頁點選顏色時也要觸發 filter
onBeforeRouteUpdate((to, form) => {
  polaroidShown.value = false;
});

// 定時觸發抽選照片
onMounted(()=>{
  window.setInterval(() => {
    lotteryPhoto();
  }, 15000);

  lotteryPhoto()
})
</script>

<template>
  <div class="z-1 min-vh-100 bg-silver">
    <main class="container pt-5 pt-lg-8">
      <div class="row">
        <div
          class="sticky-top d-flex justify-content-between"
          style="top: 30px"
        >
          <div>
            <h1 class="fs-4 ff-serif fw-bolder mb-4">相近的顏色</h1>
            <div class="mb-2">
              <span>{{
                dataFiltered.length + "張 / " + data.length + "張照片"
              }}</span>
            </div>
          </div>  
          <div class="bg-white rounded-3 p-3 shadow-lg row col-5">
            <p
              :style="{ 'background-color': colorHex }"
              class="rounded-3 mb-0 col-5"
            ></p>
            <div class="col-7">
              <p class="mb-1">{{ colorHex }}</p>
              <p class="mb-1">
                {{ "RGB: " + colorRgb.r + ", " + colorRgb.g + ", " + colorRgb.b }}
              </p>
              <p class="mb-0">
                {{
                  "HSL: " +
                  colorHsl.h +
                  "o, " +
                  colorHsl.s +
                  "%, " +
                  colorHsl.l +
                  "%"
                }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
    <!-- 隨機照片 -->
    <section class="my-5">
      <div v-if="randomPhoto" class="mt-3 random-photo-container ms-auto position-relative" :style="{'border-bottom': '20px solid '+randomPhotoColor}">
        <img :src="randomPhoto.url_google" alt="" ref="randomPhotoEl" class="opacity-0 position-absolute w-100" @load="loadRandomPhoto">
        <transition name="fade" mode="out-in">
          <img v-if="randomPhotoLoaded" :src="randomPhoto.url_google" class="img-fluid w-100 position-absolute random-photo"
          @click="showPolaroid(randomPhoto)" role="button" :style="{'top': randomPhotoOffsetY}"/>
          <div v-else class="h-100" :style="{'background-color':randomPhotoColor}">
            <p class="opacity-0">{{randomPhoto}}</p>
          </div>
        </transition>
      </div>
      <transition name="fade" mode="out-in">
        <section v-if="randomPhotoLoaded" class="container">
          <div>
            <div class="d-flex gap-2 my-2">
              <p v-for="p of randomPhoto.places" class="fw-semibold mb-0 rounded-pill p-2 bg-dark text-white">#{{p}}</p>
            </div>
            <p>{{ randomPhoto.description }}</p>
          </div>
        </section>
      </transition>
    </section>
    <section class="container pb-8">
      <div v-if="hasData" class="row">
          <div class="d-flex gap-2 py-4 border-top border-bottom mb-3">
              <div class="d-flex gap-1 align-items-center">
                <div style="width: 15px; height: 15px;" class="rounded-pill bg-dark opacity-25"></div>
                <span>關西地區</span>
              </div>
              <div class="d-flex gap-1 align-items-center">
                <div style="width: 15px; height: 15px;" class="bg-dark opacity-25"></div>
                <span>非關西地區</span>
              </div>
          </div>
          <section v-for="month of months" class="mb-3">
            <p
              class="mb-2 ff-serif"
              :class="
                dataFiltered.filter((d) => d.date.split('/')[1] == month.key)
                  .length > 0
                  ? ''
                  : 'opacity-50'
              "
            >
              <strong>{{ month.label.split(" ")[0] }}</strong>
              {{ month.label.split(" ")[1] }}
            </p>
            <div class="d-flex">
              <div
                v-for="d of dataFiltered.filter(
                  (d) => d.date.split('/')[1] == month.key
                )"
                :style="{
                  'background-color': hsl2Hex(
                    d.main_color.h,
                    d.main_color.s,
                    d.main_color.l
                  )
                }"
                :class="d.area == 'kansai' ? 'rounded-pill' : ''"
                role="button"
                class="position-relative color-data"
                :data-place="d.places.length > 0 ? d.places : '無'"
                @click="showPolaroid(d)"
              ></div>
            </div>
          </section>
      </div>
      <div v-else class="row">
        <div class="col-lg-6 mx-lg-auto mt-6">
          <p class="text-center mb-5">
            找不太到相似顏色的照片，試試搜尋這些顏色？
          </p>
          <div class="d-flex gap-3 justify-content-center">
            <transition-group name="fade">
              <div v-for="rec of recommends" :style="{'background-color': hsl2Hex(rec.h, rec.s, rec.l)}"
              class="rounded-pill color-circle"
              role="button"
              :key="rec.h+rec.s+rec.l"
              @click="reSearch(rec)"></div>
            </transition-group>
          </div>
        </div>
      </div>
    </section>
    <!-- Polaroid -->
    <transition name="fade" mode="out-in">
      <section
        class="vh-100 bg-silver fixed-top d-flex justify-content-center align-items-center gap-5"
        v-if="polaroidShown"
      >
        <polaroid :photo="nowPolaroid"></polaroid>
        <polaroid-text
          :photo="nowPolaroid"
          :bg-style="{ 'background-color': '#232323', color: '#f6f6f6' }"
        ></polaroid-text>
        <i
          class="fa-solid fa-xmark fa-xl position-absolute top-0 end-0 p-5 opacity-50-hover"
          role="button"
          @click="polaroidShown = false"
        ></i>
        <div
          class="position-absolute end-0 d-flex flex-column px-3 pb-3 pb-lg-0 gap-3"
        >
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
    <bookmark
      class="position-fixed top-0 d-flex align-items-center gap-1"
    ></bookmark>
    <!-- Nav -->
    <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
  </div>
</template>

<style scoped>
.color-data {
  --size: 15px;
  width: var(--size);
  height: var(--size);
}

.color-circle{
  --size: 60px;
  height: var(--size);
  width: var(--size);
  transition: .2s ease-out;
}
.color-circle:hover{
  transform: translateY(-10px);
}

.random-photo-container{
  height: 300px;
  /* max-width: 450px; */
  overflow: hidden;
}

.random-photo{
  transform-origin: center center;
  transition: transform 1s ease-in-out;
}

.random-photo:hover{
  transform: scale(1.05);
}
</style>