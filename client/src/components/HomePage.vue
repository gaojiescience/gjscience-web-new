<template>
  <div class="root" @mousemove="moveImage">
    <div :class="'page-header ' + headerBackground">
      <div class="header-left">
        <div class="icon-box" v-if="!isChangeHeader">
          <img src="../assets/logo.png"/>
        </div>
        <div class="icon-box" v-else>
          <img src="../assets/logo.png"/>
        </div>
      </div>
      <div :class="'header-right ' + (!isChangeHeader ? '' : 'dark-header')">
        <div class="link-box" @click="linkTo('market')">
          行情
        </div>
        <div class="link-box">
          产品
        </div>
        <div class="link-box">
          关于我们
        </div>
      </div>
    </div>
    <div class="page-center">
      <div class="banner-holder">
        <div class="content-holder">
          <div class="text-line">
            您的智能分析助手
          </div>
          <div class="text-line-2">
            提问&回答
          </div>
          <div class="button-line">
            <div class="go-button">
              立即体验
            </div>
          </div>
          <div class="search-line">
            <div class="search-box">
              <input class="search-input" placeholder="沪深300股票代码"/>
              <img src="../assets/search.png">
            </div>
          </div>
        </div>
      </div>
      <div class="info-holder">
        <div class="text-box">
          <header>
            <h2 :style="'transform: translate3d(' + titleLeft + ','  + titleTop + ',' + '0px )'">
              介绍
            </h2>
            <h1 :style="'transform: translate3d(' + textLeft + ','  + textTop + ',' + '0px )'">
              About
            </h1>
            <img src="../assets/company.png" :style="'transform: translate3d(' + imgLeft + ','  + imgTop + ',' + '0px )'"/>
          </header>
          <div class="info-content">
            <h3>
              2017
            </h3>
            <h3>
              深圳高街科技公司是高街集团在深圳的子公司
            </h3>
            <br>
            <span>
              深圳高街科技有限公司聘用了世界500强企业高管，资深科学家和金融专家，组成强大的团队，为客户提供最好的信息技术和人工智能应用。我们开发了享有专利的大数据和人工智能处理系统。同时我们也拥有强大的品牌运营能力。
            </span>
            <br>
            <br>
            <h3>
              2018
            </h3>
            <h3>
              高街科技落户深圳南山区软件产业基地
            </h3>
            <br>
            <span>
              高街科技与其他高科技企业一起入住南山区软件产业基地。
            </span>
          </div>
        </div>
        <div class="image-box">
          <img src="../assets/skyline.jpg"/>
        </div>
      </div>
      <div class="info-holder businesses-holder">

        <div class="image-box">
          <img src="../assets/businesses.jpg" class="businesses"/>
        </div>
        <div class="text-box">
          <header class="dark">
            <h2 :style="'transform: translate3d(' + titleLeft + ','  + titleTop + ',' + '0px )'">
              业务
            </h2>
            <h1 :style="'transform: translate3d(' + textLeft + ','  + textTop + ',' + '0px )'">
              Businesses
            </h1>
            <img src="../assets/businesses.png" :style="'transform: translate3d(' + imgLeft + ','  + imgTop + ',' + '0px )'"/>
          </header>
          <div class="info-content dark">
            <h3>
              信息技术服务
            </h3>
            <br>
            <span>
              高街科技有限公司的深圳办公室有强大的信息科学家和工程师团队。可以给客户提供一系列的信息技术服务：比如提供云服务器，手机APP开发， 微信小程序开发运营，系统集成服务，人工智能分析系统，和管理电商平台和微信公众号等等。
              <br>
我们有领先的自己开发的人工智能系统。同时拥有多项中国专利和软著。我们的客户包括中小企和基金公司。
            </span>
            <br>
            <br>
            <h3>
              品牌运营服务
            </h3>
            <br>
            <span>
              品牌运营极为重要。 高街科技有着丰富的互联网宣发能力。同时我们与多家传媒和广告公司合作。
              <br>
