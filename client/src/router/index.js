import Vue from 'vue';
import Router from 'vue-router';
// import HelloWorld from '@/components/HelloWorld';
import HomePage from '@/components/HomePage';
import MarketPage from '@/components/MarketPage';
import StockPage from '@/components/StockDetail';
import IndexPage from '@/components/IndexPage'
import Register from '@/components/Register'
import Login from '@/components/Login'
import News from '@/components/News'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
      meta: {
        title: "高街科技-首页"
      }
    },
    {
      path: '/market',
      name: 'MarketPage',
      component: MarketPage,
      meta: {
        title: "高街科技-行情"
      }
    },
    {
      path: '/stock/:exchange/:stock/:type',
      name: 'StockPage',
      component: StockPage,
      // meta: {
      //   title: this.$route.params.stock
      // }
    },
    {
      path: '/community',
      name: 'IndexPage',
      component: IndexPage,
      meta: {
        title: "高街科技-社区"
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        title: "高街科技-注册"
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        title: "高街科技-登录"
      }
    },
    {
      path: '/news/:id/',
      name: 'News',
      component: News,
    },
  ]
})
