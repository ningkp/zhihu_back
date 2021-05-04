
// 体育选课内的添加志愿、志愿列表的出现和消失、志愿的移动效果.

$(function() {

// 添加志愿按钮			写在class.js里面
// $('#xk-Panel .panel-default .panel-body .content li button').click(add_Class);

// 清空按钮
$('.listPanel .panel-default .panel-heading .panel-title .empty').click(empty_localClass);

//折叠按钮
$('.listPanel .panel-default .panel-heading .panel-title .slideUp').click(slide_Up);

//展开按钮
$('.listBox .list').click(slide_Down);



// 删除按钮



//清空服务器志愿按钮
$('#cancel').click(empty_serverClass);



});




// 添加志愿按钮
var classNum = 0;		//classNum为班级数
var className;			//班级名字
window.add_Class = function (e) {
	console.log(currentStage);
	if(currentStage==60||currentStage==100){
		save_class(e);			//复选或抢课
		return ;
	}
	e = window.event;
	thisButton = e.target?e.target:e.srcElement;
	classNum++;
	//最多只能设置MaxOrders个志愿
	if(classNum>classMaxNum.MaxOrders)
	{
	    $('#classNumWarning').modal({keyboard: false});
		classNum = classMaxNum.MaxOrders;
		return;
	}
	//将按钮设置为禁用	
	$(thisButton).removeClass('btn-success').addClass('btn-default').attr('disabled', true).text('已选');

	//将课程放到选课篮子里以及使更改志愿数
	className = $(thisButton).parent().find('span').text();		//获取班级名字
	classId = $(thisButton).parent().find('span').attr("id");
	$('.listPanel .panel-default .panel-body .list-group li').eq(classNum - 1).removeClass('hide').addClass('show').find('span.label').text(className).attr({"title": className, "id": classId});
	$('.listBox .num .classNum').text(classNum);
}

window.submit_DangerClass = function (thisDangerButton) {
	console.log(currentStage);
	if(currentStage==60||currentStage==100){
		save_Dangerclass(thisDangerButton);			//复选或抢课
		return ;
	}
	thisButton = thisDangerButton;
	classNum++;
	//最多只能设置MaxOrders个志愿
	if(classNum>classMaxNum.MaxOrders)
	{
	    $('#classNumWarning').modal({keyboard: false});
		classNum = classMaxNum.MaxOrders;
		return;
	}
	//将按钮设置为禁用	
	$(thisButton).removeClass('btn-success').addClass('btn-default').attr('disabled', true).text('已选');

	//将课程放到选课篮子里以及使更改志愿数
	className = $(thisButton).parent().find('span').text();		//获取班级名字
	classId = $(thisButton).parent().find('span').attr("id");
	$('.listPanel .panel-default .panel-body .list-group li').eq(classNum - 1).removeClass('hide').addClass('show').find('span.label').text(className).attr({"title": className, "id": classId});
	$('.listBox .num .classNum').text(classNum);
}

window.thisDangerButton;

window.add_dangerClass = function (e) {
	$('#classDangerWarning').modal({keyboard: false});
	e = window.event;
	thisButton = e.target?e.target:e.srcElement;
	window.thisDangerButton = thisButton;
	return;
}

window.submitDangerClass = function (){
	submit_DangerClass(window.thisDangerButton);
}


//清空志愿
function empty_localClass(argument) {
	//清空班级数
	classNum = 0;
	$('.listBox .num .classNum').text(classNum);

	// 清空志愿列表以及将按钮设置为可用状态
	$('.listPanel .panel-default .panel-body .list-group li').addClass('hide').removeClass('show');
	$('#xk-Panel .panel-default .panel-body .content li button').removeClass('btn-default').addClass('btn-success').attr('disabled', false).text('+志愿');

}


// 折叠志愿列表
window.slide_Up = function (argument) {
	$('.listPanel').slideUp('1000');
	$('.listBox .list').text('志愿列表');
}


