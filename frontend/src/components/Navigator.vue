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
    <nav class="d-flex gap-4 py-3 py-lg-4">
        <router-link :to="{
                path: '/about'
            }"
            :style="{'color': theme.color}"
            class="txt-lang-hover">
            <div>
                <span>關於 iroironairo</span>
                <span>色々な色について</span>
            </div>
        </router-link>
        <router-link :to="{
                path: '/all',
            }"
            :style="{'color': theme.color}"
            class="txt-lang-hover">
            <div>
                <span>瀏覽全部相片</span>
                <span>全ての写真</span>
            </div>
        </router-link>
    </nav>
</template>

<style scoped>
nav a {
    text-decoration: none;
}
</style>