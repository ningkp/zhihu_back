<?php
namespace Home\Controller;
use Think\Controller;
// header('Access-Control-Allow-Origin:*');  
// header('Access-Control-Allow-Methods:GET, POST, OPTIONS');        //跨域
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header('Access-Control-Allow-Methods: GET, POST, PUT');

//实现功能有
    // 1.上传数据集(数据逐一上传)
    // 2.获取下一个待标注数据(先按照random来做)
    // 3.上传标注数据 & 保存标注历史
    // 4.创建者获取所有人的标注历史，普通用户获取自己的历史

class DataApiController extends Controller {
    public function test(){
        $redis=new \Redis();
        $redis->connect('127.0.0.1',40001);
        $redis->auth('algroup2019');
        $redis->set('name','hello,redis');
        echo $redis->get('name');
        phpinfo();
        //测试调用python
        // $pro = "python /home/wwwroot/default/alcloud/alcloud/feature/test.py 1111 222";
        // $pro = '/root/anaconda3/bin/python /home/wwwroot/default/alcloud/alcloud/feature/img_feature.py "/home/wwwroot/default/./Public/Img Sel Data/9/16" 方法1 "/home/wwwroot/default/./Public/Img Sel Data/9/16_Features/fea_vector.pik"';
        // $pro = '/usr/local/bin/sshpass -p ALcloud2019 rsync -avz --delete -e ssh "/home/wwwroot/default/./Public/Img Sel Data/9/18/" root@172.26.111.197:/mnt/uda1/test/ 2>&1';
        // $p = shell_exec($pro);
        
        // echo json_encode($p);
    }

