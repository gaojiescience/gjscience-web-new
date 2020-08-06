<template>
  <div class="root">
    <TopNavbar></TopNavbar>
    <div class="center-holder">
      <div class="center-left">
        <div class="content-box">
          <div class="box-header">
            <div class="header-title">
              <h2>今日指数</h2>
            </div>
            <div class="header-btn">
              <div :class="(nowChosenMarket == 'sh' ? 'underline' : '')" id="sh" @click="changeMarket">
                <span>A股</span>
              </div>
              <div :class="(nowChosenMarket == 'hk' ? 'underline' : '')" id="hk" @click="changeMarket">
                <span>港股</span>
              </div>
              <div :class="(nowChosenMarket == 'us' ? 'underline' : '')" id="us" @click="changeMarket">
                <span>美股</span>
              </div>
            </div>
          </div>
          <div class="box-center">
            <div class="left-box">
              <div class="echarts-box" id="timeLine">
                <img :src="timeLineUrl"/>
              </div>
            </div>
            <div class="right-box">
              <div class="box-header right-box-header">
                <div class="header-btn more-width">
                  指数
                </div>
                <div class="header-btn">
                  最新价
                </div>
                <div class="header-btn">
                  涨跌幅
                </div>
              </div>
              <div class="box-center right-box-center">
                <div :class="'box-center-line ' + (item[3] == nowChosenIndex ? 'background-gray' : '')" v-for="(item, index) in indexList" v-bind:key="index" :id="item[3]" @click="changeIndex">
                  <div class="line-first">
                    {{ item[0] }}
                  </div>
                  <div class="line-second">
                    {{ item[1] }}
                  </div>
                  <div :class="'line-third ' + (item[2] > 0 ? 'color-red' : 'color-green')">
                    {{ item[2] }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="content-box">
          <div class="box-header">
            <div class="header-title">
              <h2>涨跌排行</h2>
            </div>
            <div class="header-btn">
              <div :class="(nowChosenRank == 'ash' ? 'underline' : '')" id="ash" @click="getRankData('ash')">
                <span>沪A</span>
              </div>
              <div :class="(nowChosenRank == 'asz' ? 'underline' : '')" id="asz" @click="getRankData('asz')">
                <span>深A</span>
              </div>
              <div :class="(nowChosenRank == 'r_main_h' ? 'underline' : '')" id="r_main_h" @click="getRankData('r_main_h')">
                <span>港股</span>
              </div>
            </div>
          </div>
          <div class="box-center rank-box">
            <div class="right-box right-rank-box">
              <div class="box-header right-box-header">
                <div class="header-btn more-width">
                  领涨排行
                </div>
                <div class="header-btn">
                  最新价
                </div>
                <div class="header-btn">
                  涨跌幅
                </div>
              </div>
              <div class="box-center right-box-center">
                <div class="box-center-line" v-for="(item, index) in rankTop10" v-bind:key="index" v-on:click="jumpToStock(item.split('~')[3])">
                  <div class="line-first">
                    {{ item.split("~")[0] }}
                  </div>
                  <div class="line-second color-red">
                    {{ item.split("~")[1] }}
                  </div>
                  <div class="line-third color-red">
                    {{ item.split("~")[2] }}%
                  </div>
                </div>
              </div>
            </div>
            <div class="right-box right-rank-box">
              <div class="box-header right-box-header">
                <div class="header-btn more-width">
                  领跌排行
                </div>
                <div class="header-btn">
                  最新价
                </div>
                <div class="header-btn">
                  涨跌幅
                </div>
              </div>
              <div class="box-center right-box-center">
                <div class="box-center-line" v-for="(item, index) in rankEnd10" v-bind:key="index" v-on:click="jumpToStock(item.split('~')[3])">
                  <div class="line-first">
                    {{ item.split("~")[0] }}
                  </div>
                  <div class="line-second color-green">
                    {{ item.split("~")[1] }}
                  </div>
                  <div class="line-third color-green">
                    {{ item.split("~")[2] }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="content-box">
          <div class="box-header">
            <div class="header-title">
              <h2>每日提示</h2>
            </div>
            <div class="header-btn">
              <div :class="(nowChosenTips == 'new' ? 'underline' : '')" @click="getTipsData('new')">
                <span>新股上市</span>
              </div>
              <!--<div :class="(nowChosenTips == 'stop' ? 'background-gray' : '')" @click="getTipsData('stop')">-->
                <!--停盘提示-->
              <!--</div>-->
            </div>
          </div>
          <div class="box-center">
            <div class="right-box right-rank-box tip-box" v-if="showIPO">
              <div class="box-header right-box-header">
                <div class="header-btn">
                  代码
                </div>
                <div class="header-btn">
                  简称
                </div>
                <div class="header-btn more-width">
                  上网发行日期
                </div>
                <div class="header-btn">
                  发行量
                </div>
                <div class="header-btn">
                  上网发行量
                </div>
                <div class="header-btn">
                  发行价格
                </div>
                <div class="header-btn">
                  市盈率
                </div>
                <div class="header-btn">
                  募集资金
                </div>
              </div>
              <div class="box-center right-box-center">
                <div class="box-center-line" v-for="(item, index) in IPOData" v-bind:key="index">
                  <div class="line-second">
                    {{ item.symbol.substring(2) }}
                  </div>
                  <div class="line-second">
                    {{ item.name }}
                  </div>
                  <div class="line-first">
                    {{ item.sgrq }}
                  </div>
                  <div class="line-third">
                    {{ item.volume == '' ? '--' : item.volume }}
                  </div>
                  <div class="line-third">
                    {{ item.online_volume == '' ? '--' : item.online_volume }}
                  </div>
                  <div class="line-third">
                    {{ item.price }}
                  </div>
                  <div class="line-third">
                    {{ item.syl == '' ? '--' : item.syl }}
                  </div>
                  <div class="line-third">
                    {{ item.zjjdr }}
                  </div>
                </div>
              </div>
            </div>
            <div class="right-box right-rank-box tip-box" v-else>
              <div class="box-header right-box-header">
                <div class="header-btn more-width">
                  证券名称
                </div>
                <div class="header-btn">
                  停牌时间
                </div>
                <div class="header-btn">
                  复牌时间
                </div>
                <div class="header-btn">
                  停牌期限
                </div>
                <div class="header-btn">
                  停牌原因
                </div>
              </div>
              <div class="box-center right-box-center">
                <div class="box-center-line" v-for="(item, index) in rankTop10" v-bind:key="index">
                  <div class="line-first">
                    {{ item.split("~")[0] }}
                  </div>
                  <div class="line-second color-red">
                    {{ item.split("~")[1] }}
                  </div>
                  <div class="line-third color-red">
                    {{ item.split("~")[2] }}%
                  </div>
                  <div class="line-third color-red">
                    {{ item.split("~")[2] }}%
                  </div>
                  <div class="line-third color-red">
                    {{ item.split("~")[2] }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="center-right">
        <div class="news-block">
          <div class="swiper">
            <swiper class="swiper-holder" ref="mySwiper" :options="swiperOptions">
              <swiper-slide class="swiper-box" v-for="(item, index) in newsSwiperList" v-bind:key="index">
                <a class="swiper-box">
                  <img :src="item.img">
                  <p>{{ item.title }}</p>
                </a>
              </swiper-slide>
              <!--<swiper-slide class="swiper-box">-->
                <!--<a>-->
                  <!--<img :src="newsSwiperList[1].img">-->
                  <!--<p>{{ newsSwiperList[1].title }}</p>-->
                <!--</a>-->
              <!--</swiper-slide>-->
              <!--<swiper-slide class="swiper-box">-->
                <!--<a>-->
                  <!--<img :src="newsSwiperList[2].img">-->
                  <!--<p>{{ newsSwiperList[2].title }}</p>-->
                <!--</a>-->
              <!--</swiper-slide>-->
              <div class="swiper-pagination" slot="pagination"></div>
            </swiper>
          </div>
          <div class="content-box">
            <div class="box-header">
              <div class="header-title">
                <h2>要闻</h2>
              </div>

            <!--<div class="header-btn">-->
              <!--<div :class="(nowChosenTips == 'new' ? 'background-gray' : '')" @click="getTipsData('new')">-->
                <!--新股上市-->
              <!--</div>-->
              <!--&lt;!&ndash;<div :class="(nowChosenTips == 'stop' ? 'background-gray' : '')" @click="getTipsData('stop')">&ndash;&gt;-->
                <!--&lt;!&ndash;停盘提示&ndash;&gt;-->
              <!--&lt;!&ndash;</div>&ndash;&gt;-->
            <!--</div>-->
            </div>
            <div class="news-list" v-for="(item, index) in newsList" v-bind:key="index">
              <div class="news-line">
                <a>{{ item.title }}</a>
              </div>
            </div>
          </div>

          <div class="content-box">
            <div class="box-header">
              <div class="header-title">
                <h2>研究</h2>
              </div>

            <!--<div class="header-btn">-->
              <!--<div :class="(nowChosenTips == 'new' ? 'background-gray' : '')" @click="getTipsData('new')">-->
                <!--新股上市-->
              <!--</div>-->
              <!--&lt;!&ndash;<div :class="(nowChosenTips == 'stop' ? 'background-gray' : '')" @click="getTipsData('stop')">&ndash;&gt;-->
                <!--&lt;!&ndash;停盘提示&ndash;&gt;-->
              <!--&lt;!&ndash;</div>&ndash;&gt;-->
            <!--</div>-->
            </div>
            <div class="news-list" v-for="(item, index) in researchList" v-bind:key="index">
              <div class="news-line">
                <a>{{ item.title }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="footer">
      <div class="footer-content">
        <div class="footer-box">
          <div class="footer-about">
            <a class="footer-btn">
              关于我们
            </a>
            <a class="footer-btn">
              用户守则
            </a>
          </div>
          <div class="footer-line">
            Copyright 2019 高街科技(深圳)有限公司 版权所有 粤ICP备19073853号
          </div>
        </div>
        <div class="footer-box">
          <div class="footer-about-right">
            <a class="footer-btn-right">
              意见反馈、互联网违法和不良信息投诉
            </a>
            <a class="footer-btn-right">
              info@GJScience.com  联系电话  075526919025
            </a>
            <!--<a class="footer-btn">-->
              <!--用户守则-->
            <!--</a>-->
          </div>
          <div class="footer-line-right">
            Copyright 2019 高街科技(深圳)有限公司 版权所有 粤ICP备19073853号
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue"
export default {
  name: 'MarketInfo',
  components: {
//    SearchAssociation,
    TopNavbar
  },
  data () {
    return {
      swiperOptions: {
        pagination: {
          el: '.swiper-pagination'
        },
        // Some Swiper option/callback...
      },
      newsSwiperList: [],
      newsList: [],
      researchList: [],
      indexList: [],
      rankTop10: [],
      rankEnd10: [],
      IPOData: [],
      nowChosenRank: "ash",
      exchangeDict: {
        "ash": "sh",
        "asz": "sz",
        "r_main_h": "hk"
      },
      nowChosenTips: "new",
      nowChosenIndex: "sh000300",
      timeLineUrl: "https://imgnode.gtimg.cn/hq_img?code=sh000001&type=minute&size=1&proj=quotecenter",
      nowChosenMarket: "sh",
      showIPO: true,
      indexDict: {
        "sh": {
          "sh000300": "沪深300指数",
          "sh000001": "上证指数",
          "sz399001": "深证成指"
        },
        "hk": {
          "hkHSI": "恒生指数",
          "hkHSCEI": "国企指数",
          "hkHSCCI": "红筹指数"
        },
        "us": {
          "usDJI": "道琼斯",
          "usIXIC": "纳斯达克",
          "usINX": "标普500"
        },

      },
//      nowChosenMarketDateParamsDict: {
//        "sh": ["9:30", "15:00", [121, 210]],
//        "hk": ["9:30", "16:00", [151, 210]],
//        "sz": ["9:30", "15:00", [121, 210]],
//        "us": ["9:30", "16:00", [0, 0]]
//      },
//      nowChosenMarketDateList: [],
//      nowChosenMarketDataList: [],
//      nowChosenMarketShowDateDict: {
//        "sh": ["9:30", "11:30/13:00", "15:00"],
//        "hk": ["9:30", "12:00/13:00", "16:00"],
////        "hk": ["9:30", "11:30/13:00", "15:00"],
//        "us": ["9:30", "16:00"],
//        "sz": ["9:30", "11:30/13:00", "15:00"]
//      },

    }
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.$swiper
    }
  },
  methods: {
    jumpToStock: function (stock) {
      const newPage = this.$router.resolve({
        name: "StockPage",
        params: {
          type: "GP",
          exchange: this.exchangeDict[this.nowChosenRank],
          stock: stock,
        }
      });
      window.open(newPage.href,'_blank')
    },
    getResearchData: function () {
      const that = this;
      const targetUrl = "/api/current";
      this.$axios.get(targetUrl, {}).then(function (res){
        that.researchList = res.data;
      })
    },
    getNewsData: function () {
      const that = this;
      const targetUrl = "/api/news";

      this.$axios.get(targetUrl, {}).then(function (res){
        that.newsSwiperList = res.data.slice(0, 3);
        that.newsList = res.data.slice(3, 10);
//        window.console.log(that.newsSwiperList);
      })
    },
    getTipsData: function (type) {
      const that = this;
      if (type == "new") {
        const targetUrl = "https://web.ifzq.finance.qq.com/stock/notice/ipo/search?market=hs&detail=1&_var=v_xgbz20";
        this.showIPO = true;
        this.nowChosenTips = "new";
        this.$axios.get(targetUrl, {}).then(function (res){
          const ipoData = JSON.parse(res.data.split("=")[1]).data.jjfx;
          that.IPOData = ipoData;
//          window.console.log(ipoData)
        })
      }
      else {
        const targetUrl = "https://stockjs.finance.qq.com/sstock/js/oTfp.js";
        this.showIPO = false;
        this.nowChosenTips = "stop";
        this.$axios.get(targetUrl, {}).then(function (res){
          const ipoData = JSON.parse(res.data.split("=")[1].split(";")[0]).datas;
          that.IPOData = ipoData;
//          window.console.log(ipoData)
        })
      }
    },
    getRankData: function (type) {
      const targetUrl = "https://qt.gtimg.cn/q=" + type + "zdftop10," + type + "zdfend10";
      const that = this;
      this.$axios.get(targetUrl, {}).then(function (res){
//        window.console.log(res)
        that.rankTop10 = res.data.split('"')[1].split("^");
        that.rankEnd10 = res.data.split('"')[3].split("^");
        that.rankTop10.pop();
        that.rankEnd10.pop();
        that.nowChosenRank = type;
//        window.console.log(res.data.split('"')[1].split("^"));
//        window.console.log(res.data.split('"')[3].split("^"))
      })
    },
    changeIndex: function (event) {
      this.nowChosenIndex = event.path[1].id;
//      window.console.log(event)
      this.getTimeLineUrl();
    },
    changeMarket: function (event) {
      window.console.log(event.path[1])
      this.nowChosenMarket = event.path[1].id;
      this.getMarketIndexList(this.nowChosenMarket);
      window.console.log(this.indexList);
      this.nowChosenIndex = Object.keys(this.indexDict[this.nowChosenMarket])[0];
      this.getTimeLineUrl();
    },
    getMarketIndexList: function (market) {
//      this.indexList = this.indexDict[market];
      let stockParams = "";
      const that = this;
      this.indexList = [];
//      window.console.log(Object.keys(this.indexDict[market]));
      for (let index in Object.keys(this.indexDict[market])) {
//        window.console.log(index);
        stockParams += (Object.keys(this.indexDict[market])[index] + ",")
      }
      const targetUrl = "http://qt.gtimg.cn/q=" + stockParams;
//      let stockData = [];
//      window.console.log(targetUrl);
      this.$axios.get(targetUrl, {}).then(function (res){
//        window.console.log(res)
        res = res.data.substr(0, res.data.length-2).split(";");
//        window.console.log(res);
        for (let index in res) {
          let data = [];
          data.push(res[index].split("~")[1]);
          data.push(res[index].split("~")[3]);
          data.push(parseFloat(res[index].split("~")[32]));
          data.push(Object.keys(that.indexDict[market])[index]);
          that.indexList.push(data);
//          window.console.log(data)
        }
      })
    },
    getTimeLineUrl: function () {
      this.timeLineUrl = "https://imgnode.gtimg.cn/hq_img?code=" + this.nowChosenIndex + "&type=minute&size=1&proj=quotecenter"
    }
//    createDateList: function (start, end, stop) {
//      const startDate = new Date(2020, 0, 1, parseInt(start.split(":")[0]), parseInt(start.split(":")[1]), 0);
////      const endDate = new Date(2020, 0, 1, parseInt(end.split(":")[0]), parseInt(end.split(":")[1]), 0);
//      const dateList = [];
//
//      let flag = startDate;
//      let flagStr = flag.getHours() + ":" + (flag.getMinutes() < 10 ? "0"+flag.getMinutes() : flag.getMinutes());
////      let count = 0;
//      while (flagStr != end) {
//        dateList.push(flagStr);
//        flag.setMinutes(flag.getMinutes() + 1);
//        flagStr = flag.getHours() + ":" + (flag.getMinutes() < 10 ? "0"+flag.getMinutes() : flag.getMinutes());
////        count += 1;
////        window.console.log(flagStr);
////        window.console.log(end);
//      }
//      dateList.push(end);
//      dateList.splice(stop[0], stop[1]-stop[0]);
//      return dateList;
////      window.console.log(dateList)
//    },
//    getTimeLineData: function () {
//      const that = this;
//      const targetUrl = "http://web.ifzq.gtimg.cn/appstock/app/hkMinute/query?_var=min_data_hkHSI&code=" + this.nowChosenMarket;
//      this.$axios.get(targetUrl, {
//
//      }).then(function (res) {
//        window.console.log(JSON.parse(res.data.split("=")[1]).data[that.nowChosenMarket]);
//        that.nowChosenMarketLastClose = parseFloat(JSON.parse(res.data.split("=")[1]).data[that.nowChosenMarket].qt[that.nowChosenMarket][4]);
//        that.nowChosenMarketShowDateList = that.nowChosenMarketShowDateDict[that.nowChosenMarket.slice(0, 2)];
//        res = JSON.parse(res.data.split("=")[1]).data[that.nowChosenMarket].data.data;
////        window.console.log(that.nowChosenMarket);
//        const nowChosenParams = that.nowChosenMarketDateParamsDict[that.nowChosenMarket.slice(0, 2)];
//        that.nowChosenMarketDateList = that.createDateList(nowChosenParams[0], nowChosenParams[1], nowChosenParams[2]);
//        res.forEach(
//          (str, index) => {
//              that.nowChosenMarketDataList.push(parseFloat(str.split(" ")[1]));
//          }
//        );
//        that.timeLineMaker();
////        window.console.log(that.nowChosenMarketDataList)
//      })
//    },
//    timeLineMaker: function () {
//      const timeLine = this.$echarts.init(document.getElementById("timeLine"));
//      const that = this;
//      const option = {
//        xAxis: [{
//            type: 'category',
//            data: that.nowChosenMarketDateList,
//            show: false
//          },
//          {
//            type: 'category',
//            data: that.nowChosenMarketShowDateList,
//            position: "bottom",
//            boundaryGap: false,
//            axisTick: {
//              alignWithLabel: true
//            },
//          },
//          {
//            type: 'category',
//            data: [],
//            position: "top",
//            boundaryGap: false,
//            axisTick: {
//              alignWithLabel: true
//            },
//            offset: -100,
//          },
//
//        ],
//        yAxis: [
//          {
//            type: 'value',
//            min: function(value) {
//              let min = Math.abs(value.max - that.nowChosenMarketLastClose) > Math.abs(value.min - that.nowChosenMarketLastClose) ? Math.abs(value.max - that.nowChosenMarketLastClose) + that.nowChosenMarketLastClose : value.min;
//              window.console.log(that.nowChosenMarketLastClose);
//              return min -20;
//            },
//            max: function(value) {
//              let max = Math.abs(value.max - that.nowChosenMarketLastClose) > Math.abs(value.min - that.nowChosenMarketLastClose) ?  value.max : Math.abs(value.min - that.nowChosenMarketLastClose) + that.nowChosenMarketLastClose;
//              return max + 20;
//            },
//            splitLine: {
//              show: false
//            },
//            show: false
//          },
//          {
//            type: "category",
//            data: [that.nowChosenMarketLastClose],
//            splitLine: {
//              show: true
//            },
//            position: "left"
//          }
//        ],
//        series: [
//          {
//            data: that.nowChosenMarketDataList,
//            type: 'line',
//            smooth: true,
//          },
//        ]
//      };
//
//      timeLine.setOption(option);
//    }
  },
  mounted() {
//    this.getTimeLineData();
    this.getTimeLineUrl();
    this.getMarketIndexList(this.nowChosenMarket);
    this.getRankData('ash');
    this.getTipsData("new");
    this.swiper.slideTo(3, 1000, false);
    this.getNewsData();
    this.getResearchData();
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

  .center-holder {
    width: 60vw;
    min-width: 1215px;
    min-height: 100vh;
    /*background-color: green;*/
    position: relative;
    z-index: 1;
    /*top: -7vh;*/
    box-sizing: content-box;
    padding-top: 3vh;
    padding-bottom: 10vh;
    display: flex;
    justify-content: center;
  }

  .center-left {
    width: 70%;
    min-width: 850px;
  }

  .center-right {
    width: 30%;
    min-width: 364px;
    padding-top: 5vh;
    padding-left: 1vw;
    box-sizing: border-box;
  }

  .content-box {
    width: 100%;
    min-height: 400px;
    /*background-color: red;*/
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-top: 5vh;
  }

  .left-box {
    width: 505px;
    height: 100%;
    /*background-color: red;*/
  }

  .right-box {
    width: 345px;
    height: 100%;
    /*background-color: green;*/
  }

  .box-header {
    width: 100%;
    height: 40px;
    /*background-color: pink;*/
    display: flex;
    /*border-bottom: 1px solid #a6a9b6;*/
  }

  .header-title {
    width: 30%;
    height: 100%;
    text-align: left;
    line-height: 40px;
  }

  .header-btn {
    width: 70%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
  }

  .header-btn div {
    /*width: 100px;*/
    /*height: auto;*/
    height: 100%;
    line-height: 40px;
    cursor: pointer;
    font-size: 150%;
    font-weight: 600;
    border-radius: 5px;
    margin-right: 60px;
  }

  .box-center {
    width: 100%;
    height: 85%;
    display: flex;
    margin-top: 5px;
  }

  .echarts-box {
    width: 100%;
    height: 100%;
  }

  .echarts-box img {
    width: 505px;
    height: 301px;
    margin-top: 30px;
    margin-left: -20px;
    /*margin-left: -30%;*/
  }

  .bottom-line {
    box-sizing: content-box;
    /*border-bottom: 7px solid #a6a9b6;*/


  }

  .background-gray {
    background-color: #f7f7fa;
    /*text-decoration: underline;*/
    /*width: 100px;*/
    /*position: relative;*/
  }

  .underline {
    /*width: 100px;*/
    position: relative;
  }

  .underline span {
    display: inline-block;
    width: auto;
    float: left;
  }

  .underline span:before {
    content: "";
    position: absolute;
    bottom: 10px;
    z-index: -1;
    width: 100%;
    /*width: auto;*/
    float: left;
    display: inline-block;
    height: 5px;
    /*background-color: #e73134;*/
    background-color: #f4a01b;
    /*opacity: 0.7;*/
    border-radius: 5px;
  }

  .right-box-header {
    height: 30px;
    line-height: 30px !important;
    text-align: left;
    border-bottom: 1px solid #a6a9b6;
    color: #a6a9b6;
    font-size: 95%;
    text-indent: 5px;
  }

  .more-width {
    width: 120% !important;
  }

  .right-box-center {
    display: flex;
    flex-direction: column;
  }

  .box-center-line {
    width: 100%;
    height: 42px;
    display: flex;
    text-align: left;
    line-height: 42px;
    cursor: pointer;
    text-indent: 5px;
    /*background-color: green;*/
  }

  .box-center-line:hover {
    background-color: #f7f7fa;
    /*background-color: #f49f19;*/
  }

  .line-first {
    width: 120%;

    /*background-color: red;*/
  }

  .line-second, .line-third {
    width: 70%;
  }

  .rank-box {
    justify-content: space-between;
  }

  .right-rank-box {
    width: 48% !important;
  }

  .color-red {
    color: #f44e50;
  }

  .color-green {
    color: #07b360;
  }

  .tip-box {
    width: 100% !important;
  }

  .news-block {
    width: 100%;
    height: 200px;
    margin-top: 1vh;
    /*background-color: red;*/
  }

  .swiper {
    width: 100%;
    height: 100%;
  }

  .swiper-holder {
    width: 100%;
    height: 100%;
  }

  .swiper-box {
    width: 100%;
    height: 100%;
    cursor: pointer;
  }

  .swiper-box p {
    color: white;
    z-index: 3;
    display: inline-block;
    position: relative;
    top: -240px;
    width: 90%;
    text-align: left;
  }

  .swiper-box img {
    z-index: 1;

  }

  .news-list {
    width: 100%;
    /*background-color: red;*/
  }

  .news-line {
    width: 100%;
    height: 45px;
    line-height: 20px;
    text-align: left;
    margin-top: 10px;
    cursor: pointer;
    box-sizing: border-box;
    padding: 5px;
    overflow : hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }

  .news-line:hover {
    background-color: #f7f7fa;
  }

  .footer {
    width: 100%;
    min-width: 1200px;
    height: 150px;
    background-color: #f7f7fa;
    display: flex;
    justify-content: center;
  }

  .footer-content {
    min-width: 1200px;
    height: 100%;
    justify-content: space-between;
    display: flex;
    /*background-color: red;*/
  }

  .footer-box {
    width: 50%;
    height: 100%;
    flex-direction: column;
  }

  .footer-about {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
    margin-top: 40px;
  }

  .footer-btn {
    /*background-color: red;*/
    display: inline-block;
    margin-right: 30px;
    height: 20px;
    line-height: 20px;
    cursor: pointer;
  }

  .footer-line {
    width: 90%;
    height: 50px;
    text-align: left;
    margin-top: -100px;
  }

  .footer-about-right {
    width: 100%;
    height: 100%;
    display: flex;
    /*justify-content: flex-end;*/
    margin-top: 40px;
    flex-direction: column;
  }

  .footer-btn-right {
    width: 100%;
    height: 40px;
    line-height: 40px;
    text-align: right;
  }


  </style>
