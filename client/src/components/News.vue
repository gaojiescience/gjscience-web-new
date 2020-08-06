<template>
  <!--<div class="root" v-wechat-title="title">-->
  <div class="root">
    <TopNavbar></TopNavbar>
    <!--<div class="page-holder">-->
    <!--</div>-->
    <div class="content-holder">
      <!--<div class="title-line">-->
        <!--{{ title }}-->
      <!--</div>-->
      <!--<div class="from-line">-->
        <!--{{ newsData.news_info.source }}  {{ publishDate }}-->
      <!--</div>-->
      <!--<div class="content">-->
        <!--<div v-for="(item, index) in newsData.news_info.content.data" class="content-line">-->
          <!--<img v-if="item.type === 'image'" :src="item.url">-->
          <!--<p v-if="item.type === 'text'" v-html="item.desc"></p>-->
        <!--</div>-->
      <!--</div>-->
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue"
import Footer from "./Footer.vue"
export default {
  name: 'News',
  components: {
//    SearchAssociation,
    TopNavbar,
    Footer
  },
  data () {
    return {
      id: this.$route.params.id,
//      title: this.$route.params.title,
      result: ""
    }
  },
  methods: {
    getNewsData: function () {
      const that = this;
      const targetUrl = "/news/highlight/detail?id=" + this.id;
      this.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res);
        that.result = res.data;
        let targetElement = document.getElementsByClassName("content-holder")[0];
        targetElement.innerHTML = that.result;
        document.getElementsByClassName("title")[0].style.cssText="color: black;";
        document.getElementsByClassName("h-name small")[0].style.cssText="color: black; font-size: 90%;";
        document.getElementsByClassName("search-img")[0].style.cssText="margin: 0 0;";
        document.getElementsByClassName("icon-img")[0].style.cssText="display: default; margin-top: 12px;";
//        that.newsData = res.data;
//        let date = new Date(res.data.news_info.publish_time*1000);
//        window.console.log(date);
//        that.publishDate = date.getFullYear() + "-" + (date.getMonth()+1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();

      })
    }

  },
  mounted() {
    this.getNewsData()
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .page-holder {
    width: 100vw;
    min-height: 100vh;
  }

  .content-holder {
    width: 40%;
    min-height: 90vh;
    margin-top: 6vh;
    display: flex;
    flex-direction: column;
    text-align: left;
    color: black !important;
    padding-bottom: 8vh;
  }
</style>