// 展开志愿列表
window.slide_Down = function (argument) {
	if($('.listBox .list').text()=='保存提交')
	{
		save_Class();
	}
	$('.listPanel').slideDown('1000');
	$('.listBox .list').text('保存提交');

}

//删除单个志愿
window.delete_Class = function (obj) {
	// 更新选课篮子的班级数以及将按钮设为可用状态
	classNum--;
	$('.listBox .num .classNum').text(classNum);
	className = $(obj).parent().find('span.label').text();
	$('#xk-Panel .panel-default .panel-body .content li span:contains(' + className + ')').parent().find('button').removeClass('btn-default').addClass('btn-success').attr('disabled', false).text('+志愿');
	// $('#xk-Panel .panel-default .panel-body .content li button').removeClass('btn-default').addClass('btn-success').attr('disabled', false).text('+志愿');



// 删除时总是最后一个志愿列
	index = $('.listPanel .panel-default .panel-body .list-group li span.glyphicon-remove').index(obj);
	for(i=index;i<classNum;i++)
	{
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + i + ') span.label').text($('.listPanel .panel-default .panel-body .list-group li:eq(' + (i+1) + ') span.label').text());			
		oldId = $('.listPanel .panel-default .panel-body .list-group li:eq(' + (i+1) + ') span.label').attr("id");
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + i + ') span.label').attr("id",oldId);
	}
	$('.listPanel .panel-default .panel-body .list-group li.show:last').removeClass('show').addClass('hide').find('.label').text('');
	// $('.listPanel .panel-default .panel-body .list-group li:eq(' + index + ')').removeClass('show').addClass('hide').find('.label').text('');
}


//保存提交初选志愿
function save_Class() {
	// alert('1');
	if(classNum<classMinNum.MinOrders){
		$('#classNumError').modal({keyboard: false});
		return;
	}
	$('#xk-Panel').addClass('hide');
	$('.listBox').addClass('hide');
	$('.listPanel').addClass('hide');
	$('#xk-result-Panel').removeClass('hide');
	$('#xk-Read').addClass('hide');
	$('#xk-Info').addClass('hide');	

//从服务器获取数据比较好
	// for(i=0;i<classNum;i++){
	// 	className = $('.listPanel .panel-default .panel-body .list-group li:eq(' + i + ') span.label').text();
	// 	// alert($('.listPanel .panel-default .panel-body .list-group li:eq(' + i + ') span.label').text());
	// 	$('#xk-result-Panel .panel-body .content li:eq(' + i + ')').removeClass('hide').find('span.xk-result-name').text(className);
	// }

	//设置提交时间
	now = new Date();
	$('#xk-result-Panel .panel .panel-heading #years').text(now.getFullYear());
	$('#xk-result-Panel .panel .panel-heading #months').text((now.getMonth() + 1));
	$('#xk-result-Panel .panel .panel-heading #days').text(now.getDate());
	times = now.getHours() + ":" + now.getMinutes();
	$('#xk-result-Panel .panel .panel-heading #times').text(times);


	//提交的id
	var choosedclassId = [];			//有bug!!!不能交换多次?
	for(i=0;i<classNum;i++)
	{
		className = $('.listPanel .panel-default .panel-body .list-group li:eq(' + i + ') span.label').attr("id");
		var totalnum = classDetail.totalclass.length;
		console.log("className");
		choosedclassId.push(className);
	}
	console.log(choosedclassId);
	// alert(classDetail.totalclass[0].id);
	postMychoose(choosedclassId);

}
//保存提交复选
function save_class(e){

	e = window.event;
	thisButton = e.target?e.target:e.srcElement;
	console.log($(thisButton).parent().children("span").text());
	$('#xk-Panel').addClass('hide');
	$('.listPanel').addClass('hide');
	$('#xk-result-Panel').removeClass('hide');
	$('#xk-Read').addClass('hide');
	$('#xk-Info').addClass('hide');	

	//设置提交时间
	now = new Date();
	$('#xk-result-Panel .panel .panel-heading #years').text(now.getFullYear());
	$('#xk-result-Panel .panel .panel-heading #months').text((now.getMonth() + 1));
	$('#xk-result-Panel .panel .panel-heading #days').text(now.getDate());
	times = now.getHours() + ":" + now.getMinutes();
	$('#xk-result-Panel .panel .panel-heading #times').text(times);


	//提交的id
	var choosedclassId = [];
	className = $(thisButton).parent().children("span").attr("id");
	choosedclassId.push(className);
	empty_localClass();
	console.log(choosedclassId);
	// alert(classDetail.totalclass[0].id);
	postMychoose(choosedclassId);
}

