<template>
  <el-button-group  style="width: 100%; height: 70%">
    <el-button text class="switch" :class="isDark ? 'isDark-switch' : 'noDark-switch'" style="width: 20%; height: 100%" @click="toggleDark">
      <el-icon v-if="isDark">
        <svg viewBox="0 0 24 24">
          <path
            d="M6.05 4.14l-.39-.39a.993.993 0 0 0-1.4 0l-.01.01a.984.984 0 0 0 0 1.4l.39.39c.39.39 1.01.39 1.4 0l.01-.01a.984.984 0 0 0 0-1.4zM3.01 10.5H1.99c-.55 0-.99.44-.99.99v.01c0 .55.44.99.99.99H3c.56.01 1-.43 1-.98v-.01c0-.56-.44-1-.99-1zm9-9.95H12c-.56 0-1 .44-1 .99v.96c0 .55.44.99.99.99H12c.56.01 1-.43 1-.98v-.97c0-.55-.44-.99-.99-.99zm7.74 3.21c-.39-.39-1.02-.39-1.41-.01l-.39.39a.984.984 0 0 0 0 1.4l.01.01c.39.39 1.02.39 1.4 0l.39-.39a.984.984 0 0 0 0-1.4zm-1.81 15.1l.39.39a.996.996 0 1 0 1.41-1.41l-.39-.39a.993.993 0 0 0-1.4 0c-.4.4-.4 1.02-.01 1.41zM20 11.49v.01c0 .55.44.99.99.99H22c.55 0 .99-.44.99-.99v-.01c0-.55-.44-.99-.99-.99h-1.01c-.55 0-.99.44-.99.99zM12 5.5c-3.31 0-6 2.69-6 6s2.69 6 6 6s6-2.69 6-6s-2.69-6-6-6zm-.01 16.95H12c.55 0 .99-.44.99-.99v-.96c0-.55-.44-.99-.99-.99h-.01c-.55 0-.99.44-.99.99v.96c0 .55.44.99.99.99zm-7.74-3.21c.39.39 1.02.39 1.41 0l.39-.39a.993.993 0 0 0 0-1.4l-.01-.01a.996.996 0 0 0-1.41 0l-.39.39c-.38.4-.38 1.02.01 1.41z"
            fill="currentColor"></path>
        </svg>
      </el-icon>
      <el-icon v-else>
        <svg viewBox="0 0 24 24">
          <path
            d="M11.01 3.05C6.51 3.54 3 7.36 3 12a9 9 0 0 0 9 9c4.63 0 8.45-3.5 8.95-8c.09-.79-.78-1.42-1.54-.95A5.403 5.403 0 0 1 11.1 7.5c0-1.06.31-2.06.84-2.89c.45-.67-.04-1.63-.93-1.56z"
            fill="currentColor"></path>
        </svg>
      </el-icon>
    </el-button>
    <el-button type="info" style="width: 15%; height: 100%" @click="toggleViewMode">
      <el-icon v-if="isListMode">
        <svg style="enable-background:new 0 0 24 24;" version="1.1" viewBox="0 0 24 24" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="info"/><g id="icons"><g id="menu"><path d="M20,10H4c-1.1,0-2,0.9-2,2c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2C22,10.9,21.1,10,20,10z"/><path d="M4,8h12c1.1,0,2-0.9,2-2c0-1.1-0.9-2-2-2H4C2.9,4,2,4.9,2,6C2,7.1,2.9,8,4,8z"/><path d="M16,16H4c-1.1,0-2,0.9-2,2c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2C18,16.9,17.1,16,16,16z"/></g></g></svg>
      </el-icon>
      <el-icon v-else><Grid /></el-icon>
    </el-button>
    <el-button type="primary" :icon="RefreshRight" @click="props.reload(true)"
               style="width: 50%; height: 100%; margin: 0 auto; display: block; font-size: 15px">
      重新加载</el-button>

    <el-dropdown trigger="click" style="width: 15%;height: 100%;" placement="bottom-end" size="large">
      <el-button type="success" @click="menuVisible = true" style="width: 100%;height: 100%;">
        <el-icon><Menu /></el-icon>
      </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item :icon="Operation" @click="showConfDialog">配置</el-dropdown-item>
            <el-dropdown-item :icon="Filter" @click="open_filter">筛选</el-dropdown-item>
            <el-dropdown-item :icon="Switch" @click="switchDelMode">删除模式</el-dropdown-item>
            <el-select v-model="select_value" placeholder="排序" placement="left-start">
              <el-option
                v-for="item in select_options" style="height: 100%" :icon="Sort"
                :key="item.value" :label="item.label" :value="item.value"
                @click="handleSortChange(item.value)"
              />
              <template #footer>
                <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
                  自定义排序
                </el-button>
                <template v-else>
                  <el-input
                    v-model="optionName" class="option-input" size="small"
                    placeholder="自定义: 'time/name'+'_'+'asc/desc'"
                  />
                  <el-button type="primary" size="small" @click="onConfirm">confirm</el-button>
                  <el-button size="small" @click="clear">cancel</el-button>
                </template>
              </template>
            </el-select>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
  </el-button-group>

  <el-dialog
      v-model="dialogVisible" title="修改配置" width="80vw"
      align-center center
    >
        <el-input type="textarea" v-model="confText"
                  :rows="5" :input-style='"white-space: nowrap;overflow-x: auto"'/>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfDialog(confText)">提交修改</el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="filterDialogVisible" title="筛选" width="65vw">
    <div class="filter-input-wrapper">
      <el-input v-model="filterInput" placeholder="大小写严格匹配" />
      <el-dropdown @command="handleKeywordSelect" trigger="click" placement="bottom-end" max-height="55vh">
        <el-button class="el-button--text">
          <el-icon><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="keyword in props.keywords_list" :key="keyword" :command="keyword">
              {{ keyword }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="filterDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleFilterConfirm">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import {Filter, RefreshRight, Menu, Sort, Operation, Switch, Grid, List, ArrowDown} from "@element-plus/icons-vue";
import {ElMessageBox, ElMessage} from 'element-plus'
import { useSettingsStore } from "@/static/store.js"

const props = defineProps({
  modelValue: {type: Boolean, required: true},
  reload:{type: Function, required: true},
  handleConf:{type: Function, required: false},
  items: {type: Object, required: false}, 
  filteredItems: {type: Object, required: false},
  handleFilter: {type: Function, required: false},
  keywords_list: {type: Array, required: false}
})

const emit = defineEmits(['send_sort', 'update:modelValue'])

const settingsStore = useSettingsStore()
const isListMode = computed(() => settingsStore.isListMode)
const isDark = computed(() => settingsStore.isDark)
const select_value = computed({
  get: () => settingsStore.sortValue,
  set: (value) => settingsStore.setSortValue(value)
})
const select_options = computed(() => [
  {value: 'time_desc', label: '时间倒序'},
  {value: 'name_asc', label: '名字顺序'},
  ...settingsStore.customSorts
])

onMounted(() => {
  emit('update:modelValue', isListMode.value)
  setTheme(isDark.value)
})

const setTheme = (isDarkMode) => {
  const html = document.querySelector('html')
  if (html) {
    if (isDarkMode) {
      html.classList.remove("dark")
      html.classList.add("light")
    } else {
      html.classList.remove("light")
      html.classList.add("dark")
    }
  }
}

const toggleDark = () => {
  settingsStore.toggleDark()
  setTheme(isDark.value)
}

const toggleViewMode = () => {
  settingsStore.toggleListMode()
  emit('update:modelValue', isListMode.value)
}

const switchDelMode = () => {
  if (settingsStore.isCompleteDel === false) {
    ElMessage ({
      message: `已切换至「彻底删除」模式，请谨慎操作`,
      type: 'warning',
      duration: 3500
    })
  }
  settingsStore.toggleDeleteMode()
}

const dialogVisible = ref(false);
const isAdding = ref(false)
const confText = ref('')
const optionName = ref('')

const filterDialogVisible = ref(false)
const filterInput = ref('')

const open_filter = () => {
  filterDialogVisible.value = true
}

const handleKeywordSelect = (keyword) => {
  filterInput.value = keyword
}

const handleFilterConfirm = () => {
  if (filterInput.value) {
    if (props.handleFilter) {
      props.handleFilter(filterInput.value)
    } else {
      props.filteredItems.arr = props.items.arr.filter(item => item.book_name.includes(filterInput.value))
    }
    filterDialogVisible.value = false
  } else {
    ElMessage.warning('请输入关键字')
  }
}

const showConfDialog = () => {
  function callBack(data){
    confText.value = data
    dialogVisible.value = true
  }
  if (props.handleConf) {
    props.handleConf(callBack);
  }
}
const handleConfDialog = (confText_) => {
  if (confText_) {
    props.handleConf(confText_);
    dialogVisible.value = false;
  } else {
    this.$message.error('请输入内容');
  }
}
const onAddOption = () => {
  isAdding.value = true
}
const onConfirm = () => {
  if (optionName.value) {
    const newOption = {
      label: optionName.value,
      value: optionName.value,
    }
    settingsStore.addCustomSort(newOption)
    clear()
  }
}
const clear = () => {
  optionName.value = ''
  isAdding.value = false
}

const handleSortChange = (value) => {
  select_value.value = value
  emit('send_sort', value)
}
</script>

<style scoped lang="scss">
.switch {
  width: 40px;
  height: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  box-sizing: border-box;
  cursor: pointer;
  padding-bottom: 0;
  padding-top: 0;

  background-color: #ebeef5 !important;
  font-size: 12px;
}

.isDark-switch {
  .el-icon {
    background-color: #fff !important;
    padding: 2px;
    border-radius: 50%;
    color: #000;
    margin-left: -8px;
  }
}

.noDark-switch {
  background-color: rgb(8, 8, 8) !important;
  .el-icon {
    color: #fff;
    margin-left: 15px;
  }
}

.filter-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  
  .el-dropdown {
    position: absolute;
    right: 10px;
  }
  
  .el-input {
    width: 100%;
  }
}
</style>