<template>
  <div class="page-container">
      <div class="top-holder">
          <div class="top-content">
              <!--<div class="content-left">-->
                  <div class="icon-box">
                      <img src="../assets/logo-light.png">
                  </div>
                  <div class="btn-box">
                      <div class="information-btn btn">
                          资讯
                      </div>
                      <div class="discussion-btn btn">
                          论坛
                      </div>
                      <div class="information-btn btn">
                          登录
                      </div>
                      <div class="discussion-btn btn">
                          注册
                      </div>
                  </div>
                  <!--<div class="search-box">-->
                      <!--<input class="search-input" placeholder="沪深300股票代码"/>-->
                      <!--<img src="../assets/search.png">-->
                  <!--</div>-->
              <!--</div>-->
              <!--<div class="content-right">-->
              <!--</div>-->

          </div>
      </div>
      <div class="center-holder">
          <div  class="center-content">
              <div class="search-box">
                  <input class="search-input" placeholder="沪深300股票代码"/>
                  <img src="../assets/search.png">
              </div>
              <div class="content-box">
                  <div class="content-block">
                      <div class="block-title" style="z-index: 10">
                          <div class="title-box">
                              沪深300排行
                          </div>
                          <div class="btn-box">
                              <div class="btn">
                                  <Calendar class="calendar" msg="hs300|start" @setStartDate="setStartDate"></Calendar>

                                  <!--<Calendar></Calendar>-->
                              </div>
                              <div class="btn">
                                  <Calendar class="calendar" msg="hs300|end" @setStartDate="setStartDate"></Calendar>
                              </div>
                              <div class="btn">
                                  <select class="sort-box" v-model="hs300Sort">
                                      <option value="1">增长最多</option>
                                      <option value="0">亏损最多</option>
                                  </select>
                              </div>
                              <div class="btn">
                                  <select class="sort-box" v-model="hs300Top">
                                      <option value="10">Top10</option>
                                      <option value="20">Top20</option>
                                  </select>
                              </div>
                              <div class="btn go-box" v-on:click="startDraw('hs300')">
                                  开始
                              </div>
                          </div>
                      </div>
                      <div class="block-center" style="z-index: 1">
                          <div id="hs300_bar" class="bar">

                          </div>
                      </div>

                  </div>
                  <div class="content-block">
                      <div class="block-title" style="z-index: 10">
                          <div class="title-box">
                              恒生50排行
                          </div>
                          <div class="btn-box">
                              <div class="btn">
                                  <Calendar class="calendar" msg="hk50|start" @setStartDate="setStartDate"></Calendar>

                                  <!--<Calendar></Calendar>-->
                              </div>
                              <div class="btn">
                                  <Calendar class="calendar" msg="hk50|end" @setStartDate="setStartDate"></Calendar>
                              </div>
                              <div class="btn">
                                  <select class="sort-box" v-model="hk50Sort">
                                      <option value="1">增长最多</option>
                                      <option value="0">亏损最多</option>
                                  </select>
                              </div>
                              <div class="btn">
                                  <select class="sort-box" v-model="hk50Top">
                                      <option value="10">Top10</option>
                                      <option value="5">Top5</option>
                                  </select>
                              </div>
                              <div class="btn go-box" v-on:click="startDraw('hk50')">
                                  开始
                              </div>
                          </div>
                      </div>
                      <div class="block-center" style="z-index: 1">
                          <div id="hk50_bar" class="bar">

                          </div>
                      </div>

                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import Calendar from "../components/Calendar"
