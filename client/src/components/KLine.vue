<template>
  <div class="canvas-holder" id="kLineCanvas">

  </div>
</template>

<script>
export default {
  name: 'KLime',
  components: {

  },
  props: {
    fullStock: {
      type: String,
//      default: 'hello world'
    },
    lineType: {
      type: String,
    },
    isIndex: {
      type: String,
    },
  },
  data () {
    return {
      startDateStr: "",
      startDate: "",
      endDate: "",
      ma5Data: [],
      ma10Data: [],
      ma20Data: [],
      endDateStr: "",
      stock: this.fullStock.split("-")[0] + this.fullStock.split("-")[1],
      kLineData: [],
      kLineDateData: [],
      kLineVolumeData: [],
      kLineVolumeColorData: [],
//      ["2005-1-1", "2005-12-31"], ["2006-1-1", "2006-12-31"], ["2007-1-1", "2007-12-31"], ["2008-1-1", "2008-12-31"], ["2009-1-1", "2009-12-31"], ["2010-1-1", "2010-12-31"],
//        ["2011-1-1", "2011-12-31"], ["2012-1-1", "2012-12-31"], ["2013-1-1", "2013-12-31"], ["2014-1-1", "2014-12-31"], ["2015-1-1", "2015-12-31"],
      yearsList: [
        ["2015-01-01", "2015-12-31"], ["2016-01-01", "2016-12-31"], ["2017-01-01", "2017-12-31"], ["2018-01-01", "2018-12-31"], ["2019-01-01", "2019-12-31"], ["2020-01-01", "2020-12-31"]
      ]
    }
  },

  methods: {
    initCanvas: function () {
      this.startDateStr = "";
      this.startDate = "";
      this.endDate = "";
      this.ma5Data = [];
      this.ma10Data = [];
      this.ma20Data = [];
      this.endDateStr = "";
//      this.stock = this.fullStock.split("-")[0] + this.fullStock.split("-")[1],
      this.kLineData = [];
      this.kLineDateData = [];
      this.kLineVolumeData = [];
      this.kLineVolumeColorData = [];
//      window.console.log(1)
//      this.getKLineData();
    },
    getKLineData: async function () {
      this.initCanvas();
      const that = this;
      const type = this.lineType.split("_")[1];

      const urlDict = {
        "sz": "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_" + type + "qfq&param=",
        "sh": "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_" + type + "qfq&param=",
        "hk": "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_" + type + "qfq&param=",
        "us": "http://web.ifzq.gtimg.cn/appstock/app/usfqkline/get?_var=kline_" + type + "qfq&param=",
        "uszs": "http://web.ifzq.gtimg.cn/appstock/app/usfqkline/get?_var=kline_" + type + "qfq&param=",
      };
//      "http://web.ifzq.gtimg.cn/appstock/app/usfqkline/get?_var=kline_weekqfq&param=us.IXIC,week,2014-01-01,2014-12-31,320,qfq&r=0.6179668098968216"
      for (let index in that.yearsList) {
        this.startDateStr = that.yearsList[index][0];
        this.endDateStr = that.yearsList[index][1];
        let targetUrl;
//        if (this.fullStock.split("-")[0] == "us") {
//          targetUrl = urlDict[this.fullStock.split("-")[0]] + this.fullStock.split("-")[0] + this.rawStock.toUpperCase() + ",day," + this.startDateStr + "," + this.endDateStr + ",320,qfq";
//        }
//        else {

        let stockUrl = urlDict[this.fullStock.split("-")[0]] + this.stock + "," + type + "," + this.startDateStr + "," + this.endDateStr + ",320,qfq";
        let indexUrl = urlDict[this.fullStock.split("-")[0]] + this.fullStock.split("-")[0] + "." + this.fullStock.split("-")[1].toUpperCase() + "," + type + "," + this.startDateStr + "," + this.endDateStr + ",320,qfq";
        targetUrl = this.isIndex == "ZS" && this.fullStock.split("-")[0] == "us" ? indexUrl : stockUrl;
        //        }
//        targetUrl = urlDict[this.fullStock.split("-")[0]] + this.stock.toUpperCase() + ",day," + this.startDateStr + "," + this.endDateStr + ",320,qfq";
//        window.console.log(targetUrl);
        await this.$axios.get(targetUrl, {}).then(function (res){
          window.console.log(targetUrl);
          window.console.log(JSON.parse(res.data.split('=')[1]));

          try {
          res = JSON.parse(res.data.split('=')[1]).data[that.stock]["qfq"+type] || JSON.parse(res.data.split('=')[1]).data[that.stock][type];
          }
          catch (e) {
            res = JSON.parse(res.data.split('=')[1]).data[that.fullStock.split("-")[0] + "." + that.fullStock.split("-")[1].toUpperCase()]["qfq"+type]
          }

          for (let index in res) {
            that.kLineDateData.push(res[index][0]);
            that.kLineData.push(res[index].slice(1, 5));
            that.kLineVolumeData.push(res[index].slice(5, 6)[0]);
            that.kLineVolumeColorData.push(res[index].slice(1, 5)[1] >= res[index].slice(1, 5)[0] ? "#E24528" : "#009933")
          }


        })
//        window.console.log(that.kLineDateData);
      }

      this.ma5Data = this.calculateMA(5);
      this.ma10Data = this.calculateMA(10);
      this.ma20Data = this.calculateMA(20);
      that.kLineMaker();
    },
    calculateMA: function (dayCount) {
      const result = [];
      for (let i in this.kLineDateData) {
        if (i < dayCount) {
            result.push("-");
            continue;
        }
        let sum = 0;
        for (let j in [...new Array(dayCount)]) {
          sum += parseFloat(this.kLineData[i - j][1]);
//          window.console.log(this.kLineData[i - j][1]);
        }
        result.push((sum / dayCount).toFixed(2));
      }
//      window.console.log(result);
      return result;
    },
    kLineMaker: function () {
      const chart = this.$echarts.init(document.getElementById('kLineCanvas'));
      const upColor = '#E24528';
      const upBorderColor = '#E24528';
      const downColor = '#009933';
      const downBorderColor = '#009933';
      const that = this;
      const option = {
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
            let date = '';
            let change = 0;
            let changeRate = 0;
            let volume = 0;
            let color = '';
            let ma5 = 0;
            let ma10 = 0;
            let ma20 = 0;
            let index = params[0].dataIndex;
//            let currentPrice, currentVolume;
//            window.console.log(params);
            date = params[0].name;
            color = params[0].color;
            change = index > 0 ? that.kLineData[index][1] - that.kLineData[index-1][1] : 0;
            changeRate = index > 0 ? ((change / that.kLineData[index-1][1])*100).toFixed(2) : 0;
            volume = that.kLineVolumeData[index];
            ma5 = that.ma5Data[index];
            ma10 = that.ma10Data[index];
            ma20 = that.ma20Data[index];


            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">时间</span><span class="value">'+ date +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">开盘</span><span class="value" style="color: ' + color +'">'+ parseFloat(that.kLineData[index][0]).toFixed(2) +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">收盘</span><span class="value" style="color: ' + color +'">'+ parseFloat(that.kLineData[index][1]).toFixed(2) + '</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">最高</span><span class="value" style="color: ' + color +'">'+ parseFloat(that.kLineData[index][2]).toFixed(2) +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">最低</span><span class="value" style="color: ' + color +'">'+ parseFloat(that.kLineData[index][3]).toFixed(2) +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">涨跌额</span><span class="value" style="color: ' + color +'">'+ change.toFixed(2) +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">涨跌幅</span><span class="value" style="color: ' + color +'">'+ changeRate + '%' +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">交易量</span><span class="value">'+ (volume / 10000).toFixed(2) + '万手' + '</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">MA5</span><span class="value" style="color: ' + color +'">'+ ma5 +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">MA10</span><span class="value" style="color: ' + color +'">'+ ma10 +'</span></div>';
            html += '<div class="tooltips-item" style="display:flex;display:-webkit-flex;justify-content: space-between;font-size: 80%;"><span class="name">MA20</span><span class="value" style="color: ' + color +'">'+ ma20 +'</span></div>';

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
        },
        grid: [
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
        dataZoom: [
          {
            xAxisIndex: [0, 1],
            type: 'inside',
            start: 95,
            end: 100
          },
        ],
        xAxis:[
          // 第一个grid的x轴属性
          {
              // 告诉echarts，这个第一个grid的x轴
              gridIndex:0,
              type: 'category',
              // x轴显示的数据
              data: this.kLineDateData,
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
              data: this.kLineDateData,
              boundaryGap:false,
              // x轴的刻度
              axisTick:{show:false},
              spritNumber: 5,
              // x轴的刻度值
              axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
                color:"black",
                backgroundColor: "#f6f6f6",
              },
            }
          },
        ],
        yAxis: [
          // 第一个grid的y轴属性
          {
            axisTick:{show:false},
            gridIndex:0,
            scale: true,
            type: 'value',
            splitNumber: 9,
            axisLabel:{
              fontSize:10,
              margin:0,
              // y轴的数值向内显示
              align:"left",
            },
            axisPointer:{
              show:true,
              type:"line",
              label:{
                show:true,
                color:"black",
                backgroundColor: "#f6f6f6",
              },
            }
          },

          // 第二个grid的y轴属性
          {
            gridIndex:1,
            type: 'value',
            axisTick:{show:false},
            splitNumber:3,
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
                color:"black",
                backgroundColor: "#f6f6f6",
              },
            }
          },

        ],
        series: [
          {
            xAxisIndex:0,
            yAxisIndex:0,
            data: this.kLineData,
            type: 'candlestick',
            smooth:true,
            // 是否显示折线上的圆点
            symbol:'none',
            // 线条颜色
            itemStyle: {
              color: upColor,
              color0: downColor,
              borderColor: upBorderColor,
              borderColor0: downBorderColor
            },
          },
          {
            xAxisIndex:1,
            yAxisIndex:1,
            data: this.kLineVolumeData,
            type: 'bar',
            itemStyle:{
              normal: {
                color: function (params) {
                  return that.kLineVolumeColorData[params.dataIndex];
                }
              }
            }
          },
          {
            name: 'MA5',
            type: 'line',
            data: that.ma5Data,
            smooth: true,
            symbol:'none',
            lineStyle: {
              opacity: 0.5,

            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: that.ma10Data,
            smooth: true,
            symbol:'none',
            lineStyle: {
              opacity: 0.5,

            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: that.ma20Data,
            smooth: true,
            symbol:'none',
            lineStyle: {
              opacity: 0.5,

            }
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
      };
      chart.setOption(option);
//      chart.on("datazoom", function (params) {
////        window.console.log(params);
//        const batch = parseInt(params.batch[0].start);
////        const opt = chart.getOption();
////        const index = opt.xAxis[0].data[parseInt(batch.start)];
//        if (batch == 0) {
//          that.startDate.setFullYear(that.startDate.getFullYear()-1);
//          const reg = new RegExp('/', "g");
//          that.startDateStr = that.startDate.toLocaleString().split(" ")[0].replace(reg, "-");
//          that.endDate.setFullYear(that.endDate.getFullYear()-1);
//          that.endDate.setMonth(11);
//          that.endDate.setDate(31);
//          that.endDateStr = that.endDate.toLocaleString().split(" ")[0].replace(reg, "-");
//          window.console.log(that.startDateStr);
//          window.console.log(that.endDateStr);
//          that.getKLineData();
//        }
//        window.console.log(batch)
////        window.console.log(opt.xAxis[0].data)
//      })
    }
  },
  mounted() {
//    this.initData();
    this.getKLineData();
//    window.console.log(1)
//    window.console.log(this.lineType)
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .canvas-holder {
    width:700px;
    height:390px;
  }


</style>



// WEBPACK FOOTER //
// src/components/KLine.vue