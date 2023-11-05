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
                    <p>終於來到做完的這一天，距離發起這個專案過了快要一年。「色々な色 (iroironairo)」是一個以色彩為主題的資料視覺化計畫，起初是在去年（2022）的 11/30 號，
                        我在神戶大學修讀「中級會話」時，期中考需要自我介紹，而我在現場臨機應變時脫口而出「色々な色」這個像回文一樣的句子。「色々」有「很多、各式各樣」的意思，
                        而「色々な色」則是指「各式各樣的色彩、色彩斑斕」。
                    </p>
                    <p>
                        在日本待的半年期間，玩的時間比上課多，多的是體驗不同的生活、聽不懂的語言、溫帶才有的氣候，和不同於台灣的顏色。作為收束從日本回來的記憶，有太多難以整理、消化的片段和零散的畫面與聲音，
                        即使只有半年。
                    </p>
                    <p>
                        「色々な色」是我將這半年在日本所見、隨手拍下，或特別感動珍藏的瞬間，整理起的相片中所萃取出的顏色，它們代表了這段時間過於龐大、難以整理的瑣碎生活。
                        這些感覺和片段或許不知道什麼時候才會消化，抑或是已經成為我的一部分，但都會是如同這樣各式各樣的色彩，與色彩斑斕的片段。
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