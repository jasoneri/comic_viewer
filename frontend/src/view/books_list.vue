<template>
    <el-container>
      <el-header height="5vh">
        <TopBtnGroup :reload="reload" :items="bookList" :filtered-items="filteredBookList" :handle-conf="handleConf" 
                     :handle-filter="handleFilter" :keywords_list="keywords_list" v-model="isListMode" @send_sort="sv_sort"/>
      </el-header>
      <el-main>
        <el-scrollbar ref="scrollbarRef">
          <div class="demo-pagination-block">
            <el-pagination
              v-model:current-page="indexPage"
              :page-size="pageSize" :total="bookTotal"
              layout="prev, pager, next, jumper"
            />
          </div>
          <!-- 列表视图 -->
          <el-table v-if="isListMode" :data="pagedBook">
            <el-table-column prop="book" label="Book" >
              <template v-slot="scope">
                <el-space wrap :size="'small'">
                  <el-button type="info"  style="width: 20%;height: 100%;" @click="setFilter(scope.row.book_name)">
                    <el-icon size="large"><Filter /></el-icon>
                  </el-button>
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
          <!-- 网格视图 -->
          <div v-else class="grid-container">
            <el-row :gutter="20">
              <el-col v-for="book in pagedBook" :key="book.book_name" :span="4" :xs="12" :sm="8" :md="6" :lg="4">
                <el-card :body-style="{ padding: '0px' }" class="book-card">
                  <router-link :to="{ path: 'book', query: { book: book.book_name}}">
                    <el-image :src="backend+book.first_img" class="book-image" :title="book.book_name" fit="cover">
                      <template #error>
                        <div class="error-container">
                          <img src="/empty.png" :alt="errorText" />
                          <div class="error-text" v-html="errorText"></div>
                        </div>
                      </template>
                    </el-image>
                    <div class="book-info">
                      <span class="book-title">{{ book.book_name }}</span>
                    </div>
                  </router-link>
                  <div class="book-actions">
                    <el-button style="width: 20%;height: 100%;" type="info" @click="setFilter(book.book_name)">
                      <el-icon size="large"><Filter /></el-icon>
                    </el-button>
                    <el-button-group :style="`width:100%;`">
                      <bookHandleBtn
                        :retainCallBack="retainCallBack" :removeCallBack="removeCallBack" :delCallBack="delCallBack"
                        :bookName="book.book_name" :bookHandlePath="'/comic/handle'" />
                    </el-button-group>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <div class="demo-pagination-block">
            <el-pagination
                v-model:current-page="indexPage"
                :page-size="pageSize" :total="bookTotal"
                layout="prev, pager, next, jumper"
            />
          </div>
          <topBottom :scrollbarRef="scrollbarRef" :hideDown="true"/>
        </el-scrollbar>
      </el-main>
    </el-container>
</template>

<script setup>
    import {computed, h, ref} from 'vue';
    import axios from "axios";
    import {backend,indexPage,bookList,filteredBookList,sortVal,pageSize} from "@/static/store.js";
    import {ElNotification,ElMessage} from "element-plus";
    import TopBtnGroup from '@/components/TopBtnGroup.vue'
    import bookHandleBtn from '@/components/bookHandleBtn.vue'
    import topBottom from '@/components/topBottom.vue'
    import { Filter } from '@element-plus/icons-vue';

    const isListMode = ref(true);
    const filterKeyword = ref('');
    const keywords_list = ref([]);
    const scrollbarRef = ref(null)
    const errorText = computed(() => '这目录..<br>没有图片...')

    // 添加过滤方法
    const applyFilter = (data) => {
      if (filterKeyword.value) {
        filteredBookList.arr = data.filter(item => item.book_name.includes(filterKeyword.value))
      } else {
        filteredBookList.arr = data
      }
    }

    const extractKeywords = (book_name) => {
      if (book_name.includes('[') && book_name.includes(']')) {
        return book_name.split('[')[1].split(']')[0]
      } else if (book_name.includes('_')) {
        return book_name.split('_')[0]
      }
      return null
    }

    // ------------------------后端交互 & 数据处理
    const getBooks = async(callBack) => {
      const params = {sort: sortVal.value};
      await axios.get(backend + '/comic/', {params})
        .then(res => {
          let result = res.data
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
      // 从 localStorage 读取排序值
      const savedSort = localStorage.getItem('sortValue')
      if (savedSort) {
        sortVal.value = savedSort
      }
      
      // 从 localStorage 读取筛选关键字
      const savedFilter = localStorage.getItem('filterKeyword')
      if (savedFilter) {
        filterKeyword.value = savedFilter
      }
      
      getBooks(callBack)
      function callBack(data){
        bookList.arr = data
        applyFilter(data)
        // 异步提取关键词
        setTimeout(() => {
          const keywords = new Set()
          data.forEach(book => {
            const keyword = extractKeywords(book.book_name)
            if (keyword) keywords.add(keyword.slice(0, 20))
          })
          keywords_list.value = Array.from(keywords).sort((a, b) => a.localeCompare(b))
        }, 0)
      }
    }
    init()
    const reload = (refreshFilterKeyword = false) => {
      if (refreshFilterKeyword) {
        filterKeyword.value = ''
        localStorage.removeItem('filterKeyword')
      }
      init()
    }
    function retainCallBack(done, path){
        notification('已移至保留目录', 'success', path)
        reload()
      }
    function removeCallBack(done, path){
        notification('已删至回收站', 'warning', path)
        reload()
      }
    function delCallBack(done, _){
        notification('已彻底删除', 'error', _)
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

    const handleFilter = (keyword) => {
      filterKeyword.value = keyword
      localStorage.setItem('filterKeyword', keyword)
      applyFilter(bookList.arr)
    }

    const setFilter = (book_name) => {
      // 1. 当book_name为`[artist]xxx`形式时，keyword=artist
      // 2. 当book_name为`xxx_第N话`形式时，keyword=xxx
      // 3. 当book_name为`xxx`形式时，keyword=xxx
      let keyword
      if (book_name.includes('[') && book_name.includes(']')) {
        keyword = book_name.split('[')[1].split(']')[0]
        handleFilter(keyword)
      } else if (book_name.includes('_')) {
        keyword = book_name.split('_')[0]
        handleFilter(keyword)
      } else {
        ElMessage({
          message: '没有适用过滤的规则',
          type: 'warning',
        });
      }
    }

</script>
<style lang="scss" scoped>
    @use '@/styles/books_list.scss';

.error-container {
  position: relative;
  display: inline-block;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  img {
    width: 100%;
    height: auto;
    object-fit: contain;
    margin-top: 3px;
  }
}

.error-text {
  position: relative;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-top: 10px;
  padding: 0 5px;
  
  /* 可选文字阴影增强可读性 */
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.925);
}
</style>