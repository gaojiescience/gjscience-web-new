<template>
  <div class="root">

    <div class="add-shadow" v-show="isShowShadow" v-on:click="changeShadowStatus">
      <div class="add-stock-holder" style="z-index: 999; background-color: rgba(255, 255, 255, 0.8); position: absolute;" v-show="isTransactionStart">

      </div>
      <div class="add-stock-holder" v-on:click.stop="enterResult(false)">
        <div class="holder-title">
          股票交易
        </div>
        <div class="info-line">
          <div class="line-header">
            股票搜索
          </div>
          <div class="line-content">
            <input placeholder="搜索股票代码/名称" @keyup="stockSearch" v-model="keyword" :class="!isStockSelected ? 'red-border' : ''"/>
          </div>
        </div>
        <div class="result-box" v-show="isShowResult">
          <div class="result-line" v-for="(item, index) in resultList" v-bind:key="index" v-on:click="enterResult(item)">
            <p>{{ item.fields.symbol }}</p>
            <p>{{ item.fields.name_cn }}</p>
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            交易类型
          </div>
          <div class="line-content">
            <select v-model="transactionType">
              <option value="0">
                买入
              </option>
              <option value="1">
                卖出
              </option>
            </select>
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            交易日期
          </div>
          <div class="line-content">
            <input v-model="date" readonly />
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            交易价格
          </div>
          <div class="line-content">
            <input v-model="tradeStockNowInfoStr" readonly />
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            交易数量
          </div>
          <div class="line-content">
            <input v-model="tradeNum" v-on:blur="checkTradeNum" type="number"/>
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            佣金/税费
          </div>
          <div class="line-content">
            <input v-model="commissionAndTax" readonly />
          </div>
        </div>
        <div class="info-line">
          <div class="line-header">
            备注
          </div>
          <div class="line-content">
            <textarea v-model="transactionMark"></textarea>
          </div>
        </div>
        <div class="btn-line">
          <div class="btn cancel"  v-on:click="changeShadowStatus">
            取消
          </div>
          <div class="btn submit" v-on:click="createTransaction">
            确认
          </div>
        </div>
      </div>
    </div>

    <div class="content-nav">
      <div class="nav-left" v-for="(item, index) in walletList" v-bind:key="index">
        <div :class="'nav-button ' + (nowChosenButton === index ? 'chosen-button' : '')">
          {{ item.wallet_name }}
        </div>
      </div>
      <div class="nav-right">
        <div class="create-button">
          数据导出
        </div>
      </div>
    </div>
    <div class="content-holder">
      <div class="sum-box">
        <div class="box-top">
          <div class="total-assets-btn">
            总资产(CNY)
          </div>
          <div class="total-assets-btn">
            总市值(CNY)
          </div>
          <div class="total-assets-btn">
            现金(CNY)
          </div>
          <div class="total-assets-btn">
            今日盈亏(CNY)
          </div>
        </div>
        <div class="box-bottom">
          <div class="total-assets-text">
            {{(parseFloat(walletList[nowChosenWalletIndex].balance) + totalValue).toFixed(2)}}
          </div>
          <div class="total-assets-text">
            {{totalValue}}
          </div>
          <div class="total-assets-text">
            {{(walletList[nowChosenWalletIndex].balance)}}
          </div>
          <div class="total-assets-text">
            {{lastChange.toFixed(2)}}({{this.lastChg.toFixed(4)}}%)
          </div>
        </div>
      </div>
    </div>

    <div class="ctrl-line">
      <div class="chosen-box">
        <div class="chosen-btn">
          持仓
        </div>
        <div class="chosen-btn">
          交易记录
        </div>
        <div class="chosen-btn">
          转账记录
        </div>
      </div>
      <div class="chosen-box">
        <div class="chosen-btn protrude-btn" v-on:click="changeShadowStatus">
          买入
        </div>
        <div class="chosen-btn protrude-btn">
          卖出
        </div>
        <div class="chosen-btn protrude-btn">
          转账
        </div>
      </div>
    </div>

    <div class="content-header">
      <div class="header-button group-header-button">
        <p id="all">
          名称/代码
        </p>
      </div>

      <div class="header-button group-header-button" v-on:click="changePriceSort('price')">
        <p>
          现价
        </p>
        <svg v-if="nowChosenSort === 'change' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'change' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>

      <div class="header-button group-header-button" v-on:click="changePriceSort('change')">
        <p>
          涨跌
        </p>
        <svg v-if="nowChosenSort === 'chg' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'chg' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>

      <div class="header-button group-header-button" v-on:click="changePriceSort('cost')">
        <p>
          市值
        </p>
        <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>

      <div class="header-button group-header-button" v-on:click="changePriceSort('volume')">
        <p>
          持仓
        </p>
        <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>

      <div class="header-button group-header-button" v-on:click="changePriceSort('float')">
        <p>
          浮动盈亏
        </p>
        <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>

      <!--<div class="header-button group-header-button" v-on:click="changePriceSort('sum')">
        <p>
          今日盈亏
        </p>
        <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>-->

      <div class="header-button group-header-button">
        <p>
          操作
        </p>
        <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
        <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
        <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
      </div>
    </div>

    <div class="content-center">
      <div class="content-line" v-for="(item, index) in walletList[nowChosenWalletIndex].stock_list" v-bind:key="index">
        <div class="line-button group-line-button">
          <div class="button-top">
            {{item.name_cn}}
          </div>
          <div class="button-down">
            {{item.stock_code}}
          </div>
        </div>
        <!--<div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">-->
        <div class="line-button group-line-button">
          {{item.now}}
        </div>

        <!--<div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">-->
        <div class="line-button group-line-button">
          {{item.change}}({{item.chg}}%)
        </div>

        <!--<div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">-->
        <div class="line-button group-line-button">
          {{item.value}}
        </div>
        <div class="line-button group-line-button">
          {{item.now_volume}}
        </div>
        <div class="line-button group-line-button">
          {{item.floatProfitChange}}({{item.floatProfitChg}}%)
        </div>
        <!--<div class="line-button group-line-button">
          0(0.00%)
        </div>-->
        <div class="line-button group-line-button">
          
        </div>
      </div>
      </div>
    </div>
