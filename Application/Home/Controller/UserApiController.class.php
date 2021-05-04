<?php
namespace Home\Controller;
use Think\Controller;
header('Access-Control-Allow-Origin:*');  
header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域

//实现功能有
	// 1.获取个人资料(包括头像，姓名之类的。。)
	// 2.支持头像，昵称，城市等的修改，不能修改性别等固有属性。
	// 3.修改密码，通过输入旧密码修改。

class UserApiController extends Controller {
    public function test(){
		echo "successful user_api test!";
	}
    public function getOthersInfo(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uId'] = $_POST['id'];
            $data = M('user')->where($map)->order('uId')->find();
            $return ['state'] = 'success';
            $return ['info'] = "Geting others info successfully!";
            $return ['id'] = $data['uId'];
            $return ["name"] = $data['uName'];
            $return ["email"] = $data['uEmail'];
            $return ["regTime"] = $data['uRegTime'];
            $return ["city"] = $data['uCity'];
            $return ["company"] = $data['uCompany'];
            $return ["sex"] = $data ['uSex'];
            $return ["education"] = $data ['uEducation'];
            $return ["work"] = $data ['uWork'];
            $return ["title"] = $data ['uTitle'];
            $return ["birth"] = $data ['uBirth'];
            $return ["imgSrc"] = $data ['uImgSrc'];
            $return ["remark"] = $data ['uRemark'];
            $return = json_encode($return);
            echo $return;
        }
    }

    public function getUserInfo(){
    	$map['uToken'] = $_POST['token'];
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
        	$data = M('user')->where($map)->order('uToken')->find();
        	$return ['state'] = 'success';
            $return ['info'] = "Geting my info successfully!";
            $return ['id'] = $data['uId'];
            $return ["name"] = $data['uName'];
            $return ["email"] = $data['uEmail'];
            $return ["regTime"] = $data['uRegTime'];
            $return ["city"] = $data['uCity'];
            $return ["company"] = $data['uCompany'];
            $return ["sex"] = $data ['uSex'];
            $return ["education"] = $data ['uEducation'];
            $return ["work"] = $data ['uWork'];
            $return ["title"] = $data ['uTitle'];
            $return ["birth"] = $data ['uBirth'];
            $return ["imgSrc"] = $data ['uImgSrc'];
            $return ["remark"] = $data ['uRemark'];    	
        	$return = json_encode($return);
        	echo $return;
        }
    }

    public function changeUserInfo(){
    	$map['uToken'] = $_POST['token'];
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
        	$change_data['uName'] = $_POST['name'];
        	// $change_data['uImgSrc'] = $_POST['imgsrc'];
            $testName = M('user')->where(array('uName'=>$_POST['name']))->order('uId')->find();
            if($testName['uName']!=null&&$testName['uToken']!=$_POST['token']){
                $return['state'] = 'error';
                $return['info'] = 'The username has been used!';
                $return = json_encode($return);
                echo $return;
                die();
            }
            
            $change_data ["uCompany"] = $_POST['company'];
            $change_data ["uEducation"] = $_POST ['education'];
            $change_data ["uWork"] = $_POST ['work'];
            $change_data ["uTitle"] = $_POST ['title'];
            $change_data ["uRemark"] = $_POST ['remark'];   
        	$change_data['uCity'] = $_POST['city'];
        	$model = M('user');
            $model -> data($change_data)->where($map)->save();//1是有修改，0是无修改
            $return ['state'] = 'success';
    		$return ['info'] = "Successful revision of personal data!";
    		$return = json_encode($return);
            echo $return;
        }
    }

    public function changePassword(){
    	$map['uToken'] = $_POST['token'];
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
        	$password_past = $_POST['passwordpast'];
        	$password_new = $_POST['passwordnew'];
        	$data = M('user')->where($map)->order('uToken')->getField('uPas');
        	if($password_past!=$data){
                $return ['state'] = 'error';
        		$return ['info'] = 'The old password is incorrect!';
        		$return = json_encode($return);
            	echo $return;
        	}
        	else{
        		$data_new ['uPas'] = $password_new;
        		$model = M('user');
                $model -> data($data_new)->where($map)->save();
                $return ['state'] = 'success';
    			$return ['info'] = "Successful password modification!";
    			$return = json_encode($return);
    	        echo $return;
        	}
        }
    }

    public function uploadUserBack(){
        //前端逐一上传，存放在服务端"./Image/用户ID/项目ID/文件名"，并设置好索引
        $token = $_POST['token'];

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

        $dataType = "userImg";
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
        $saveName = $uData['uToken'].".".$type; //时间戳命名
        $upload_path = "./Public/".$dataType."/"; //上传文件的存放路径
        $rootUrl = "http://39.100.145.105";
        $dDir1 = $upload_path;            //一级文件夹
        $dSrc = $upload_path."/".$saveName;  //本地路径
        $dSrc2 = $rootUrl."//Public/".$dataType."/".$saveName;   //外网访问路径
        
        //判断一级文件夹是否存在
        if(!is_dir($dDir1)){
            mkdir($dDir1,777);  
        } 

        //开始移动文件到相应的文件夹(该函数不会自动创建文件夹)
        if(move_uploaded_file($file['tmp_name'],iconv("UTF-8","gb2312",$dSrc))){
            
            //修改project_info
            $data_new2['uImgSrc'] = $dSrc2;
            M('user') -> data($data_new2)->where(array('uId'=>$uData['uId']))->save();

            //修改project_list
            M('project_list') -> data($data_new2)->where(array('uId'=>$uData['uId']))->save();
            
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

    //上传头像图片
    // 1.token
    // 2.file
    public function changeHeadImg(){
        $file = $_FILES['file'];//得到传输的数据
        //得到文件名称
        $name = $file['name'];

        $token = $_POST['token'];

        $type = strtolower(substr($name,strrpos($name,'.')+1)); //得到文件类型，并且都转化成小写
        $allow_type = array('jpg','jpeg','gif','png'); //定义允许上传的类型
        //判断文件类型是否被允许上传
        if(!in_array($type, $allow_type)){
            //如果不被允许，则直接停止程序运行
            $return['error'] = "文件格式不對!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        //判断是否是通过HTTP POST上传的
        if(!is_uploaded_file($file['tmp_name'])){
            //如果不是通过HTTP POST上传的
            $return['error'] = "請使用http POST 上傳方式";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $upload_path = "./Img/head/"; //上传文件的存放路径
        $uImgSrc = $upload_path.$token.".".$type;
        //开始移动文件到相应的文件夹
        if(move_uploaded_file($file['tmp_name'],$uImgSrc)){
          
          //保存图片路径
            $data_arr ["uImgSrc"] = "http://192.168.56.1/Img/head/".$token.".".$type;
            $model = M('user');
            $model -> data($data_arr)->where(array('uToken'=>$token))->save();  
            
            $return['state'] = 'success';
            $return['info'] = "Successfully!";
            $return = json_encode($return);
            echo $return;
        }else{
            $return['error'] = "Failed!";
            $return = json_encode($return);
            echo $return;
        }
    } 

}