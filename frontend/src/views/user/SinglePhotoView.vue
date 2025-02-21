<script setup>
import { inject, ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import { hsl2Hex, getReverseColor } from "@/composable/common";
import Bookmark from '@/components/Bookmark.vue';
import Navigator from '@/components/Navigator.vue';
import PolaroidText from '@/components/PolaroidText.vue';

const data = inject('csvData', [])
const usingMobile = inject('usingMobile', false)
const imgLoaded = ref(false)

onBeforeRouteUpdate((to, from) =>{
  imgLoaded.value = false
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  })
})

function hasLoaded(){
  imgLoaded.value = true
}

const place2Roma = computed(()=>{
  if (nowPhoto.value.places){
    switch (nowPhoto.value.places[0]){
      case '東京':
        return 'Tokyo'
      case '神奈川':
        return 'Kanagawa'
      case '栃木':
        return 'Tochigi'
      case '山梨':
          return 'Yamanashi'
      case '靜岡':
        return 'Shizuoka'
      case '愛知':
        return 'Aichi'
      case '富山':
        return 'Toyama'
      case '石川':
        return 'Ishikawa'
      case '岐阜':
        return 'Gifu'
      case '滋賀':
        return 'Shiga'
      case '三重':
        return 'Sanjyuu'
      case '和歌山':
        return 'Wakayama'
      case '奈良':
        return 'Nara'
      case '兵庫':
        return 'Hyogo'
      case '京都':
        return 'Kyoto'
      case '大阪':
        return 'Osaka'
      case '神戶':
        return 'Kobe'
      case '岡山':
        return 'Okayama'
      case '廣島':
        return 'Hiroshima'
      case '島根':
        return 'Shimane'
      case '屋久島':
        return 'Yakushima'
      case '鹿耳島':
        return 'Kagoshima'
      case '神戶港':
        return 'Kobe Port'
      case '六甲':
        return 'Rokko'
      case '神戶大學':
        return 'Kobe Daigaku'
      case 'ポートアイランド':
        return 'Port Island'
      case '元町':
        return 'Motomachi'
      case '三宮':
        return 'Sannomiya'
      default:
        return nowPhoto.value.places[0]
    }
  }else return
})

const route = useRoute()
const nowPhoto = computed(()=>{
  if (JSON.stringify(route.query) !== '{}'){
    const nowPhotoName = JSON.parse(route.query.photo)
    if (data.value.length > 0){
      return data.value.find((d) => d.name === nowPhotoName);
    }else return {}
  }
})

const mainColor = computed(()=>{
  if (nowPhoto.value['main_color']){
    const color = nowPhoto.value['main_color']
    return hsl2Hex(color.h, color.s, color.l)
  }else return
})

const themeStyle = computed(()=>{
  if (Object.keys(nowPhoto.value).length > 0){
    let hslObj = nowPhoto.value['main_color']
    let reverseObj = getReverseColor(hslObj)
    return {
      "color": hsl2Hex(reverseObj.h, reverseObj.s, reverseObj.l),
      "backgroundColor": hsl2Hex(hslObj.h, hslObj.s, hslObj.l)
    }
  }else return
})

const main = ref(null)
</script>
<template>
    <main>
        <section
          ref="main"
          v-if="nowPhoto"
          class="vh-100 bg-silver gap-lg-5 d-flex flex-column flex-lg-row align-items-center">
            <div
              id="photo"
              class="col-12 col-lg-6 vh-100 p-4 pt-5 p-lg-7"
              :style="{'background-color': mainColor}">
              <img
                :src="nowPhoto.url_google"
                alt=""
                class="d-none"
                @load="hasLoaded" />
              <transition
                name="fade"
                mode="out-in">
                <img
                  v-if="imgLoaded"
                  alt=""
                  class="w-100 h-100 object-fit-cover"
                  :src="nowPhoto.url_google" />
              </transition>
            </div>
            <section
              id="photo-des-el"
              class="col-12 col-lg-6 rounded-4 p-4 py-3 p-lg-0 bg-silver">
              <p>{{nowPhoto.date}} {{nowPhoto.time}}</p>
              <polaroid-text
                :photo="nowPhoto"
                :bg-style="{'background-color': '#232323', 'color': '#f6f6f6'}" />
            </section>
        </section>
        <!-- Watermark -->
        <div
          class="position-fixed bottom-0 text-end"
          style="transform-origin: 100% center; rotate: 90deg; right: 50px;">
          <span class="ff-serif watermark">
            {{ place2Roma }}
          </span>
        </div>
        <!-- Bookmark -->
        <bookmark
          :theme="themeStyle"
          class="position-fixed top-0 d-flex align-items-center gap-1" />
        <!-- Nav -->
        <navigator
          :theme="usingMobile ? themeStyle:{
            'color': '#232323',
            'backgroundColor': '#F6F6F6'
          }" />
    </main>
</template>

<style scoped>
.watermark{
  opacity: 0.1;
  font-size: 100px;
}

#photo-des-el{
  z-index: 1030;
  margin-top: -15vh;
}

@media screen and (min-width: 992px) {
  #photo-des-el{
    z-index: unset;
    margin-top: unset;
  }
}
</style>