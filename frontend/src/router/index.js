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
    title: "comic book"
  },
  component: () => import('@/view/book.vue')
},{
  path: '/kemono',
  name: 'kemono',
  meta: {
    title: "kemono artists"
  },
  component: () => import('@/view/kemono.vue')
},{
  path: '/kemono_books',
  name: 'kemono_books',
  meta: {
    title: "kemono artist books"
  },
  component: () => import('@/view/kemono_books.vue')
},{
  path: '/kemono_book',
  name: 'kemono_book',
  meta: {
    title: "kemono book"
  },
  component: () => import('@/view/kemono_book.vue')
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