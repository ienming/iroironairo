<script setup>
  import {ref} from 'vue'
  import axios from 'axios'

  
  const nowPage = ref(0)
  // Fetch all photos from db through API
  const dataLoading = ref(false)
  const data = ref([])
  const API_URL = 'http://127.0.0.1:3000'
  
  function fetchPhotos(){
    dataLoading.value = true
    axios.get(`${API_URL}/fetch_all_photos`, {
      params: {
        page: nowPage.value
      }
    })
    .then((response) => {
      data.value = response.data
      dataLoading.value = false
      // 無限載入
      // response.data.forEach(d => {
        // data.value.push(d)
      // })
      // nowPage.value += 1
    })
      .catch((error) => {
        console.error(error);
      });
  }
</script>

<template>
  <main class="main mx-auto">
    <div class="mt-5 mb-4">
      <h1 class="fs-4">色々な色 照片資料管理</h1>
      <h2 class="fs-5">iroironairo</h2>
      <!-- <button @click="readFromCSV">測試讀取CSV檔案</button> -->
    </div>
    <div class="mb-4 form-floating">
      <select name="" id="floatingSelect" class="form-select" v-model="nowPage" @change="fetchPhotos">
        <option value="0" disabled>上次處理到...</option>
        <option :value="i" v-for="i of 28">{{ `${50*(i-1)+1}-${50*i}筆` }}</option>
      </select>
      <label for="floatingSelect">讀取資料</label>
    </div>
    <div class="mb-5">
      <p v-if="dataLoading">載入中...</p>
      <table v-else class="table table-hover table-striped">
        <thead>
          <th>照片</th>
          <th>拍攝時間</th>
          <th>拍攝地點</th>
          <th>代表顏色</th>
          <th>說明</th>
          <th>編輯</th>
          <th>URL</th>
        </thead>
        <tbody>
          <tr v-for="d of data" :key="d.id">
            <td>{{ d.name.slice(0, 8) }}</td>
            <td>{{ d.date }}</td>
            <!-- Places -->
            <td v-if="d.places">
              <span v-for="(place,id) of d.places">
                <span>{{ place }}</span>
                <span v-if="id+1 !== d.places.length">、</span>
              </span>
            </td>
            <td v-else>尚未儲存</td>
            <!-- Colors -->
            <td v-if="d.colors" class="d-flex align-center">
              <div v-for="color of d.colors" class="main-cs"
              :style="{ 'background-color': 'hsl(' + color.h + ',' + color.s + '%,' + color.l + '%)' }">
              </div>
            </td>
            <td v-else>尚未儲存</td>
            <!-- Description -->
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
      </table>
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
</style>
