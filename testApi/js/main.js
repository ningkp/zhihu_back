var weekStartDate;
var weekEndDate;



// Vue.config.debug = true;//在上线之前删掉这一行


var leftTopBox = new Vue({
    el: '#leftTopBox',
    data: {
        login: false,
        userdata: Object(),
        imgurl: window.localStorage['imgurl'],
        name: null,
        passerror: false,
    }
});
var navbar = new Vue({
    el: '#navbar',
    data: {
        login: false,
        name: null,
    }
});

var xk_enter = new Vue({
    el: '#xk-enter',
    data: {
        title: "",
        content: "",
        planType: "",
        beginTime: "",
        beginTimes: [],
        Interval:null,
        time: "",
        nowTime: -1,
        day: "",
        hour: "",
        min: "",
        sec: "",
        currentSchedule: "",
        count: 0,
        canEnter: false,
    },
    ready: function() {
        var self = this;
        self.Interval = setInterval(testTime,100,self);
        function runTime(arg) {
            if(self.nowTime == -1) {
                self.count = 0;
                clearInterval(self.Interval);
                self.Interval = setInterval(testTime,100,self);
            }
            else {
                var nowTime = moment();
                nowTime = nowTime.toDate();
                var now = self.nowTime;
                var passTime = moment(arg.beginTimes[now].beginTime);
                passTime = passTime.toDate();
                nowTime = Math.floor(nowTime.getTime() / 1000) + delayTime;
                passTime = Math.floor(passTime.getTime() / 1000);
                var total = passTime - nowTime;
                var day = parseInt(total / (24*60*60));
                var afterDay = total - day*24*60*60;
                var hour = parseInt(afterDay/(60*60));
                var afterHour = total - day*24*60*60 - hour*60*60;
                var min = parseInt(afterHour/60);
                var afterMin = total - day*24*60*60 - hour*60*60 - min*60;
                var subTime = day + "day" + hour + "hour" + min + "min" + afterMin + "sec";
                self.time = subTime;
                self.day = day;
                self.hour = hour;
                self.min = min;
                self.sec = afterMin;
                if(self.count == 0) {
                    self.count = 1;
                }
            }
        }
        function testTime(self) {
            if(!self.beginTimes.length) {
                return ;
            }
            var i;
            var totalTime = self.beginTimes.length;
            var nowTime = moment();
            nowTime = nowTime.toDate();
            nowTime = Math.floor(nowTime.getTime() / 1000) + delayTime;
            for(i = 0;i < totalTime;i++) {
                var passTime = moment(self.beginTimes[i].beginTime);
                passTime = passTime.toDate();
                passTime = Math.floor(passTime.getTime() / 1000);
                if(nowTime < passTime) {
                    clearInterval(self.Interval);
                    self.nowTime = i;
                    self.Interval = setInterval(runTime,1000,self);
                    switch(self.beginTimes[i].stage) {
                        case 20:
                            self.currentSchedule = "进入初选";
                            break;
                        case 60:
                            self.currentSchedule = "进入复选";
                            break;
                        case 80:
                            self.currentSchedule = "查看最终结果";
                            break;
                        case 100:
                            self.currentSchedule = "进入抢课";
                            break; 
                        default :
                            self.currentSchedule = "";
                            break;
                    }
                    break;
                }
            }
            if(i==totalTime){        
                self.count = 0;
                self.nowTime = 0;
            }
        }
        
    },
    methods:{
        enter: function(event) {
            enterXk();
        }
    },
});

var xk_date = new Vue({
    el: '#dateth',
    data: {
        date: Array(),
        one: "",
        two: "",
        three: "",
        four: "",
    }
});

var xk_plan = new Vue({
    el: '#date',
    data: {
        classes: [{
            schedules: [{
                    beginTime: "",
                    endTime: "",
                    stage: "",
                    place: "",
                    name: "",
                    planType: "",
                }],
            name: "",
            planType: ""
        }],
        line: Array(),
        lineSize: 0,
    },
    methods:{
        getIntroduce : function(event)     //弹出解释框
        {      
            var elem = $(event.target);
            var content = $(elem).text();
            var totalClassesNum = xk_plan.classes.length;
            var totalClassesSchdulesNum;
            var find = false;
            for(var i = 0;i<totalClassesNum;i++){
                totalClassesSchdulesNum = xk_plan.classes[i].schedules.length;
                for(var j=0;j<totalClassesSchdulesNum;j++){
                    if(xk_plan.classes[i].schedules[j]){
                        if(xk_plan.classes[i].schedules[j].planType==content){
                            content = xk_plan.classes[i].schedules[j].name;
                            find = true;
                            break;
                        }
                    }
                }
                if(find){
                    break;
                }
            }

            $(elem).attr('title', content); 
            $(elem).tooltip('show');
        },
        Enter : function(event) {
            var elem = $(event.target);
            var content = $(elem).text();
            getEnter(content);
        }
    },
    ready: function(event){
    }
});

