
#RegApi:	
	
	url:	/Home/RegApi/checkNameRepeat
	type:	post
	data:	{'name':'name'}
	return	{'state': state, 'info':info}

---

	url:	/Home/RegApi/checkEmailRepeat
	type:	post
	data:	{'email':'email'}
	return	{'state': state, 'info':info}

---

	url:	/Home/RegApi/sendCode
	type:	post
	data:	{'email':'email'}
	return	{'state': state, 'info':info}

---

	url:	/Home/RegApi/checkCode
	type:	post
	data:	{
				'email':'email',
				'password':'password',
				'code':'401782',
				'name': 'name',
				'city': 'city',
				'company': 'company',
				'sex': 'sex',
				'education': 'education',
				'work': 'work',
				'title': 'title',
				'birth': 'birth',
				'remark': 'remark',
			}
	return	{'state': state, 'info':info, 'token': uToken}

---



#LogApi:	
	
	url:	/Home/LogApi/checkNameandMail
	type:	post
	data:	{'login':'name or email'}
	return	{'state': state, 'info':info}

---

	url:	/Home/LogApi/checkPassAndName
	type:	post
	data:	{'login':'name or email', 'password':'password'}
	return	{'state': state, 'info':info}

---

	url:	/Home/LogApi/forgetPass
	type:	post
	data:	{'email':'email'}
	return	{'state': state, 'info':info}

---

	url:	/Home/LogApi/changePass
	type:	post
	data:	{
				'email':'email',
				'password':'password',
				'code': 'code'
			}
	return	{'state': state, 'info':info, 'token': uToken}

---



#UserApi:

	url:	/Home/UserApi/getOthersInfo
	type:	post
	data:	{
				'token':'token',
				'id':'id'
			}
	return	{
				'state': state, 
				'info':info, 
				'id': id, 
				'name': name, 
				'email': email, 
				'regTime': regTime, 
				'city': city, 
				'company': company, 
				'sex': sex, 
				'education': education, 
				'work': work, 
				'title': title, 
				'birth': birth, 
				'imgSrc': imgSrc, 
				'remark': remark
			}

---

	url:	/Home/UserApi/getUserInfo
	type:	post
	data:	{'token':'token'}
	return	{
				'state': state, 
				'info':info, 
				'id': id, 
				'name': name, 
				'email': email, 
				'regTime': regTime, 
				'city': city, 
				'company': company, 
				'sex': sex, 
				'education': education, 
				'work': work, 
				'title': title, 
				'birth': birth, 
				'imgSrc': imgSrc, 
				'remark': remark
			}

---

	url:	/Home/UserApi/changeUserInfo
	type:	post
	data:	{
				'token': token, 
				'name': name, 
				'city': city, 
				'company': company, 
				'education': education, 
				'work': work, 
				'title': title, 
				'remark': remark
			}
	return	{'state': state, 'info':info}


	url:	/Home/UserApi/changePassword
	type:	post
	data:	{	
				'token':token,
				'passwordpast':passwordpast, 
				'passwordnew':passwordnew
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/RegApi/changeHeadImg
	type:	post
	data:	{'token':'token',file}
	return	{'state': state, 'info':info}



#NewsApi

	url:	/Home/NewsApi/sendNews
	type:	post
	data:	{
				'token': 'token',
				'receiveUE': 'UE',
				'content': content,
			}
	return	{'state': state, 'info':info}

---

	url:	/Home/NewsApi/checkIsRead
	type:	post
	data:	{'token':'token','newsId':newsId}
	return	{'state': state, 'info':info, 'isRead':isRead}
			
---

	url:	/Home/NewsApi/receiveNews
	type:	post
	data:	{'token':'token'}
	return	{
				'state': state,
				 'newsList':[{
					 			'id':id,
								'sendId':sendId,
								'receiveId':receiveId,
								'content':content,
								'isRead':isRead,
								'time':time
							}]
			}
	
---

	url:	/Home/NewsApi/setIsRead
	type:	post
	data:	{'token':'token', 'newsId':newsId}
	return	{'state': state, 'info':info}



#ProjectApi
	
	url:	/Home/ProjectApi/creatProject
	type:	post
	data:	{
				'token': 'token',
				'projectName': projectName,
				'projectRemark': projectRemark,
				'dataType':dataType,
				'signType':signType,
				'labelType':labelType,
				'feaMethod':feaMethod,
				'model':model,
				'modelParam':modelParam,
				'metric':metric,
				'query':query,
				'queryParam':queryParam,
				'querySpeedSet':querySpeedSet,
				'labelStore':labelStore,
				'projStatus':projStatus,
				'needTest':needTest,
				'iniSet':iniSet,
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/ProjectApi/changeProject
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
				'projectName': projectName,
				'projectRemark': projectRemark,
				'dataType':dataType,
				'signType':signType,
				'labelType':labelType,
				'feaMethod':feaMethod,
				'model':model,
				'modelParam':modelParam,
				'metric':metric,
				'query':query,
				'queryParam':queryParam,
				'querySpeedSet':querySpeedSet,
				'labelStore':labelStore,
				'projStatus':projStatus,
				'needTest':needTest,
				'iniSet':iniSet,
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/ProjectApi/delProject
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/ProjectApi/addProjectMemberInvitation
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
				'ue': username or email,
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/ProjectApi/leaveProject
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
			}
	return	{'state': state, 'info':info}

---
	
	url:	/Home/ProjectApi/getMyProjects
	type:	post
	data:	{
				'token': 'token',
				'getType': 0 or 1 or 2 (0获取all，1获取我创建的，2获取我参与的),
			}
	return	{
				'state': state, 
				'projectList':[{
									'id':id,
									'pId':pId,
									'pName':pName,
									'pImgSrc':pImgSrc,
									'pRemark':pRemark,
									'uId':uId,
									'uName':uName,
									'uImgSrc':uImgSrc,
									'isCreater':isCreater,
									'uJoinTime':uJoinTime,
							  }]
			}

---
	
	url:	/Home/ProjectApi/getProjectDetail
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
			}
	return	{
				'state': state, 
				'projectData':{
									'pId':pId,
									'pName':pName,
									'uId':uId,
									'pCreatTime':pCreatTime,
									'pImgSrc':pImgSrc,
									'pRemark':pRemark,
									'pDataType':pDataType,
									'pSignType':pSignType,
									'pLabelType':pLabelType,
									'pFeaMethod':pFeaMethod,
									'pModel':pModel,
									'pModelParam':pModelParam,
									'pMetric':pMetric,
									'pQuery':pQuery,
									'pQueryParam':pQueryParam,
									'pQuerySpeedSet':pQuerySpeedSet,
									'pLabelStore':pLabelStore,
									'isCreater':isCreater,
									'createrData':{
														'uName':uName,
														'uEmail':uEmail,
														'uImgSrc':uImgSrc,
												  }
							  }
			}

---
	
	url:	/Home/ProjectApi/getProjectMembers
	type:	post
	data:	{
				'token': 'token',
				'projectId': projectId,
			}
	return	{
				'state': state, 
				'membersList':[{
									'id':id,
									'pId':pId,
									'pName':pName,
									'pImgSrc':pImgSrc,
									'pRemark':pRemark,
									'uId':uId,
									'uName':uName,
									'uImgSrc':uImgSrc,
									'isCreater':isCreater,
									'uJoinTime':uJoinTime,
							  }]
			}

