<template>
    <el-container>
      <el-header>
        <TopBtnGroup :reload="reload" :items="bookList" :filtered-items="filteredBookList" :handle-conf="handleConf"
                     @send_sort="sv_sort"/>
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
                                   :bookName="scope.row.book_name" :bookHandlePath="'/comic/handle'" />
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
    import {computed,h} from 'vue';
    import axios from "axios";
    import {backend,indexPage,bookList,filteredBookList,sortVal,pageSize} from "@/static/store.js";
    import {ElNotification} from "element-plus";
    import topBottom from '@/components/topBottom.vue'
    import TopBtnGroup from '@/components/TopBtnGroup.vue'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'

    // ------------------------后端交互 & 数据处理
    const getBooks = async(callBack) => {
      const params = {sort: sortVal.value};
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
    const bookTotal = computed(() => {
      return filteredBookList.arr.length
    });
    const pagedBook = computed(() => {
      const start = (indexPage.value - 1) * pageSize;
      const end = start + pageSize;
      return filteredBookList.arr.slice(start, end);
    });
    const handleConf = async(param) => {
      if (typeof param === "function") {
        await axios.get(backend + '/comic/conf/')
          .then(res => {param(res.data);})
          .catch(function (error) {console.log(error);})
      } else if (typeof param === "string") {
        let body = {text: param};
        await axios.post(backend + '/comic/conf/', body)
          .then(res => {
            reload();
            ElNotification.success({
              title: '配置更改已成功',
              message: h('i', { style: 'white-space: pre-wrap; word-wrap: break-word;' }, `改配置后端会对静态资源锚点进行更新\n切换后点第一遍点书读图会404，再点下书就好了\n（目前未解，操作多了一点点而已）`),
              offset: 100,
              duration: 7000
            })
          })
          .catch(
              function (error) {
                ElNotification.error({
                  title: 'Error',
                  message: '处理配置发生错误，自行去终端窗口查看报错堆栈',
                  offset: 100,
                })
              }
          )
      } else {
         console.log("handleConf-param type = " + typeof param);
      }
    }
    // ------------------------渲染相关
    const init = () => {
      getBooks(callBack)
      function callBack(data){
        bookList.arr = data
        filteredBookList.arr = data
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