var nowplc = new Vue({
    el: "#nowplc",
    data:{
        num: 0,
    },
});

var errorModal = new Vue({
    el: "#errorModal",
    data:{
        content:"",
    }
});

var warningModal = new Vue({
    el: "#warningModal",
    data:{
        content:"",
    }
});

var noClassModal = new Vue({
    el: "#noClassModal",
    data:{
        content:"",
    }
});

window.login = function () {
	if($("#uid").val()=='')
	{
		// alert('用户名为空!');
		$('#emptyUserPassword').modal({keyboard: false});
		$('#emptyUserPassword .modal-body').text('用户名不能为空!');
		return;
	}
	else if($("#password").val()=='')
	{
		$('#emptyUserPassword').modal({keyboard: false});
		$('#emptyUserPassword .modal-body').text('密码不能为空!');
		return;
	}
	else {
        $('#loading').removeClass('hide').addClass('show');         //显示等待框
		var uid = $("#uid").val();
		var password = $("#password").val();
		var password = $.nuaaMD5(password);
		$.ajax({
	        type: "POST",
	        url: apiUrl + "user",
	        data: JSON.stringify({
	            username: uid,
				hashedPassword: password
	        }),
			contentType: "application/json",
	        error: function(request) {
                // console.log(request);
                $('#loading').removeClass('show').addClass('hide');
                $('#ErrorUserPassword').modal({keyboard: false});
	        },
	        success: function(data) {
                // loading.finish = true;
                navbar.login = true;
                leftTopBox.login = true;
                navbar.name = data.name;
                leftTopBox.userdata.classnumber = data.classnumber;
                leftTopBox.userdata.number = data.number;
                leftTopBox.userdata.gender = data.gender;
                leftTopBox.name = data.name;
                window.localStorage.setItem('user',JSON.stringify(data));
                setCookie();
                $('#loading').removeClass('show').addClass('hide');
	        }
	    });
        $.ajax({
            type: "GET",
            url: imageHost + 'account/' + uid + '/' + password,
            success: function(data) {
                leftTopBox.imgurl = imageHost + "account/head/" + data.uToken;
                window.localStorage.setItem('imgurl',leftTopBox.imgurl);
            }
        });
	}
}

window.delayTime = null;

function getDelayTime() {
    $.ajax({
        type: "GET",
        url: apiUrl + "basic/utctime",
        success: function(data) {
            var severTime = moment(data.time).unix();
            var localTime = moment().unix();
            delayTime = severTime - localTime;
            getClassPlan();
        },
        error: function(data) {
            console.log(data);
        }
    });
}

