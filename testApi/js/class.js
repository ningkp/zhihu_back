window.currentStage;
window.currentStageCanExit;

window.maxNum = new Vue({
    el: '#maxNum',
    data: {
        maxNum: "",
    }
})
window.classMaxNum = new Vue({        //最大志愿数
    el: '#classNumWarning',
    data: {
        MaxOrders: "",
    }
});
window.classMinNum = new Vue({        //最小志愿数
    el: '#classNumError',
    data: {
        MinOrders: "",
    }
});


window.navbar = new Vue({
    el: '#navbar',
    data: {
        login: false,
        name: null,
    }
});

window.classDetail = new Vue({             //可以选的课程          
    el: "#classDetail",
    data: {
         totalclass : Array(), 
    }
    // created: getClassPlanDetail(GetQueryString('planId'))
});

window.xkRead = new Vue({          //选课必读信息
    el: "#xk-Read",
    data: {
        content: "",
    }
});

window.xkInfo = new Vue({          //通道信息
    el: "#xk-Info",
    data: {
        content: "",
    }
});


window.electiveTime = new Vue({        //选课时间
    el: "#electiveTime",
    data: {
        schedules : Array(),
    }
});

window.electiveType = new Vue({           //判断当前为初选还是复选
    el: "#electiveType",
    data: {
        type: "",
    }
});

window.xkResult_classDetail = new Vue({             //学生选的志愿
    el: "#xkResult_classDetail",
    data:{
        choosedClass: Array(),
        stage: "",
    }
});

window.xkLastResult = new Vue({            //选课最终界面信息
    el: "#xk-LastResult-Detail",
    data:{
        classname: "",
        classplace: "",
        classtime: "",
        classweeks: "",
    }
});

var lastResult_Panel = new Vue({
    el: "#xk-LastResult-Panel",
    data: {
        stage:"",
        type:false,
    }
//    created: getFirstResult(),
});

var errorModal = new Vue({
    el: "#errorModal",
    data:{
        content:"",
    }
});
var successModal = new Vue({
    el: "#successModal",
    data:{
        content:"",
    }
});



$(function() {
    if(document.cookie.indexOf("login") < 0){
        localStorage.clear();
    }
    if(localStorage.getItem('user')) {//存储用户数据
        navbar.login = true;
        var info = JSON.parse(localStorage.getItem('user'));
        navbar.name = info.name;

        getStage();
        //判断是否选过课
        
    }
    else        //如果没有登录
    {
        $('#loading').removeClass('show').addClass('hide');
        $('#loginError').modal({keyboard: false});
        $('#errorModal').on('hidden.bs.modal', function (e) {
            logout();
        });
        $('#loginError').on('hidden.bs.modal', function (e) {
            logout();
        });
    }
});

