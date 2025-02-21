<script setup>
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
    <input
        :id="props.value"
        type="checkbox"
        class="d-none"
        @change="emit('change-value', {'key': props.value, 'value': !props.checked})">
    <label
        :for="props.value"
        role="button"
        class="m-0 px-2 py-1 rounded-pill border border-dark flex-shrink-0 opacity-75-hover"
        :class="props.quant.quant > 0 && props.checked ? ['bg-dark', 'text-white']:'opacity-25'">
        {{ props.label }}
        <i
            v-if="!props.checked"
            class="fa-solid fa-plus" />
        <i
            v-else
            class="fa-solid fa-check" />
        <span v-if="props.value !== '全部'">({{ props.quant['quant'] }})</span>
    </label>
</template>