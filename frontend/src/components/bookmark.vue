<script setup>
const props = defineProps({
    theme: {
        type: Object,
        default: {
            "color": "#232323",
            "backgroundColor": "#F6F6F6"
        }
    }
})
</script>

<template>
    <div class="bookmark ff-serif p-3 p-lg-4 flex-lg-column" ref="bookmarkEl"
    :style="{'--bookmark-color': theme.color}">
        <span class="text">iroironairo</span>
    </div>
</template>

<style scoped>
.bookmark {
    z-index: 1020;
}
</style>