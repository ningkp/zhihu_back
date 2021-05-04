-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1:3306
-- 生成日期： 2019-07-13 06:44:16
-- 服务器版本： 5.7.24
-- PHP 版本： 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `alcloud`
--
CREATE DATABASE IF NOT EXISTS `alcloud` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `alcloud`;

-- --------------------------------------------------------

--
-- 表的结构 `tp_model_data`
--

DROP TABLE IF EXISTS `tp_model_data`;
CREATE TABLE IF NOT EXISTS `tp_model_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pId` int(10) NOT NULL COMMENT '项目id',
  `uId` int(10) NOT NULL COMMENT '创始人',
  `dName` varchar(50) NOT NULL COMMENT '文件名',
  `dSrc` mediumtext NOT NULL COMMENT '数据src',
  `dSignJson` mediumtext COMMENT '数据标注',
  `dIsSign` int(1) NOT NULL DEFAULT '0' COMMENT '(0:未请求,1:请求但未标注,2:标注未保存,3:标注且保存)',
  `dIndex` int(10) NOT NULL COMMENT '索引',
  `dType` int(1) NOT NULL DEFAULT '0' COMMENT '(0:默认,1:初始标记,2:测试集)',
  `dUploadTime` datetime NOT NULL COMMENT '上传时间',
  `dSignTime` datetime DEFAULT NULL COMMENT '标注时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_model_data`
--

