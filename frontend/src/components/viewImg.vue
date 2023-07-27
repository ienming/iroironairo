<script setup>
    const props = defineProps(['imgNum'])
    const getImgUrl = function(n){
        let url = new URL(`../assets/img/${n}.jpg`, import.meta.url).href
        // console.log(url)
        return url
    }
</script>

<template>
    <Transition name="fade" mode="out-in">
        <img
        :src="getImgUrl(props.imgNum)"
        :key="getImgUrl(props.imgNum)"
        class="img-view" />
    </Transition>
</template>

<style scoped>
.img-view{
    max-width: 200px;
    margin-bottom: 32px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>