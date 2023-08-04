<script setup>
import p5Canvas from '../../components/p5Canvas.vue'
// import selectImg from '../components/selectImg.vue';
// import viewImg from '../components/viewImg.vue';
// import selectScale from '../components/selectScale.vue';
// import selectOrder from '../components/selectOrder.vue';
// import showMainColor from '../components/showMainColor.vue';
// import showData from '../components/showData.vue';
import { ref, onMounted } from 'vue'

let mainColors = ref({})
function showMainColors(colors){
  let obj = {}, arr = []
  colors.forEach(c => {
    obj.h = Math.floor(c.color[0])
    obj.s = Math.floor(c.color[1])
    obj.l = Math.floor(c.color[2])
    arr.push(obj)
    obj = {}
  })
  mainColors.value = arr
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
const route = useRoute();

const photo = ref({})
const photoLoading = ref(true)
function getPhoto() {
  const API_URL = 'http://127.0.0.1:3000'
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
  <div class="wrapper">
    <aside>
      <h1>後台編輯頁面</h1>
      <h2>照片：{{ route.query.name }}</h2>
      <p v-if="photoLoading">Loading photo...</p>
      <div v-else>
        <img :src="photo.url_google" alt="" class="photo" />
        <p>Image shot date: {{ photo.date }}</p>
        <p>Image shot time: {{ photo.time }}</p>
        <div class="d-flex">
          <div :style="{ 'background-color': 'hsl('+color.h+','+color.s+'%,'+color.l+'%)'}"
          class="main-cs"
          v-for="color of mainColors"></div>
        </div>
        <form action="">
          <textarea name="description" id="" cols="30" rows="10"></textarea>
          <button>Submit</button>
        </form>
      </div>
    </aside>
    <main>
      <p5Canvas :photo-name="route.query.name"
      @main-colors-handler="showMainColors"/>
      <!-- <section id="descripPanel">
                <viewImg :img-num="imgNum"/>
                <showMainColor :img-num="imgNum"/>
                <showData />
            </section>
            <aside id="controlPanel">
                <selectScale/>
                <selectOrder/>
                <selectImg :img-num="imgNum" @prev-img="prevImg" @next-img="nextImg" @random-img="randomImg" />
            </aside> -->
    </main>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.photo {
  max-width: 300px;
}

.main-cs{
  height: 30px;
  width: 30px;
  margin: 0 3px;
  border-radius: 50%;
  cursor: pointer;
  transition: all .5s ease
}

.main-cs:hover{
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

.wrapper {
  display: flex;
}
</style>