<script setup>
    import {inject} from 'vue'
    const order = inject('order')
</script>

<template>
    <div>
        <label for="orders">Ordered by:</label>
        <select name="orders" id="orders" v-model="order">
            <option>hue</option>
            <option>saturation</option>
            <option>lightness</option>
        </select>
    </div>
</template>

<style scoped></style>