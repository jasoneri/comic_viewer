import {reactive, ref} from "vue";
import { defineStore } from 'pinia'

export const backend = import.meta.env.LAN_IP
export let indexPage = ref(1)
export const bookList = reactive({arr: []})
export const filteredBookList = reactive({arr: []})
export let sortVal = ref("")
export let pageSize = 30
export const kemonoData = {
  ArtistsList: reactive({arr: []}),
  BookList: reactive({arr: []})
}
export let scrollIntervalTime = ref(0)
export let scrollIntervalPixel = ref(0)

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    isListMode: localStorage.getItem('isListMode') === 'true',
    isDark: localStorage.getItem('isDark') === 'true',
    showSlider: localStorage.getItem('showSlider') === 'true',
    sortValue: localStorage.getItem('sortValue') || '',
    customSorts: JSON.parse(localStorage.getItem('customSorts') || '[]'),
    isCompleteDel: localStorage.getItem('isCompleteDel') === 'true',
    scrollTopRecords: JSON.parse(localStorage.getItem('scrollTopRecords') || '{}')
  }),
  actions: {
    toggleListMode() {
      this.isListMode = !this.isListMode
      localStorage.setItem('isListMode', this.isListMode)
    },
    toggleDark() {
      this.isDark = !this.isDark
      localStorage.setItem('isDark', this.isDark)
    },
    toggleSlider(value) {
      this.showSlider = value
      localStorage.setItem('showSlider', this.showSlider)
    },
    setSortValue(value) {
      this.sortValue = value
      localStorage.setItem('sortValue', value)
    },
    addCustomSort(sort) {
      this.customSorts.push(sort)
      localStorage.setItem('customSorts', JSON.stringify(this.customSorts))
    },
    toggleDeleteMode() {
      this.isCompleteDel = !this.isCompleteDel
      localStorage.setItem('isCompleteDel', this.isCompleteDel)
    },
    saveScrollTopRecord(bookName, page) {
      this.scrollTopRecords[bookName] = page
      localStorage.setItem('scrollTopRecords', JSON.stringify(this.scrollTopRecords))
    },
    getScrollTopRecord(bookName) {
      return this.scrollTopRecords[bookName] || 0
    }
  }
})