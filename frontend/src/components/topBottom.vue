<template>
    <el-backtop :right="60" :bottom="110" >
        <el-icon size="25" color="#00f5e1"><ArrowUpBold /></el-icon>
    </el-backtop>
    <el-backtop :right="60" :bottom="60" :visibility-height="0" @click="toggleScroll" >
        <el-icon size="25" color="#00f5e1">
          <ArrowDownBold v-if="!isScrolling" /><VideoPause v-if="isScrolling" />
        </el-icon>
    </el-backtop>
</template>

<script setup>
import {ArrowDownBold, ArrowUpBold, VideoPause} from "@element-plus/icons-vue";
import { ref } from 'vue';
import {scrollIntervalTime, scrollIntervalPixel, backend} from "@/static/store.js";
import axios from "axios";

const isScrolling = ref(false);
const toggledScrolling = ref(false);
let currScrollHeight = ref(0)
let scrollInterval = null;

const toggleScroll = () => {
  if (isScrolling.value) {
    // 如果正在滚动，停止滚动并恢复按钮图标
    clearInterval(scrollInterval);
    isScrolling.value = false;
    window.scrollBy(0, 0);
  } else {
    // 启动自动滚动
    toggledScrolling.value = true;
    isScrolling.value = true;
    window.scrollBy({top: 0, behavior: "smooth"});
    scrollInterval = setInterval(() => {
      // 判断自动滚动停止
      const currentScrollTop = window.scrollY || document.documentElement.scrollTop;
      const maxScrollTop = document.documentElement.scrollHeight - window.innerHeight;
      if (currentScrollTop >= maxScrollTop) {
        clearInterval(scrollInterval);
        isScrolling.value = false;
        return;
      }
      // 常规自动滚动
      currScrollHeight.value += scrollIntervalPixel.value;
      window.scrollBy({top: scrollIntervalPixel.value, behavior: "auto"});
    }, scrollIntervalTime.value);
  }
};
const _getScrollConf = async() => {
  await axios.get(backend + '/comic/conf_scroll')
    .then(res => {
      scrollIntervalTime.value = res.data.IntervalTime
      scrollIntervalPixel.value = res.data.IntervalPixel
    })
};
const getScrollConf = () => {_getScrollConf()}
if (scrollIntervalPixel.value === 0 && scrollIntervalPixel.value === 0) {
  getScrollConf()
}
</script>

<style scoped>
</style>