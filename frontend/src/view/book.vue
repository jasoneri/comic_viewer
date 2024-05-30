<template>
  <el-container>
    <el-header>
      <el-button-group style="width: 100%; height: 100%;">
        <bookHandleBtn
            :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack" :bookName="book_name"
        />
      </el-button-group>
    </el-header>
    <el-main class="demo-image__lazy" style="height: 100%">
        <el-image v-for="url in imgUrls" :key="url" :src="url" lazy />
    </el-main>
    <el-backtop :right="60" :bottom="110" >
        <div style="height: 100%; width: 100%; text-align: center; line-height: 45px; color: #00f5e1;">
          <el-icon><ArrowUpBold /></el-icon>
        </div>
    </el-backtop>
  </el-container>
</template>

<script setup>
    import {backend} from '@/utils/settings.js'
    import axios from 'axios'
    import {useRoute, useRouter} from 'vue-router'
    import {reactive,markRaw} from "vue";
    import {ElMessageBox} from 'element-plus'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {ArrowUpBold, Delete, Finished, Warning} from "@element-plus/icons-vue";

    const route = useRoute()
    const router = useRouter()
    const book_name = route.query.book
    let imgUrls = reactive([])

    const getBook = async(book) => {
      let result = []
      await axios.get(backend + '/comic/' + book)
        .then(res => {
          result = res.data.map((_) => {
            return backend + _
          });
        })
        .catch(function (error) {
          console.log(error);
        })
      return result;
    }
    const list = getBook(book_name)
    list
    .then((data) => {
      imgUrls.push(...data)
    })
    .catch((error) => {
      console.log(error);
    });


    function retainCallBack(done, path) {MsgOpen(done, Finished, path)}
    function removeCallBack(done, path) {MsgOpen(done, Warning, path)}
    function delCallBack(done, path) {MsgOpen(done, Delete, path)}
    const MsgOpen = (handle, _ico, book) => {
      ElMessageBox.alert(
        book,
        handle,
        {
          confirmButtonText: 'OK',
          callback: (action) => {
            router.push({path: '/',query: {page:route.query.index_page}})   // 处理完保持返回书堆的第几页
          },
          center: true,
          icon: markRaw(_ico),
        })
    }
</script>

<style scoped>
.demo-image__lazy {
  height: 400px;
  overflow-y: auto;
}
.demo-image__lazy .el-image {
  display: block;
  min-height: 200px;
  margin-bottom: 10px;
}
.demo-image__lazy .el-image:last-child {
  margin-bottom: 0;
}
</style>
