<template>
  <div class="top-holder">
      <div class="top-content">
      <!--<div class="content-left">-->
        <div class="icon-box">
            <img src="../assets/logo.png" class="icon-img">
        </div>
        <div class="btn-box">
          <div class="information-btn btn">
            资讯
          </div>
          <div class="discussion-btn btn">
            论坛
          </div>
        </div>
        <SearchAssociation></SearchAssociation>
        <div class="btn-box" v-if="isLogin !== '1'">
          <div class="information-btn btn" v-on:click="jump('login')">
            登录
          </div>
          <div class="discussion-btn btn" v-on:click="jump('register')">
            注册
          </div>
        </div>
        <div class="btn-box" v-else>
          <div class="information-btn avatar">
            <img :src="userAvatar">
            <!--<img src="../assets/default_avatar.jpg">-->
          </div>
          <div class="information-btn btn">
            {{ userNick }}
          </div>
        </div>


      </div>
    </div>
</template>

<script>
import SearchAssociation from "./SearchAssociation.vue"
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
      userNick: ""
    }
  },
  methods: {
    jump: function (type) {
      let newPage;
      if (type == "register") {
        newPage = this.$router.resolve({
          name: "Register",
        });
      }
      else {
        newPage = this.$router.resolve({
          name: "Login",
        });
      }
      window.open(newPage.href,'_self')
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
      window.console.log(this.userAvatar)
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
    width: 60vw;
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
    min-width: 300px;
    height: 30px;
    width: 300px;
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
</style>
