<script setup>
import { ref, computed, onMounted } from 'vue'
import { hsl2Hex } from '@/composable/common';
import { useRouter, onBeforeRouteLeave } from 'vue-router'
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

const color = computed(() => {
    return hsl2Hex(props.colorHsl.h, props.colorHsl.s, props.colorHsl.l)
})
const toolTips = ref(null)

// Router
const router = useRouter()
function navigateTo() {
    // 銷毀Bootstrap tooltip
    // tooltipList.forEach(tooltip => {
    //     tooltip.hide()
    // });
    tooltipList.hide()
    router.push({
        path: '/color_search',
        query: {
            color: JSON.stringify(props.colorHsl)
        },
    })
}

let tooltipList, tooltipTriggerList;
onBeforeRouteLeave((to, from) => {
    // 銷毀Bootstrap tooltip
    // tooltipList.forEach(tooltip => {
    //     tooltip.hide()
    // });
    tooltipList.hide()
    return true;
})

onMounted(() => {
    // tooltipTriggerList = toolTips.value.querySelectorAll('[data-bs-toggle="tooltip"]')
    // tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    tooltipTriggerList = toolTips.value
    tooltipList = new bootstrap.Tooltip(toolTips.value)
})
</script>

<template>
    <div class="color-swatch txt-lang-hover" data-bs-placement="bottom" data-bs-toggle="tooltip" data-bs-title="相近的顏色"
    ref="toolTips" @click="navigateTo" role="button">
        <div :style="{ 'background-color': color }">
        </div>
        <p class="w-100 m-0 d-flex justify-content-between align-items-center">
            <div class="me-3 txt-lang-container">
                <span>{{ label }}</span>
                <span>{{ label }}</span>
            </div>
            <div class="d-flex gap-3 gap-lg-2">
                <i v-if="viewPhoto" class="fa-solid fa-image" data-bs-title="查看照片" data-bs-toggle="tooltip"
                    @click="emit('show-polaroid')"></i>
                <i class="fa-solid fa-magnifying-glass"></i>
            </div>
        </p>
    </div>
</template>

<style scoped>
i {
    opacity: .35;
    cursor: pointer;
}

/* i:hover {
    opacity: 1;
} */
</style>