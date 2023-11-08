<script setup>
import { ref } from "vue";
const props = defineProps({
    theme: {
        type: Object,
        default: {
            "color": "#232323",
            "backgroundColor": "#F6F6F6"
        }
    }
})

const mobileMenuOpening = ref(false)
</script>

<template>
    <section class="position-fixed top-0 end-0 pt-4 pt-lg-0 pe-4">
        <div class="d-lg-none">
            <div class="rounded-pill p-3 d-flex justify-content-center align-items-center shadow-lg" style="width: 60px; height: 60px;"
            :style="{'background-color': theme.color, 'color': theme.backgroundColor}"
            @click="mobileMenuOpening = true">
                <i class="fa-solid fa-bars fa-xl" role="button"></i>
            </div>
        </div>
        <!-- Mobile -->
        <transition name="fade">
            <section v-show="mobileMenuOpening" class="position-fixed top-0 start-0 w-100 vh-100 luc-mobile-nav px-3"
            :style="{'background-color': theme.color}">
                <div class="mt-8 d-flex flex-column gap-5 ff-serif">
                    <router-link :to="{
                            path: '/'
                        }"
                        :style="{'color': theme.backgroundColor}"
                        @click="mobileMenuOpening = false">
                        <div class="d-flex align-items-center">
                            <span>首頁 ホーム</span>
                        </div>
                    </router-link>
                    <router-link :to="{
                            path: '/all',
                        }"
                        :style="{'color': theme.backgroundColor}"
                        @click="mobileMenuOpening = false">
                        <div class="d-flex align-items-center">
                            <span>全部相片 全ての写真</span>
                        </div>
                    </router-link>
                    <router-link :to="{
                            path: '/about'
                        }"
                        :style="{'color': theme.backgroundColor}"
                        @click="mobileMenuOpening = false">
                        <div class="d-flex align-items-center">
                            <span>關於 iroironairo 色々な色について</span>
                        </div>
                    </router-link>
                </div>
                <div @click="mobileMenuOpening = false" class="text-center d-flex justify-content-center position-fixed bottom-0 start-50 translate-middle-x pb-5">
                    <div class="rounded-pill p-3 d-flex justify-content-center align-items-center shadow-lg" style="width: 60px; height: 60px;"
                    :style="{'background-color': theme.backgroundColor, 'color': theme.color}">
                        <i class="fa-solid fa-xmark fa-xl" role="button"></i>
                    </div>
                </div>
            </section>
        </transition>
        <!-- Desktop -->
        <div>
            <nav class="d-flex gap-3 py-3 py-lg-4 ff-serif d-none d-lg-block" style="z-index: 1020;">
                <router-link :to="{
                        path: '/'
                    }"
                    :style="{'color': theme.color}"
                    class="txt-lang-hover">
                    <div>
                        <span>首頁</span>
                        <span>ホーム</span>
                    </div>
                </router-link>
                <router-link :to="{
                        path: '/all',
                    }"
                    :style="{'color': theme.color}"
                    class="txt-lang-hover">
                    <div>
                        <span>全部相片</span>
                        <span>全ての写真</span>
                    </div>
                </router-link>
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
            </nav>
        </div>
    </section>
</template>

<style scoped>
nav a {
    text-decoration: none;
}

.luc-mobile-nav{
    background-color: #f6f6f6;
    color: #232323;
}
</style>