//获取当前阶段
function getStage(){  
    $('#loading').removeClass('hide').addClass('show'); 

    var url = apiUrl + 'plans/' + GetQueryString('planId');
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;

    $.ajax({
        type: "GET",
        url: url,
        headers: {
            token: token,
        },
        success: function(data) {
            var Now = new Date();
            settings = JSON.parse(data.currentSchedule.settingsJson);
            if(settings["CanExit"]){
                currentStageCanExit = true;
            }

            data.schedules.forEach(function (schedule) {
            switch (schedule.stage) {
                case 20:            //初选
                    var pt1 = moment(schedule.startDate).toDate();
                    var pt2 = moment(schedule.endDate).toDate();
                    if (Now > pt1 && Now < pt2) { 
                        var info = JSON.parse(localStorage.getItem('user'));
                        var token = info.token;
                        $.ajax({
                            url: apiUrl + "user/records?planId=" + GetQueryString('planId') + "&deleted=false",
                            headers: { token: token, },
                            success: function (data) {   
                                var length = data.length;
                                var elected = false;
                                for(var index = 0;index < length;index++) {
                                    if(data[index].stage == 20) {
                                        elected = true;
                                    }
                                }
                                if(elected) {
                                    // console.log('success!!!!');
                                    // console.log(data);
                                    getMyclass();          //进入志愿列表页面
                                }                     //初选选过课了
                                else if(data.length==0)                          //初选未选课   待完善
                                {
                                    // alert('还未选课');
                                    getClassPlanDetail(GetQueryString('planId'));       //这里要改!!!
                                }
                            },
                            error: function(data) {     
                                //console.log(JSON.parse(data.responseText).message);
                                errorModal.content = JSON.parse(data.responseText).message;
                                $('#errorModal').modal({keyboard: false});
                                $('#errorModal').on('hidden.bs.modal', function (e) {
                                    logout();
                                });
                            }   
                        });
                        currentStage = schedule.stage;
                    }
                    break;
                case 40:                                //初选结果
                    var time1 = moment(schedule.startDate).toDate();
                    var time2 = moment(schedule.endDate).toDate();
                    if (Now > time1 && Now < time2) { 
                        getMyclass();
                        currentStage = schedule.stage;
                     }                     
                    break;
                case 60:                            //复选
                    var time1 = moment(schedule.startDate).toDate();
                    var time2 = moment(schedule.endDate).toDate();
                    if (Now > time1 && Now < time2) { 

                        var info = JSON.parse(localStorage.getItem('user'));
                        var token = info.token;
                        $.ajax({                    //获取中选班级的id            
                            url: apiUrl + "user/records?planId=" + GetQueryString('planId') + "&isWin=true&deleted=false",
                            headers: { token: info.token },
                            success: function (data) {
                                //console.log(data);
                                if(data.length==0)      //
                                {
                                    currentStage = schedule.stage;
                                    getMyclass();
                                }
                                else                    //中选    返回结果页面
                                {
                                    currentStage = schedule.stage;
                                    getFirstResult();
                                }
                            },
                            error: function(data) {
                                //console.log(JSON.parse(data.responseText).message);
                                errorModal.content = JSON.parse(data.responseText).message;
                                $('#errorModal').modal({keyboard: false});
                                $('#errorModal').on('hidden.bs.modal', function (e) {
                                    logout();
                                });
                            }
                        });

                        // console.log(needCheck);
                        // alert('1');
                        // if(needCheck==false)
                        // {
                        //     getMyclass();
                        //     currentStage = schedule.stage;
                        // }
                        // 
                     } 
                    break;
                case 80:
                    var time1 = moment(schedule.startDate).toDate();
                    var time2 = moment(schedule.endDate).toDate();
                    if (Now > time1 && Now < time2) { 
                        getFirstResult();
                        currentStage = schedule.stage;
                    }
                    break;
                case 100:                            //复选
                    var time1 = moment(schedule.startDate).toDate();
                    var time2 = moment(schedule.endDate).toDate();
                    if (Now > time1 && Now < time2) { 

                        var info = JSON.parse(localStorage.getItem('user'));
                        var token = info.token;
                        $.ajax({                    //获取中选班级的id            
                            url: apiUrl + "user/records?planId=" + GetQueryString('planId') + "&isWin=true&deleted=false",
                            headers: { token: info.token },
                            success: function (data) {
                                //console.log(data);
                                if(data.length==0)      //
                                {
                                    currentStage = schedule.stage;
                                    getClassPlanDetail(GetQueryString('planId'));
                                }
                                else                    //中选    返回结果页面
                                {
                                    currentStage = schedule.stage;
                                    getFirstResult();
                                }
                            },
                            error: function(data) {
                                //console.log(JSON.parse(data.responseText).message);
                                errorModal.content = JSON.parse(data.responseText).message;
                                $('#errorModal').modal({keyboard: false});
                                $('#errorModal').on('hidden.bs.modal', function (e) {
                                    logout();
                                });
                            }
                        });
                     } 
                    break;   
                default:console.log('stageError');break;
            }
            $('#loading').removeClass('show').addClass('hide'); 
        });
        },
        error: function(data) {     
            //console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
            $('#errorModal').on('hidden.bs.modal', function (e) {
                logout();
            });
        }  
    });
}

window.logout = function () {
    localStorage.clear();
    clearCookie();
    window.location.href="../../index.html";
};

