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
        <div class="full-progress">
          <div class="now-progress" :style="'width: ' + this.nowProgress + '%;'">

          </div>
        </div>



      </div>
      <div class="btn-line">
        <div :class="'btn ' + (nowChosenBtn == 'email' ? 'now-chosen-btn' : '')" v-on:click="chosenRegisterType('email')">
          <span>邮箱注册</span>
        </div>
        <div :class="'btn ' + (nowChosenBtn == 'phone' ? 'now-chosen-btn' : '')" v-on:click="chosenRegisterType('phone')">
          <span>手机注册</span>
        </div>
      </div>
      <div class="input-holder">
        <input placeholder="请输入邮箱地址" v-model="email" v-on:input="listenEmailChange">
      </div>
      <div class="tips" v-if="isShowEmailTips">
        {{ emailTips }}
      </div>
      <div class="input-holder verification-input">
        <input placeholder="请输入邮箱验证码" class="verification-input" v-model="verificationCode" v-on:input="listenVerificationCode">
        <div :class="(isShowSendBtn ? 'able-btn' : 'ban-btn')" v-on:click="requestVerificationCode">{{ btnText }}</div>
        <!--<div v-if="isBanSendBtn" :class="'ban-btn ' + (isBanSendBtn ? 'gray-color' : '')">{{ btnText }}</div>-->
      </div>
      <div class="tips" v-if="isShowVerificationCodeTips">
        {{ verificationCodeTips }}
      </div>
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
      <div class="btn-line">
        <div class='btn only-btn'>
          <span>重复密码</span>
        </div>
      </div>
      <div class="input-holder">
        <input placeholder="请再次输入密码" v-model="passwordRepeat" v-on:input="isPasswordRepeat" type="password">
      </div>
      <div class="tips" v-if="isShowPasswordRepeatTips">
        {{ passwordRepeatTips }}
      </div>
      <div class="full-btn" v-on:click="sendRegisterInfo">
        立 即 注 册
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
  import Footer from "./Footer.vue"
  import { throttle } from "../tools.js"
