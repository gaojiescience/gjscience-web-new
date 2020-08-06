<template>
  <div class="canvas-holder" id="timeLineCanvas">

  </div>
</template>

<script>
export default {
  name: 'TimeLime',
  components: {

  },
  props: {
    fullStock: {
      type: String,
//      default: 'hello world'
    },
    isIndex: {
      type: String,
    },
  },
  data () {
    return {
      timeLineData: [],
      timeLineDateData: [],
      gridData0: [],
      gridData1: [],
      VOLUME_COLOR: []
    }
  },

  methods: {
    getDateData: function () {
//      window.console.log(this.fullStock);
      const market = this.fullStock.split("-")[0];
      const startTimeStamp = new Date();

      const marketToTimestamp = {
        "sh": [9, 30, 0, 0, 120, 13, 0, 0, 0, 120],
        "sz": [9, 30, 0, 0, 120, 13, 0, 0, 0, 120],
        "hk": [9, 30, 0, 0, 149, 13, 0, 0, 0, 179],
        "us": [9, 30, 0, 0, 149, 12, 0, 0, 0, 239],
        "uszs": [9, 30, 0, 0, 149, 12, 0, 0, 0, 239],
        "shzs": [9, 30, 0, 0, 120, 13, 0, 0, 0, 120],
        "szzs": [9, 30, 0, 0, 120, 13, 0, 0, 0, 120],
        "hkzs": [9, 30, 0, 0, 149, 13, 0, 0, 0, 179],
      };
      startTimeStamp.setHours(marketToTimestamp[market][0]);
      startTimeStamp.setMinutes(marketToTimestamp[market][1]);
      startTimeStamp.setSeconds(marketToTimestamp[market][2]);
      startTimeStamp.setMilliseconds(marketToTimestamp[market][3]);
//      window.console.log(startTimeStamp);
      let dateList = [startTimeStamp.toLocaleString().split("午")[1].split(":00")[0]];
      for (let index in [...new Array(marketToTimestamp[market][4])]) {
//        window.console.log(index);
        startTimeStamp.setMinutes(startTimeStamp.getMinutes() + 1);
        dateList.push(startTimeStamp.toLocaleString().split("午")[1].split(":00")[0])
      }

      startTimeStamp.setHours(marketToTimestamp[market][5]);
      startTimeStamp.setMinutes(marketToTimestamp[market][6]);
      startTimeStamp.setSeconds(marketToTimestamp[market][7]);
      dateList.push(startTimeStamp.toLocaleString().split("午")[1].split(":00")[0]);
      for (let index in [...new Array(marketToTimestamp[market][9])]) {
//        window.console.log(index);
        startTimeStamp.setMinutes(startTimeStamp.getMinutes() + 1);
        dateList.push(startTimeStamp.toLocaleString().split("午")[1].split(":00")[0])
      }

      this.timeLineDateData = dateList;
//      window.console.log(this.timeLineDateData.slice(0, 6));
//      this.gridData0 = dateList;
//      this.gridData1 = dateList;
    },
    getTimeLimeData: function () {
      const that = this;
      const startTimeStamp = new Date();
      startTimeStamp.setHours(9);
      startTimeStamp.setMinutes(0);
      startTimeStamp.setSeconds(0);
//      window.console.log(this.getDateData("sh"));
      const urlDict = {
        "sh": "https://www.laohu8.com/proxy/stock/astock/stock_info/time_trend/day/" + this.fullStock.split("-")[1] + "?beginTime=" + startTimeStamp.valueOf(),
        "sz": "https://www.laohu8.com/proxy/stock/astock/stock_info/time_trend/day/" + this.fullStock.split("-")[1] + "?beginTime=" + startTimeStamp.valueOf(),
        "hk": "https://www.laohu8.com/proxy/stock/hkstock/stock_info/time_trend/day/" + this.fullStock.split("-")[1].toUpperCase() + "?manualRefresh=true",
        "us": "https://www.laohu8.com/proxy/stock/stock_info/time_trend/day/" + this.fullStock.split("-")[1].split(".")[0].toUpperCase(),
        "uszs": "https://www.laohu8.com/proxy/stock/stock_info/time_trend/day/." + this.fullStock.split("-")[1].split(".")[0].toUpperCase(),
        "shzs": "https://www.laohu8.com/proxy/stock/astock/stock_info/time_trend/day/" + this.fullStock.split("-")[1] + "?beginTime=" + startTimeStamp.valueOf(),
        "szzs": "https://www.laohu8.com/proxy/stock/astock/stock_info/time_trend/day/" + this.fullStock.split("-")[1] + "?beginTime=" + startTimeStamp.valueOf(),
        "hkzs": "https://www.laohu8.com/proxy/stock/hkstock/stock_info/time_trend/day/" + this.fullStock.split("-")[1].toUpperCase() + "?manualRefresh=true",

      };
//      "https://www.laohu8.com/proxy/stock/stock_info/time_trend/day/.IXIC"
//      "https://www.laohu8.com/proxy/stock/hkstock/stock_info/time_trend/day/HSI?manualRefresh=true"
      let stockUrl = urlDict[this.fullStock.split("-")[0]];
      let indexUrl = urlDict[this.fullStock.split("-")[0]+"zs"];
      const targetUrl = this.isIndex == "ZS" && this.fullStock.split("-")[0] == "us" ? indexUrl : stockUrl;
      window.console.log(urlDict[targetUrl]);
//      const targetUrl =
//      try{
        this.$axios.get(targetUrl, {}).then(function (res) {
//          window.console.log(res);
          that.timeLineData = res;
          that.preClose = that.timeLineData.data.preClose;
          that.initData();
          that.timeLineMaker(that);
  //        res.data.items.pop();

//          if (res.data.ret == 30001) {
//            window.console.log(res);
//            const that2 = that;
//            that.$axios.get(urlDict[(that.fullStock.split("-")[0])], {}).then(function (res) {
//              window.console.log(res);
//              that2.timeLineData = res;
//              that2.preClose = that.timeLineData.data.preClose;
//              that2.initData();
//              that2.timeLineMaker(that);
//
//            })
//          }
//          else {
////            window.console.log(898989);
//            that.timeLineData = res;
//            that.preClose = that.timeLineData.data.preClose;
//            that.initData();
//            that.timeLineMaker(that);
//          }
        });

    },
    initData: function () {
      this.timeLineDateData = [];
      this.gridData0 = [];
      this.gridData1 = [];
      this.VOLUME_COLOR = [];
//      window.console.log(111)
      this.getDateData();
//      window.console.log(222)
      for (let index in this.timeLineData.data.items) {
        this.UP_COLOR = "#E24528";
        this.DOWN_COLOR = "#009933";
        this.NORMAL_COLOR = "#33353C";

        this.gridData0.push(this.timeLineData.data.items[index].price);
        this.gridData1.push(this.timeLineData.data.items[index].volume);

        if (index >0) {
          this.VOLUME_COLOR.push(this.timeLineData.data.items[index].price > this.timeLineData.data.items[index-1].price ? this.UP_COLOR : this.DOWN_COLOR)
        }
        else {
          this.VOLUME_COLOR.push(this.timeLineData.data.items[index].price > this.preClose ? this.UP_COLOR : this.DOWN_COLOR)
        }
      }
      this.priceMax = Math.max(...this.gridData0);
      this.priceMin = Math.min(...this.gridData0);

      this.volumeMax = Math.max(...this.gridData1);
      this.volumeMin = Math.min(...this.gridData1);

      if((this.preClose - this.priceMax) * -1 > (this.preClose - this.priceMin)){
          this.priceMin = (this.preClose - ((this.preClose - this.priceMax)* -1));
      }else{
          this.priceMax =(this.preClose + (this.preClose - this.priceMin));
      }

      this.priceInterval = (this.priceMax - this.preClose) / 4;
      this.volumeInterval = this.volumeMax / 2;


//      window.console.log(this.VOLUME_COLOR);
//      window.console.log(this.gridData1);
    },
    timeLineMaker: function (that) {
      const chart = this.$echarts.init(document.getElementById('timeLineCanvas'));
//      window.console.log(1);
      const option = {
        grid:[
            // 第一个grid
          {
            top:10,// 图表的外边距
            height:230,// 图表的高度
            width:'96%',//因为是左右各一个图表，使用百分比的方式显得更方便，
            left: "2%"
          },
          // 第二个grid，第二个图表是在第一个图表的下方，所以要把它定位到底部
          {
            top:260,//设置上方的外边距是第一个图表的高度再加10，使用top是方便我们调整下方grid的高度
            width:'96%',// 宽度与第一个图表一个大
            height:100,
            left: "2%"
          }
        ],
        // 多个图表则会存在对个x轴y轴，所以这里的配置我们也换成数组的方式
        // x轴配置，
        xAxis:[
          // 第一个grid的x轴属性
          {
              // 告诉echarts，这个第一个grid的x轴
              gridIndex:0,
              type: 'category',
              // x轴显示的数据
              data: this.timeLineDateData,
              show: false,
              boundaryGap:false,
              // x轴的刻度
              axisTick:{show:false},
              // x轴的刻度值
              axisLabel:{show:false},
              axisPointer:{
                show:true,
                label:{
                    show:false
                }
              }
          },
          // 第二个grid的x轴属性
          {
              // 告诉echarts，这个第一个grid的x轴
              gridIndex:1,
              type: 'category',
              // x轴显示的数据
              data: this.timeLineDateData,
              boundaryGap:false,
              // x轴的刻度
              axisTick:{show:false},
              spritNumber: 5,
              // x轴的刻度值
//              axisLabel:{show:false},
              axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
//                fontSize:10,
//                margin:-44,
//                padding:2,
//                shadowBlur:0,
                color:"black",
                backgroundColor: "#f6f6f6",
//                formatter:function(data){
//                  return data.value.toFixed(2);
//                }
              },
            }
          },
//          {
//              // 告诉echarts，这个第一个grid的x轴
//            gridIndex:1,
//            type: 'category',
//            // x轴显示的数据
//            data: [1, 2, 3],
//            show: true,
//            position: 'bottom',
////            axisTick:{show:false},
//              // x轴的刻度值
////            axisLabel:{show:false},
//          },
        ],
        // y轴配置
        yAxis: [
          // 第一个grid的y轴属性
          {
            axisTick:{show:false},
            gridIndex:0,
            type: 'value',
            min: this.priceMax,
            max: this.priceMin,
            interval: this.priceInterval,
            splitNumber: 9,
            axisLabel:{
              fontSize:10,
              margin:0,
              // y轴的数值向内显示
              align:"left",
              formatter: function (value, index) {
                  return value.toFixed(2);
              },
              color: function (value, index) {

                // 中间基准线的数值为黑色
                if(parseFloat(value).toFixed(2) == that.preClose){
                    return that.NORMAL_COLOR;
                }

                // 上涨区域的数字为红色
                if(value > that.preClose){
                    return that.UP_COLOR;
                }

                // 下方下跌的数值为绿色
                if(value < that.preClose){
                    return that.DOWN_COLOR;
                }

              }
            },
            axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
//                fontSize:10,
//                margin:-44,
//                padding:2,
//                shadowBlur:0,
                color:"black",
                backgroundColor: "#f6f6f6",
                formatter:function(data){
                  return data.value.toFixed(2);
                }
              },
            }
          },

          // 第二个grid的y轴属性
          {
            gridIndex:1,
            type: 'value',
            axisTick:{show:false},
            splitNumber:3,
            interval:this.volumeInterval,
            max:this.volumeMax,
            min:0,
            splitLine:{
              lineStyle:{
                color:"#ECEEF2",
                // 设置线条喂风格为虚线
//                type:"dashed"
              }
            },
            axisLine:{
              lineStyle:{
                color:"#ECEEF2"
              }
            },
            axisLabel:{
                //设置显示坐标轴的数值为不显示
              show:false
            },
            axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
//                fontSize:10,
//                margin:-44,
//                padding:2,
//                shadowBlur:0,
                color:"black",
                backgroundColor: "#f6f6f6",
                formatter:function(data){
                  return parseFloat(data.value / 1000000).toFixed(2)+"万手";
                }
              },
            }
