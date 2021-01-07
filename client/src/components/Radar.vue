<template>
  <div class="canvas-holder">
    <div class="radar-header">
      <div class="header-text">
        财报雷达
      </div>
      <div class="header-bar">
        <div :class="'year-btn ' + (chosenYearIndex === index ? 'chosen-year' : '') " v-for="(item, index) in yearList" v-bind:key="index" v-on:click="chosenYear(index)">
          {{ item }}
        </div>
      </div>
    </div>
    <div class="container" v-show="startToShow">
      <div id="radarCanvas">

      </div>
      <div class="comment-box" id="radarContent" v-if="startToShow">
        <div class="comment-line">
          <div class="comment-title">
            现金流
          </div>
          <div class="comment-text">
            <p><span :class="'level' + cashToAssetsRatioLevel" v-bind:title="cashToAssetsRatioMessage">{{cashToAssetsRatioComment}}</span> <span :class="'level' + cashFlowRatioLevel" v-bind:title="cashFlowRatioMessage">{{cashFlowRatioComment}}</span> <span :class="'level' + accountsReceivTurnOverLevel" v-bind:title="accountsReceivTurnOverMessage">{{accountsReceivTurnOverComment}}</span></p>
          </div>
        </div>
        <div class="comment-line">
          <div class="comment-title">
            盈利能力
          </div>
          <div class="comment-text">
            <p><span :class="'level' + GrossProfitMarginLevel" v-bind:title="GrossProfitMarginMessage">{{GrossProfitMarginComment}}</span> <span :class="'level' + costRateLevel" v-bind:title="costRateMessage">{{costRateComment}}</span> <span :class="'level' + incomeRateLevel" v-bind:title="incomeRateMessage">{{incomeRateComment}}</span> <span :class="'level' + roeLevel" v-bind:title="roeMessage">{{roeComment}}</span> <span :class="'level' + basicEPSLevel" v-bind:title="basicEPSMessage">{{basicEPSComment}}</span></p>
          </div>
        </div>
        <div class="comment-line">
          <div class="comment-title">
            运营能力
          </div>
          <div class="comment-text">
            <p><span :class="'level' + totalAssetsTurnOverLevel" v-bind:title="totalAssetsTurnOverMessage">{{totalAssetsTurnOverComment}}</span> <span :class="'level' + inventoriesTurnOverLevel" v-bind:title="inventoriesTurnOverMessage">{{inventoriesTurnOverComment}}</span> <span :class="'level' + businessDaysLevel" v-bind:title="businessDaysMessage">{{businessDaysComment}}</span><span :class="'level' + operationGrowthRatioLevel" v-bind:title="operationGrowthRatioMessage">{{ operationGrowthRatioComment }}</span></p>
          </div>
        </div>
        <div class="comment-line">
          <div class="comment-title">
            杠杆结构
          </div>
          <div class="comment-text">
            <p><span :class="'level' + debtToAssetsRatioLevel" v-bind:title="debtToAssetsRatioMessage">{{debtToAssetsRatioComment}}</span> <span :class="'level' + longTermAssetsToFixAssetsRatioLevel" v-bind:title="longTermAssetsToFixAssetsRatioMessage">{{longTermAssetsToFixAssetsRatioComment}}</span></p>
          </div>
        </div>
        <div class="comment-line">
          <div class="comment-title">
            偿债能力
          </div>
          <div class="comment-text">
            <p><span :class="'level' + quickRatioLevel" v-bind:title="quickRatioMessage">{{quickRatioComment}}</span></p>
          </div>
        </div>
      </div>
    </div>
    <div class="radar-shadow" id="radarShadow" v-show="!startToShow">
      <div>
        敬请期待
      </div>
    </div>


  </div>
</template>

