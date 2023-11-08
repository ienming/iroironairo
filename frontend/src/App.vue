<script>
import { ref, provide, nextTick } from 'vue';
import { useRouter } from 'vue-router'
import { hsl2Hex } from "@/composable/common";
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
        // console.log("讀取 CSV")
      })
      .catch((error) => {
        console.error(error);
      });
    
    provide('csvData', data);
      
    const router = useRouter()
    router.beforeEach((to, from) => {
      console.log(`From ${from.path} to ${to.path}`)
    })

    return {
      data,
    }
  },
  methods: {
    onBeforeEnter(){
      const url = new URL(window.location.href).href
      const containerDom = this.$refs.container
      const fusumas = containerDom.querySelectorAll(".fusuma")
      // 如果是透過顏色搜尋
      const colorParam = url.match(/color=([^&]+)/);
      const photoParam = url.match(/photo=([^&]+)/)
      if (colorParam) {
        const color = decodeURIComponent(colorParam[1].replace(/%22/g, '"'));
        const colorObj = JSON.parse(color)
        Array.from(fusumas).forEach(fusuma => {
          fusuma.style['background-color'] = hsl2Hex(colorObj.h, colorObj.s, colorObj.l)
        })
      }else if(photoParam){
        const name = decodeURIComponent(photoParam[1].replace(/%22/g, '"'));
        const colorObj = this.data.find(d => d.name == name.slice(1, -1))['main_color']
        Array.from(fusumas).forEach(fusuma => {
          fusuma.style['background-color'] = hsl2Hex(colorObj.h, colorObj.s, colorObj.l)
        })
      }else{
        Array.from(fusumas).forEach(fusuma => {
          fusuma.style['background-color'] = '#f6f6f6'
        })
      }
    },
    onEnter(){
      console.log("--------Start transition---------")
      const containerDom = this.$refs.container
      const fusumas = containerDom.querySelectorAll(".fusuma")
      gsap.to(fusumas, {
        delay: 2,
        duration: .5,
        opacity: 0,
        x: "100%",
        stagger: {
          each: .05,
          from: 'end'
        },
        onComplete: () => { 
          containerDom.style['z-index'] = '-1' 
        }
      })
    },
    onBeforeLeave(){
      console.log("--------Before leave transition--------")
      // console.log("切換分頁時執行")
      const el = this.$refs.container
      gsap.set(el, {
        'z-index': 1030
      })
      const containerDom = this.$refs.container
      const fusumas = containerDom.querySelectorAll(".fusuma")
      gsap.to(fusumas, {
        duration: .5,
        opacity: 1,
        stagger: .05,
        x: 0,
        // delay: 0.55
      })
    }
  },
  mounted(){
    // Get colors for enter animation
    let timer = window.setInterval(()=>{
      const els = document.querySelector("#logoContainer").querySelectorAll(".fusuma")
      Array.from(els).forEach(el => {
        const randomIndex = Math.floor(Math.random()*this.data.length+1)
        const color = this.data[randomIndex]['main_color']
        el.style['background-color'] = hsl2Hex(color.h, color.s, color.l)
      })
    }, 500)
    // GSAP animation
    const logoTypeJp = this.$refs.logoTypeJp
    const logoTypes = Array.from(logoTypeJp.querySelectorAll("span"))
    const first = logoTypes.shift()
    const rests = logoTypes
    const master = gsap.timeline({
      delay: .5,
    })
    const [offset, kerning] = [30, 6]
    let tl_intro = gsap.timeline().fromTo(first, {
      opacity: 0,
      scale: 5
    }, {
      opacity: 1,
      scale: 1,
      duration: 1,
    })
    .to(first, {
      x: `-${offset*2+kerning*4}px`,
      duration: .5,
      onComplete: ()=>{
        clearInterval(timer)
        const el = document.querySelector("#logoContainer")
        el.style.color = '#333'
        const fusumas = el.querySelectorAll(".fusuma")
        for (let i=0; i<fusumas.length; i++){
          if (i == 4 ){
            Array.from(fusumas)[i].style['background-color'] = "#f6f6f6"
          }
        }
        const els = document.querySelector("#logoContainer").querySelectorAll("span")
        Array.from(els).forEach(el => {
          el.style['background-color'] = 'transparent'
        })
      }
    })

    let tl_rest = gsap.timeline().fromTo(logoTypes,{
      opacity: 0,
      x: i => {
        if (i == 0){
          return `-${offset+kerning*2}px`
        }else if (i == 1){
          return `0px`
        }else if (i == 2){
          return `${offset+kerning*2}px`
        }
      },
      y: `${offset}px`
    }, {
      opacity: 1,
      stagger: .2,
      y: 0
    })

    const logoEng = this.$refs.logoContainer.querySelector("h2")
    let tl_eng = gsap.timeline().fromTo(logoEng, {
      opacity: 0,
      y: `${offset*2}px`
    }, {
      opacity: 1,
      y: `${offset+kerning*2}px`,
      duration: .5
    })

    const logoContainer = this.$refs.logoContainer
    const logoFusumas = logoContainer.querySelectorAll(".fusuma")
    let tl_fusuma = gsap.to(logoFusumas, {
        duration: .5,
        opacity: 0,
        x: "100%",
        stagger: {
          amount: .4,
          from: 'end'
        },
        onComplete: () => { logoContainer.style['z-index'] = '-1' }
      })

    let tl_text_fade = gsap.to(logoContainer.querySelector("div"), {
      opacity: 0,
      duration: .5,
      x: "100%"
    })

    // 
    master
      .add(tl_intro)
      .add(tl_rest, "-=1")
      .add(tl_eng, "-=1")
      .add(tl_fusuma, "+=2")
      .add(tl_text_fade, "-=1")
  }
};
</script>

<template>
  <!-- Logo -->
  <section id="logoContainer" ref="logoContainer" class="ff-serif position-fixed">
    <div class="d-flex flex-column align-items-center position-absolute top-50 start-50 translate-middle">
      <h1 class="position-relative" ref="logoTypeJp">
        <span class="position-absolute d-inline-block">色</span>
        <span class="position-absolute d-inline-block">々</span>
        <span class="position-absolute d-inline-block">な</span>
        <span class="position-absolute d-inline-block">色</span>
      </h1>
      <h2 class="fs-4">iroironairo</h2>
    </div>
    <section class="vw-100 vh-100 fusuma-container">
      <div class="fusuma" v-for="n of 9"></div>
    </section>
  </section>
  <!-- Transition -->
  <section ref="container" class="vw-100 vh-100 position-fixed top-0 fusuma-container">
      <div class="fusuma" v-for="n of 9"></div>
  </section>
  <router-view v-slot="{ Component }">
    <transition
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @before-leave="onBeforeLeave" name="page-fade">
      <component :is="Component"/>
    </transition>
  </router-view>
</template>

<style scoped>
#logoContainer{
  z-index: 1060;
}
#logoContainer>.fusuma-container{
  grid-template-columns: repeat(3, 1fr);
}
.fusuma-container{
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    z-index: 1030;
}
.fusuma{
    background-color: #F6F6F6;
}
</style>