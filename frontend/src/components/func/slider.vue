<template>
    <div v-if="settingsStore.showSlider" class="slider-container">
      <el-tooltip content="记录当前页" placement="top">
        <el-icon class="edit-pen" @click="saveCurrentPage">
          <EditPen />
        </el-icon>
      </el-tooltip>
      <el-slider
        v-model="currentPage"
        :min="0"
        :max="props.totalPages"
        :step="1"
        @change="slider2Page"
      />
    </div>
</template>

<script setup>
import {EditPen} from "@element-plus/icons-vue";
import {reactive, ref, watch, onMounted, nextTick, watchEffect, onUnmounted, computed } from "vue";
import { useRoute } from 'vue-router'
import { useScroll } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import _ from 'lodash';
import { useSettingsStore } from '@/static/store'

const route = useRoute()
const settingsStore = useSettingsStore()
const props = defineProps({
  totalPages:{type: Number, required: true},
})

const emit = defineEmits(['imagesLoaded'])

const scrollContainer = ref(null)
const currentPage = ref(0)
// 当前可见的图片索引
const observer = ref(null)

// 处理页面跳转
const slider2Page = (page) => {
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
  // 保存到 store
  settingsStore.savePageRecord(route.query.book, currentPage.value)
  ElMessage.success(`已记录第 ${currentPage.value} 页`)
}

// 修改初始化逻辑
const initSlider = async () => {
  const findContainer = () => document.querySelector('.demo-image__lazy')
  // 等待容器加载
  while (!findContainer()) {
    await new Promise(resolve => requestAnimationFrame(resolve))
  }
  scrollContainer.value = findContainer()
  
  // 初始化观察器
  initObserver()
  emit('imagesLoaded')
}

// 优化后的初始化
onMounted(() => {
  // 统一初始化逻辑
  const init = async () => {
    await nextTick()
    await initSlider()
  }
  init()
})

// 监听路由变化
watch(() => route.query.book, () => {
  initObserver()
})

// 初始化 Intersection Observer
const initObserver = () => {
  // 确保有图片元素
  const imgs = scrollContainer.value?.querySelectorAll('img')
  if (!imgs || imgs.length === 0) {
    console.log('没有找到图片元素，延迟初始化 observer') // TODO[1] 此处放有马加奈动图加载
    setTimeout(initObserver, 100)
    return
  }
  const savedPage = settingsStore.getPageRecord(route.query.book)
  if (savedPage) {
    slider2Page(savedPage)
    currentPage.value = savedPage
  }
}

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