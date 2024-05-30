// 引入vue router
import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [{
  path: '/',
  name: 'books',
  meta: {
    title: "comic books index"
  },
  component: () => import('@/view/comic.vue')
},{
  path: '/book',
  name: 'book',
  meta: {
    title: "comic waterfall"
  },
  component: () => import('@/view/book.vue')
}]
// 创建 vueRouter 实例
const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach((to, from) => {
    document.title=to.meta.title
})

export default router