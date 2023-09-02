<script setup>
const props = defineProps(['theme'])
</script>

<template>
    <div class="bookmark ff-serif p-3 p-lg-4 flex-lg-column" ref="bookmarkEl">
        <span class="anim-line"
        :style="{'background-color': theme.color}"></span>
        <span class="text">iroironairo</span>
    </div>
</template>