function getMyclass() {               //获取选课志愿列表  
    //初始化界面
    $('#xk-result-Panel').removeClass('hide');
    $('#loading').removeClass('hide').addClass('show'); 
    $('.listBox').addClass('hide');
    $('.listPanel').addClass('hide');

    //获取已选志愿信息
    var url = apiUrl + "user/records?planId=" + GetQueryString('planId') + "&deleted=false";
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        type: "GET",
        url: url,
        headers: {
            token: token,
        },
        success: function(data) {           //获取到我的选课列表了
            console.log(data);
            //初选没有选课的并且在40阶段和60阶段的情况下
            if(data.length==0&&currentStage==40){
                errorModal.content = "你好像初选没有来选课,请关注复选时间,复选再来吧!";
                $('#errorModal').modal({keyboard: false});
                $('#errorModal').on('hidden.bs.modal', function (e) {
                    window.location.href="../../index.html";
                });
            }

            //排序
            data.sort(function (a, b) { return a.orderNum - b.orderNum });
            console.log(data);

            var needCheck = true;      //是否需要复选
            var chooseClass = new Array();
            var length = data.length;
            var weeks = ["一","二","三","四","五","六","天"];

            for(var i = 0;i < length;i++)
            {
                chooseClass[i] = data[i];       //排序
                if(currentStage==20){
                    chooseClass[i].width = Math.round(data[i].item.total/data[i].item.quota*50); 
                    chooseClass[i].stageIs = true;  
                    chooseClass[i].info = "已选人数";                 
                }
                else {
                    chooseClass[i].width = Math.round(data[i].item.winCount/data[i].item.quota*100);
                    chooseClass[i].stageIs = false; 
                    chooseClass[i].info = "中选人数";
                }
                if(data[i].isWin==true)
                {
                    needCheck = false;
                }
                var placesFlag = false;
                var setPlaces;
                if(data[i].item.sections[0]){
                    placesFlag = true;
                }
                if(placesFlag){
                    setPlaces = data[i].item.sections[0].places;
                    var classtime1 = "星期" + weeks[setPlaces[0].dayOfWeek - 1] + "  第" + setPlaces[0].begin + "-" + (setPlaces[0].begin+1) + "节";
                    var weeksLength1 = setPlaces[0].weeks.length;
                    for(var j = 0;j < weeksLength1;j++);
                    var classweeks1 = setPlaces[0].weeks[0] + "-" + setPlaces[0].weeks[j-1] + "周";
                    chooseClass[i].time1 = classtime1 + classweeks1;
                    chooseClass[i].place1 = setPlaces[0].place;
                    if(setPlaces[1]){
                        var classtime2 = "星期" + weeks[setPlaces[1].dayOfWeek - 1] + "  第" + setPlaces[1].begin + "-" + (setPlaces[1].begin+1) + "节";
                        var weeksLength2 = setPlaces[1].weeks.length;
                        for(var j = 0;j < weeksLength2;j++);
                        var classweeks2 = setPlaces[1].weeks[0] + "-" + setPlaces[1].weeks[j-1] + "周";
                        chooseClass[i].time2 = classtime2 + classweeks2;
                        chooseClass[i].place2 = setPlaces[1].place;
                    }
                }
                if(data[i].item.course.require){
                    chooseClass[i].item.course.require = "课程要求: " + data[i].item.course.require;
                }
            }
            xkResult_classDetail.choosedClass = chooseClass;            //vue的bug
            if(currentStage==20) //初选
            {
                xkResult_classDetail.stage = "已选";
            }
            else if(currentStage==40)//初选结果
            {
                $('#cancelBtn').addClass('hide disabled');
                if(needCheck)
                {
                    errorModal.content = "你好像初选没有选上课,请关注复选时间,复选再来吧!";
                    $('#errorModal').modal({keyboard: false});
                    $('#checkClass').removeClass('hide').addClass('disabled').mouseover(getCheckIntroduce());
                }
                else
                {
                    $('#checkClass').addClass('hide');
                }
                xkResult_classDetail.stage = "未中";
            }
            else if(currentStage==60)//复选
            {
                console.log(currentStage);
                if(data.length==0){
                    $('#xk-result-Panel').addClass('hide');
                    errorModal.content = "您没有参加初选!";
                    $('#errorModal').modal({keyboard: false});
					$('#errorModal').unbind('hidden.bs.modal');
                    getClassPlanDetail(GetQueryString('planId'));
                }
                else{
                    $('#cancelBtn').addClass('hide disabled');
                    $('#checkClass').removeClass('hide');
                    $('#checkClass').mouseover(getCheckIntroduce());
                    $('#checkClass').click(function() {
                        $('#xk-result-Panel').addClass('hide');
                        getClassPlanDetail(GetQueryString('planId'));
                    });
                    xkResult_classDetail.stage = "未中";
                }
            }
            console.log(xkResult_classDetail.choosedClass);
            $('#loading').removeClass('show').addClass('hide');
        },
        error: function(data) {
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
            $('#errorModal').on('hidden.bs.modal', function (e) {
                logout();
            });
            $('#loading').removeClass('show').addClass('hide');            
        }
    }); 
}