我们在微博，头条，微信公众号和抖音上都管理着宣发平台。我们独有的人工智能分析平台能够最优地选择广告投放平台。
            </span>
          </div>
        </div>
      </div>
      <div class="info-holder">
        <div class="text-box">
          <header>
            <h2 :style="'transform: translate3d(' + titleLeft + ','  + titleTop + ',' + '0px )'">
              团队
            </h2>
            <h1 :style="'transform: translate3d(' + textLeft + ','  + textTop + ',' + '0px )'">
              Team
            </h1>
            <img src="../assets/intro.png" :style="'transform: translate3d(' + imgLeft + ','  + imgTop + ',' + '0px )'"/>
          </header>
          <div class="info-content">
            <span>
              我们的管理团队由优秀的企业高管及有成就的科学家/工程师组成。团队主要基于深圳，香港和北京。
              <br>
              高街科技的团队有着丰富的世界500强企业管理和投资银行的金融能力。团队成员曾在Motorola 及美国通用电气集团等知名机构担任高管职务。
              <br>
我们欢迎有志上述行业的人才与我们联络。
            </span>
          </div>
        </div>
        <div class="image-box">
          <img src="../assets/team.jpg"/>
        </div>
      </div>
      <div class="info-holder businesses-holder">
        <div class="image-box">
          <img src="../assets/join.jpg" class="us"/>
        </div>
        <div class="text-box dark">
          <header>
            <h2 :style="'transform: translate3d(' + titleLeft + ','  + titleTop + ',' + '0px )'">
              加入
            </h2>
            <h1 :style="'transform: translate3d(' + textLeft + ','  + textTop + ',' + '0px )'">
              Join Us
            </h1>
            <img src="../assets/us.png" :style="'transform: translate3d(' + imgLeft + ','  + imgTop + ',' + '0px )'"/>
          </header>
          <div class="info-content">
            <h3>
              我们的管理团队由优秀的企业高管，投资银行家，及有成就的科学家/工程师组成。
            <br>
