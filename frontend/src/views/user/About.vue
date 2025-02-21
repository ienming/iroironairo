<script setup>
import Bookmark from "@/components/Bookmark.vue";
import Navigator from "@/components/Navigator.vue";
</script>
<template>
    <main>
        <section class="min-vh-100 d-flex justify-content-center align-items-lg-center ff-serif">
            <section class="row flex-column w-100 pt-7 px-1 px-lg-6 pt-lg-0 gap-5 gap-lg-0">
                <section class="col-12 col-lg-6 d-flex align-items-center pt-4 pt-lg-0 mb-0 mb-lg-5">
                    <div class="col-lg-8">
                        <h2 class="fs-6">iroironairo</h2>
                        <h1 class="fw-semibold mt-2 mb-3 d-flex align-items-center gap-1">
                            <span>色々な色</span>
                            <img
                                src="/favicon.png"
                                alt="logo" />
                        </h1>
                    </div>
                </section>
                <section class="col-12 col-lg-6">
                    <p>
                        「色々な色」這個計畫是將我在日本作為交換學生的半年間，所玩所見的照片整理起來的資料視覺化作品。
                    </p>
                    <p>
                        「色々」有「很多、各式各樣」的意思，而「色々な色」則是指「各式各樣的色彩、色彩斑斕」。 起初這個詞是在神戶大學「中級會話」課程的期中考中，自我介紹時無意間講出來的詞。因為發音很有趣、有某種回文的韻味，於是有了「以顏色為主題紀錄交換生活」的想法。
                    </p>
                    <p>
                        透過萃取照片中的顏色並整理後，它們呈現我在那段時間生活、旅遊、第一次在異國長時間居住時，所看見與自己背景文化的差異。也代表我關注、喜歡，且一直注視的那些重複的主題和色彩，並以此構成我的經驗與記憶。
                    </p>
                    <p
                        class="text-end mt-8"
                        style="font-size: 12px;">
                        Copyright © 2023 Lucien Hsieh
                    </p>
                </section>
            </section>
        </section>
        <!-- Bookmark -->
        <bookmark class="position-fixed top-0 d-flex align-items-center gap-1" />
        <!-- Nav -->
        <navigator />
    </main>
</template>

<style scoped>
.txt-lang-container i {
    font-size: 12px;
    padding-left: 4px;
    opacity: 0.85;
}
</style>