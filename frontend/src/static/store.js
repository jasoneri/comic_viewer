
import {reactive, ref} from "vue";

export const backend = "http://192.168.114.514:12345"

export let indexPage = ref(1)
 export const bookList = reactive({arr: []})
 export let sortVal = ref("")
export let pageSize = 20
