import {reactive, ref} from "vue";

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