function getClassPlan() {       //获取选课计划
    if(delayTime == null) {
        getDelayTime();
    }
    else {
        var start = moment().startOf('day').add(-2, 'days').unix() + delayTime;
        var end = moment().startOf('day').add(5, 'days').unix() + delayTime;
        var url = apiUrl + "plans/lite?start=" + start + "&end=" + end;
        $.ajax({
            type: "GET",
            url: url,
            success: function(data) {
                console.log(data);
                setEnter(data);         //设置能选课的通道
                getDay();               //设置日期栏
                var totalClass = data.length;
                var stageName = {20:"初选",40:"初选结果",60:"复选",80:"最终结果",100:"抢课",255:"补退选"};
                var tempPlace = [];
                var count = 0;
                for(var i = 0;i < totalClass;i++) {
                    xk_plan.classes[i] = Object();
                    xk_plan.classes[i].name = data[i].name;
                    xk_plan.classes[i].planType = data[i].planType;
                    var totalSchedules = data[i].schedules.length;
                    xk_plan.classes[i].schedules = [];
                    for(var j = 0;j < totalSchedules;j++) {//用来加上时间
                        var full = 0;
                        var schedulesEndTime = data[i].schedules[j].endDate;
                        schedulesEndTime = moment(schedulesEndTime);
                        schedulesEndTime = Math.floor(schedulesEndTime.toDate() / 1000);
                        var schedulesBeginTime = data[i].schedules[j].startDate;
                        schedulesBeginTime = moment(schedulesBeginTime);
                        schedulesBeginTime = Math.floor(schedulesBeginTime.toDate() / 1000);
                        var beginTime = schedulesBeginTime - start;
                        var endTime = schedulesEndTime - start;
                        beginTime = (beginTime / (3600 * 24));
                        endTime = (endTime / (3600 * 24));
                        var tempData = Math.floor(beginTime);
                        var tempEnd = Math.floor(endTime);
                        var effect = 1;
                        if(data[i].schedules[j].stage == 80) {
                            effect = 0;
                        }
                        if(beginTime < 0 && endTime < 0) {
                            effect = 0;
                        }
                        else if(beginTime > 7 && endTime > 7) {
                            effect = 0;
                        }
                        else if(beginTime < 0) {
                            tempData = 0;
                            beginTime = 0;
                        }
                        else if(endTime > 7) {
                            tempEnd = 7;
                            endTime = 7;
                        }
                        if(effect == 0) {
                            continue;
                        }
                        tempPlace[count] = Object();
                        tempPlace[count].beginTime = beginTime;
                        tempPlace[count].endTime = endTime;
                        for(var index = 0;index < count;index++) {
                            if(tempPlace[index].beginTime <= beginTime && tempPlace[index].endTime >= beginTime) {
                                full++;
                            }
                            else if(tempPlace[index].beginTime <= endTime && tempPlace[index].endTime >= endTime) {
                                full++;
                            }
                        }
                        count++;
                        xk_plan.classes[i].schedules[j] = Object();
                        xk_plan.classes[i].schedules[j].place = full;
                        xk_plan.lineSize++;
                        console.log(xk_plan.classes[i].name + "place" + xk_plan.classes[i].schedules[j].place);
                        xk_plan.classes[i].schedules[j].beginTime = Math.floor((beginTime / 7) * 100);
                        xk_plan.classes[i].schedules[j].endTime = Math.floor((endTime / 7) * 100);
                        xk_plan.classes[i].schedules[j].name = data[i].name + "-" + stageName[data[i].schedules[j].stage];
                        xk_plan.classes[i].schedules[j].planType = data[i].planType + "-" + stageName[data[i].schedules[j].stage]; 
                        console.log(xk_plan.classes[i].schedules[j].beginTime);
                        console.log(xk_plan.classes[i].schedules[j].endTime);
                        xk_plan.classes[i].schedules[j].stage = data[i].schedules[j].stage;
                    }
                }
                count--;
                //console.log(count);
                //console.log(tempPlace);
                for(var index = 0;index <= count;index++) {
                    if(tempPlace[index].beginTime < 3 && tempPlace[index].beginTime > 2) {
                        nowplc.num++;
                    }
                    else if(tempPlace[index].endTime < 3 && tempPlace[index].endTime > 2) {
                        nowplc.num++;
                    }
                    else if(tempPlace[index].endTime > 3 && tempPlace[index].beginTime < 2) {
                        nowplc.num++;
                    }
                }
                console.log(xk_plan.classes);
                //console.log(nowplc.num);
                if(xk_plan.lineSize < 2) {
                    xk_plan.lineSize = 2;
                }
                lineSize = xk_plan.lineSize;
                tempArray = Array();
                for(var lineIndex = 0;lineIndex < lineSize;lineIndex++) {
                    tempArray[lineIndex] = Object();
                    tempArray[lineIndex].schedules = Array();
                    tempArray[lineIndex].id = lineIndex;
                }
                classesSize = xk_plan.classes.length;
                for(var classesIndex = 0;classesIndex < classesSize;classesIndex++) {
                    schedulesSize = xk_plan.classes[classesIndex].schedules.length;
                    tempItem = Object();
                    for(var schedulesIndex = 0;schedulesIndex < schedulesSize;schedulesIndex++) {
                        tempSchedules = xk_plan.classes[classesIndex].schedules[schedulesIndex];
                        tempItem = tempSchedules;
                        if(tempItem) {
                            tempItem.width = tempItem.endTime - tempItem.beginTime;
                            tempArray[tempItem.place].schedules.push(tempItem);
                        }
                    }
                }
                for(var lineIndex = 0;lineIndex < lineSize;lineIndex++) {
                    Vue.set(xk_plan.line,lineIndex,tempArray[lineIndex]);
                }
                console.log(xk_plan.line);
                

                //var line0Num = 0,line1Num = 0;
                // var line0Array = Array();
                // var line1Array = Array();        
                // for(var i in xk_plan.classes){
                //     for(var j in xk_plan.classes[i].schedules){
                //         if(xk_plan.classes[i].schedules[j].place==0){
                //             line0Array[line0Num] = xk_plan.classes[i].schedules[j];
                //             line0Array[line0Num].width = xk_plan.classes[i].schedules[j].endTime - xk_plan.classes[i].schedules[j].beginTime;
                //             line0Num++;
                //         }
                //         else if(xk_plan.classes[i].schedules[j].place==1){
                //             line1Array[line1Num] = xk_plan.classes[i].schedules[j];
                //             line1Array[line1Num].width = xk_plan.classes[i].schedules[j].endTime - xk_plan.classes[i].schedules[j].beginTime;
                //             line1Num++;                    
                //         }
                //     }
                // }

                // xk_plan.line0 = line0Array;
                // xk_plan.line1 = line1Array;
                //console.log(xk_plan.line0);
                //console.log(xk_plan.line1);

                $('.loadingBox').removeClass('show').addClass('hide');  //隐藏掉等待框
                $('.table').removeClass('hide');
            },
            error: function(data) {
                alert("加载失败，请刷新重试");
            },
        });
    }
    
}

