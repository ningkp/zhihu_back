<?php
namespace Home\Controller;
use Think\Controller;
header('Access-Control-Allow-Origin:*');  
header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域

//实现功能有
    // 1.创建项目
    // 2.管理项目
    // 3.删除项目
    // 4.创建者添加项目成员
    // 5.非创建者离开项目
    // 6.获取我的项目列表
    // 7.根据项目id获取项目详细信息
    // 8.创建者获取项目成员


class ProjectApiController extends Controller {
    public function test(){
		echo "successful project_api test!";
    }

    public function uploadProBack(){
        //前端逐一上传，存放在服务端"./Image/用户ID/项目ID/文件名"，并设置好索引
        $token = $_POST['token'];
        $projectName = $_POST['projectId']; //这里传proName
        $dataType = $_POST['dataType'];

        // $return['1'] = $token;
        // $return['2'] = $pid;
        // $return['3'] = $dataType;
        // $return['4'] = $_FILES['file'];

        // echo json_encode($return);
        // die();
        //判断token是否为该pid的创始人
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();

        $file = $_FILES['file'];//得到传输的数据
        //得到文件名称
        $name = $file['name'];

        $type = strtolower(substr($name,strrpos($name,'.')+1)); //得到文件类型，并且都转化成小写

        $dataType = "projImg";
        $allow_type = array('jpg','jpeg','gif','png'); //定义允许上传的类型

        if(!in_array($type, $allow_type)){
            //如果不被允许，则直接停止程序运行
            $return['state'] = 'error';
            $return['info'] = "文件格式不對!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        //判断是否是通过HTTP POST上传的
        if(!is_uploaded_file($file['tmp_name'])){
            //如果不是通过HTTP POST上传的
            $return['state'] = 'error';
            $return['info'] = "請使用http POST 上傳方式";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $saveName = time().".".$type; //时间戳命名
        $upload_path = "./Public/".$dataType."/"; //上传文件的存放路径
        $rootUrl = "http://39.100.145.105";
        $dDir1 = $upload_path.$uData['uId'];            //一级文件夹
        $dSrc = $upload_path.$uData['uId']."/".$saveName;  //本地路径
        $dSrc2 = $rootUrl."//Public/".$dataType."/".$uData['uId']."/".$saveName;   //外网访问路径
        
        //判断一级文件夹是否存在
        if(!is_dir($dDir1)){
            mkdir($dDir1,777);  
        } 

        //开始移动文件到相应的文件夹(该函数不会自动创建文件夹)
        if(move_uploaded_file($file['tmp_name'],iconv("UTF-8","gb2312",$dSrc))){
            
            //修改project_info
            $data_new2['pImgSrc'] = $dSrc2;
            M('project_info') -> data($data_new2)->where(array('pName'=>$projectName,'uId'=>$uData['uId']))->save();

            //修改project_list
            M('project_list') -> data($data_new2)->where(array('pName'=>$projectName,'uId'=>$uData['uId']))->save();
            
            $return['state'] = 'success';
            $return['info'] = "Successfully!";
            $return['0'] = $projectName;
            $return['1'] = $uData['uId'];
            $return = json_encode($return);
            echo $return;
        }else{
            $return['state'] = 'error';
            $return['info'] = "Failed!";
            $return = json_encode($return);
            echo $return;
        }
    }

    private function checkstr($str){
		$st = "@";
		$temp = explode($st,$str);
		if(count($temp)>1){
			return true;
		}
		else{
			return false;
		}
	}
    
    public function creatProject(){
        
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            
            $personData = M('user')->where($map)->order('uToken')->find();

            #判断项目名是否创建过
            $tempMap['uId'] = $personData['uId'];
            $tempMap['pName'] = $_POST['projectName'];
            $test = M('project_info')->where($tempMap)->order('pId')->find();
            if($test!=null){
                $return['state'] = 'error';
                $return['info'] = 'The project name has been used.';
                $return = json_encode($return);
                echo $return;
                die();
            }

            
            //插入项目
            ###### 项目基本信息 #####
            $data_arr['pName'] = $_POST['projectName'];
            $data_arr['uId'] = $personData['uId'];
            $data_arr['pCreatTime'] = date ( 'Y-m-d H:i:s', time () );
            // $data_arr['pImgSrc'] = "";   项目头像在另外一个函数上传
            $data_arr['pRemark'] = $_POST['projectRemark'];

            ##### 项目模型参数信息 #####
            $data_arr['pDataType'] = $_POST['dataType'];            #数据类型
            $data_arr['pLabelType'] = $_POST['labelType'];            #标记类型
            $data_arr['pAnnotationType'] = $_POST['annotationType'];              #标注类型
            $data_arr['pFeaMethod'] = $_POST['feaMethod'];          #特征提取方法 
            $data_arr['pModel'] = $_POST['model'];                  #分类模型 
            $data_arr['pModelParam'] = $_POST['modelParam'];        #模型参数(json字符串) 
            $data_arr['pMetric'] = $_POST['metric'];                #性能度量 
            $data_arr['pQuery'] = $_POST['query'];                  #查询策略 
            $data_arr['pQueryParam'] = $_POST['queryParam'];        #查询策略参数(json字符串) 
            $data_arr['pQuerySpeedSet'] = $_POST['querySpeedSet'];  #查询加速设置(json字符串)  
            $data_arr['pLabelSpace'] = $_POST['labelSpace'];        #标记空间  (类别1,类别2)
            $data_arr['pLabelStore'] = $_POST['labelStore'];        #标注存储格式 
            $data_arr['pProjStatus'] = $_POST['projStatus'];        #项目状态
            $data_arr['pNeedTest'] = $_POST['needTest'];            #是否有上传测试集(0代表否，1代表是)
            $data_arr['pIniSet'] = $_POST['iniSet'];                #是否有上传初始标记集合(0代表否，1代表是)	
            
            #往project_info添加新的一条项目
            $data = D ( 'project_info' );
            $insertId = -1;
            if(!$data->create($data_arr)){
                $return['state'] = 'error';
                $return['info'] = "Network Error! Refresh and Retry!";
                $return = json_encode($return);
                echo $return;
                die();
            }else{
                $insertId = $data->add();
            }
            ###################################################################################
            
            $data_arr2['pId'] = $insertId;
            $data_arr2['pName'] = $data_arr['pName'];
            // $data_arr2['pImgSrc'] = $data_arr['pImgSrc'];   项目头像另外一个函数上传
            $data_arr2['pRemark'] = $data_arr['pRemark'];
            $data_arr2['uId'] = $data_arr['uId'];
            $data_arr2['uName'] = $personData['uName'];
            $data_arr2['uImgSrc'] = $personData['uImgSrc'];
            $data_arr2['isCreater'] = 1;
            $data_arr2['uJoinTime'] = $data_arr['pCreatTime'];

            #往project_list添加新的list
            $data2 = D('project_list');
            if(!$data2->create($data_arr2)){
                $return['state'] = 'error';
                $return['info'] = "Network Error! Refresh and Retry!";
                $return = json_encode($return);
                echo $return;
                die();
            }else{
                $data2->add();
            }

            $return['state'] = 'success';
            $return['info'] = 'Creat a project successfully!';
            $return = json_encode($return);
            echo $return;
        }
    }

    public function changeProject(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();

            #判断项目名是否创建过
            $tempMap['uId'] = $data['uId'];
            $tempMap['pName'] = $_POST['projectName'];
            $tempMap['pId'] = array('NEQ',$_POST['projectId']);
            $test = M('project_info')->where($tempMap)->order('pId')->find();
            if($test!=null){
                $return['state'] = 'error';
                $return['info'] = 'The project name has been used.';
                $return = json_encode($return);
                echo $return;
                die();
            }
            
            $map2['pId'] = $_POST['projectId'];
            $map2['uId'] = $data['uId'];
            $temp = M('project_info')->where($map2)->order('pId')->find();
            if($temp==NULL){
                $return['state'] = 'error';
                $return['info'] = "You don't have permission to modify";
                $return = json_encode($return);
                echo $return;
                die();
            }


            //修改项目
            ###### 项目基本信息 #####
            $data_new['pName'] = $_POST['projectName'];
            // $data_new['pImgSrc'] = "";   项目头像在另外一个函数上传
            $data_new['pRemark'] = $_POST['projectRemark'];

            ##### 项目模型参数信息 #####
            $data_new['pDataType'] = $_POST['dataType'];            #数据类型
            $data_new['pLabelType'] = $_POST['labelType'];            #标记类型
            $data_new['pAnnotationType'] = $_POST['annotationType'];              #标注类型
            $data_new['pFeaMethod'] = $_POST['feaMethod'];          #特征提取方法 
            $data_new['pModel'] = $_POST['model'];                  #分类模型 
            $data_new['pModelParam'] = $_POST['modelParam'];        #模型参数(json字符串) 
            $data_new['pMetric'] = $_POST['metric'];                #性能度量 
            $data_new['pQuery'] = $_POST['query'];                  #查询策略 
            $data_new['pQueryParam'] = $_POST['queryParam'];        #查询策略参数(json字符串) 
            $data_new['pQuerySpeedSet'] = $_POST['querySpeedSet'];  #查询加速设置(json字符串)
            $data_new['pLabelSpace'] = $_POST['labelSpace'];        #标记空间   
            $data_new['pLabelStore'] = $_POST['labelStore'];        #标注存储格式 
            $data_new['pProjStatus'] = $_POST['projStatus'];        #项目状态
            $data_new['pNeedTest'] = $_POST['needTest'];            #是否有上传测试集(0代表否，1代表是)
            $data_new['pIniSet'] = $_POST['iniSet'];                #是否有上传初始标记集合(0代表否，1代表是)	
            
            $model = M('project_info');
            $model -> data($data_new)->where($map2)->save();

            # 更新project_list
            $data_arr2['pName'] = $_POST['projectName'];
            // $data_arr2['pImgSrc'] = $data_arr['pImgSrc'];   项目头像另外一个函数上传
            $data_arr2['pRemark'] = $_POST['projectRemark'];
            
            $updateProList = M('project_list');
            //读取list的所有data
            $map3['pId'] = $_POST['projectId'];
            $allProListData = $updateProList->where($map3)->select();
            //更新list
            for($i=0;$i<count($allProListData);$i++){
                $updateListMap['pId'] = $allProListData[$i]['pId'];
                $updateListMap['uId'] = $allProListData[$i]['uId'];
                $updateProList -> data($data_arr2)->where($updateListMap)->save();
            }
            

            $return ['state'] = 'success';
            $return ['info'] = "Successful project modification!";
            $return = json_encode($return);
            echo $return;
        }
    }

