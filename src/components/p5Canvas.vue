<script setup>
// vue
let [draw, sample] = [undefined, undefined]
import {watch, inject} from 'vue'
const props = defineProps(['imgNum'])
watch(props, (newValue, oldValue)=>{
  console.log("p5: imgNum props changed to "+newValue.imgNum)
  sample()
})

// p5
import p5 from "p5";
const P5 = p5;

// temporary Data to be interactive
const sampling = inject('sampling')
watch(sampling, (newValue, oldValue)=>{
  console.log("p5: imgNum sampling changed to "+newValue.imgNum)
  sample()
})
let nowOrder = 'lightness'

const script = function (p5) {
  let [imgs, cs] = [[], []];
  let [pct, dWidth, dHeight] = [0.25, 0, 0];

  // p5 Preload
  p5.preload = (_) => {
    for (let i=0; i<5; i++){
      let img = p5.loadImage(`./src/assets/img/${i+1}.jpg`);
      imgs.push(img)
    }
  }

  // p5 Setup
  p5.setup = (_) => {
    let canvas = p5.createCanvas(window.innerWidth / 2, window.innerHeight);
    canvas.parent("p5Canvas")
    p5.background(220);
    sample()
  };


  // draw
  draw = function(){
    console.log("canvas draw image number: "+props.imgNum)
    // draw color
    for (let i=0; i<cs.length; i++){
      p5.fill(cs[i].r, cs[i].g, cs[i].b)
      p5.noStroke()
      p5.rect(0, i*window.innerHeight/cs.length, window.innerWidth/2, window.innerHeight/cs.length)
    }
  };

  // sampling color
  sample = function(){
    // clear cs
    cs.length = 0
    let num = props.imgNum-1
    dWidth = imgs[num].width * pct;
    dHeight = imgs[num].height * pct;
    // place image
    p5.image(
      imgs[num],
      0,
      0,
      imgs[num].width * pct,
      imgs[num].height * pct,
      0,
      0,
      imgs[num].width,
      imgs[num].height,
      p5.CONTAIN
    );
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
        p5.fill(0);
        p5.circle(x, y, 0.25);
      }
    }
    // reorder cs
    switch (nowOrder) {
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
    }
    console.log("reorder")
    console.log(cs);
    p5.clear()

    // call draw
    draw()
  }
};

new P5(script);
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