    //上传数据集(数据逐一上传)    (上传大文件需要更改php.ini,upload_max_filesize、post_max_size)
    public function uploadDataSet(){
        //前端逐一上传，存放在服务端"./Image/用户ID/项目ID/文件名"，并设置好索引
        $token = $_POST['token'];
        $pid = $_POST['projectId'];
        $dataType = $_POST['dataType'];
        $isLast = $_POST['isLast'];

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
        $pData = M('project_info')->where(array('pId'=>$pid))->order('pId')->find();
        if($uData['uId']!=$pData['uId']){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to upload data!";
            $return = json_encode($return);
            echo $return;
            die();
        }

        $file = $_FILES['file'];//得到传输的数据
        //得到文件名称
        $name = $file['name'];

        $type = strtolower(substr($name,strrpos($name,'.')+1)); //得到文件类型，并且都转化成小写

        //根据dataType来判断文件类型是否被允许上传
        if($dataType=="Image"){
            $allow_type = array('jpg','jpeg','gif','png'); //定义允许上传的类型
        }elseif($dataType=="Audio"){
            $allow_type = array('mp3'); //定义允许上传的类型
        }elseif($dataType=="Text"){
            $allow_type = array('txt','md');               //定义允许上传的类型
        }elseif($dataType=="Video"){
            $allow_type = array('avi','mp4');              //定义允许上传的类型
        }

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
        $upload_path = "./Public/".$dataType."/"; //上传文件的存放路径
        $rootUrl = "http://39.100.145.105";
        $dDir1 = $upload_path.$uData['uId'];            //一级文件夹
        $dDir2 = $upload_path.$uData['uId']."/".$pid;   //二级文件夹
        $dDir2_Feature = $upload_path.$uData['uId']."/".$pid."_Features";   //特征文件夹
        $dSrc = $upload_path.$uData['uId']."/".$pid."/".$name;  //本地路径
        $dSrc_Feature = $upload_path.$uData['uId']."/".$pid."_Features/fea_vector.pik"; //特征文件路径
        $dSrc2 = $rootUrl."//Public/".$dataType."/".$uData['uId']."/".$pid."/".$name;   //外网访问路径
        
        //判断一级文件夹是否存在
        if(!is_dir($dDir1)){
            mkdir($dDir1,0777);  
        } 
        //判断二级文件夹是否存在
        if(!is_dir($dDir2)){
            mkdir($dDir2,0777);  
        } 
        //判断特征文件是否存在
        if(!is_dir($dDir2_Feature)){
            mkdir($dDir2_Feature,0777);  
        } 

        //如果名字重复只需要更新即可!!!!!!!!!!!!----------------------------------d
        $updateFlag = FALSE;
        if(file_exists(iconv("UTF-8","gb2312",$dSrc))){
            $updateFlag = TRUE;
        }

        //开始移动文件到相应的文件夹(该函数不会自动创建文件夹)
        if(move_uploaded_file($file['tmp_name'],iconv("UTF-8","gb2312",$dSrc))){
            //提取数据特征！(等将python代码加入到该项目中)

            //上传最后一个数据后才一起提特征
            if($isLast=="1"){

                $pro = "";  #命令
                // $rootP = "E:/nkp/wamp64/www/".$dDir2;
                $rootP = "/home/wwwroot/default/".$dDir2;
                
                // $saveFile = "E:/nkp/wamp64/www/".$dSrc_Feature;
                $saveFile = "/home/wwwroot/default/".$dSrc_Feature;
                
                $param = '"'.iconv("UTF-8","gb2312",$rootP).'"'." ".$pData['pFeaMethod']." ".'"'.iconv("UTF-8","gb2312",$saveFile).'"';    #参数
                if($dataType=="Image"){
                    // $pro = "python E:/nkp/wamp64/www/alcloud/alcloud/feature/img_feature.py ";
                    $pro = "/root/anaconda3/bin/python /home/wwwroot/default/alcloud/alcloud/feature/img_feature.py ";

                }elseif($dataType=="Audio"){
                    // $pro = "python E:/nkp/wamp64/www/alcloud/alcloud/feature/img_feature.py ";
                    $pro = "/root/anaconda3/bin/python /home/wwwroot/default/alcloud/alcloud/feature/audio_feature.py ";
                    
                }elseif($dataType=="Text"){
                    // $pro = "python E:/nkp/wamp64/www/alcloud/alcloud/feature/txt_feature.py ";
                    $pro = "/root/anaconda3/bin/python /home/wwwroot/default/alcloud/alcloud/feature/txt_feature.py ";
                
                }elseif($dataType=="Video"){
                    // $pro = "python E:/nkp/wamp64/www/alcloud/alcloud/feature/video_feature.py ";
                    $pro = "/root/anaconda3/bin/python /home/wwwroot/default/alcloud/alcloud/feature/video_feature.py ";
                
                }
                // ./Public/Img Sel Data/9/24/avatar-1.jpg 方法1
                
                #提取得到特征并存入到文件中 让python写文件
                $featureVector = shell_exec($pro.$param.' 2>&1');
                // $return['vector'] = $featureVector;
                // $return['state'] = 'error';
                // $return['info'] = $pro.$param;
                // $return = json_encode($return);
                // echo $return;
                // die();
                if($featureVector==null){
                    $return['state'] = 'error';
                    $return['info'] = $pro.$param;
                    $return = json_encode($return);
                    echo $return;
                    die();
                }

                //同步数据
                $pro1 = 'sshpass -p ALcloud2019 rsync -avz --delete -e ssh '.'"'.iconv("UTF-8","gb2312",$rootP).'"'.' root@172.26.111.197:/mnt/uda1/user_data/';
                $pro2 = 'sshpass -p ALcloud2019 rsync -avz --delete -e ssh '.'"'.iconv("UTF-8","gb2312",$saveFile).'"'.' root@172.26.111.197:/mnt/uda1/user_fea/'.$pid.'/';
                $p1 = shell_exec($pro1);
                $p2 = shell_exec($pro2);
                $pro1 = 'sshpass -p ALcloud2019 rsync -avz --delete -e ssh '.'"'.iconv("UTF-8","gb2312",$rootP).'"'.' root@172.26.111.196:/mnt/uda1/user_data/';
                $pro2 = 'sshpass -p ALcloud2019 rsync -avz --delete -e ssh '.'"'.iconv("UTF-8","gb2312",$saveFile).'"'.' root@172.26.111.196:/mnt/uda1/user_fea/'.$pid.'/';
                $p1 = shell_exec($pro1);
                $p2 = shell_exec($pro2);
            }

            if($updateFlag==FALSE){
                //每个data的信息都要存入数据库
                $data_arr['pId'] = $pid;
                $data_arr['uId'] = $uData['uId'];
                $data_arr['dName'] = $name;
                $data_arr['dSrc'] = $dSrc2;
                $data_arr['dIndex'] = 0;    #初始化为未读
                $data_arr ["dUploadTime"] = date ( 'Y-m-d H:i:s', time () );
                
                $data = D ( 'model_data' );
                if(!$data->create($data_arr)){
                    $return['state'] = 'error';
                    $return['info'] = "Network Error! Refresh and Retry!";
                    $return = json_encode($return);
                    echo $return;
                    die();
                }else{
                    $data->add();
                }
            }else{
                //更新
                $data_new['dUploadTime'] = date('Y-m-d H:i:s',time());
                $data_new['dSignJson'] = null;
                $data_new['dIsSign'] = 0;
                $data_new['dSignTime'] = null;
                $model = M('model_data');
                $model -> data($data_new)->where(array('pId'=>$pid,'uId'=>$uData['uId'],'dName'=>$name))->save();
            }

            //修改model_info
            $data_new2['pUploadData'] = 1;
            M('project_info') -> data($data_new2)->where(array('pId'=>$pid))->save();
            
            $return['state'] = 'success';
            $return['info'] = "Successfully!";
            $return = json_encode($return);
            echo $return;
        }else{
            $return['state'] = 'error';
            $return['info'] = "Failed!";
            $return = json_encode($return);
            echo $return;
        }
    }

