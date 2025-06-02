<template>
    <el-backtop class="nav-btn" :style="{right: '5vw', bottom: '16vh'}" :visibility-height=0 @click="scrollToTop">
        <el-icon size="25" color="#00f5e1"><ArrowUpBold /></el-icon>
    </el-backtop>
   <el-button class="nav-btn" size="large" @click="toggleScroll" style="position: fixed;right: 5vw; bottom: 10vh" circle>
      <el-icon size="25" color="#00f5e1">
          <ArrowDownBold v-if="!isScrolling" /><VideoPause v-if="isScrolling" />
        </el-icon>
   </el-button>
</template>

<script setup>
import {ArrowDownBold, ArrowUpBold, VideoPause} from "@element-plus/icons-vue";
import { ref } from 'vue';
import {scrollIntervalTime, scrollIntervalPixel, backend} from "@/static/store.js";
import axios from "axios";

const props = defineProps({
  scrollbarRef: {type: [Object, null], required: true}
});

const isScrolling = ref(false);
const toggledScrolling = ref(false);
let currScrollHeight = ref(0)

const scrollToTop = () => {
  props.scrollbarRef?.setScrollTop(0);
};

const toggleScroll = () => {
  if (isScrolling.value) {
    // 如果正在滚动，停止滚动并恢复按钮图标
    isScrolling.value = false;
    return;
  }

  // 启动自动滚动
  toggledScrolling.value = true;
  isScrolling.value = true;
  
  // 判断是动画式还是PPT式
  const isAnimationMode = scrollIntervalTime.value <= 200 && scrollIntervalPixel.value <= 20;
  
  if (isAnimationMode) {
    // 动画式：使用requestAnimationFrame实现平滑滚动
    let lastTimestamp = 0;
    const targetSpeed = scrollIntervalPixel.value / scrollIntervalTime.value; // 目标速度 (像素/毫秒)
    let currentSpeed = 0;
    const acceleration = 0.002; // 加速度
    const maxSpeed = targetSpeed * 1.2; // 最大速度略高于目标速度

    const animate = (timestamp) => {
      if (!isScrolling.value) return;
      
      if (!lastTimestamp) lastTimestamp = timestamp;
      const deltaTime = timestamp - lastTimestamp;
      lastTimestamp = timestamp;

      const scrollbar = props.scrollbarRef;
      if (!scrollbar) return;
      
      const scrollContainer = scrollbar.wrapRef || scrollbar.wrap$;
      if (!scrollContainer) return;
      
      const currentScrollTop = scrollContainer.scrollTop;
      const maxScrollTop = scrollContainer.scrollHeight - scrollContainer.clientHeight;
      
      if (currentScrollTop >= maxScrollTop) {
        isScrolling.value = false;
        return;
      }

      // 平滑加速
      currentSpeed = Math.min(currentSpeed + acceleration * deltaTime, maxSpeed);
      
      // 计算这一帧要滚动的距离
      const scrollDistance = currentSpeed * deltaTime;
      
      // 应用滚动
      currScrollHeight.value += scrollDistance;
      scrollbar.setScrollTop(currentScrollTop + scrollDistance);

      // 继续动画
      requestAnimationFrame(animate);
    };

    // 开始动画
    requestAnimationFrame(animate);
  } else {
    // PPT式：使用setInterval实现大跨度滚动
    const scrollInterval = setInterval(() => {
      if (!isScrolling.value) {
        clearInterval(scrollInterval);
        return;
      }

      const scrollbar = props.scrollbarRef;
      if (!scrollbar) return;
      
      const scrollContainer = scrollbar.wrapRef || scrollbar.wrap$;
      if (!scrollContainer) return;
      
      const currentScrollTop = scrollContainer.scrollTop;
      const maxScrollTop = scrollContainer.scrollHeight - scrollContainer.clientHeight;
      
      if (currentScrollTop >= maxScrollTop) {
        clearInterval(scrollInterval);
        isScrolling.value = false;
        return;
      }
      
      currScrollHeight.value += scrollIntervalPixel.value;
      scrollbar.setScrollTop(currentScrollTop + scrollIntervalPixel.value);
    }, scrollIntervalTime.value);
  }
};

const _getScrollConf = async() => {
  await axios.get(backend + '/comic/conf_scroll')
    .then(res => {
      scrollIntervalTime.value = parseInt(res.data.IntervalTime)
      scrollIntervalPixel.value = parseInt(res.data.IntervalPixel)
    })
};
const getScrollConf = () => {_getScrollConf()}
if (scrollIntervalPixel.value === 0 && scrollIntervalPixel.value === 0) {
  getScrollConf()
}
</script>

<style lang="scss" scoped>
.nav-btn {
  background-color: #ffffff61
}
</style>