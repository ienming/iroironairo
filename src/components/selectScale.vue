<script setup>
    import {inject} from 'vue'
    const sampling = inject('sampling')
</script>

<template>
    <div>
        <p>Choose Scale</p>
        <label for="scale">Scale</label>
        <input type="range" id="scale" name="scale" min="2" max="50" step="1"
            v-model="sampling">
    </div>
</template>

<style scoped></style>