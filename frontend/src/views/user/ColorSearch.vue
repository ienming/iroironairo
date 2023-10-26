<script setup>
import { computed, inject, ref } from 'vue';
import { useRoute } from 'vue-router';
import { hsl2Hex, hex2Rgb } from '@/composable/common';
import { diff } from 'color-diff';
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import ColorSwatch from '@/components/ColorSwatch.vue';
import Polaroid from '../../components/Polaroid.vue';
import PolaroidText from '../../components/PolaroidText.vue';

const route = useRoute();
const data = inject('csvData', [])

const colorHsl = computed(()=>{
    return JSON.parse(route.query.color)
})
const colorHex = computed(()=>{
    return hsl2Hex(colorHsl.value.h, colorHsl.value.s, colorHsl.value.l)
})
const colorRgb = computed(()=>{
    return hex2Rgb(colorHex.value)
})

function colorDifference(color1, color2) {
  let result = diff(color1, color2)
  return result;
}

const threshold = 10
const dataFiltered = computed(()=>{
    let arr = [...data.value]
    arr = arr.filter(d => d['main_color'])
    let output = []
    for (let i=0; i<arr.length; i++){
        // 只找最多的顏色
        const currentHsl = arr[i].colors[0]
        const currentHex = hsl2Hex(currentHsl.h, currentHsl.s, currentHsl.l)
        const currentRgb = hex2Rgb(currentHex)

        if (colorDifference(colorRgb.value, currentRgb) < threshold){
            output.push(arr[i])
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
    return Array.from(new Set(output))
})

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
  if (currentPhotoIndex > 0){
      if (dataFiltered.value[currentPhotoIndex-1]['main_color']){
        nowPolaroid.value = dataFiltered.value[currentPhotoIndex-1]
      }
}else{
    nowPolaroid.value = dataFiltered.value[dataFiltered.value.length-1]
  }
}
function showNext(){
  const findingFunction = (d) => d.name === nowPolaroid.value.name
  const currentPhotoIndex = dataFiltered.value.findIndex(findingFunction)
  if (currentPhotoIndex == dataFiltered.value.length-1){
    nowPolaroid.value = dataFiltered.value[0]
  }else{
    if (dataFiltered.value[currentPhotoIndex+1]['main_color']){
      nowPolaroid.value = dataFiltered.value[currentPhotoIndex+1]
    }
  }
}
</script>

<template>
    <div class="z-1 min-vh-100 bg-silver">
        <main class="container pt-5 pb-8 pt-lg-8">
            <div class="row">
                <div class="col-lg-4">
                    <div class="sticky-top" style="top: 30px;">
                        <h1 class="fs-2 fw-bolder mb-4">相近的顏色</h1>
                        <div class="bg-white rounded-3 p-3 shadow-lg w-75">
                            <p style="height: 50px" :style="{'background-color':colorHex}" class="rounded-3"></p>
                            <p class="mb-1">{{ colorHex }}</p>
                            <p class="mb-1">{{ 'RGB: '+colorRgb.r+', '+colorRgb.g+', '+colorRgb.b }}</p>
                            <p class="mb-0">{{ 'HSL: '+colorHsl.h+'o, '+colorHsl.s+'%, '+colorHsl.l+'%' }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="mb-5">
                        <span>{{ dataFiltered.length+'張 / '+data.length+'張照片' }}</span>  
                    </div>
                    <section class="d-flex gap-3 flex-wrap">
                        <!-- Color Swatch -->
                        <color-swatch class="col-2 flex-grow-1"
                            v-for="d of dataFiltered"
                          :label="'#'+d.places[0]"
                          :view-photo="true"
                          :color-hsl="d.main_color"
                          @show-polaroid="showPolaroid(d)"></color-swatch>
                    </section>
                </div>
            </div>
        </main>
        <!-- Polaroid -->
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