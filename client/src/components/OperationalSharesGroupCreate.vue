<template>
  <div class="content">
    <div class="content-top">
      <div class="base-info">
        <div class="name-line">
          <div class="name-title">
            组合名称
          </div>
          <div class="name-input">
            <input placeholder="必填" v-model="groupName" :class="(groupNameIsRepeat ? 'red-bottom' : '')"  v-on:blur="checkGroupName"/>
          </div>
        </div>
        <div class="name-line">
          <div class="name-title">
            市场范围
          </div>
          <div class="name-input">
            <select v-model="exchange">
              <option value="hs">
                沪深
              </option>
              <option value="hk">
                港股
              </option>
              <option value="us">
                美股
              </option>
            </select>
          </div>
        </div>
      </div>
      <div class="base-info">
        <div class="name-line">
          <div class="name-title">
            添加成分
          </div>
          <div class="name-input">
            <input class="search-input" placeholder="搜索股票\点击添加" v-on:input="searchConnect" v-model="searchInput" v-on:focus="(isShowResult = true)" />
            <div class="result-block" v-if="isShowResult">
              <div class="result-line" v-for="(item, index) in searchResult" v-bind:key="index" v-on:click="addItemInGroup(index)">
                {{ item.name }} ({{ item.stock }})
              </div>
            </div>
          </div>
        </div>
        <div class="name-line">
          <p>已选</p><p :class="leftScale == 0 ? 'red' : 'green'">{{ group.length }}</p><p>只股票，剩余仓位</p><p :class="leftScale == 0 ? 'red' : 'green'">{{ leftScale }}</p:class="leftScale><p>%</p>
        </div>
      </div>
      <div class="content-holder">
        <div class="content-header">
          <div class="header-button group-header-button">
            <p>
              股票
            </p>
            <!--          <i class="icon" style="background: url('../assets/sort_none.png') no-repeat center"></i>-->
          </div>

          <div class="header-button group-header-button">
            <p>
              成交价格
            </p>
          </div>

          <div class="header-button group-header-button">
            <p>
              所属行业
            </p>
          </div>

          <div class="header-button group-header-button">
            <p>
              持仓比例
            </p>
          </div>
        </div>
        <div class="content-center">
          <div class="content-line" v-for="(item, index) in group" v-bind:key="index">
            <div class="line-button group-line-button">
              <div class="button-top">
                {{ item.stockName }}
              </div>
              <div class="button-down">
                {{ item.stockCode }}
              </div>
            </div>
            <div :class="'line-button group-line-button ' + (item.chg.substr(0, 1) === '-' ? 'green' : 'red')">
              {{ item.price }}({{ item.chg }}%)
            </div>
            <div class="line-button group-line-button">
              {{ item.industry }}
            </div>
            <div class="line-button group-line-button">
              <input v-model="item.scale" v-on:blur="fixScaleInput(item.scale, index)" />%
            </div>
            <div class="line-button group-line-button">
              <img src="../assets/delete.png" v-on:click="deleteItemInGroup(index)" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="content-bottom">
      <div class="create-now" v-on:click="createNow">立即创建</div>
    </div>
    </div>
</template>

