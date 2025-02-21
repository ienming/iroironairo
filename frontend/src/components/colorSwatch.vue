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
    <div
        ref="toolTips"
        role="button"
        class="txt-lang-hover color-swatch"
        data-bs-placement="bottom"
        data-bs-toggle="tooltip"
        data-bs-title="相近的顏色"
        @click="navigateTo">
        <div
            class="color-fill"
            :style="{ 'background-color': color }" />
        <p class="w-100 m-0 d-flex justify-content-between align-items-center p-2">
            <div class="me-3 txt-lang-container">
                <span>{{ label }}</span>
                <span>{{ label }}</span>
            </div>
            <div class="d-flex gap-3 gap-lg-2">
                <i
                    v-if="viewPhoto"
                    class="fa-solid fa-image"
                    data-bs-title="查看照片"
                    data-bs-toggle="tooltip"
                    @click="emit('show-polaroid')" />
                <i class="fa-solid fa-magnifying-glass" />
            </div>
        </p>
    </div>
</template>

<style scoped>
.color-swatch {
    padding: 4px !important;
}

.color-swatch .color-fill {
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

i {
    cursor: pointer;
    font-size: 12px;
    opacity: 0.35;
}
</style>