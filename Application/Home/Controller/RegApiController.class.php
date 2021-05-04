<?php
namespace Home\Controller;
use Think\Controller;
header('Access-Control-Allow-Origin:*');  
header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域

//实现功能有
// 	1.判断用户名(邮箱)和昵称是否重复
// 	2.邮箱验证码验证信息
// 	3.上传用户信息到数据库，头像存放到服务器

class RegApiController extends Controller {
    public function test(){
      echo "successful reg_api test!";
    }

    //判断用户名(邮箱)和昵称是否重复
    public function checkEmailRepeat(){
      $map['uEmail'] = $_POST['email'];
      $testEmail = M('user')->where($map)->order('uId')->getField('uId');
      if($testEmail!=null){
        $return['state'] = 'error';
        $return['info'] = 'The email has been registered.';
        $return = json_encode($return);
        echo $return;
      }else{
        $return['state'] = 'success';
        $return['info'] = 'The email can be used.';
        $return = json_encode($return);
        echo $return;
      }
    }

    public function checkNameRepeat(){
      $map['uName'] = $_POST['name'];
      $testName = M('user')->where($map)->order('uId')->getField('uId');
      if($testName!=null){
        $return['state'] = 'error';
        $return['info'] = 'The name has been registered.';
        $return = json_encode($return);
        echo $return;
      }else{
        $return['state'] = 'success';
        $return['info'] = 'The name can be used.';
        $return = json_encode($return);
        echo $return;
      }
    }



	 //发送验证码
    public function sendCode(){     
      // 检测是否已经注册 
      $map['uEmail'] = $_POST['email'];
      $testEmail = M('user')->where($map)->order('uId')->getField('uId');
      if($testEmail!=null){
        $return['state'] = 'error';
        $return['info'] = "The email has been registered.";
        $return = json_encode($return);
        echo $return;
        die();
      }
      //如果没有被注册
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

    //检测验证码并且save并且返回token
    public function checkCode(){
        //先检测邮箱和用户名是否注册
        // 检测是否已经注册 
        $mapEmail['uEmail'] = $_POST['email'];
        $testEmail = M('user')->where($mapEmail)->order('uId')->getField('uId');
        if($testEmail!=null){
          $return['state'] = 'error';
          $return['info'] = "The email has been registered.";
          $return = json_encode($return);
          echo $return;
          die();
        }
        $mapName['uName'] = $_POST['name'];
        $testName = M('user')->where($mapName)->order('uId')->getField('uId');
        if($testName!=null){
          $return['state'] = 'error';
          $return['info'] = 'The name has been registered.';
          $return = json_encode($return);
          echo $return;
          die();
        }

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
          $data_arr ["uName"] = $_POST['name'];   
          $data_arr ["uEmail"] = $_POST['email'];
          $data_arr ["uPas"] = md5($_POST['password']); 
          $data_arr ["uRegTime"] = date ( 'Y-m-d H:i:s', time () );
          $data_arr ["uCity"] = $_POST['city'];
          $data_arr ["uCompany"] = $_POST['company'];
          $data_arr ["uSex"] = $_POST['sex'];
          $data_arr ["uEducation"] = $_POST['education'];
          $data_arr ["uWork"] = $_POST['work'];
          $data_arr ["uTitle"] = $_POST['title'];
          $data_arr ["uBirth"] = $_POST['birth'];
          $data_arr ["uImgSrc"] = "http://localhost//Public/userImg/default.jpg";                 //注册使用默认头像
          $data_arr ["uRemark"] = $_POST['remark'];
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
}