function getDay(){          //设置周几
    var week = ['周日','周一','周二','周三','周四','周五','周六'];
    var today = "周" + "日一二三四五六".split("")[new Date().getDay()];

    for(var i=0;i<week.length;i++)
    {
        if(today==week[i])
        {
            var k = (i+5)%7;
            xk_date.date[0] = week[k];
            k = i+2;
            for(var num=1;num<4;k++,num++)
            {
                k = k%7;
                xk_date.date[num] = week[k];
            }
        }
    }
    xk_date.one = xk_date.date[0];
    xk_date.two = xk_date.date[1];
    xk_date.three = xk_date.date[2];
    xk_date.four = xk_date.date[3];
    console.log(xk_date.date);
}

window.logout = function () {
    clearCookie();
    localStorage.clear();
    //console.log(leftTopBox.login);
	window.location.href="./index.html";
};



function loading() {
	for(i=1;i<6;i++)
	{
		var c=document.getElementById("myCanvas" + i);
		var cxt=c.getContext("2d");
		cxt.fillStyle="#e5e5e5";
		cxt.beginPath();
		cxt.arc(15,15,15,0,Math.PI*2,true);
		cxt.closePath();
		cxt.fill();
	}
}

var enter_accessRule;
var currentScheduleAccessRule;
var canEnterTable = Array();

function setEnter(data){        //筛选选课入口通道  setEnter(data)  return 所有可选的课的planId和其planType
    var start = moment().startOf('day').add(-2, 'days').unix();
    var end = moment().startOf('day').add(5, 'days').unix();
    var allClass = data.length;
    for(var i=0;i<allClass;i++){
        canEnterTable[i] = Object();
        canEnterTable[i].planType = data[i].planType;
        canEnterTable[i].planId = data[i].id;
    }
}