export default {
    name: 'IndexPage',
    components: {
        Calendar,
    },
    data () {
        return {
            nowChosenStock: "000651",
            hs300Start: "2019-1-1",
            hs300End: "2020-1-1",
            hs300Data: [],
            hs300Days: [],
            hs300Sort: "1",
            hs300Top: "10",
            hk50Start: "2019-1-1",
            hk50End: "2020-1-1",
            hk50Data: [],
            hk50Days: [],
            hk50Sort: "1",
            hk50Top: "10"
        }
    },
    methods: {
        startDraw (type) {
            const that = this;
//            window.console.log(this.sort)
            let params;
            if (type == "hs300") {
                params = {
                    stock: this.nowChosenStock,
                    start: this.hs300Start,
                    end: this.hs300End,
                    method: "growth",
                    top: this.hs300Top,
                    sort: this.hs300Sort,
                    area: "hs300"
                };

                this.$axios.get("/community/kline", {
//                start=2019-1-1&end=2020-6-1&method=growth&top=10&sort=1
                    params: params
                }).then(function (res) {
                    that.hs300DataList = [];
                    that.hs300DataWithSignList = [];
                    that.hs300NameList = [];
                    that.hs300StockList = [];
                    [...Array(res.data.length).keys()].forEach(function (data) {
    //                    window.console.log(res.data[data])
                        that.hs300DataList.push(parseFloat(res.data[data]["rate_of_increase"]));
                        that.hs300DataWithSignList.push(res.data[data]["rate_of_increase"] + "%");
    //                    that.rateList.push(res.data[data]["rate_of_increase"])
                        that.hs300NameList.push(res.data[data]["name"]);
                        that.hs300StockList.push({
                            "value": res.data[data]["stock"]
                        });

    //                    that.priceList.push(res.data[data]["start_price"] + "-" + res.data[data]["end_price"])
                    });
                    that.$forceUpdate();
    //                window.console.log(that.dataList);
                    that.hs300BarMaker(type);
                })
            }
            else {
                params = {
                    stock: this.nowChosenStock,
                    start: this.hk50Start,
                    end: this.hk50End,
                    method: "growth",
                    top: this.hk50Top,
                    sort: this.hk50Sort,
                    area: "hk50"
                }

                this.$axios.get("/community/kline", {
//                start=2019-1-1&end=2020-6-1&method=growth&top=10&sort=1
                    params: params
                }).then(function (res) {
                    that.hk50DataList = [];
                    that.hk50DataWithSignList = [];
                    that.hk50NameList = [];
                    that.hk50StockList = [];
                    [...Array(res.data.length).keys()].forEach(function (data) {
    //                    window.console.log(res.data[data])
                        that.hk50DataList.push(parseFloat(res.data[data]["rate_of_increase"]));
                        that.hk50DataWithSignList.push(res.data[data]["rate_of_increase"] + "%");
    //                    that.rateList.push(res.data[data]["rate_of_increase"])
                        that.hk50NameList.push(res.data[data]["name"]);
                        that.hk50StockList.push({
                            "value": res.data[data]["stock"]
                        });

    //                    that.priceList.push(res.data[data]["start_price"] + "-" + res.data[data]["end_price"])
                    });
                    that.$forceUpdate();
    //                window.console.log(that.dataList);
                    that.hk50BarMaker(type);
                })
            }



        },
        setStartDate (event) {
//            window.console.log(event);
            if (event.split("|")[1] == "start") {
                if (event.split("|")[0] == "hs300") {
                    this.hs300Start = event.split("|")[2];
                }
                else {
                    this.hk50Start = event.split("|")[2];
                }
            }
            else {
                if (event.split("|")[0] == "hs300") {
                    this.hs300End = event.split("|")[2];
                }
                else {
                    this.hk50End = event.split("|")[2];
                }
            }
        },
        getNowChosenStockKlineData () {
            const that = this;
            this.$axios.get("/community/kline", {
                params: {
                    stock: this.nowChosenStock,
                    start: this.hs300Start,
                    end: this.hs300End,
                    method: "daily"
                }
            }).then(function (res) {
                that.data = res.data.data;
                that.days = res.data.days;
                that.klineMaker();
            })
        },
        hs300BarMaker() {
            let bar = this.$echarts.init(document.getElementById("hs300_bar"))
            window.console.log(bar)
            const that = this;
            const option = {
                tooltip: {
                    trigger: 'axis',
//                    axisPointer: {
//                        type: 'shadow'
//                    }
                },
                grid: [
                    {
                        top: 50,
                        bottom: 200,
                        left: 60,
                        right: 0,
                        z: 5
                    },
                    {
                        height: 60,
                        bottom: 170,
                        left: 60,
                        right: 0,
                        z: 5
                    }
                ],
                xAxis: [{
                    type: 'category',
                    data: that.hs300NameList,
                    gridIndex: 0,
                    axisLabel: {
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#e7e7e7'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#e7e7e7'
                        }
                    },
                    zlevel: 2
                }, {
                    type: 'category',
                    data: that.hs300StockList,
                    gridIndex: 1,
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    zlevel: 1
                }],
                yAxis: [{
                    type: 'value',
                    name: '增长率',
                    yAxisIndex: 0,
                    gridIndex: 0,
                    axisLabel: {
                        color: '#333',
                        formatter: '{value} %'
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    }
                },{
                    type: 'value',
                    yAxisIndex: 1,
                    gridIndex: 1,
                    axisLabel: {
                        show: false
                    },
                    axisLine: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    }
                }],
                series: [{
                    data: that.hs300DataList,
                    type: 'bar',
                    label: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: '#555'
                        },
//                        formatter: '{value} %'
                    },
                    itemStyle: {
                        normal: {
                            color: (params) => {
                                let colors = ['#4150d8', '#28bf7e', '#ed7c2f', '#f2a93b', '#f9cf36', '#4a5bdc', '#4cd698', '#f4914e', '#fcb75b', '#ffe180', '#b6c2ff', '#96edc1']
                                return colors[params.dataIndex]
                            }
                        }
                    },
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                },
//                {
//                    data: this.rateList,
//                    type: 'bar',
//                    label: {
//                        show: true,
//                        position: 'top',
//                        textStyle: {
//                            color: '#555'
//                        }
//                    },
//                    itemStyle: {
//                        normal: {
//                            color: (params) => {
//                                let colors = ['#4150d8', '#28bf7e', '#ed7c2f', '#f2a93b', '#f9cf36', '#4a5bdc', '#4cd698', '#f4914e', '#fcb75b', '#ffe180', '#b6c2ff', '#96edc1']
//                                return colors[params.dataIndex]
//                            }
//                        }
//                    },
//                    xAxisIndex: 1,
//                    yAxisIndex: 1,
//                },
                ]
            }

            bar.on('click', function (params) {
//                window.console.log(that.stockList)
                const dataIndex = params.dataIndex;

                let stock = that.hs300StockList[dataIndex].value;
                if (stock.substr(0, 1) == "6") {
                    stock = "SH" + stock
                }
                else {
                    stock = "SZ" + stock
                }

                window.open("https://www.gjscience.cn/stock-info/" + stock)
//                window.console.log(stock)
            })
            bar.setOption(option)
        },
        hk50BarMaker() {
            let bar = this.$echarts.init(document.getElementById("hk50_bar"))
            window.console.log(bar)
            const that = this;
            const option = {
                tooltip: {
                    trigger: 'axis',
//                    axisPointer: {
//                        type: 'shadow'
//                    }
                },
                grid: [
                    {
                        top: 50,
                        bottom: 200,
                        left: 60,
                        right: 0,
                        z: 5
                    },
                    {
                        height: 60,
                        bottom: 170,
                        left: 60,
                        right: 0,
                        z: 5
                    }
                ],
                xAxis: [{
                    type: 'category',
                    data: that.hk50NameList,
                    gridIndex: 0,
                    axisLabel: {
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#e7e7e7'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#e7e7e7'
                        }
                    },
                    zlevel: 2
                }, {
                    type: 'category',
                    data: that.hk50StockList,
                    gridIndex: 1,
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    zlevel: 1
                }],
                yAxis: [{
                    type: 'value',
                    name: '增长率',
                    yAxisIndex: 0,
                    gridIndex: 0,
                    axisLabel: {
                        color: '#333',
                        formatter: '{value} %'
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    },
                    axisTick: {
                        lineStyle: {
                            color: '#ccc'
                        }
                    }
                },{
                    type: 'value',
                    yAxisIndex: 1,
                    gridIndex: 1,
                    axisLabel: {
                        show: false
                    },
                    axisLine: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    }
                }],
                series: [{
                    data: that.hk50DataList,
                    type: 'bar',
                    label: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: '#555'
                        },
//                        formatter: '{value} %'
                    },
                    itemStyle: {
                        normal: {
                            color: (params) => {
                                let colors = ['#4150d8', '#28bf7e', '#ed7c2f', '#f2a93b', '#f9cf36', '#4a5bdc', '#4cd698', '#f4914e', '#fcb75b', '#ffe180', '#b6c2ff', '#96edc1']
                                return colors[params.dataIndex]
                            }
                        }
                    },
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                },
//                {
//                    data: this.rateList,
//                    type: 'bar',
//                    label: {
//                        show: true,
//                        position: 'top',
//                        textStyle: {
//                            color: '#555'
//                        }
//                    },
//                    itemStyle: {
//                        normal: {
//                            color: (params) => {
//                                let colors = ['#4150d8', '#28bf7e', '#ed7c2f', '#f2a93b', '#f9cf36', '#4a5bdc', '#4cd698', '#f4914e', '#fcb75b', '#ffe180', '#b6c2ff', '#96edc1']
//                                return colors[params.dataIndex]
//                            }
//                        }
//                    },
//                    xAxisIndex: 1,
//                    yAxisIndex: 1,
//                },
                ]
            }

            bar.on('click', function (params) {
//                window.console.log(that.stockList)
                const dataIndex = params.dataIndex;

                let stock = that.hk50StockList[dataIndex].value;
                stock = "HK" + stock

                window.open("https://www.gjscience.cn/stock-info/" + stock)
//                window.console.log(stock)
            })
            bar.setOption(option)
        },
        klineMaker() {
            let kline = this.$echarts.init(document.getElementById('kline'))

            const option = {
                backgroundColor: "rgba(0, 0, 0, 0)",
//                legend: {
//                    data: ['日K'],
//                    inactiveColor: '#777',
//                    textStyle: {
//                        color: '#fff'
//                    }
//                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        animation: false,
                        type: 'cross',
                        lineStyle: {
                            color: "rgba(110, 110, 110, 0.6)",
                            width: 1,
                            opacity: 1
                        }
                    }
                },
                xAxis: {
                    type: 'category',
                    data: this.days,
                    axisLine: { lineStyle: { color: "rgba(110, 110, 110, 0.6)" } },
                    axisTick: {
                        show: true,
                        inside: true
                    },
                },
                yAxis: {
                    scale: true,
                    axisLine: { lineStyle: { color: "rgba(110, 110, 110, 0.6)" } },
                    splitLine: { show: false },
                    axisTick: {
                        show: true,
                        inside: true
                    },
                    axisLabel:{
                        interval: 0,
                        rotate:0
                    }
                },
                grid: {
                    bottom: 90
                },
