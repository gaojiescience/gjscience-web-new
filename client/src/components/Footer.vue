<template>
  <div class="footer">
    <div class="footer-content">
      <div class="footer-box">
        <div class="footer-about">
          <a class="footer-btn">
            关于我们
          </a>
          <a class="footer-btn">
            用户守则
          </a>
        </div>
        <div class="footer-line">
          Copyright 2019 高街科技(深圳)有限公司 版权所有 粤ICP备19073853号
        </div>
      </div>
      <div class="footer-box">
        <div class="footer-about-right">
          <a class="footer-btn-right">
            意见反馈、互联网违法和不良信息投诉
          </a>
          <a class="footer-btn-right">
            info@GJScience.com  联系电话  075526919025
          </a>
          <!--<a class="footer-btn">-->
            <!--用户守则-->
          <!--</a>-->
        </div>
        <div class="footer-line-right">
          Copyright 2019 高街科技(深圳)有限公司 版权所有 粤ICP备19073853号
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Footer',
  data () {
    return {

    }
  },
  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .footer {
    width: 100%;
    min-width: 1200px;
    height: 150px;
    background-color: #f7f7fa;
    display: flex;
    justify-content: center;
  }

  .footer-content {
    min-width: 1200px;
    height: 100%;
    justify-content: space-between;
    display: flex;
    /*background-color: red;*/
  }

  .footer-box {
    width: 50%;
    height: 100%;
    flex-direction: column;
  }

  .footer-about {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
    margin-top: 40px;
  }

  .footer-btn {
    /*background-color: red;*/
    display: inline-block;
    margin-right: 30px;
    height: 20px;
    line-height: 20px;
    cursor: pointer;
  }

  .footer-line {
    width: 90%;
    height: 50px;
    text-align: left;
    margin-top: -100px;
  }

  .footer-about-right {
    width: 100%;
    height: 100%;
    display: flex;
    /*justify-content: flex-end;*/
    margin-top: 40px;
    flex-direction: column;
  }

  .footer-btn-right {
    width: 100%;
    height: 40px;
    line-height: 40px;
    text-align: right;
  }
</style>
