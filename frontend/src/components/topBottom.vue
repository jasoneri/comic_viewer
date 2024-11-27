<template>
    <el-backtop :right="60" :bottom="110" >
        <div style="height: 100%; width: 100%; text-align: center; line-height: 45px; color: #00f5e1;">
          <el-icon><ArrowUpBold /></el-icon>
        </div>
    </el-backtop>
    <el-backtop :right="60" :bottom="60" :visibility-height="0" @click="scrollToBottom" >
        <div style="height: 100%; width: 100%; text-align: center; line-height: 43px; color: #00f5e1;">
          <el-icon><ArrowDownBold /></el-icon>
        </div>
    </el-backtop>
</template>

<script setup>
import {ArrowDownBold, ArrowUpBold} from "@element-plus/icons-vue";
function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  });
}
</script>

<style scoped>
</style>