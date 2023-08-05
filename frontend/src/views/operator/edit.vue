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
    })
    .catch((error) => {
      // 處理錯誤
      console.error(error);
    });
}


// Send data
function sendData() {
  console.log("Send data to backend")
  console.log(description.value, mainColors.value, photo.value.name)
  axios.post(`${API_URL}/update_photo/`, {
    name: photo.value.name,
    description: description.value,
    colors: mainColors.value
  })
    .then((response) => {
      // 處理後端回傳的資料
      console.log(response)
    })
    .catch((error) => {
      // 處理錯誤
      console.error(error);
    });
}

onMounted(() => {
  getPhoto()
})
</script>

<template>
  <div :style="articleBgObj" id="Article">
    <v-sheet class="wrapper" :elevation="4" rounded style="width: 80vw;">
      <v-container>
        <v-row justify="space-between">
          <v-col>
            <p class="mb-4">
              <router-link :to="{
            path: '/operator'
          }" class="text-teal-lighten-1">&lt;返回</router-link>
              <h1 class="d-inline ml-2 text-h6">修改照片資訊</h1>
            </p>
            <h2 class="text-h2">{{ route.query.name }}</h2>
          </v-col>
          <v-col>
            <div class="d-flex mr-2">
              <div :style="{ 'background-color': 'hsl(' + color.h + ',' + color.s + '%,' + color.l + '%)' }" class="main-cs"
                v-for="color of mainColors"></div>
            </div>
            <p5Canvas :photo-name="route.query.name" :canvas-width="45" :canvas-height="60"
              @main-colors-handler="showMainColors" />
          </v-col>
        </v-row>
        <v-divider class="my-4"></v-divider>
        <p v-if="photoLoading">正在取得照片...</p>
        <v-row v-else>
          <v-col>
            <form action="">
              <v-textarea label="照片說明" variant="filled" clearable clear-icon="mdi-close-circle"
                v-model="description"></v-textarea>
              <v-btn class="bg-indigo-darken-1 float-right" @click.prevent="sendData">
                更新資訊
              </v-btn>
            </form>
          </v-col>
          <v-col class="d-flex">
            <div>
              <p>拍攝日期: {{ photo.date }}</p>
              <p>拍攝時間: {{ photo.time }}</p>
              <p>文字說明: {{ description }}</p>
            </div>
            <img :src="photo.url_google" alt="" class="photo ml-3" />
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>
  </div>
</template>

<style scoped>
#Article {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

header {
  line-height: 1.5;
}
.photo {
  max-width: 250px;
}
.main-cs {
  height: 30px;
  width: 30px;
  margin: 0 3px;
  border-radius: 50%;
  cursor: pointer;
  transition: all .5s ease
}
.main-cs:hover {
  opacity: .5;
}

#descripPanel {
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /*  */
  position: fixed;
  left: 0;
  top: 0;
  background-color: #fff;
  padding: 12px;
}

#controlPanel {
  position: fixed;
  bottom: 0;
  left: 0;
  background-color: #fff;
  padding: 12px;
  width: 224px;
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

.wrapper{
  padding: 30px;
}
</style>