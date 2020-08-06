<template>
    <div class="calendar-holder">
        <div class="calendar-button" v-on:click="showBlock">
            <div class="calendar-icon">
                <img src="../assets/calendar.png"/>
            </div>
            <div class="calendar-date">
                {{ chosenDate }}
            </div>
        </div>
        <div class="calendar-block" v-if="isShowBlock">
            <div class="block-header">
                <div class="ctrl-btn" v-on:click.stop="resetCalendar" id="lastYear">
                    <<
                </div>
                <div class="ctrl-btn" v-on:click.stop="resetCalendar" id="lastMonth">
                    <
                </div>
                <div class="ctrl-time">
                    {{ nowYear }}年{{ nowMonth }}月
                </div>
                <div class="ctrl-btn" v-on:click.stop="resetCalendar" id="nextMonth">
                    >
                </div>
                <div class="ctrl-btn" v-on:click.stop="resetCalendar" id="nextYear">
                    >>
                </div>
            </div>
            <div class="block-center">
                <div class="center-header">
                    <div class="day">
                        一
                    </div>
                    <div class="day">
                        二
                    </div>
                    <div class="day">
                        三
                    </div>
                    <div class="day">
                        四
                    </div>
                    <div class="day">
                        五
                    </div>
                    <div class="day">
                        六
                    </div>
                    <div class="day">
                        日
                    </div>
                </div>
                <div class="center-center">
                    <div v-on:click.stop="choseDate" :class="'day day-hover ' + (item.isCurrentMonth ? 'current' : 'non-current') " v-for="(item, index) in dateArray" v-bind:key="index" :id="item.date" :style="(item.date == currentDate ? 'background-color: #CCFFFF' : '')">
                        {{ item.num }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Calendar',
        data () {
            return {
                chosenDate: "选择日期",
                isShowBlock: false,
            }
        },
        props: ['msg',],
        methods: {
            choseDate: function (event) {
                window.console.log(1)
                const date = event.path[0].id;
                this.$emit("setStartDate", this.msg + "|" + date);
                this.chosenDate = date;
                this.isShowBlock = false;
            },
            showBlock() {
                this.isShowBlock = !this.isShowBlock;
            },
            initCalendarParameter() {
                const newDate = new Date();
                this.nowYear = newDate.getFullYear();
                this.nowMonth = newDate.getMonth() + 1;
                this.nowDate = newDate.getDate();
                this.currentDate = this.nowYear + "-" + this.nowMonth + "-" + this.nowDate;
                this.chosenDate = this.msg.split("|")[1] == "start" ? "2019-1-1" : "2020-1-1"
            },
            setCalendar(year, month, date_) {
                const that = this;
                this.dayOfFirstDay = new Date(year, month-1, 1).getDay();
                this.dayOfLastDay = new Date(year, month, 0).getDay();
                this.dayNumOfMonth = new Date(year, month, 0).getDate();
                this.dayNumOfLastMonth = new Date(year, month-1, 0).getDate();
                this.dateArray = [];
                [...Array(this.dayNumOfMonth).keys()].forEach(function (date) {
                    that.dateArray.push({
                        "date": year + "-" + month + "-" + (date+1),
                        "num": date + 1,
                        "isCurrentMonth": true
                    })
                });
                try {
                    [...Array(this.dayOfFirstDay-1).keys()].forEach(function (date) {
                        that.dateArray.unshift({
                            "date": (month == 1 ? year - 1 : year) + "-" + (month == 1 ? 12 : month - 1) + "-" + (that.dayNumOfLastMonth - date),
                            "num": that.dayNumOfLastMonth - date,
                            "isCurrentMonth": false
                        })
                    });
                    [...Array(7-this.dayOfLastDay).keys()].forEach(function (date) {
                        that.dateArray.push({
                            "date": (month == 12 ? year + 1 : year) + "-" + (month == 12 ? 1 : month + 1) + "-" + (date+1),
                            "num": date+1,
                            "isCurrentMonth": false
                        })
                    })
                }
                catch (err) {
                    [...Array(6).keys()].forEach(function (date) {
                        that.dateArray.unshift({
                            "date": (month == 1 ? year - 1 : year) + "-" + (month == 1 ? 12 : month - 1) + "-" + (that.dayNumOfLastMonth - date),
                            "num": that.dayNumOfLastMonth - date,
                            "isCurrentMonth": false
                        })
                    });
                    [...Array(6).keys()].forEach(function (date) {
                        that.dateArray.push({
                            "date": (month == 12 ? year + 1 : year) + "-" + (month == 12 ? 1 : month + 1) + "-" + (date+1),
                            "num": date+1,
                            "isCurrentMonth": false
                        })
                    })
                }

//                this.dateArray = this.dateArray;
                this.$forceUpdate();
//                window.console.log(this.dateArray)
            },
            resetCalendar (event) {
                event.stopPropagation();
                event.preventDefault();
//                window.console.log(event.path[0].id)
                const changeOrder = event.path[0].id;
//                const nowChosenDate = new Date(this.nowYear+"/"+(this.nowMonth-1)+"/"+this.nowDate)

//                window.console.log(nowChosenDate.getFullYear()+"-"+nowChosenDate.getMonth()+"-"+nowChosenDate.getDate())
//                const orderMap = {
//                    "lastMonth": new Date(nowChosenDate.setMonth(nowChosenDate.getMonth() - 1)),
//                    "nextMonth": new Date(nowChosenDate.setMonth(nowChosenDate.getMonth() + 1)),
//                    "lastYear": new Date(nowChosenDate.setFullYear(nowChosenDate.getFullYear() - 1)),
//                    "nextYear": new Date(nowChosenDate.setFullYear(nowChosenDate.getFullYear() + 1)),
//                }
////                window.console.log(new Date(nowChosenDate.setFullYear(nowChosenDate.getFullYear() + 1)))
//                this.nowYear = orderMap[changeOrder].getFullYear();
//                this.nowMonth = orderMap[changeOrder].getMonth()+1;
//                this.nowDate = orderMap[changeOrder].getDate();
//                window.console.log(this.nowYear+"-"+this.nowMonth+"-"+this.nowDate);

                if (changeOrder == "lastMonth") {
                    this.nowYear = (this.nowMonth == 1 ? this.nowYear-1 : this.nowYear);
                    this.nowMonth = (this.nowMonth == 1 ? 12 : this.nowMonth - 1);
//                    this.nowDate = 1;
                }
                else if (changeOrder == "nextMonth") {
                    this.nowYear = (this.nowMonth == 12 ? this.nowYear + 1 : this.nowYear);
                    this.nowMonth = (this.nowMonth == 12 ? 1 : this.nowMonth + 1);
//                    this.nowDate = 1;
                }
                else if (changeOrder == "lastYear") {
                    this.nowYear = this.nowYear - 1;
//                    this.nowDate = 1;
                }
                else {
                    this.nowYear = this.nowYear + 1;
//                    this.nowDate = 1;
                }

                const daysNumOfMonth = new Date(this.nowYear, this.nowMonth, 0).getDate();
                this.nowDate = (daysNumOfMonth < this.nowDate ? daysNumOfMonth : this.nowDate)

//                window.console.log(this.nowYear+"-"+this.nowMonth+"-"+this.nowDate);
                this.setCalendar(this.nowYear, this.nowMonth, this.nowDate);
            }
        },
        mounted() {
            this.initCalendarParameter();
            this.setCalendar(this.nowYear, this.nowMonth, this.nowDate);
        }

    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .calendar-holder {
        width: 120px;
        height: 25px;
        line-height: 25px;
        z-index: 9999;
        /*background-color: green;*/
    }

    .calendar-button {
        width: 100%;
        height: 100%;
        display: flex;
        display: -webkit-flex;
        border: 1px solid #ebecf1;
        border-radius: 4px;
    }

    .calendar-button img {
        width: 18px;
        height: 18px;
        margin-top: 3px;
        margin-left: 3px;
    }

    .calendar-date {
        width: 100px;
        height: 25px;
        margin-left: 2px;
    }

    .calendar-icon {
        width: 25px;
        height: 25px;
    }

    .calendar-block {
        width: 240px;
        /*height: 280px;*/
        /*background-color: pink;*/
        display: flex;
        display: -webkit-flex;
        flex-direction: column;
        border-radius: 5px;
        border: 1px solid #ebecf1;
        box-sizing: border-box;
        padding: 10px;
        font-size: 90%;
        z-index: 99;
        background-color: white;
    }

    .block-header {
        display: flex;
        display: -webkit-flex;
        justify-content: space-between;
        padding-left: 5px;
        padding-right: 5px;
    }

    .ctrl-btn {
        /*background-color: red;*/
        width: 20px;
        border-radius: 3px;
    }

    .ctrl-btn:hover {
        background-color: #CCFFFF;
    }

    .block-center {
        display: flex;
        display: -webkit-flex;
        flex-direction: column;
    }

    .center-header {
        display: flex;
        display: -webkit-flex;
        justify-content: space-between;
    }

    .center-center {
        display: flex;
        display: -webkit-flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .day {
        width: 13.5%;
        line-height: 35px;
        border-radius: 3px;
    }

    .day-hover:hover {
        background-color: #CCFFFF;

    }

    .non-current {
        color: #a6a9b6;
    }

    .btn {
        display: flex;
        display: -webkit-flex;
    }
</style>
