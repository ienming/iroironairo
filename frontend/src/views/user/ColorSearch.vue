<script setup>
import { computed, inject } from 'vue';
import { useRoute } from 'vue-router';
import { hsl2Hex, hex2Rgb } from '@/composable/common';
import { diff } from 'color-diff';
const route = useRoute();
const data = inject('csvData', [])

const colorHsl = JSON.parse(route.query.color)
const colorHex = computed(()=>{
    return hsl2Hex(colorHsl.h, colorHsl.s, colorHsl.l)
})
const colorRgb = computed(()=>{
    return hex2Rgb(colorHex.value)
})
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

        </main>
    </div>
</template>