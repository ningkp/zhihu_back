<?php
namespace Home\Controller;
use Think\Controller;
header('Access-Control-Allow-Origin:*');  
header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域

//实现功能有
    // 1.发送消息
    // 2.检测已读情况
    // 3.接收消息
    // 4.设置为已读

class NewsApiController extends Controller {
    public function test(){
		echo "successful news_api test!";
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
    
    public function sendNews(){
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
            $judge=$_POST['receiveUE'];
            if($this->checkstr($judge)){
                $map2['uEmail'] = $judge;
            }
            else{
                $map2['uName'] = $judge;
            }
            //判断用户名邮箱是否存在
            $receiver = M('user')->where($map2)->order('uId')->find();
            if($receiver==null){
                $return['state'] = 'error';
                $return['info'] = 'The userName or email does not exist.';
                $return = json_encode($return);
                echo $return;
                die();
            }
            //不能给自己留言
            if($judge==$data['uEmail']||$judge==$data['uName']){
                $return['state'] = 'error';
                $return['info'] = "You can't leave messages for yourself.";
                $return = json_encode($return);
                echo $return;
                die();
            }

            //插入消息
            $data_arr['receiveId'] = $receiver['uId'];
            $data_arr['sendId'] = $data['uId'];
            $data_arr['content'] = $_POST['content'];
            $data_arr['isRead'] = 0;    #初始化为未读
            $data_arr ["time"] = date ( 'Y-m-d H:i:s', time () );
            
            $data = D ( 'news_list' );
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
            $return['info'] = 'Successful send!';
            $return = json_encode($return);
            echo $return;
        }
    }

    public function checkIsRead(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['id'] = $_POST['newsId'];
            $data = M('news_list')->where($map)->order('id')->find();
            $return['state'] = 'success';
            $return['info'] = 'Successful send!';
            $return['isRead'] = $data['isRead'];
            $return = json_encode($return);
            echo $return;
        }
    }

    public function receiveNews(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['uToken'] = $_POST['token'];
            $data = M('user')->where($map)->order('uToken')->find();
            $map2['receiveId'] = $data['uId'];
            //连表查询
            // $news = M('news_list')->join('user u ON news_list.sendId=u.uId')->where($map2)->order('time desc')->select();
            // $news = M('news_list a')->join('user b')->where('a.sendid = b.uid')->select();
            // $news = M('news_list')->where($map2)->order('time desc')->select();
            $Model = new \Think\Model();
            
            $news = $Model->query("select a.id,a.sendId,a.receiveId,a.content,a.isRead,a.time,b.uId,b.uName,b.uImgSrc from tp_news_list as a left join tp_user as b on a.sendId=b.uId where a.receiveId=".$data['uId']." order by a.time desc");

            $return['state'] = 'success';
            $return['newsList'] = $news;
            $return = json_encode($return);
            echo $return;
        }
    }

    public function setIsRead(){
        if($_POST['token']==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
        }
        else{
            $map['id'] = $_POST['newsId'];
            $data_new ['isRead'] = 1;
            $model = M('news_list');
            $model -> data($data_new)->where($map)->save();
            $return ['state'] = 'success';
            $return ['info'] = "Successful!";
            $return = json_encode($return);
            echo $return;
        }
    }
}