    public function delProject(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            
            $map2['pId'] = $_POST['projectId'];
            $map2['uId'] = $data['uId'];
            $temp = M('project_info')->where($map2)->order('pId')->find();
            if($temp==NULL){
                $return['state'] = 'error';
                $return['info'] = "You don't have permission to delete";
                $return = json_encode($return);
                echo $return;
                die();
            }
            
            #删除project_info中的信息
            $delMap['pId'] = $_POST['projectId'];
            $flag = M("project_info")->where($delMap)->delete(); 
            #删除project_list中的信息
            $flag2 = M("project_list")->where($delMap)->delete(); 
            
            if($flag&&$flag2){
                $return ['state'] = 'success';
                $return ['info'] = "Successful delete!";
                $return = json_encode($return);
                echo $return;
            }else{
                $return ['state'] = 'error';
                $return ['error'] = "Unsuccessful delete!";
                $return = json_encode($return);
                echo $return;
            }
        }
    }

    #发送添加项目成员邀请(暂时使用直接邀请进入)
    public function addProjectMemberInvitation(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            
            #判断是否有邀请权限
            $map2['pId'] = $_POST['projectId'];
            $map2['uId'] = $data['uId'];
            $temp = M('project_info')->where($map2)->order('pId')->find();
            if($temp==NULL){
                $return['state'] = 'error';
                $return['info'] = "You don't have permission to add member!";
                $return = json_encode($return);
                echo $return;
                die();
            }
            

            #提交username or email来添加项目成员
            $ue = $_POST['ue'];
            if($this->checkstr($ue)){
                $map3['uEmail'] = $ue;
            }
            else{
                $map3['uName'] = $ue;
            }
            $personData = M('user')->where($map3)->order('uId')->find();

            #不能邀请自己
            if($data['uId']==$personData['uId']){
                $return['state'] = 'error';
                $return['info'] = "You can't invite yourself to join the project!";
                $return = json_encode($return);
                echo $return;
                die();
            }

            #不能重复邀请
            $test = M('project_list')->where(array('pId'=>$_POST['projectId'],'uId'=>$personData['uId']))->order('uId')->find();
            if($test!=null){
                $return['state'] = 'error';
                $return['info'] = "The member '".$_POST['ue']."' is already in this project!";
                $return = json_encode($return);
                echo $return;
                die();
            }

            if($personData!=null){
                #获取projectData
                $projectData = M('project_info')->where(array('pId'=>$_POST['projectId']))->order('pId')->find();
                $data_arr['pId'] = $_POST['projectId'];
                $data_arr['pName'] = $projectData['pName'];
                $data_arr['pImgSrc'] = $projectData['pImgSrc'];
                $data_arr['pRemark'] = $projectData['pRemark'];
                $data_arr['uId'] = $personData['uId'];
                $data_arr['uName'] = $personData['uName'];
                $data_arr['uImgSrc'] = $personData['uImgSrc'];
                $data_arr['isCreater'] = 0;
                $data_arr['uJoinTime'] = date ( 'Y-m-d H:i:s', time () );
    
                #往project_list添加新的list
                $data2 = D('project_list');
                if(!$data2->create($data_arr)){
                    $return['state'] = 'error';
                    $return['info'] = "Network Error! Refresh and Retry!";
                    $return = json_encode($return);
                    echo $return;
                    die();
                }else{
                    $data2->add();
                }

                #发送系统通知至被邀请人
                $data_arr_news['receiveId'] = $personData['uId'];
                $data_arr_news['sendId'] = -1;
                $data_arr_news['content'] = '您已被用户"'.$data['uName'].'"邀请至项目"'.$projectData['pName'].'"!';
                $data_arr_news['isRead'] = 0;    #初始化为未读
                $data_arr_news ["time"] = date ( 'Y-m-d H:i:s', time () );
                
                $newsData = D ( 'news_list' );
                if(!$newsData->create($data_arr_news)){
                    $return['state'] = 'error';
                    $return['info'] = "Network Error! Refresh and Retry!";
                    $return = json_encode($return);
                    echo $return;
                    die();
                }else{
                    $newsData->add();
                }
                
                $return['state'] = 'success';
                $return['info'] = "Add Member '".$_POST['ue']."' to project '".$temp['pName']."' successfully!";
                $return = json_encode($return);
                echo $return;
            }
            else{
                $return['state'] = 'error';
                $return['info'] = 'The userName or email does not exist.';
                $return = json_encode($return);
                echo $return;
            }
        }
    }

    #非创建者离开项目(是否为非创建者前端判断，需要发系统通知给管理者(前端自己发，uId为-1))
    public function leaveProject(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();

            //获取接收者id
            $projectData = M('project_info')->where(array('pId'=>$_POST['projectId']))->order('pId')->find();
            //发送系统通知
            $data_arr['receiveId'] = $projectData['uId'];
            $data_arr['sendId'] = -1;
            $data_arr['content'] = '用户"'.$data['uName'].'"已经离开了项目"'.$projectData['pName'].'"!';
            $data_arr['isRead'] = 0;    #初始化为未读
            $data_arr ["time"] = date ( 'Y-m-d H:i:s', time () );
            
            $newsData = D ( 'news_list' );
            if(!$newsData->create($data_arr)){
                $return['state'] = 'error';
                $return['info'] = "Network Error! Refresh and Retry!";
                $return = json_encode($return);
                echo $return;
                die();
            }else{
                $newsData->add();
            }

            
            $delMap['pId'] = $_POST['projectId'];
            $delMap['uId'] = $data['uId'];

            $flag = M("project_list")->where($delMap)->delete(); 
            if($flag){
                $return ['state'] = 'success';
                $return ['info'] = "Successful leave!";
                $return = json_encode($return);
                echo $return;
            }else{
                $return ['state'] = 'error';
                $return ['error'] = "Unsuccessful leave!";
                $return = json_encode($return);
                echo $return;
            }
        }
    }

    #获取我的项目列表
    public function getMyProjects(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $getType = $_POST['getType'];   #获取项目类型 0获取all，1获取我创建的，2获取我参与的
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            
            if($getType==0){
                $map_0['uId'] = $data['uId'];
                $projectList = M('project_list')->where($map_0)->order('uJoinTime desc')->select();

            }elseif($getType==1){
                $map_1['uId'] = $data['uId'];
                $map_1['isCreater'] = 1;
                $projectList = M('project_list')->where($map_1)->order('uJoinTime desc')->select();

            }elseif($getType==2){
                $map_2['uId'] = $data['uId'];
                $map_2['isCreater'] = 0;
                $projectList = M('project_list')->where($map_2)->order('uJoinTime desc')->select();
            }

            $return['state'] = 'success';
            $return['projectList'] = $projectList;
            $return = json_encode($return);
            echo $return;
        }
    }

    #根据项目id获取项目详细信息
    public function getProjectDetail(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            
            #获取projectData
            $projectData = M('project_info')->where(array('pId'=>$_POST['projectId']))->order('pId')->find();
            
            #获取项目创建者信息
            $tempData = M('user')->where(array('uId'=>$projectData['uId']))->order('uId')->find();
            $createrData['uName'] = $tempData['uName'];
            $createrData['uEmail'] = $tempData['uEmail'];
            $createrData['uImgSrc'] = $tempData['uImgSrc'];

            #获取是否为项目创建者
            $proListData = M('project_list')->where(array('pId'=>$_POST['projectId'],'uId'=>$data['uId']))->order('pId')->find();

            $projectData['createrData'] = $createrData;
            $projectData['isCreater'] = $proListData['isCreater'];

            $return['state'] = 'success';
            $return['projectData'] = $projectData;
            $return = json_encode($return);
            echo $return;
        }
    }

    #创建者获取项目成员
    public function getProjectMembers(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            
            $map2['pId'] = $_POST['projectId'];
            $map2['uId'] = $data['uId'];
            $temp = M('project_info')->where($map2)->order('pId')->find();
            if($temp==NULL){
                $return['state'] = 'error';
                $return['info'] = "You don't have permission to get project's members";
                $return = json_encode($return);
                echo $return;
                die();
            }

            $mapForGetMembers['pId'] = $_POST['projectId'];
            $membersList = M('project_list')->where($mapForGetMembers)->order('uJoinTime')->select();

            $return['state'] = 'success';
            $return['membersList'] = $membersList;
            $return = json_encode($return);
            echo $return;
        }
    }

}