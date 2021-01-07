<template>
  <div class="content-holder">
    <div class="content-header">
      <div class="header-text">
        我的自选
      </div>
      <div class="content-block" v-if="isShowContent">
        <div class="content-box" v-for="(item, index) in dataList" v-bind:key="index" v-on:click="jump(operationalSharesList[index])" v-on:mouseenter="hoverContent(index)" v-on:mouseleave="hoverContent(999)">
          <span class="box-title">{{ item[2] }}</span>
          <span :class="'box-text ' + (item[1].substr(0, 1) === '-' ? 'green' : 'red')">{{item[0]}}</span>
          <span :class="'box-text ' + (item[1].substr(0, 1) === '-' ? 'green' : 'red')">{{item[1]}}%</span>
<!--          <span class="box-title">{{ item.fields.name_cn }}</span>-->
<!--          <span class='box-text'>{{informationList[index][0]}}</span>-->
<!--          <span class='box-text'>{{informationList[index][1]}}%</span>-->
          <span class="delete" v-if="hoverIndex === index" v-on:click.stop="deleteOperationalShares(operationalSharesList[index])">
            ×
          </span>
        </div>
      </div>
      <div class="content-block shadow" v-else-if="!isLogin">
        <div>
          <a class='light-blue block' style="text-decoration: none;" href="/#/login">登录</a>  后解锁自选股
        </div>
      </div>
      <div class="content-block shadow" v-else>
        <div>
          还没有添加自选股
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'OperationalShares',
  components: {

  },
  props: {
    stock: {
      type: String,
    },
  },
  data () {
    return {
      operationalSharesList: [],
      isShowContent: false,
      informationList: [],
      hoverIndex: 999,
      startToShow: false,
      isLogin: false,
      dataList: [],
    }
  },

  methods: {
    deleteOperationalShares: function (stock) {

      const that = this;
      const userCode = this.$cookie.get("userCode");
      this.$axios.delete("/api/optionalShares?userCode=" + userCode + "&stockCode=" + stock.fields.stock_code, {}).then(function (res){

        that.getOperationalShares();
      })
    },
    hoverContent: function (index) {
      this.hoverIndex = index;

    },
    jump: function (stock) {

      const newPage = this.$router.resolve({
        name: "StockPage",
        params: {
          type: "GP",
          exchange: stock.fields.exchange,
          stock: stock.fields.stock_code,
        }
      });
      window.open(newPage.href,'_blank')
    },
    getOperationalShares: async function () {
      const that = this;
      const userCode = this.$cookie.get("userCode");
      window.console.log(7)
      await this.$axios.get("/api/optionalShares?userCode=" + userCode, {}).then(function (res){

        if (res.data === 404) {
          that.isShowContent = false
        }
        else {
          that.operationalSharesList = res.data;
          window.console.log(8)

          for (let stockIndex in res.data) {
            if (that.stock === res.data[stockIndex].fields.stock_code) {
              that.$parent.changeAddButton(true);
            }
          }
        }

      })
      window.console.log(9)
      await this.getNowPrice();
    },
    getNowPrice: function () {
      const that = this;
      let targetUrl = "/gu/q="
      window.console.log(10)
      for (let stockIndex in that.operationalSharesList) {
        if (that.operationalSharesList[stockIndex].fields.exchange === "sz" || that.operationalSharesList[stockIndex].fields.exchange === "sh") {
          targetUrl += "s_" + that.operationalSharesList[stockIndex].fields.exchange + that.operationalSharesList[stockIndex].fields.stock_code + ","
        }
        else if (that.operationalSharesList[stockIndex].fields.exchange === "us") {
          let stock = that.operationalSharesList[stockIndex].fields.stock_code.toLowerCase().split(".")[0];
          targetUrl += "s_us" + stock.toUpperCase() + ","
        }
        else if (that.operationalSharesList[stockIndex].fields.exchange === "hk") {
          targetUrl += "s_" + that.operationalSharesList[stockIndex].fields.exchange + that.operationalSharesList[stockIndex].fields.stock_code + ","
        }
      }
      that.$axios.get(targetUrl, {}).then(function (res){
        window.console.log(res.data)
        const data = res.data.split(";");
        let informationList = [];
        data.pop();

        for (let stockIndex in data) {

          informationList.push([data[stockIndex].split("~")[3], data[stockIndex].split("~")[5], that.operationalSharesList[stockIndex].fields.name_cn]);

          window.console.log(data.length)
          window.console.log(informationList.length)
        }
        window.console.log(informationList)
        if (informationList.length === data.length) {
          that.isShowContent = true;
          that.dataList = informationList;
          that.$forceUpdate();
          window.console.log(555)
        }
        else {
          window.console.log(666)
        }

      })
      window.console.log(12)
    }
  },
  mounted() {
    if (!this.$cookie.get("userCode")) {
      this.isLogin = false;
    }
    else {
      this.isLogin = true;
      this.getOperationalShares();
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .content-holder {
    width: 100%;
    min-height: 150px;
    /*background-color: red;*/
    margin-top: 400px;
  }

  .content-header {
    width: 100%;
    height: 35px;
  }

  .header-text {
    width: 100%;
    height: 35px;
    text-align: left;
    font-size: 130%;
    font-weight: 600;
    line-height: 35px;
  }

  .content-block {
    width: 110%;
    height: auto;
    /*background-color: green;*/
    /*overflow: scroll;*/
    /*overflow-x: hidden;*/
    display: flex;
    flex-wrap: wrap;
  }

  .content-box {
    width: auto;
    height: 30px;
    padding-left: 10px;
    padding-right: 10px;
    background-color: #F6F6F6;
    line-height: 30px;
    font-size: 90%;
    margin-right: 10px;
    border-radius: 15px;
    cursor: pointer;
    margin-top: 10px;
    display: flex;
  }

  .content-box span {
    display: inline-block;
  }

  .light-blue {
    color: #06c;
  }

  .block {
    display: inline-block;
    cursor: pointer;
    user-select: none;
    /*line-height: 20px;*/
    word-break: break-all;
    height: 20px;
  }

  .shadow {
    width: 100%;
    height: 100px;
    background-color: rgba(250, 250, 250, 0.8);
    position: relative;
    overflow: hidden !important;
  }

  .shadow>div {
    width: 200px;
    height: 50px;
    left: calc(50% - 100px);
    top: 25px;
    position: relative;
    line-height: 50px;
    color: rgb(160, 160, 160);
  }

  .content-info-box {
    width: 80px;
    height: 80px;
    background-color: red;
    z-index: 999;
  }

  .box-title {
    font-size: 95% !important;
    max-width: 200px;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
    display: inline-block;
  }

  .box-text {
    margin-left: 5px;
    font-size: 95% !important;
  }

  .green{
    color:#009933;
  }

  .red{
    color:#E24528;
  }

  .delete {
    width: 20px;
    height: 20px;
    font-size: 100% !important;
    /*margin-top: 5px;*/
    /*position: relative;*/
    /*top: 5px;*/
    color: red;
    border-radius: 10px;
  }

  /*.delete:hover {*/
  /*  background-color: red;*/
  /*  color: white;*/
  /*  !*margin-top: 5px;*!*/
  /*}*/

</style>


