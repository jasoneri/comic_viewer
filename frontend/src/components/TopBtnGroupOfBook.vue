<template>
  <el-button style="width: 40%; height: 100%" type="primary" :icon="ArrowLeft" @click="props.previousBook">上一排序</el-button>
  <el-button style="width: 40%; height: 100%" type="primary" @click="props.nextBook">下一排序<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
  <el-dropdown trigger="click" style="width: 20%;height: 100%;" placement="bottom-end" size="large">
    <el-button type="info"  @click="menuVisible = true" style="width: 100%;height: 100%;">
      <el-icon><Operation /></el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item :icon="ArrowDownBold" @click="showScrollConfDia">自动下滑</el-dropdown-item>
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
</template>

<script setup>
import {ArrowDownBold, ArrowLeft, ArrowRight, Operation, InfoFilled} from "@element-plus/icons-vue";
import {reactive, ref} from "vue";
import {backend, scrollIntervalPixel, scrollIntervalTime} from "@/static/store.js";
import axios from "axios";

const props = defineProps({
  previousBook:{type: Function, required: true},
  nextBook:{type: Function, required: true},
})
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const form = reactive({
  IntervalTime: 0,
  IntervalPixel: 0,
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
</style>