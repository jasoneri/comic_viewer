<template>
  <el-button 
      :class="['handle-btn', { 'vertical-btn-sv': verticalMode }]"
      type="success" 
      @click="retain(props.bookName)"
  >
      <el-icon size="large"><svg class="feather feather-save" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg></el-icon>
  </el-button>
  <el-button 
      :class="['handle-btn', { 'vertical-btn-del': verticalMode }]"
      :type="isCompleteDel ? 'danger' : 'warning'" 
      @click="isCompleteDel ? delBook(props.bookName) : removeBook(props.bookName)"
  ><el-icon size="large"><Delete /></el-icon></el-button>
</template>

<script setup>
    import { Delete, Download } from '@element-plus/icons-vue'
    import axios from "axios";
    import {backend} from "@/static/store.js";
    import { ElMessage } from 'element-plus'
    import { computed } from 'vue'
    import { useSettingsStore } from "@/static/store.js"

    const settingsStore = useSettingsStore()
    const isCompleteDel = computed(() => settingsStore.viewSettings.isCompleteDel)

    const props = defineProps({
      bookName:{type: String, required: true},
      retainCallBack:{type: Function, required: true},
      removeCallBack:{type: Function, required: true},
      delCallBack:{type: Function, required: true},
      bookHandlePath:{type: String, required: true},
      handleApiBodyExtra:{type: Object, required: false},
      verticalMode:{type: Boolean, required: false}
    })

    const handleBook = async(handle, book, callBack) => {
      let body = {handle: handle, name: book};
      body = {...body, ...props.handleApiBodyExtra}
      axios.post(backend + props.bookHandlePath, body)
        .then(res => {
          callBack(res.data.handled, res.data.path)
        })
        .catch(function (error) {
          console.log(error);
          ElMessage('此为缓存，【'+book+'】已经处理过了，无法再次处理')
        })
    }
    const retain = (book) => {
      handleBook('save', book, props.retainCallBack)
    }
    const removeBook = (book) => {
      handleBook('remove', book, props.removeCallBack)
    }
    const delBook = (book) => {
      handleBook('del', book, props.delCallBack)
    }
</script>

<style lang="scss" scoped>
.handle-btn {
    width: 50%;
    height: 100%;

    @mixin vertical-btn($bottom) {
      position: fixed;
      width: 10vw;
      max-width: 50px;
      height: 8vh;
      left: 0vw;
      bottom: $bottom;
      opacity: 0.6;
      &:hover {
        opacity: 1;
      }
    }
    &.vertical-btn-sv {
      @include vertical-btn(18vh);
    }
    &.vertical-btn-del {
      @include vertical-btn(10vh);
      margin: 0;
    }
}
</style>