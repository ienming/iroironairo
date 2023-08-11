<script setup>
import p5Canvas from '../../components/p5Canvas.vue'
import modalLoading from '../../components/modalLoading.vue'
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
const updating = ref(false)
function updateData() {
  updating.value = true
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
      updating.value = false
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
}

onMounted(() => {
  getPhoto()
})
</script>

<template>
  <main>
    <div>
      <div class="card">
        <nav class="mb-4 d-flex justify-content-between">
          <router-link :to="{
            path: '/operator'
          }" class="text-teal-lighten-1">&lt;返回</router-link>
          <h1 class="d-inline ml-2 fs-6">修改照片資訊：{{ route.query.name }}</h1>
        </nav>
        <p v-if="photoLoading">正在取得照片...</p>
        <section v-else>
          <section>
            <img :src="photo.url_google" alt="" class="photo" />
            <div class="mt-2 mb-4">
              <p class="mb-3"><b>拍攝日期｜</b>{{ photo.date }}</p>
              <p class="mb-3"><b>拍攝時間｜</b>{{ photo.time }}</p>
              <p class="mb-3"><b>拍攝地點｜</b></p>
              <div class="d-flex gap-1">
                <p v-for="place of places" class="chip" @click="removePlace(place)">
                  <span>{{ place }}</span>
                </p>
              </div>
              <p class="mb-3"><b>文字說明｜</b>{{ description }}</p>
            </div>
            <div :style="{ 'background-color': 'hsl(' + color.h + ',' + color.s + '%,' + color.l + '%)' }"
              class="main-cs" v-for="color of mainColors"></div>
          </section>
          <hr />
          <section>
            <h2 class="fs-4">更新資料</h2>
            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="inpt_place" v-model="place"
              placeholder="照片拍攝地點：都道府縣、市...">
              <label for="inpt_place">拍攝地點</label>
              <button class="btn btn-primary mt-2" :disabled="place ? false : true"
              @click="addShotPlace">新增拍攝地點</button>
            </div>
            <div class="form-floating">
              <textarea class="form-control" placeholder="輸入照片當時的一些事情" id="inpt_descript"
              v-model="description" style="height: 150px"></textarea>
              <label for="inpt_descript">文字說明</label>
              <button class="d-block w-100 mt-2 btn btn-primary" @click.prevent="updateData">
                更新資訊
              </button>
            </div>
          </section>
        </section>
      </div>
      <div style="position: fixed; top: 0; right: 0;">
        <p5Canvas :photo-name="route.query.name" @main-colors-handler="showMainColors" />
      </div>
    </div>
  </main>
  <transition name="fade">
    <modalLoading v-if="updating"></modalLoading>
  </transition>
</template>

<style scoped>
p {
  word-wrap: break-word;
}

header {
  line-height: 1.5;
}

.card {
  position: relative;
  z-index: 99;
  background-color: #fff;
  max-width: 500px;
  padding: 30px;
  margin: 30px;
  border-radius:  12px;
}

.photo {
  max-width: 250px;
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