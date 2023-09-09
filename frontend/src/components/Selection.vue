<script setup>
import { ref } from 'vue';
const props = defineProps(['label', 'options', 'currentValue'])
const emits = defineEmits(['change-value'])

const listShown = ref(false)

function changeValue(value) {
    emits('change-value', value)
    switchList()
}

function openList() {

}
</script>

<template>
    <div class="iro-selection position-relative" @mouseenter="listShown = true" @mouseleave="listShown = false">
        <div class="iro-selection-button p-2 rounded position-relative" type="button">
            <span>{{ label + '：' }}</span>
            <span>
                <span class="me-5">{{ currentValue }}</span>
                <i class="fa-solid fa-chevron-down"></i>
            </span>
        </div>
        <ul class="list-group list-group-flush shadow-lg rounded position-absolute w-100 iro-selection-list"
            v-show="listShown">
            <li type="button" class="list-group-item list-group-item-action"
            :class="currentValue == opt.label ? 'active':''"
            aria-current="true" v-for="opt of options"
                @click="changeValue(opt.key)">
                {{ opt.label }}
            </li>
        </ul>
    </div>
</template>