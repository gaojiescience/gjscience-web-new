<template>
  <div class="root">
    <TopNavbar></TopNavbar>
    <div class="container">
      <div class="container-left">
        <div class="content-left">
          <div class="content-bar">
            <div class="user-info-box">
              <div class="avatar-box">
<!--                <img :src="userAvatar">-->
                <img src="../assets/default_avatar.jpg">
              </div>
              <div class="name-box">
                <div class="name-line" contenteditable="false" v-on:blur="changeName" v-on:keydown="lestenInputName($event)">
                  {{ userNick }}
                </div>
                <div class="edit-line" v-on:click="editName">
                  <img src="../assets/edit.png">
                </div>
              </div>
              <div class="social-box">
                <div class="follow-box">
                  <div class="follow-content">
                    <div class="content-title-line">
                      关注
                    </div>
                    <div class="content-data-line">
                      {{ followNum }}
                    </div>
                  </div>
                </div>
                <div class="fans-box">
                  <div class="fans-content">
                    <div class="content-title-line">
                      粉丝
                    </div>
                    <div class="content-data-line">
                      {{ fansNum }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="edit-bar">
              <div class="edit-bar-line">
                基本资料
              </div>
              <div class="edit-bar-line">
                我的评论
              </div>
              <div class="edit-bar-line">
                我的收藏
              </div>
            </div>
            <div class="func-bar">
              <div class="edit-bar-line" v-on:click="changePage('operationalShares')">
                自选组合
              </div>
              <div class="edit-bar-line" v-on:click="changePage('fakeStock')">
                虚拟账户
              </div>
            </div>
          </div>
        </div>
        <div class="content-right">
          <div class="content-holder">
            <OperationalSharesDetail v-if="nowChosenPage === 'operationalShares'"></OperationalSharesDetail>
            <FakeStock v-if="nowChosenPage === 'fakeStock'" style="width: 150% !important; z-index: 999;"></FakeStock>
          </div>
        </div>
      </div>
      <!--<div class="container-right">

      </div>-->
    </div>
    <div class="page-footer">
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import Footer from "./Footer.vue"
import TopNavbar from "./TopNavbar.vue"
  import OperationalSharesDetail from "./OperationalSharesDetail.vue"
  import FakeStock from "./FakeStock.vue"
export default {
  name: 'UserProfile',
  components: {
    Footer,
    TopNavbar,
    OperationalSharesDetail,
    FakeStock
  },
  data () {
    return {
      userAvatar: "",
      userNick: "",
      userAvatarDev: "/assets/default_avatar.jpg",
      followNum: 0,
      fansNum: 0,
      isEditName: false,
      nowChosenPage: "operationalShares"
    }
  },
  methods: {
    getLoginStatus: function () {
      this.isLogin = this.$cookie.get("isLogin");
      this.token = this.$cookie.get("token");
      this.userCode = this.$cookie.get("userCode");
      this.userAvatar = this.$cookie.get("userAvatar");
      this.userNick = this.$cookie.get("userNick");
    },
    changePage: function (pageType) {
      this.nowChosenPage = pageType
    },
    lestenInputName: function (event) {
      window.console.log(event)
      if (event.keyCode == 13) {
        window.console.log(1)
        const editor = document.getElementsByClassName("name-line")[0];
        editor.setAttribute("contenteditable", "false");
        this.changeName()
      }
    },
    editName: function () {
      const editor = document.getElementsByClassName("name-line")[0];
      editor.setAttribute("contenteditable", "true");
      editor.innerHTML = editor.innerText
      editor.focus();      
    },
    changeName: function () {
      window.console.log(111)
      const that = this;
      const editor = document.getElementsByClassName("name-line")[0];
      let newName = editor.innerText.replace(/(^\s*)|(\s*$)/g, "");
      if (newName.length >= 16) {
        alert("昵称长度不能超过16！")
        editor.innerText = this.userNick;
        return 0
      }
      if (newName.length == 0) {
        alert("昵称不能为空！");
        editor.innerText = this.userNick;
        return 0
      };

      if (newName.indexOf(" ") != -1) {
        alert("昵称不能包含空格！");
        editor.innerText = this.userNick;
        return 0
      };
      this.$axios.patch("/api/userProfile", { "name": newName, "code": this.userCode }).then(function (res) {
        if (res.data == newName) {
          that.$cookie.set("userNick", res.data);
        }
      })
    },
  },
  mounted() {
    this.getLoginStatus();
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

  .page-footer {
    width: 100vw;
    height: 150px;
    /*background-color: pink;*/
  }

  .container {
    width: 60vw;
    min-width: 1215px;
    min-height: 97vh;
    display: flex;
  }

  .container-left {
    width: 70%;
    min-height: 97vh;

    display: flex;
  }

  .container-right {
    width: 30%;
    min-height: 97vh;

  }

  .content-left {
    width: 25%;
    min-height: 97vh;
    /*background-color: green;*/
  }

  .content-right {
    min-width: 75%;
    min-height: 97vh;
    padding-top: 30px;
  }

  .content-bar {
    width: 180px;
    height: 500px;
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    border-radius: 2px;
    border: 1px solid #F6F6F6;
  }

  .user-info-box {
    width: 100%;
    height: 250px;

    display: flex;
    flex-direction: column;
    border-bottom: 1px solid #F6F6F6;
  }

  .avatar-box {
    width: 100%;
    height: 120px;

  }

  .avatar-box img {
    width: 80px;
    height: 80px;
    border-radius: 40px;
    position: relative;
    top: 40px
  }

  .name-box {
    width: 100%;
    height: 30px;
    /*background-color: red;*/
    margin-top: 10px;
    display: flex;
    justify-content: center;
  }

  .name-line {
    height: 30px;
    line-height: 30px;
    font-size: 95%;
  }

  .edit-line img {
    margin-top: 5px;
    margin-left: 5px;
    cursor: pointer;
  }

  .social-box {
    width: 100%;
    height: 90px;
    display: flex;
  }

  .follow-box {
    width: 50%;
    height: 90px;
  }

  .fans-box {
    width: 50%;
    height: 90px;
  }

  .follow-content {
    height: 60px;
    margin-top: 10px;
    border-right: 1px solid #F6F6F6;
  }

  .fans-content {
    height: 60px;
    margin-top: 10px;
  }

  .content-title-line {
    height: 50%;
    line-height: 30px;
    font-size: 95%;
  }

  .content-data-line {
    height: 50%;
    line-height: 30px;
    cursor: pointer;
  }

  .edit-bar {
    width: 100%;
    height: 140px;
    /*padding: 20px;*/
    padding-top: 10px;
    box-sizing: border-box;
    border-bottom: 1px solid #F6F6F6;
  }

  .edit-bar-line {
    width: 100%;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
  }

  .edit-bar-line:hover {
    background-color: #F6F6F6;
  }

  .func-bar {
    padding-top: 10px;
  }

  .content-holder {
    width: 100%;
    min-height: 97vh;
    /*background-color: #07b360;*/
  }

</style>



// WEBPACK FOOTER //
// src/components/UserProfile.vue
