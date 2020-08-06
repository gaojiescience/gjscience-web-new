<template>
  <div class="content-holder">
    <div class="text-area" contenteditable="true" v-on:input="listenMouseSelect" v-on:click="setRangePosition">

        <a onselectstart='return false' class='light-blue block' style="text-decoration: none;" :href="'/#/stock/' + exchange + '/' + stock + '/' + isIndex" readonly='true'>$ {{name}}({{exchange.toUpperCase()}}{{stock}}) $</a>&nbsp;

    </div>
    <div class="search-box" :style="'left: ' + (newRange) + 'px;top:' + newHeight + 'px'" v-if="isShowSearchBox">
      <div class="box-header">
        想要引用的股票：
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
          <img src="../assets/face.png" v-on:click="showEmojiDropDown">
          <div class="emoji-dropdown" v-if="isShowEmojiDropDown">
            <div v-for="(item, index) in emojiList" v-bind:key="index" v-html="item" class="emoji-box" v-on:click="insertEmoji(item)">

            </div>
          </div>
        </div>
        <div class="tool-btn" v-on:click="selectFile">
          <img src="../assets/img.png">
          <input type="file" accept=".jpg,.png,.gif" @change="handleFileChange" ref="selectFile" multiple="multiple">
        </div>
        <div class="tool-btn" v-on:click="inputStock">
          <img src="../assets/stock.png">
        </div>
      </div>
      <div class="right-bar">
        <div class="send-btn">
          发布
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import SearchAssociation from "./SearchAssociation.vue"
export default {
  name: 'Comments',
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
//      inputData: ["&nbsp;<a onselectstart='return false' class='light-blue block'>${{name}}({{exchange.toUpperCase()}}{{stock}})$&nbsp;</a>"],
      range: 0,
      isShowSearchBox: false,
      searchAssociation: [],
      searchInput: "",
      emojiList: ["&#x1F434;", "&#x1F435;", "&#x1F436;", "&#x1F42E;", "&#x1F432;", "&#x1F620;", "&#x1F629;", "&#x1F632;", "&#x1F61E;", "&#x1F635;", "&#x1F630;", "&#x1F612;", "&#x1F60D;", "&#x1F624;", "&#x1F61C;", "&#x1F61D;", "&#x1F60B;", "&#x1F618;", "&#x1F61A;", "&#x1F637;", "&#x1F602;", "&#x1F621;", "&#x1F631;", "&#x1F60F;", "&#x1F62D;", "&#x1F64F;", "&#x1F525;", "&#x1F48A;", "&#x1F4A3;", "&#x1F44F;",],
      isShowEmojiDropDown: false
    }
  },
  methods: {
    inputStock: function () {
      const that = this;
      const ele = document.getElementsByClassName("text-area")[0];
      let childNodes = ele.childNodes;
      ele.focus();
      this.setRange(5);
      this.nowRange = this.getCurrentRange();
      let cursor = 0;

      if (childNodes.length === 0) {
        ele.innerText = "$";
        this.nowRange = 1;
        ele.focus();
        this.setRange(5);
        this.listenMouseSelect({data: "$"});
      }
      else {
        for (let nodeIndex in childNodes) {
          if ((cursor+childNodes[nodeIndex].textContent.length) < this.nowRange ) {
            window.console.log(childNodes[nodeIndex].textContent);
            cursor += childNodes[nodeIndex].textContent.length;
          }
          else {
            childNodes[nodeIndex].textContent = childNodes[nodeIndex].textContent.substr(0, this.nowRange-(cursor-childNodes[nodeIndex].textContent.length)) + "$" + childNodes[nodeIndex].textContent.substr(this.nowRange-(cursor-childNodes[nodeIndex].textContent.length), cursor + childNodes[nodeIndex].textContent.length)

            this.listenMouseSelect({data: "$"});
            break
          }
        }
      }

    },
    selectFile: function () {
      this.$refs.selectFile.dispatchEvent(new MouseEvent('click'));
    },
    handleFileChange: function (event) {
      window.console.log(event);
      const that = this;
      const ele = document.getElementsByClassName("text-area")[0];

      let imgFiles = [];
      const fileReader = new FileReader();
      for (let fileIndex in event.path[0].files) {
        if (event.path[0].files[fileIndex].size/1024 < 5120) {
          imgFiles.push(event.path[0].files[fileIndex])
        }
      }

      let childNodes = ele.childNodes;
      let text = ele.innerText;
      if (childNodes.length === 0) {
        let fileIndex = 0;
        fileReader.readAsDataURL(imgFiles[fileIndex]);

        fileReader.onload = function (res) {
          let imgNode = document.createElement("img");
          imgNode.setAttribute("src", fileReader.result);
          imgNode.classList.add("upload-img");
          ele.appendChild(imgNode);
          fileIndex += 1;
          if (fileIndex < imgFiles.length) {
            fileReader.readAsDataURL(imgFiles[fileIndex])
          }
        }

      }
      else {
        let cursor = 0;
        window.console.log(ele.innerHTML);
        window.console.log(childNodes);
        let fileIndex = 0;
        fileReader.readAsDataURL(imgFiles[fileIndex]);

        fileReader.onload = function (res) {
          let imgNode = document.createElement("img");
          window.console.log(childNodes);
          imgNode.setAttribute("src", fileReader.result);
          imgNode.classList.add("upload-img");
//              ele.appendChild(imgNode);
//              ele.insertBefore(startEle, childNodes[nodeIndex]);
          ele.appendChild(imgNode);
//              ele.insertBefore(endEle, childNodes[nodeIndex]);
//              ele.removeChild(childNodes[nodeIndex]);
          fileIndex += 1;
          if (fileIndex < imgFiles.length) {
            fileReader.readAsDataURL(imgFiles[fileIndex])
          }
        };

//        for (let nodeIndex in childNodes) {
//          window.console.log(1);
//          window.console.log(childNodes.length);
////          cursor += childNodes[nodeIndex].textContent.length ? childNodes[nodeIndex].textContent.length : 0;
//          window.console.log(2)
//          if (cursor > this.nowRange) {
//            window.console.log(3);
//            window.console.log(childNodes[nodeIndex].textContent.length);
//            let startEle = document.createElement("text");
//            startEle.textContent = childNodes[nodeIndex].textContent.substr(0, this.nowRange-(cursor-childNodes[nodeIndex].textContent.length));
////            window.console.log(startEle);
//            let endEle = document.createElement("text");
//            endEle.textContent = childNodes[nodeIndex].textContent.substr(this.nowRange-(cursor-childNodes[nodeIndex].textContent.length), cursor);
////            window.console.log(endEle);
//
//            let fileIndex = 0;
//            fileReader.readAsDataURL(imgFiles[fileIndex]);
//
//            fileReader.onload = function (res) {
//              let imgNode = document.createElement("img");
//              imgNode.setAttribute("src", fileReader.result);
//              imgNode.classList.add("upload-img");
////              ele.appendChild(imgNode);
//              ele.insertBefore(startEle, childNodes[nodeIndex]);
//              ele.insertBefore(imgNode, childNodes[nodeIndex]);
//              ele.insertBefore(endEle, childNodes[nodeIndex]);
//              ele.removeChild(childNodes[nodeIndex]);
//              that.nowRange += 1;
//              fileIndex += 1;
//              if (fileIndex < imgFiles.length) {
//                fileReader.readAsDataURL(imgFiles[fileIndex])
//              }
//            }
////            break
//          }
//        }
      }
    },
//    setRangeBlur: function () {
//      this.nowRange += 1;
//      window.console.log(this.nowRange)
//    },
    showEmojiDropDown: function () {
      this.isShowEmojiDropDown = !this.isShowEmojiDropDown;
      const ele = document.getElementsByClassName("text-area")[0];
      ele.focus();
      this.setRange(5);
      this.nowRange = this.getCurrentRange();
      window.console.log(5)
    },
    setRangePosition: function () {
      this.nowRange = this.getCurrentRange();
      window.console.log(this.nowRange);
    },
    listenMouseSelect: function (event) {
      const ele = document.getElementsByClassName("text-area")[0];
      const newRange = document.getElementsByClassName("text-area")[0].innerText.replace(/[\u0391-\uFFE5]/g,"aa").length;
      this.newRange = (newRange*7.7 + ele.offsetLeft + 8);
      this.newHeight = Math.floor(this.newRange / ele.clientWidth) + 25 + ele.offsetTop;
      this.nowRange = this.getCurrentRange();
      window.console.log(this.nowRange);
//      const currentDom = range.endContainer.nextSibling;
//      window.console.log(ele.innerText.split("$").length&1);

//      if (ele.childElementCount === 0) {
//        window.console.log(7979)
//        let newEle = document.createElement("p");
////        let newEleChild = document.createElement("text")
////        newEleChild.textContent = "&nbsp;"
////        newEle.appendChild(newEleChild)
//        newEle.innerText = "     "
//        ele.appendChild(newEle)
//      }

      if (event.data === null && (ele.innerText.split("$").length&1) === 0) {

        const stockList = document.getElementsByClassName("block");
        for (let eleIndex in stockList) {
//          window.console.log(stockList[eleIndex].innerText.substr(stockList[eleIndex].innerText.length-1, 1));
          if (stockList[eleIndex].innerText.substr(stockList[eleIndex].innerText.length-1, 1) !== "$") {
            stockList[eleIndex].parentNode.removeChild(stockList[eleIndex]);
            break
          }
        }
      }

      if ((ele.innerText.split("$").length&1) === 0) {
        this.isShowSearchBox = true;
//        window.console.log(this.isShowSearchBox);
//        this.insertHtml(event.data + "$", this.getCurrentRange());

        if (event.data === null) {
//          this.searchInput = ele.innerText.split("$")[ele.innerText.split("$").length-1];
          this.searchInput = this.searchInput.substr(0, this.searchInput.length-1);
          this.searchConnect();
        }
        else {
//          this.searchInput = ele.innerText.split("$")[ele.innerText.split("$").length-1];
          this.searchInput += (event.data === "$" ? "" : event.data);
//          window.console.log(ele.innerText.split("$"));
          this.searchConnect();
        }

      }
      else {
        this.isShowSearchBox = false;
        this.searchInput = "";
        if (event.data === null) {
//          window.console.log(event)
        }
      }
    },
    insertHtml: function (data, nowRange) {
      const ele = document.getElementsByClassName("text-area")[0];
      const text = ele.innerHTML;
//      const range = nowRange + data.length;
      const range = nowRange;
      const dataText = "$" + data.name + "(" + data.exchange_abbr.toUpperCase() + data.stock + ")$";
//      let html = text.split("$");
      let html = text.replace("$"+this.searchInput, dataText);
      window.console.log(data);
      html = html.replace(/\$(.+?)\$/g, "<a onselectstart='return false' href='/#/stock/" + data.exchange_abbr + "/" + data.stock + "/" + data.isIndex + "' style='text-decoration: none;' class='light-blue block' readonly='true'>\$ $1 \$</a>");
//      window.console.log(html);
//      html = text.replace(/\s+/g, " ");

      ele.innerHTML = html;
      window.console.log(this.nowRange)
      this.nowRange += dataText.length + 5;
      ele.focus();
      this.setRange(5);
      window.console.log(this.nowRange)


//      this.setRange(range);

    },
    insertEmoji: function (emoji) {

      const ele = document.getElementsByClassName("text-area")[0];
//      window.console.log(ele.childNodes[0].childNodes);
      let cursor = 0;
      let parent = ele.childNodes;
      window.console.log(parent);
      if (parent.length === 0) {
        let emojiEle = document.createElement("span");
        emojiEle.innerHTML = emoji;
        ele.appendChild(emojiEle);
      }
      else{
        for (let child in parent) {

          if ((cursor+parent[child].textContent.length) < this.nowRange ) {
            window.console.log(parent[child].textContent);
            cursor += parent[child].textContent.length;
          }
          else {
  //          parent[child].textContent = parent[child].textContent.slice(0, this.nowRange-cursor) + emoji + parent[child].textContent.slice(this.nowRange-cursor, parent[child].textContent.length);
            let emojiEle = document.createElement("span");
            emojiEle.innerHTML = parent[child].textContent.slice(0, this.nowRange-cursor) + emoji + parent[child].textContent.slice(this.nowRange-cursor, parent[child].textContent.length);
            ele.removeChild(parent[child]);
            ele.insertBefore(emojiEle, parent[child+1]);
            window.console.log(ele.childNodes);
            break
          }

        }
      }
      this.nowRange += 2;
      ele.focus();
      this.setRange(5);
      this.isShowEmojiDropDown = false;
    },
    getCurrentRange: function () {
      let currentOffSet = 0;
      const ele = document.getElementsByClassName("text-area")[0];
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const preRange = range.cloneRange();
        preRange.selectNodeContents(ele);
        preRange.setEnd(range.endContainer, range.endOffset);
        currentOffSet = preRange.toString().length;
      }
      return currentOffSet;
    },
    setRange: function (pos) {
      let range, selection;
      const ele = document.getElementsByClassName("text-area")[0];
//      range = document.createRange();
//      range.selectNodeContents(ele);
//      window.console.log(ele.childNodes);
//      if (ele.innerHTML.length > 0) {
//        range.setStart(ele.childNodes[0], pos);
//
//      }
//      range.collapse(true);
//      selection = window.getSelection();
//      selection.removeAllRanges();
//      selection.addRange(range)

      range = window.getSelection();
      range.selectAllChildren(ele);
      range.collapseToEnd();
    },
    choseStock: function (index) {
//      window.console.log(stock.split("-")[0]);
      this.isShowSearchBox = false;
      const data = this.searchAssociation[index];
//      window.console.log(data);
      this.insertHtml(data, 5);
      this.searchInput = "";
    },
    searchConnect: function() {
      const that = this;
      const targetUrl = "/api/searchAssociation?input=" + this.searchInput;
//      window.console.log(this.searchInput);
      this.$axios.get(targetUrl, {}).then(function (res){
        window.console.log(res);
        that.showChoices = true;
        that.searchAssociation = res.data;
      })
    },
  },
  mounted() {

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
