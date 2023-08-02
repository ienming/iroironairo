<script setup>
  import p5Canvas from '../components/p5Canvas.vue'
  import selectImg from '../components/selectImg.vue';
  import viewImg from '../components/viewImg.vue';
  import selectScale from '../components/selectScale.vue';
  import selectOrder from '../components/selectOrder.vue';
  import showMainColor from '../components/showMainColor.vue';
  import showData from '../components/showData.vue';
  import {ref, provide} from 'vue'
  import axios from 'axios'

  const sampling = ref(20)
  const order = ref('lightness')
  provide('sampling', sampling)
  provide('order', order)
  const imgNum = ref(1)
  const photoNum = 18

  function prevImg(){
    if (imgNum.value > 1){
      imgNum.value--
    }else{imgNum.value = photoNum}
  }

  function nextImg(){
    if (imgNum.value < photoNum){
      imgNum.value ++
    }else{
      imgNum.value = 1
    }
  }

  function randomImg(){
    let [max, min] = [photoNum,1];
    imgNum.value = Math.floor(Math.random() * (max - min) + min)
  }

  // 0802
  // fetch photos data from db through API
  const API_URL = 'http://127.0.0.1:3000'
  axios.get(`${API_URL}/fetch_all_photos`)
    .then((response) => {
      // 處理後端回傳的資料
      console.log(response.data);
    })
    .catch((error) => {
      // 處理錯誤
      console.error(error);
    });
</script>

<template>
  <main>
    <p5Canvas :imgNum="imgNum"/>
    <section id="descripPanel">
      <viewImg :img-num="imgNum"/>
      <showMainColor :img-num="imgNum"/>
      <showData />
    </section>
    <aside id="controlPanel">
      <selectScale/>
      <selectOrder/>
      <selectImg :img-num="imgNum" @prev-img="prevImg" @next-img="nextImg" @random-img="randomImg" />
    </aside>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
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

main{
  display: flex;
  justify-content: space-between;
}
</style>
