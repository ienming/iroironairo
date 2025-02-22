<script setup>
import { computed, inject, ref, onMounted, nextTick } from "vue";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";
import { hsl2Hex, hex2Rgb } from "@/composable/common";
import { diff } from "color-diff";
import Bookmark from "@/components/Bookmark.vue";
import Navigator from "@/components/Navigator.vue";
import IroModal from "@/components/IroModal.vue";

const route = useRoute();
const data = inject("csvData", []);

const colorHsl = computed(() => {
  if (route.query.color){
    return JSON.parse(route.query.color);
  }else return
});
const colorHex = computed(() => {
  if (colorHsl.value){
    return hsl2Hex(colorHsl.value.h, colorHsl.value.s, colorHsl.value.l);
  }else return
});
const colorRgb = computed(() => {
  if (colorHex.value){
    return hex2Rgb(colorHex.value);
  }else return
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
function loadRandomPhoto(){
  randomPhotoLoaded.value = true;
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
const modalController = ref(null)
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
  if(clearData.length > 0){
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
    router.push({
        path: '/color_search',
        query: {
            color: JSON.stringify(recColor)
        },
    })
}

function searchByPlace(place){
  router.push({
        path: '/all',
        query: {
            place: JSON.stringify(place)
        },
    })
}

// 同一頁點選顏色時也要觸發 filter
onBeforeRouteUpdate((to, from) => {
  polaroidShown.value = false;
});

// 定時觸發抽選照片
onMounted(()=>{
  window.setInterval(() => {
    lotteryPhoto();
  }, 60000);

  lotteryPhoto()
})
</script>

<template>
  <main class="z-1 min-vh-100 bg-silver">
    <div class="container pt-5 pt-lg-8">
      <div class="row">
        <div
          class="sticky-top d-flex flex-column flex-lg-row justify-content-between"
          style="top: 30px"
        >
          <div class="py-4 py-lg-0">
            <h1 class="fs-4 ff-serif fw-bolder mb-4">
              <span class="d-block">相近的顏色</span>
              <span class="fs-6 fw-normal">選んだ色に近い色の写真</span>
            </h1>
            <div class="mb-2">
              <span>{{
                dataFiltered.length + "張 / " + data.length + "張照片"
              }}</span>
            </div>
          </div>  
          <div class="bg-white rounded-3 ms-0 shadow-lg overflow-hidden row col-12 col-lg-4">
            <div
              :style="{ 'background-color': colorHex }"
              class="mb-lg-0 col-lg-6 color-searched" />
            <div class="col-lg-6 py-1 py-lg-3">
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
    </div>
    <section
      v-if="hasData"
      class="mt-5 grid-layout">
      <!-- 隨機照片 -->
      <section>
        <div
          v-if="randomPhoto"
          class="position-sticky top-0">
          <img
            :src="randomPhoto.url_google"
            style="width: 1px;"
            class="position-absolute"
            @load="loadRandomPhoto">
          <transition
            name="fade"
            mode="out-in">
            <section
              v-if="randomPhotoLoaded">
              <div class="random-photo-container">
                <img
                  ref="randomPhotoEl"
                  class="img-fluid w-100 random-photo"
                  role="button"
                  :src="randomPhoto.url_google"
                  @click="showPolaroid(randomPhoto)" />
              </div>
              <div class="px-4 ps-lg-6 pb-lg-6">
                <div class="d-flex gap-2 my-2 my-lg-4">
                  <div
                    v-for="place of randomPhoto.places"
                    :key="place.key"
                    class="px-2 py-1 rounded-pill transition txt-lang-hover bg-dark text-white flex-wrap"
                    role="button"
                    @click="searchByPlace(place)">
                    <div class="txt-lang-container">
                      <span>#{{place }}</span>
                      <span>#{{place }}</span>
                    </div>
                  </div>
                </div>
                <p>{{ randomPhoto.description }}</p>
              </div>
            </section>
          </transition>
        </div>
      </section>
      <!-- Data viz -->
      <section class="ps-4 ps-lg-0 pb-8 overflow-x-scroll">
        <div>
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
              <div class="d-flex gap-2 ff-serif"
                  :class="
                    dataFiltered.filter((d) => d.date.split('/')[1] == month.key)
                      .length > 0
                      ? ''
                      : 'opacity-50'
                  ">
                <p
                >
                  <strong>{{ month.label.split(" ")[0] }}</strong>
                  {{ month.label.split(" ")[1] }}
                </p>
                <span>({{ dataFiltered.filter(
                    (d) => d.date.split('/')[1] == month.key
                  ).length }})</span>
              </div>
              <div class="d-flex py-4 overflow-x-auto">
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
                  class="position-relative color-data flex-shrink-0"
                  :data-place="d.places.length > 0 ? d.places : '無'"
                  @click="showPolaroid(d)"
                ></div>
              </div>
            </section>
        </div>
      </section>
    </section>
    <section v-else class="row">
      <div class="col-lg-6 mx-lg-auto mt-6">
        <p class="text-center mb-5">
          找不太到相似顏色的照片，試試搜尋這些顏色？
        </p>
        <div class="d-flex gap-3 justify-content-center">
          <transition-group name="fade">
            <div v-for="rec of recommends" :style="{'background-color': hsl2Hex(rec.h, rec.s, rec.l)}"
            class="rounded-pill color-other"
            role="button"
            :key="rec.h+rec.s+rec.l"
            @click="reSearch(rec)"></div>
          </transition-group>
        </div>
      </div>
    </section>
    <!-- Polaroid -->
    <transition
      name="fade"
      mode="out-in">
      <iro-modal
        v-if="polaroidShown"
        :photo="nowPolaroid"
        @show-prev="showPrev"
        @show-next="showNext"
        @close-modal="polaroidShown = false" />
    </transition>
    <!-- Bookmark -->
    <bookmark class="position-fixed top-0 d-flex align-items-center gap-1" />
    <!-- Nav -->
    <navigator />
  </main>
</template>

<style scoped>
.color-searched{
  height: 80px;
}
@media screen and (min-width: 992px) {
  .color-searched{
    height: unset;
  }
}
.color-data {
  --size: 30px;
  width: var(--size);
  height: var(--size);
}

.color-other{
  --size: 60px;
  height: var(--size);
  width: var(--size);
  transition: .2s ease-out;
}
.color-other:hover{
  transform: translateY(-10px);
}

.random-photo-container{
  overflow: hidden;
  max-height: 80vh;
}

.random-photo{
  transform-origin: center center;
  transition: transform 1s ease-in-out;
}

.random-photo:hover{
  transform: scale(1.05);
}

.grid-layout {
  display: grid;
  grid-template-columns: none;
  gap: 16px;
}

@media screen and (min-width: 992px) {
  .grid-layout {
    grid-template-columns: minmax(50vw, 700px) auto;
  }
}
</style>