//                dataZoom: [{
//                    textStyle: {
//                        color: '#8392A5'
//                    },
//                    dataZoomIndex: 100,
//                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
//                    handleSize: '100%',
//                    dataBackground: {
//                        areaStyle: {
//                            color: '#8392A5'
//                        },
//                        lineStyle: {
//                            opacity: 0.8,
//                            color: '#8392A5'
//                        }
//                    },
//                    handleStyle: {
//                        color: '#fff',
//                        shadowBlur: 3,
//                        shadowColor: 'rgba(0, 0, 0, 0.6)',
//                        shadowOffsetX: 2,
//                        shadowOffsetY: 2
//                    }
//                }, {
//                    type: 'inside'
//                }],
                animation: false,
                series: [
                    {
                        type: 'candlestick',
                        name: '日K',
                        data: this.data,
                        itemStyle: {
                            color: '#FD1050',
                            color0: '#0CF49B',
                            borderColor: '#FD1050',
                            borderColor0: '#0CF49B'
                        }
                    },

                ]
            }

            kline.setOption(option);

        }
    },
    mounted() {
//        this.getNowChosenStockKlineData();
        this.startDraw("hs300");
        this.startDraw("hk50");
    }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .page-container {
        /*position: relative;*/
        min-height: 100vh;
        min-width: 100vw;
        display: flex;
        display: -webkit-flex;
        flex-direction: column;
        overflow: hidden;
        background-image: url("../assets/index.jpg");
    }

    .top-holder {
        width: 100vw;
        min-height: 6vh;
        display: flex;
        display: -webkit-flex;
        justify-content: center;
        /*border-bottom: 1px solid #f7f7fa;*/

        /*background-color: red;*/
    }

    .top-content {
        min-width: 100vw;
        /*background-color: yellow;*/
        display: flex;
        display: -webkit-flex;
        flex-wrap: wrap-reverse;
        align-content: space-between;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    .icon-box {
        width: 150px;
        /*background-color: pink;*/
    }

    .icon-box img {
        width: 130px;
    }

    .title-box {
        min-width: 100px;
        width: 200px;
        height: 30px;
        font-size: 150%;
        font-weight: 600;
        text-align: left;
    }

    .btn-box {
        min-width: 300px;
        height: 30px;
        width: 600px;
        display: flex;
        display: -webkit-flex;
        justify-content: flex-end;
        align-items: flex-end;
        flex-direction: row;
        flex-wrap: wrap;
        flex-grow: 1;

        /*background-color: red;*/
    }

    .btn {
        width: 150px;
        /*height: auto;*/
        height: 30px;
        line-height: 30px;
        cursor: pointer;
        /*background-color: pink;*/
    }

    .search-box {
        min-width: 300px;
        min-height: 32px;
        width: 50vw;
        height: 60px;
        /*background-color: red;*/
        display: flex;
        display: -webkit-flex;
        justify-content: center;
        align-items: center;
        background-color: #f7f7fa;
        border-radius: 8px;
        margin-top: 30vh;
    }

    .search-box input {
        min-width: 250px;
        min-height: 25px;
        width: 45vw;
        height: 60px;
        border: none;
        background-color: #f7f7fa;
        outline: none;
        color: #a6a9b6;
        font-size: 150%;
    }

    .search-box img {
        width: 20px;
        height: 20px;
    }

    .center-holder {
        width: 100vw;
        min-height: 93vh;
        /*min-height: 93vh;*/
        display: flex;
        display: -webkit-flex;
        justify-content: center;

        /*background-color: green;*/
    }

    .center-content {
        min-width: 60vw;
        min-height: 93vh;
        display: flex;
        display: -webkit-flex;
        /*overflow: hidden;*/
        /*flex-wrap: wrap;*/
        position: relative;
        /*justify-content: center;*/
        align-items: center;
        flex-direction: column;
    }

    .content-box {
        /*flex-grow: 1;*/
        min-width: 320px;
        /*min-height: 300px;*/
        width: 100vw;
        /*height: 60vh;*/
        margin-top: 50px;
        background-color: white;
        display: flex;
        display: -webkit-flex;
        /*justify-content: center;*/
        align-items: center;
        flex-direction: column;
    }

    .content-block {
        min-width: 300px;
        min-height: 300px;
        width: 80vw;
        height: 600px;
        margin-top: 50px;
        display: flex;
        display: -webkit-flex;
        flex-direction: column;
        /*background-color: red;*/
    }

    .block-title {
        width: 100%;
        height: 50px;
        /*background-color: red;*/
        display: flex;
        display: -webkit-flex;
        flex-direction: row;
        align-items: baseline;
        position: relative;
    }

    #kline {
        width: 25rem;
        min-width: 20rem;
        height: 300px;
    }

    .sort-box {
        width: 120px;
        height: 28px;
        line-height: 25px;
        border: 1px solid #ebecf1;
        border-radius: 4px;
        position: relative;
        /*top: -3px;*/
        font-size: 102%;
        outline: none;
    }

    .sort-box option {
        outline: none;
    }

    .go-box {
        width: 120px;
        height: 26px;
        /*line-height: 25px;*/
        border: 1px solid #ebecf1;
        border-radius: 4px;
        position: relative;
        top: -2px;
        line-height: 27px;
    }

    .block-center {
        width: 100%;
        height: 100%;
    }

    .bar {
        width: 100%;
        height: 600px;
        /*padding-left: 3%;*/
        z-index: 4;
        /*margin-top: 300px;*/
    }

    .bar>div {
        z-index: 3;
    }

    .bar>div>canvas {
        z-index: 3;
    }

    .calendar {
        z-index: 9999;
    }
</style>
