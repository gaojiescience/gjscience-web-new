<template>
  <div class="content-holder">
    <div class="text-area" v-if="isLogin!=='1'">
      <p>
        <a class='light-blue block' style="text-decoration: none;" href="/#/login">登录</a>  后发表评论
      </p>
    </div>
    <div class="text-area" contenteditable="true" v-on:input="watchKeyboardInput" v-on:blur="recoverRangePosition" v-model="commentsHtml" v-else>
      <p>
        <br>
        <!--<a onselectstart='return false' class='light-blue block' style="text-decoration: none;" :href="'/#/stock/' + exchange + '/' + stock + '/' + isIndex" readonly='true'>$ {{name}}({{exchange.toUpperCase()}}{{stock}}) $</a>&nbsp;-->
      </p>
    </div>

    <div class="search-box" :style="'left: ' + searchBoxLeft + 'px;top:' + searchBoxTop + 'px'" v-show="showSearchBox" >
      <div class="box-header">
        <p>想要引入的股票:</p>
        <input class="box-header-input" id="stockInput" v-model="searchInput" v-on:input="searchConnect" @keydown.stop.prevent.up="upChosenStock" @keydown.stop.prevent.down="downChosenStock">
      </div>
      <div class="choices-box">
        <div class="choice-line" v-for="(item, index ) in searchAssociation" v-bind:key="index" v-on:click="choseStock(index)">
          <div class="line-content stock-content">
            {{ item.stock }}
          </div>
          <div class="line-content name-content">
            {{ item.name }}
          </div>
        </div>
      </div>
    </div>
    <div class="toolbar">
      <div class="left-bar">
        <div class="tool-btn">
          <img src="../assets/face.png" v-on:click="emojiBoxDropDown()">
          <div class="emoji-dropdown" v-if="showEmojiBox">
            <div v-for="(item, index) in emojiList" v-bind:key="index" v-html="item" class="emoji-box" v-on:click="insertEmoji(item)">

            </div>
          </div>
        </div>
        <div class="tool-btn" v-on:click="selectFile">
          <img src="../assets/img.png">
          <input type="file" accept=".jpg,.png,.gif" @change="handleFileChange" ref="selectFile" multiple="multiple">
        </div>
        <div class="tool-btn">
          <img src="../assets/stock.png" v-on:click.stop.prevent="showStockSearchBox">
        </div>
      </div>
      <div class="right-bar">
        <div class="send-btn" v-on:click="uploadComments">
          发布
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import SearchAssociation from "./SearchAssociation.vue"
export default {
  name: 'SearchAssociation',
  components: {
//    SearchAssociation,
  },
  props: {
    stock: {
      type: String
    },
    name: {
      type: String
    },
    exchange: {
      type: String
    },
    isIndex: {
      type: String
    }
  },
  data () {
    return {
      showSearchBox: false,
      showEmojiBox: false,
      searchBoxLeft: 0,
      searchBoxTop: 0,
      searchInput: "",
      searchAssociation: [],
      emojiList: ["&#x1F434;", "&#x1F435;", "&#x1F436;", "&#x1F42E;", "&#x1F432;", "&#x1F620;", "&#x1F629;", "&#x1F632;", "&#x1F61E;", "&#x1F635;", "&#x1F630;", "&#x1F612;", "&#x1F60D;", "&#x1F624;", "&#x1F61C;", "&#x1F61D;", "&#x1F60B;", "&#x1F618;", "&#x1F61A;", "&#x1F637;", "&#x1F602;", "&#x1F621;", "&#x1F631;", "&#x1F60F;", "&#x1F62D;", "&#x1F64F;", "&#x1F525;", "&#x1F48A;", "&#x1F4A3;", "&#x1F44F;",],
      nowChosenStock: 0,
      commentsHtml: "",
      isLogin: "0"
    }
  },
  methods: {
    watchKeyboardInput: function (e) {
      const inputContent = e.data;
      const topElement = document.getElementsByClassName("text-area")[0];
//      window.console.log(e);
      if (inputContent === null) {
//        window.console.log(topElement);
        if (topElement.childNodes.length === 0) {
          topElement.appendChild(document.createElement("p").appendChild(document.createElement("br")))
        }
      }
    },
    showStockSearchBox: function (e) {
      let ele = document.getElementsByClassName("text-area")[0];
      this.showSearchBox = !this.showSearchBox;
      this.searchBoxTop = ele.offsetTop + 140;
      this.searchBoxLeft =  ele.offsetLeft + 60;
      let getFocus = function () {
        let focusElement = document.getElementsByClassName("box-header-input")[0];
        focusElement.focus();
        focusElement.select();
      };

      setTimeout(getFocus, 500);
    },
    resetRangePosition: function (id) {
      let topElement = document.getElementsByClassName("text-area")[0];
      document.getElementsByClassName("text-area")[0].focus();
      let selection = document.getSelection();
      let range = selection.getRangeAt(0);
//      let offSet = this.nowRange.startOffset + text.length;
      let focuseElement = document.getElementById(id);
      for (let eleIndex in topElement.childNodes[0].childNodes) {
        if (topElement.childNodes[0].childNodes[eleIndex].id === id.toString()) {
          range.setStartAfter(topElement.childNodes[0].childNodes[eleIndex]);
          range.collapse(true);
        }
      }
    },
    insertStockLink: function (href, text) {
      // 将link作为节点插入至光标位置
      let id = new Date;
      id = id.getTime();
      let stockElement = document.createElement("a");
      stockElement.className = "light-blue block";
      stockElement.innerText = text;
      stockElement.setAttribute("contenteditable", "false");
      stockElement.id = id;
      this.nowRange.insertNode(stockElement);
      // 输入框重新获取焦点，移动光标至刚插入元素的后面

//      range.selectNodeContents(focuseElement);
      this.resetRangePosition(id)
    },
    searchConnect: function(e) {
      const that = this;
      const targetUrl = "/api/searchAssociation?input=" + this.searchInput;
//      window.console.log(this.searchInput);
      this.$axios.get(targetUrl, {}).then(function (res){
//        window.console.log(res);
        that.showChoices = true;
        that.searchAssociation = res.data;
      })
//      window.console.log(e);
    },
    choseStock: function (index) {
      let topElement = document.getElementsByClassName("text-area")[0];
//      window.console.log(this.searchAssociation[index]);
      let searchAssociation = this.searchAssociation;
      let stockHref = '/#/stock/' + searchAssociation[index]["exchange_abbr"] + '/' + searchAssociation[index]["stock"] + '/' + searchAssociation[index]["isIndex"];
      let stockText = "$" + searchAssociation[index]["name"] + "(" + searchAssociation[index]["exchange_abbr"].toUpperCase() + searchAssociation[index]["stock"] + ")$";
      this.insertStockLink(stockHref, stockText);
      this.searchInput = "";
      this.searchAssociation = [];
      this.showSearchBox= false;

    },
    recoverRangePosition: function (e) {
      let topElement = document.getElementsByClassName("text-area")[0];
//      topElement.focus();
      let selection = document.getSelection();
      let range = selection.getRangeAt(0);
//      window.console.log(selection);
      this.nowSelection = selection;
      this.nowRange = range;
    },
    emojiBoxDropDown: function () {
      this.showEmojiBox = !this.showEmojiBox;
    },
    insertEmoji: function (emoji) {
      let id = new Date;
      id = id.getTime();
      let emojiElement = document.createElement("span");
      emojiElement.setAttribute("contenteditable", "false");
      emojiElement.id = id;
      emojiElement.innerHTML = emoji;
      this.nowRange.insertNode(emojiElement);
      this.showEmojiBox = false;
      this.resetRangePosition(id);
    },
    selectFile: function () {
      this.$refs.selectFile.dispatchEvent(new MouseEvent('click'));
    },
    handleFileChange: function (event) {
//      window.console.log(event);
      const that = this;
      let imgFiles = [];
      const fileReader = new FileReader();
      for (let fileIndex in event.path[0].files) {
        if (event.path[0].files[fileIndex].size/1024 < 5120) {
          imgFiles.push(event.path[0].files[fileIndex])
        }
      }
//      window.console.log(imgFiles)
      let fileIndex = 0;
      fileReader.readAsDataURL(imgFiles[fileIndex]);
      fileReader.onload = function (res) {
        let imgNode = document.createElement("img");
        let id = new Date;
        id = id.getTime();
        imgNode.setAttribute("src", fileReader.result);
        imgNode.id = id;
        imgNode.classList.add("upload-img");
        that.nowRange.insertNode(imgNode);
        fileIndex += 1;
        if (fileIndex < imgFiles.length) {
          fileReader.readAsDataURL(imgFiles[fileIndex])
        }
      }
    },
    upChosenStock: function () {
//      this.nowChosenStock += 1;
    },
    downChosenStock: function () {
//      this.nowChosenStock -= 1;
    },
    uploadComments: function () {
      const that = this;
      this.commentsHtml = document.getElementsByClassName("text-area")[0].innerHTML;
      const data = this.qs.stringify({
        "user": this.$cookie.get("userCode"),
        "stock": this.stock,
        "content": this.commentsHtml,
      });
//      window.console.log(data);
      this.$axios.post("/api/comments", data).then(function (res) {
//        window.console.log(res);
        if (res.status === 200) {
          that.commentsHtml = "";
          document.getElementsByClassName("text-area")[0].innerText = "";
          that.$emit("updateCommentsData");
        }
      });
    }
  },
  mounted() {
    this.isLogin = this.$cookie.get("isLogin");
//    window.console.log(this.isLogin)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .content-holder {
    width: 100%;
    min-height: 140px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .text-area {
    width: 100%;
    min-height: 96px;
    background-color: white;
    box-sizing: border-box;
    padding: 5px 10px;
    text-align: left;
    border-radius: 5px;
    border: 1px solid #F6F6F6;
    outline: none;
    overflow-x: hidden;
  }

  .text-area >>> img {
    max-width: 650px;
    margin: 15px auto;
    display: block;
  }

  .text-area >>> img:after {
    content: "delete";
    width: 30px;
    height: 30px;
    position: relative;
    top: 20px;
    color: white;
  }

  .text-area >>> a {
    color: #06c;
  }

  .toolbar {
    width: 100%;
    height: 30px;
    background-color: white;
    display: flex;
    justify-content: space-between;
  }

  .light-blue {
    color: #06c;
  }

  .block {
    display: inline-block;
    cursor: pointer;
    user-select: none;
    line-height: 20px;
    word-break: break-all;
    height: 20px;
  }

  .search-box {
    min-width: 200px;
    min-height: 150px;
    max-height: 300px;

    background-color: white;
    position: absolute;
    z-index: 5;
    border-radius: 5px;
    box-shadow: 0 2px 8px 0 rgba(44,46,59,.1);
  }

  .box-header {
    width: 200px;
    height: 40px;
    text-align: left;
    text-indent: 10px;
    line-height: 40px;
    font-size: 90%;
    position: relative;
    top: 0;
    display: flex;
  }

  .box-header p {
    display: block;
    width: 120px;
    height: 100%;
  }

  .box-header input {
    width: 60px;
    height: 100%;
    outline: none;
    border: none;
  }

  .choices-box {
    max-height: 250px;
    min-height: 100px;
    margin-bottom: 10px;
    overflow: scroll;
    overflow-x: hidden;
  }

  .choice-line {
    width: 100%;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
    display: flex;
  }

  .choice-line:hover {
    background-color: #f7f7fa;
  }

  .line-content {
    width: 80px;
    height: 100%;
    text-align: left;
  }

  .exchange-content {
    width: 40px;
    text-align: right !important;
    overflow : hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }

  .stock-content {
    text-indent: 8px;
  }

  .name-content {
    width: 140px;
  }

  .left-bar {
    width: 80%;
    display: flex;
    justify-content: flex-start;

  }

  .right-bar {
    width: 20%;
    display: flex;
    justify-content: flex-end;
  }

  .tool-btn {
    width: 30px;
    height: 30px;
    box-sizing: border-box;
    padding: 5px;
    cursor: pointer;
    z-index: 999;
  }

  .tool-btn input {
    display: none;
  }

  .tool-btn img {
    width: 100%;
    height: 100%;
  }

  .send-btn {
    width: 64px;
    height: 30px;
    background-color: #0084ff;
    border-radius: 3px;
    color: white;
    cursor: pointer;
    text-align: center;
    line-height: 30px;
    font-size: 95%;
    border: 1px solid #0084ff;
  }

  .send-btn:hover {
    background-color: #1369bf;
  }

  .emoji-dropdown {
    width: 200px;
    height: 200px;
    background-color: white;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.4);
    border-radius: 3px;
    box-sizing: border-box;
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    cursor: default !important;
  }

  .emoji-box {
    width: 30px;
    height: 30px;
    cursor: pointer;
    /*background-color: red;*/
    margin-right: 6px;
    text-align: center;
  }

  .upload-img {
    max-width: 700px;
  }

</style>



// WEBPACK FOOTER //
// src/components/StockCommentsEditor.vue