    //上传初始标记集
    public function uploadIniDataSet(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];
        $dataType = $_POST['dataType'];

        //判断token是否为该pid的创始人
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_info')->where(array('pId'=>$pid))->order('pId')->find();
        if($uData['uId']!=$pData['uId']){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to upload data!";
            $return = json_encode($return);
            echo $return;
            die();
        }

        $file = $_FILES['file'];//得到传输的数据
        //得到文件名称
        $name = $file['name'];

        $type = strtolower(substr($name,strrpos($name,'.')+1)); //得到文件类型，并且都转化成小写

        //根据dataType来判断文件类型是否被允许上传
        if($dataType=="Image"){
            $allow_type = array('csv'); //定义允许上传的类型
        }elseif($dataType=="Audio"){
            $allow_type = array('csv'); //定义允许上传的类型
        }elseif($dataType=="Text"){
            $allow_type = array('csv');               //定义允许上传的类型
        }elseif($dataType=="Video"){
            $allow_type = array('csv');              //定义允许上传的类型
        }

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

        
        //--------------------------------解析csv--------------------------------
        //打开要读的文件
        $handle = fopen($file['tmp_name'], 'r');
        // $labelSpace = 
        //解析csv文件
        $dNameArr = [];
        $dSignJsonArr = [];
        $labelSpace = [];
        $count = 0;
        $countLabel = 0;

        while ($arrResult = fgetcsv($handle)) {
            //判断读到的每一行是否有值
            if (!empty($arrResult)) {
                //编码转换
                for($i=0;$i<count($arrResult);$i++){
                    $arrResult[$i]=iconv('gb2312','utf-8',$arrResult[$i]); 
                }
                $dName = $arrResult[0];
                $dSignJson = $arrResult[1];

                // echo(json_decode($arrResult[1])->anno_obj->text);
                $dNameArr[$count] = $dName;
                $dSignJsonArr[$count] = $dSignJson;
                $count++;

                if(!in_array(json_decode($arrResult[1])->anno_obj->text,$labelSpace)){
                    $labelSpace[$countLabel] = json_decode($arrResult[1])->anno_obj->text;
                    $countLabel++;
                }
                // echo $dName;
                // echo json_encode($dSignJson);
                // die();
            }
        }
        // echo json_encode($dSignJsonArr);
        //关闭文件流
        fclose($handle);
        // die();

