<template>
    <el-button style="width: 50%; height: 100%;" type="success" @click="retain(props.bookName)">
      保留<el-icon class="el-icon--right"><Download /></el-icon>
    </el-button>
    <el-popconfirm
      confirm-button-text="Del" confirm-button-type="danger" @confirm="delBook(props.bookName)"
      cancel-button-text="No, just remove" cancel-button-type="warning" @cancel="removeBook(props.bookName)"
      :icon="InfoFilled" icon-color="#626AEF" width=60% :title=props.bookName
    >
      <template #reference>
        <el-button style="width: 50%; height: 100%;" type="danger" :icon="Delete" />
      </template>
    </el-popconfirm>
</template>

<script setup>
    import { Delete, Download, InfoFilled } from '@element-plus/icons-vue'
    import axios from "axios";
    import {backend} from "@/static/store.js";
    import { ElMessage } from 'element-plus'
    const props = defineProps({
      bookName:{type: String, required: true},
      retainCallBack:{type: Function, required: true},
      removeCallBack:{type: Function, required: true},
      delCallBack:{type: Function, required: true},
      bookHandlePath:{type: String, required: true},
      handleApiBodyExtra:{type: Object, required: false}
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
</style>