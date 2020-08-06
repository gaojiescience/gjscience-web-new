<template>
  <div class="root">
    <div class="page-holder">
      <div class="header-holder">
        <div class="header-box">
          <img src="../assets/logo.png"/>
        </div>
        <!--<div class="header-box">-->
          <!--<span>注 册</span>-->
        <!--</div>-->
        <!--<div class="full-progress">-->
          <!--<div class="now-progress" :style="'width: ' + this.nowProgress + '%;'">-->

          <!--</div>-->
        <!--</div>-->



      </div>
      <div class="btn-line">
        <div :class="'btn ' + (nowChosenBtn == 'email' ? 'now-chosen-btn' : '')" v-on:click="chosenLoginType('email')">
          <span>邮箱登录</span>
        </div>
        <div :class="'btn ' + (nowChosenBtn == 'phone' ? 'now-chosen-btn' : '')" v-on:click="chosenLoginType('phone')">
          <span>手机登录</span>
        </div>
      </div>
      <div class="input-holder">
        <input placeholder="请输入邮箱地址" v-model="email" v-on:input="listenEmailChange">
      </div>
      <div class="tips" v-if="isShowEmailTips">
        {{ emailTips }}
      </div>
      <!--<div class="input-holder verification-input">-->
        <!--<input placeholder="请输入邮箱验证码" class="verification-input" v-model="verificationCode" v-on:input="listenVerificationCode">-->
        <!--<div :class="(isShowSendBtn ? 'able-btn' : 'ban-btn')" v-on:click="requestVerificationCode">{{ btnText }}</div>-->
        <!--&lt;!&ndash;<div v-if="isBanSendBtn" :class="'ban-btn ' + (isBanSendBtn ? 'gray-color' : '')">{{ btnText }}</div>&ndash;&gt;-->
      <!--</div>-->
      <!--<div class="tips" v-if="isShowVerificationCodeTips">-->
        <!--{{ verificationCodeTips }}-->
      <!--</div>-->
      <div class="btn-line">
        <div class='btn only-btn'>
          <span>密码</span>
        </div>
      </div>
      <div class="input-holder">
        <input placeholder="请输入密码" v-model="password" v-on:input="listenPasswordChange" type="password">
      </div>
      <div class="tips" v-if="isShowPasswordTips">
        {{ passwordTips }}
      </div>
      <!--<div class="btn-line">-->
        <!--<div class='btn only-btn'>-->
          <!--<span>重复密码</span>-->
        <!--</div>-->
      <!--</div>-->
      <!--<div class="input-holder">-->
        <!--<input placeholder="请再次输入密码" v-model="passwordRepeat" v-on:input="isPasswordRepeat" type="password">-->
      <!--</div>-->
      <!--<div class="tips" v-if="isShowPasswordRepeatTips">-->
        <!--{{ passwordRepeatTips }}-->
      <!--</div>-->
      <div class="full-btn" v-on:click="sendLoginInfo" v-if="!isBanSendBtn">
        立 即 登 录
      </div>
      <div class="full-btn" v-on:click="sendLoginInfo" v-if="isBanSendBtn">
        登 录 中
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from "./Footer.vue"
export default {
  name: 'Register',
  components: {
    Footer,
  },
  data () {
    return {
      nowChosenBtn: "email",
      email: "",
      isShowEmailTips: false,
      emailTips: "",
      password: "",
      isShowPasswordTips: false,
      passwordTips: "",
      isBanSendBtn: false,
      defaultAvatar: "/api/media/avatar/default_avatar.jpg"
    }
  },
  computed: {

  },
  methods: {
    chosenLoginType: function (type) {
//      window.console.log(type);
      this.nowChosenBtn = type
    },
    listenPasswordChange: function () {
      if (this.password.length === 0) {
        this.isShowPasswordTips = true;
        this.passwordTips = "请输入密码！"
      }
      else if (this.password.length <= 8 && this.password.length > 0) {
        this.isShowPasswordTips = true;
        this.passwordTips = "密码长度过短！"
      }
      else {
        this.isShowPasswordTips = false;
        this.passwordTips = ""
      }
    },
    listenEmailChange: function () {

      if (this.email.length == 0) {
        this.isShowSendBtn = false;
        this.isShowEmailTips = true;
        this.emailTips = "邮箱地址不能为空！"
      }
      else {
        const reg = new RegExp(/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/);
        if (reg.test(this.email)) {
          this.isBanSendBtn = false;
          this.isShowSendBtn = true;
          this.isShowEmailTips = false;
          this.emailTips = "";
        }
        else {
          this.isShowSendBtn = false;
          this.isShowEmailTips = true;
          this.emailTips = "请输入正确的邮箱地址！"
        }
      }

    },
    sendLoginInfo: function () {
      const that = this;
      const data = this.qs.stringify({
        "email": this.email,
        "type": "email",
        "password": this.password
      });
      this.isBanSendBtn = true;
      this.$axios.post("/api/login", data).then(function (res) {
        window.console.log(res);
        res = res.data;
        if (res[0] === 200) {
          that.isShowPasswordTips = false;
          that.passwordTips = "";
          that.$cookie.set('token', res[2], 1);
          that.$cookie.set('isLogin', 1, 1);
          that.$cookie.set('userCode', res[1].user_code, 1);
          that.$cookie.set('userNick', res[1].nickname_str, 1);
          that.$cookie.set('userAvatar', res[1].avatar_str ? res[1].avatar_str : that.defaultAvatar, 1);

          const newPage = that.$router.resolve({
            name: "MarketPage",
          });
          window.open(newPage.href,'_self')
        }
        else {
          that.isShowPasswordTips = true;
          that.passwordTips = "邮箱地址或密码错误！"
        }
        that.isBanSendBtn = false;
      })
    },
  },
  mounted() {

  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .footer {
    /*position: absolute;*/
    /*top: 93vh;*/
    margin-top: 78vh;
  }

  .page-holder {
    width: 600px;
    min-height: 100vh;
    /*background-color: red;*/
    position: absolute;
    top: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .header-holder {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    height: 150px;
    margin-top: 10vh;
  }

  .header-box {
    width: 130px;
    height: 52px;
    text-align: right;
    /*margin-bottom: 20px;*/
    position: relative;
    left: -10px;
    top: -20px;
    /*background-color: red;*/
  }

  .header-box img {
    width: 100%;
    height: 100%;
  }

  .header-box span {
    text-align: right;
    font-size: 200%;
    font-weight: 600;
    line-height: 52px;
  }

  .btn-line {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    height: 30px;
    margin-top: 10px;
    /*background-color: red;*/
  }

  .btn-line div {
    /*width: 100px;*/
    height: 30px;
    line-height: 30px;
    text-align: left;
    margin-right: 30px;
    cursor: pointer;
    font-size: 90%;
  }

  .now-chosen-btn {
    font-size: 100% !important;
    cursor: default !important;
    position: relative;
  }

  .only-btn {
    cursor: default !important;
    font-size: 100% !important;

  }

  .now-chosen-btn span {
    display: inline-block;
    width: auto;
    float: left;
  }

  .now-chosen-btn span:before {
    content: "";
    position: absolute;
    bottom: 10px;
    z-index: -1;
    width: 100%;
    /*width: auto;*/
    float: left;
    display: inline-block;
    height: 3px;
    /*background-color: #e73134;*/
    background-color: #f4a01b;
    /*opacity: 0.7;*/
    border-radius: 5px;
  }

  .input-holder {
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  .input-holder input {
    width: 100%;
    height: 38px;
    margin-top: 6px;
    border-radius: 3px;
    background-color: #fff;
    border: 1px solid #ced4da;
    text-indent: 20px;
    font-size: 100%;
    /*color: #ced4da;*/
  }

  .input-holder input::-webkit-input-placeholder {
    color: #ced4da;
  }

  .input-holder input:focus {
    outline: none;
    border: 1px solid #f4a01b;
  }

  .verification-input input {
    width: 40% !important;
  }

  .verification-input div {
    width: 55%;
    height: 38px;
    border: 1px solid #ced4da;
    margin-top: 6px;
    border-radius: 3px;
    line-height: 38px;
    cursor: default;
  }

  .able-btn {
    cursor: pointer !important;
    background-color: #f4a01b !important;
    border: 1px solid #f4a01b !important;
    color: white;
  }

  .able-btn:hover {
    background-color: #af710e !important;
    color: white;
    border: 1px solid #af710e !important;
  }

  .ban-btn {
    cursor: default;
    color: #ced4da;
  }

  .ban-btn:hover {
    background-color: #ced4da;
    color: white;
  }

  .tips {
    width: 100%;
    height: 30px;
    line-height: 30px;
    color: red;
    font-size: 90%;
    text-align: left;
  }

  .gray-color {
    color: #ced4da;
  }

  .full-btn {
    width: 100%;
    height: 38px;
    border: 1px solid #f4a01b;
    border-radius: 3px;
    line-height: 38px;
    cursor: pointer;
    background-color: #f4a01b;
    color: white;
    margin-top: 30px;
  }

  .full-btn:hover {
    /*background-color: rgb(244, 160, 27);*/
    background-color: #af710e;
    border: 1px solid #af710e;
  }



</style>