var planId;
var xkPlanType;
window.ngController;
function getEnter(itemPlanType) {              // 写到这 

    //console.log(itemPlanType);
    var tableLength = canEnterTable.length;
    var flag = false;
    var url;
    var id = Array();
    xkPlanType = itemPlanType;
    for(var i=0;i<tableLength;i++){
        if(itemPlanType.indexOf(canEnterTable[i].planType)>=0){
            planId = canEnterTable[i].planId;
            flag = true;
            break;
        }
    }
    if(flag==true){
        url = apiUrl + 'plans/' + planId;
    }
    else{
        console.log("该课程没有开课");
        noClassModal.content = "该课程没有开课";
        $('#noClassModal').modal({keyboard: false});                
        $('#loading').removeClass('show').addClass('hide');
        return;
    }



    // 初始化界面
    $('#loading').removeClass('hide').addClass('show'); 
    $('#calendar_div').addClass('hide');
    $('#info_page').addClass('hide');
    $('#xk-enter').removeClass('hide');


    $.ajax({
        type: "GET",
        url: url,
        success: function(data) {
            console.log(data);
            window.ngController = data.schedules[0].ngController;
            enter_accessRule = data.accessRule;
            if(data.currentSchedule!=null){
                currentScheduleAccessRule = data.currentSchedule.accessRule;
            }
            xk_enter.planType = data.planType;
            xk_enter.content = data.description;
            xk_enter.title = data.name;
            xk_enter.nowTime = -1;
            if(data.currentSchedule == null) {
                xk_enter.canEnter = false;
                xk_enter.beginTime = data.schedules[0].startDate;
            }
            else{
                xk_enter.canEnter = true;
                //console.log(xk_enter);
            }
            var totalTime = data.schedules.length;
            console.log(totalTime);
            for(var i = 0;i < totalTime;i++) {
                tempTime = Object(); 
                tempTime.beginTime = data.schedules[i].startDate;
                tempTime.stage = data.schedules[i].stage;
                Vue.set(xk_enter.beginTimes,i,tempTime);
            }

            // checkTime();             改用倒计时

            $('#loading').removeClass('show').addClass('hide');
            $('#xk-enter .panel-footer .btn').removeClass('hide'); 
            $('#xk-enter .panel-footer .time').removeClass('hide'); 

            console.log(planId);
        },
        error: function(data) {     
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});                
            $('#loading').removeClass('show').addClass('hide'); 
        }
    });
}

function enterXk() {
    if(!localStorage.getItem('user')){
        $('#loading').removeClass('show').addClass('hide'); 
        $('#loginError').modal({keyboard: false});
        $('#loginError').on('hidden.bs.modal', function (e) {
            logout();
        });
        return;
    }
    var info = JSON.parse(localStorage.getItem('user'));
    if (!judge(enter_accessRule, info)) {
        warningModal.content = "您不属于此选课计划";
        $('#warningModal').modal({keyboard: false});
        return;
    }
    //当前阶段的规则
    if (!judge(currentScheduleAccessRule, info)) {
        errorModal.content = "您不属于此选课计划";
        $('#warningModal').modal({keyboard: false});
        return;
    }
    // if((xkPlanType.indexOf("学科拓展课")>=0)) {
    //     window.location = './mod/ggxk/index.html?planId='+planId;
    // }
    // else {
    //     window.location = './mod/xk/index.html?planId='+planId;
    // }
    window.location = "./mod/" + window.ngController + '?planId=' + planId;
}

function GetQueryString(name) {
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}//获取地址栏参数

$(function() {
    if(document.cookie.indexOf("login") < 0){
        localStorage.clear();
    }
	$('#login').click(login);
    $(document).keyup(function(event){
        var uidIsFocus=$("#uid").is(":focus");
        var passwordIsFocus=$("#password").is(":focus");        
        if(event.keyCode==13&&(uidIsFocus==true||passwordIsFocus==true)){
            login();
        }
    });
    getClassPlan();
    $('#bxk').click(function(){
        getEnter("必修课");
    }); 
    $('#whszk').click(function(){
        getEnter("文化素质课");
    });
    $('#xktzk').click(function(){
        getEnter("学科拓展课");
    });
    $('#tyxk').click(function(){
        getEnter("体育专项课");
    });
    $('#xsytk').click(function(){
        getEnter("新生研讨课");
    });
    $('#ggxxk').click(function(){
        getEnter("公共选修课");
    });
    $('#wlkc').click(function(){
        getEnter("在线开放课");
    }); 
    $('#errorModal').on('hidden.bs.modal', function (e) {
        logout();
    }); 

   // ceshi();
   // ceshi2();
	loading();
    if(localStorage != undefined && localStorage.getItem('user')) {//存储用户数据
        leftTopBox.login = true;
        navbar.login = true;
        var info = JSON.parse(localStorage['user']);
        leftTopBox.name = info.name;
        navbar.name = info.name;
        leftTopBox.userdata.number = info.number;
        leftTopBox.userdata.imgurl = localStorage.getItem('imgurl');
        leftTopBox.userdata.classnumber = info.classnumber;
    }
});


function DateDiff(sDate1, sDate2) {
    var d2 = new Date(sDate2);
    var d1 = new Date(sDate1);
    var n = parseInt(d2.getTime() - d1.getTime()) / (24 * 60 * 60 * 1000);      //得到相差几天
    return n + 1;
}

