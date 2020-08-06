<template>
  <div class="page-holder">
    <div class="search-box">
      <input class="search-input" v-model="searchInput" placeholder="股票代码" v-on:input="searchConnect" v-on:blur="(showChoices = isMouseInChoices)" v-on:focus="(showChoices = true)"/>
      <img src="../assets/search.png" class="search-img">
    </div>
    <div class="search-choices" v-if="showChoices" v-on:mouseenter="mouseInChoices" v-on:mouseleave="mouseLeaveChoices">
      <div class="choices-box">
        <div class="choice-line" v-for="(item, index ) in searchAssociation" v-bind:key="index" v-on:click="choseStock(index)">
          <div class="line-content stock-content">
            {{ item.stock }}
          </div>
          <div class="line-content name-content">
            {{ item.name }}
          </div>
          <div class="line-content exchange-content">
            {{ item.exchange }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchAssociation',
  data () {
    return {
      searchInput: "",
      searchAssociation: [],
      showChoices: false,
      isMouseInChoices: false,
    }
  },
  methods: {
    mouseInChoices: function (event) {
      window.console.log(event);
      this.isMouseInChoices = true
    },
    mouseLeaveChoices: function (event) {
      window.console.log(event);
      this.isMouseInChoices = false
    },
    choseStock: function (index) {
//      window.console.log(stock.split("-")[0]);
      this.showChoices = false;
//      this.$router.push({
//
//      })
      window.console.log(this.searchAssociation[index]);
      const newPage = this.$router.resolve({
        name: "StockPage",
        params: {
          type: this.searchAssociation[index].isIndex,
          exchange: this.searchAssociation[index].exchange_abbr,
          stock: this.searchAssociation[index].stock,
        }
      });
      window.open(newPage.href,'_blank')
    },
    searchConnect: function() {
      const that = this;
      const targetUrl = "/api/searchAssociation?input=" + this.searchInput;
      window.console.log(this.searchInput);
      this.$axios.get(targetUrl, {}).then(function (res){
        window.console.log(res);
        that.showChoices = true;
        that.searchAssociation = res.data;
      })
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .search-box {
    min-width: 300px;
    min-height: 32px;
    width: 300px;
    height: 32px;
    /*background-color: red;*/
    display: flex;
    display: -webkit-flex;
    justify-content: center;
    align-items: center;
    background-color: #f7f7fa;
    border-radius: 1.5vh;
    /*padding-left: 20px;*/
  }

  .search-box input {
    min-width: 250px;
    min-height: 25px;
    width: 80%;
    height: 30px;
    border: none;
    background-color: #f7f7fa;
    outline: none;
    color: #a6a9b6;
    font-size: 100%;
  }

  .search-box img {
    width: 20px;
    height: 20px;
  }

  .search-choices {
    width: 300px;
    min-height: 40px;
    background-color: white;
    /*margin-top: 5px;*/
    border-radius: 5px;
    /*border: 1px solid rgba(150, 150, 150, 0.9);*/
    box-shadow: 1px 1px 3px rgba(150, 150, 150, 0.9);
    position: absolute;
    /*top: 5px;*/
    margin-top: 5px;
  }

  .choices-box {
    width: 280px;
    margin: 10px 10px 10px 10px;
    /*background-color: red;*/
  }

  .choice-line {
    width: 100%;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
    display: flex;
  }

  .choice-line:hover {
    background-color: #f7f7fa;
  }

  .line-content {
    width: 80px;
    height: 100%;
    text-align: left;
  }

  .exchange-content {
    width: 40px;
    text-align: right !important;
    overflow : hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }

  .stock-content {
    text-indent: 8px;
  }

  .name-content {
    width: 140px;
  }
</style>