我们欢迎有志上述行业的人才与我们联络。请将您的简历发到以下联络我们的地址。我们欢迎科技人才兼职参与我们工作！
            </h3>
            <h3>
              <a href="mailto:info@GJScience.com">发送邮件 mailto:info@GJScience.com</a>
            </h3>
          </div>
        </div>
      </div>
    </div>
    <div class="page-footer">
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import Footer from "./Footer.vue"
export default {
  name: 'HomePage',
  components: {
    Footer
  },
  data () {
    return {
      imgLeft: "-70px",
      imgTop: "-100px",
      textLeft: "0px",
      textTop: "-20px",
      titleLeft: "0px",
      titleTop: "0px",
      isChangeHeader: false,
      headerBackground: ''
    }
  },
  methods: {
    linkTo: function (event) {
//      window.console.log(event);
//      this.$router.push("/" + event);

      const newPage = this.$router.resolve({
        name: "MarketPage",
      });
      window.open(newPage.href,'_blank')
    },
    moveImage: function (event) {
      this.imgLeft = -(30 + event.clientX / 50) + "px";
      this.imgTop = -(70 + event.clientY / 30)+ "px";
      this.textLeft = (event.clientX / 70) + "px";
      this.textTop = (event.clientY / 50)+ "px";
      this.titleLeft = (event.clientX / 120) + "px";
      this.titleTop = (event.clientY / 80)+ "px";
//        window.console.log(event)
    },
    changeHeader: function () {
      let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
//      window.console.log(scrollTop);
      if (scrollTop <= 650) {
        this.headerBackground = '';
        this.isChangeHeader = false;
      }
      else if (scrollTop > 650 && scrollTop <= 1200) {
        this.isChangeHeader = false;
        this.headerBackground = 'blue-background';
      }
      else if (scrollTop > 1200 && scrollTop < 1800) {
        this.isChangeHeader = true;
        this.headerBackground = 'white-background';
      }
      else if (scrollTop > 1800) {
        this.headerBackground = 'blue-background';
        this.isChangeHeader = false;
      }
//      window.console.log(document.documentElement.scrollTop || document.body.scrollTop)
    }
  },
  mounted() {
    window.addEventListener('scroll', this.changeHeader)
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    display: flex;
    flex-direction: column;
  }

  .page-header {
    width: 100%;
    height: 7vh;
    /*background-color: red;*/
    position: fixed;
    top: 0;
    display: flex;
    flex-direction: row;
    z-index: 2;
  }

  .header-left {
    width: 30%;
    height: 100%;
    display: flex;
  }

  .icon-box {
    width: 170px;
    height: 100%;
    cursor: pointer;
  }

  .icon-box img {
    width: 130px;
    height: 80%;
    margin-top: 5%;
  }

  .header-right {
    width: 70%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
  }

  .link-box {
    width: 100px;
    height: 100%;
    line-height: 7vh;
    text-align: center;
    color: white;
    cursor: pointer;
  }

  .page-center {
    width: 100vw;
    min-height: 100vh;
    /*background-color: green;*/
    position: relative;
    z-index: 1;
    top: -7vh;
  }

  .page-footer {
    width: 100vw;
    height: 150px;
    margin-top: -7vh;
    /*background-color: pink;*/
  }

  .banner-holder {
    width: 100%;
    min-width: 32vw;
    height: 40vw;
    background-image: url("../assets/banner1.jpg");
    background-size: 100%;
    background-repeat: no-repeat;
    display: flex;
    justify-content: center;
  }

  .content-holder {
    width: 50%;
    min-width: 500px;
    height: 60%;
    margin-top: 15%;
    /*background-color: yellow;*/
    /*margin-left: 25%;*/
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .text-line {
    width: 100%;
    height: 15%;
    /*margin-top: 20%;*/
    text-align: left;
    font-size: 1.5rem;
    color: white;
    font-weight: 600;
    line-height: 100%;
  }

  .text-line-2 {
    width: 100%;
    height: 15%;
    line-height: 100%;
    /*margin-top: 10%;*/
    text-align: left;
    font-size: 2rem;
    color: white;
    font-weight: 600;
  }

  .button-line {
    width: 100%;
    height: 50px;
  }

  .go-button {
    width: 120px;
    height: 50px;
    border-radius: 5px;
    border: 2px solid white;
    line-height: 50px;
    color: white;
    font-size: 120%;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1vh;
  }

  .search-line {
    width: 100%;
    height: 7vh;
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
    margin-top: 5vh;
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

  .info-holder {
    width: 100vw;
    min-width: 1200px;
    height: 555px;
    background-color: #b5d7e0;
    display: flex;
    justify-content: center;
  }

  .businesses-holder {
    background-color: #f6f6f6 !important;
  }

  .text-box {
    width: 30%;
    min-width: 600px;
    height: 100%;
    color: white;
    box-sizing: content-box;
    padding: 5%;
  }

  header {
    text-align: left;
    width: 100%;
    height: 20%;
    /*margin-top: 10%;*/
  }

  header h1 {
    font-size: 300%;
  }

  header h2 {
    font-size: 150%;
  }

  header img {
    filter: blur(3px);
    position: relative;
  }

  .info-content {
    margin-top: 5%;
    text-align: left;
  }

  .image-box {
    width: 30%;
    min-width: 600px;
    height: 100%;
    padding: 5%;
  }

  .image-box img {
    width: 100%;
    height: 60%;
    /*margin-top: 20%;*/
  }

  .businesses {
    width: 100% !important;
    height: 80% !important;
    /*margin-top: 10% !important;*/
  }

  .dark {
    color: black;
  }

  .us {
    height: 80% !important;
  }

  .dark-header div {
    color: black;
  }

  .white-background {
    background-color: #f6f6f6 !important;
  }

  .blue-background {
    background-color: #b5d7e0 !important;
  }
</style>



// WEBPACK FOOTER //
// src/components/HomePage.vue