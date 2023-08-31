<script setup>
import { watch, ref, onMounted } from 'vue';
const props = defineProps(['theme', 'shuffling'])

const controllerContainer = ref(null)

watch(props, (oldValue, newValue)=>{
    let newStyle = newValue.theme
    setStyle(newStyle)
})

function setStyle(styleObj){
    controllerContainer.value.style
        .setProperty('--luc-bg-color', styleObj['color'])
    controllerContainer.value.style
        .setProperty('--luc-text-color', styleObj['color'])
    controllerContainer.value.style
        .setProperty('--luc-border-color', styleObj['color'])
    controllerContainer.value.style
        .setProperty('--luc-text-color-reverse', styleObj['backgroundColor'])
}

onMounted(()=>{
    setStyle(props.theme)
})
</script>

<template>
    <section class="position-fixed top-50 translate-middle-y w-100 d-flex justify-content-between align-items-center"
    ref="controllerContainer">
        <div class="d-flex flex-column p-3 gap-3">
            <button class="luc-controller" @click="shuffle">
                <i class="fa-solid fa-shuffle"></i>
            </button>
            <!-- 沒有播放時出現 -->
            <button class="luc-controller" @click="autoPlay">
                <i class="fa-solid fa-play"></i>
            </button>
            <!-- 正在播放時出現 -->
            <button class="luc-controller" @click="stopAuto">
                <!-- 顯示數字 -->
                <!-- Hover 顯示圖案 -->
                <i class="fa-solid fa-stop"></i>
            </button>
        </div>
        <div class="d-flex flex-column p-3 gap-3">
            <button class="luc-controller" @click="prev">
                <i class="fa-solid fa-arrow-left"></i>
            </button>
            <button class="luc-controller" @click="next">
                <i class="fa-solid fa-arrow-right"></i>
            </button>
        </div>
    </section>
</template>

<style scoped>
section {
    --luc-border-color: #000;
    --luc-bg-color: #fff;
    --luc-text-color: #000;
    --luc-text-color-reverse: #000;
}

button {
    border: 1px solid var(--luc-border-color);
    color: var(--luc-text-color);
}

button:hover{
    background-color: var(--luc-bg-color);
    color: var(--luc-text-color-reverse);
}
</style>