</template>

<script>
  export default {
    name: "OperationalSharesDetail.vue",
    data() {
      return {
        nowChosenButton: 0,
        walletList: [],
        nowChosenWalletIndex: 0,
        nowChosenSort: "change",
        nowSortIndex: 0,
        stockList: [],
        isShowShadow: false,
        keyword: "",
        date: "",
        isShowResult: false,
        tradeStockNowInfo: ["", ""],
        tradeStockNowInfoStr: "",
        resultList: [],
        tradeNum: "",
        transactionMark: "",
        stock: "",
        stockName: "",
        commissionAndTax: "1‰",
        transactionType: "0",
        isTransactionStart: false,
        isStockSelected: true,
        isTradeNumSelected: true,
        allStockNowInfo: [],
        todayProfitChange: 0,
        todayProfitChg: 0,
        record: {},
        totalValue: 0,
        lastChange: 0.00,
        lastChg : 0.00,
      }
    },
    methods: {
      getWalletList: function () {
        const that = this;
        this.$axios.get("/api/wallet?userCode=" + this.userCode + "&stockList=1").then(function (res) {
          window.console.log(res)
          that.walletList = res.data.data;
          //that.getStockList()
        })
      },
      getStockList: function (symbols) {
        const that = this;
        this.$axios.get("/api/stockManager?symbols=" + symbols).then(function (res) {
          window.console.log(res)
          that.stockList = res.data.data;
          //that.getStockList()
        })
      },
      checkTradeNum: function () {
        //window.console.log((56.1).toFixed(0))
        if (this.tradeNum <= 0 || !this.tradeNum) {
          this.tradeNum = 1
        }
        else {
          this.tradeNum = parseFloat(this.tradeNum).toFixed(0);
        }
      },
      getCurrentPrice: function () {
        const that = this;
        //window.console.log(that.walletList)
        //window.console.log(that.walletList[0])
        //window.console.log(that.nowChosenWalletIndex)
        const stockList = this.walletList[this.nowChosenWalletIndex].stock_list;
        let stockCodes = "";
        for (let stockIndex in stockList) {
          stockCodes += stockList[stockIndex].stock_code + ","
        }
         this.$axios.get("/api/wallet?walletCode=" + walletCode + "&type=info").then(function (res) {
           window.console.log(res)
           that.stockList = res.data;
           that.getAllStockNowPrice();
           that.getAllTransactionRecord(that.date);
           
        })
      },
      changePriceSort: function (sort) {
        this.nowSortIndex === 2 ? this.nowSortIndex = 0 : this.nowSortIndex += 1;
        this.nowChosenSort = sort;
      },
      changeShadowStatus: function () {
        this.isShowShadow = !this.isShowShadow;
        if (this.isShowShadow) {
          document.documentElement.style.overflowY = 'hidden';
          this.tradeStockNowInfo = ["", ""];
          this.tradeStockNowInfoStr = "";
          this.resultList = [];
          this.tradeNum = "";
          this.keyword = "";
          this.mark = ""
        }
        else {
          document.documentElement.style.overflowY = 'scroll';
        }
      },
      nothing: function () {

      },
      stockSearch: function () {
        window.console.log(this.keyword);
        const that = this;
        this.isShowResult = true;
        this.$axios.get("/api/stockSearch?keyword=" + this.keyword).then(function (res) {
           window.console.log(res)
          that.resultList = res.data;
        })
      },
      enterResult: function (item) {
        if (item) {
          this.keyword = item.fields.symbol + "    " + item.fields.name_cn;
          let func = function (data, that) {
            data = data[0].split("~")
            that.tradeStockNowInfo = [parseFloat(data[3]), parseFloat(data[32])];
            that.tradeStockNowInfoStr = parseFloat(data[3]) + "  (" + parseFloat(data[32]) + "%)";
          }
          let exchange = item.fields.exchange == "SSE" ? "sh" : "sz";
          let stock = item.fields.symbol;
          this.stock = stock;
          this.exchange = exchange;
          this.stockName = item.fields.name_cn;
          this.getStockRealTimeInfo(exchange+stock, func);
        }
        this.isShowResult = false;
        this.isStockSelected = true;
      },
      getAllTransactionRecord: function (date) {
        const that = this;
        this.$axios.get("/api/transaction?walletCode=" + this.walletList[this.nowChosenWalletIndex].fields.wallet_code + "&date=" + date).then(function (res) {
          that.record = res.data;
          window.console.log(that.record)
        })
      },
      calcDailyProfit: function () {
        let lastValue = this.walletList[this.nowChosenWalletIndex].fields.balance;
        for (let dataIndex in this.stockList) {
          //window.console.log(this.record[this.stockList[dataIndex].fields.stock_code])
          if (!this.record[this.stockList[dataIndex].fields.stock_code]) {
            this.lastChange += (this.stockList[dataIndex].fields["now"] - this.stockList[dataIndex].fields["last"]) * this.stockList[dataIndex].fields["now_volume"];
            this.lastChg += ((this.stockList[dataIndex].fields["now"] - this.stockList[dataIndex].fields["last"]) * this.stockList[dataIndex].fields["now_volume"]) / (this.stockList[dataIndex].fields["last"] * this.stockList[dataIndex].fields["now_volume"])
          }
          else {
            window.console.log(12)
            for (let recordIndex in this.record[this.stockList[dataIndex].fields.stock_code]) {
              lastValue -= (parseFloat(this.record[this.stockList[dataIndex].fields.stock_code][recordIndex]["transaction_commission"]) + parseFloat(this.record[this.stockList[dataIndex].fields.stock_code][recordIndex]["transaction_sum"]))
              lastValue -= this.stockList[dataIndex].fields["last"] * (this.stockList[dataIndex].fields["now_volume"] - this.record[this.stockList[dataIndex].fields.stock_code][recordIndex]["item_num"])
            }
            this.lastChange = parseFloat(this.walletList[this.nowChosenWalletIndex].fields.balance) + parseFloat(this.totalValue) - 100000
            this.lastChg = this.lastChange / 100000
          }
        }
        window.console.log(lastValue)
        this.$forceUpdate();
      },
      getAllStockNowPrice: function () {
        let stocks = "";
        for (let stockIndex in this.stockList) {
          let exchange = this.stockList[stockIndex].fields.exchange;
          stocks += (exchange + this.stockList[stockIndex].fields.stock_code + ",")
        }
        let func = function (data, that) {
          window.console.log(data);
          that.totalValue = 0;
          for (let dataIndex in data) {
            let nowData = data[dataIndex].split("~");
            
            that.stockList[dataIndex].fields["now"] = parseFloat(nowData[3]);
            that.stockList[dataIndex].fields["last"] = nowData[4];
            that.stockList[dataIndex].fields["chg"] = nowData[32];
            that.stockList[dataIndex].fields["change"] = nowData[31];
            that.stockList[dataIndex].fields["value"] = (that.stockList[dataIndex].fields["now"] * that.stockList[dataIndex].fields["now_volume"]).toFixed(2);
            that.stockList[dataIndex].fields["floatProfitChange"] = ((that.stockList[dataIndex].fields["now"] - that.stockList[dataIndex].fields["cost"]) * that.stockList[dataIndex].fields["now_volume"]).toFixed(2);
            that.stockList[dataIndex].fields["floatProfitChg"] = (that.stockList[dataIndex].fields["floatProfitChange"] / (that.stockList[dataIndex].fields["cost"] * that.stockList[dataIndex].fields["now_volume"])).toFixed(4);
            that.totalValue += parseFloat(that.stockList[dataIndex].fields["value"])
          }
          that.$forceUpdate();
          that.calcDailyProfit()
          window.console.log(that.stockList);
        }
        this.getStockRealTimeInfo(stocks, func);
      },
      getStockRealTimeInfo: function (stocks, func) {
        let targetUrl = "/gu/q=" + stocks;
        const that = this;
        this.$axios.get(targetUrl, {}).then(function (res) {
          window.console.log(res)
          const data = res.data.split(";");
          data.pop();
          window.console.log(data)
          func(data, that);
        })
      },
      checkData: function () {
        this.isStockSelected = this.stock ? true : false;
        this.isTradeNumSelected = this.tradeNum ? true : false;
      },
      createTransaction: function () {
        this.checkData();
        window.console.log(this.isStockSelected)
        if (!(this.isStockSelected && this.isTradeNumSelected)) {
          return false;
        }
        this.isTransactionStart = true;
        const that = this;
        let walletCode = this.walletList[this.nowChosenWalletIndex].fields.wallet_code;
        let targetUrl = "/api/transaction"
        const data = {
          "walletCode": walletCode,
          "itemCode": this.stock,
          "itemNum": parseFloat(this.tradeNum).toFixed(0),
          "itemCost": parseFloat(this.tradeStockNowInfo[0]),
          "itemName": this.stockName,
          "transactionType": parseInt(this.transactionType),
          "transactionMark": this.transactionMark,
          "exchange": this.exchange
        }
        window.console.log(data)
        this.$axios.post(targetUrl, this.qs.stringify(data)).then(function (res) {
          window.console.log(res)
          if (res.data == 200) {
            setTimeout(function(){ that.isTransactionStart = false;that.isShowShadow = false; that.getWalletList(); that.$forceUpdate();}, 1000);
          }
          
        })
      }
    },
    mounted() {
      this.userCode = this.$cookie.get("userCode");
      let date = new Date();
      this.date = (date.getFullYear()).toString() + "-" + ((date.getMonth() + 1) < 10 ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1)).toString() + "-" + (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()).toString();
      date.setTime(date.getTime() - 24 * 60 * 60 * 1000);
      this.lastDate = (date.getFullYear()).toString() + "-" + ((date.getMonth() + 1) < 10 ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1)).toString() + "-" + (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()).toString();
    },
    watch: {
     
    }
  }
