<script setup>
    const props = defineProps(['imgNum'])
</script>

<template>
    <div>
        <p>累死了快發瘋</p>
        <!-- <p>now show: {{ props.imgNum }}</p> -->
        <button @click="$emit('prevImg')">Prev</button>
        <button @click="$emit('nextImg')">Next</button>
        <button @click="$emit('randomImg')">Random</button>
    </div>
</template>

<style scoped></style>