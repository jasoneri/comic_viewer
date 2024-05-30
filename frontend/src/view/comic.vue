<template>
    <el-container>
      <el-header>
        <el-button-group style="width: 100%; height: 100%; margin: 0 auto; display: block;">
          <Dark style="width: 15%; height: 100%"/>
          <el-button type="primary" :icon="RefreshRight" @click="reload"
                     style="width: 85%; height: 100%; margin: 0 auto; display: block; font-size: 18px">
            重新加载页面</el-button>
        </el-button-group>
      </el-header>
      <el-main>
        <el-scrollbar>
          <div class="demo-pagination-block">
            <el-pagination
              v-model:current-page="currentPage"
              :page-size="pageSize" :total="bookTotal"
              layout="prev, pager, next, jumper"
            />
          </div>
          <el-table :data="pagedBook">
            <el-table-column prop="book" label="Book" >
              <template v-slot="scope">
                <el-space wrap :size="'small'">
                  <el-button-group>
                    <bookHandleBtn :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack"
                                   :bookName="scope.row.book_name"/>
                  </el-button-group>
                  <router-link :style="`font-size: var(--el-font-size-extra-large)`"
                               :to="{ path: 'book', query: { book: scope.row.book_name, index_page: currentPage }}">
                    {{ scope.row.book_name }}
                  </router-link>
                </el-space>
              </template>
            </el-table-column>
          </el-table>
          <div class="demo-pagination-block">
            <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize" :total="bookTotal"
                layout="prev, pager, next, jumper"
            />
          </div>
        </el-scrollbar>
        <topBottom></topBottom>
      </el-main>
    </el-container>
</template>
<script setup>
    import {reactive, ref, computed} from 'vue';
    import axios from "axios";
    import { h } from 'vue'
    import {backend} from "@/utils/settings.js";
    import { RefreshRight } from '@element-plus/icons-vue'
    import {ElNotification} from "element-plus";
    import topBottom from '@/components/topBottom.vue'
    import Dark from '@/components/darkModeBtn.vue'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {useRoute} from "vue-router";

    const route = useRoute()
    let bookList = reactive([])
    let bookTotal = ref(0)
    let currentPage = route.query.page ? ref(parseInt(route.query.page)) : ref(1)
    let pageSize = 20

    // ------------------------后端交互 & 数据处理
    const getBooks = async(callBack) => {
      await axios.get(backend + '/comic/')
        .then(res => {
          let result = res.data.map((_) => {
            return { book_name: _}
          });
          callBack(result)
        })
        .catch(function (error) {
          console.log(error);
        })
    }
    const pagedBook = computed(() => {
      const start = (currentPage.value - 1) * pageSize;
      const end = start + pageSize;
      return bookList.slice(start, end);
    });
    // ------------------------渲染相关
    const init = () => {
      getBooks(callBack)
      function callBack(data){
        bookList.push(...data)
        bookTotal.value = data.length
      }
    }
    init()
    const reload = () => {
      bookTotal.value = 0
      bookList.length = 0
      bookList.splice(0, bookList.length)
      init()
    }
    function retainCallBack(done, path){
        notification('已移至保留['+done+']', 'success', path)
        reload()
      }
    function removeCallBack(done, path){
        notification('已移至待删除['+done+']', 'warning', path)
        reload()
      }
    function delCallBack(done, _){
        notification('已删除['+done+']', 'error', _)
        reload()
      }
    const notification = (handle, _type, book) => {
      ElNotification({
        title: handle,
        message: h('i', { style: 'color: teal;font-size: 18px' }, book),
        type: _type,
        duration: 3500,
      })
    }

</script>
<style lang="scss" scoped>
    .app-container {
        display: flex;
        width: 100%;
        justify-content: center;
        .container {
            width: v-bind(waterfallWidthPx);
            display: flex;
            flex-wrap: wrap;
            position: relative;
            .handler {
              width: v-bind(waterfallWidthPx);
              display: flex;
              justify-content: center;
            }
        }
    }
</style>