function checkTime(){
    $.get(apiUrl+"basic/utctime").success(function(time){
        console.log(time);
        if(time!=undefined){
            var severtime=new Date(time.time);
            var localtime=new Date();
            var diff=Math.abs(localtime.getTime()-severtime.getTime())/1000/60;
            //console.log(diff);
            if(diff>10){
                errorModal.content = "您电脑的时间好像不太对哦，为了您能够正确选课，建议您校正电脑时间。当前服务器时间是：" + severtime.toString();
                $('#errorModal').modal({keyboard: false});  
            }
            if(diff>60){
                errorModal.content = "您是穿越来的吧，电脑上的时间不太对哦，为确保您能够正常选课，请先校对电脑的时间。当前服务器时间是："+ severtime.toString();
                $('#errorModal').modal({keyboard: false});
            }
        }
    });
};


//登录身份失效
window.imgError = function (){
    if(localStorage['user']) {
        errorModal.content = "您的登录身份已失效!请重新登录!";
        $('#errorModal').modal({keyboard: false});
        $('#errorModal').on('hidden.bs.modal', function (e) {
            logout();
        });
    }
}


//学长写好的judge函数
function getPath(json, path) {
    path.forEach(function (p) {
        var match = false;
        $.each(json, function (i, item) {
            if (i.toLowerCase() == p.toLowerCase()) {
                match = true;
                json = item;
            }
            return !match;
        });
        if (!match) return undefined;
    });
    return json;
}
function judgeSub(rule, obj) {
    var path = rule.key.split('.');
    var value = getPath(obj, path);
    if (!value || rule.value != value) return undefined;
    if (rule.subRules) {
        var result = undefined;
        for (var i = 0; i < rule.subRules.length; i++) {
            result = judgeSub(rule.subRules[i], obj);
            if (result != undefined) return result;
        }
    }
    return rule.allow;
}

function judge(accessRule, obj) {           //第一个参数为规则object    第二个为user obj
    var json = JSON.stringify(obj);
    if (accessRule.rules) {             //如果有子规则的话
        var result = undefined;
        for (var i = 0; i < accessRule.rules.length; i++) {
            result = judgeSub(accessRule.rules[i], obj);
            if (result != undefined) return result;
        }
    }
    return accessRule.defaultAllow;
}

//w3c官网的代码
function setCookie(cname, cvalue) {
    document.cookie = "login";  
}
//清除cookie
function clearCookie(name) {
    document.cookie = "";
}


//./mod/PE2016/tyxk.html?planId=d8f76d6e-4ea1-43df-9d8b-2e892b88f02d

window.ceshi = function()            //测试使用
{
    url = apiUrl + "cache/{6A2910C9-C119-4952-A8FF-47452A0E56E8}";
    var info = JSON.parse(localStorage['user']);
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '6D469BDFC5E7474390DC5D0A9E12B88A',
        },
        success: function(data) {
            //console.log(data);
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
}

window.ceshi2 = function()            //测试使用
{
    url = apiUrl + "cache/{34E03D9A-4340-4A75-9C4D-11B0C60EEBF1}";
    var info = JSON.parse(localStorage['user']);
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '6D469BDFC5E7474390DC5D0A9E12B88A',
        },
        success: function(data) {
            //console.log(data);
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
}

window.ceshi3= function()            //测试使用
{
    url = apiUrl + "cache/{228EE30B-9927-4F6B-9347-98B30D33D7F2}";
    var info = JSON.parse(localStorage['user']);
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '6D469BDFC5E7474390DC5D0A9E12B88A',
        },
        success: function(data) {
            //console.log(data);
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
}

window.ceshi4= function()            //测试使用
{
    url = apiUrl + "cache/{34E03D9A-4340-4A75-9C4D-11B0C60EEBF1}";
    var info = JSON.parse(localStorage['user']);
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '6D469BDFC5E7474390DC5D0A9E12B88A',
        },
        success: function(data) {
            //console.log(data);
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
}

window.ceshi5= function()            //测试使用
{
    url = apiUrl + "cache/{C60440A5-491D-4895-B1D5-F4E6FE25C72C}";
    var info = JSON.parse(localStorage['user']);
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '6D469BDFC5E7474390DC5D0A9E12B88A',
        },
        success: function(data) {
            //console.log(data);
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
}

window.ceshiAll = function()
{
    ceshi();
    ceshi2();
    ceshi3();
    ceshi4();
    ceshi5();
}

