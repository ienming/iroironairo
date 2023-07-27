<script setup>
import { onMounted, ref } from 'vue';
import { eventBus } from '../main.js';
import ExcelJs from 'exceljs'

const props = defineProps(['imgNum'])

let mainColors = ref({}) //空物件以便之後可以存取，用ref將它變成可以響應的資料
let allImgsColors = new Set()
onMounted(() => {
  eventBus.on('main-colors-evt', colors => {
    let obj = {}, arr = []
    colors.forEach(c => {
      obj.h = Math.floor(c.color[0])
      obj.s = Math.floor(c.color[1])
      obj.l = Math.floor(c.color[2])
      arr.push(obj)
      obj = {}
    })
    mainColors.value = arr
  });
});

function submitMainColor(){
  let arr = []
  mainColors._rawValue.forEach(el=>{
    arr.push(Object.values(el))
  })
  let img = {}
  img.id = props.imgNum
  img.colors = arr
  console.log(img) // 點擊後可以送出該圖片的前五個主要色（HSL）
  allImgsColors.add(img)
}

function outputData(){
  const workbook = new ExcelJs.Workbook();
  const sheet = workbook.addWorksheet('工作表範例1');
  sheet.columns = [{header:"id", key:"id"},
    {header:"color1", key:"color1"},
    {header:"color2", key:"color2"},
    {header:"color3", key:"color3"},
    {header:"color4", key:"color4"},
    {header:"color5", key:"color5"}]

  let arr = Array.from(allImgsColors)
  for (let i=0; i<arr.length; i++){
    let data = {
      id: arr[i].id,
      color1: arr[i].colors[0],
      color2: arr[i].colors[1],
      color3: arr[i].colors[2],
      color4: arr[i].colors[3],
      color5: arr[i].colors[4]
    }
    sheet.addRow(data)
  }
  workbook.xlsx.writeBuffer().then((content) => {
	  const link = document.createElement("a");
    const blobData = new Blob([content], {
      type: "application/vnd.ms-excel;charset=utf-8;"
    });
    link.download = '測試的試算表.xlsx';
    link.href = URL.createObjectURL(blobData);
    link.click();
  });
}
</script>

<template>
    <section>
      <div class="d-flex">
          <div :style="{ 'background-color': 'hsl('+color.h+','+color.s+'%,'+color.l+'%)'}"
          class="main-cs"
          v-for="color of mainColors"></div>
      </div>
      <button @click="submitMainColor">Submit Main Color: {{ props.imgNum }}</button>
      <button @click="outputData">Create Excel</button>
    </section>
</template>

<style scoped>
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
</style>