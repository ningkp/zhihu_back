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
		echo "successful Question_api test!";
	}

	public function haveQuestion(){
		if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            //插入问题
            $data_arr['uId'] = $_POST['uId'];
            $data_arr['question_str'] = $_POST['question_str'];
            $data_arr['question_content'] = $_POST['question_content'];
			$data_arr['question_type'] = $_POST['question_type'];
            $data_arr["time"] = date ( 'Y-m-d H:i:s', time () );
            
            $data = D ( 'question_list' );
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
            $return['info'] = 'Successful!';
            $return = json_encode($return);
            echo $return;
		}
	}

	# 获取问题细节
	public function getQuestionDetail(){
		if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['questionId'] = $_POST['questionId'];
            $data = M('question_list')->where($map)->order('questionId')->find();

            $return['state'] = 'success';
            $return['data'] = $data;
            $return = json_encode($return);
            echo $return;
		}
	}

	# 获取所有答案细节
	public function getAllAnswerDetail(){
		if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['questionId'] = $_POST['questionId'];
            $data = M('answer_list')->where($map)->order('answerId')->find();

            $return['state'] = 'success';
            $return['data'] = $data;
            $return = json_encode($return);
            echo $return;
		}
	}
	
}