        //--------------------------------将对应的数据添加标记，并标注其未初始标记集--------------------------------
        $redis=new \Redis();
        $redis->connect('127.0.0.1',40001);
        $redis->auth('algroup2019');
        $redis->select(1);

        for($i=0;$i<count($dSignJsonArr);$i++){
            $dName = $dNameArr[$i];
            $dSignJson = $dSignJsonArr[$i];
            $dIsSign = 3;
            $dType = 1;
            $dSignTime = date('Y-m-d H:i:s',time());

            //更新
            M('model_data') -> data(array('dSignJson'=>$dSignJson,'dIsSign'=>$dIsSign,'dType'=>$dType,'dSignTime'=>$dSignTime))->where(array('pId'=>$pid,'uId'=>$uData['uId'],'dName'=>$dName))->save();
            
            $dData = M('model_data') -> where(array('pId'=>$pid,'uId'=>$uData['uId'],'dName'=>$dName))->find();

            //往db为1的容器里对projectId添加所有的数据id
            $redis->lPush($pid,$dData['id']);
            //添加projectID_dataIndex
            $redis->set($pid."_".$dData['id'],$dSignJson);
        }

        //--------------------------------提取标记空间到projectInfo--------------------------------
        $labelSpaceStr = "";
        for($i=0;$i<count($labelSpace);$i++){
            $labelSpaceStr = $labelSpaceStr.$labelSpace[$i];
            if($i<count($labelSpace)-1){
                $labelSpaceStr .= ",";
            }
        }
        //更新
        M('project_info') -> data(array('pLabelSpace'=>$labelSpaceStr,'pIniSet'=>1))->where(array('pId'=>$pid,'uId'=>$uData['uId']))->save();
        //往redis中addSet一个projectId, 主动学习根据redis里的id来更新算法
        //往labelArrivalProject中添加新上传的projectId
        $requestId = $redis->sAdd('labelArrivalProject',$pid);

