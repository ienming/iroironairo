<script setup>
    const props = defineProps(['imgNum'])
</script>

<template>
    <div>
        <img :src="'/src/assets/img/'+props.imgNum+'.jpg'" class="img-view"/>
    </div>
</template>

<style scoped>
.img-view{
    overflow: hidden;
}
</style>