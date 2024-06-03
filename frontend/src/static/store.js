
import {reactive, ref} from "vue";

export const backend = "http://192.168.114.514:12345"

export let indexPage = ref(1)
 export let bookList = reactive([])
 export let sort_val = ref("")
export let pageSize = 20
