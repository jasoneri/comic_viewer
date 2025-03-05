<template>
  <el-button style="width: 40%; height: 100%" type="primary" :icon="ArrowLeft" @click="previousBook">上一排序</el-button>
  <el-button style="width: 40%; height: 100%" type="primary" @click="nextBook">下一排序<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
  <el-dropdown trigger="click" style="width: 20%;height: 100%;" placement="bottom-end" size="large">
    <el-button type="info"  @click="menuVisible = true" style="width: 100%;height: 100%;">
      <el-icon><Operation /></el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item :icon="ArrowDownBold" @click="showScrollConfDia">自动下滑</el-dropdown-item>
        <el-dropdown-item>
          <el-switch v-model="show_slide" :active-action-icon="View" :inactive-action-icon="Hide" active-text="页数滚动条"></el-switch>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
  <el-dialog v-model="dialogFormVisible" title="调速" :width="'80%'" align-center>
    <el-form :model="form">
      <el-form-item label="间隔时间毫秒" :label-width="formLabelWidth">
        <el-input v-model="form.IntervalTime" autocomplete="off"  :clearable="true"/>
      </el-form-item>
      <el-form-item label="下滑像素" :label-width="formLabelWidth">
        <el-input v-model="form.IntervalPixel" autocomplete="off" :clearable="true"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-popover
          placement="bottom-start"
          :width="250"
          trigger="click"
        >
          <template #reference>
            <el-button class="m-2" :icon="InfoFilled" type="info">数值相关</el-button>
          </template>
          大致分为两种形式 <br><hr style="border-style: dotted">
          动画式：流畅下滑，数值均设小，<br>例如 15ms/1px <br><hr style="border-style: dashed">
          ppt式：跨度大，预留阅读时间，<br>例如 3000ms/400px<hr style="border-style: dashed">
        </el-popover>
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="setScrollConf">Ok</el-button>
      </div>
    </template>
  </el-dialog>
  <div v-if="show_slide" class="slider-container">
      <el-slider
        v-model="currentPage"
        vertical
        height="100%"
        placement="right"
        :min="0"
        :max="props.totalPages"
        :step="1"
        @change="handlePageChange"
      />
      <el-tooltip content="记录当前页" placement="right">
        <el-icon class="edit-pen" @click="saveCurrentPage">
          <EditPen />
        </el-icon>
      </el-tooltip>
  </div>
</template>

<script setup>
import axios from "axios";
import {ArrowDownBold, ArrowLeft, ArrowRight, Operation, InfoFilled, Hide, View, EditPen} from "@element-plus/icons-vue";
import {reactive, ref, watch, onMounted, nextTick, watchEffect } from "vue";
import { useRoute } from 'vue-router'
import { useScroll } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import {backend, scrollIntervalPixel, scrollIntervalTime} from "@/static/store.js";

const route = useRoute()
const show_slide = ref(false)
const currentPage = ref(1)
const scrollContainer = ref(null)
const { y: scrollY } = useScroll(scrollContainer)

const props = defineProps({
  previousBook:{type: Function, required: true},
  nextBook:{type: Function, required: true},
  totalPages: {type: Number,required: true}
})
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const form = reactive({
  IntervalTime: 0,
  IntervalPixel: 0,
})

// 处理页面跳转
const handlePageChange = (page) => {
  if (!scrollContainer.value) return
  const target = scrollContainer.value.children[page - 1]
  if (target) {
    target.scrollIntoView({ 
      behavior: 'smooth',
      block: 'center'
    })
  }
}
// 保存当前页
const saveCurrentPage = () => {
  if (localStorage.getItem(`page-${route.query.book}`)) {localStorage.removeItem(`page-${route.query.book}`)};
  localStorage.setItem(`page-${route.query.book}`, currentPage.value)
  ElMessage.success(`已记录第 ${currentPage.value} 页`)
}
const wrapShowSlide = (callBack) => {
  props.totalPages = 1
  if (show_slide.value === true){
    show_slide.value = false;
    callBack(_callBack);
    function _callBack() {
      const checkTotalPages = () => {
        if (props.totalPages!== 1) {
          show_slide.value = true;
          console.log('props.totalPages 不为 0，已将 show_slide.value 设置为 true');
        } else {setTimeout(checkTotalPages, 50);}
      };
      checkTotalPages();
    }
  }
  else {callBack(()=>{});}
}
function nextBook() {wrapShowSlide(props.nextBook)}
function previousBook() {wrapShowSlide(props.previousBook)}