window.postMychoose = function (choosedclassId) {               //保存志愿
    $('#loading').removeClass('hide').addClass('show');
    
    var url = apiUrl + "user/records?planId=" + GetQueryString('planId');
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;

    console.log(JSON.stringify(choosedclassId));
    $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(choosedclassId),
        headers: {
            token: token,
        },
        success: function(data) {           
            console.log(data);
            $('#loading').removeClass('show').addClass('hide'); 
            if(currentStage==60||currentStage==100)        //如果是复选或者抢课进结果
            {
                getFirstResult();                
            }
            //发送完之后执行获取志愿列表
            getMyclass();          
        },
        error: function(data) {
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});          
            $('#loading').removeClass('show').addClass('hide'); 
        }
    });
}

//关于取消志愿的开始
window.cancleAllChoose = function cancleAllChoose() {                 //初选志愿列表取消所有志愿
    var url = apiUrl + "user/records?planId=" + GetQueryString('planId');
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({                             
        type: "DELETE",
        url: url,
        headers: { token: token },
        success: function (data) {
            console.log(data);
            $('#loading').removeClass('show').addClass('hide'); 
            location.reload();
            getClassPlanDetail(GetQueryString('planId'));
        },
        error: function(data) {
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
            $('#loading').removeClass('show').addClass('hide'); 
        }
    });
}

function cancleSingleChoose(cancledclassId) {                 //复选结果取消单个志愿!!
    $('#loading').addClass('show').removeClass('hide');
    var url = apiUrl + "user/records/" + cancledclassId;
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        data: JSON.stringify(cancledclassId),
        headers: {
            token: token,
        },
        success: function(data) {
            console.log(data);
            $('#loading').removeClass('show').addClass('hide');
            successModal.content = "取消志愿成功!";
            $('#successModal').modal({keyboard: false});
        },
        error: function(data) {
            console.log('error');
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
            $('#loading').removeClass('show').addClass('hide'); 
            $('#errorModal').on('hidden.bs.modal', function (e) {
                window.location.href="../../index.html";
            });
        }
    });
}
//关于取消志愿的结束

function getMyclassDetail(sectionId) {                  //获取我的班级详细信息?????
    var url = apiUrl + "sections/" + sectionId;
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        type: "GET",
        url: url,
        headers: {
            token: token,
        },
        success: function(data) {
            console.log(data);
        },
        error: function(request) {
            console.log('error');
        }
    });
}

//初选选中的两个处理函数  开始
window.getFirstResult = function() {             //初选结果    
    $('#loading').removeClass('hide').addClass('show');

    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({                    //获取中选班级的id            
        url: apiUrl + "user/records?planId=" + GetQueryString('planId') + "&isWin=true&deleted=false",
        headers: { token: info.token },
        success: function (data) {
            console.log(data);
            $('#loading').removeClass('show').addClass('hide');
            if(data.length==0)      //未中选  返回志愿列表页面(等待复选)
            {
                if(currentStage==80||currentStage==100)
                {
                    errorModal.content = '啊哦,你好像没选上课!';
                    $('#errorModal').modal({keyboard: false}); 

                }
                return false;
            }
            else                    //中选    返回结果页面
            {
                console.log(currentStage);
                if(data[0].stage==20)
                {
                    lastResult_Panel.stage = "初选";
                }
                else if(data[0].stage==60)
                {
                    lastResult_Panel.stage = "复选";
                }
                else if(data[0].stage==100)
                {
                    lastResult_Panel.stage = "抢课";
                }
                if((currentStage==60||currentStage==100)&&currentStageCanExit)        //当前阶段为60且当前阶段允许退课
                {
                    lastResult_Panel.type = true;
                }
                getclassDetail(data[0].item.id,data);
            }
        },
        error: function(data) {
            $('#loading').removeClass('show').addClass('hide');
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
            $('#errorModal').on('hidden.bs.modal', function (e) {
                logout();
            });
        }
    });

    // var classId;
    
    // getclassDetail(classId);
}

