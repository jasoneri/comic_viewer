<template>
    <el-container>
      <el-header>
        <TopBtnGroup :reload="reload" @send_sort="sv_sort"/>
      </el-header>
      <el-main>
        <el-scrollbar>
          <div class="demo-pagination-block">
            <el-pagination
              v-model:current-page="indexPage"
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
                               :to="{ path: 'book', query: { book: scope.row.book_name}}">
                    {{ scope.row.book_name }}
                  </router-link>
                </el-space>
              </template>
            </el-table-column>
          </el-table>
          <div class="demo-pagination-block">
            <el-pagination
                v-model:current-page="indexPage"
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
    import {h} from 'vue'
    import {backend,indexPage,bookList,sort_val,pageSize} from "@/static/store.js";
    import { RefreshRight } from '@element-plus/icons-vue'
    import {ElNotification} from "element-plus";
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroup from '@/components/TopBtnGroup.vue'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {useRoute} from "vue-router";

    const route = useRoute()
    let bookTotal = ref(0)

    // ------------------------后端交互 & 数据处理
    const getBooks = async(callBack) => {
      const params = {sort: sort_val.value};
      await axios.get(backend + '/comic/', {params})
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
      const start = (indexPage.value - 1) * pageSize;
      const end = start + pageSize;
      return bookList.slice(start, end);
    });
    // ------------------------渲染相关
    const init = () => {
      getBooks(callBack)
      function callBack(data){
        bookList.length = 0
        bookList.splice(0, bookList.length)
        bookList.push(...data)
        bookTotal.value = data.length
      }
    }
    init()
    const reload = () => {
      bookTotal.value = 0
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
    function sv_sort(val){
      sort_val.value = val
      reload()
    }

</script>
<style lang="scss" scoped>
    .app-container {
        display: flex;
        width: 100%;
        justify-content: center;
        .container {
            display: flex;
            flex-wrap: wrap;
            position: relative;
            .handler {
              display: flex;
              justify-content: center;
            }
        }
    }
</style>