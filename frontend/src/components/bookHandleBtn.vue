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
    import {backend} from "@/utils/settings.js";
    const props = defineProps({
      bookName:{type: String, required: true},
      retainCallBack:{type: Function, required: true},
      removeCallBack:{type: Function, required: true},
      delCallBack:{type: Function, required: true},
    })

    const handleBook = async(handle, book, callBack) => {
      axios.post(backend + '/comic/handle', {handle: handle, name: book})
        .then(res => {
          callBack(res.data.handled, res.data.path)
        })
        .catch(function (error) {
          console.log(error);
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

<style scoped>
</style>