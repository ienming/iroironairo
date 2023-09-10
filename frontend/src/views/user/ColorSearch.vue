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
        for (let j=0; j<arr[i].colors.length; j++){
            const currentHsl = arr[i].colors[j]
            const currentHex = hsl2Hex(currentHsl.h, currentHsl.s, currentHsl.l)
            const currentRgb = hex2Rgb(currentHex)

            if (colorDifference(colorRgb.value, currentRgb) < threshold){
                output.push(arr[i])
            }
        }
    }
    return new Set(output)
})

// Polaroid
const polaroidShown = ref(false)
const nowPolaroid = ref(null)
function showPolaroid(data){
  nowPolaroid.value = data
  polaroidShown.value = true
}
</script>

<template>
    <div class="z-1">
        <h1>Color Search</h1>
        <div>
            <p>{{ colorHsl }}</p>
            <p>{{ colorHex }}</p>
            <p>{{ colorRgb }}</p>
            <p style="height: 50px" :style="{'background-color':colorHex}"></p>
        </div>
        <main>
            <h2>Results:</h2>
            <p>{{ dataFiltered.size+'張照片' }}</p>
            <div v-for="d of dataFiltered" class="d-flex">
                <!-- <p>{{ d.name }}</p>
                <div class="main-cs" v-for="c of d.colors"
                :style="{'background-color': hsl2Hex(c.h, c.s, c.l) }"></div> -->

                <!-- Color Swatch -->
                <color-swatch class="flex-grow-1"
                  :label="'#'+d.places[0]"
                  :view-photo="true"
                  :color-hsl="d.main_color"
                  @show-polaroid="showPolaroid(d)"></color-swatch>
            </div>
        </main>
        <!-- Polaroid -->
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