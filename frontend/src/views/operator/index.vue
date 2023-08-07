<script setup>
  import {onMounted, ref} from 'vue'
  import axios from 'axios'

  
  const nowPage = ref(1)
  // Fetch all photos from db through API
  const dataLoading = ref(true)
  const data = ref([])
  const API_URL = 'http://127.0.0.1:3000'
  
  function fetchPhotos(){
    axios.get(`${API_URL}/fetch_all_photos`, {
      params: {
        page: nowPage.value
      }
    })
    .then((response) => {
      response.data.forEach(d => {
        data.value.push(d)
      })
      dataLoading.value = false
      nowPage.value += 1
    })
      .catch((error) => {
        console.error(error);
      });
  }

  onMounted(()=>{
    fetchPhotos()
  })
</script>

<template>
  <main>
    <h1>Hello 後台頁面</h1>
    <v-btn @click="fetchPhotos">載入更多</v-btn>
    <div>
      <p v-if="dataLoading">載入中...</p>
      <v-table v-else>
        <thead>
          <th>照片</th>
          <th>拍攝時間</th>
          <th>主要顏色</th>
          <th>說明</th>
          <th>編輯</th>
          <th>URL</th>
        </thead>
        <tbody>
          <tr v-for="d of data" :key="d.id">
            <td>{{ d.name }}</td>
            <td>{{ d.date }}</td>
            <td v-if="d.colors" class="d-flex align-center">
              <div v-for="color of d.colors" class="main-cs"
              :style="{ 'background-color': 'hsl(' + color.h + ',' + color.s + '%,' + color.l + '%)' }">
              </div>
            </td>
            <td v-else>尚未儲存</td>
            <td v-if="d.description">{{ d.description.slice(0, 10)+'...' }}</td>
            <td v-else>尚無說明</td>
            <td>
              <router-link :to="{
                path: '/operator_edit',
                query: {
                  name: d.name
                }}"
                target="_blank"
              class="text-teal-lighten-1">編輯</router-link>
            </td>
            <td><a :href="d.url_google" target="_blank">連結</a></td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.main-cs {
  height: 15px;
  width: 15px;
  border-radius: 50%;
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
