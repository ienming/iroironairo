<script setup>
import { ref } from 'vue';
const props = defineProps(['label', 'options', 'optionsQuants', 'currentLabel'])
const emits = defineEmits(['change-value'])

const listShown = ref(false)

function changeValue(value) {
    emits('change-value', value)
}
</script>

<template>
    <div class="iro-selection position-relative" @mouseenter="listShown = true" @mouseleave="listShown = false">
        <div class="iro-selection-button p-2 rounded position-relative d-flex" type="button">
            <span class="flex-shrink-0">{{ label + '：' }}</span>
            <span class="w-100 d-flex justify-content-between align-items-center">
                <span class="me-5">{{ currentLabel }}</span>
                <i class="fa-solid fa-chevron-down"></i>
            </span>
        </div>
        <ul class="list-group list-group-flush shadow-lg rounded position-absolute top-0 w-100 iro-selection-list"
            v-show="listShown">
            <li type="button" class="list-group-item list-group-item-action"
            :class="currentLabel == opt.label ? 'active':''"
            aria-current="true" v-for="opt of options"
                @click="changeValue(opt.key)">
                {{ opt.label }}
                <span v-if="optionsQuants && opt.label !== '全部'">({{ optionsQuants.find(q => q.key == opt.key)['quant'] }})</span>
            </li>
        </ul>
    </div>
</template>