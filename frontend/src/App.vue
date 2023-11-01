<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script>
import { ref, provide } from 'vue';
import axios from 'axios';
const CSV_URL = "/iroironairo/data.csv";

export default {
  name: "App",
  setup() {
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
          d.date = d.date.replace(/:/g, '/')
          d.time = d.time.replace(/:[^:]*$/, '')
        })
        console.log("讀取本地 CSV 成功")
      })
      .catch((error) => {
        console.error(error);
      });

      
    provide('csvData', data);
    return {
      data,
    }
  }
};
</script>
