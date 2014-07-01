-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: probe_db
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.12.04.1

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
-- Table structure for table `Nocout_Health_Service`
--

DROP TABLE IF EXISTS `Nocout_Health_Service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Nocout_Health_Service` (
  `Probe_Name` varchar(45) DEFAULT NULL,
  `CPU_Usage` decimal(10,6) DEFAULT NULL,
  `Latency` decimal(10,6) DEFAULT NULL,
  `Timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nocout_Health_Service`
--

LOCK TABLES `Nocout_Health_Service` WRITE;
/*!40000 ALTER TABLE `Nocout_Health_Service` DISABLE KEYS */;
/*!40000 ALTER TABLE `Nocout_Health_Service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Nocout_Probe_Service_Conf`
--

DROP TABLE IF EXISTS `Nocout_Probe_Service_Conf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Nocout_Probe_Service_Conf` (
  `service_id` int(11) NOT NULL DEFAULT '0',
  `check_name` varchar(128) DEFAULT NULL,
  `check_parameter` varchar(45) DEFAULT NULL,
  `ip_host_address` varchar(1024) DEFAULT NULL,
  `warning` decimal(10,6) DEFAULT NULL,
  `critical` decimal(10,6) DEFAULT NULL,
  `timeout` int(11) DEFAULT NULL,
  `max_attempt` int(11) DEFAULT NULL,
  `check_interval` int(11) DEFAULT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nocout_Probe_Service_Conf`
--

LOCK TABLES `Nocout_Probe_Service_Conf` WRITE;
/*!40000 ALTER TABLE `Nocout_Probe_Service_Conf` DISABLE KEYS */;
/*!40000 ALTER TABLE `Nocout_Probe_Service_Conf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Nocout_performance_services`
--

DROP TABLE IF EXISTS `Nocout_performance_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Nocout_performance_services` (
  `Service_id` int(11) DEFAULT NULL,
  `SVC_Name` varchar(45) DEFAULT NULL,
  `SVC_Param` varchar(45) DEFAULT NULL,
  `Timestamp` datetime DEFAULT NULL,
  `Value` decimal(10,6) DEFAULT NULL,
  `Probe_Name` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nocout_performance_services`
--

LOCK TABLES `Nocout_performance_services` WRITE;
/*!40000 ALTER TABLE `Nocout_performance_services` DISABLE KEYS */;
/*!40000 ALTER TABLE `Nocout_performance_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perf_data`
--

DROP TABLE IF EXISTS `perf_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perf_data` (
  `service_id` int(11) DEFAULT NULL,
  `current_check_attempt` int(11) DEFAULT NULL,
  `max_check_attempt` int(11) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `timeout` int(11) DEFAULT NULL,
  `execution_time` decimal(10,6) DEFAULT NULL,
  `return_code` int(11) DEFAULT NULL,
  `output` varchar(1023) DEFAULT NULL,
  `perfdata` varchar(1023) CHARACTER SET big5 DEFAULT NULL,
  `check_name` varchar(45) DEFAULT NULL,
  `check_param` varchar(45) DEFAULT NULL,
  `target_ip` varchar(45) DEFAULT NULL,
  `probe_name` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perf_data`
--

LOCK TABLES `perf_data` WRITE;
/*!40000 ALTER TABLE `perf_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `perf_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `probe_lock`
--

DROP TABLE IF EXISTS `probe_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `probe_lock` (
  `name` varchar(50) NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `probe_lock`
--

LOCK TABLES `probe_lock` WRITE;
/*!40000 ALTER TABLE `probe_lock` DISABLE KEYS */;
INSERT INTO `probe_lock` VALUES ('conf_update','0'),('Probe_id','0');
/*!40000 ALTER TABLE `probe_lock` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-01  0:51:29
