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
import {useSettingsStore} from "@/static/store.js";

const settingsStore = useSettingsStore()
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
  const isAnimationMode = settingsStore.scrollConf.intervalTime <= 200 && settingsStore.scrollConf.intervalPixel <= 20;
  
  isAnimationMode ? animateScroll() : pptScroll();
};

const animateScroll = () => {
  let lastTimestamp = 0;
  const targetSpeed = settingsStore.scrollConf.intervalPixel / settingsStore.scrollConf.intervalTime;
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
    
    currScrollHeight.value += settingsStore.scrollConf.intervalPixel;
    scrollbar.setScrollTop(currentScrollTop + settingsStore.scrollConf.intervalPixel);
  }, settingsStore.scrollConf.intervalTime);
};
</script>

<style lang="scss" scoped>
.nav-btn {
  background-color: #ffffff61
}
</style>