function getclassDetail(itemId,record) {                       //获取我的班级信息
    //初始化界面
    $('#xk-result-Panel').addClass('hide'); 
    $('#xk-LastResult-Panel').removeClass('hide');

    url = apiUrl + "items/" + itemId + "/sections?self=true";
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        type: "GET",
        url: url,
        headers: {
            token: token,
        },
        success: function(data) {
            console.log(data);
            if(data[0]){               //不是网络课程
                var weeks = ["一","二","三","四","五","六","天"];

                xkLastResult.classname = data[0].name;
                xkLastResult.classplace = data[0].places[0].place;
                xkLastResult.classtime = "星期" + weeks[data[0].places[0].dayOfWeek - 1] + "  第" + data[0].places[0].begin + "-" + (data[0].places[0].begin+1) + "节";
                var weeksLength = data[0].places[0].weeks.length;
                for(var i = 0;i < weeksLength;i++);
                xkLastResult.classweeks = "第" + data[0].places[0].weeks[0] + "周~第" + data[0].places[0].weeks[i-1] + "周";
                $('#cancelCheck').unbind("click");
                $('#cancelCheck').click(function() {             //到这!
                    cancleSingleChoose(record[0].id); 
                    $('#xk-LastResult-Panel').addClass('hide');
                    getClassPlanDetail(GetQueryString('planId'));
                });
            }
            else{
                xkLastResult.classname = record[0].item.course.name;
                xkLastResult.classplace = record[0].item.course.hour;         //学时
                xkLastResult.classtime = record[0].item.course.credit;        //学分
                if(record[0].item.course.require){
                    xkLastResult.classweeks = record[0].item.course.require;  //需求
                }
                else{
                    xkLastResult.classweeks = "暂无课程需求";
                }
                $('#cancelCheck').unbind("click");
                $('#cancelCheck').click(function() {             //到这!
                    cancleSingleChoose(record[0].id); 
                    $('#xk-LastResult-Panel').addClass('hide');
                    getClassPlanDetail(GetQueryString('planId'));
                });
            }
        },
        error: function(data) {
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
        }
    });
}
//初选选中的两个处理函数  结束


function GetQueryString(name) {
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}//获取地址栏参数

