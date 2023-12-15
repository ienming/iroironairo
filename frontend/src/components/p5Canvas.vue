<script setup>
import { onMounted, ref } from 'vue'
import { diff, closest } from 'color-diff';
let [draw, sample, reorder, findMainColor, data, mainCs] = [undefined, undefined, undefined, undefined, undefined, []]

const props = defineProps({
  "photoName": {
    default: ""
  },
  "canvasWidth": {
    default: window.innerWidth
  },
  "canvasHeight": {
    default: window.innerHeight
  }
})
const emit = defineEmits(['main-colors-handler'])

// 測試用 hardcode
const sampling = ref(25)
const nowOrder = ref('lightness')

// if the img is changed
// watch(props, (newValue, oldValue)=>{
//   // console.log("p5: imgNum props changed to "+newValue.imgNum)
//   sample()
// })

// Change sampling number
// const sampling = inject('sampling')
// watch(sampling, (newValue, oldValue)=>{
//   sample()
//   reorder()
//   draw()
// })

// Change order by
// const nowOrder = inject('order')
// watch(nowOrder, (newValue, oldValue)=>{
//   reorder()
//   draw()
// })

function colorDifference(color1, color2) {
  let result = diff(color1, color2)
  return result;
}

// p5
import p5 from "p5";

const script = function (p5) {
  let canvas;
  let canvasW = props.canvasWidth
  let canvasH = props.canvasHeight
  let cs = [];
  let [pct, dWidth, dHeight] = [0.25, 0, 0];

  // p5 Setup
  p5.setup = (_) => {
    canvas = p5.createCanvas(canvasW, canvasH)
    canvas.parent("p5Canvas")
    p5.background(220)
    sample()
  };

  // draw
  draw = function () {
    // clear
    p5.clear()
    p5.noStroke()
    // draw
    for (let i = 0; i < cs.length; i++) {
      p5.fill(cs[i].r, cs[i].g, cs[i].b)
      p5.rect(0, i * window.innerHeight / cs.length, canvasW, window.innerHeight / cs.length)
    }
  };

  // sampling color
  sample = function () {
    // clear cs
    cs.length = 0
    p5.loadImage(new URL(`../assets/photos/${props.photoName}.jpg` || `../assets/photos/${props.photoName}.JPG`, import.meta.url).href,
      img => {
        p5.image(
          img,
          0,
          0,
          img.width * pct,
          img.height * pct,
          0,
          0,
          img.width,
          img.height,
          p5.CONTAIN
        );
        dWidth = img.width * pct;
        dHeight = img.height * pct;
        // start sampling
        for (let i = 0; i < sampling.value; i++) {
          for (let j = 0; j < sampling.value; j++) {
            let [x, y] = [
              dWidth / (sampling.value * 2) + (dWidth / sampling.value) * i,
              dHeight / (sampling.value * 2) + (dHeight / sampling.value) * j,
            ];
            let c = p5.get(x, y);
            let [h, s, l] = [p5.hue(c), p5.saturation(c), p5.lightness(c)];
            let [r, g, b] = [p5.red(c), p5.green(c), p5.blue(c)];
            let obj = {
              h: p5.int(h),
              s: p5.int(s),
              l: p5.int(l),
              r: p5.int(r),
              g: p5.int(g),
              b: p5.int(b),
            };
            cs.push(obj);
          }
        }
        findMainColor()
        reorder()
        draw()
      }
    )
  }

  reorder = function () {
    // reorder cs
    switch (nowOrder.value) {
      case "hue":
        cs.sort(function (a, b) {
          return a.h - b.h;
        });
        break;
      case "lightness":
        cs.sort(function (a, b) {
          return b.l - a.l;
        });
        break;
      case "saturation":
        cs.sort(function (a, b) {
          return b.s - a.s;
        });
        break;
    }
    console.log("reorder")
    // console.log(cs);
  }

  findMainColor = function () {
    mainCs = []
    // start sampling
    for (let i = 0; i < 100; i++) {
      for (let j = 0; j < 100; j++) {
        let [x, y] = [
          dWidth / (100 * 2) + (dWidth / 100) * i,
          dHeight / (100 * 2) + (dHeight / 100) * j,
        ];
        let c = p5.get(x, y);
        let [h, s, l] = [p5.hue(c), p5.saturation(c), p5.lightness(c)];
        let colorRGB = {
          "R": p5.red(c),
          "G": p5.green(c),
          "B": p5.blue(c)
        }

        // match main color
        let threshold = 18;
        if (mainCs.length > 0){
          const palette = mainCs.map(color => color.color_rgb)
          // console.log(palette)
          const now = colorRGB
          const nearest = closest(now, palette)
          if (colorDifference(now, nearest) <= threshold){
            const middle = {
              "R": (nearest['R']+now['R'])/2,
              "G": (nearest['G']+now['G'])/2,
              "B": (nearest['B']+now['B'])/2,
            }
            const middle_p5 = p5.color(middle['R'], middle['G'], middle['B'])
            const target = mainCs.find(color => JSON.stringify(color.color_rgb) === JSON.stringify(nearest))
            target.color = [p5.hue(middle_p5), p5.saturation(middle_p5), p5.lightness(middle_p5)]
            target.color_rgb = middle
            target.amount += 1;
          }else{
            mainCs.push({ color: [h, s, l], color_rgb: colorRGB, amount: 1 });
          }
        }else{
          mainCs.push({ color: [h, s, l], color_rgb: colorRGB, amount: 1 });
        }
      }
    }
    mainCs = mainCs.sort((a, b) => b.amount - a.amount)
    if (mainCs.length > 3) {
      mainCs.length = 3
    }
    console.log('find main colors')
    console.log(mainCs)
    emit('main-colors-handler', mainCs)
  }
};

onMounted(() => {
  new p5(script)
})
</script>

<template>
  <div id="p5Canvas"></div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}
</style>