<script setup>
  import {ref} from 'vue'
  import axios from 'axios'

  // Fetch all photos from db through API
  const dataLoading = ref(true)
  const data = ref([])
  const API_URL = 'http://127.0.0.1:3000'
  axios.get(`${API_URL}/fetch_all_photos`)
    .then((response) => {
      data.value = response.data
      dataLoading.value = false
    })
    .catch((error) => {
      console.error(error);
    });
</script>

<template>
  <main>
    <h1>Hello 後台頁面</h1>
    <div>
      <p v-if="dataLoading">載入中...</p>
      <div v-else>
        <div v-for="d of data" :key="d.id">
        <router-link :to="{
          path: '/operator_edit',
          query: {
            name: d.name
          }}"
          class="text-teal-lighten-1">前往後台編輯頁面</router-link>
          <p>{{ d }}</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}

main{
  display: flex;
  justify-content: space-between;
}
</style>
