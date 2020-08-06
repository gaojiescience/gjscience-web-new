// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import echarts from 'echarts'
import QS from 'qs'
import vueSwiper from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
import VueWechatTitle from 'vue-wechat-title';
import cookie from 'vue-cookie'

Vue.use(VueWechatTitle);
Vue.use(vueSwiper, /* { default options with global component } */);
Vue.prototype.$cookie = cookie;
Vue.prototype.$axios = axios;
Vue.prototype.qs = QS;
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});

// router.beforeEach((to,from,next) => {
//   if(to.meta.title){
//     document.title = to.meta.title
//   }
// });
