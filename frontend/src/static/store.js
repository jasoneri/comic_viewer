
import {reactive, ref} from "vue";

export const backend = import.meta.env.LAN_IP
export let indexPage = ref(1)
 export const bookList = reactive({arr: []})
 export let sortVal = ref("")
export let pageSize = 20
