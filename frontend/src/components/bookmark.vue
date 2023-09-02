<script setup>
import { watch, ref, onMounted } from 'vue';
const props = defineProps(['theme'])

const bookmarkEl = ref(null)

watch(props, (oldValue, newValue)=>{
    let newStyle = newValue.theme
    setStyle(newStyle)
})

function setStyle(styleObj){
    bookmarkEl.value.style
        .setProperty('--luc-bg-color', styleObj['color'])
}

onMounted(()=>{
    setStyle(props.theme)
})
</script>

<template>
    <div class="bookmark ff-serif" ref="bookmarkEl">
        <span>iroironairo</span>
    </div>
</template>

<style scoped>
div{
    --luc-bg-color: #000;
}
div::before{
    background-color: var(--luc-bg-color);
}
</style>