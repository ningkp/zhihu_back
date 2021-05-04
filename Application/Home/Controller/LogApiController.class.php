<?php
namespace Home\Controller;
use Think\Controller;
header('Access-Control-Allow-Origin:*');  
header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域

//实现功能有
	// 1.忘记密码，通过邮箱验证码来更改密码但是只支持账号密码登录
	// 2.判断用户名/邮箱是否存在
	// 3.验证账号密码正确
	// 4.注销(这个可以在前端)  将token置空
class LogApiController extends Controller {
	public function test(){
		echo "successful log_api test!";
	}

	//发送验证码
    public function sendCode(){     
		// 检测是否已经注册 
		$map['uEmail'] = $_POST['email'];
		$randCode =rand(100000,900000);
		if(IS_POST){
			$to = $_POST['email'];
			//$to = "291371205@qq.com";
			$title = "AlCloud Register";
			$content = "Hi,I'm AlGroup。Welcome to register alCloud, the verification code is:".$randCode;
			$flag = sendMail($to,$title,$content);        //是否发送成功
		
			// session('CHECK_CODE',$randCode);
			// session('EMAIL_NUM',$to);
  
			//存入数据库
			$data_arr ["time"] = date ( 'Y-m-d H:i:s', time () );
			$data_arr ["email"] = $to;
			$data_arr ["code"] = $randCode;
			$data = D ('reg_code');
			if(!$data->create($data_arr)){
			  $return['state'] = 'error';
			  $return['info'] = "Network Error! Refresh and Retry!";
			  $return = json_encode($return);
			  echo $return;
			  die();
			}else{
			  $data->add();
			}
			$return['state'] = 'success';
			$return['info'] = "Verification code has been sent to mailbox!";
			$return = json_encode($return);
			echo $return;
		}
	}

	public function checkCode(){
        //先检测邮箱和用户名是否注册
        // 检测是否已经注册 
        $mapEmail['uEmail'] = $_POST['email'];
        $mapName['uName'] = $_POST['name'];

        $map['email'] = $_POST['email'];
        $data = M('reg_code')->where($map)->order('time desc')->getField('code');
        $code = $_POST['code'];
        if($code != $data){
			$return['state'] = 'error';
			$return['info'] = 'The verification code is incorrect, please re-enter it!';
			$return['uToken'] = "";
			$return = json_encode($return);
			echo $return;
        }else{
			//存入数据库
			$data_arr ["uToken"] = md5($_POST['email']);
			$data_arr ["uName"] = "";   
			$data_arr ["uEmail"] = $_POST['email']; 
			// $data_arr ["uRegTime"] = date ( 'Y-m-d H:i:s', time () );
			// $data_arr ["uCity"] = $_POST['city'];
			// $data_arr ["uCompany"] = $_POST['company'];
			// $data_arr ["uSex"] = $_POST['sex'];
			// $data_arr ["uEducation"] = $_POST['education'];
			// $data_arr ["uWork"] = $_POST['work'];
			// $data_arr ["uTitle"] = $_POST['title'];
			// $data_arr ["uBirth"] = $_POST['birth'];
			$data_arr ["uImgSrc"] = "http://localhost//Public/userImg/default.jpg";                 //注册使用默认头像
			// $data_arr ["uRemark"] = $_POST['remark'];
			$data = D ( 'user' );
			if(!$data->create($data_arr)){
				$return['state'] = 'error';
				$return['info'] = "Network Error! Refresh and Retry!";
				$return = json_encode($return);
				echo $return;
				die();
			}else{
				$data->add();
			}
			$return['state'] = 'success';
			$return['info'] = 'Successful register!';
			$return['uToken'] = $data_arr ["uToken"];    //返回token(用md5(pas))
			$return = json_encode($return);
			echo $return;
        }
    } 

	public function forgetPass(){
		$map['uEmail'] = $_POST['email'];
		$testEmail = M('user')->where($map)->order('uId')->getField('uId');
		if($testEmail==null){
			$return['state'] = 'error';
			$return['info'] = 'The email does not exist!';
			$return = json_encode($return);
			echo $return;
		}
		else{
			$randCode=rand(100000,900000);
			if(IS_POST){
				$temp = $_POST['email'];
				$title = "AlCloud ForgetPassword";
				$content = "Hi,I'm AlGroup。The verification code for changing password is ：".$randCode;
				$flag = sendMail($temp,$title,$content);
				$data_arr ["time"] = date ( 'Y-m-d H:i:s', time () );
         		$data_arr ["email"] = $temp;
         		$data_arr ["code"] = $randCode;
         		$data = D ( 'reg_code' );
         		if(!$data->create($data_arr)){
					$return['state'] = 'error';
         			$return['info'] = "Network Error! Refresh and Retry!";
		            $return = json_encode($return);
		            echo $return;
		            die();
         		}
         		else{
         			$data->add();
         		}
         		if($flag){
					$return['state'] = 'success';
         			$return['info'] = 'Verification code has been sent to mailbox!';
					$return = json_encode($return);
					echo $return;
         		}
         		else{
					$return['state'] = 'error';
         			$return['info'] = 'The verification code failed to send. Please try again later.';
					$return = json_encode($return);
					echo $return;
         		}
			}
		}
	}

	public function changePass(){
		$map['email'] = $_POST['email'];
		$map2['uEmail'] =  $_POST['email'];
		$data = M('reg_code')->where($map)->order('time desc')->getField('code');
		$code = $_POST['code'];
		if($code != $data){
			$return['state'] = 'error';
			$return['info'] = 'The verification code is incorrect, please re-enter it!';
			$return['token'] = "";
			$return = json_encode($return);
			echo $return;
			die();
		}
		else{
			$data_arr ["uPas"] = $_POST['password'];
			$model = M('user');
			$model -> data($data_arr)->where($map2)->save();
			$return['state'] = 'success';
			$return['info'] = 'Successful password modification!';
			$return['token'] = "";
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

	public function checkNameandMail(){
		$judge=$_POST['login'];
        if($this->checkstr($judge)){
        	$map['uEmail'] = $judge;
        }
        else{
        	$map['uName'] = $judge;
        }
        $test = M('user')->where($map)->order('uId')->find();
        if($test!=null){
			$return['state'] = 'success';
        	$return['info'] = 'The userName or email exists.';
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

    public function checkPassAndName(){
        $judge=$_POST['login'];
        $pass=md5($_POST['password']);
        if($this->checkstr($judge)){
        	$map['uEmail'] = $judge;
        }
        else{
        	$map['uName'] = $judge;
        }
        $test = M('user')->where($map)->order('uId')->find();
        if($test!=null){
        	if($test['uPas']==$pass){
				$return['state'] = 'success';
        		$return['info']="Login successfully!";
        		$return['token'] = $test['uToken'];
        		$return = json_encode($return);
        		echo $return;
        	}
        	else{
				$return['state'] = 'error';
        		$return['info']="Login failed! Username or password incorrect!";
        		$return = json_encode($return);
        		echo $return;
        	}
        }
        else{
			$return['state'] = 'error';
        	$return['info'] = 'The userName or email does not exist.';
        	$return = json_encode($return);
        	echo $return;
        }
    }
}