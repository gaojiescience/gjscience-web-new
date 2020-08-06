<template>
  <div class="content-holder">
    <StockCommentsEditor v-bind:stock="stock" v-bind:name="name" v-bind:exchange="exchange" v-bind:isIndex="isIndex" style="z-index: 999"></StockCommentsEditor>
    <!--<img :src="avatar"/>-->
    <div class="header-bar">
      <div :class="'header-button ' + (selectedBlock === 'news' ? 'selected' : '')" v-on:click="selectBlock('news')">
        新闻
      </div>
      <div :class="'header-button ' + (selectedBlock === 'notice' ? 'selected' : '')" v-on:click="selectBlock('notice')">
        公告
      </div>
      <div :class="'header-button ' + (selectedBlock === 'comments' ? 'selected' : '')" v-on:click="selectBlock('comments')">
        讨论
      </div>
    </div>
    <div class="content-block">
      <div class="news-block" v-if="selectedBlock === 'news'">
        <div class="news-line" v-for="(item, index) in newsList">
          <div class="news-left">
            <img :src="item.thumbnail" v-on:click="jumpToNews(item.source_url)">
          </div>
          <div class="news-right">
            <div class="news-title">
              <p v-on:click="jumpToNews(index)">{{ item.title }}</p>
            </div>
            <div class="news-from">
              {{ item.media }} {{ item.pubTime.split(' ')[1] }}
            </div>
          </div>
        </div>
      </div>

      <div class="news-block" v-if="selectedBlock === 'notice'">
        <div class="notice-line" v-for="(item, index) in noticeList">
          <div class="notice-title">
            <p v-on:click="jumpToNotice(item.url)">{{ item.summary }}</p>
          </div>
          <div class="notice-date">
            {{ item.pubTime.split(' ')[0] }}
          </div>
        </div>
      </div>

      <div class="news-block" v-if="selectedBlock === 'comments'">
        <div class="comments-btn-header">
          <div :class="'comments-btn ' + (commentsType === 'today' ? 'selected-comments-type' : 'non-selected-comments-type')" v-on:click="commentsType = 'today';selectBlock('comments')">
            今日
          </div>
          <div :class="'comments-btn ' + (commentsType === 'hot' ? 'selected-comments-type' : 'non-selected-comments-type')" v-on:click="commentsType = 'hot';selectBlock('comments')">
            热门
          </div>
        </div>
        <div class="comments-line" v-for="(item, index) in commentsData">
          <div class="comments-header">
            <div class="header-box">
              <img :src="item.fields.avatar ? item.fields.avatar : avatar">
            </div>
            <div class="header-box">
              <a>{{ item.fields.nick }}</a> <span>· {{ item.fields.create_date.split("T")[1].split(".")[0] }}</span>
            </div>
          </div>
          <div class="comment-content" v-html="htmlDict[item.fields.comment_code]">
            <!--{{ htmlDict }}-->

          </div>
          <div class="comments-footer">
            <div class="footer-left">
              <div class="footer-box">
                <img src="../assets/turn.png"/>
                <span>转发</span>
              </div>
              <div class="footer-box">
                <img src="../assets/comments.png"/>
                <span>评论</span>
              </div>
              <div class="footer-box">
                <img src="../assets/agree.png"/>
                <span>点赞</span>
              </div>
            </div>
            <div class="footer-right">
              <div class="footer-box" v-on:click="showCommentsDetail(index)" v-if="commentsDetailList.indexOf(index) === -1">
                <img src="../assets/more.png"/>
                <span>展开</span>
              </div>
              <div class="footer-box" v-on:click="hideCommentsDetail(index)" v-else>
                <img src="../assets/more.png"/>
                <span>收起</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
