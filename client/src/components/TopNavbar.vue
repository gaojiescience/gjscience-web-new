<template>
  <div class="top-holder">
      <div class="top-content">
      <!--<div class="content-left">-->
        <a class="icon-box" href="/#/market">
            <img src="../assets/logo.png" class="icon-img">
        </a>
        <div class="btn-box">
          <div class="information-btn btn" v-on:click="jumpToCommunity()">
            社区
          </div>
          <div class="discussion-btn btn">
            论坛
          </div>
        </div>
        <SearchAssociation></SearchAssociation>
        <div class="btn-box">
          <div class="download-btn btn" v-on:click="downloadApp">
            扫码下载App
          </div>
          <div class="download-block" v-if="isShowDownload">
            <img src="../assets/download.png">
          </div>
        </div>
        <div class="btn-box" v-if="isLogin !== '1'">
          <div class="information-btn btn" v-on:click="jump('login')">
            登录
          </div>
          <div class="discussion-btn btn" v-on:click="jump('register')">
            注册
          </div>
        </div>
        <div class="btn-box" v-else v-on:click="clickInformation">
          <div class="information-btn avatar">
            <img src="../assets/default_avatar.jpg">
            <!--<img src="../assets/default_avatar.jpg">-->
          </div>
          <div class="information-btn btn" id="information">
            {{ userNick }}
          </div>
          <div class="information-block" v-if="isClickInformation">
            <div class="information-box" v-on:click="jumpToUserProfile">
              个人中心
            </div>
            <div class="information-box" v-on:click="logOut">
              退出登录
            </div>
          </div>
        </div>


      </div>
    </div>
</template>

<script>
import SearchAssociation from "./SearchAssociation.vue"
import Qr from 'vue-qr'
export default {
  name: 'TopNavbar',
  components: {
    SearchAssociation,
  },
  data () {
    return {
      isLogin: 0,
      token: "",
      userCode: "",
//      userName: "",
      userNick: "",
      isClickInformation: false,
      userAvatar: "",
      isShowDownload: false
    }
  },
  methods: {
    logOut: function () {
      this.$cookie.delete("isLogin");
      this.$cookie.delete("token");
      this.$cookie.delete("userCode");
      this.$cookie.delete("userAvatar");
      this.$cookie.delete("userNick");
      window.console.log(this.$cookie.get("isLogin"))
      location.reload();
    },
    downloadApp: function () {
      this.isShowDownload = !this.isShowDownload;
      // window.open("/media/test.zip")
    },
    clickInformation: function (event) {
      this.isClickInformation = !this.isClickInformation
      // if (event.target.id === "information") {
      //   this.isClickInformation = true
      // }
      // else {
      //   this.isClickInformation = false
      // }
    },
    jump: function (type) {
      let newPage;
      if (type === "register") {
        newPage = this.$router.resolve({
          name: "Register",
        });
      }
      else if (type ==="login") {
        newPage = this.$router.resolve({
          name: "Login",
        });
      }
      window.open(newPage.href,'_self')
    },
    jumpToCommunity: function () {
      window.open('http://58.250.250.99:8000/#/community','_blank')
    },
    jumpToUserProfile: function () {
      const newPage = this.$router.resolve({
        name: "UserProfile",
      })
      window.open(newPage.href,'_blank')
    },
    getLoginStatus: function () {
      this.isLogin = this.$cookie.get("isLogin");
      this.token = this.$cookie.get("token");
      this.userCode = this.$cookie.get("userCode");
      this.userAvatar = this.$cookie.get("userAvatar");
      this.userNick = this.$cookie.get("userNick");
//      if (this.isLogin === "1") {
//        this.getUserProfile(this)
//      }
//      window.console.log(this.userAvatar)
    },
//    getUserProfile: function (this_) {
////      window.console.log(this_.isLogin);
//      const that = this_;
//      this.$axios.get("/api/login?code=" + this.userCode + "&token=" + this.token, {}).then(function (res) {
////        window.console.log(res);
//        that.userName = res.data;
//      })
//    },
  },
  mounted() {
    this.getLoginStatus();
    document.addEventListener('click', (e)=> {
      if (e.target.id != 'information') {
        this.isClickInformation= false;
      }
    })
//    window.console.log(this.isLogin);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .top-holder {
    width: 100vw;
    height: 7vh;
    min-height: 7vh;
    display: flex;
    display: -webkit-flex;
    justify-content: center;
    position: fixed;
    top: 0;
    border-bottom: 1px solid #f7f7fa;
    z-index: 2;
    background-color: rgba(255, 255, 255, 1 );
  }

  .top-content {
    min-width: 1200px;
    width: 1200px;
    /*background-color: yellow;*/
    display: flex;
    display: -webkit-flex;
    /*flex-wrap: wrap-reverse;*/
    /*align-content: space-between;*/
    /*justify-content: space-between;*/
    justify-content: center;
    align-items: center;
    /*color: white;*/
  }

  .icon-box {
    width: 150px;
    margin-left: -20px;
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
    /*min-width: 300px;*/
    height: 30px;
    /*width: 300px;*/
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
    width: 100px;
    /*height: auto;*/
    height: 30px;
    line-height: 30px;
    cursor: pointer;
    display: block;
    /*background-color: pink;*/
  }

  .avatar {
    width: 30px !important;
    height: 30px !important;
    /*overflow: hidden;*/

    /*margin-top: -5px;*/
  }

  .avatar img {
    width: 110%;
    height: 110%;
    border-radius: 5px;
    margin-top: -5%;
  }

  .information-block {
    width: 150px;
    height: 96px;
    background-color: white;
    border-radius: 3px;
    top: 70px;
    position: absolute;
    box-shadow: 1px 1px 4px rgba(120, 120, 120, 0.9);
    display: flex;
    flex-direction: column;
  }

  .information-box {
    width: 100%;
    height: 46px;
    /*background-color: red;*/
    line-height: 46px;
    cursor: pointer;
    border-bottom: 1px solid #F6F6F6;
  }

  .information-box:hover {
    background-color: #F6F6F6;
  }

  .download-btn {
    background-color: #0084ff;
    color: white;
    border-radius: 15px;
    padding-left: 10px;
    padding-right: 10px;
    font-size: 95%;
  }

  .download-block {
    width: 120px;
    height: 120px;
    position: absolute;
    background-color: white;
    box-shadow: 2px 2px 5px rgba(120, 120, 120, 0.9);
    top: 60px;
    /*left: 25px;*/
    border-radius: 5px;
  }

  .download-block img {
    width: 90%;
    height: 90%;
    margin-top: 5%;
    margin-left: 2%;
  }
</style>



// WEBPACK FOOTER //
// src/components/TopNavbar.vue
