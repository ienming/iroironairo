<script setup>
import { watch, inject } from 'vue'
import { eventBus } from '../main.js'

let [draw, sample, reorder, findMainColor, data, mainCs] = [undefined, undefined, undefined, undefined, undefined, []]

// if the img is changed
const props = defineProps(['imgNum'])
watch(props, (newValue, oldValue)=>{
  console.log("p5: imgNum props changed to "+newValue.imgNum)
  sample()
})

// temporary Data to be interactive
const sampling = inject('sampling')
watch(sampling, (newValue, oldValue)=>{
  console.log("p5: imgNum sampling changed to "+newValue.imgNum)
  sample()
  reorder()
  draw()
})
const nowOrder = inject('order')
watch(nowOrder, (newValue, oldValue)=>{
  console.log("p5: imgNum nowOrder changed to "+newValue.imgNum)
  reorder()
  draw()
})

// p5
import p5 from "p5";

const script = function (p5) {
  let canvas;
  let canvasW = window.innerWidth
  let canvasH = window.innerHeight
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
  draw = function(){
    console.log("canvas draw image number: "+props.imgNum)
    // clear
    p5.clear()
    p5.noStroke()
    // draw
    for (let i=0; i<cs.length; i++){
      p5.fill(cs[i].r, cs[i].g, cs[i].b)
      p5.rect(0, i*window.innerHeight/cs.length, canvasW, window.innerHeight/cs.length)
    }
  };

  // sampling color
  sample = function(){
    // clear cs
    cs.length = 0
    p5.loadImage(new URL(`../assets/img/${props.imgNum}.jpg`, import.meta.url).href,
      img=>{
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
            //debug
            // p5.fill(0);
            // p5.circle(x, y, 0.25);
          }
        }
        findMainColor()
        reorder()
        draw()
      }
    )
  }

  reorder = function(){
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

  findMainColor = function(){
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

        // match main color
        let threshold = 10
        let temp = mainCs.find((el) => {
          return Math.abs(el.color[0] - h) <= threshold &&
          Math.abs(el.color[1] - s) <= threshold*3 &&
          Math.abs(el.color[2] - l) <= threshold*4;
        });

        if (!temp) {
            mainCs.push({ color: [h, s, l], amount: 1});  
        } else {
            temp.amount += 1; 
        }
      }
    }
    mainCs = mainCs.sort((a, b) => b.amount - a.amount)
    if (mainCs.length > 5){
      mainCs.length = 5
    }
    console.log('find main colors')
    console.log(mainCs)
    eventBus.emit('main-colors-evt', mainCs);
  }
};

new p5(script)
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