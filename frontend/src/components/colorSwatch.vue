<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps(['colorHsl'])
const color = computed(()=>{
    return hsl2Hex(props.colorHsl.h, props.colorHsl.s, props.colorHsl.l)
})
const copyText = ref("複製 コピー")
const toolTipEl = ref(null)

// HSL to Hex
function hsl2Hex(h, s, l) {
  l /= 100;
  const a = s * Math.min(l, 1 - l) / 100;
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
  };
  let result = `#${f(0)}${f(8)}${f(4)}`
  return result.toUpperCase();
}

// Copy color to clipboard
function copyColor(){
    navigator.clipboard.writeText(color.value)
    copyText.value = "已複製 コピーされました！"
}

function resetCopyText(){
    copyText.value = "複製 コピー"
}

onMounted(()=>{
    const tooltip = new bootstrap.Tooltip(toolTipEl.value)
})
</script>

<template>
    <div class="color-swatch">
        <div :style="{'background-color': color }"
        :data-copy-text="copyText"
        @click="copyColor"
        @mouseout="resetCopyText"></div>
        <p class="w-100 m-0 d-flex justify-content-between align-items-center">
            <span>{{ color }}</span>
            <i class="fa-solid fa-magnifying-glass"
            data-bs-placement="bottom"
            data-bs-toggle="tooltip"
            data-bs-title="搜尋顏色"
            ref="toolTipEl"></i>
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