export default {
  name: 'Register',
  components: {
    Footer,
  },
  data () {
    return {
      nowChosenBtn: "email",
      email: "",
      isShowSendBtn: false,
      isShowEmailTips: false,
      emailTips: "",
      isBanSendBtn: false,
      count: 0,
      password: "",
      isShowPasswordTips: false,
      isShowPasswordRepeatTips: false,
      passwordTips: "",
      passwordRepeat: "",
      passwordRepeatTips: "",
      verificationCodeTips: "",
      isShowVerificationCodeTips: false,
      verificationCode: "",
      nowProgress: 0,
    }
  },
  computed: {
    btnText () {
      return (this.count !== 0 ? "重新发送: " + this.count + " 秒" : "发送邮箱验证码")
    }
  },
  methods: {
    changeProgress: function () {
      let flag1;
      let flag2;
      let flag3;
      let flag4;
      let flag5;
      let flag;
      if (!this.isShowEmailTips && this.email.length !== 0) {
        flag1 = 20
      }
      else {
        flag1 = 0
      }

      if (!this.isShowPasswordTips && this.password.length !== 0) {
        flag2 = 20
      }
      else {
        flag2 = 0
      }

      if (!this.isShowPasswordRepeatTips && this.passwordRepeat.length !== 0) {
        flag3 = 20
      }
      else {
        flag3 = 0
      }

      if (!this.isShowVerificationCodeTips && this.verificationCode.length !== 0) {
        flag4 = 20
      }
      else {
        flag4 = 0
      }

      if (this.isBanSendBtn) {
        flag5 = 20
      }
      else {
        flag5 = 0
      }

      flag = flag1 + flag2 + flag3 + flag4 + flag5;
//      window.console.log(flag)
//      window.console.log(this.isBanSendBtn)
//      window.console.log(this.count)
      const ele = window.document.getElementsByClassName("now-progress")[0];
      this.nowProgress = flag;
      ele.setAttribute("progress", flag + "%");
    },
    listenVerificationCode: function () {

//      window.console.log(this.verificationCode.length)
      if (this.verificationCode.length == 0) {
        this.isShowVerificationCodeTips = true;
        this.verificationCodeTips = "验证码不能为空！"
      }
      else if (this.verificationCode.length > 0 && this.verificationCode.length < 6) {
        this.isShowVerificationCodeTips = true;
        this.verificationCodeTips = "验证码为6位有效数字！"
      }
      else {
        this.isShowVerificationCodeTips = false;
        this.verificationCodeTips = ""
      }

      this.changeProgress();
    },
    sendRegisterInfo: throttle(function () {
      const that = this;
      this.listenEmailChange();
      this.listenPasswordChange();
      this.isPasswordRepeat();
      this.listenVerificationCode();
      window.console.log((this.emailTips+this.passwordTips+this.passwordRepeatTips+this.verificationCodeTips))
      if ((this.emailTips+this.passwordTips+this.passwordRepeatTips+this.verificationCodeTips).length == 0) {
        const data = this.qs.stringify({
          "email": this.email,
          "password": this.password,
          "type": "email",
          "code": this.verificationCode
        });
        window.console.log(data);
        this.$axios.post("/api/register", data).then(function (res) {
          window.console.log(res);
          if (res.data[0] === 200) {
            let newPage = that.$router.resolve({
              name: "Login",
            });
            localStorage.setItem("userEmail", JSON.stringify(that.email))
            window.open(newPage.href, '_self')
          }
        });
      }
    }, 1000),
    isPasswordRepeat: function () {
      if (this.password === this.passwordRepeat) {
        this.isShowPasswordRepeatTips = false;
        this.passwordRepeatTips = ""
      }
      else {
        this.isShowPasswordRepeatTips = true;
        this.passwordRepeatTips = "两次输入的密码不一致！"
      }
      this.changeProgress();
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
      this.changeProgress();
    },
    chosenRegisterType: function (type) {
//      window.console.log(type);
      this.nowChosenBtn = type
    },
    countdown: function () {
      this.count = 60;
      this.interval=setInterval(()=>{
        this.count--;
        if(this.count === 0){
          this.isBanSendBtn = false;
          clearInterval(this.interval);
        }
      },1000);
    },
    listenEmailChange: function () {

      if (!this.isBanSendBtn) {
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
      }
      this.changeProgress();

    },

    requestVerificationCode: throttle(function () {
      const that = this;
      if (this.isShowSendBtn) {
        const data = this.qs.stringify({
          "email": this.email,
          "type": "email"
        });

        this.$axios.post("/api/register", data).then(function (res) {
          window.console.log(res)
          if (res.data[0] === 500) {
            that.isShowEmailTips = true;
            that.isShowSendBtn = false;
            that.isBanSendBtn = false;
            that.emailTips = "该邮箱已被使用！"
          }
          else if (res.data[0] === 200) {
            that.isShowSendBtn = false;
            that.isBanSendBtn = true;
            that.changeProgress();
            that.countdown();
          }
        });
        
      }

    }, 1000)
  },
  mounted() {
    this.changeProgress();
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

  .full-progress {
    width: 100%;
    height: 5px;
    border-radius: 2px;
    background-color: #ced4da;
    margin-bottom: 30px;
  }

  .now-progress {
    /*width: 20%;*/
    height: 5px;
    border-radius: 2px;
    background-color: #5cb85c;
    position: relative;
    transition: width 1s;
  }

  .now-progress:after {
    content: attr(progress);
    position: absolute;
    bottom: 10px;
    z-index: -1;
    width: 40px;
    /*width: auto;*/
    float: right;
    right: -20px;
    display: inline-block;
    height: 30px;
    /*background-color: #e73134;*/
    background-color: #fff;
    /*opacity: 0.7;*/
    border-radius: 5px;
    box-shadow: 1px 1px 5px #ced4da;
    font-size: 90%;
    line-height: 30px;
    color: #5cb85c;
    font-weight: 600;
  }

  .now-progress:before {
    content: '';
    position: relative;
    border: 0.3rem solid #d8d8d8;
    border-color: #fff transparent transparent;
    /*box-shadow: 1px 1px 1px #ced4da;*/
    width: 0;
    height: 0;
    left: 0.3rem;
    float: right;
    right: -20px;
    top: -5px;
  }


</style>



// WEBPACK FOOTER //
// src/components/Register.vue
