<script>
import { ref, provide } from 'vue';
import gsap from 'gsap';
import axios from 'axios';
const CSV_URL = "/iroironairo/data.csv";

export default {
  name: "App",
  setup() {
    // 地點分群
    const Kansai = [
      "神戶",
      "京都",
      "大阪",
      "港島",
      "神戶港",
      "三宮",
      "六甲",
      "摩耶山",
      "ポートアイランド",
      "兵庫",
      "和歌山",
    ];
    
    const data = ref([]);

    axios.get(CSV_URL)
      .then((response) => {
        let raw_d = response.data.replace("\r", "").split("\n")
        let cols = raw_d[0].split(",")
        raw_d.shift()
        raw_d.forEach(d => {
          const parts = [];
          let currentPart = '';
          let withinBracket = false;

          for (const char of d) {
            if (char === '[') {
              withinBracket = true;
            } else if (char === ']') {
              withinBracket = false;
            }

            if (char === ',' && !withinBracket) {
              parts.push(currentPart.trim());
              currentPart = '';
            } else {
              currentPart += char;
            }
          }

          if (currentPart) {
            parts.push(currentPart.trim());
          }

          let obj = {}
          for (let i = 0; i < cols.length; i++) {
            if (cols[i] == 'colors' && parts[i]) {
              let colorString = parts[i].replace(/'/g, '"')
              parts[i] = JSON.parse(colorString.slice(1, -1))
              obj['main_color'] = parts[i][0]
            }
            if (cols[i] == 'places' && parts[i]) {
              let placeString = parts[i].replace(/'/g, '"')
              if (placeString.indexOf(',') !== -1) {
                parts[i] = JSON.parse(placeString.slice(1, -1))
              } else {
                parts[i] = JSON.parse(placeString)
              }
            }
            obj[cols[i]] = parts[i]
          }
          data.value.push(obj)
        })
        data.value.forEach(d => {
          if (d.date){
            d.date = d.date.replace(/:/g, '/')
          }
          if (d.time){
            d.time = d.time.replace(/:[^:]*$/, '')
          }
          if (d.places){
            d["area"] = "other"
            for (let i = 0; i<d.places.length; i++){
              let p = d.places[i];
              if (Kansai.includes(p)) {
                d["area"] = "kansai";
                break;
              }
            }
          }
        })
        console.log("讀取本地 CSV 成功")
      })
      .catch((error) => {
        console.error(error);
      });

      
    provide('csvData', data);
    return {
      data
    }
  },
  methods: {
    onEnter(){
      console.log("--------Start transition---------")
      const el = this.$refs.container
      gsap.to(".fusuma", {
        delay: 2,
        duration: .5,
        opacity: 0,
        x: "100%",
        stagger: {
          amount: .2,
          from: 'end'
        },
        onComplete: () => { el.style['z-index'] = '-1' }
      })
    },
    onLeave(){
      console.log("--------Leave transition--------")
      console.log("切換分頁時執行")
      const el = this.$refs.container
      gsap.to(el, {
        duration: .5,
        opacity: 1,
      })
      gsap.set(el, {
        'z-index': 1030
      })
      gsap.to(".fusuma", {
        duration: .5,
        opacity: 1,
        stagger: .2,
        x: 0
      })
    }
  }
};
</script>

<template>
  <!-- Transition -->
  <section ref="container" class="vw-100 vh-100 position-fixed top-0 fusuma-container">
      <div class="fusuma"></div>
      <div class="fusuma"></div>
      <div class="fusuma"></div>
  </section>
  <router-view v-slot="{ Component }">
    <!-- <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition> -->
    <transition
    @enter="onEnter"
    @leave="onLeave">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style scoped>
.fusuma-container{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    z-index: 1030;
}
.fusuma{
    background-color: brown;
}
</style>