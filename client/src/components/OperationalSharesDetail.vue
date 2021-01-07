<template>
  <div class="root">
    <div class="content-nav">
      <div class="nav-left">
        <div :class="'nav-button ' + (nowChosenButton === 'all' ? 'chosen-button' : '')" v-on:click="slelectOperationalsharesBlock('all')">
          自选股票
        </div>
        <div :class="'nav-button ' + (nowChosenButton === 'group' ? 'chosen-button' : '')" v-on:click="slelectOperationalsharesBlock('group')">
          自选组合
        </div>
      </div>
      <div class="nav-right">
        <div class="create-button" v-if="(nowChosenButton === 'group' && !groupCreateIsSuccess)" v-on:click="showCreateGroupBlock">
          创建组合
        </div>
        <div class="ban-create-button" v-if="(nowChosenButton === 'group' && groupCreateIsSuccess)" v-on:click="showCreateGroupBlock">
          取消创建
        </div>
      </div>
    </div>

    <div class="content-wrap" v-show="!isShow">
      <div class="content-holder">
        <div class="content-header">
          <div class="header-button" v-on:click="showAllChoices">
            <p id="all">
              {{ selectParamsCn[nowChosenChoice] }}
            </p>
            <svg t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>
          <div class="all-choices" v-if="isShowAllChoices">
            <div class="choice-btn" v-on:click="changeStocks('all')">
              全部
            </div>
            <div class="choice-btn" v-on:click="changeStocks('hs')">
              沪深
            </div>
            <div class="choice-btn" v-on:click="changeStocks('hk')">
              港股
            </div>
            <div class="choice-btn" v-on:click="changeStocks('us')">
              美股
            </div>
          </div>
          <div class="header-button" v-on:click="changePriceSort('price')">
            <p>
              当前价
            </p>
            <!--          <i class="icon" style="background: url('../assets/sort_none.png') no-repeat center"></i>-->

            <svg v-if="nowChosenSort === 'price' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'price' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button" v-on:click="changePriceSort('chg')">
            <p>
              涨跌幅
            </p>
            <svg v-if="nowChosenSort === 'chg' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'chg' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button" v-on:click="changePriceSort('threeMonth')">
            <p>
              近3个月
            </p>
            <svg v-if="nowChosenSort === 'threeMonth' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'threeMonth' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button" v-on:click="changePriceSort('sixMonth')">
            <p>
              近6个月
            </p>
            <svg v-if="nowChosenSort === 'sixMonth' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'sixMonth' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button" v-on:click="changePriceSort('twelveMonth')">
            <p>
              近12个月
            </p>
            <svg v-if="nowChosenSort === 'twelveMonth' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'twelveMonth' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>
        </div>

        <div class="content-center" v-if="startToShow">
          <div class="content-line" v-for="(item, index) in operationalSharesList" v-bind:key="index">
            <div class="line-button" v-on:click="jumpToStock(item.fields.exchange, item.fields.stock_code, item.fields.type)" style="cursor: pointer">
              <div class="button-top">
                {{ item.fields.name_cn }}
              </div>
              <div class="button-down">
                {{ item.fields.stock_code }}
              </div>
            </div>
            <div class="line-button">
              {{ item.fields.price }}
            </div>
            <div :class="'line-button ' + (item.fields.chg > 0 ? 'red' : 'green')">
              {{ item.fields.chg }}%
            </div>
            <div :class="'line-button ' + ((item.fields.price - item.fields.threeMonth) < 0 ? 'green' : 'red')">
              {{ ((item.fields.price - item.fields.threeMonth) / item.fields.price * 100).toFixed(2) }}%
            </div>
            <div :class="'line-button ' + ((item.fields.price - item.fields.sixMonth) < 0 ? 'green' : 'red')">
              {{ ((item.fields.price - item.fields.sixMonth) / item.fields.price * 100).toFixed(2) }} %
            </div>
            <div :class="'line-button ' + ((item.fields.price - item.fields.twelveMonth) > 0 ? 'red' : 'green')">
              {{ ((item.fields.price - item.fields.twelveMonth) / item.fields.price * 100).toFixed(2) }}%
            </div>
          </div>
        </div>

        <div class="content-center" v-else>
          <div class="content-line">
            <p>还没有添加自选股</p>
          </div>
        </div>
      </div>
    </div>

    <div class="content-wrap" v-show="isShow">
      <OperationalSharesGroupCreate @groupCreated="groupCreateResult" v-if="groupCreateIsSuccess"></OperationalSharesGroupCreate>
      <div class="content-holder">
        <div class="content-header">
          <div class="header-button group-header-button" v-on:click="showAllChoices">
            <p id="all">
              {{ selectParamsCn[nowChosenChoice] }}
            </p>
            <svg t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>
          <div class="all-choices" v-if="isShowAllChoices">
            <div class="choice-btn" v-on:click="changeStocks('all')">
              全部
            </div>
            <div class="choice-btn" v-on:click="changeStocks('hs')">
              沪深
            </div>
            <div class="choice-btn" v-on:click="changeStocks('hk')">
              港股
            </div>
            <div class="choice-btn" v-on:click="changeStocks('us')">
              美股
            </div>
          </div>

          <div class="header-button group-header-button" v-on:click="changePriceSort('change')">
            <p>
              日收益
            </p>
            <svg v-if="nowChosenSort === 'change' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'change' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button group-header-button" v-on:click="changePriceSort('chg')">
            <p>
              月收益
            </p>
            <svg v-if="nowChosenSort === 'chg' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'chg' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>

          <div class="header-button group-header-button" v-on:click="changePriceSort('volume')">
            <p>
              总收益
            </p>
            <svg v-if="nowChosenSort === 'volume' && nowSortIndex === 1" t="1599631634411" class="icon" viewBox="0 0 1820 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11386" width="200" height="200"><path d="M1625.884444 965.404444H149.162667c-126.065778 0-154.737778-72.362667-65.649778-161.564444L725.902222 161.564444a228.693333 228.693333 0 0 1 323.128889 0l642.389333 642.275556c88.974222 89.088 59.847111 161.564444-65.649777 161.564444z" fill="#0066cc" p-id="11387"></path></svg>
            <svg v-else-if="nowChosenSort === 'volume' && nowSortIndex === 2" t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#0066cc" p-id="14601"></path></svg>
            <svg v-else t="1599631760752" class="icon" viewBox="0 0 1638 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14600" width="200" height="200"><path d="M822.0672 1024a98.7136 98.7136 0 0 1-75.1616-35.2256L26.0096 149.9136A109.9776 109.9776 0 0 1 33.3824 0h1570.816c41.7792 39.3216 44.8512 106.496 7.3728 149.9136l-714.752 838.8608A97.6896 97.6896 0 0 1 822.272 1024z" fill="#707070" p-id="14601"></path></svg>
          </div>
        </div>
        <div class="content-center" v-if="startToShowGroup">
          <div class="content-line" v-for="(item, index) in operationalSharesGroupList" v-bind:key="index">
            <div class="line-button group-line-button">
              <div class="button-top">
                {{ item.fields.group_name }}
              </div>
              <div class="button-down">
                {{ selectParamsCn[item.fields.exchange] }}
              </div>
            </div>
            <div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">
              {{ item.dayGrowth }}%
            </div>
            <div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">
              {{ item.monthGrowth }}%
            </div>
            <div :class="'line-button group-line-button ' + (item.wholeGrowth > 0 ? 'red' : 'green')">
              {{ item.wholeGrowth }}%
            </div>
          </div>
        </div>

        <div class="content-center" v-else>
          <div class="content-line">
            <p>还没有创建组合</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import OperationalSharesGroupCreate from "./OperationalSharesGroupCreate.vue"
  export default {
    name: "OperationalSharesDetail.vue",
    components: {
      OperationalSharesGroupCreate
    },
    data () {
      return {
        nowChosenButton: "all",
        isShowContent: false,
        groupRawData: [],
        operationalSharesList: [],
        operationalSharesGroupList: [],
        informationList: [],
        dataDict: {},
        groupCreateIsSuccess: false,
        startToShow: false,
        startToShowGroup: false,
        isShowAllChoices: false,
        nowShowStocks: ["us", "hs", "hk"],
        selectParams: {
          "us": "us",
          "sz": "hs",
          "sh": "hs",
          "hk": "hk"
        },
        selectParamsCn: {
          "us": "美股",
          "hk": "港股",
          "hs": "沪深",
          "all": "全部"
        },
        nowChosenChoice: "all",
        nowSortIndex: 0,
        nowChosenSort: "",
        userCode: "",
        isShow: false,
        groupDict: {},
        itemDataDict: {},
        promiseFlag: 0,
        monthData: {},
        dataDone: 0,
        itemDataDone: 0,
      }
    },
    methods: {

      slelectOperationalsharesBlock: function (type) {
        this.nowChosenButton = type;
        if (this.nowChosenButton == "group") {
          this.isShow = true;
          this.getOperationalGroupInfo();
        }
        else {
          this.isShow = false;
        }
      },
      jumpToStock: function (exchange, stock, type) {
       const newPage = this.$router.resolve({
        name: "StockPage",
        params: {
          type: type,
          exchange: exchange,
          stock: stock,
        }
      });
      window.open(newPage.href,'_blank')
      },
      showCreateGroupBlock: function () {
        this.groupCreateIsSuccess = !this.groupCreateIsSuccess;
      },
      groupCreateResult: function (res) {
        if (res) {
          this.groupCreateIsSuccess = false;
          this.getOperationalGroupInfo();
        }
      },
      calculateItemData: function () {
        for (let groupIndex in this.operationalSharesGroupList) {
          let items = this.groupDict[this.operationalSharesGroupList[groupIndex].fields.group_code];
          let dayGrowth = 0;
          let monthGrowth = 0;
          let wholeGrowth = 0;
          for (let itemIndex in items) {
            let nowPrice = parseFloat(this.itemDataDict[itemIndex]["price"])
            let nowChg = parseFloat(this.itemDataDict[itemIndex]["chg"])
            let nowVolume = parseFloat(items[itemIndex]["now_volume"])
            let monthPrice = parseFloat(this.monthData[itemIndex])
            let salePrice = parseFloat(items[itemIndex]["sale_price"])
            window.console.log(monthPrice)
            window.console.log(monthPrice)
            dayGrowth += (nowChg * nowVolume / 100);
            monthGrowth += ((nowPrice - monthPrice) * nowVolume / 100);
            wholeGrowth += ((nowPrice - salePrice) * nowVolume / 100);
          }
          let todayDate = new Date();
          let todayString = todayDate.getFullYear() + "-" + ((todayDate.getMonth() + 1) > 9 ? (todayDate.getMonth() + 1) : "0"+(todayDate.getMonth() + 1)) + "-" + todayDate.getDate() > 9 ? todayDate.getDate() : "0"+todayDate.getDate();
          let createString = this.operationalSharesGroupList[groupIndex].fields.create_date.split("T")[0];
          if (todayString == createString) {
            monthGrowth = dayGrowth;
            wholeGrowth = dayGrowth
          }
          this.operationalSharesGroupList[groupIndex].dayGrowth = dayGrowth.toFixed(2);
          this.operationalSharesGroupList[groupIndex].monthGrowth = monthGrowth.toFixed(2);
          this.operationalSharesGroupList[groupIndex].wholeGrowth = wholeGrowth.toFixed(2);
          this.dataDone = 0;
          this.$forceUpdate();
          //this.operationalSharesGroupList[groupIndex].fields.chg = this.itemDataDict[]
        }
      },
      getOperationalGroupInfo: function () {
        const that = this;
        this.$axios.get("/api/optionalSharesGroup?userCode=" + this.userCode, {}).then(function (res) {
          if (res.data === 404) {
            that.startToShowGroup = false
          }
          else {
            that.startToShowGroup = true;
            that.operationalSharesGroupList = res.data;
            let groupIdParams = ""
            for (let groupIndex in that.operationalSharesGroupList) {
              //that.groupDict[that.operationalSharesGroupList[groupIndex].fields.group_code] = {};
              //that.getOpretaionalItemInfo(that.operationalSharesGroupList[groupIndex].fields.group_code, that);
              groupIdParams += (that.operationalSharesGroupList[groupIndex].fields.group_code + ",");

            }
            that.getOpretaionalItemInfo(groupIdParams, that)
          }
        })
      },
      getStockMonthPrice: function (stockCodes, createDates) {
        const that = this;
        let targetUrl = "/api/daily?stockCodes=" + stockCodes + "&createDates=" + createDates;
        this.$axios.get(targetUrl, {}).then(function (res) {
          that.monthData = res.data;
          that.dataDone += 1;
          window.console.log(that.dataDone)
        })
      },
      getStockTodayPrice: function (stockCodes, func) {
        let targetUrl = "/gu/q=" + stockCodes;
        const that = this;
        this.$axios.get(targetUrl, {}).then(function (res) {
          window.console.log(res)
          const data = res.data.split(";");
          data.pop();
          window.console.log(data)
          func(data, that);
        })
      },
      getStockHistoryData: function (stockCodes, date, func, field) {
        const that = this;
        let targetUrl = "/api/daily?stockCodes=" + stockCodes + "&date=" + date;
        this.$axios.get(targetUrl, {}).then(function (res) {
          func(res.data, that, field)
          window.console.log(that.operationalSharesList)
        })
      },
      getOpretaionalItemInfo: function (groupCodes, that) {
        that.$axios.get("/api/optionalSharesItem?groupCodes=" + groupCodes, {}).then(function (res) {
          that.groupDict = res.data;
          let stockCodes = "";
          let createDates = ""
          for (let groupIndex in that.groupDict) {
            for (let stockIndex in that.groupDict[groupIndex]) {
              stockCodes += (that.groupDict[groupIndex][stockIndex]["exchange"] + stockIndex + ",")
              createDates += (that.groupDict[groupIndex][stockIndex]["create_date"] + ",")
            }
          }
          const putDataInDailyList = function (data, that) {
            for (let stockIndex in data) {
              window.console.log(data[stockIndex].length)
              if (!that.itemDataDict[data[stockIndex].split("~")[2]] && data[stockIndex].length > 1) {
                that.itemDataDict[data[stockIndex].split("~")[2]] = {};
                that.itemDataDict[data[stockIndex].split("~")[2]]["price"] = data[stockIndex].split("~")[3];
                that.itemDataDict[data[stockIndex].split("~")[2]]["chg"] = data[stockIndex].split("~")[32];
              }    
            }
            that.dataDone += 1;
          }

          that.getStockTodayPrice(stockCodes, putDataInDailyList);
          that.getStockMonthPrice(stockCodes, createDates);
        })
      },
      changePriceSort: function (sort) {
        this.nowSortIndex === 2 ? this.nowSortIndex = 0 : this.nowSortIndex += 1;
        this.nowChosenSort = sort;

        if (this.nowSortIndex === 0) {
          this.operationalSharesList.sort();
          this.nowChosenSort = "";
        }
        else if (this.nowSortIndex === 1) {
          window.console.log(this.operationalSharesList)
          if (sort === "chg" || sort === "price") {
            this.operationalSharesList.sort(function (a, b) {
              return parseFloat(a.fields[sort]) - parseFloat(b.fields[sort])
            })
          }
          else {
            this.operationalSharesList.sort(function (a, b) {
              return ((a.fields[sort] - parseFloat(a.fields["price"])) / parseFloat(a.fields["price"])) - ((b.fields[sort] - parseFloat(b.fields["price"])) / parseFloat(b.fields["price"]))
            })
          }
          
        }
        else {
          if (sort === "chg" || sort === "price") {
            this.operationalSharesList.sort(function (a, b) {
              return parseFloat(b.fields[sort]) - parseFloat(a.fields[sort])
            })
          }
          else {
            this.operationalSharesList.sort(function (a, b) {
              return ((b.fields[sort] - parseFloat(b.fields["price"])) / parseFloat(b.fields["price"])) - ((a.fields[sort] - parseFloat(a.fields["price"])) / parseFloat(a.fields["price"]))
            })
          }
          
        }
      },
      changeStocks: function (exchange) {
        if (exchange === "all") {
          this.nowShowStocks = ["us", "hs", "hk"]
        }
        else {
          this.nowShowStocks = [exchange]
        }

        this.nowChosenChoice = exchange;
        window.console.log(this.selectParamsCn[this.nowChosenChoice])
      },
      showAllChoices: function () {
        this.isShowAllChoices = !this.isShowAllChoices;
      },
      getOperationalShares: function () {
        const that = this;
        const userCode = this.$cookie.get("userCode");
        this.$axios.get("/api/optionalShares?userCode=" + userCode, {}).then(function (res){
          if (res.data === 404) {
            that.startToShow = false
          }
          else {
            window.console.log(4242)
            window.console.log(res.data)
            that.operationalSharesList = res.data;
            let stockCodes = "";
            
            for (let itemIndex in that.operationalSharesList) {
              stockCodes += that.operationalSharesList[itemIndex].fields.exchange + that.operationalSharesList[itemIndex].fields.stock_code.split(".")[0] + ","
            }

            const putDailyDataInList = function (data, that) {
              window.console.log(that.operationalSharesList)
              for (let stockIndex in data) {
                that.operationalSharesList[stockIndex].fields["price"] = data[stockIndex].split("~")[3]
                that.operationalSharesList[stockIndex].fields["chg"] = data[stockIndex].split("~")[32]
                that.operationalSharesList[stockIndex].fields["type"] = data[stockIndex].split("~")[61]
              }
              that.itemDataDone += 1;
              window.console.log(that.itemDataDone)
              window.console.log(that.startToShow)
            }

            const today = new Date();
            const threeMonthsAgo = new Date(today.valueOf() - 3600 * 1000 * 24 * 90);
            const threeMonthsAgoStr = threeMonthsAgo.getFullYear().toString() + (threeMonthsAgo.getMonth() + 1 > 9 ? (threeMonthsAgo.getMonth() + 1) : "0" + (threeMonthsAgo.getMonth() + 1)).toString() + (threeMonthsAgo.getDate() > 9 ? threeMonthsAgo.getDate() : "0" + threeMonthsAgo.getDate()).toString()
            const sixMonthsAgo = new Date(today.valueOf() - 3600 * 1000 * 24 * 180);
            const sixMonthsAgoStr = sixMonthsAgo.getFullYear().toString() + (sixMonthsAgo.getMonth() + 1 > 9 ? (sixMonthsAgo.getMonth() + 1) : "0" + (sixMonthsAgo.getMonth() + 1)).toString() + (sixMonthsAgo.getDate() > 9 ? sixMonthsAgo.getDate() : "0" + sixMonthsAgo.getDate()).toString()
            const twelveMonthsAgo = new Date(today.valueOf() - 3600 * 1000 * 24 * 360);
            const twelveMonthsAgoStr = twelveMonthsAgo.getFullYear().toString() + (twelveMonthsAgo.getMonth() + 1 > 9 ? (twelveMonthsAgo.getMonth() + 1) : "0" + (twelveMonthsAgo.getMonth() + 1)).toString() + (twelveMonthsAgo.getDate() > 9 ? twelveMonthsAgo.getDate() : "0" + twelveMonthsAgo.getDate()).toString()

            const putMonthDataInList = function (data, that, field) {
              for (let stockIndex in data) {
                that.operationalSharesList[stockIndex].fields[field] = data[stockIndex]
              }
              that.itemDataDone += 1;
              window.console.log(that.itemDataDone)
              window.console.log(that.startToShow)
            }

            that.getStockTodayPrice(stockCodes, putDailyDataInList)
            that.getStockHistoryData(stockCodes, threeMonthsAgoStr, putMonthDataInList, "threeMonth");
            that.getStockHistoryData(stockCodes, sixMonthsAgoStr, putMonthDataInList, "sixMonth");
            that.getStockHistoryData(stockCodes, twelveMonthsAgoStr, putMonthDataInList, "twelveMonth");

          }
        })
      },
      getNowPrice: function (that) {
        //let targetUrl = "/gu/q="
        //for (let stockIndex in that.operationalSharesList) {
        //  if (that.operationalSharesList[stockIndex].fields.exchange === "sz" || that.operationalSharesList[stockIndex].fields.exchange === "sh") {
        //    targetUrl += "s_" + that.operationalSharesList[stockIndex].fields.exchange + that.operationalSharesList[stockIndex].fields.stock_code + ","
        //  }
        //  else if (that.operationalSharesList[stockIndex].fields.exchange === "us") {
        //    let stock = that.operationalSharesList[stockIndex].fields.stock_code.toLowerCase().split(".")[0];
        //    targetUrl += "s_us" + stock.toUpperCase() + ","
        //  }
        //  else if (that.operationalSharesList[stockIndex].fields.exchange === "hk") {
        //    targetUrl += "s_" + that.operationalSharesList[stockIndex].fields.exchange + that.operationalSharesList[stockIndex].fields.stock_code + ","
        //  }
        //}
        //let stockCodes = ""
        //for (let itemIndex in that.)

        that.$axios.get(targetUrl, {}).then(function (res){

          const data = res.data.split(";");
          data.pop();
          for (let stockIndex in data) {
            that.informationList.push([data[stockIndex].split("~")[3], data[stockIndex].split("~")[4], data[stockIndex].split("~")[5], data[stockIndex].split("~")[6], data[stockIndex].split("~")[2], data[stockIndex].split("~")[1], data[stockIndex].split("_")[2].substring(0, 2)])
          }

          const today = new Date();
          const yearsAgo = new Date(today.valueOf() - 3600 * 1000 * 24 * 365);
          const yearsAgoCursor = new Date(today.valueOf() - 3600 * 1000 * 24 * 375);
          const yearsAgoCursorStr = yearsAgoCursor.getFullYear() + "-" + (yearsAgoCursor.getMonth()+1 > 9 ? (yearsAgoCursor.getMonth()+1) : "0"+(yearsAgoCursor.getMonth()+1)) + "-" + (yearsAgoCursor.getDate() > 9 ? yearsAgoCursor.getDate() : "0"+yearsAgoCursor.getDate())
          const yeasAgoStr = yearsAgo.getFullYear() + "-" + (yearsAgo.getMonth()+1 > 9 ? (yearsAgo.getMonth()+1) : "0"+(yearsAgo.getMonth()+1)) + "-" + (yearsAgo.getDate() > 9 ? yearsAgo.getDate() : "0"+yearsAgo.getDate())
          let targetUrl;

          for (let stockIndex in that.operationalSharesList) {
            let fullCode = that.operationalSharesList[stockIndex].fields.exchange + that.operationalSharesList[stockIndex].fields.stock_code;
            if (that.operationalSharesList[stockIndex].fields.exchange === "sz" || that.operationalSharesList[stockIndex].fields.exchange === "sh") {
              targetUrl = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=" + fullCode + ",day," + yearsAgoCursorStr + "," + yeasAgoStr + ",1,qfq";
            }
            else if (that.operationalSharesList[stockIndex].fields.exchange === "hk") {
              targetUrl = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=" + fullCode + ",day," + yearsAgoCursorStr + "," + yeasAgoStr + ",1,qfq";
            }
            else if (that.operationalSharesList[stockIndex].fields.exchange === "us") {
              targetUrl = "http://web.ifzq.gtimg.cn/appstock/app/usfqkline/get?_var=kline_dayqfq&param=" + fullCode + ",day," + yearsAgoCursorStr + "," + yeasAgoStr + ",1,qfq";
            }

            that.$axios.get(targetUrl, {}).then(function (res){
              that.dataDict[that.operationalSharesList[stockIndex].fields.stock_code] = JSON.parse(res.data.split("=")[1])["data"][fullCode]["qfqday"][0][2];
              for (let index in that.informationList) {
                if (that.informationList[index][4] === that.operationalSharesList[stockIndex].fields.stock_code) {
                  that.informationList[index].push((parseFloat(that.informationList[index][0]) - parseFloat(JSON.parse(res.data.split("=")[1])["data"][fullCode]["qfqday"][0][2])) / parseFloat(JSON.parse(res.data.split("=")[1])["data"][fullCode]["qfqday"][0][2]))
                }
              }
              if (that.operationalSharesList.length === Object.keys(that.dataDict).length) {
                that.startToShow = true;
              }
            })
          }
          that.informationList.sort();
        })

        // while (true) {
        //   if (that.operationalSharesList.length === Object.keys(that.dataDict).length) {
        //     that.startToShow = true;
        //     that.$forceUpdate();
        //     break
        //   }
        //
        // }
      }
    },
    mounted() {
      this.userCode = this.$cookie.get("userCode");
      if (!this.userCode) {
        const newPage = this.$router.resolve({
          name: "Login",
        });
        window.open(newPage.href,'_self')
      }
      else {
        this.getOperationalShares();
        document.addEventListener('click', (e)=> {
          if (e.target.id != 'all') {
            this.isShowAllChoices = false;
          }
        })
      }
    },
    watch: {
      dataDone(val) {
        if (this.dataDone == 2) {
          this.calculateItemData();
        }
      },
      itemDataDone(val) {
        if (this.itemDataDone == 4) {
          this.startToShow = true;
          this.$forceUpdate()
        }
      }
    }
  }