INSERT INTO `tp_model_data` (`id`, `pId`, `uId`, `dName`, `dSrc`, `dSignJson`, `dIsSign`, `dIndex`, `dType`, `dUploadTime`, `dSignTime`) VALUES
(1, 12, 9, '1.mp4', 'http://localhost//Public/Video Data/9/12/1.mp4', '{\"anno_obj\":{\"text\":\"休闲\"}}', 3, 0, 2, '2019-06-26 15:32:19', '2019-07-09 17:47:30'),
(2, 12, 9, '2.mp4', 'http://localhost//Public/Video Data/9/12/2.mp4', '{\"anno_obj\":{\"text\":\"舞蹈\"}}', 3, 0, 2, '2019-06-26 15:32:19', '2019-07-09 17:47:30'),
(3, 12, 9, '3.mp4', 'http://localhost//Public/Video Data/9/12/3.mp4', '{\"anno_obj\":{\"text\":\"休闲\"}}', 3, 0, 2, '2019-06-26 15:32:20', '2019-07-09 17:47:30'),
(4, 12, 9, '4.mp4', 'http://localhost//Public/Video Data/9/12/4.mp4', '{\"anno_obj\":{\"text\":\"娱乐\"}}', 3, 0, 2, '2019-06-26 15:32:20', '2019-07-09 17:47:30'),
(5, 12, 9, '5.mp4', 'http://localhost//Public/Video Data/9/12/5.mp4', '{\"anno_obj\":{\"text\":\"休闲\"}}', 1, 0, 0, '2019-06-26 15:32:21', '2019-06-26 15:34:01'),
(6, 9, 9, 'allPro代码.txt', 'http://localhost//Public/Text Data/9/9/allPro代码.txt', NULL, 0, 0, 0, '2019-06-26 15:33:01', NULL),
(7, 9, 9, 'api文档.md', 'http://localhost//Public/Text Data/9/9/api文档.md', NULL, 0, 0, 0, '2019-06-26 15:33:01', NULL),
(8, 9, 9, '阿联酋count100.txt', 'http://localhost//Public/Text Data/9/9/阿联酋count100.txt', NULL, 0, 0, 0, '2019-06-26 15:33:01', NULL),
(9, 9, 9, '阿曼count75.txt', 'http://localhost//Public/Text Data/9/9/阿曼count75.txt', '{\"anno_obj\":{\"text\":\"新闻\"}}', 1, 0, 0, '2019-06-26 15:33:01', '2019-06-26 15:34:26'),
(10, 9, 9, '埃塞俄比亚count100.txt', 'http://localhost//Public/Text Data/9/9/埃塞俄比亚count100.txt', NULL, 0, 0, 0, '2019-06-26 15:33:01', NULL),
(11, 9, 9, '安提瓜和巴布达count28.txt', 'http://localhost//Public/Text Data/9/9/安提瓜和巴布达count28.txt', '{\"anno_obj\":{\"text\":\"新闻\"}}', 1, 0, 0, '2019-06-26 15:33:01', '2019-06-26 15:35:02'),
(12, 9, 9, '巴巴多斯count30.txt', 'http://localhost//Public/Text Data/9/9/巴巴多斯count30.txt', '{\"anno_obj\":{\"text\":\"新闻\"}}', 1, 0, 0, '2019-06-26 15:33:01', '2019-07-08 12:23:31'),
(13, 9, 9, '中文文档.txt', 'http://localhost//Public/Text Data/9/9/中文文档.txt', NULL, 0, 0, 0, '2019-06-26 15:33:01', NULL),
(14, 13, 9, 'avatar-1.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-1.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(15, 13, 9, 'avatar-2.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-2.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(16, 13, 9, 'avatar-3.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-3.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(17, 13, 9, 'avatar-4.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-4.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(18, 13, 9, 'avatar-5.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-5.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(19, 13, 9, 'avatar-6.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-6.jpg', NULL, 0, 0, 0, '2019-06-26 15:32:41', NULL),
(20, 13, 9, 'avatar-7.jpg', 'http://localhost//Public/Img Sel Data/9/13/avatar-7.jpg', '{\"anno_obj\":{\"text\":\"熊猫\"}}', 1, 0, 0, '2019-06-25 20:38:47', '2019-06-25 20:44:30'),
(21, 14, 9, 'avatar-1.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-1.jpg', NULL, 0, 0, 0, '2019-06-26 15:31:00', NULL),
(22, 14, 9, 'avatar-2.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-2.jpg', NULL, 0, 0, 0, '2019-06-26 15:31:00', NULL),
(23, 14, 9, 'avatar-3.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-3.jpg', NULL, 0, 0, 0, '2019-06-26 15:31:00', NULL),
(24, 14, 9, 'avatar-4.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-4.jpg', NULL, 0, 0, 0, '2019-06-26 15:31:00', NULL),
(25, 14, 9, 'avatar-5.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-5.jpg', NULL, 0, 0, 0, '2019-06-26 15:31:01', NULL),
(26, 14, 9, 'avatar-6.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-6.jpg', '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.3416666666666667,\"y\":0.425,\"width\":0.31833333333333336,\"height\":0.14166666666666666},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', 1, 0, 0, '2019-06-26 15:31:01', '2019-06-26 15:31:29'),
(27, 14, 9, 'avatar-7.jpg', 'http://localhost//Public/Img Bbox Data/9/14/avatar-7.jpg', '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"11\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.28833333333333333,\"y\":0.46,\"width\":0.4116666666666667,\"height\":0.205},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', 0, 0, 0, '2019-06-26 15:31:01', '2019-06-26 15:31:53');

-- --------------------------------------------------------

--
-- 表的结构 `tp_news_list`
--

DROP TABLE IF EXISTS `tp_news_list`;
CREATE TABLE IF NOT EXISTS `tp_news_list` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sendId` int(10) NOT NULL COMMENT '发送者id(-1为系统通知)',
  `receiveId` int(10) NOT NULL COMMENT '接收者id',
  `content` mediumtext NOT NULL COMMENT '内容',
  `isRead` int(1) NOT NULL COMMENT '已读标志(0未读，1已读)',
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_news_list`
--

INSERT INTO `tp_news_list` (`id`, `sendId`, `receiveId`, `content`, `isRead`, `time`) VALUES
(2, 9, 10, '你好!', 1, '2019-06-06 21:59:22'),
(3, 9, 10, '222222', 1, '2019-06-06 22:05:20'),
(4, 10, 9, '你好呀', 1, '2019-06-08 17:38:26'),
(5, 9, 10, '嗯    不错', 1, '2019-06-08 17:49:48'),
(6, 9, 10, '你项目做的不错', 1, '2019-06-08 17:52:36'),
(7, 10, 9, '好的', 1, '2019-06-08 17:56:55'),
(8, 9, 10, '都打得', 1, '2019-06-08 17:57:45'),
(9, 9, 10, '测试', 1, '2019-06-11 11:48:19'),
(10, 9, 10, '111111', 1, '2019-06-12 14:26:51'),
(11, 10, 9, '44444', 1, '2019-06-14 18:06:52'),
(12, 9, 10, 'ok', 1, '2019-06-14 18:15:42'),
(27, -1, 9, '用户\"typ\"已经离开了项目\"视频车辆识别任务\"!', 1, '2019-06-16 17:14:15'),
(28, -1, 10, '您已被用户\"kid\"邀请至项目\"视频车辆识别任务\"!', 1, '2019-06-16 17:14:42'),
(26, -1, 9, '用户\"typ\"已经离开了项目\"超市零食图片分类\"!', 1, '2019-06-16 17:11:56'),
(23, -1, 9, '用户\"typ\"已经离开了项目\"新闻分类任务\"!', 1, '2019-06-16 17:06:04'),
(24, -1, 9, '用户\"typ\"已经离开了项目\"小视频分类任务\"!', 1, '2019-06-16 17:11:48'),
(25, -1, 9, '用户\"typ\"已经离开了项目\"视频车辆识别任务\"!', 1, '2019-06-16 17:11:52'),
(29, -1, 10, '您已被用户\"kid\"邀请至项目\"超市零食图片分类\"!', 1, '2019-06-16 17:14:53'),
(30, -1, 10, '您已被用户\"kid\"邀请至项目\"小视频分类任务\"!', 1, '2019-06-16 17:15:01'),
(31, -1, 10, '您已被用户\"kid\"邀请至项目\"新闻分类任务\"!', 1, '2019-06-16 17:15:11'),
(32, -1, 9, '用户\"typ\"已经离开了项目\"新闻分类任务\"!', 1, '2019-06-25 16:17:55'),
(33, -1, 10, '您已被用户\"kid\"邀请至项目\"新闻分类任务\"!', 1, '2019-06-25 16:18:15');

-- --------------------------------------------------------

--
-- 表的结构 `tp_project_info`
--

DROP TABLE IF EXISTS `tp_project_info`;
CREATE TABLE IF NOT EXISTS `tp_project_info` (
  `pId` int(10) NOT NULL AUTO_INCREMENT,
  `pName` varchar(50) NOT NULL,
  `uId` int(10) NOT NULL COMMENT '创建者id',
  `pCreatTime` datetime NOT NULL,
  `pImgSrc` mediumtext COMMENT '项目头像',
  `pRemark` mediumtext NOT NULL,
  `pDataType` varchar(50) NOT NULL COMMENT '数据类型',
  `pLabelType` varchar(50) NOT NULL COMMENT '标记类型',
  `pAnnotationType` varchar(50) NOT NULL COMMENT '标注类型',
  `pFeaMethod` varchar(50) NOT NULL COMMENT '特征提取方法',
  `pModel` varchar(50) NOT NULL COMMENT '分类模型',
  `pModelParam` mediumtext NOT NULL COMMENT '模型参数(json字符串)',
  `pMetric` varchar(50) NOT NULL COMMENT '性能度量',
  `pQuery` varchar(50) NOT NULL COMMENT '查询策略',
  `pQueryParam` mediumtext NOT NULL COMMENT '查询策略参数',
  `pQuerySpeedSet` mediumtext NOT NULL COMMENT '查询加速设置',
  `pLabelStore` varchar(50) NOT NULL COMMENT '标注存储格式',
  `pProjStatus` varchar(50) DEFAULT '0' COMMENT '项目状态(主动学习是否准备好数据了)',
  `pNeedTest` int(1) NOT NULL DEFAULT '0' COMMENT '是否有上传测试集(0代表否，1代表是)',
  `pIniSet` int(1) NOT NULL DEFAULT '0' COMMENT '是否有上传初始标记集合(0代表否，1代表是)',
  `pUploadData` int(1) NOT NULL DEFAULT '0' COMMENT '是否上传待训练数据',
  `pLabelSpace` mediumtext COMMENT '标记空间',
  PRIMARY KEY (`pId`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_project_info`
--

INSERT INTO `tp_project_info` (`pId`, `pName`, `uId`, `pCreatTime`, `pImgSrc`, `pRemark`, `pDataType`, `pLabelType`, `pAnnotationType`, `pFeaMethod`, `pModel`, `pModelParam`, `pMetric`, `pQuery`, `pQueryParam`, `pQuerySpeedSet`, `pLabelStore`, `pProjStatus`, `pNeedTest`, `pIniSet`, `pUploadData`, `pLabelSpace`) VALUES
(9, '新闻分类任务', 9, '2019-06-06 14:17:25', NULL, '将新闻分成不同的类别，例如：娱乐，体育，生活。。。', 'Text Data', 'Multi class', '111', '方法1', 'Regression', '', 'Accuracy', 'Random', '', 'set 1', 'txt', '0', 0, 0, 1, '网页,代码,新闻,体育,娱乐,小说,散文'),
(12, '小视频分类任务', 9, '2019-06-14 18:49:49', NULL, '标记抖音的小视频分为不同的类别，提升分类模型的准确率，为后续的推荐算法提供基础保障。', 'Video Data', 'Multi class', '2', '方法1', 'Regression', '', 'Accuracy', 'Random', '', 'set 1', 'csv', '0', 1, 1, 1, '休闲,舞蹈,娱乐'),
(13, '超市零食图片分类', 9, '2019-06-14 18:51:06', NULL, '将收集的大量超市零食图片进行标注，标注为不同的食品类别，提升分类模型的性能！', 'Img Sel Data', 'Multi class', '3', '方法1', 'Regression', '', 'Accuracy', 'Random', '', 'set 1', 'csv', '0', 0, 0, 1, '狗,狮子,狐狸,熊猫,老虎,豹子'),
(14, '视频车辆识别任务', 9, '2019-06-14 18:54:19', NULL, '对视频按帧截取的图片进行标注，将图片中的车辆用bounding box将其标出，并且标注其类别，提升车辆目标识别任务模型的性能。', 'Img Bbox Data', 'Multi class', '4', '方法1', 'Regression', '', 'Accuracy', 'Random', '', 'set 1', 'csv', '0', 0, 0, 1, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `tp_project_list`
--

DROP TABLE IF EXISTS `tp_project_list`;
CREATE TABLE IF NOT EXISTS `tp_project_list` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pId` int(10) NOT NULL,
  `pName` varchar(50) NOT NULL,
  `pImgSrc` mediumtext COMMENT '项目头像',
  `pRemark` mediumtext NOT NULL COMMENT '项目备注',
  `uId` int(10) NOT NULL,
  `uName` varchar(50) NOT NULL,
  `uImgSrc` mediumtext,
  `isCreater` int(1) NOT NULL COMMENT '是否是项目创建者(0代表不是，1代表是)',
  `uJoinTime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_project_list`
--

INSERT INTO `tp_project_list` (`id`, `pId`, `pName`, `pImgSrc`, `pRemark`, `uId`, `uName`, `uImgSrc`, `isCreater`, `uJoinTime`) VALUES
(9, 9, '新闻分类任务', NULL, '将新闻分成不同的类别，例如：娱乐，体育，生活。。。', 9, 'kid', NULL, 1, '2019-06-06 14:17:25'),
(18, 9, '新闻分类任务', NULL, '将新闻分成不同的类别，例如：娱乐，体育，生活。。。', 19, 'huang', NULL, 0, '2019-06-14 18:47:34'),
(19, 12, '小视频分类任务', NULL, '标记抖音的小视频分为不同的类别，提升分类模型的准确率，为后续的推荐算法提供基础保障。', 9, 'kid', NULL, 1, '2019-06-14 18:49:49'),
(20, 13, '超市零食图片分类', NULL, '将收集的大量超市零食图片进行标注，标注为不同的食品类别，提升分类模型的性能！', 9, 'kid', NULL, 1, '2019-06-14 18:51:06'),
(21, 14, '视频车辆识别任务', NULL, '对视频按帧截取的图片进行标注，将图片中的车辆用bounding box将其标出，并且标注其类别，提升车辆目标识别任务模型的性能。', 9, 'kid', NULL, 1, '2019-06-14 18:54:19'),
(34, 14, '视频车辆识别任务', NULL, '对视频按帧截取的图片进行标注，将图片中的车辆用bounding box将其标出，并且标注其类别，提升车辆目标识别任务模型的性能。', 10, 'typ', NULL, 0, '2019-06-16 17:14:42'),
(23, 14, '视频车辆识别任务', NULL, '对视频按帧截取的图片进行标注，将图片中的车辆用bounding box将其标出，并且标注其类别，提升车辆目标识别任务模型的性能。', 19, 'huang', NULL, 0, '2019-06-14 18:54:43'),
(38, 9, '新闻分类任务', NULL, '将新闻分成不同的类别，例如：娱乐，体育，生活。。。', 10, 'typ', NULL, 0, '2019-06-25 16:18:15'),
(25, 13, '超市零食图片分类', NULL, '将收集的大量超市零食图片进行标注，标注为不同的食品类别，提升分类模型的性能！', 19, 'huang', NULL, 0, '2019-06-14 18:55:13'),
(26, 12, '小视频分类任务', NULL, '标记抖音的小视频分为不同的类别，提升分类模型的准确率，为后续的推荐算法提供基础保障。', 19, 'huang', NULL, 0, '2019-06-14 18:55:26'),
(35, 13, '超市零食图片分类', NULL, '将收集的大量超市零食图片进行标注，标注为不同的食品类别，提升分类模型的性能！', 10, 'typ', NULL, 0, '2019-06-16 17:14:53'),
(36, 12, '小视频分类任务', NULL, '标记抖音的小视频分为不同的类别，提升分类模型的准确率，为后续的推荐算法提供基础保障。', 10, 'typ', NULL, 0, '2019-06-16 17:15:01');

-- --------------------------------------------------------

--
-- 表的结构 `tp_reg_code`
--

DROP TABLE IF EXISTS `tp_reg_code`;
CREATE TABLE IF NOT EXISTS `tp_reg_code` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `code` int(6) NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_reg_code`
--

INSERT INTO `tp_reg_code` (`id`, `email`, `code`, `time`) VALUES
(1, '474455920@qq.com', 885059, '2019-05-09 13:32:13'),
(2, '291371205@qq.com', 755347, '2019-05-09 14:15:48'),
(3, '291371205@qq.com', 639478, '2019-05-09 14:20:55'),
(4, '291371205@qq.com', 795752, '2019-05-09 14:31:20'),
(5, 'ningkp@nuaa.edu.cn', 613794, '2019-06-05 17:13:43');

-- --------------------------------------------------------

--
-- 表的结构 `tp_sign_history`
--

DROP TABLE IF EXISTS `tp_sign_history`;
CREATE TABLE IF NOT EXISTS `tp_sign_history` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `dId` int(10) NOT NULL COMMENT '数据id',
  `dName` varchar(50) NOT NULL,
  `pId` int(10) NOT NULL COMMENT '项目id',
  `uId` int(10) NOT NULL COMMENT '用户id',
  `hSignContent` mediumtext NOT NULL COMMENT '标注内容',
  `hSignTime` datetime NOT NULL COMMENT '标注时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_sign_history`
--

INSERT INTO `tp_sign_history` (`id`, `dId`, `dName`, `pId`, `uId`, `hSignContent`, `hSignTime`) VALUES
(1, 10, '埃塞俄比亚count100.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-25 20:39:50'),
(2, 12, '巴巴多斯count30.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-25 20:40:06'),
(3, 6, 'allPro代码.txt', 9, 10, '{\"anno_obj\":{\"text\":\"网页\"}}', '2019-06-25 20:40:09'),
(4, 13, '中文文档.txt', 9, 10, '{\"anno_obj\":{\"text\":\"娱乐\"}}', '2019-06-25 20:40:11'),
(5, 11, '安提瓜和巴布达count28.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-25 20:40:14'),
(6, 7, 'api文档.md', 9, 10, '{\"anno_obj\":{\"text\":\"代码\"}}', '2019-06-25 20:40:19'),
(7, 8, '阿联酋count100.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-25 20:40:21'),
(8, 9, '阿曼count75.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-25 20:40:23'),
(9, 2, '2.mp4', 12, 10, '{\"anno_obj\":{\"text\":\"舞蹈\"}}', '2019-06-25 20:40:50'),
(10, 1, '1.mp4', 12, 10, '{\"anno_obj\":{\"text\":\"休闲\"}}', '2019-06-25 20:40:58'),
(11, 3, '3.mp4', 12, 10, '{\"anno_obj\":{\"text\":\"休闲\"}}', '2019-06-25 20:41:03'),
(12, 5, '5.mp4', 12, 10, '{\"anno_obj\":{\"text\":\"体育\"}}', '2019-06-25 20:41:07'),
(13, 4, '4.mp4', 12, 10, '{\"anno_obj\":{\"text\":\"娱乐\"}}', '2019-06-25 20:41:15'),
(14, 24, 'avatar-4.jpg', 14, 19, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.37166666666666665,\"y\":0.445,\"width\":0.28833333333333333,\"height\":0.08333333333333333},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}},{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"left ear\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.08166666666666667,\"y\":0.21333333333333335,\"width\":0.26166666666666666,\"height\":0.315},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}},{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"right ear\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.6333333333333333,\"y\":0.23,\"width\":0.31,\"height\":0.3233333333333333},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:42:08'),
(15, 27, 'avatar-7.jpg', 14, 19, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.19333333333333333,\"y\":0.46,\"width\":0.595,\"height\":0.25333333333333335},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}},{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"left ear\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.14,\"y\":0.16833333333333333,\"width\":0.21166666666666667,\"height\":0.21833333333333332},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}},{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"right ear\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.6116666666666667,\"y\":0.16833333333333333,\"width\":0.24,\"height\":0.21833333333333332},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:42:26'),
(16, 23, 'avatar-3.jpg', 14, 19, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.3616666666666667,\"y\":0.51,\"width\":0.2833333333333333,\"height\":0.07166666666666667},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:42:33'),
(17, 15, 'avatar-2.jpg', 13, 19, '{\"anno_obj\":{\"text\":\"豹子\"}}', '2019-06-25 20:42:55'),
(18, 16, 'avatar-3.jpg', 13, 19, '{\"anno_obj\":{\"text\":\"狮子\"}}', '2019-06-25 20:42:57'),
(19, 18, 'avatar-5.jpg', 13, 19, '{\"anno_obj\":{\"text\":\"狐狸\"}}', '2019-06-25 20:42:59'),
(20, 25, 'avatar-5.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.29333333333333333,\"y\":0.535,\"width\":0.39666666666666667,\"height\":0.09166666666666666},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:43:18'),
(21, 21, 'avatar-1.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.41333333333333333,\"y\":0.3983333333333333,\"width\":0.16833333333333333,\"height\":0.08666666666666667},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:43:24'),
(22, 22, 'avatar-2.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.36333333333333334,\"y\":0.42333333333333334,\"width\":0.2633333333333333,\"height\":0.11333333333333333},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:43:34'),
(23, 26, 'avatar-6.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.36833333333333335,\"y\":0.47333333333333333,\"width\":0.2683333333333333,\"height\":0.1},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-25 20:43:41'),
(24, 14, 'avatar-1.jpg', 13, 10, '{\"anno_obj\":{\"text\":\"狗\"}}', '2019-06-25 20:44:28'),
(25, 20, 'avatar-7.jpg', 13, 10, '{\"anno_obj\":{\"text\":\"熊猫\"}}', '2019-06-25 20:44:30'),
(26, 17, 'avatar-4.jpg', 13, 10, '{\"anno_obj\":{\"text\":\"狗\"}}', '2019-06-25 20:44:34'),
(27, 19, 'avatar-6.jpg', 13, 10, '{\"anno_obj\":{\"text\":\"老虎\"}}', '2019-06-25 20:44:36'),
(28, 26, 'avatar-6.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"eye\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.3416666666666667,\"y\":0.425,\"width\":0.31833333333333336,\"height\":0.14166666666666666},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-26 15:31:29'),
(29, 27, 'avatar-7.jpg', 14, 10, '[{\"anno_obj\":{\"src\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/img/test_img.jpg\",\"text\":\"11\",\"shapes\":[{\"type\":\"rect\",\"geometry\":{\"x\":0.28833333333333333,\"y\":0.46,\"width\":0.4116666666666667,\"height\":0.205},\"style\":{}}],\"context\":\"file:///E:/nkp/activeLearning%E5%B7%A5%E5%85%B7%E5%8C%85/alcloud_front/annotate_img_bbox.html\"}}]', '2019-06-26 15:31:53'),
(30, 2, '2.mp4', 12, 19, '{\"anno_obj\":{\"text\":\"舞蹈\"}}', '2019-06-26 15:33:22'),
(31, 3, '3.mp4', 12, 19, '{\"anno_obj\":{\"text\":\"休闲\"}}', '2019-06-26 15:33:49'),
(32, 1, '1.mp4', 12, 19, '{\"anno_obj\":{\"text\":\"休闲\"}}', '2019-06-26 15:33:54'),
(33, 4, '4.mp4', 12, 19, '{\"anno_obj\":{\"text\":\"娱乐\"}}', '2019-06-26 15:33:58'),
(34, 5, '5.mp4', 12, 19, '{\"anno_obj\":{\"text\":\"休闲\"}}', '2019-06-26 15:34:01'),
(35, 9, '阿曼count75.txt', 9, 19, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-26 15:34:26'),
(36, 11, '安提瓜和巴布达count28.txt', 9, 19, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-06-26 15:35:02'),
(37, 12, '巴巴多斯count30.txt', 9, 10, '{\"anno_obj\":{\"text\":\"新闻\"}}', '2019-07-08 12:23:31');

-- --------------------------------------------------------

--
-- 表的结构 `tp_user`
--

DROP TABLE IF EXISTS `tp_user`;
CREATE TABLE IF NOT EXISTS `tp_user` (
  `uId` int(10) NOT NULL AUTO_INCREMENT,
  `uToken` varchar(50) NOT NULL COMMENT 'md5(uEmail)',
  `uName` varchar(50) NOT NULL,
  `uEmail` varchar(50) NOT NULL,
  `uPas` varchar(50) NOT NULL COMMENT 'md5(pas)',
  `uRegTime` datetime NOT NULL,
  `uCity` varchar(50) DEFAULT NULL COMMENT '选填',
  `uCompany` varchar(50) DEFAULT NULL COMMENT '选填',
  `uSex` int(1) DEFAULT NULL COMMENT '选填(0代表女1代表男)',
  `uEducation` varchar(50) DEFAULT NULL COMMENT '选填',
  `uWork` varchar(50) DEFAULT NULL COMMENT '选填',
  `uTitle` varchar(50) DEFAULT NULL COMMENT '选填(职称、资质)',
  `uBirth` datetime DEFAULT NULL COMMENT '选填',
  `uImgSrc` mediumtext COMMENT '选填(头像)',
  `uRemark` mediumtext COMMENT '选填(备注)',
  PRIMARY KEY (`uId`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tp_user`
--

INSERT INTO `tp_user` (`uId`, `uToken`, `uName`, `uEmail`, `uPas`, `uRegTime`, `uCity`, `uCompany`, `uSex`, `uEducation`, `uWork`, `uTitle`, `uBirth`, `uImgSrc`, `uRemark`) VALUES
(9, '7e92ef35f719edf7143d79d767455689', 'kid', '291371205@qq.com', '14e1b600b1fd579f47433b88e8d85291', '2019-05-09 14:57:11', '南京', '南京航空航天大学', 0, '本科', '学生', '学生', '2019-05-09 00:00:00', NULL, '天天向下'),
(10, '8066b8ddba4bd2538febd6a0b39b9887', 'typ', 'ningkp@nuaa.edu.cn', '14e1b600b1fd579f47433b88e8d85291', '2019-06-05 17:14:37', '南京', '南京航空航天大学', 0, '本科', '学生', '学生', '1997-08-15 00:00:00', NULL, '无'),
(19, '53a5090af1ace8ee9cd0898b895e4b53', 'huang', '474455920@qq.com', '14e1b600b1fd579f47433b88e8d85291', '2019-06-14 17:34:06', '南京', '南京航空航天大学', 0, '本科', '老师', '副教授', '0000-00-00 00:00:00', NULL, '天天向上'),
(-1, '', '系统通知', '', '', '0000-00-00 00:00:00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
