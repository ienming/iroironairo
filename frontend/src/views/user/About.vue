<script setup>
import Bookmark from "@/components/Bookmark.vue";
import Navigator from "@/components/Navigator.vue";
</script>
<template>
    <main>
        <section class="min-vh-100 d-flex justify-content-center align-items-center ff-serif">
            <section class="row flex-column flex-lg-row w-100 px-1 px-lg-6">
                <section class="col-6">
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
                <section class="col-6">Description</section>
            </section>
        </section>
        <!-- Bookmark -->
        <bookmark class="position-fixed top-0 d-flex align-items-center gap-1"></bookmark>
        <!-- Nav -->
        <navigator class="position-fixed top-0 end-0 pe-4"></navigator>
    </main>
</template>