<script>export default {
  name: 'OperationalSharesGroupCreate',
  data () {
    return {
      groupName: "",
      groupNameIsRepeat: false,
      searchInput: "",
      isShowResult: false,
      searchResult: [],
      group: [],
      leftScale: 100,
      userCode: "",
      exchange: "hs",
      itemCreatedNum: 0,
    }
  },
  methods: {
    focusSearch: function () {
      this.isShowResult = true;
    },
    checkGroupName: function () {
      window.console.log(this.groupName)
      const that = this;
      if (this.groupName.length == 0) {
        this.groupNameIsRepeat = true;
        alert("组合名称为必填项！");
        return 0
      };

      if (this.groupName.indexOf(" ") != -1) {
        this.groupNameIsRepeat = true;
        alert("组合名称不能包含空格！");
        return 0
      };
      this.$axios.get("/api/optionalSharesGroup?userCode=" + this.userCode + "&groupName=" + this.groupName).then(function (res) {
        window.console.log(res)
        if (res.data != 404) {
          that.groupNameIsRepeat = true;
          alert("组合名称不能重复！您已有名为" + this.groupName + "的组合。")
        }
        else {
          that.groupNameIsRepeat = false;
        }
      })
    },
    createNow: function () {
      const that = this;
      if (this.groupNameIsRepeat) {
        return 0
      }
      if (this.group.length == 0) {
        alert("至少需要添加一只成分股！")
        return 0
      }
      const data = this.qs.stringify({
        "groupName": this.groupName,
        "userCode": this.userCode,
        "exchange": this.exchange,
      })
      this.$axios.post("/api/optionalSharesGroup", data).then(function (res) {
        window.console.log(res);
        if (res.data != 500) {
          const groupCode = res.data;
          for (let groupIndex in that.group) {
            let itemData = that.qs.stringify({
              "groupCode": groupCode,
              "stockCode": that.group[groupIndex]["stockCode"],
              "nameCN": that.group[groupIndex]["stockName"],
              "exchange": that.group[groupIndex]["exchange"],
              "salePrice": that.group[groupIndex]["price"],
              "nowVolume": that.group[groupIndex]["scale"],
              "userCode": that.userCode
            })
            that.$axios.post("/api/optionalSharesItem", itemData).then(function (res) {
              window.console.log(res)
              if (res.data == 200) {
                that.itemCreatedNum += 1;
                window.console.log(that.itemCreatedNum)
                if (that.itemCreatedNum == that.group.length) {
                  window.console.log(that.itemCreatedNum)
                  that.$emit('groupCreated', true)
                }
              }
              //else {
                
              //  that.$emit('groupCreated', false)
              //}
            })
          }
        }
      })
    },
    deleteItemInGroup: function (index) {
      const targetScale = parseFloat(this.group[index]["scale"]);
      this.leftScale += targetScale;
      this.group.splice(index, 1);

    },
    fixScaleInput: function (scale, index) {
      scale = parseFloat(scale).toFixed(2)
      this.group[index]["scale"] = 0;
      let scaleSum = 0;
      for (let groupIndex in this.group) {
        scaleSum += parseFloat(this.group[groupIndex]["scale"]);
      }
      window.console.log(scale)
      window.console.log(scaleSum)
      this.leftScale = 100 - scaleSum;
      window.console.log(this.leftScale)
      if (scale <= this.leftScale) {
        this.leftScale -= scale;
        this.leftScale.toFixed(2);
        this.group[index]["scale"] = scale;

      }
      else {
        this.group[index]["scale"] =  this.leftScale.toFixed(2);
        this.leftScale = 0.00;
      }

      this.$forceUpdate();
    },
    getPrice: function (stockCode, exchange, that) {
      let targetUrl = "/gu/q=";
      if (exchange === "sz" || exchange === "sh") {
        targetUrl += "s_" + exchange + stockCode + ","
      }
      else if (exchange === "us") {
        let stock = stockCode.toLowerCase().split(".")[0];
        targetUrl += "s_us" + stock.toUpperCase() + ","
      }
      else if (exchange === "hk") {
        targetUrl += "s_" + exchange + stock_code + ","
      }
      that.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res)
        for (let groupIndex in that.group) {
          if (that.group[groupIndex]["stockCode"] == stockCode) {
            that.group[groupIndex]["price"] = res.data.split("~")[3];
            that.group[groupIndex]["chg"] = res.data.split("~")[5];
          }
        }
      })
    },
    getIndustry: function (stockCode, that) {
      const targetUrl = "/api/stockIndustry?stockCode=" + stockCode;
      that.$axios.get(targetUrl, {}).then(function (res) {
        
        for (let groupIndex in that.group) {
          if (that.group[groupIndex]["stockCode"] == stockCode) {
            that.group[groupIndex]["industry"] = res.data;
          }
        }
      })

    },
    searchConnect: function() {
      const that = this;
      const targetUrl = "/api/searchAssociation?input=" + this.searchInput + "&filter=" + this.exchange;
      this.$axios.get(targetUrl, {}).then(function (res) {
        window.console.log(res.data)
        that.searchResult = [];
        if (res.data.length != 0) {
          that.isShowResult = true;
          that.searchResult = res.data;
        }
        else {
          that.isShowResult = false;
          that.searchResult = [];
        }
      })
    },
    addItemInGroup: function (index) {
      const that = this;
      let itemInfo = {
        "stockCode": this.searchResult[index]["stock"],
        "stockName": this.searchResult[index]["name"],
        "exchange": this.searchResult[index]["exchange_abbr"],
        "price": "",
        "industry": "",
        "scale": 0,
        "chg": ""
      };
      let isInGroup = false;
      for (let itemIndex in this.group) {
        if (this.group[itemIndex]["stockCode"] == itemInfo["stockCode"]) {
          isInGroup = true;
        }
      }

      if (isInGroup == false) {
        this.group.push(itemInfo);
        this.getPrice(itemInfo["stockCode"], itemInfo["exchange"], that);
        this.getIndustry(itemInfo["stockCode"], that);
        window.console.log(this.group)
      }
    }
    },
    mounted() {
      const _this = this;
      document.addEventListener("click", (e) => {
        let targetClassName = e.target.className;
        if (targetClassName != "result-block" && targetClassName != "result-line" && targetClassName != "search-input") {
          this.isShowResult = false;
        }
      })
      this.userCode = this.$cookie.get("userCode");
2    
    }
}</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .content {
    width: 100%;
    /*height: 300px;*/
    /*border: 1px solid #F6F6F6;*/
    /*background-color: red;*/
  }

  .content-top {
    border: 1px solid #F6F6F6;
  }

  .content-bottom {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .base-info {
    width: 100%;
    height: 44px;
    display: flex;
  }

  .name-line {
    width: 50%;
    height: 44px;
    display: flex;
  }

  .name-title {
    width: 80px;
    height: 44px;
    line-height: 44px;
    font-size: 95%;
    /*text-align: left;*/
  }

  .name-input {
    height: 44px;
    /*flex-grow: 4;*/
  }

  .name-input input {
    width: 100%;
    height: 40px;
    outline: none;
    border: none;
    border-bottom: 1px solid #F6F6F6;
    text-indent: 10px;
  }

  .name-input select {
    border: none;
    width: 80px;
    height: 44px;
    outline: none;
    border-bottom: 1px solid #F6F6F6;
    line-height: 40px;
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

  .result-block {
    width: 170px;
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: white;
    border-radius: 3px;
    border: 1px solid #F6F6F6;
    top: -1px;
  }

  .result-line {
    width: 100%;
    height: 30px;
    line-height: 30px;
    font-size: 90%;
    display: flex;
    text-align: left;
    cursor: pointer;
    padding-left: 10%;
    box-sizing: border-box;
  }

  .result-line:hover {
    background-color: #F6F6F6;
  }

  .content-holder {
    width: 100%;
    /*border: 1px solid #F6F6F6;*/
    display: flex;
    flex-direction: column;
    margin-top: 2px;
  }

  .content-header {
    width: 100%;
    height: 44px;
    background-color: #F6F6F6;
    display: flex;
  }

  .content-center {
    width: 100%;
    min-height: 44px;
    /*border: 1px solid #F6F6F6;*/
  }

  .content-line {
    width: 100%;
    height: 44px;
    display: flex;
    border-top: 1px solid #F6F6F6;
    border-bottom: 1px solid #F6F6F6;
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
  }

  .group-header-button {
    width: 20%!important;
  }

  .header-button:hover {
    background-color: #F9F9F9;
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

  .line-button input {
    width: 45px;
    outline: none;
    border: 1px solid #F6F6F6;
  }

  .line-button input:hover {
    background-color: #F6F6F6;
  }

  .name-line p {
    font-size: 95%;
    line-height: 44px;
    text-indent: 10px;
  }

  .line-button img {
    width: 20px;
    height: 20px;
    position: relative;
    left: 80px;
    top: 6px;
    cursor: pointer;  
  }

  .create-now {
    width: 30%;
    height: 40px;
    background-color: #009933;
    line-height: 40px;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 70%;
  }

  .red-bottom {
    border-bottom: 1px solid #E24528 !important;
    color: #E24528 !important;
  }
</style>
