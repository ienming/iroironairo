<script setup>
import { ref, computed, onMounted } from 'vue'
import { hsl2Hex } from '@/composable/common';
const props = defineProps({
  colorHsl: Object,
  label: {
    type: String,
    default: "",
  },
  viewPhoto: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['show-polaroid'])

const color = computed(()=>{
    return hsl2Hex(props.colorHsl.h, props.colorHsl.s, props.colorHsl.l)
})
const copyText = ref("複製顏色")
const toolTips = ref(null)

// Copy color to clipboard
function copyColor(){
    navigator.clipboard.writeText(color.value)
    copyText.value = "已複製！"
}

function resetCopyText(){
    copyText.value = "複製顏色"
}

onMounted(()=>{
    const tooltipTriggerList = toolTips.value.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
})
</script>

<template>
    <div class="color-swatch">
        <div :style="{'background-color': color }"
        :data-copy-text="copyText"
        @click="copyColor"
        @mouseout="resetCopyText"></div>
        <p class="w-100 m-0 d-flex justify-content-between align-items-center">
            <span class="me-3">{{ label }}</span>
            <div class="d-flex gap-3 gap-lg-2" ref="toolTips">
                <i v-if="viewPhoto"
                class="fa-solid fa-image"
                data-bs-title="查看照片"
                data-bs-toggle="tooltip"
                @click="emit('show-polaroid')"></i>
                <i class="fa-solid fa-magnifying-glass"
                data-bs-placement="bottom"
                data-bs-toggle="tooltip"
                data-bs-title="搜尋顏色"
                ref="toolTips"></i>
            </div>
        </p>
    </div>
</template>

<style scoped>
i {
    opacity: .35;
    cursor: pointer;
}

i:hover{
    opacity: 1;
}
</style>