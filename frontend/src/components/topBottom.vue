<template>
    <el-backtop class="nav-btn" :style="{right: '5vw', bottom: '16vh'}" :visibility-height=0 @click="scrollToTop">
        <el-icon size="25" color="#00f5e1"><ArrowUpBold /></el-icon>
    </el-backtop>
   <el-button class="nav-btn" size="large" @click="toggleScroll" style="position: fixed;right: 5vw; bottom: 10vh" circle v-if="props.hideDown !== true">
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
  scrollbarRef: {type: [Object, null], required: true},
  hideDown: {type:Boolean, required: false},
});

const isScrolling = ref(false);
const toggledScrolling = ref(false);
let currScrollHeight = ref(0)

const scrollToTop = () => props.scrollbarRef?.setScrollTop(0);


const toggleScroll = () => {
  isScrolling.value = !isScrolling.value;
  if (!isScrolling.value) return;
  
  toggledScrolling.value = true;
  
  // 判断是动画式还是PPT式
  const isAnimationMode = scrollIntervalTime.value <= 200 && scrollIntervalPixel.value <= 20;
  
  isAnimationMode ? animateScroll() : pptScroll();
};

const animateScroll = () => {
  let lastTimestamp = 0;
  const targetSpeed = scrollIntervalPixel.value / scrollIntervalTime.value;
  let currentSpeed = 0;
  const acceleration = 0.002;
  const maxSpeed = targetSpeed * 1.2;

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

    currentSpeed = Math.min(currentSpeed + acceleration * deltaTime, maxSpeed);
    const scrollDistance = currentSpeed * deltaTime;
    currScrollHeight.value += scrollDistance;
    scrollbar.setScrollTop(currentScrollTop + scrollDistance);

    requestAnimationFrame(animate);
  };

  requestAnimationFrame(animate);
};

const pptScroll = () => {
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
};

const _getScrollConf = async() => {
  await axios.get(backend + '/comic/conf_scroll')
    .then(res => {
      scrollIntervalTime.value = parseInt(res.data.IntervalTime)
      scrollIntervalPixel.value = parseInt(res.data.IntervalPixel)
    })
};

const getScrollConf = () => _getScrollConf();

if (scrollIntervalPixel.value === 0 && scrollIntervalPixel.value === 0) {
  getScrollConf()
}
</script>

<style lang="scss" scoped>
.nav-btn {
  background-color: #ffffff61
}
</style>