<script>
export default {
  name: 'Radar',
  components: {

  },
  props: {
    stock: {
      type: String,
    },
  },
  data () {
    return {
      lastScore: 0,
      cashScore: 0,
      deptScore: 0,
      businessScore: 0,
      profitScore: 0,
      emScore: 0,
      yearList: ["2015","2016","2017","2018","2019",],
      chosenYearIndex: 4,
      cashComment: "",
      quickRatioComment: "",
      cashToAssetsRatioLevelMessage: "",
      cashToAssetsRatioLevel: 0,
      cashFlowRatioMessage: "",
      cashFlowRatioComment: "",
      cashFlowRatioLevel: 0,
      accountsReceivTurnOverMessage: "",
      isShowRadar: false,
      startToShow: false
    }
  },

  methods: {
    getFinancialStatement: function () {
      const that = this;
      const targetUrl = "/api/financial?symbol=" + this.stock + "&date=" + this.yearList[this.chosenYearIndex]+"1231";
      this.$axios.get(targetUrl, {}).then(function (res){
        if (res.data === 404) {
          that.startToShow = false;
          // document.getElementById("radarCanvas").style.display = "none"
          // document.getElementById("radarShadow").style.display = "block"
          // document.getElementById("radarContent").style.display = "none"
        }
        else {
          // document.getElementById("radarCanvas").style.display = "block"
          // document.getElementById("radarShadow").style.display = "none"
          // document.getElementById("radarContent").style.display = "block"
          const data = res.data;
          
          that.sumScore = data.roic_score / 4 + data.roa_score / 4 + data.em_score_ / 10 + data.em_score / 10 + data.cash_flow_score * 3 / 10;
          
          that.cashScore = data.cash_score.toFixed(0);
          that.profitScore = data.roa_score.toFixed(0);
          that.businessScore = data.roe_score.toFixed(0);
          that.deptScore = data.pay_score.toFixed(0);
          that.emScore = data.em_score.toFixed(0);
          that.cashToAssetsRatio = data.cash_to_assets_ratio;
          that.cashToAssetsRatioMessage = "现金与约当现金比率:" + (data.cash_to_assets_ratio).toFixed(0) + "%";
          if (that.cashToAssetsRatio >= 0.25) {
            that.cashToAssetsRatioComment = "现金超多!"
            that.cashToAssetsRatioLevel = 1
          }
          else if (that.cashToAssetsRatio < 0.25 && that.cashToAssetsRatio >= 0.2) {
            that.cashToAssetsRatioComment = "现金还不错."
            that.cashToAssetsRatioLevel = 2
          }
          else if (that.cashToAssetsRatio < 0.2 && that.cashToAssetsRatio >= 0.15) {
            that.cashToAssetsRatioComment = "现金OK."
            that.cashToAssetsRatioLevel = 3
          }
          else if (that.cashToAssetsRatio < 0.15 && that.cashToAssetsRatio >= 0.1) {
            that.cashToAssetsRatioComment = "有一定现金."
            that.cashToAssetsRatioLevel = 4
          }
          else {
            that.cashToAssetsRatioComment = "现金状况堪忧."
            that.cashToAssetsRatioLevel = 5
          }
          
          that.operationGrowthRatio = data.operation_growth_ratio ? data.operation_growth_ratio : 0;
          that.operationGrowthRatioMessage = "近三年平均营业收入增长率: " + (that.operationGrowthRatio).toFixed(2) + "%"
          window.console.log(that.operationGrowthRatio)
          if (that.operationGrowthRatio >= 30) {
            that.operationGrowthRatioComment = "营业成长非常好!"
            that.operationGrowthRatioLevel = 1
          }
          else if (that.operationGrowthRatio < 30 && that.operationGrowthRatio >= 20) {
            that.operationGrowthRatioComment = "营业成长还可以."
            that.operationGrowthRatioLevel = 2
          }
          else if (that.operationGrowthRatio < 20 && that.operationGrowthRatio >= 10) {
            that.operationGrowthRatioComment = "营业成长一般."
            that.operationGrowthRatioLevel = 3
          }
          else if (that.operationGrowthRatio < 10 && that.operationGrowthRatio >= 0) {
            that.operationGrowthRatioComment = "营业成长令人担忧."
            that.operationGrowthRatioLevel = 3
          }
          else {
            that.operationGrowthRatioComment = "营业收入逆增长."
            that.operationGrowthRatioLevel = 6
          }
            
          
          if (data.operation_cash_flow_ratio > 1 && data.cash_adequancy_ratio > 1 && data.crir > 0.1) {
            that.cashFlowRatioMessage = "100/100/10.";
            that.cashFlowRatioComment = "现金流状况很好!";
            that.cashFlowRatioLevel = 1
          }
          else if (data.operation_cash_flow_ratio < 0 && data.cash_adequancy_ratio < 0 && data.crir < 0) {
            that.cashFlowRatioMessage = "0/0/0.";
            that.cashFlowRatioComment = "现金流状况糟糕.";
            that.cashFlowRatioLevel = 3
          }
          else {
            that.cashFlowRatioMessage = "0~100/0~100/0~10.";
            that.cashFlowRatioComment = "现金流状况一般.";
            that.cashFlowRatioLevel = 2
          }
          
          that.accountsReceivTurnOver = data.accounts_receiv_turnover ? data.accounts_receiv_turnover : 0;
          that.accountsReceivTurnOverMessage = "应收账款周转天数:" + that.accountsReceivTurnOver.toFixed(0) + "天";
          if (that.accountsReceivTurnOver < 15) {
            that.accountsReceivTurnOverComment = "收款速度很快!"
            that.accountsReceivTurnOverLevel = 1
          }
          else if (that.accountsReceivTurnOver >= 15 && that.accountsReceivTurnOver < 60) {
            that.accountsReceivTurnOverComment = "收款速度还可以."
            that.accountsReceivTurnOverLevel = 2
          }
          else if (that.accountsReceivTurnOver >= 60 && that.accountsReceivTurnOver < 100) {
            that.accountsReceivTurnOverComment = "收款速度一般."
            that.accountsReceivTurnOverLevel = 3
          }
          else {
            that.accountsReceivTurnOverComment = "收款速度很慢."
            that.accountsReceivTurnOverLevel = 4
          }

          that.GrossProfitMargin = data.gross_profit_margin;
          that.GrossProfitMarginMessage = "毛利率:" + (data.gross_profit_margin).toFixed(0) + "%";
          
          if (data.gross_profit_margin > 0.7) {
            that.GrossProfitMarginComment = "一本万利!";
            that.GrossProfitMarginLevel = 1
          }
          else if (data.gross_profit_margin > 0.6 && data.gross_profit_margin <= 0.7) {
            that.GrossProfitMarginComment = "毛利高到流口水.";
            that.GrossProfitMarginLevel = 2
          }
          else if (data.gross_profit_margin > 0.5 && data.gross_profit_margin <= 0.6) {
            that.GrossProfitMarginComment = "毛利还不错.";
            that.GrossProfitMarginLevel = 3
          }
          else if (data.gross_profit_margin > 0.3 && data.gross_profit_margin <= 0.5) {
            that.GrossProfitMarginComment = "毛利还可以.";
            that.GrossProfitMarginLevel = 4
          }
          else if (data.gross_profit_margin > 0.2 && data.gross_profit_margin <= 0.3) {
            that.GrossProfitMarginComment = "毛利一般.";
            that.GrossProfitMarginLevel = 5
          }
          else {
            that.GrossProfitMarginComment = "毛利不太行.";
            that.GrossProfitMarginLevel = 6
          }

          that.costRate = data.cost_rate.toFixed(2);
          that.costRateMessage = "三费合计";
          if (data.cost_rate > 0.05) {
            that.costRateComment = "费用率" + that.costRate + "个点."
            that.costRateLevel = 0
          }
          else {
            that.costRateComment = "费用率" + that.costRate + "个点.很会省钱!"
            that.costRateLevel = 1
          }

          that.incomeRate = data.income_rate;
          that.incomeRateMessage = "净利率:" + (data.income_rate).toFixed(0) + "%";
          if (data.income_rate > 0.3) {
            that.incomeRateComment = "刨去成本也很赚钱!"
            that.incomeRateLevel = 1
          }
          else if (data.income_rate > 0.25 && data.income_rate <= 0.3) {
            that.incomeRateComment = "税后利润还不错."
            that.incomeRateLevel = 2
          }
          else if (data.income_rate > 0.20 && data.income_rate <= 0.25) {
            that.incomeRateComment = "税后利润还可以."
            that.incomeRateLevel = 3
          }
          else if (data.income_rate > 0.15 && data.income_rate <= 0.20) {
            that.incomeRateComment = "税后利润OK."
            that.incomeRateLevel = 4
          }else if (data.income_rate > 0.10 && data.income_rate <= 0.15) {
            that.incomeRateComment = "税后利润一般."
            that.incomeRateLevel = 5
          }
          else {
            that.incomeRateComment = "税后利润不太行."
            that.incomeRateLevel = 6
          }
          
          that.roe = data.roe;
          that.roeMessage = "ROE:" + (data.roe).toFixed(0) + "%";
          if (data.roe > 0.4) {
            that.roeComment = "回报率突破天际!"
            that.roeLevel = 1
          }
          else if (data.roe <= 0.4 && data.roe > 0.3) {
            that.roeComment = "很牛逼的回报率."
            that.roeLevel = 2
          }
          else if (data.roe <= 0.3 && data.roe > 0.2) {
            that.roeComment = "回报率相当优秀."
            that.roeLevel = 3
          }
          else if (data.roe <= 0.2 && data.roe > 0.1) {
            that.roeComment = "回报率很不错."
            that.roeLevel = 4
          }
          else if (data.roe <= 0.1 && data.roe > 0.05) {
            that.roeComment = "回报还可以."
            that.roeLevel = 5
          }
          else {
            that.roeComment = "回报率一般."
            that.roeLevel = 6
          }

          that.basicEPS = data.basic_eps;
          that.basicEPSComment = "每股收益为" + that.basicEPS + "元."
          that.basicEPSMessage = "基本每股收益"
          that.basicEPSLevel = 0

          that.totalAssetsTurnOver = data.total_assets_turnover;
          that.totalAssetsTurnOverMessage = "总资产周转率: " + (data.total_assets_turnover*100).toFixed(0) + "%";
          if (data.total_assets_turnover < 0.8) {
            that.totalAssetsTurnOverComment = "周转很慢."
            that.totalAssetsTurnOverLevel = 4
          }
          else if (data.total_assets_turnover > 0.8 && data.total_assets_turnover < 1.1) {
            that.totalAssetsTurnOverComment = "周转速度一般."
            that.totalAssetsTurnOverLevel = 3
          }
          else if (data.total_assets_turnover > 1.1 && data.total_assets_turnover < 1.3) {
            that.totalAssetsTurnOverComment = "周转速度还可以."
            that.totalAssetsTurnOverLevel = 2
          }
          else if (data.total_assets_turnover > 1.3 && data.total_assets_turnover < 1.5) {
            that.totalAssetsTurnOverComment = "周转速度很快!"
            that.totalAssetsTurnOverLevel = 1
          }

          that.inventoriesTurnOver = data.inventories_turnover;
          that.inventoriesTurnOverMessage = "存货周转天数: " + (data.inventories_turnover).toFixed(0) + "天";
          if (data.inventories_turnover < 30) {
            that.inventoriesTurnOverComment = "货卖得很好!"
            that.inventoriesTurnOverLevel = 1
          }
          else if (data.inventories_turnover >= 30 && data.inventories_turnover < 60) {
            that.inventoriesTurnOverComment = "货卖得还不错."
            that.inventoriesTurnOverLevel = 2
          }
          else if (data.inventories_turnover >= 60 && data.inventories_turnover < 90) {
            that.inventoriesTurnOverComment = "货卖得还可以."
            that.inventoriesTurnOverLevel = 3
          }
          else if (data.inventories_turnover >= 90 && data.inventories_turnover < 120) {
            that.inventoriesTurnOverComment = "货卖得OK."
            that.inventoriesTurnOverLevel = 4
          }
          else if (data.inventories_turnover >= 120 && data.inventories_turnover < 150) {
            that.inventoriesTurnOverComment = "货卖得一般."
            that.inventoriesTurnOverLevel = 5
          }
          else {
            that.inventoriesTurnOverComment = "货卖得不行.";
            that.inventoriesTurnOverLevel = 6
          }

          that.businessDays = (data.business_days ? data.business_days : 0).toFixed(0);
          that.businessDaysComment = "做一轮生意要" + that.businessDays + "天."
          that.businessDaysMessage = "完整生意周期"
          that.businessDaysLevel = 0

          that.debtToAssetsRatio = data.debt_to_assets_ratio;
          that.debtToAssetsRatioMessage = "负债占资产比率:" + (data.debt_to_assets_ratio).toFixed(0) + "%";
          if (that.debtToAssetsRatio >= 100) {
            that.debtToAssetsRatioComment = "杠杆比率太高了.风险巨大."
            that.debtToAssetsRatioLevel = 5
          }
          else if (that.debtToAssetsRatio < 100 && that.debtToAssetsRatio >= 80) {
            that.debtToAssetsRatioComment = "杠杆比率非常高.风险偏高."
            that.debtToAssetsRatioLevel = 4
          }
          else if (that.debtToAssetsRatio < 80 && that.debtToAssetsRatio >= 60) {
            that.debtToAssetsRatioComment = "杠杆比率偏高."
            that.debtToAssetsRatioLevel = 3
          }
          else if (that.debtToAssetsRatio < 60 && that.debtToAssetsRatio >= 30) {
            that.debtToAssetsRatioComment = "杠杆比率还可以."
            that.debtToAssetsRatioLevel = 2
          }
          else {
            that.debtToAssetsRatioComment = "基本没什么杠杆.股东很有信心!"
            that.debtToAssetsRatioLevel = 1
          }

          that.longTermAssetsToFixAssetsRatio = data.longterm_assets_to_fix_assets_ratio;
          that.longTermAssetsToFixAssetsRatioMessage = "长期资金占不动产及设备比率:" + (data.longterm_assets_to_fix_assets_ratio*100).toFixed(0) + "%";
          if (data.longterm_assets_to_fix_assets_ratio > 3) {
            that.longTermAssetsToFixAssetsRatioComment = "长期看来不缺钱!"
            that.longTermAssetsToFixAssetsRatioLevel = 1
          }
          else if (data.longterm_assets_to_fix_assets_ratio <= 3 && data.longterm_assets_to_fix_assets_ratio > 2) {
            that.longTermAssetsToFixAssetsRatioComment = "公司基础扎实."
            that.longTermAssetsToFixAssetsRatioLevel = 2
          }
          else if (data.longterm_assets_to_fix_assets_ratio <= 2 && data.longterm_assets_to_fix_assets_ratio > 1) {
            that.longTermAssetsToFixAssetsRatioComment = "公司基础一般."
            that.longTermAssetsToFixAssetsRatioLevel = 3
          }
          else {
            that.longTermAssetsToFixAssetsRatioComment = "公司基础不太行."
            that.longTermAssetsToFixAssetsRatioLevel = 4
          }

          that.quickRatio = data.quick_ratio;
          that.quickRatioMessage = "速动比率:" + (data.quick_ratio*100).toFixed(0) + "%";
          if (data.quick_ratio > 2) {
            that.quickRatioComment = "即使发生债务纠纷,公司也能立即清偿!"
            that.quickRatioLevel = 1
          }
          else if (data.quick_ratio <= 2 && data.quick_ratio > 1.5) {
            that.quickRatioComment = "即使发生债务纠纷,公司清偿问题也不大."
            that.quickRatioLevel = 2
          }
          else if (data.quick_ratio <= 1.5 && data.quick_ratio > 1) {
            that.quickRatioComment = "如果发生债务纠纷,公司可能遇到清偿问题."
            that.quickRatioLevel = 3
          }
          else {
            that.quickRatioComment = "如果发生债务纠纷,公司可能难以立即清偿."
            that.quickRatioLevel = 4
          }
          that.isShowRadar = true;
          that.startToShow = true;
          that.$forceUpdate();
          that.radarMaker(that);
        }


        // const lastScore = (res.data.cash_flow_score * 3 / 10) + (res.data.dept_paying_score / 10) + (res.data.em_score / 10)  + (res.data.roa_score / 4) + (res.data.roic_score / 4)
        // that.profitScore = Math.round(res.data.roic_score);
        // that.businessScore = Math.round(res.data.roa_score);
        // that.deptScore = Math.round(res.data.dept_paying_score);
        // that.cashScore = Math.round(res.data.cash_flow_score);
        // that.emScore = Math.round(50 + res.data.em_score / 2);
        // that.lastScore = Math.round(lastScore);
        // window.console.log(lastScore);

      })
    },
    radarMaker: function (that) {
      const chart = this.$echarts.init(document.getElementById('radarCanvas'));
      const stock = that.stock;
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        radar: [
          {
            indicator: [
              {text: '现金流', max: 100},
              {text: '偿债能力', max: 100},
              {text: '杠杆结构', max: 100},
              {text: '盈利能力', max: 100},
              {text: '运营能力', max: 100}
            ],
            center: ['50%', '50%'],
            radius: 90,
            startAngle: 90,
            shape: 'circle',
            name: {
              textStyle: {
                color: '#72ACD1'
              }
            },

          },
        ],
        series: [
          {
            type: 'radar',
            tooltip: {
              trigger: 'item'
            },
            areaStyle: {},
            data: [
              {
                value: [that.cashScore, that.deptScore, that.emScore, that.profitScore, that.businessScore],
                name: stock
              }
            ]
          },
        ]
      };
      chart.setOption(option);
    },
    chosenYear: function (index) {
      this.chosenYearIndex = index;
      this.getFinancialStatement();
    }
  },
  mounted() {
    this.getFinancialStatement()
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .canvas-holder {
    width: 100%;
    height: 300px;
  }

  #radarCanvas {
    width: 350px;
    height: 250px;
    z-index: 1;
  }

  #radarCanvas>div {
    z-index: 1;
  }

  #radarCanvas>div>canvas {
    z-index: 1;
  }

  .radar-header {
    width: 100%;
    height: 90px;
  }

  .header-text {
    width: 100%;
    height: 35px;
    text-align: left;
    font-size: 130%;
    font-weight: 600;
    line-height: 35px;
  }

  .header-bar {
    width: 100%;
    height: 40px;
    /*background-color: red;*/
    margin-top: 5px;
    display: flex;
    border-bottom: 1px solid #f7f7fa;
  }

  .year-btn {
    width: 20%;
    height: 40px;
    text-align: center;
    cursor: pointer;
    line-height: 40px;

  }

  .chosen-year {
    color: #0084ff;
    border-bottom: 2px solid #0084ff;
  }

  .comment-box {
    width: 100%;
    height: 302px;
    display: flex;
    flex-direction: column;
    border-top: 1px solid #F6F6F6;
  }

  .comment-line {
    width: 100%;
    height: 60px;
    border-bottom: 1px solid #F6F6F6;
    display: flex;
  }

  .comment-title {
    width: 20%;
    height: 60px;
    font-size: 90%;
    line-height: 60px;
    color: #a6a9b6;
    text-align: left;
  }

  .comment-text {
    width: 80%;
    /*font-size: 95%;*/
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .comment-text p {
    display: inline-block;
  }

  .level1 {
    color: #108ee9;
    font-size: 110% !important;
  }

  .level2 {
    color: #00CCCC;
    font-size: 100% !important;
  }

  .level3 {
    color: #32CD32;
    font-size: 90% !important;
  }

  .level4 {
    color: #CC9900;
    font-size: 90% !important;
  }

  .level5 {
    color: #FF3300;
    font-size: 100% !important;
  }

  .level6 {
    color: #DE0C2D;
    font-size: 110% !important;
  }

  .level0 {
    font-size: 90% !important;
  }

  .radar-shadow {
    width: 100%;
    height: 550px;
    background-color: rgba(250, 250, 250, 0.8);
    z-index: 9999;

    position: relative;

    /*top: 120px;*/
  }

  .radar-shadow>div {
    width: 100px;
    height: 50px;
    left: calc(50% - 50px);
    top: 250px;
    position: relative;
    cursor: pointer;
    line-height: 50px;
    color: rgb(160, 160, 160);
  }
</style>



// WEBPACK FOOTER //
// src/components/KLine.vue