        $return['state'] = 'success';
        $return['info'] = "Successfully!";
        $return = json_encode($return);
        echo $return;
    }

    //上传测试标记
    public function uploadTestDataSet(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];
        $dataType = $_POST['dataType'];

        //判断token是否为该pid的创始人
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_info')->where(array('pId'=>$pid))->order('pId')->find();
        if($uData['uId']!=$pData['uId']){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to upload data!";
            $return = json_encode($return);
            echo $return;
            die();
        }

        $file = $_FILES['file'];//得到传输的数据
        //得到文件名称
        $name = $file['name'];

        $type = strtolower(substr($name,strrpos($name,'.')+1)); //得到文件类型，并且都转化成小写

        //根据dataType来判断文件类型是否被允许上传
        if($dataType=="Image"){
            $allow_type = array('csv'); //定义允许上传的类型
        }elseif($dataType=="Audio"){
            $allow_type = array('csv'); //定义允许上传的类型
        }elseif($dataType=="Text"){
            $allow_type = array('csv');               //定义允许上传的类型
        }elseif($dataType=="Video"){
            $allow_type = array('csv');              //定义允许上传的类型
        }

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

        
        //--------------------------------解析csv--------------------------------
        //打开要读的文件
        $handle = fopen($file['tmp_name'], 'r');
        // $labelSpace = 
        //解析csv文件
        $dNameArr = [];
        $dSignJsonArr = [];
        $labelSpace = [];
        $count = 0;
        $countLabel = 0;

        while ($arrResult = fgetcsv($handle)) {
            //判断读到的每一行是否有值
            if (!empty($arrResult)) {
                //编码转换
                for($i=0;$i<count($arrResult);$i++){
                    $arrResult[$i]=iconv('gb2312','utf-8',$arrResult[$i]); 
                }
                $dName = $arrResult[0];
                $dSignJson = $arrResult[1];

                // echo(json_decode($arrResult[1])->anno_obj->text);
                $dNameArr[$count] = $dName;
                $dSignJsonArr[$count] = $dSignJson;
                $count++;

                if(!in_array(json_decode($arrResult[1])->anno_obj->text,$labelSpace)){
                    $labelSpace[$countLabel] = json_decode($arrResult[1])->anno_obj->text;
                    $countLabel++;
                }
                // echo $dName;
                // echo json_encode($dSignJson);
                // die();
            }
        }
        // echo json_encode($dSignJsonArr);
        //关闭文件流
        fclose($handle);
        // die();

        //--------------------------------将对应的数据添加标记，并标注其未初始标记集--------------------------------
        for($i=0;$i<count($dSignJsonArr);$i++){
            $dName = $dNameArr[$i];
            $dSignJson = $dSignJsonArr[$i];
            $dIsSign = 3;
            $dType = 2;
            $dSignTime = date('Y-m-d H:i:s',time());

            //更新
            M('model_data') -> data(array('dSignJson'=>$dSignJson,'dIsSign'=>$dIsSign,'dType'=>$dType,'dSignTime'=>$dSignTime))->where(array('pId'=>$pid,'uId'=>$uData['uId'],'dName'=>$dName))->save();
        }

        //--------------------------------更新projectInfo--------------------------------
        //更新
        M('project_info') -> data(array('pNeedTest'=>1))->where(array('pId'=>$pid,'uId'=>$uData['uId']))->save();
        
        $return['state'] = 'success';
        $return['info'] = "Successfully!";
        $return = json_encode($return);
        echo $return;
    }

    //获取下一个待标注数据(先按照random来做)
    public function getNextData(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];

        //判断token是否为该pid的成员
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_list')->where(array('pId'=>$pid,'uId'=>$uData['uId']))->order('pId')->find();
        if($pData==null||$pData['isCreater']==1){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to label!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        
        //判断AL是否准备好
        $projectInfoData = M('project_info')->where(array('pId'=>$pid))->find();
        if($projectInfoData['pProjStatus']!=1){
            $return['state'] = 'error';
            $return['info'] = "The project is not ready yet!";
            $return = json_encode($return);
            echo $return;
            die();
        }

        //从redis中pop一个数据
        $redis=new \Redis();
        $redis->connect('127.0.0.1',40001);
        $redis->auth('algroup2019');
        $redis->select(0);
        //根据项目id获取该项目下的数据id, redis里的id顺序由主动学习生成
        $requestId = $redis->lPop($pid);
        if($requestId==null){
            $return['state'] = 'error';
            $return['info'] = '后台正在计算中!';
            echo json_encode($return);
            die();
        }else{
            //对该数据id在数据库判断其dIsSign是否为0
            $dData = M('model_data')->where(array('id'=>$requestId,'dIsSign'=>0))->order('id')->find();
            //将该数据dIsSign设置为1
            M('model_data')->data(array('dIsSign'=>1))->where(array('id'=>$requestId))->save();
            $return['state'] = 'success';
            $return['query'] = $dData;
            $return = json_encode($return);
            echo $return;
            die();
        }

        // //按照策略获取待查询的数据
        // $dData = M('model_data')->where(array('pId'=>$pid,'dIsSign'=>0))->order('id')->select();
        // $randIndex = rand(0,count($dData)-1);

        // $return['state'] = 'success';
        // $return['query'] = $dData[$randIndex];
        // $return = json_encode($return);
        // echo $return;
    }

    //获取下一个待标注数据(先按照random来做)
    public function getNextData2(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];

        //判断token是否为该pid的成员
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_list')->where(array('pId'=>$pid,'uId'=>$uData['uId']))->order('pId')->find();
        if($pData==null||$pData['isCreater']==1){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to label!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        
        //按照策略获取待查询的数据
        $dData = M('model_data')->where(array('pId'=>$pid,'dIsSign'=>0))->order('id')->select();
        $randIndex = rand(0,count($dData)-1);

        $return['state'] = 'success';
        $return['query'] = $dData[$randIndex];
        $return = json_encode($return);
        echo $return;
    }

    //上传标注数据 & 保存标注历史
    public function uploadLabeledData(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];
        $did = $_POST['dataId'];
        $dSignJson = $_POST['signJson'];

        //判断token是否为该pid的成员
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_list')->where(array('pId'=>$pid,'uId'=>$uData['uId']))->order('pId')->find();
        if($pData==null||$pData['isCreater']==1){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to label!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        
        //往redis里添加新标注   告诉后台有新数据上传
        $redis=new \Redis();
        $redis->connect('127.0.0.1',40001);
        $redis->auth('algroup2019');
        $redis->select(1);
        //往db为1的容器里对projectId添加所有的数据id
        $redis->lPush($pid,$did);
        //添加projectID_dataIndex
        $redis->set($pid."_".$did,$dSignJson);
        //往labelArrivalProject中addSet一个projectId, 主动学习根据redis里的id来更新算法
        $requestId = $redis->sAdd('labelArrivalProject',$pid);

        //将标注存入数据库
        $data_new['dSignJson'] = $dSignJson;
        $data_new['dIsSign'] = 2;   #标注但未保存
        $data_new['dSignTime'] = date('Y-m-d H:i:s',time());
        
        $model = M('model_data');
        $model -> data($data_new)->where(array('id'=>$did))->save();

        //获取样本名
        $dData = M('model_data')->where(array('id'=>$did))->order('id')->find();

        //将标注历史存入数据库
        $data_arr['dId'] = $did;
        $data_arr['dName'] = $dData['dName'];
        $data_arr['pId'] = $pid;
        $data_arr['uId'] = $uData['uId'];
        $data_arr['hSignContent'] = $dSignJson;
        $data_arr ["hSignTime"] = $data_new['dSignTime'];

        $data = D ( 'sign_history' );
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
        $return['info'] = 'Successful annotation!';
        $return = json_encode($return);
        echo $return;
    }

    //创建者获取所有人的标注历史，普通用户获取自己的历史
    public function getSignHistory(){
        $token = $_POST['token'];
        $pid = $_POST['projectId'];
        
        //判断token是否为该pid的成员
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $pData = M('project_list')->where(array('pId'=>$pid,'uId'=>$uData['uId']))->order('pId')->find();
        if($pData==null){
            $return['state'] = 'error';
            $return['info'] = "You don't have permission to get history!";
            $return = json_encode($return);
            echo $return;
            die();
        }

        //判断用户类型
        if($pData['isCreater']==1){
            //获取所有用户的历史
            $hData = M('sign_history')->where(array('pId'=>$pid))->order('id')->select();
            $return['state'] = 'success';
            $return['history'] = $hData;
            $return = json_encode($return);
            echo $return;
            die();
        }else{
            //获取自己的历史
            $hData = M('sign_history')->where(array('pId'=>$pid,'uId'=>$uData['uId']))->order('id')->select();
            $return['state'] = 'success';
            $return['history'] = $hData;
            $return = json_encode($return);
            echo $return;
            die();
        }
    }

    //获取自己所有的标记历史
    public function getMySignHistory(){
        $token = $_POST['token'];
        
        //判断token是否为该pid的成员
        if($token==""){
            $return['state'] = 'error';
            $return['info'] = "Please login again if authentication fails!";
            $return = json_encode($return);
            echo $return;
            die();
        }
        $uData = M('user')->where(array('uToken'=>$token))->order('uToken')->find();
        $hData = M('sign_history')->where(array('uId'=>$uData['uId']))->order('id')->select();
        $return['state'] = 'success';
        $return['history'] = $hData;
        $return = json_encode($return);
        echo $return;
    }
}