</script>

<style scoped>

  .root {
    width: 100%;
    min-height: 600px;
  }

  .content-nav {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: space-around;
  }

  .nav-left {
    width: 60%;
    height: 100%;
    /*border-bottom: 1px solid #F6F6F6;*/
    display: flex;
    justify-content: flex-start;
  }

  .nav-right {
    width: 40%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
    /*background-color: black;*/
  }

  .create-button {
    width: 80px;
    height: 28px;
    margin-top: 7px;
    line-height: 28px;
    background-color: #0084FF;
    color: white;
    border-radius: 3px;
    font-size: 95%;
    cursor: pointer;
  }

  .ban-create-button {
    width: 80px;
    height: 28px;
    margin-top: 7px;
    line-height: 28px;
    background-color: #E24528;
    color: white;
    border-radius: 3px;
    font-size: 95%;
    cursor: pointer;
  }

  .nav-button {
    width: 80px;
    height: 100%;
    line-height: 40px;
    cursor: pointer;
  }

  .chosen-button {
    border-bottom: 2px solid #0084ff;
    color: #06c;
  }

  .content-holder {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-top: 5px;
  }

  .sum-box {
    width: 100%;
    height: 150px;
    border: 1px solid #F6F6F6;
    display: flex;
    flex-direction: column;
  }

  .box-top {
    width: 100%;
    height: 50px;
    display: flex;
  }

  .total-assets-btn {
    width: 200px;
    height: 100%;
    font-size: 90%;
    line-height: 80px;
    text-align: left;
    text-indent: 30px;
    color: #666c72;
  }

  .box-bottom {
    width: 100%;
    height: 100px;
    display: flex;
  }

  .total-assets-text {
    width: 200px;
    height: 100%;
    text-align: left;
    text-indent: 30px;
    font-size: 200%;
    line-height: 70px;
    color: #07b360;
  }

  .ctrl-line {
    width: 100%;
    height: 44px;
    display: flex;
    padding-top: 20px;
    justify-content: space-between;
  }

  .chosen-box {
    height: 30px;
    display: flex;
  }

  .chosen-btn {
    padding-left: 10px;
    padding-right: 10px;
    margin-right: 10px;
    height: 28px;
    line-height: 28px;
    border-radius: 3px;
    font-size: 95%;
    cursor: pointer;
  }

  .content-header {
    width: 100%;
    height: 44px;
    background-color: #F6F6F6;
    display: flex;
  }

  .content-center {
    width: 100%;
    /*border: 1px solid #F6F6F6;*/
  }

  .content-line {
    width: 100%;
    height: 44px;
    display: flex;
    border-top: 1px solid #F6F6F6;
  }

  .header-button {
    width: 15%;
    height: 44px;
    line-height: 44px;
    text-align: start;
    text-indent: 20px;
    font-size: 95%;
    display: flex;
    cursor: pointer;
    user-select:none;
  }

  .group-header-button {
    width: 20%!important;
  }

    .header-button:hover {
      background-color: #F9F9F9;
    }


  .icon {
    width: 10px;
    height: 5px;
    margin-top: 20px;
    margin-left: 3px;
  }

  .header-button i {
    width: 10px;
    height: 20px !important;
  }

  .line-button {
    width: 15%;
    height: 44px;
    line-height: 44px;
    text-align: start;
    text-indent: 20px;
    font-size: 90%;
  }

  .group-line-button {
    width: 20%!important;
  }

  .button-top {
    height: 50%;
    line-height: 28px !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .button-down {
    height: 50%;
    line-height: 20px !important;
    color: #a6a9b6;
  }

  .green {
    color: #009933;
  }

  .red {
    color: #E24528;
  }

  .content-line p {
    display: inline-block;
    width: 100%;
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-size: 95%;
  }

  .all-choices {
    width: 120px;
    height: 165px;
    background-color: white;
    box-shadow: 1px 1px 4px rgba(120, 120, 120, 0.9);
    position: absolute;
    /*left: -90px;*/
    top: 178px;
    border-radius: 3px;
  }

  .choice-btn {
    width: 100%;
    height: 40px;
    line-height: 40px;
    border-bottom: 1px solid #F6F6F6;
    cursor: pointer;
    text-align: left;
    text-indent: 20px;
    font-size: 95%;
  }

    .choice-btn:hover {
      background-color: #F6F6F6;
    }

  .protrude-btn {
    background-color: #0084FF;
    color: white;
  }

  .add-shadow {
    width: 100vw;
    height: 100vh;
    position: absolute;
    left: 0;
    top: 0;
    background-color: rgba(0, 0, 0,  0.5);
    z-index: 9999;
  }

  .add-stock-holder {
    width: 400px;
    height: 600px;
    background-color: white;
    position: relative;
    left: calc(50vw - 200px);
    top: calc(50vh - 300px);
    border-radius: 5px;
    box-sizing: border-box;
    padding: 10px 30px 10px 30px;
  }

  .holder-title {
    width: 100%;
    height: 50px;
    text-align: left;
    font-size: 110%;
    font-weight: 600;
    line-height: 50px;
    border-bottom: 1px solid #edf0f5;
  }

  .info-line {
     width: 100%;
     height: 50px;
     display: flex;
     line-height: 50px;
     margin-top: 10px;
  }

  .line-header {
    width: 30%;
    text-align: left;
    font-size: 95%;

  }

  .line-content {
    width: 70%;
    height: 50px;
  }

  .line-content input {
    width: 100%;
    height: 30px;
    outline: none;
    border: 1.5px solid #edf0f5;
    border-radius: 5px;
    text-indent: 10px;
  }

  .line-content select {
    width: 100%;
    height: 32px;
    outline: none;
    border: 1.5px solid #edf0f5;
    border-radius: 5px;
    text-indent: 5px;
  }

  .line-content textarea {
    width: 100%;
    height: 100%;
    margin-top: 10px;
    outline: none;
    border: 1.5px solid #edf0f5;
    border-radius: 5px;
    box-sizing: border-box;
    padding: 5px;
  }

  .result-box {
    width: 240px;
    background-color: white;
    border: 1px solid #edf0f5;
    z-index: 999;
    position: absolute;
    left: 33%;
  }

  .result-line {
    width: 100%;
    height: 30px;
    display: flex;
    line-height: 30px;
    font-size: 90%;
    cursor: pointer;
    padding-left: 10px;
    padding-right: 10px;
    box-sizing: border-box;
  }

  .result-line:hover {
    background-color: #F6F6F6;
  }

  .result-line p {
    width: 50%;
    text-align: left;
  }

  .btn-line {
    width: 100%;
    height: 50px;
    display: flex;
    margin-top: 40px;
    justify-content: space-between;
  }

  .btn {
    width: 90px;
    height: 28px;
    line-height: 28px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 95%;
  }

  .cancel {
    background-color: #e6f1fb;
    color: #0084FF;
  }

  .submit {
    background-color: #0084FF;
    color: white;
  }

  .red-border {
    border: 1px solid #f44e50 !important;
    color: red;
  }
</style>
