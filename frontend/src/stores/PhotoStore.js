import { defineStore } from 'pinia'

export const usePhotoStore = defineStore('PhotoStore', {
  state: () => {
    return { photos: undefined }
  },
//   actions: {
//     increment() {
//       this.count++
//     },
//   },
})