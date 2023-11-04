<script setup>
import { ref } from 'vue';
import { gsap } from "gsap";

const container = ref(null)
 function transition() {
    // gsap.to(".fusuma", {
    //   duration: 0.5, 
    //   opacity: 0, 
    //   x: '100%', 
    //   stagger: 0.15,
    //   onComplete: () => { container.value.style['z-index'] = '-1' }
    // });
 }
</script>

<template>
    <section @click="transition" ref="container" class="vw-100 vh-100 position-fixed top-0 fusuma-container"
    style="top: 200px !important;">
        <div class="fusuma"></div>
        <div class="fusuma"></div>
        <div class="fusuma"></div>
    </section>
</template>

<style scoped>
.fusuma-container{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    z-index: 1030;
}
.fusuma{
    background-color: brown;
}
</style>