//            axisPointer: {
//              show:true,
//              type:"line",
//              shadowStyle: {
//                color: "#f6f6f6"
//              },
//              label:{
//                show:true,
////                fontSize:10,
////                padding:2,
////                shadowBlur:0,
//                color:"black",
//                backgroundColor: "#f6f6f6",
//                formatter:function(data){
//                  if(data.value > 1000000){
//                      return parseFloat(data.value / 1000000).toFixed(2)+"万手";
//                  }
//                  return data.value;
//                }
//              },
//            }
          },
          {
            axisTick:{show:false},
            gridIndex:0,
            type: 'value',
            min: this.priceMax,
            max: this.priceMin,
            interval: this.priceInterval,
            splitNumber: 9,
            axisLabel:{
              fontSize:10,
              margin:0,
              // y轴的数值向内显示
              align:"right",
              formatter: function (value, index) {
                  return ((value-that.preClose)/that.preClose*100).toFixed(2) + "%";
              },
              color: function (value, index) {

                // 中间基准线的数值为黑色
                if(parseFloat(value).toFixed(2) == that.preClose){
                    return that.NORMAL_COLOR;
                }

                // 上涨区域的数字为红色
                if(value > that.preClose){
                    return that.UP_COLOR;
                }

                // 下方下跌的数值为绿色
                if(value < that.preClose){
                    return that.DOWN_COLOR;
                }

              }
            },
            axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
//                fontSize:10,
//                margin:-44,
//                padding:2,
//                shadowBlur:0,
                color:"black",
                backgroundColor: "#f6f6f6",
                formatter:function(data){
                  return ((data.value-that.preClose)/that.preClose*100).toFixed(2) + "%"
                }
              },
            }
