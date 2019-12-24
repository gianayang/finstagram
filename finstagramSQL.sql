-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 24, 2019 at 01:30 AM
-- Server version: 5.7.26
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finstagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `belongto`
--

DROP TABLE IF EXISTS `belongto`;
CREATE TABLE IF NOT EXISTS `belongto` (
  `member_username` varchar(20) NOT NULL,
  `owner_username` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  PRIMARY KEY (`member_username`,`owner_username`,`groupName`),
  KEY `owner_username` (`owner_username`,`groupName`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `belongto`
--

INSERT INTO `belongto` (`member_username`, `owner_username`, `groupName`) VALUES
('A', 'C', 'best friends');

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
  `username` varchar(200) NOT NULL,
  `photoID` varchar(200) NOT NULL,
  `comment` varchar(200) NOT NULL,
  PRIMARY KEY (`username`,`photoID`,`comment`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`username`, `photoID`, `comment`) VALUES
('A', '3', 'cute!'),
('A', '8', 'cute!');

-- --------------------------------------------------------

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
CREATE TABLE IF NOT EXISTS `follow` (
  `username_followed` varchar(20) NOT NULL,
  `username_follower` varchar(20) NOT NULL,
  `followstatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`username_followed`,`username_follower`),
  KEY `username_follower` (`username_follower`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `follow`
--

INSERT INTO `follow` (`username_followed`, `username_follower`, `followstatus`) VALUES
('A', 'B', 1),
('A', 'C', 0),
('A', 'D', 0),
('A', 'E', 1),
('B', 'A', 1),
('B', 'D', 1),
('B', 'E', 1),
('C', 'D', 1),
('E', 'A', 1);

-- --------------------------------------------------------

--
-- Table structure for table `friendgroup`
--

DROP TABLE IF EXISTS `friendgroup`;
CREATE TABLE IF NOT EXISTS `friendgroup` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`groupOwner`,`groupName`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `friendgroup`
--

INSERT INTO `friendgroup` (`groupOwner`, `groupName`, `description`) VALUES
('C', 'best friends', 'Cathy\'s best friends'),
('D', 'best friends', 'Dave\'s best friends');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
CREATE TABLE IF NOT EXISTS `likes` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `liketime` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  PRIMARY KEY (`username`,`photoID`),
  KEY `photoID` (`photoID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`username`, `photoID`, `liketime`, `rating`) VALUES
('D', 1, '2019-12-11 00:00:00', 5),
('D', 2, '2019-12-11 00:00:00', 5),
('E', 1, '2019-12-11 00:00:00', 3),
('A', 1, NULL, 1),
('A', 2, NULL, 1),
('A', 7, NULL, 10);

-- --------------------------------------------------------

--
-- Table structure for table `photo`
--

DROP TABLE IF EXISTS `photo`;
CREATE TABLE IF NOT EXISTS `photo` (
  `photoID` int(11) NOT NULL AUTO_INCREMENT,
  `postingdate` datetime DEFAULT CURRENT_TIMESTAMP,
  `filepath` varchar(100) DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL,
  `caption` varchar(100) DEFAULT NULL,
  `photoPoster` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`photoID`),
  KEY `photoPoster` (`photoPoster`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `photo`
--

INSERT INTO `photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES
(1, '2019-12-10 00:00:00', 'photo1B.jpg', 1, 'photo 1', 'B'),
(2, '2019-12-11 00:00:00', 'photo2C.jpg', 1, 'photo 2', 'C'),
(3, '2019-12-12 00:00:00', 'photo3D.jpg', 1, 'photo 3', 'D'),
(4, '2019-12-13 00:00:00', 'photo4D.jpg', 1, NULL, 'D'),
(5, '2019-12-14 00:00:00', 'photo5E.jpg', 0, 'photo 5', 'E'),
(7, NULL, 'Kung-Fu-Panda-270x400.jpg', 1, NULL, 'A'),
(8, '2019-12-13 13:26:04', 'panda01.jpg', 1, NULL, 'A');

-- --------------------------------------------------------

--
-- Table structure for table `sharedwith`
--

DROP TABLE IF EXISTS `sharedwith`;
CREATE TABLE IF NOT EXISTS `sharedwith` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  PRIMARY KEY (`groupOwner`,`groupName`,`photoID`),
  KEY `photoID` (`photoID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sharedwith`
--

INSERT INTO `sharedwith` (`groupOwner`, `groupName`, `photoID`) VALUES
('C', 'best friends', 2),
('D', 'best friends', 3);

-- --------------------------------------------------------

--
-- Table structure for table `tagged`
--

DROP TABLE IF EXISTS `tagged`;
CREATE TABLE IF NOT EXISTS `tagged` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `tagstatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`username`,`photoID`),
  KEY `photoID` (`photoID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tagged`
--

INSERT INTO `tagged` (`username`, `photoID`, `tagstatus`) VALUES
('A', 1, 0),
('D', 1, 1),
('D', 2, 1),
('E', 1, 1),
('B', 7, 0),
('A', 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `bio` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `firstName`, `lastName`, `bio`) VALUES
('A', 'A', 'Ann', 'Andrews', 'Ann is awesome'),
('B', 'B', 'Bill', 'Barker', 'Bill is a big shot'),
('C', 'C', 'Cathy', 'Chen', 'Cathy is charismatic'),
('D', 'D', 'Dave', 'Davis', 'Dave is diligent'),
('E', 'E', 'Emily', 'Elhaj', 'Emily is energetic');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
