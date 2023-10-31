<script setup>
import { ref } from 'vue';
const emit = defineEmits(['change-value'])
const props = defineProps({
    label: {
        type: String,
        default: "Label"
    },
    value: {
        type: String,
        default: "Value"
    },
    checked: {
        type: Boolean,
        default: false
    },
    quant: {
        type: Object,
        default: {}
    }
});
</script>

<template>
    <input type="checkbox" :id="props.value" class="d-none"
    @change="emit('change-value', {'key': props.value, 'value': !props.checked})">
    <label :for="props.value"
    class="m-0 p-2 rounded-pill border border-dark flex-shrink-0 opacity-75-hover"
    :class="props.checked ? '':'opacity-25'"
    role="button">
        {{ props.label }}
        <i class="fa-solid fa-plus" v-if="!props.checked"></i>
        <i class="fa-solid fa-check" v-else></i>
        ({{ props.quant['quant'] }})
    </label>
</template>