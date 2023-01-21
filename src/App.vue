<script setup>
  import p5Canvas from './components/p5Canvas.vue'
  import selectImg from './components/selectImg.vue';
  import viewImg from './components/viewImg.vue';
  import selectScale from './components/selectScale.vue';
  import {ref, provide} from 'vue'
  const sampling = ref(20)
  provide('sampling', sampling)
  const imgNum = ref(1)
  function prevImg(){
    if (imgNum.value > 1){
      imgNum.value--
    }else{imgNum.value = 1}
  }

  function nextImg(){
    imgNum.value++
  }

  function randomImg(){
    let [max, min] = [5,1];
    imgNum.value = Math.floor(Math.random() * (max - min) + min)
  }
</script>

<template>
  <main>
    <p5Canvas :imgNum="imgNum"/>
    <div>
      <h1>色色な色</h1>
      <h2>iroironairo</h2>
      <viewImg :img-num="imgNum"/>
      <selectScale/>
      <selectImg :img-num="imgNum" @prev-img="prevImg" @next-img="nextImg" @random-img="randomImg" />
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
}
</style>
