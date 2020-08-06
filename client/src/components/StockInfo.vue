<template>
  <div class="page-holder">
    <div class="prime-title-list" v-for="(item, index) in info" v-bind:key="index" v-on:click="showOrHideBlock(item.infoTitle)">
      <div class="prime-title-box">
        {{ item.infoName }}
      </div>
      <div class="secondary-title-box">
        <!--<div :class="'secondary-title-list ' + (showBlockList.indexOf(secondaryItem.fatherTitle) != -1 ? 'show-block' : '')" v-if="showBlockList.indexOf(secondaryItem.fatherTitle) != -1" v-for="(secondaryItem, secondaryIndex) in item.secondaryInfoTitles" v-bind:key="secondaryIndex">-->
        <div :class="'secondary-title-list ' + (showBlockList.indexOf(secondaryItem.fatherTitle) != -1 ? 'show-block' : '')" v-for="(secondaryItem, secondaryIndex) in item.secondaryInfoTitles" v-bind:key="secondaryIndex" v-on:click.stop="jumpToPage(secondaryItem.url)">
          {{ secondaryItem.secondaryInfoName }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StockInfo',
  props: {
    stock: {
      type: String,
//      default: 'hello world'
    },
    exchange: {
      type: String,
    },
  },
  data () {
    return {
      stock: "",
      showBlockList: ["stockInfo", "stockCapital"],
      info: [
        {
          infoTitle: "stockInfo",
          infoName: "公司概况",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "stockIntro",
              secondaryInfoName: "公司简介",
              fatherTitle: "stockInfo",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "stockManager",
              secondaryInfoName: "公司高管",
              fatherTitle: "stockInfo",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "stockIndex",
              secondaryInfoName: "所属指数",
              fatherTitle: "stockInfo",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpXiangGuan/stockid/" + this.stock +".phtml#SSZS"
            },
            {
              secondaryInfoTitle: "stockIPO",
              secondaryInfoName: "IPO文件",
              fatherTitle: "stockInfo",
              url: "http://stock.jrj.com.cn/share," + this.stock +",zgsms.shtml"
            },
          ]
        },
        {
          infoTitle: "stockCapital",
          infoName: "股本信息",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "capitalStructure",
              secondaryInfoName: "股本结构",
              fatherTitle: "stockCapital",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "primeStockHolder",
              secondaryInfoName: "主要股东",
              fatherTitle: "stockCapital",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/" + this.stock +"/displaytype/30.phtml"
            },
            {
              secondaryInfoTitle: "flowStockHolder",
              secondaryInfoName: "流通股东",
              fatherTitle: "stockCapital",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CirculateStockHolder/stockid/" + this.stock +"displaytype/30.phtml"
            },
            {
              secondaryInfoTitle: "fundHoldings",
              secondaryInfoName: "基金持股",
              fatherTitle: "stockCapital",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/" + this.stock +"displaytype/30.phtml"
            },
            {
              secondaryInfoTitle: "managerHoldings",
              secondaryInfoName: "高管持股",
              fatherTitle: "stockCapital",
              url: "http://stock.jrj.com.cn/share," + this.stock +",ggcg.shtml"
            },
            {
              secondaryInfoTitle: "restrictedShareHolders",
              secondaryInfoName: "限售股东",
              fatherTitle: "stockCapital",
              url: "http://stock.jrj.com.cn/share," + this.stock +",xsgd.shtml"
            },
          ]
        },
        {
          infoTitle: "transactionData",
          infoName: "交易数据",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "transactionDetail",
              secondaryInfoName: "成交明细",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "minutePrice",
              secondaryInfoName: "分时价表",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "bigOrder",
              secondaryInfoName: "大单统计",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill.php?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "blockTrading",
              secondaryInfoName: "大宗交易",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "charts",
              secondaryInfoName: "交易榜单",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhbstock/index.phtml?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "financeDetail",
              secondaryInfoName: "融资融券",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrqstock/index.phtml?symbol=" + this.exchange + this.stock
            },
            {
              secondaryInfoTitle: "historicalPrice",
              secondaryInfoName: "历史价格",
              fatherTitle: "transactionData",
              url: "https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price_history.php?symbol=" + this.exchange + this.stock
            },
          ]
        },
        {
          infoTitle: "stockNotice",
          infoName: "公司公告",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "lastNotice",
              secondaryInfoName: "最新公告",
              fatherTitle: "stockNotice",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "summaryNotice",
              secondaryInfoName: "年度公告",
              fatherTitle: "stockNotice",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/" + this.stock +"/page_type/ndbg.phtml"
            },
          ]
        },
        {
          infoTitle: "financeAnalysis",
          infoName: "财务分析",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "holdersMeeting",
              secondaryInfoName: "股东大会",
              fatherTitle: "financeAnalysis",
              url: "http://money.finance.sina.com.cn/corp/go.php/vGP_StockHolderMeeting/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "incomeStructure",
              secondaryInfoName: "收入构成",
              fatherTitle: "financeAnalysis",
              url: "http://stockpage.10jqka.com.cn/" + this.stock +"/operate/#analysis"
            },
            {
              secondaryInfoTitle: "bigDeal",
              secondaryInfoName: "重大事项",
              fatherTitle: "financeAnalysis",
              url: "https://q.stock.sohu.com/cn/" + this.stock +"/bw.shtml"
            },
            {
              secondaryInfoTitle: "shareDetail",
              secondaryInfoName: "分红配送",
              fatherTitle: "financeAnalysis",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "additional",
              secondaryInfoName: "增发一览",
              fatherTitle: "financeAnalysis",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_AddStock/stockid/" + this.stock +".phtml"
            },
            {
              secondaryInfoTitle: "internalTransaction",
              secondaryInfoName: "内部交易",
              fatherTitle: "financeAnalysis",
              url: "http://data.eastmoney.com/executive/gdzjc/" + this.stock + ".html"
            },
            {
              secondaryInfoTitle: "IRRecover",
              secondaryInfoName: "IR活动记录",
              fatherTitle: "financeAnalysis",
              url: "http://sns.sseinfo.com/search.do?keyword=" + this.stock
            },
          ]
        },
        {
          infoTitle: "baseData",
          infoName: "基本数据",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "balanceSheet",
              secondaryInfoName: "资产负债表",
              fatherTitle: "baseData",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/" + this.stock + "/ctrl/part/displaytype/4.phtml"
            },
            {
              secondaryInfoTitle: "cashFlow",
              secondaryInfoName: "现金流量表",
              fatherTitle: "baseData",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/" + this.stock + "/ctrl/part/displaytype/4.phtml"
            },
            {
              secondaryInfoTitle: "incomeStatement",
              secondaryInfoName: "利润表",
              fatherTitle: "baseData",
              url: "https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/" + this.stock + "/ctrl/part/displaytype/4.phtml"
            },
          ]
        },
        {
          infoTitle: "researchAndAnalysis",
          infoName: "研究分析",
          secondaryInfoTitles: [
            {
              secondaryInfoTitle: "DuPondDetail",
              secondaryInfoName: "杜邦分析",
              fatherTitle: "researchAndAnalysis",
              url: "http://quotes.money.163.com/f10/dbfx_" + this.stock + ".html"
            },
            {
              secondaryInfoTitle: "analysisReport",
              secondaryInfoName: "研究报告",
              fatherTitle: "researchAndAnalysis",
              url: "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?t1=2&symbol=" + this.stock
            },
            {
              secondaryInfoTitle: "techAnalysis",
              secondaryInfoName: "财务指标",
              fatherTitle: "researchAndAnalysis",
              url: "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/" + this.stock + "/displaytype/4.phtml"
            },
          ]
        },
      ]
    }
  },
  methods: {
//    getInfo: function () {
//      const that = this;
//      const targetUrl = "/api/stockInfo?stock=000651";
//      this.$axios.get(targetUrl, {}).then(function (res){
//        window.console.log(res);
//      })
//    }
    jumpToPage: function (url) {
      window.open(url,'_blank')
    },
    showOrHideBlock: function (event) {
      window.console.log(event);
      if (this.showBlockList.indexOf(event) == -1) {
        this.showBlockList.push(event)
      }
      else {
        this.showBlockList.splice(this.showBlockList.indexOf(event))
      }
    }
  },
  mounted() {
//    this.getInfo();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .page-holder {
    width: 100%;
    min-height: 100vh;
    /*background-color: red;*/
    text-align: left;
  }

  .prime-title-list {
    width: 50%;
    text-align: center;
  }

  .prime-title-box {
    height: 50px;
    line-height: 50px;
    font-size: 90%;
    cursor: pointer;
    background-color: white;
    z-index: 2;
    position: relative;
    user-select: none;
  }

  .prime-title-box:hover {
    background-color: #f7f7fa;
  }

  .secondary-title-box {
    z-index: 1;
    position: relative;
  }

  .secondary-title-list {
    /*text-indent: 10px;*/
    transition: height 0.5s, opacity 0.5s;
    -moz-transition: height 0.5s, opacity 0.5s;
    -webkit-transition: height 0.5s, opacity 0.5s;

    height: 0;
    line-height: 30px;
    font-size: 80%;
    cursor: pointer;
    opacity: 0;
    color: white;
    /*z-index: -1;*/
    user-select: none;
  }

  .secondary-title-list:hover {
    background-color: #f7f7fa;
  }

  .show-block {
    height: 30px;
    opacity: 1;
    color: #a6a9b6;
  }
</style>