// ----------------------------------------
const initSlider = async () => {
  const findContainer = () => document.querySelector('.demo-image__lazy')
  if (!findContainer()) {
    await new Promise(resolve => setTimeout(resolve, 300))
    return initSlider()
  }
  scrollContainer.value = findContainer()
  // 加载保存的页数（带容错）
  const savedPage = localStorage.getItem(`page-${route.query.book}`)
  if (savedPage && !isNaN(savedPage)) {
    currentPage.value = Math.min(
      Math.max(1, parseInt(savedPage)),
      props.totalPages
    )
    // 延迟执行确保容器渲染完成
    nextTick(() => handlePageChange(currentPage.value))
  }
}
// 合并后的统一监听
watchEffect(() => {
  if (!scrollContainer.value) return
  
  // 精确计算当前页
  const pageHeight = scrollContainer.value.clientHeight
  const currentScroll = scrollContainer.value.scrollTop
  currentPage.value = Math.min(
    Math.max(1, Math.floor(currentScroll / pageHeight) + 1),
    props.totalPages
  )
})
// 优化后的初始化
onMounted(() => {
  // 统一初始化逻辑
  const init = async () => {
    await nextTick()
    await initSlider()
    // 添加滚动监听
    scrollContainer.value?.addEventListener('scroll', () => {
      const pageHeight = scrollContainer.value.clientHeight
      currentPage.value = Math.floor(scrollContainer.value.scrollTop / pageHeight) + 1
    })
  }
  init()
})
// 监听totalPages变化
watch(() => props.totalPages, (newVal) => {
  currentPage.value = Math.min(currentPage.value, newVal)
})
// 自动检测当前页
watchEffect(() => {
  if (!scrollContainer.value) return
  
  const images = [...scrollContainer.value.children]
  const containerHeight = scrollContainer.value.clientHeight
  const scrollPos = scrollY.value + containerHeight / 2
  
  currentPage.value = images.findIndex(img => {
    const imgTop = img.offsetTop
    const imgBottom = imgTop + img.offsetHeight
    return scrollPos >= imgTop && scrollPos <= imgBottom
  }) + 1
})

const showScrollConfDia = () => {
  getScrollConf(callback)
  function callback() {
    dialogFormVisible.value = true
  }
}
const getScrollConf = async(callback) => {
  await axios.get(backend + '/comic/conf_scroll')
    .then(res => {
      form.IntervalTime = res.data.IntervalTime
      form.IntervalPixel = res.data.IntervalPixel
      callback()
    })
    .catch(function (error) {console.log(error);})
}
const setScrollConf = async() => {
  await axios.post(backend + '/comic/conf_scroll', form)
    .then(res => {
      dialogFormVisible.value = false
      scrollIntervalTime.value = form.IntervalTime
      scrollIntervalPixel.value = form.IntervalPixel
    })
    .catch(function (error) {console.log(error);})
}
</script>
<style scoped lang="scss">
.slider-container {
  position: fixed;
  left: 5%;
  top: 50%;
  height: 60%;
  transform: translateY(-50%);
  z-index: 2000;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
}
.edit-pen {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  padding: 5px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(255, 255, 255, 0.9);
  transition: all 0.3s;
}

.edit-pen:hover {
  color: var(--el-color-primary);
  transform: translateX(-50%) scale(1.1);
}

@media (max-width: 768px) {
  .slider-container {
    left: 10px;
    padding: 10px;
  }
}
</style>