function getClassPlanDetail(planId) {           //获取选课(初选和复选)计划的时间信息   以及选课班级内容
    //初始化界面
    $('#loading').removeClass('hide').addClass('show'); 
    $('#xk-Panel').removeClass('hide');
    $('#xk-Read').removeClass('hide');
    $('#xk-Info').removeClass('hide');
    if(currentStage==20){
        $('.listBox').removeClass('hide');
        $('.listPanel').removeClass('hide');
    }
    // console.log(planId);
    // var url = apiUrl + "plans/" + GetQueryString('planId');       //index.html用
    var url = apiUrl + "plans/" + planId + "/detail";
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        // type: "GET",
        url: url,
        headers: {
            token: token,
        },
        success: function(data) {
            console.log(data);

            // 怀疑执行不到，不属于计划人员应该服务器会返回错误    先判断是否属于该选课计划
            var accessRule = data.accessRule;
            if (!judge(accessRule, info)) {
                errorModal.content = "您不属于此选课计划";
                $('#errorModal').modal({keyboard: false});
                return;
            }

            //初选还是复选
            if(data.currentSchedule.stage == 20) {
                electiveType.type = "初选";
            }
            else if(data.currentSchedule.stage == 60) {
                electiveType.type = "复选";
            }
            else if(data.currentSchedule.stage == 100) {
                electiveType.type = "抢课";
            }
            else {
                electiveType.type = "补选";
            }

            var weeks = ["一","二","三","四","五","六","天"];

            //选课信息       最多最少几个志愿    
            var json = JSON.parse(data.currentSchedule.settingsJson);
            // console.log(json);
            classMaxNum.MaxOrders = json.MaxOrders;
            classMinNum.MinOrders = json.MinOrders;
            maxNum.maxNum = json.MaxOrders;
            xkRead.content = json.Notice;
            var channelLength = data.channels.length;
            for (var i = 0;i < channelLength;i++) {
                if($.inArray(info.classnumber,data.channels[i].classes) != -1 || data.channels[i].classes == null) {    //找到对应自己的班级通道
                    //通道信息
                    xkInfo.content = data.channels[i].name;

                    var totalclass = new Array();
                    var num = 0;
                    var itemLength = data.channels[i].items.length;
                    for(var k = 0;k < itemLength;k++)
                    {
                        var I_rules = data.channels[i].items[k].accessRule;           //改成统一用这个进行筛选
                        if (!judge(I_rules, info)) {
                            continue;
                        }
                        if(data.channels[i].items[k].quota==0){
                            continue;
                        }
                        var placesFlag = false;
                        var setPlaces;
                        if(data.channels[i].items[k].sections[0]){
                            placesFlag = true;
                        }
                        if(placesFlag){
                            setPlaces = data.channels[i].items[k].sections[0].places;
                        }
                        totalclass[num] = data.channels[i].items[k];
                        if(currentStage==20){
                            if(placesFlag){             //如果section存在
                                var classtime1 = "星期" + weeks[setPlaces[0].dayOfWeek - 1] + "  第" + setPlaces[0].begin + "-" + (setPlaces[0].begin+1) + "节";
                                var weeksLength1 = setPlaces[0].weeks.length;
                                for(var j = 0;j < weeksLength1;j++);
                                var classweeks1 = setPlaces[0].weeks[0] + "-" + setPlaces[0].weeks[j-1] + "周";
                                totalclass[num].time1 = classtime1 + classweeks1;
                                totalclass[num].place1 = setPlaces[0].place;
                                if(setPlaces[1]){
                                    var classtime2 = "星期" + weeks[setPlaces[1].dayOfWeek - 1] + "  第" + setPlaces[1].begin + "-" + (setPlaces[1].begin+1) + "节";
                                    var weeksLength2 = setPlaces[1].weeks.length;
                                    for(var j = 0;j < weeksLength2;j++);
                                    var classweeks2 = setPlaces[1].weeks[0] + "-" + setPlaces[1].weeks[j-1] + "周";
                                    totalclass[num].time2 = classtime2 + classweeks2;
                                    totalclass[num].place2 = setPlaces[1].place;
                                }
                            }
                            if(totalclass[num].course.require){
                                totalclass[num].course.require = "课程要求: " + totalclass[num].course.require;
                            }
                            totalclass[num].hot = Math.round(data.channels[i].items[k].total/data.channels[i].items[k].quota*50);
                            totalclass[num].stageIs = true;
                            totalclass[num].stageMethod = "+志愿";
                            totalclass[num].canSubmit = false;
                        }
                        if(currentStage==60||currentStage==100){
                            if(placesFlag){             //如果section存在
                                var classtime1 = "星期" + weeks[setPlaces[0].dayOfWeek - 1] + "  第" + setPlaces[0].begin + "-" + (setPlaces[0].begin+1) + "节";
                                var weeksLength1 = setPlaces[0].weeks.length;
                                for(var j = 0;j < weeksLength1;j++);
                                var classweeks1 = setPlaces[0].weeks[0] + "-" + setPlaces[0].weeks[j-1] + "周";
                                totalclass[num].time1 = classtime1 + classweeks1;
                                totalclass[num].place1 = setPlaces[0].place;
                                if(setPlaces[1]){
                                    var classtime2 = "星期" + weeks[setPlaces[1].dayOfWeek - 1] + "  第" + setPlaces[1].begin + "-" + (setPlaces[1].begin+1) + "节";
                                    var weeksLength2 = setPlaces[1].weeks.length;
                                    for(var j = 0;j < weeksLength2;j++);
                                    var classweeks2 = setPlaces[1].weeks[0] + "-" + setPlaces[1].weeks[j-1] + "周";
                                    totalclass[num].time2 = classtime2 + classweeks2;
                                    totalclass[num].place2 = setPlaces[1].place;
                                }
                            }
                            if(totalclass[num].course.require){
                                totalclass[num].course.require = "课程要求: " + totalclass[num].course.require;
                            }
                            totalclass[num].hot = Math.round(data.channels[i].items[k].winCount/data.channels[i].items[k].quota*100);
                            totalclass[num].stageIs = false;
                            if(data.channels[i].items[k].winCount>=data.channels[i].items[k].quota){
                                totalclass[num].stageMethod = "已选满";
                                totalclass[num].canSubmit = true;
                            }
                            else{
                                totalclass[num].stageMethod = "提交";
                                totalclass[num].canSubmit = false;
                            }
                        }
                        num++;

                        // if(info.gender==data.channels[i].items[k].remark)       //做一个性别的筛选(待完善用一个统一的规则函数来筛选)
                        // {
                        //     totalclass[num] = data.channels[i].items[k];
                        //     num++;
                        // }

                    }
                    if(placesFlag){
                        var newPlace = Array();
                        var oldPlace = Array();
                        var indexNew = 0;
                        var indexOld = 0;
                        var myPlace = JSON.parse(window.localStorage["user"]).campus;
                        var num = totalclass.length;
                        for(var i = 0;i < num;i++) {
                            if(totalclass[i].place1.indexOf(myPlace) != -1) {
                                newPlace[indexNew] = totalclass[i];
                                newPlace[indexNew].danger = false;
                                indexNew++;
                            }
                            else {
                                oldPlace[indexOld] = totalclass[i];
                                oldPlace[indexOld].danger = true;
                                indexOld++;
                            }
                        }
                        for(var i = 0;i < indexNew;i++) {
                            totalclass[i] = newPlace[i];
                        }
                        for(var i = 0;i < indexOld;i++) {
                            totalclass[indexNew] = oldPlace[i];
                            indexNew++;
                        }
                    }
                    classDetail.totalclass = totalclass;       //选课内容


                    electiveTime.schedules = data.schedules;            //选课时间
                    var scheduleLength = data.schedules.length;
                    for(var j = 0;j < scheduleLength;j++) {
                        if(data.schedules[j].stage == 20) {
                            electiveTime.schedules[j].stage = "初选";
                        }
                        else if(data.schedules[j].stage == 60) {
                            electiveTime.schedules[j].stage = "复选";
                        }
                        else if(data.schedules[j].stage == 40){
                            electiveTime.schedules[j].stage = "查看初选结果";
                        }
                        else if(data.schedules[j].stage == 80){
                            electiveTime.schedules[j].stage = "查看最终结果";
                        }
                        else if(data.schedules[j].stage == 100){
                            electiveTime.schedules[j].stage = "抢课";
                        }
                        else if(data.schedules[j].stage == 255){
                            electiveTime.schedules[j].stage = "补选";
                        }
                    }
                }
            }

            // 添加志愿按钮           
            $('#loading').removeClass('show').addClass('hide'); 
            $('#xk-Panel .panel-default .panel-body .content li button').click(add_Class);

        },
        error: function(data) {
            console.log(JSON.parse(data.responseText).message);
            errorModal.content = JSON.parse(data.responseText).message;
            $('#errorModal').modal({keyboard: false});
        }
    });
}