//保存提交复选
function save_Dangerclass(thisDangerButton2){

	thisButton = thisDangerButton2;
	console.log($(thisButton).parent().children("span").text());
	$('#xk-Panel').addClass('hide');
	$('.listPanel').addClass('hide');
	$('#xk-result-Panel').removeClass('hide');
	$('#xk-Read').addClass('hide');
	$('#xk-Info').addClass('hide');	

	//设置提交时间
	now = new Date();
	$('#xk-result-Panel .panel .panel-heading #years').text(now.getFullYear());
	$('#xk-result-Panel .panel .panel-heading #months').text((now.getMonth() + 1));
	$('#xk-result-Panel .panel .panel-heading #days').text(now.getDate());
	times = now.getHours() + ":" + now.getMinutes();
	$('#xk-result-Panel .panel .panel-heading #times').text(times);


	//提交的id
	var choosedclassId = [];
	className = $(thisButton).parent().children("span").text();
	var totalnum = classDetail.totalclass.length;
	for(var j = 0;j < totalnum;j++)
	{
		if(className==classDetail.totalclass[j].name)
		{
			// console.log(classDetail.totalclass[j].name);
			choosedclassId.push(classDetail.totalclass[j].id);
			break;
		}
	}
	empty_localClass();
	console.log(choosedclassId);
	// alert(classDetail.totalclass[0].id);
	postMychoose(choosedclassId);
}


//下移
window.down = function (obj) {
	text = $(obj).parent().find('span.label').text();
	index = $(obj).parent().index();
	preId = $(obj).parent().find('span.label').attr("id");
	if($('.listPanel .panel-default .panel-body .list-group li:eq(' + (index+1) + ') span.label').text()!='')
	{
		nextId = $('.listPanel .panel-default .panel-body .list-group li:eq(' + (index+1) + ') span.label').attr("id");
		$(obj).parent().find('span.label').text($('.listPanel .panel-default .panel-body .list-group li:eq(' + (index+1) + ') span.label').text());
		$(obj).parent().find('span.label').attr("id",nextId);
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + (index+1) + ') span.label').text(text);
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + (index+1) + ') span.label').attr("id",preId);
	}
}

// 上移
window.up = function (obj) {
	text = $(obj).parent().find('span.label').text();
	index = $(obj).parent().index();
	nextId = $(obj).parent().find('span.label').attr("id");
	if($('.listPanel .panel-default .panel-body .list-group li:eq(' + (index-1) + ') span.label').text()!='')
	{
		preId = $('.listPanel .panel-default .panel-body .list-group li:eq(' + (index-1) + ') span.label').attr("id");
		$(obj).parent().find('span.label').text($('.listPanel .panel-default .panel-body .list-group li:eq(' + (index-1) + ') span.label').text());
		$(obj).parent().find('span.label').attr("id",preId);
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + (index-1) + ') span.label').text(text);
		$('.listPanel .panel-default .panel-body .list-group li:eq(' + (index-1) + ') span.label').attr("id",nextId);
	}
}

//清空服务器志愿
window.empty_serverClass = function () {  
    $('#loading').removeClass('hide').addClass('show'); 
	cancleAllChoose();
}