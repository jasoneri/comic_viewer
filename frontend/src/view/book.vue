<template>
  <el-container>
    <el-header height="5vh">
      <el-button-group style="width: 100%; height: 100%;" id="top-btn-group">
        <TopBtnGroupOfBook :nextBook="nextBook" :previousBook="previousBook" />
      </el-button-group>
    </el-header>
    <el-main id="main">
      <el-scrollbar class="demo-image__lazy" ref="scrollbarRef" 
        height="90vh" always @scroll.native.capture="handleRealScroll">
          <el-image 
            v-for="url in imgUrls.arr" 
            :key="url" 
            :src="url" 
            lazy 
            @load="handleImageLoad"
          />
          <bookHandleBtn 
              :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack" 
              :bookName="route.query.book"  :bookHandlePath="'/comic/handle'" :verticalMode="true"
          />
          <topBottom />
      </el-scrollbar>
    </el-main>
    <slider 
      :totalPages="imgUrls.arr.length" 
      :currentPage="currentPage"
      @changeSlider="changeSlider"
      @setCurrentPage="setCurrentPage"
    />
    
  </el-container>
</template>

<script setup>
    import {backend,bookList,filteredBookList} from '@/static/store.js'
    import axios from 'axios'
    import {useRoute,useRouter} from 'vue-router'
    import {reactive,markRaw,computed,ref, onMounted, onBeforeUnmount} from "vue"
    import {ElMessageBox} from 'element-plus'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {Delete, Finished, Warning,} from "@element-plus/icons-vue"
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroupOfBook from '@/components/TopBtnGroupOfBook.vue'
    import slider from '@/components/func/slider.vue'

    const route = useRoute()
    const router = useRouter()
    const imgUrls = reactive({arr:[]})
    const loadedImages = ref(0)
    const totalImages = ref(0)
    const currentPage = ref(0)
    const scrollbarRef = ref(null)
    let scrollElement = null // 存储实际滚动元素

    const handleImageLoad = () => {
      loadedImages.value++
    }

    const getBook = async(book, callBack) => {
      await axios.get(backend + '/comic/' + encodeURIComponent(book))
        .then(res => {
          let result = res.data.map((_) => {
            return backend + _
          });
          totalImages.value = result.length
          loadedImages.value = 0
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

    function retainCallBack(done, path) {MsgOpen(done, Finished, 'success', path)}
    function removeCallBack(done, path) {MsgOpen(done, Warning, 'warning', path)}
    function delCallBack(done, path) {MsgOpen(done, Delete, 'error', path)}
    const MsgOpen = (handle, _ico, _type, book) => {
      function back_index(){router.push({path: '/'})}
      ElMessageBox.confirm(
        book,
        handle + ' (点消息框右上x返回目录)',
        {
          distinguishCancelAndClose: true,
          confirmButtonText: '下一排序',
          cancelButtonText: '上一排序',
          center: true,
          type: _type,
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

    const handleRealScroll = (e) => {
      const scrollTop = e.target.scrollTop
      console.log("真实滚动位置:", scrollTop)
      // TODO[1] 计算图片位置并更新currentPage和slider.vue的localPage值
    }
    const scroll = ({ scrollTop }) => {
      console.log("scroll: "+scrollTop)
      currentPage.value = obj
    }
    const setCurrentPage = (value) => {
      currentPage.value = value
    }
    const changeSlider = (page) => {
      const images = document.querySelector('.demo-image__lazy').querySelectorAll('.el-image')
      const target = images[page - 1]
      if (target) {
        target.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
      }
    }
</script>

<style lang="scss" scoped>
  @use '@/styles/book.scss';
</style>
