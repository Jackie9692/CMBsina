/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : cmb_sina

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2017-05-05 22:48:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` bigint(11) NOT NULL,
  `user_id` bigint(11) DEFAULT NULL,
  `status_id` bigint(11) DEFAULT NULL,
  `text` text,
  `create_date` datetime DEFAULT NULL,
  `emotion` varchar(255) DEFAULT NULL,
  `collect_date` datetime DEFAULT NULL,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for status
-- ----------------------------
DROP TABLE IF EXISTS `status`;
CREATE TABLE `status` (
  `status_id` bigint(20) NOT NULL,
  `text` text,
  `create_date` datetime DEFAULT NULL,
  `userurl` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `repost_count` int(255) DEFAULT NULL,
  `comments_count` int(11) DEFAULT NULL,
  `attitude_count` int(255) DEFAULT NULL,
  `statusurl` varchar(255) DEFAULT NULL,
  `geo` varchar(255) DEFAULT NULL,
  `pic_urls` varchar(255) DEFAULT NULL,
  `collect_by_keywords` varchar(255) DEFAULT NULL,
  `collect_date` datetime DEFAULT NULL,
  `jieba_text` text,
  `user_id` bigint(11) DEFAULT NULL,
  `emotion` varchar(20) DEFAULT NULL,
  `isValidated` int(2) DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` bigint(11) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `friends_count` int(255) DEFAULT NULL,
  `followers_count` int(255) DEFAULT NULL,
  `statuses_count` int(255) DEFAULT NULL,
  `collect_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
