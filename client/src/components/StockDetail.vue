<template>
  <div class="root" v-wechat-title="name+'('+stock+')'">
    <TopNavbar></TopNavbar>
    <!--<div class="page-holder">-->

      <div class="center-holder">
        <div class="center-left">
          <div class="center-left-left">
            <StockInfo v-bind:exchange="exchange" v-bind:stock="stock"></StockInfo>
          </div>
          <div class="center-left-right">

            <div class="center-header">
              <div class="center-header-left">
                <div class="center-header-left-first">
                  <div class="left-line stock-line">
                    {{ stock }}
                  </div>
                  <div class="right-line name-line">
                    {{ name }}
                  </div>
                </div>
                <div class="center-header-left-second">
                  <div class="left-line status-line">
                    {{ marketStatus }}
                  </div>
                  <div class="right-line date-line">
                    {{ dateForUser }}
                  </div>
                </div>
                <div class="center-header-left-third">
                  <div :class="'price-line ' + (change >= 0 ? 'color-red' : 'color-green')">
                    {{ latestPrice }}
                  </div>
                  <div class="growth-line">
                    <div :class="'change-line ' + (change >= 0 ? 'color-red' : 'color-green')">
                      {{ change >= 0 ? '+' : '' }}{{ change }}
                    </div>
                    <div :class="'change-line ' + (change >= 0 ? 'color-red' : 'color-green')">
                      {{ change >= 0 ? '+' : '' }}{{ changeRate }}%
                    </div>
                  </div>
                </div>
              </div>
              <div class="center-header-right">
                <div class="data-box" v-for="(item, index) in stockDataList" v-bind:key="index">
                  {{ item }}
                </div>
              </div>
            </div>

            <div class="operation-bar">
              <div class="operation-box" v-on:click="addToOperationalShares" v-if="!isAdded && isIndex !== 'ZS'">
                +自选
              </div>
              <div class="" v-else-if="(!isAdded && isIndex === 'ZS' )">

              </div>
              <div class="" v-else-if="exchange==='us'">

              </div>
              <div class="operation-box added" v-else>
                ✔已添加
              </div>
            </div>

            <div class="content-box">
              <div class="box-header">
                <div class="header-title">
                  <h2>交易数据</h2>
                </div>
                <div class="header-btn">
                  <div :class="(nowChosenType == 'time' ? 'underline' : '')" @click="changeCanvas('time')">
                    <span>分时</span>
                  </div>
                  <div :class="(nowChosenType == 'k_day' ? 'underline' : '')" @click="changeCanvas('k_day')">
                    <span>日K</span>
                  </div>
                  <div :class="(nowChosenType == 'k_week' ? 'underline' : '')" @click="changeCanvas('k_week')">
                    <span>周K</span>
                  </div>
                  <div :class="(nowChosenType == 'k_month' ? 'underline' : '')" @click="changeCanvas('k_month')">
                    <span>月K</span>
                  </div>
                  <!--<div :class="(nowChosenType == 'k_all' ? 'background-gray' : '')" @click="changeCanvas('k_all')">-->
                    <!--全部-->
                  <!--</div>-->
                </div>
              </div>
              <div class="box-center rank-box">
                <div class="canvas" v-if="nowChosenType == 'time'">
                  <TimeLine v-bind:isIndex="isIndex" v-bind:fullStock="exchange+'-'+stock"></TimeLine>
                </div>
                <div  class="canvas" v-if="nowChosenType != 'time'" :key="kLineKey">
                  <KLine v-bind:isIndex="isIndex" v-bind:lineType="nowChosenType" v-bind:fullStock="exchange+'-'+stock"></KLine>
                </div>
                <!--<div  class="canvas" v-if="nowChosenType == 'k_week'">-->
                  <!--<KLine v-bind:isIndex="isIndex" v-bind:lineType="nowChosenType" v-bind:fullStock="exchange+'-'+stock"></KLine>-->
                <!--</div>-->
                <!--<div  class="canvas" v-if="nowChosenType == 'k_month'">-->
                  <!--<KLine v-bind:isIndex="isIndex" v-bind:lineType="nowChosenType" v-bind:fullStock="exchange+'-'+stock"></KLine>-->
                <!--</div>-->
              </div>
            </div>
            <Comments v-bind:stock="stock" v-bind:name="name" v-bind:exchange="exchange" v-bind:isIndex="isIndex"></Comments>
          </div>
        </div>
        <div class="center-right">
          <Radar v-bind:stock="stock"></Radar>
          <OperationalShares ref="refresh" v-bind:stock="stock"></OperationalShares>
        </div>
      </div>
      <Footer></Footer>
    <!--</div>-->
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue"
import TimeLine from "./TimeLine.vue"
import KLine from "./KLine.vue"
import StockInfo from "./StockInfo.vue"
import Comments from "./Comments.vue"
import Footer from "./Footer.vue"
import Radar from "./Radar.vue"
import OperationalShares from "./OperationalShares.vue"
export default {
  name: 'SearchAssociation',
  components: {
//    SearchAssociation,
    TopNavbar,
    TimeLine,
    KLine,
    StockInfo,
    Comments,
    Footer,
    Radar,
    OperationalShares
  },
  data () {
    return {
      stock: this.$route.params.stock,
      isIndex: this.$route.params.type,
      exchange: this.$route.params.exchange,
      name: "",
      marketStatus: "",
      dateForUser: "",
      nowPrice: "",
      change: "",
      changeRate: "",
      high: "",
      low: "",
      open: "",
      close: "",
      latestPrice: "",
      per: "",
      amplitude: "",
      currencyValue: "",
      totalValue: "",
      volume: "",
      turnoverRate: "",
      pbr: "",
      stockDataList: [],
      nowChosenType: "time",
      kLineKey: 1,
      isAdded: false
    }
  },
  methods: {
    changeAddButton: function (e) {
      this.isAdded = e
    },
    addToOperationalShares: function () {
      const that = this;
      const userCode = this.$cookie.get("userCode");
      if (this.exchange == "us" || this.exchange == "hk") {
        alert("暂不支持美、港股自选，敬请期待！")
        return 0
      }

      const data = this.qs.stringify({
        "userCode": userCode,
        "stockCode": this.stock,
        "exchange": this.exchange,
        "stockName": this.name
      })
      this.$axios.post("/api/optionalShares", data).then(function (res) {
        if (res.data === 200) {
          that.$refs.refresh.getOperationalShares();
        }
      });
    },
    changeCanvas: function (type) {
      this.nowChosenType = type;
      this.kLineKey = (this.kLineKey == 1 ? 2 : 1);
//      window.console.log(type);
//      if (type != "time") {
//        this.$destroy('TimeLine')
//      }
//      this.kLineKey = new Date();
//      this.$refs.changeCanvasType.initCanvas()
    },
    getStockMainData: function () {
      const that = this;
      this.rawStock = this.stock.split(".")[0].toUpperCase();
      this.stock = this.stock.toUpperCase();
      this.dateForUser = (new Date()).toLocaleString();
//      let urlDict = {
//        "sh": "https://www.laohu8.com/proxy/stock/astock/stock_info/detail/" + this.stock,
//        "sz": "https://www.laohu8.com/proxy/stock/astock/stock_info/detail/" + this.stock,
//        "hk": "https://www.laohu8.com/proxy/stock/hkstock/stock_info/detail/" + this.stock,
//        "us": "https://www.laohu8.com/proxy/stock/stock_info/detail/" + this.stock,
//        "uszs": "https://www.laohu8.com/proxy/stock/stock_info/detail/." + this.stock
//      };
      let urlDict = {
        "sh": "https://www.laohu8.com/proxy/stock/astock/stock_info/detail/" + this.stock,
        "sz": "https://www.laohu8.com/proxy/stock/astock/stock_info/detail/" + this.stock,
        "hk": "https://www.laohu8.com/proxy/stock/hkstock/stock_info/detail/" + this.stock,
        "us": "https://www.laohu8.com/proxy/stock/stock_info/detail/" + this.rawStock,
        "uszs": "https://www.laohu8.com/proxy/stock/stock_info/detail/." + this.stock
      };

      this.setData = function (that, res) {
        that.name = res.data.items[0].nameCN;
        that.latestPrice = res.data.items[0].latestPrice;
        that.change = res.data.items[0].change;
        that.changeRate = res.data.items[0].changeRate*100 ? (res.data.items[0].changeRate*100).toFixed(2) : (res.data.items[0].change / res.data.items[0].latestPrice * 100).toFixed(2);
        that.high = res.data.items[0].high;
        that.low = res.data.items[0].low;
        that.volume = res.data.items[0].volume;
        that.amount = res.data.items[0].amount;
        that.open = res.data.items[0].open;
        that.preClose = res.data.items[0].preClose;
        that.amplitude = res.data.items[0].amplitude;
        that.turnoverRate = res.data.items[0].turnoverRate;
        that.marketValue = res.data.items[0].marketValue;
        that.floatMarketCap = res.data.items[0].floatMarketCap;
        that.shares = res.data.items[0].shares;
        that.floatShares = res.data.items[0].floatShares;
        that.week52High = res.data.items[0].week52High ? res.data.items[0].week52High : "--";
        that.week52Low = res.data.items[0].week52Low ? res.data.items[0].week52Low : "--";
        that.peRate = res.data.items[0].peRate ? res.data.items[0].peRate : 0;
//        that.peRate = 0;
        that.pbRate = res.data.items[0].pbRate;
        that.dividePrice = res.data.items[0].dividePrice ? res.data.items[0].dividePrice : "--";
        that.divideRate = res.data.items[0].divideRate ? res.data.items[0].divideRate : "--";
        that.roa = res.data.items[0].roa;
        that.roe = res.data.items[0].roe;
        that.eps = res.data.items[0].eps;
        that.marketStatus = res.data.items[0].marketStatus;

        if (that.exchange == "sh" || that.exchange == "sz") {
//          window.console.log(that.exchange)
          that.stockDataList = [
            "最高:"+that.high, "最低:"+that.low, "成交量:"+(that.volume/10000).toFixed(0)+"万", "成交额:"+(that.amount>100000000 ? (that.amount/100000000).toFixed(2)+"亿" : ((that.amount/10000).toFixed(2)+"万")), "今开:"+that.open, "昨收:"+that.preClose,
            "日振幅:"+(that.amplitude*100).toFixed(2)+"%", "换手率:"+(that.turnoverRate*100).toFixed(2)+"%", "总市值:"+(that.marketValue/100000000).toFixed(0)+"亿", "流通市值:"+(that.floatMarketCap/100000000).toFixed(0)+"亿",
            "市盈率:"+(that.peRate).toFixed(2), "市净率:"+that.pbRate, "ROE:"+that.roe, "每股收益:"+that.eps,

          ];
        }
        else {
          that.stockDataList = [
            "最高:"+that.high, "最低:"+that.low, "成交量:"+(that.volume/10000).toFixed(0)+"万", "成交额:"+(that.amount>100000000 ? (that.amount/100000000).toFixed(2)+"亿" : ((that.amount/10000).toFixed(2)+"万")), "今开:"+that.open, "昨收:"+that.preClose,
            "日振幅:"+(that.amplitude*100).toFixed(2)+"%",
            "总股本:"+(that.shares/100000000).toFixed(2)+"亿", "流通股本:"+(that.floatShares/100000000).toFixed(2)+"亿", "每股收益:"+that.eps,

          ];
        }
      };
//      window.console.log(1)
      this.$axios.get(urlDict[this.exchange], {}).then(function (res){
//        window.console.log(res);
        const that2 = that;
        if (res.data.items[0].high == 0) {
          that.$axios.get(urlDict[that.exchange+"zs"], {}).then(function (res){
            that2.setData(that2, res)
          })
        }
        else {
          that.setData(that, res)
        }

      })




//        window.console.log(marketStatus);
//        window.console.log(stockStatus);

//        window.console.log(that.change);


    }
  },
  mounted() {
//    window.console.log(this.isIndex)
//    window.console.log(this.$route.params)
//    window.console.log(this.stock)
//    window.console.log(555)
    this.getStockMainData();
    this.timer = setInterval(this.getStockMainData, 60000);
    this.$once('hook:beforeDestroy', () => {
      clearInterval(this.timer);
    })
//    window.console.log(this.exchange)
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

  .center-holder {
    width: 60vw;
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
    min-width: 1215px;
  }

  .center-left {
    width: 70%;
    min-width: 850px;
    display: flex;
  }

  .center-right {
    width: 30%;
    min-width: 364px;
    /*padding-top: 5vh;*/
    padding-left: 1vw;
    box-sizing: border-box;
    /*background-color: pink;*/
  }

  .center-left-left {
    width: 150px;
    min-height: 100vh;
    /*background-color: green;*/
  }

  .center-left-right {
    width: 700px;
    min-height: 100vh;
    /*background-color: red;*/
  }

  .center-header {
    width: 100%;
    height: 150px;
    /*background-color: red;*/
    display: flex;
  }

  .center-header-left {
    width: 250px;
    height: 120px;
    background-color: white;
  }

  .center-header-left-first {
    width: 100%;
    height: 35px;
    /*background-color: yellow;*/
    display: flex;
    justify-content: space-between;
  }

  .stock-line {
    font-size: 130%;
    line-height: 35px;
    font-weight: 600;
  }

  .name-line {
    font-size: 130%;
    line-height: 35px;
    font-weight: 600;
    overflow: hidden;
  }

  .center-header-left-second {
    width: 100%;
    height: 35px;
    /*background-color: yellow;*/
    display: flex;
    justify-content: space-between;
  }

  .status-line {
    font-size: 100%;
    line-height: 35px;
    color: #a6a9b6;
  }

  .date-line {
    font-size: 100%;
    line-height: 35px;
    color: #a6a9b6;
  }

  .center-header-left-third {
    width: 100%;
    height: 50px;
    /*background-color: yellow;*/
    display: flex;
    justify-content: space-between;
  }

  .price-line {
    font-size: 280%;
    line-height: 50px;
  }

  .growth-line {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .change-line {
    /*background-color: red;*/
    line-height: 25px;
    text-align: right;
  }

  .color-green {
    color: #07b360;
  }

  .color-red {
    color: #f44e50;
  }

  .center-header-right {
    height: 120px;
    width: 400px;
    /*background-color: yellow;*/
    margin-left: 50px;
    display: flex;
    flex-wrap: wrap;
    align-content: space-between;
    justify-content: space-between;
  }

  .data-box {
    min-width: 120px;
    max-width: 300px;
    height: 25px;
    line-height: 25px;
    text-align: left;
    font-size: 92%;
    /*margin-left: 10px;*/
  }

  .content-box {
    width: 100%;
    min-height: 400px;
    /*background-color: red;*/
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    /*margin-top: 5vh;*/
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
    width: 20%;
    height: 100%;
    text-align: left;
    line-height: 40px;
    /*border-bottom: 1px solid #f7f7fa;*/
  }

  .header-btn {
    width: 80%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
    border-bottom: 1px solid #f7f7fa;
  }

  .header-btn div {
    width: 80px;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
  }

  .box-center {
    width: 100%;
    height: 85%;
    display: flex;
    margin-top: 5px;
  }

  .background-gray {
    background-color: #f7f7fa;
  }

  .underline {
    /*width: 100px;*/
    color: #06c !important;
    border-bottom: 2px solid #0084ff;
  }

  /*.underline span {*/
    /*display: inline-block;*/
    /*width: auto;*/
    /*float: left;*/
  /*}*/

  /*.underline span:before {*/
    /*content: "";*/
    /*position: absolute;*/
    /*bottom: 10px;*/
    /*z-index: -1;*/
    /*width: 100%;*/
    /*!*width: auto;*!*/
    /*float: left;*/
    /*display: inline-block;*/
    /*height: 5px;*/
    /*!*background-color: #e73134;*!*/
    /*background-color: #f4a01b;*/
    /*!*opacity: 0.7;*!*/
    /*border-radius: 5px;*/
  /*}*/

  .operation-bar {
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: start;
    /*background-color: #0084ff;*/
    /*margin-top: 5vh;*/
  }

  .operation-box {
    width: 70px;
    height: 30px;
    background-color: #0084ff;
    line-height: 30px;
    /*padding-left: 5px;*/
    cursor: pointer;
    /*font-weight: 600;*/
    color: white;
    text-align: center;
    border-radius: 15px;
    font-size: 95%;
  }

  .added {
    width: 80px !important;
    font-size: 90% !important;
  }

</style>



// WEBPACK FOOTER //
// src/components/StockDetail.vue
