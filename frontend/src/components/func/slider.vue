<template>
    <div v-if="props.show_slide" class="slider-container">
      <el-tooltip content="记录当前页" placement="right">
        <el-icon class="edit-pen" @click="saveCurrentPage">
          <EditPen />
        </el-icon>
      </el-tooltip>
      <el-slider
        v-model="currentPage"
        :min="0"
        :max="props.totalPages"
        :step="1"
        @change="handlePageChange"
      />
    </div>
</template>

<script setup>
import {EditPen} from "@element-plus/icons-vue";
import {reactive, ref, watch, onMounted, nextTick, watchEffect, onUnmounted } from "vue";
import { useRoute } from 'vue-router'
import { useScroll } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import _ from 'lodash';

const route = useRoute()
const props = defineProps({
  totalPages:{type: Number, required: true},
  show_slide: {type: Boolean,required: true},
})
const scrollContainer = ref(null)
const { y: scrollY } = useScroll(scrollContainer)
const currentPage = ref(1)
// 当前可见的图片索引
const visibleIndex = ref(0)
const observer = ref(null)
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
  if (props.show_slide.value === true){
    props.show_slide.value = false;
    callBack(_callBack);
    function _callBack() {
      const checkTotalPages = () => {
        if (props.totalPages!== 1) {
          props.show_slide.value = true;
          console.log('props.totalPages 不为 0，已将 props.show_slide.value 设置为 true');
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
// 初始化 Intersection Observer
const initObserver = () => {
  if (localStorage.getItem(`page-${route.query.book}`)) {
    debugger;
    handlePageChange(parseInt(localStorage.getItem(`page-${route.query.book}`)))
  }
  if (!scrollContainer.value) return
  // 配置选项
  const options = {
    root: scrollContainer.value,
    rootMargin: '0px',
    threshold: 0.5 // 当50%的图片可见时触发
  }
  // 创建观察器
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const index = Array.from(scrollContainer.value.children)
          .indexOf(entry.target)
        visibleIndex.value = index + 1
      }
    })
  }, options)
  // 观察所有图片
  Array.from(scrollContainer.value.children).forEach(child => {
    observer.value.observe(child)
  })
}
// 修改滚动处理逻辑
watchEffect(() => {
  currentPage.value = visibleIndex.value
})

// 修改初始化逻辑
const initSlider = async () => {
  const findContainer = () => document.querySelector('.demo-image__lazy')
  // 等待容器加载
  while (!findContainer()) {
    await new Promise(resolve => requestAnimationFrame(resolve))
  }
  scrollContainer.value = findContainer()
  // 等待图片加载完成
  await new Promise(resolve => {
    const checkImages = () => {
      const imgs = Array.from(scrollContainer.value.querySelectorAll('img'))
      if (imgs.every(img => img.complete)) {
        resolve()
      } else {
        requestAnimationFrame(checkImages)
      }
    }
    checkImages()
  })
  // 初始化观察器
  initObserver()
}
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
// 统一滚动处理逻辑（替换原有的两个watchEffect）
watchEffect((onCleanup) => {
  const container = scrollContainer.value
  if (!container) return
  const handleScroll = () => {
    const scrollTop = container.scrollTop
    const containerHeight = container.clientHeight
    const pageHeight = containerHeight
    // 精确的页数计算（带30%偏移量）
    currentPage.value = Math.min(
      Math.max(1, Math.floor((scrollTop + containerHeight * 0.3) / pageHeight) + 1),
      props.totalPages
    )
  }
  // 清除旧监听器
  if (debouncedScrollHandler.value) {
    container.removeEventListener('scroll', debouncedScrollHandler.value)
  }
  // 创建新的防抖处理函数
  debouncedScrollHandler.value = _.debounce(handleScroll, 150)
  // 绑定新监听器
  container.addEventListener('scroll', debouncedScrollHandler.value)
  // 组件卸载时自动清理
  onCleanup(() => {
    container.removeEventListener('scroll', debouncedScrollHandler.value)
  })
  // 初始化计算当前页
  handleScroll()
});
// 组件卸载时清理
onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
});
</script>

<style scoped lang="scss">
.slider-container {
  position: fixed;
  bottom: 2vh;
  left: 50%;
  transform: translateX(-50%);
  width: 80vw;
  padding: 15px;
  border-radius: 8px;
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 20px;
}

.edit-pen {
  cursor: pointer;
  padding: 5px;
  background: #ffffff72;
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

@media (max-width: 768px) {
  .slider-container {
    width: 80vw;
    bottom: 2.5vh;
  }
}
</style>