window.getChoosedIntroduce = function()     //弹出解释框
{
    var content = "点击查看中选课程信息";
    $('#getChoosedIntroduce').attr('title', content).tooltip('show');   
}
window.getCheckIntroduce = function()     //弹出解释框
{
    var content = "进入复选";
    $('#getChoosedIntroduce').attr('title', content).tooltip('show');   
}



function ceshi()            //测试使用
{
    url = apiUrl + "cache/{D8F76D6E-4EA1-43DF-9D8B-2E892B88F02D}";
    var info = JSON.parse(localStorage.getItem('user'));
    var token = info.token;
    $.ajax({
        type: "DELETE",
        url: url,
        headers: {
            key: '0EBC8996E2E946838E88555C9B88669A',
        },
        success: function(data) {
            console.log('success');
        },
        error: function(request) {
            console.log('error');
        }
    });
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



// $.ajax({                    //复选            !!可以随时清除
//         type: "DELETE",
//         url: apiHost + "user/records/"+$(e).data("guid"),
//         headers: { token: user.token },
//         success: function (data) {
//             flag = false;
//             $('#myModalbody').html("提示");
//             $('#myModalbody').html("清除成功");
//             $('#myModal').on('hidden.bs.modal', function () {
//                 window.location.href = "./60.html?id=" + getQueryString("id");
//             });
//             $("#myModal").modal();

//         },
//         error:  errorHandler
//     })



// $.ajax({                                 //清除所有的
//         type: "DELETE",
//         url: apiHost + "user/records?planId=" + getQueryString("id"),
//         headers: { token: user.token },
//         success: function (data) {
//             $('#loading').fadeOut(500);
//             $('#myModalLabel').html("提示");
//             $('#myModalbody').html("清除成功");
//             $('#myModal').modal();
//         },
//         error: errorHandler
//     });
