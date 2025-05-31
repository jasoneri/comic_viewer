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
let scrollInterval = null;

const scrollToTop = () => {
  props.scrollbarRef?.setScrollTop(0);
};

const toggleScroll = () => {
  if (isScrolling.value) {
    // 如果正在滚动，停止滚动并恢复按钮图标
    clearInterval(scrollInterval);
    isScrolling.value = false;
  } else {
    // 启动自动滚动
    toggledScrolling.value = true;
    isScrolling.value = true;
    scrollInterval = setInterval(() => {
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