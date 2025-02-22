<script setup>
import { watch, ref, onMounted } from 'vue';
const props = defineProps(['theme', 'isAutoPlay', 'timeLeft'])
const emit = defineEmits(['show-next', 'show-prev', 'start-playing', 'stop-playing', 'shuffle'])

const controllerEl = ref(null)
const isHoveringStopBtn = ref(false)

watch(props, (oldValue, newValue)=>{
    let newStyle = newValue.theme
    setStyle(newStyle)
})

function setStyle(styleObj){
    controllerEl.value.style
    .setProperty('--luc-text-color', styleObj['color'])
    controllerEl.value.style
    .setProperty('--luc-border-color', styleObj['color'])
    controllerEl.value.style
        .setProperty('--luc-bg-color', styleObj['color'])
    controllerEl.value.style
        .setProperty('--luc-text-color-reverse', styleObj['backgroundColor'])
}

onMounted(()=>{
    setStyle(props.theme)
})
</script>

<template>
    <section class="position-fixed w-100 d-flex flex-row justify-content-center justify-content-lg-between align-items-center"
    ref="controllerEl">
        <div class="d-flex flex-row flex-lg-column px-2 py-2 py-lg-0 gap-4 gap-lg-3">
            <button class="luc-controller" @click="emit('shuffle')">
                <i class="fa-solid fa-shuffle"></i>
            </button>
            <button
                v-if="isAutoPlay"
                class="luc-controller"
                @click="emit('stop-playing'); console.log('stop-playing');"
                @mouseenter="isHoveringStopBtn = true"
                @mouseleave="isHoveringStopBtn = false">
                <span v-if="!isHoveringStopBtn">{{ timeLeft }}</span>
                <i v-else 
                    class="fa-solid fa-stop" />
            </button>
            <button
                v-else
                class="luc-controller"
                @click="emit('start-playing')">
                <i class="fa-solid fa-play" />
            </button>
        </div>
        <div class="d-flex flex-row flex-lg-column px-2 py-2 py-lg-0 gap-4 gap-lg-3">
            <button
                class="luc-controller"
                @click="emit('show-prev')">
                <i class="fa-solid fa-arrow-left" />
            </button>
            <button
                class="luc-controller"
                @click="emit('show-next')">
                <i class="fa-solid fa-arrow-right" />
            </button>
        </div>
    </section>
</template>

<style scoped>
section {
    --luc-text-color: #000;
    --luc-border-color: #000;
    --luc-bg-color: #000;
    --luc-text-color-reverse: #fff;
    bottom: 0;
    right: 0;
    background-color: var(--luc-bg-color);
}

button {
    border: 1px solid var(--luc-text-color-reverse);
    color: var(--luc-text-color-reverse);
}

button:hover{
    background-color: var(--luc-bg-color);
    color: var(--luc-text-color-reverse);
}

@media screen and (min-width: 992px) {
  section{
    bottom: unset;
    right: unset;
    top: 50%;
    transform: translateY(-50%);
    background-color: transparent;
  }
  button {
    border: 1px solid var(--luc-border-color);
    color: var(--luc-text-color);
    }
}
</style>