//            axisPointer:{
//              show:true,
//              type:"line",
//              label:{
//                show:true,
////                fontSize:10,
////                margin:-44,
////                padding:2,
////                shadowBlur:0,
////                color:"#33353C",
//                formatter:function(data){
//                  return ((data.value-that.preClose)/that.preClose*100).toFixed(2) + "%"
//                }
//              },
//            }
          },
        ],
        // 数据可以通过xAxisIndex，yAxisIndex属性，来指定是哪个grid的数据
        series: [
          {
            xAxisIndex:0,
            yAxisIndex:0,
            data: this.gridData0,
            type: 'line',
            smooth:true,
            // 是否显示折线上的圆点
            symbol:'none',
            // 线条颜色
            lineStyle:{
                color:"#0983F8",
                width: 1
            },
          },
          {
            xAxisIndex:1,
            yAxisIndex:1,
            data: this.gridData1,
            type: 'bar',
            itemStyle:{
              normal: {
                color: function (params) {
                  return that.VOLUME_COLOR[params.dataIndex];
                }
              }
            }

          },
          {
            xAxisIndex:0,
            yAxisIndex:2,
            data: this.gridData0,
            type: 'line',
            smooth:true,
            // 是否显示折线上的圆点
            symbol:'none',
            // 线条颜色
            lineStyle:{
                color:"#0983F8",
                width: 1
            },

          },
        ],
        axisPointer:{
          show:true,
          // 配置线条风格为虚线风格
          lineStyle:{
            type:'dashed'
          },
          link:[
            {
                xAxisIndex:[0,1],
            },
//            {
//                xAxisIndex:[2,3],
//            },{
//                yAxisIndex:[0,2]
//            },{
//                yAxisIndex:[1,3]
//            }
          ]
        },
        tooltip:{
          trigger:'axis',
          position: function(point, params, dom, rect, size){
            const obj ={
                top:10
            };

            if(point[0] > size.viewSize[0] / 2){
                obj["left"] = 50;
            }else{
                obj["right"] = 50;
            }

            return obj;
          },
          formatter:function(params,ticket,callback){
            let html = '';
//            let currentPrice, currentVolume;
//            window.console.log(params);
            let index = params[0].dataIndex;
            let currentDate = that.timeLineDateData[index];
            let currentPrice = that.gridData0[index];
            let currentVolume = that.gridData1[index];
            let currentChange = currentPrice - that.preClose;
            let currentChg = ((currentChange / that.preClose) * 100).toFixed(2) + "%";
            let currentColor = currentChange > 0 ? that.UP_COLOR : that.DOWN_COLOR;

            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">时间</span><span class="value">'+ currentDate +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">最新</span><span class="value" style="color: ' + currentColor +'">'+ currentPrice +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">涨跌幅</span><span class="value" style="color: ' + currentColor +'">'+ currentChg + '</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">涨跌额</span><span class="value" style="color: ' + currentColor +'">'+ currentChange.toFixed(2) +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">成交量</span><span class="value">'+ (currentVolume / 1000000).toFixed(2) + '万' + '</span></div>';

            return html;
          },
          textStyle:{
              color:"#000"
          },
          borderWidth:1,
          borderColor:"#ECEEF2",
          backgroundColor:"rgba(255,255,255,0.9)",
          transitionDuration:0,
          axisPointer:{
              animation:false,
              type:"cross"
          }
        }
      };


      chart.setOption(option);
    }
  },
  mounted() {
//    window.console.log(this.rawStock)
    this.getTimeLimeData();
//    this.timeLineMaker();
    this.timer = setInterval(this.getTimeLimeData, 30000);

  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .canvas-holder {
    width:700px;
    height:390px;
  }

  .tooltips-item{
    display:flex;
    display:-webkit-flex;
    justify-content: space-between;
    color:red;
    /*color:#33333c;*/
    font-size:10px;
    width:120px;
  }

  .green{
    color:#009933;
  }

  .red{
    color:#E24528;
  }
</style>
