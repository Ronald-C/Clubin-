CREATE DATABASE  IF NOT EXISTS `Clubin` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Clubin`;
-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: Clubin
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Advisor`
--

DROP TABLE IF EXISTS `Advisor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Advisor` (
  `AdvisorID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(45) NOT NULL,
  `MiddleName` varchar(25) DEFAULT NULL,
  `LastName` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  PRIMARY KEY (`AdvisorID`),
  UNIQUE KEY `AdvisorID_UNIQUE` (`AdvisorID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Advisor`
--

LOCK TABLES `Advisor` WRITE;
/*!40000 ALTER TABLE `Advisor` DISABLE KEYS */;
/*!40000 ALTER TABLE `Advisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Comment`
--

DROP TABLE IF EXISTS `Comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comment` (
  `Article_fk` int(11) unsigned NOT NULL,
  `Author_fk` int(11) unsigned NOT NULL,
  `Content` varchar(200) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `fk_Comment_1_idx` (`Article_fk`),
  KEY `fk_Comment_2_idx` (`Author_fk`),
  CONSTRAINT `fk_Comment_1` FOREIGN KEY (`Article_fk`) REFERENCES `NewsfeedArticle` (`ArticleID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comment_2` FOREIGN KEY (`Author_fk`) REFERENCES `Student` (`UID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comment`
--

LOCK TABLES `Comment` WRITE;
/*!40000 ALTER TABLE `Comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Interest`
--

DROP TABLE IF EXISTS `Interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Interest` (
  `InterestID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `Title` varchar(45) NOT NULL,
  PRIMARY KEY (`InterestID`),
  UNIQUE KEY `InterestID_UNIQUE` (`InterestID`),
  UNIQUE KEY `Name_UNIQUE` (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Interest`
--

LOCK TABLES `Interest` WRITE;
/*!40000 ALTER TABLE `Interest` DISABLE KEYS */;
/*!40000 ALTER TABLE `Interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MemberOf`
--

DROP TABLE IF EXISTS `MemberOf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MemberOf` (
  `Student_fk` int(11) unsigned NOT NULL,
  `Organization_fk` int(11) unsigned NOT NULL,
  `JoinDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Active` tinyint(4) unsigned NOT NULL DEFAULT '1',
  KEY `fk_MemberOf_1_idx` (`Student_fk`),
  KEY `fk_MemberOf_2_idx` (`Organization_fk`),
  CONSTRAINT `fk_MemberOf_1` FOREIGN KEY (`Student_fk`) REFERENCES `Student` (`UID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_MemberOf_2` FOREIGN KEY (`Organization_fk`) REFERENCES `Organization` (`OrganizationID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MemberOf`
--

LOCK TABLES `MemberOf` WRITE;
/*!40000 ALTER TABLE `MemberOf` DISABLE KEYS */;
/*!40000 ALTER TABLE `MemberOf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `NewsfeedArticle`
--

DROP TABLE IF EXISTS `NewsfeedArticle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NewsfeedArticle` (
  `OrganizationID` int(11) unsigned NOT NULL,
  `ArticleID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ArticleTitle` varchar(100) NOT NULL,
  `ArticleContent` varchar(4000) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ArticleID`),
  UNIQUE KEY `ArticleID_UNIQUE` (`ArticleID`),
  KEY `fk_NewsfeedArticle_1_idx` (`OrganizationID`),
  CONSTRAINT `fk_NewsfeedArticle_1` FOREIGN KEY (`OrganizationID`) REFERENCES `Organization` (`OrganizationID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `NewsfeedArticle`
--

LOCK TABLES `NewsfeedArticle` WRITE;
/*!40000 ALTER TABLE `NewsfeedArticle` DISABLE KEYS */;
/*!40000 ALTER TABLE `NewsfeedArticle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OfficerOf`
--

DROP TABLE IF EXISTS `OfficerOf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OfficerOf` (
  `Student_fk` int(11) unsigned NOT NULL,
  `Organization_fk` int(11) unsigned NOT NULL,
  `AdminRank` varchar(45) DEFAULT NULL,
  `Active` tinyint(4) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`Student_fk`,`Organization_fk`),
  UNIQUE KEY `unique_org_admin` (`Organization_fk`,`AdminRank`),
  KEY `fk_OfficerOf_1_idx` (`Student_fk`),
  KEY `fk_OfficerOf_2_idx` (`Organization_fk`),
  CONSTRAINT `fk_OfficerOf_1` FOREIGN KEY (`Student_fk`) REFERENCES `Student` (`UID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_OfficerOf_2` FOREIGN KEY (`Organization_fk`) REFERENCES `Organization` (`OrganizationID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OfficerOf`
--

LOCK TABLES `OfficerOf` WRITE;
/*!40000 ALTER TABLE `OfficerOf` DISABLE KEYS */;
/*!40000 ALTER TABLE `OfficerOf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organization`
--

DROP TABLE IF EXISTS `Organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Organization` (
  `OrganizationID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `OrganizationName` varchar(45) NOT NULL,
  `Description` varchar(200) DEFAULT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Building` varchar(45) DEFAULT NULL,
  `RoomNumber` varchar(45) DEFAULT NULL,
  `Address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`OrganizationID`),
  UNIQUE KEY `orgName_UNIQUE` (`OrganizationName`),
  UNIQUE KEY `OrgID_UNIQUE` (`OrganizationID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organization`
--

LOCK TABLES `Organization` WRITE;
/*!40000 ALTER TABLE `Organization` DISABLE KEYS */;
/*!40000 ALTER TABLE `Organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrganizationAdvisor`
--

DROP TABLE IF EXISTS `OrganizationAdvisor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrganizationAdvisor` (
  `Organization_fk` int(11) unsigned NOT NULL,
  `Advisor_fk` int(11) unsigned NOT NULL,
  KEY `fk_OrganizationAdvisor_1_idx` (`Organization_fk`),
  KEY `fk_OrganizationAdvisor_2_idx` (`Advisor_fk`),
  CONSTRAINT `fk_OrganizationAdvisor_1` FOREIGN KEY (`Organization_fk`) REFERENCES `Organization` (`OrganizationID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrganizationAdvisor_2` FOREIGN KEY (`Advisor_fk`) REFERENCES `Advisor` (`AdvisorID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrganizationAdvisor`
--

LOCK TABLES `OrganizationAdvisor` WRITE;
/*!40000 ALTER TABLE `OrganizationAdvisor` DISABLE KEYS */;
/*!40000 ALTER TABLE `OrganizationAdvisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrganizationInterest`
--

DROP TABLE IF EXISTS `OrganizationInterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrganizationInterest` (
  `Organization_fk` int(11) unsigned NOT NULL,
  `Interest_fk` int(11) unsigned NOT NULL,
  KEY `fk_OrganizationInterest_1_idx` (`Organization_fk`),
  KEY `fk_OrganizationInterest_2_idx` (`Interest_fk`),
  CONSTRAINT `fk_OrganizationInterest_1` FOREIGN KEY (`Organization_fk`) REFERENCES `Organization` (`OrganizationID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrganizationInterest_2` FOREIGN KEY (`Interest_fk`) REFERENCES `Interest` (`InterestID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrganizationInterest`
--

LOCK TABLES `OrganizationInterest` WRITE;
/*!40000 ALTER TABLE `OrganizationInterest` DISABLE KEYS */;
/*!40000 ALTER TABLE `OrganizationInterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student`
--

DROP TABLE IF EXISTS `Student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Student` (
  `UID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `SJSUID` varchar(9) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `FirstName` varchar(45) NOT NULL,
  `MiddleName` varchar(25) DEFAULT NULL,
  `LastName` varchar(45) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `SJSUID_UNIQUE` (`SJSUID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `StudentID_UNIQUE` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student`
--

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentInterest`
--

DROP TABLE IF EXISTS `StudentInterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StudentInterest` (
  `Student_fk` int(11) unsigned NOT NULL,
  `Interest_fk` int(11) unsigned NOT NULL,
  KEY `fk_StudentInterest_1_idx` (`Student_fk`),
  KEY `fk_StudentInterest_2_idx` (`Interest_fk`),
  CONSTRAINT `fk_StudentInterest_1` FOREIGN KEY (`Student_fk`) REFERENCES `Student` (`UID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_StudentInterest_2` FOREIGN KEY (`Interest_fk`) REFERENCES `Interest` (`InterestID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentInterest`
--

LOCK TABLES `StudentInterest` WRITE;
/*!40000 ALTER TABLE `StudentInterest` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentInterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TroubleMaker`
--

DROP TABLE IF EXISTS `TroubleMaker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TroubleMaker` (
  `Student_fk` int(11) unsigned NOT NULL,
  `Officer_fk` int(11) unsigned NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `fk_TroubleMaker_1_idx` (`Student_fk`),
  KEY `fk_TroubleMaker_2_idx` (`Officer_fk`),
  CONSTRAINT `fk_TroubleMaker_2` FOREIGN KEY (`Officer_fk`) REFERENCES `OfficerOf` (`Student_fk`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_TroubleMaker_1` FOREIGN KEY (`Student_fk`) REFERENCES `Student` (`UID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TroubleMaker`
--

LOCK TABLES `TroubleMaker` WRITE;
/*!40000 ALTER TABLE `TroubleMaker` DISABLE KEYS */;
/*!40000 ALTER TABLE `TroubleMaker` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-29 18:00:18
