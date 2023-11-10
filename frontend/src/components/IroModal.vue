<script setup>
import { watch, ref, nextTick, onMounted } from 'vue';
import Polaroid from '@/components/Polaroid.vue';
import PolaroidText from '@/components/PolaroidText.vue';
import { hsl2Hex, getReverseColor } from "@/composable/common";

const props = defineProps(['photo'])
const emit = defineEmits(['show-next', 'show-prev', 'close-modal'])
const modalController = ref(null)

watch(() => props.photo, ()=>{
  nextTick(()=>{
    setDynamicColor()
  })
})

function setDynamicColor(){
  const color = props.photo['main_color']
  const colorReverse = getReverseColor(color)
  modalController.value.style
    .setProperty('--luc-controller-bg', hsl2Hex(color.h, color.s, color.l))
  modalController.value.style
    .setProperty('--luc-controller-color', hsl2Hex(colorReverse.h, colorReverse.s, colorReverse.l))
}

onMounted(()=>{
  setDynamicColor()
})
</script>

<template>
    <section
        class="vh-100 bg-silver fixed-top overflow-scroll d-lg-flex justify-content-center align-items-center"
        style="z-index: 1050;"
      >
      <div class="d-flex flex-column flex-lg-row px-3 pt-4 pb-8 p-lg-0 justify-content-center align-items-center gap-5">
        <polaroid :photo="photo"></polaroid>
        <polaroid-text
          :photo="photo"
          :bg-style="{ 'background-color': '#232323', color: '#f6f6f6' }"
        ></polaroid-text>
      </div>
      <div
          class="position-fixed end-0 d-flex flex-row flex-lg-column px-2 py-2 gap-3 w-100 w-lg-auto justify-content-around modal-controller"
          ref="modalController"
        >
          <button class="luc-controller" @click="emit('show-prev')">
            <i class="fa-solid fa-arrow-left"></i>
          </button>
          <button class="luc-controller" @click="emit('close-modal')">
            <i class="fa-solid fa-xmark fa-xl"></i>
          </button>
          <button class="luc-controller" @click="emit('show-next')">
            <i class="fa-solid fa-arrow-right"></i>
          </button>
        </div>
    </section>
</template>

<style scoped>
.modal-controller{
  --luc-controller-bg: #f6f6f6;
  --luc-controller-color: #232323;
  bottom: 0;
  background-color: var(--luc-controller-bg);
  color: var(--luc-controller-color);
  border-color: var(--luc-controller-color);
}
</style>