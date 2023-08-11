<script setup>
import p5Canvas from '../../components/p5Canvas.vue'
// import selectImg from '../components/selectImg.vue';
// import viewImg from '../components/viewImg.vue';
// import selectScale from '../components/selectScale.vue';
// import selectOrder from '../components/selectOrder.vue';
// import showMainColor from '../components/showMainColor.vue';
// import showData from '../components/showData.vue';
import { ref, onMounted } from 'vue'


// UI
const articleBgObj = ref({})
const cavansWidth = ref(window.innerWidth / 2)

let mainColors = ref({})
function showMainColors(colors) {
  let obj = {}, arr = []
  colors.forEach(c => {
    obj.h = Math.floor(c.color[0])
    obj.s = Math.floor(c.color[1])
    obj.l = Math.floor(c.color[2])
    arr.push(obj)
    obj = {}
  })
  mainColors.value = arr

  // Update article bg color
  articleBgObj.value = {
    backgroundColor: `hsl(${mainColors.value[0]['h']},${mainColors.value[0]['s']}%,${mainColors.value[0]['l']}%)`
  }
}

// const sampling = ref(20)
// const order = ref('lightness')
// provide('sampling', sampling)
// provide('order', order)
// const imgNum = ref(1)
// const photoNum = 18

// function prevImg(){
//   if (imgNum.value > 1){
//     imgNum.value--
//   }else{imgNum.value = photoNum}
// }

// function nextImg(){
//   if (imgNum.value < photoNum){
//     imgNum.value ++
//   }else{
//     imgNum.value = 1
//   }
// }

// function randomImg(){
//   let [max, min] = [photoNum,1];
//   imgNum.value = Math.floor(Math.random() * (max - min) + min)
// }
//   ---------------------------------------編輯的功能 0803----------------
import { useRoute } from 'vue-router';
import axios from 'axios'
const API_URL = 'http://127.0.0.1:3000'
const route = useRoute();

const photo = ref({})
const description = ref("")
const photoLoading = ref(true)

// Place
const place = ref("")
const places = ref([])
const addShotPlace = function(){
  places.value.push(place.value)
  place.value = ""
}

function getPhoto() {
  axios.get(`${API_URL}/fetch_photo/`, {
    params: {
      name: route.query.name
    }
  })
    .then((response) => {
      // 處理後端回傳的資料
      console.log(response)
      photo.value = response.data
      photoLoading.value = false
      if (photo.value.description) {
        description.value = photo.value.description
      }
      if (photo.value.places) {
        places.value = photo.value.places
      }
    })
    .catch((error) => {
      // 處理錯誤
      console.error(error);
    });
}

// Update data
function updateData() {
  console.log("Update data to backend")
  console.log(description.value, mainColors.value, photo.value.name)
  axios.post(`${API_URL}/update_photo/`, {
    name: photo.value.name,
    description: description.value,
    colors: mainColors.value,
    places: places.value
  })
    .then((response) => {
      // 處理後端回傳的資料
      console.log(response)
      alert("資料更新成功！")
    })
    .catch((error) => {
      // 處理錯誤
      console.error(error);
    });
}

function removePlace(target){
  let result = places.value.filter((place)=>place !== target)
  places.value = result
  updateData()
}

onMounted(() => {
  getPhoto()
})
</script>

<template>
  <main>
    <div>
      <div style="padding-top: 100px;">
        <nav class="top-nav px-3">
          <p class="mb-4">
            <router-link :to="{
              path: '/operator'
            }" class="text-teal-lighten-1">&lt;返回</router-link>
          <h1 class="d-inline ml-2 text-h6">修改照片資訊：{{ route.query.name }}</h1>
          </p>
        </nav>
        <p v-if="photoLoading">正在取得照片...</p>
        <article v-else>
          <img :src="photo.url_google" alt="" class="photo" />
          <div class="mb-4">
            <p class="mb-2">拍攝日期: {{ photo.date }}</p>
            <p class="mb-2">拍攝時間: {{ photo.time }}</p>
            <p class="mb-2">拍攝地點: </p>
            <div>
              <p v-for="place of places">{{ place }} <span @click="removePlace(place)">Delete</span></p>
            </div>
            <p class="mb-2">文字說明: {{ description }}</p>
          </div>
          <div :style="{ 'background-color': 'hsl(' + color.h + ',' + color.s + '%,' + color.l + '%)' }"
            class="main-cs" v-for="color of mainColors"></div>
          <hr />
          <div>
            <label for="inpt_place">
              <input type="text" id="inpt_place" v-model="place"/>
            </label>
            <button @click="addShotPlace">新增拍攝地點</button>
          </div>
          <label for="#inpt_descript">
            <p>文字說明</p>
            <textarea id="inpt_descript" v-model="description"></textarea>
          </label>
          <button class="bg-indigo-darken-1" @click.prevent="updateData">
            更新資訊
          </button>
        </article>
      </div>
      <div style="position: fixed; top: 0; right: 0;">
        <p5Canvas :photo-name="route.query.name" :canvas-width="cavansWidth" @main-colors-handler="showMainColors" />
      </div>
    </div>
  </main>
</template>

<style scoped>
p {
  word-wrap: break-word;
}

header {
  line-height: 1.5;
}

.photo {
  max-width: 250px;
}

.main-cs {
  height: 50px;
  width: 100%;
  margin: 0 3px;
  border-radius: 4px;
  cursor: pointer;
  transition: all .5s ease
}

.main-cs:hover {
  opacity: .5;
}

.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  background-color: rgba(255, 255, 255, .5);
  backdrop-filter: blur(4px);
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

.wrapper {
  padding: 30px;
}
</style>