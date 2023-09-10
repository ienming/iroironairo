<script setup>
import { useRoute } from 'vue-router';
import { hsl2Hex } from '@/composable/common';
const route = useRoute();
const colorSearched = JSON.parse(route.query.color)
</script>
<template>
    <div class="z-1">
        <h1>Color Search</h1>
        <div>
            <p>{{ colorSearched }}</p>
            <p>{{ hsl2Hex(colorSearched.h, colorSearched.s, colorSearched.l) }}</p>
            <p style="height: 50px" :style="{'background-color':hsl2Hex(colorSearched.h, colorSearched.s, colorSearched.l)}"></p>
        </div>
    </div>
</template>