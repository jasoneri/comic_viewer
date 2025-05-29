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
                                   :bookName="scope.row.book" :bookHandlePath="'/kemono/handle'" :handleApiBodyExtra="{u_s: u_s}"/>
                  </el-button-group>
                  <router-link :style="`font-size: var(--el-font-size-extra-large)`"
                               :to="{ path: 'kemono_book', query: {u_s: u_s, book: scope.row.book}}">
                    {{ scope.row.book }}
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
    import {computed,h} from 'vue';
    import axios from "axios";
    import {backend,indexPage,kemonoData,sortVal,pageSize} from "@/static/store.js";
    import {ElNotification} from "element-plus";
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroup from '@/components/TopBtnGroup.vue'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import {useRoute} from "vue-router";

    const route = useRoute()
    const u_s = route.query.u_s
    // ------------------------后端交互 & 数据处理
    const getBooks = async(callBack) => {
      const params = {u_s: u_s, sort: sortVal.value};
      await axios.get(backend + '/kemono/book/', {params})
        .then(res => {
          let result = res.data.map((_) => {
            return { book: _}
          });
          callBack(result)
        })
        .catch(function (error) {
          console.log(error);
        })
    }
    const bookTotal = computed(() => {
      return kemonoData.BookList.arr.length
    });
    const pagedBook = computed(() => {
      const start = (indexPage.value - 1) * pageSize;
      const end = start + pageSize;
      return kemonoData.BookList.arr.slice(start, end);
    });
    // ------------------------渲染相关
    const init = () => {
      getBooks(callBack)
      function callBack(data){
        kemonoData.BookList.arr = data
      }
    }
    init()
    const reload = init
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
      sortVal.value = val
      reload()
    }

</script>
<style lang="scss" scoped>
    @use '@/styles/books_list.scss';
</style>