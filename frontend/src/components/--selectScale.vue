<script setup>
    import {inject} from 'vue'
    const sampling = inject('sampling')
</script>

<template>
    <div>
        <label for="scale">Sampling</label>
        <input type="range" id="scale" name="scale" min="2" max="30" step="1"
            v-model="sampling">
    </div>
</template>

<style scoped></style>