//import RichTextEditor from "./RichTextEditor.vue"
import StockCommentsEditor from "./StockCommentsEditor.vue"
export default {
  name: 'Comments',
  components: {
    StockCommentsEditor,
  },
  props: {
    stock: {
      type: String
    },
    name: {
      type: String
    },
    exchange: {
      type: String
    },
    isIndex: {
      type: String
    }
  },
  data () {
    return {
      avatar: "http://127.0.0.1:8000/media/avatar/default_avatar.jpg",
      selectedBlock: "news",
      newsPage: 1,
      newsList: [],
      noticeList: [],
      commentsType: "today",
      commentsPage: 1,
      commentsData: [],
      htmlDict: [],
      commentsDetailList: []
    }
  },
  methods: {
    selectBlock: function (e) {
      window.console.log(e);
      this.selectedBlock = e;
      if (e === "news") {
        this.getStockNews()
      }
      else if (e === "notice") {
        this.getStockNotice()
      }
      else if (e === "comments") {
        this.getStockComments()
      }
    },
    getStockNews: function () {
      const that = this;
      const targetUrl = "https://www.laohu8.com/proxy/news/news/list?symbols=" + this.stock + "&pageCount=" + this.newsPage;
      this.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res);
        that.newsList = res.data.items;
      })
    },
    getStockNotice: function () {
      const that = this;
      const targetUrl = "https://www.laohu8.com/proxy/news/notice/list?symbols=" + this.stock;
      this.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res);
        that.noticeList = res.data.items;
      })
    },
    getStockComments: function () {
      const that = this;
      const targetUrl = "/api/comments?type=" + this.commentsType + "&stock=" + this.stock + "&page=" + this.commentsPage;
      window.console.log(this.commentsPage);
      this.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res.data);
        that.commentsData = res.data;
        for (let index in res.data) {
          that.getCommentHtml(that, res.data[index].fields.comment_code, res.data[index].fields.content_html,)

        }
      })
    },
    getCommentHtml: function (that, code, path) {
      const that_ = that;
      that.$axios.get("/api/"+path, {}).then(function (res) {
        window.console.log(res)
        that_.htmlDict[code] = res.data;
        that.$forceUpdate();
//        that.userName = res.data;
      })
    },
    jumpToNotice: function (url) {
      window.open(url,'_blank')
    },
    jumpToNews: function (index) {
//      "http://gu.qq.com/resources/shy/news/detail-v2/index.html#/?id=nesSN202008041444237a98e68a&s=b"
//      https://snp.tenpay.com/cgi-bin/snpgw_unified_newsinfo.fcgi?&filter=0&news_id=SN202008041444237a98e68a&zappid=zxg_h5&sign=0fc7a79b0ac20c7376b2a7a7c60bc6c0&nonce=536&reserve=1572995&&channel=zxg&user_openid=undefined&user_skey=undefined
      const targetData = this.newsList[index];
      window.console.log(targetData);
      const id = targetData.id;
      const newPage = this.$router.resolve({
        name: "News",
        params: {
          id: id,
        }
      });
      window.open(newPage.href,'_blank')
    },
    showCommentsDetail: function (index) {
      let targetElement = document.getElementsByClassName("comments-line")[index];
      window.console.log(targetElement.childNodes[2]);
      targetElement.childNodes[2].style.cssText="transition: height 1s; height: auto !important;";
      window.console.log(targetElement);
      this.commentsDetailList.push(index)
    },
    hideCommentsDetail: function (index) {
      let targetElement = document.getElementsByClassName("comments-line")[index];
      targetElement.childNodes[2].style.cssText="transition: height 1s; height: 63px !important;";
      window.console.log(this.commentsDetailList)
      this.commentsDetailList.splice(this.commentsDetailList.indexOf(index), 1);
      window.console.log(this.commentsDetailList)
      window.console.log(this.commentsDetailList.indexOf(index))
    }
  },
  mounted() {
    this.getStockNews();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .content-holder {
    width: 100%;
    /*min-height: 30vh;*/
    /*background-color: red;*/
  }

  .content-holder img {
    width: 100px;
    height: 100px;
  }

  .header-bar {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: flex-start;
    /*background-color: red;*/
    margin-top: 10px;
    border-bottom: 1px solid #f7f7fa;
  }

  .header-button {
    width: 80px;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
  }

  .selected {
    color: #06c !important;
    border-bottom: 2px solid #0084ff;
  }

  .content-block {
    width: 100%;
  }

  .news-block {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .news-line {
    width: 100%;
    height: 115px;
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    border-bottom: 1px solid #f7f7fa;
  }

  .news-left {
    width: 160px;
    height: 95px;
    margin-top: 10px;
    overflow: hidden;
  }

  .news-left img {
    width: 100%;
    height: 100%;
    cursor: pointer;
    transition: transform 1s;
  }

  .news-left img:hover {
    transform: scale(1.2);
  }

  .news-right {
    width: 520px;
    text-align: left;
    /*text-indent: 50px;*/
    height: 95px;
    margin-top: 10px;
  }

  .news-title {
    width: 100%;
    height: 70px;
    line-height: 20px;
    font-weight: 600;
    word-wrap: break-word;
  }

  .news-from {
    font-size: 90%;
    color: #a6a9b6;
  }

  .news-title p {
    cursor: pointer;
  }

  .news-title p:hover {
    color: #0084ff;
  }

  .notice-line {
    width: 100%;
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-top: 20px;
    border-bottom: 1px solid #f7f7fa;
  }

  .notice-title {
    width: 100%;
    height: 35px;
    line-height: 20px;
    text-align: left;
    text-indent: 20px;
    cursor: pointer;
  }

  .notice-date {
    width: 100%;
    height: 25px;
    line-height: 15px;
    text-align: right;
    font-size: 90%;
    color: #a6a9b6;
  }

  .notice-title p:hover {
    color: #0084ff;
  }

  .comments-btn-header {
    width: 100%;
    height: 50px;
    display: flex;
    /*line-height: 50px;*/
    font-size: 90%;
  }

  .comments-btn {
    width: 60px;
    height: 25px;
    line-height: 25px;
    cursor: pointer;
    margin-top: 12.5px;
    border-radius: 3px;
  }

  .selected-comments-type {
    background-color: #0084ff;
    color: white;
  }

  /*.non-selected-comments-type {*/

  /*}*/

  /*.non-selected-comments-type:hover {*/
    /*background-color: #e6f1fb;*/
  /*}*/
  .comments-line {
    width: 100%;
    /*height: 140px;*/
    display: flex;
    flex-direction: column;
    margin-top: 20px;
    border-bottom: 1px solid #f7f7fa;
    transition: height 1s;
  }

  .comments-header {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: flex-start;
    margin-bottom: 20px;
  }

  .header-box {
    height: 40px;
  }

  .header-box img {
    width: 33px;
    height: 33px;
    margin-top: 3.5px;
    border-radius: 5px;
  }

  .header-box a {
    line-height: 20px;
    height: 20px;
    margin-top: 10px;
    display: inline-block;
    margin-left: 15px;
  }

  .header-box span {
    color: #a6a9b6;
  }

  .comment-content {
    width: 100%;
    height: 63px;
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    transition: height 1s;
    /*margin-top: 20px;*/
    /*margin-bottom: 5px;*/
    /*background-color: red;*/
  }

  /deep/ .comment-content img {
    width: 100%;
    margin-top: 10px;
  }

  .comments-footer {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  .footer-left {
    width: 70%;
    height: 100%;
    display: flex;
  }

  .footer-right {
    width: 30%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
  }

  .footer-box {
    width: 60px;
    height: 25px;
    display: flex;
    cursor: pointer;
    margin-top: 10px;
    margin-right: 10px;
    /*background-color: red;*/
  }

  .footer-box img {
    width: 20px;
    height: 20px;
    margin-top: 2.5px;
  }

  .footer-box span {
    display: inline-block;
    height: 40px;
    line-height: 25px;
    font-size: 90%;
    color: #8a8a8a;
    text-indent: 5px;

  }

  .comments-detail {
    height: auto;
  }

</style>
