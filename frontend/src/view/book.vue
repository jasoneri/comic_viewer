<template>
  <el-container>
    <el-header height="5vh" v-show="showBtn">
      <el-button-group style="width: 100%; height: 100%;" id="top-btn-group">
        <TopBtnGroupOfBook :nextBook="nextBook" :previousBook="previousBook" />
      </el-button-group>
    </el-header>
    <el-main id="main">
      <el-scrollbar class="demo-image__lazy" :height="showBtn?`90vh`:`95vh`" always 
      ref="scrollbarRef" @scroll.native.capture="handleRealScroll">
        <div ref="imageContainer">
          <el-image 
            v-for="url in imgUrls.arr" 
            :key="url" 
            :src="url" 
            :lazy="!settingsStore.displaySettings.showSlider"
            @load="handleImageLoad"
          />
          <el-empty class="custom-empty" v-if="!loadedFlag && imgUrls.arr.length===0"
            image="/empty.png" :image-size="`40vw`" :description="errorText" />
        </div>
        <topBottom v-if="settingsStore.displaySettings.showNavBtn" :scrollbarRef="scrollbarRef" />
      </el-scrollbar>
      <div v-show="showBtn">
        <bookHandleBtn 
            :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack" 
            :bookName="route.query.book"  :bookHandlePath="'/comic/handle'" :verticalMode="true"
        />
      </div>
    </el-main>
    <!-- [slider.vue] template -->
    <div v-if="settingsStore.displaySettings.showSlider" class="slider-container">
        <el-icon class="edit-pen" @click="saveCurrScrollTop">
          <EditPen />
        </el-icon>
      <el-slider
        v-model="currScrollTop"
        :max="maxScrollHeight"
        :show-tooltip="false"
        @input="inputSlider"
      />
    </div>
  </el-container>
</template>

<script setup>
    import {backend,bookList,filteredBookList} from '@/static/store.js'
    import axios from 'axios'
    import {useRoute,useRouter} from 'vue-router'
    import {reactive,markRaw,computed,ref,h} from "vue"
    import {ElMessageBox} from 'element-plus'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {Delete, Finished, Warning,} from "@element-plus/icons-vue"
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroupOfBook from '@/components/TopBtnGroupOfBook.vue'
    // import slider from '@/components/func/slider.vue'

// [slider.vue] script
import {EditPen} from "@element-plus/icons-vue";
import {onMounted, onBeforeUnmount, nextTick, watch} from "vue";
import { ElMessage,ElNotification } from 'element-plus'
import { useSettingsStore } from '@/static/store'
import { debounce } from 'lodash-es';
const settingsStore = useSettingsStore()
const imageContainer = ref(null) // 引用图片容器
const maxScrollHeight = ref(0)   // 最大滚动高度
// [slider.vue] script end

    const route = useRoute()
    const router = useRouter()
    const imgUrls = reactive({arr:[]})
    const loadedImages = ref(0)
    const totalImages = ref(0)
    const currScrollTop = ref(0)
    const scrollbarRef = ref(null)
    const showBtn = ref(true)
    const btnShowThreshold = 0.15
    const errorText = computed(() => '已经说过没图片了！..')

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
      currScrollTop.value = scrollTop

      const maxScrollTop = e.target.scrollHeight - e.target.clientHeight
      const thresholdVal = maxScrollTop * btnShowThreshold
      showBtn.value = 
        scrollTop <= thresholdVal || 
        scrollTop >= maxScrollTop - thresholdVal
    }
    const inputSlider = (scrollTopVal) => {
      scrollbarRef.value?.setScrollTop(scrollTopVal)
    }

// [slider.vue] script
const handleImageLoad = () => {
  loadedImages.value++
  if (loadedImages.value === totalImages.value && totalImages.value > 0) {
    nextTick(() => {
      calculateTotalHeight()
      const savedScrollTop = settingsStore.getScrollTopRecord(route.query.book)
      savedScrollTop && scroll2Top(savedScrollTop)
    })
  }
}
const loadedFlag = computed(() => {
  if (totalImages.value === 0) return
  const _loadFlag = loadedImages.value === totalImages.value
  if (!settingsStore.displaySettings.showSlider && _loadFlag) return true;
  if (!(imageContainer.value || _loadFlag)) return;
  const imgs = imageContainer.value.querySelectorAll('.el-image');
  return !imgs || imgs.length === totalImages.value
})
const calculateTotalHeight = () => {
  if (!imageContainer.value) return;
  // 获取所有图片元素
  const images = imageContainer.value.querySelectorAll('.el-image');
  let totalHeight = 0;
  // 计算所有图片的总高度
  images.forEach((img, index) => {
    const imgHeight = img.offsetHeight;
    // 解决部分过长书，其最后图片只显示一半左右的情况
    totalHeight += (index === images.length-1) ? imgHeight * 1.5 : imgHeight
  });
  // 设置最大滚动高度（总高度减去视口高度）
  const scrollWrap = scrollbarRef.value?.wrap$;
  maxScrollHeight.value = scrollWrap 
    ? Math.max(0, totalHeight - scrollWrap.clientHeight) 
    : totalHeight
  console.log('计算最大滚动高度:', maxScrollHeight.value);
};
// 保存当前页
const saveCurrScrollTop = () => {
  const v = parseInt(currScrollTop.value)
  settingsStore.saveScrollTopRecord(route.query.book, v)
  ElMessage.success(`已记录翻滚像素 ${v} `)
  ElNotification({
    title: '仅限滚动条可视状态下',
    message: h('span', { style: 'font-size: large' }, '重读此本会自动跳到此处'),
    type: 'info',offset: 50,duration: 2800,
  })
}
const scroll2Top = (val) => {
  if (settingsStore.displaySettings.showSlider && !loadedFlag.value && maxScrollHeight.value) {
    console.log('scroll2Top 循环中！');
    setTimeout(()=>{scroll2Top(val)}, 150)
  }
  if (loadedFlag.value) {
    currScrollTop.value = val
    scrollbarRef.value?.setScrollTop(val);
  }
}
// 初始化：计算总高度
onMounted(() => {
  if (settingsStore.displaySettings.showSlider) {
    nextTick(calculateTotalHeight);
  }
});

// 监听滑块显示状态变化
watch(() => settingsStore.displaySettings.showSlider, (newValue, oldValue) => {
  if (newValue && oldValue === false) {
    // 强制重新渲染所有图片（取消懒加载）
    const urls = [...imgUrls.arr];
    imgUrls.arr = [];
    nextTick(() => {
      imgUrls.arr = urls;
      loadedImages.value = 0;
      totalImages.value = urls.length;
    });
  }
});
</script>

<style lang="scss" scoped>
  @use '@/styles/book.scss';

  .custom-empty {
    position: fixed;
    top: 60vh;
    left: 50vw;
    transform: translate(-50%, -50%);

    :deep(.el-empty__description) {
      p {
        font-size: 1.3rem;
      }
    }
  }

  // [slider.vue] scss
  .slider-container {
    position: fixed;
    bottom: 3.2vh;
    background: #ffffff04;
    left: 50%;
    transform: translateX(-50%);
    width: 90vw;
    max-height: 3px;
    padding: 10px;
    border-radius: 15px;
    z-index: 2000;
    display: flex;
    align-items: center;
    gap: 15px;
  }

  .edit-pen {
    cursor: pointer;
    padding: 5px;
    background: #0000003b;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(255, 255, 255, 0.599);
    transition: all 0.3s;
  }

  .edit-pen:hover {
    transform: scale(1.1);
  }

  :deep(.el-slider) {
    width: 100%;
  }
</style>