</script>

<style scoped>

  .root {
    width: 100%;
    min-height: 600px;
  }

  .content-nav {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: space-around;
  }

  .nav-left {
    width: 60%;
    height: 100%;
    /*border-bottom: 1px solid #F6F6F6;*/
    display: flex;
    justify-content: flex-start;
  }

  .nav-right {
    width: 40%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
    /*background-color: black;*/
  }

  .create-button {
    width: 80px;
    height: 28px;
    margin-top: 7px;
    line-height: 28px;
    background-color: #0084FF;
    color: white;
    border-radius: 3px;
    font-size: 95%;
    cursor: pointer;
  }

  .ban-create-button {
    width: 80px;
    height: 28px;
    margin-top: 7px;
    line-height: 28px;
    background-color: #E24528;
    color: white;
    border-radius: 3px;
    font-size: 95%;
    cursor: pointer;
  }

  .nav-button {
    width: 80px;
    height: 100%;
    line-height: 40px;
    cursor: pointer;
  }

  .chosen-button {
    border-bottom: 2px solid #0084ff;
    color: #06c;
  }

  .content-wrap {
    width: 100%;
    /*border: 1px solid #F6F6F6;*/
    display: flex;
    flex-direction: column;
    margin-top: 2px;
  }

  .content-holder {
    width: 100%;
    border: 1px solid #F6F6F6;
    display: flex;
    flex-direction: column;
    margin-top: 2px;
  }

  .content-header {
    width: 100%;
    height: 44px;
    background-color: #F6F6F6;
    display: flex;
  }

  .content-center {
    width: 100%;
    /*border: 1px solid #F6F6F6;*/
  }

  .content-line {
    width: 100%;
    height: 44px;
    display: flex;
    border-top: 1px solid #F6F6F6;
  }

  .header-button {
    width: 15%;
    height: 44px;
    line-height: 44px;
    text-align: start;
    text-indent: 20px;
    font-size: 95%;
    display: flex;
    cursor: pointer;
    user-select:none;
  }

  .group-header-button {
    width: 20%!important;
  }

    .header-button:hover {
      background-color: #F9F9F9;
    }


  .icon {
    width: 10px;
    height: 5px;
    margin-top: 20px;
    margin-left: 3px;
  }

  .header-button i {
    width: 10px;
    height: 20px !important;
  }

  .line-button {
    width: 15%;
    height: 44px;
    line-height: 44px;
    text-align: start;
    text-indent: 20px;
    font-size: 90%;
  }

  .group-line-button {
    width: 20%!important;
  }

  .button-top {
    height: 50%;
    line-height: 28px !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .button-down {
    height: 50%;
    line-height: 20px !important;
    color: #a6a9b6;
  }

  .green {
    color: #009933;
  }

  .red {
    color: #E24528;
  }

  .content-line p {
    display: inline-block;
    width: 100%;
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-size: 95%;
  }

  .all-choices {
    width: 120px;
    height: 165px;
    background-color: white;
    box-shadow: 1px 1px 4px rgba(120, 120, 120, 0.9);
    position: absolute;
    /*left: -90px;*/
    top: 178px;
    border-radius: 3px;
  }

  .choice-btn {
    width: 100%;
    height: 40px;
    line-height: 40px;
    border-bottom: 1px solid #F6F6F6;
    cursor: pointer;
    text-align: left;
    text-indent: 20px;
    font-size: 95%;
  }

    .choice-btn:hover {
      background-color: #F6F6F6;
    }
</style>
