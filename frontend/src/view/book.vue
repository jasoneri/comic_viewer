<template>
  <el-container>
    <el-header style="height: 45px">
      <el-button-group style="width: 35%; height: 100%;">
        <bookHandleBtn
            :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack" :bookName="route.query.book"  :bookHandlePath="'/comic/handle'"
        />
      </el-button-group>
      <el-button-group style="width: 65%; height: 100%;">
        <TopBtnGroupOfBook
          :nextBook="nextBook" :previousBook="previousBook"
          :total-pages="imgUrls.arr.length"
        />
      </el-button-group>
    </el-header>
    <el-main class="demo-image__lazy" style="height: 100%">
        <el-image v-for="url in imgUrls.arr" :key="url" :src="url" lazy :preview-src-list="imgUrls.arr"/>
      <topBottom />
    </el-main>
    <el-button-group style="width: 100%; height: 50px;">
        <bookHandleBtn
            :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack" :bookName="route.query.book"  :bookHandlePath="'/comic/handle'"
        />
    </el-button-group>
  </el-container>
</template>

<script setup>
    import {backend,bookList,filteredBookList} from '@/static/store.js'
    import axios from 'axios'
    import {useRoute,useRouter} from 'vue-router'
    import {reactive,markRaw,computed} from "vue"
    import {ElMessageBox} from 'element-plus'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {Delete, Finished, Warning,} from "@element-plus/icons-vue"
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroupOfBook from '@/components/TopBtnGroupOfBook.vue'

    const route = useRoute()
    const router = useRouter()
    const imgUrls = reactive({arr:[]})
    const getBook = async(book, callBack) => {
      await axios.get(backend + '/comic/' + encodeURIComponent(book))
        .then(res => {
          let result = res.data.map((_) => {
            return backend + _
          });
          callBack(result)
        })
        .catch(function (error) {
          console.log(error);
        })
    }
    const bookIndex = computed(() => {
      return filteredBookList.arr.findIndex(item => item.book_name === route.query.book)
    });
    const init = (_book) => {
      getBook(_book, callBack)
      function callBack(data){
        imgUrls.arr = data
      }
    }
    init(route.query.book)
    function triggerInit(_book){
      imgUrls.arr = []
      router.replace({path:'book',query:{book:_book}})
      init(_book)
    }
    function previousBook(){
        triggerInit(filteredBookList.arr[bookIndex.value-1].book_name)
    }
    function nextBook(){
        triggerInit(filteredBookList.arr[bookIndex.value+1].book_name)
    }

    function retainCallBack(done, path) {MsgOpen(done, Finished, path)}
    function removeCallBack(done, path) {MsgOpen(done, Warning, path)}
    function delCallBack(done, path) {MsgOpen(done, Delete, path)}
    const MsgOpen = (handle, _ico, book) => {
      function back_index(){router.push({path: '/'})}
      ElMessageBox.confirm(
        book,
        handle + ' (点消息框右上x返回目录)',
        {
          distinguishCancelAndClose: true,
          confirmButtonText: '下一排序',
          cancelButtonText: '上一排序',
          center: true,
          icon: markRaw(_ico),
        }
      )
      .then(() => {
        nextBook()
      })
      .catch((action) => {
        const catch_func = action === 'cancel' ? previousBook : back_index;
        catch_func();
      })
    }
</script>

<style lang="scss" scoped>
  @use '@/styles/book.scss';
</style>
