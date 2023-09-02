<script setup>
import { watch, ref, onMounted } from 'vue';
const props = defineProps(['theme'])

const navEl = ref(null)

watch(props, (oldValue, newValue)=>{
    let newStyle = newValue.theme
    setStyle(newStyle)
})

function setStyle(styleObj){
    navEl.value.style
        .setProperty('--luc-bg-color', styleObj['color'])
}

onMounted(()=>{
    setStyle(props.theme)
})
</script>

<template>
    <nav class="d-flex gap-4 py-3 py-lg-4" ref="navEl">
        <router-link :to="{
                path: '/about'
            }"
            class="txt-lang-hover">
            <div>
                <span>關於 iroironairo</span>
                <span>色々な色について</span>
            </div>
        </router-link>
        <router-link :to="{
                path: '/all'
            }"
            class="txt-lang-hover">
            <div>
                <span>瀏覽全部相片</span>
                <span>全ての写真</span>
            </div>
        </router-link>
    </nav>
</template>

<style scoped>
nav{
    --luc-bg-color: #000;
}

nav a {
    color: var(--luc-bg-color);
    text-decoration: none;
}
</style>