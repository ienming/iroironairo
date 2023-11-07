<script setup>
import Bookmark from "@/components/Bookmark.vue";
import Navigator from "@/components/Navigator.vue";
</script>
<template>
    <main>
        <section class="min-vh-100 d-flex justify-content-center align-items-center ff-serif">
            <section class="row flex-column flex-lg-row w-100 px-1 px-lg-6">
                <section class="col-12 col-lg-6 d-flex align-items-center">
                    <div class="col-lg-8">
                        <h2 class="fs-6">iroironairo</h2>
                        <h1 class="fw-semibold mt-2 mb-3">色々な色</h1>
                        <h3
                        class="d-flex flex-grow align-items-center opacity-50"
                        style="font-size: 14px"
                        >
                        <span>2022.09.28</span>
                        <div style="height: 1px" class="w-100 bg-dark mx-2"></div>
                        <span>2023.03.24</span>
                        </h3>
                    </div>
                </section>
                <section class="col-12 col-lg-6">
                    <p>「色々な色 (iroironairo)」是一個以色彩為主題的資料視覺化計畫。「色々」有「很多、各式各樣」的意思，
                        而「色々な色」則是指「各式各樣的色彩、色彩斑斕」。
                    </p>
                    <p>
                        「色々な色」是我將在日本生活所見、隨手拍下，整理起的相片中所萃取出的顏色，它們代表了這段時間過於龐大、難以整理的瑣碎生活，也暗示我在什麼時間、去了哪裡時，看見了這樣的色彩，並組合成那段時光的記憶。
                    </p>
                </section>
            </section>
        </section>
        <!-- Bookmark -->
        <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
        <!-- Nav -->
        <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
    </main>
</template>