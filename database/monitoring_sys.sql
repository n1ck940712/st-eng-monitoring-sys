-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 03, 2022 at 03:18 PM
-- Server version: 10.3.31-MariaDB-0+deb10u1
-- PHP Version: 7.3.29-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `monitoring_sys`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_logdata`
--

CREATE TABLE `app_logdata` (
  `id` int(11) NOT NULL,
  `batch` int(11) NOT NULL,
  `type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `flow` decimal(10,3) DEFAULT NULL,
  `flow_unit` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pressure` decimal(10,3) DEFAULT NULL,
  `pressure_unit` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `temperature` decimal(10,3) DEFAULT NULL,
  `temperature_unit` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `heater_set` decimal(10,3) DEFAULT NULL,
  `heater_set_unit` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_logdata`
--

INSERT INTO `app_logdata` (`id`, `batch`, `type`, `flow`, `flow_unit`, `pressure`, `pressure_unit`, `temperature`, `temperature_unit`, `heater_set`, `heater_set_unit`, `timestamp`) VALUES
(1, 1, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 02:41:06'),
(2, 1, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 02:41:11'),
(3, 2, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 02:48:08'),
(4, 3, 'production part 1', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '80.000', '°C', '2022-02-18 02:53:17'),
(5, 4, 'production part 1', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '80.000', '°C', '2022-02-18 02:54:32'),
(6, 4, 'production part 1', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '80.000', '°C', '2022-02-18 02:54:38'),
(7, 4, 'production part 2', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '65.000', '°C', '2022-02-18 02:55:03'),
(8, 4, 'production part 2', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '65.000', '°C', '2022-02-18 02:55:32'),
(9, 4, 'production part 3', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '60.000', '°C', '2022-02-18 02:55:57'),
(10, 4, 'production part 3', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '60.000', '°C', '2022-02-18 02:56:27'),
(11, 4, 'production part 3', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', '60.000', '°C', '2022-02-18 02:56:57'),
(12, 5, 'post production day 1', '0.000', 'L/min', '98.387', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:00:08'),
(13, 5, 'post production day 1', '0.000', 'L/min', '98.392', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:00:38'),
(14, 5, 'post production day 1', '0.000', 'L/min', '98.383', 'kPa', '28.934', '°C', NULL, NULL, '2022-02-18 03:01:07'),
(15, 5, 'post production day 2', '0.000', 'L/min', '98.383', 'kPa', '28.934', '°C', NULL, NULL, '2022-02-18 03:01:29'),
(16, 5, 'post production day 2', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:02:00'),
(17, 5, 'post production day 2', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:02:29'),
(18, 5, 'post production day 3', '0.000', 'L/min', '98.383', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:02:50'),
(19, 5, 'post production day 3', '0.000', 'L/min', '98.383', 'kPa', '28.934', '°C', NULL, NULL, '2022-02-18 03:03:21'),
(20, 5, 'post production day 3', '0.000', 'L/min', '98.379', 'kPa', '28.900', '°C', NULL, NULL, '2022-02-18 03:03:50'),
(21, 6, 'pre production', '19.496', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:09:05'),
(22, 7, 'pre production', '54.536', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:10:32'),
(23, 8, 'pre production', '48.582', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:12:20'),
(24, 9, 'pre production', '81.022', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:14:37'),
(25, 10, 'pre production', '150.810', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:16:06'),
(26, 11, 'pre production', '160.039', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:17:21'),
(27, 12, 'pre production', '19.761', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:18:12'),
(28, 13, 'pre production', '19.281', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 03:20:54'),
(29, 14, 'pre production', '20.596', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 06:27:38'),
(30, 15, 'production part 1', '46.825', 'L/min', '98.204', 'kPa', '29.209', '°C', '80.000', '°C', '2022-02-18 06:34:17'),
(31, 15, 'production part 1', '45.772', 'L/min', '98.204', 'kPa', '29.175', '°C', '80.000', '°C', '2022-02-18 06:34:25'),
(32, 15, 'production part 2', '49.072', 'L/min', '98.221', 'kPa', '29.209', '°C', '65.000', '°C', '2022-02-18 06:34:54'),
(33, 15, 'production part 2', '48.479', 'L/min', '98.546', 'kPa', '29.209', '°C', '65.000', '°C', '2022-02-18 06:35:17'),
(34, 15, 'production part 3', '49.858', 'L/min', '99.008', 'kPa', '29.158', '°C', '60.000', '°C', '2022-02-18 06:36:50'),
(35, 15, 'production part 3', '49.924', 'L/min', '99.113', 'kPa', '29.158', '°C', '60.000', '°C', '2022-02-18 06:37:21'),
(36, 15, 'production part 3', '49.899', 'L/min', '99.183', 'kPa', '29.141', '°C', '60.000', '°C', '2022-02-18 06:37:50'),
(37, 16, 'pre production', '19.955', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 06:39:20'),
(38, 17, 'production part 1', '56.769', 'L/min', '98.188', 'kPa', '29.141', '°C', '80.000', '°C', '2022-02-18 06:42:05'),
(39, 17, 'production part 1', '48.595', 'L/min', '98.625', 'kPa', '29.141', '°C', '80.000', '°C', '2022-02-18 06:42:11'),
(40, 17, 'production part 2', '50.850', 'L/min', '99.154', 'kPa', '29.141', '°C', '65.000', '°C', '2022-02-18 06:42:45'),
(41, 17, 'production part 2', '49.104', 'L/min', '99.192', 'kPa', '29.141', '°C', '65.000', '°C', '2022-02-18 06:42:46'),
(42, 17, 'production part 3', '150.986', 'L/min', '100.000', 'kPa', '29.141', '°C', '60.000', '°C', '2022-02-18 06:43:55'),
(43, 18, 'pre production', '151.836', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 06:53:07'),
(44, 19, 'pre production', '149.138', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:00:42'),
(45, 20, 'pre production', '148.652', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:06:56'),
(46, 21, 'pre production', '148.810', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:08:56'),
(47, 22, 'pre production', '22.467', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:10:52'),
(48, 23, 'production part 1', '48.661', 'L/min', '98.704', 'kPa', '29.175', '°C', '80.000', '°C', '2022-02-18 07:17:49'),
(49, 23, 'production part 1', '49.081', 'L/min', '98.971', 'kPa', '29.175', '°C', '80.000', '°C', '2022-02-18 07:17:55'),
(50, 23, 'production part 2', '50.764', 'L/min', '99.358', 'kPa', '29.175', '°C', '65.000', '°C', '2022-02-18 07:18:14'),
(51, 24, 'pre production', '149.882', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:33:11'),
(52, 25, 'pre production', '158.075', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:35:08'),
(53, 26, 'pre production', '49.764', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 07:40:31'),
(54, 27, 'pre production', '8.064', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 08:19:55'),
(55, 28, 'pre production', '49.900', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 08:21:38'),
(56, 28, 'pre production', '50.300', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 08:22:37'),
(57, 29, 'pre production', '20.045', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 08:30:56'),
(58, 29, 'pre production', '20.228', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-18 08:35:56'),
(59, 30, 'production part 1', '50.071', 'L/min', '1.808', 'kPa', '29.296', '°C', '80.000', '°C', '2022-02-21 00:01:24'),
(60, 30, 'production part 1', '50.189', 'L/min', '1.833', 'kPa', '48.432', '°C', '80.000', '°C', '2022-02-21 00:31:25'),
(61, 30, 'production part 1', '51.553', 'L/min', '1.850', 'kPa', '61.419', '°C', '80.000', '°C', '2022-02-21 01:01:26'),
(62, 30, 'production part 1', '48.787', 'L/min', '1.850', 'kPa', '63.453', '°C', '80.000', '°C', '2022-02-21 01:08:13'),
(63, 30, 'production part 2', '48.551', 'L/min', '1.867', 'kPa', '64.200', '°C', '67.500', '°C', '2022-02-21 01:11:09'),
(64, 31, 'production part 1', '51.077', 'L/min', '1.483', 'kPa', '64.496', '°C', '80.000', '°C', '2022-02-21 01:22:22'),
(65, 31, 'production part 1', '51.385', 'L/min', '1.538', 'kPa', '64.496', '°C', '80.000', '°C', '2022-02-21 01:22:26'),
(66, 32, 'production part 1', '51.311', 'L/min', '1.104', 'kPa', '64.461', '°C', '80.000', '°C', '2022-02-21 01:24:23'),
(67, 32, 'production part 1', '51.050', 'L/min', '1.283', 'kPa', '64.461', '°C', '80.000', '°C', '2022-02-21 01:24:28'),
(68, 32, 'production part 2', '51.248', 'L/min', '1.638', 'kPa', '64.426', '°C', '67.500', '°C', '2022-02-21 01:24:55'),
(69, 33, 'production part 1', '44.579', 'L/min', '0.642', 'kPa', '64.409', '°C', '80.000', '°C', '2022-02-21 01:25:50'),
(70, 33, 'production part 1', '46.204', 'L/min', '0.875', 'kPa', '64.461', '°C', '80.000', '°C', '2022-02-21 01:25:55'),
(71, 33, 'production part 2', '44.764', 'L/min', '1.342', 'kPa', '64.461', '°C', '67.500', '°C', '2022-02-21 01:26:09'),
(72, 34, 'production part 1', '45.172', 'L/min', '0.800', 'kPa', '64.531', '°C', '80.000', '°C', '2022-02-21 01:28:09'),
(73, 34, 'production part 1', '44.459', 'L/min', '0.983', 'kPa', '64.531', '°C', '80.000', '°C', '2022-02-21 01:28:14'),
(74, 34, 'production part 2', '44.949', 'L/min', '1.333', 'kPa', '64.531', '°C', '67.500', '°C', '2022-02-21 01:28:28'),
(75, 35, 'production part 1', '46.375', 'L/min', '0.679', 'kPa', '64.583', '°C', '80.000', '°C', '2022-02-21 01:29:36'),
(76, 35, 'production part 1', '45.007', 'L/min', '1.033', 'kPa', '64.600', '°C', '80.000', '°C', '2022-02-21 01:29:43'),
(77, 35, 'production part 2', '44.186', 'L/min', '1.542', 'kPa', '64.635', '°C', '67.500', '°C', '2022-02-21 01:30:32'),
(78, 36, 'production part 1', '18.418', 'L/min', '0.417', 'kPa', '64.670', '°C', '80.000', '°C', '2022-02-21 01:31:26'),
(79, 36, 'production part 1', '48.894', 'L/min', '0.617', 'kPa', '64.687', '°C', '80.000', '°C', '2022-02-21 01:31:31'),
(80, 36, 'production part 2', '51.068', 'L/min', '1.417', 'kPa', '64.687', '°C', '67.500', '°C', '2022-02-21 01:31:49'),
(81, 36, 'production part 2', '51.297', 'L/min', '1.717', 'kPa', '65.557', '°C', '67.500', '°C', '2022-02-21 02:01:49'),
(82, 36, 'production part 2', '50.728', 'L/min', '1.712', 'kPa', '65.922', '°C', '67.500', '°C', '2022-02-21 02:31:51'),
(83, 36, 'production part 2', '48.694', 'L/min', '1.708', 'kPa', '66.200', '°C', '67.500', '°C', '2022-02-21 03:01:53'),
(84, 36, 'production part 2', '50.815', 'L/min', '1.708', 'kPa', '66.357', '°C', '67.500', '°C', '2022-02-21 03:31:54'),
(85, 36, 'production part 2', '51.315', 'L/min', '1.704', 'kPa', '66.479', '°C', '67.500', '°C', '2022-02-21 04:01:26'),
(86, 36, 'production part 3', '150.100', 'L/min', '6.179', 'kPa', '66.427', '°C', '67.500', '°C', '2022-02-21 04:12:37'),
(87, 36, 'production part 3', '150.062', 'L/min', '5.883', 'kPa', '66.392', '°C', '67.500', '°C', '2022-02-21 05:12:38'),
(88, 36, 'production part 3', '149.996', 'L/min', '5.883', 'kPa', '66.357', '°C', '67.500', '°C', '2022-02-21 06:12:40'),
(89, 36, 'production part 3', '150.032', 'L/min', '5.887', 'kPa', '66.392', '°C', '67.500', '°C', '2022-02-21 07:12:42'),
(90, 36, 'production part 3', '149.983', 'L/min', '5.900', 'kPa', '66.409', '°C', '67.500', '°C', '2022-02-21 08:12:37'),
(91, 37, 'production part 1', '0.000', 'L/min', '98.646', 'kPa', '48.207', '°C', '80.000', '°C', '2022-02-22 00:51:01'),
(92, 37, 'production part 1', '0.000', 'L/min', '98.642', 'kPa', '48.190', '°C', '80.000', '°C', '2022-02-22 00:51:06'),
(93, 37, 'production part 2', '0.000', 'L/min', '98.646', 'kPa', '48.173', '°C', '67.500', '°C', '2022-02-22 00:51:22'),
(94, 38, 'production part 1', '50.020', 'L/min', '6.671', 'kPa', '47.775', '°C', '80.000', '°C', '2022-02-22 01:41:23'),
(95, 39, 'production part 1', '49.781', 'L/min', '1.525', 'kPa', '50.683', '°C', '80.000', '°C', '2022-02-22 01:43:06'),
(96, 39, 'production part 1', '49.827', 'L/min', '1.538', 'kPa', '50.752', '°C', '80.000', '°C', '2022-02-22 01:43:10'),
(97, 39, 'production part 1', '49.827', 'L/min', '1.538', 'kPa', '50.752', '°C', '80.000', '°C', '2022-02-22 01:43:10'),
(98, 39, 'production part 2', '49.741', 'L/min', '1.575', 'kPa', '51.029', '°C', '67.500', '°C', '2022-02-22 01:43:40'),
(99, 39, 'production part 2', '49.741', 'L/min', '1.575', 'kPa', '51.029', '°C', '67.500', '°C', '2022-02-22 01:43:40'),
(100, 39, 'production part 2', '50.001', 'L/min', '1.592', 'kPa', '51.358', '°C', '67.500', '°C', '2022-02-22 01:44:41'),
(101, 39, 'production part 2', '50.001', 'L/min', '1.592', 'kPa', '51.358', '°C', '67.500', '°C', '2022-02-22 01:44:40'),
(102, 40, 'production part 1', '50.714', 'L/min', '1.513', 'kPa', '51.653', '°C', '80.000', '°C', '2022-02-22 01:47:43'),
(103, 40, 'production part 1', '49.288', 'L/min', '1.521', 'kPa', '51.653', '°C', '80.000', '°C', '2022-02-22 01:47:49'),
(104, 40, 'production part 2', '50.803', 'L/min', '1.546', 'kPa', '51.722', '°C', '67.500', '°C', '2022-02-22 01:48:56'),
(105, 40, 'production part 2', '49.599', 'L/min', '1.550', 'kPa', '51.757', '°C', '67.500', '°C', '2022-02-22 01:49:57'),
(106, 40, 'production part 2', '49.556', 'L/min', '1.558', 'kPa', '51.722', '°C', '67.500', '°C', '2022-02-22 01:50:58'),
(107, 40, 'production part 2', '49.305', 'L/min', '1.571', 'kPa', '51.705', '°C', '67.500', '°C', '2022-02-22 01:52:00'),
(108, 40, 'production part 2', '50.425', 'L/min', '1.575', 'kPa', '51.722', '°C', '67.500', '°C', '2022-02-22 01:53:01'),
(109, 41, 'production part 1', '50.730', 'L/min', '1.575', 'kPa', '52.120', '°C', '80.000', '°C', '2022-02-22 01:55:10'),
(110, 41, 'production part 1', '50.577', 'L/min', '1.683', 'kPa', '63.435', '°C', '80.000', '°C', '2022-02-22 02:23:25'),
(111, 41, 'production part 2', '50.371', 'L/min', '1.683', 'kPa', '63.644', '°C', '67.500', '°C', '2022-02-22 02:24:09'),
(112, 41, 'production part 2', '49.773', 'L/min', '1.688', 'kPa', '63.661', '°C', '67.500', '°C', '2022-02-22 02:24:10'),
(113, 41, 'production part 3', '150.037', 'L/min', '5.971', 'kPa', '64.426', '°C', '67.500', '°C', '2022-02-22 02:30:39'),
(114, 42, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-22 02:43:08'),
(115, 43, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-22 04:41:10'),
(116, 44, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-22 04:41:38'),
(117, 44, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-22 04:41:44'),
(118, 45, 'production part 1', '0.000', 'L/min', '98.525', 'kPa', '62.862', '°C', '80.000', '°C', '2022-02-22 04:42:29'),
(119, 46, 'production part 1', '0.000', 'L/min', '98.521', 'kPa', '62.844', '°C', '80.000', '°C', '2022-02-22 04:43:08'),
(120, 46, 'production part 1', '0.000', 'L/min', '98.521', 'kPa', '62.844', '°C', '80.000', '°C', '2022-02-22 04:43:22'),
(121, 46, 'production part 2', '0.000', 'L/min', '98.521', 'kPa', '62.809', '°C', '67.500', '°C', '2022-02-22 04:44:16'),
(122, 46, 'production part 2', '0.000', 'L/min', '98.517', 'kPa', '62.809', '°C', '67.500', '°C', '2022-02-22 04:44:18'),
(123, 46, 'production part 3', '0.000', 'L/min', '98.517', 'kPa', '62.792', '°C', '67.500', '°C', '2022-02-22 04:45:04'),
(124, 46, 'production part 3', '0.000', 'L/min', '98.512', 'kPa', '62.792', '°C', '67.500', '°C', '2022-02-22 04:45:34'),
(125, 47, 'post production day 1', '0.000', 'L/min', '98.125', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:48:37'),
(126, 47, 'post production day 1', '0.000', 'L/min', '98.125', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:48:44'),
(127, 47, 'post production day 1', '0.000', 'L/min', '98.125', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:48:49'),
(128, 47, 'post production day 2', '0.000', 'L/min', '98.125', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:49:39'),
(129, 47, 'post production day 2', '0.000', 'L/min', '98.121', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:49:45'),
(130, 47, 'post production day 2', '0.000', 'L/min', '98.121', 'kPa', '32.205', '°C', NULL, NULL, '2022-02-25 07:49:50'),
(131, 47, 'post production day 3', '0.000', 'L/min', '98.121', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:50:45'),
(132, 47, 'post production day 3', '0.000', 'L/min', '98.121', 'kPa', '32.222', '°C', NULL, NULL, '2022-02-25 07:50:51'),
(133, 47, 'post production day 3', '0.000', 'L/min', '98.121', 'kPa', '32.205', '°C', NULL, NULL, '2022-02-25 07:50:56'),
(134, 48, 'production part 1', '0.000', 'L/min', '98.121', 'kPa', '32.205', '°C', '80.000', '°C', '2022-02-25 08:05:25'),
(135, 49, 'production part 1', '0.000', 'L/min', '98.113', 'kPa', '32.205', '°C', '80.000', '°C', '2022-02-25 08:07:40'),
(136, 50, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-28 00:55:04'),
(137, 51, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-28 00:55:52'),
(138, 51, 'pre production', '0.000', 'L/min', NULL, NULL, NULL, NULL, NULL, NULL, '2022-02-28 00:56:22'),
(139, 52, 'production part 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', '80.000', '°C', '2022-02-28 01:00:02'),
(140, 52, 'production part 1', '0.000', 'L/min', '98.592', 'kPa', '28.883', '°C', '80.000', '°C', '2022-02-28 01:00:07'),
(141, 52, 'production part 2', '0.000', 'L/min', '98.592', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:00:31'),
(142, 52, 'production part 2', '0.000', 'L/min', '98.592', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:01:01'),
(143, 52, 'production part 2', '0.000', 'L/min', '98.592', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:01:33'),
(144, 52, 'production part 2', '0.000', 'L/min', '98.592', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:02:02'),
(145, 52, 'production part 3', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:02:25'),
(146, 52, 'production part 3', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:02:56'),
(147, 52, 'production part 3', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:03:25'),
(148, 53, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:04:32'),
(149, 53, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:04:44'),
(150, 53, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:04:58'),
(151, 53, 'post production day 1', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:05:11'),
(152, 53, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:05:24'),
(153, 53, 'post production day 1', '0.000', 'L/min', '98.567', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:05:32'),
(154, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:05:52'),
(155, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:05:59'),
(156, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:06'),
(157, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:13'),
(158, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:20'),
(159, 53, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:21'),
(160, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:42'),
(161, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:06:49'),
(162, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.865', '°C', NULL, NULL, '2022-02-28 01:06:56'),
(163, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:07:03'),
(164, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:07:10'),
(165, 53, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:07:12'),
(166, 54, 'post production day 1', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:08:46'),
(167, 54, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:08:53'),
(168, 54, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:09:00'),
(169, 54, 'post production day 1', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:09:04'),
(170, 54, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:10:39'),
(171, 54, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:10:45'),
(172, 54, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:10:52'),
(173, 54, 'post production day 2', '0.000', 'L/min', '98.600', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:10:56'),
(174, 54, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:12:29'),
(175, 54, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:12:36'),
(176, 54, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:12:43'),
(177, 54, 'post production day 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', NULL, NULL, '2022-02-28 01:12:47'),
(178, 55, 'production part 1', '0.000', 'L/min', '98.604', 'kPa', '28.865', '°C', '80.000', '°C', '2022-02-28 01:13:38'),
(179, 55, 'production part 1', '0.000', 'L/min', '98.604', 'kPa', '28.865', '°C', '80.000', '°C', '2022-02-28 01:13:43'),
(180, 55, 'production part 2', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:14:10'),
(181, 55, 'production part 2', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:14:22'),
(182, 55, 'production part 2', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:14:36'),
(183, 55, 'production part 2', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:14:38'),
(184, 55, 'production part 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:15:06'),
(185, 55, 'production part 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:15:19'),
(186, 55, 'production part 3', '0.000', 'L/min', '98.571', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:15:33'),
(187, 55, 'production part 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:15:46'),
(188, 55, 'production part 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:15:59'),
(189, 55, 'production part 3', '0.000', 'L/min', '98.604', 'kPa', '28.883', '°C', '67.500', '°C', '2022-02-28 01:16:06'),
(190, 56, 'post production day 1', '0.000', 'L/min', '98.717', 'kPa', '28.848', '°C', NULL, NULL, '2022-03-01 02:15:58'),
(191, 56, 'post production day 1', '0.000', 'L/min', '98.713', 'kPa', '28.883', '°C', NULL, NULL, '2022-03-01 02:16:04'),
(192, 56, 'post production day 1', '0.000', 'L/min', '98.713', 'kPa', '28.848', '°C', NULL, NULL, '2022-03-01 02:16:09');

-- --------------------------------------------------------

--
-- Table structure for table `app_logdatatype`
--

CREATE TABLE `app_logdatatype` (
  `id` int(11) NOT NULL,
  `type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `unit` varchar(10) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_logdatatype`
--

INSERT INTO `app_logdatatype` (`id`, `type`, `unit`) VALUES
(1, 'n2 flow rate', 'L/min'),
(2, 'temperature', '°C'),
(3, 'pressure', 'bar');

-- --------------------------------------------------------

--
-- Table structure for table `app_processlayout`
--

CREATE TABLE `app_processlayout` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `category` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `layout` longtext COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_processlayout`
--

INSERT INTO `app_processlayout` (`id`, `name`, `category`, `layout`) VALUES
(1, 'idle', 'idle', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"idle\",\"widget_name\":\"\"}]'),
(2, 'pre production', 'pre production', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"pre production\",\"widget_name\":\"\"}]'),
(3, 'production part 1', 'production part 1', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"production_part_1\",\"widget_name\":\"\"}]'),
(4, 'production part 2', 'production part 2', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"production_part_2\",\"widget_name\":\"\"}]'),
(5, 'production part 3', 'production part 3', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"production_part_3\",\"widget_name\":\"\"}]'),
(6, 'post production day 1', 'post production day 1', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"post_production_day_1\",\"widget_name\":\"\"}]'),
(7, 'post production day 2', 'post production day 2', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"post_production_day_2\",\"widget_name\":\"\"}]'),
(8, 'post production day 3', 'post production day 3', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"post_production_day_3\",\"widget_name\":\"\"}]'),
(9, 'post production wait day 2', 'post production wait day 2', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"post_production_wait_day_2\",\"widget_name\":\"\"}]'),
(10, 'post production wait day 3', 'post production wait day 3', '[{\"gs_x\":\"0\",\"gs_y\":\"0\",\"gs_w\":\"64\",\"gs_h\":\"64\",\"widget_id\":\"1\",\"widget_type\":\"post_production_wait_day_3\",\"widget_name\":\"\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `app_processlist`
--

CREATE TABLE `app_processlist` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `last_complete` timestamp NULL DEFAULT NULL,
  `category` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `order` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_processlist`
--

INSERT INTO `app_processlist` (`id`, `name`, `status`, `last_complete`, `category`, `order`) VALUES
(1, 'logging', 'not active', '2021-09-30 16:00:00', 'pre production', 2),
(8, 'data input', 'not active', '2021-09-30 16:00:00', 'pre production', 1),
(9, 'waiting to log', 'not active', '2021-09-30 16:00:00', 'pre production', 1),
(10, 'waiting to log', 'not active', '2021-09-30 16:00:00', 'production_part_1', 1),
(11, 'data input', 'not active', '2021-09-30 16:00:00', 'production_part_1', 1),
(12, 'logging', 'not active', '2021-09-30 16:00:00', 'production_part_1', 1),
(13, 'data input', 'not active', '2021-09-30 16:00:00', 'production_part_2', 1),
(14, 'waiting to log', 'not active', '2021-09-30 16:00:00', 'production_part_2', 1),
(15, 'logging', 'not active', '2021-09-30 16:00:00', 'production_part_2', 1),
(16, 'data input', 'not active', '2021-09-30 16:00:00', 'production_part_3', 1),
(17, 'waiting to log', 'not active', '2021-09-30 16:00:00', 'production_part_3', 1),
(19, 'logging', 'not active', '2021-09-30 16:00:00', 'production_part_3', 1),
(20, 'waiting to release vacuum', 'not active', '2021-09-30 16:00:00', 'production_part_3', 1),
(21, 'data input', 'not active', '2021-09-30 16:00:00', 'post_production_day_1', 1),
(22, 'logging', 'not active', '2021-09-30 16:00:00', 'post_production_day_1', 1),
(23, 'data input', 'not active', '2021-09-30 16:00:00', 'post_production_day_2', 1),
(24, 'logging', 'not active', '2021-09-30 16:00:00', 'post_production_day_2', 1),
(25, 'data input', 'not active', '2021-09-30 16:00:00', 'post_production_day_3', 1),
(26, 'logging', 'not active', '2021-09-30 16:00:00', 'post_production_day_3', 1),
(27, 'waiting to start day 2', 'not active', '2021-09-30 16:00:00', 'post_production_wait_day_2', 1),
(28, 'waiting to start day 3', 'not active', '2021-09-30 16:00:00', 'post_production_wait_day_3', 1),
(29, 'waiting to release vacuum', 'not active', '2021-09-30 16:00:00', 'pre production', 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_progress`
--

CREATE TABLE `app_progress` (
  `id` int(11) NOT NULL,
  `process` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(300) COLLATE utf8_unicode_ci NOT NULL,
  `percentage` decimal(4,1) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `app_report`
--

CREATE TABLE `app_report` (
  `id` int(11) NOT NULL,
  `type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `time_completed` timestamp NULL DEFAULT NULL,
  `file_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_report`
--

INSERT INTO `app_report` (`id`, `type`, `time_completed`, `file_name`, `deleted`) VALUES
(1, 'pre production', '2022-02-18 02:42:00', 'pre_production_18Feb2022', 1),
(2, 'pre production', '2022-02-18 02:48:35', 'pre_production_18Feb2022(1)', 1),
(3, 'production', '2022-02-18 02:54:03', 'production_18Feb2022', 0),
(4, 'production', '2022-02-18 02:57:04', 'production_18Feb2022(1)', 0),
(5, 'post production', '2022-02-18 03:03:52', 'post_production_18Feb2022', 0),
(6, 'pre production', '2022-02-18 03:10:11', 'pre_production_18Feb2022(1)(1)', 1),
(7, 'pre production', '2022-02-18 03:10:34', 'pre_production_18Feb2022(1)(1)(1)', 1),
(8, 'pre production', '2022-02-18 03:13:15', 'pre_production_18Feb2022(1)(1)(1)(1)', 1),
(9, 'pre production', '2022-02-18 03:14:58', 'pre_production_18Feb2022(1)(1)(1)(1)(1)', 1),
(10, 'pre production', '2022-02-18 03:16:34', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)', 1),
(11, 'pre production', '2022-02-18 03:17:31', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)(1)', 1),
(12, 'pre production', '2022-02-18 03:18:51', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)(1)(1)', 1),
(13, 'pre production', '2022-02-18 03:21:13', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)(1)(1)(1)', 1),
(14, 'pre production', '2022-02-18 06:27:48', 'pre_production_18Feb2022(1)', 1),
(15, 'production', '2022-02-18 06:37:56', 'production_18Feb2022(1)(1)', 0),
(16, 'pre production', '2022-02-18 06:39:40', 'pre_production_18Feb2022(1)(1)', 1),
(17, 'production', '2022-02-18 06:43:56', 'production_18Feb2022(1)(1)(1)', 0),
(18, 'pre production', '2022-02-18 06:55:17', 'pre_production_18Feb2022(1)(1)(1)', 1),
(19, 'pre production', '2022-02-18 07:06:35', 'pre_production_18Feb2022(1)(1)(1)(1)', 1),
(20, 'pre production', '2022-02-18 07:08:09', 'pre_production_18Feb2022(1)(1)(1)(1)(1)', 1),
(21, 'pre production', '2022-02-18 07:10:15', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)', 1),
(22, 'pre production', '2022-02-18 07:12:07', 'pre_production_18Feb2022(1)(1)(1)(1)(1)(1)(1)', 1),
(23, 'production', '2022-02-18 07:19:27', 'production_18Feb2022(1)(1)(1)(1)', 0),
(24, 'pre production', '2022-02-18 07:34:39', 'pre_production_18Feb2022', 0),
(25, 'pre production', '2022-02-18 07:36:32', 'pre_production_18Feb2022(1)', 0),
(26, 'pre production', '2022-02-18 07:42:53', 'pre_production_18Feb2022(1)(1)', 0),
(27, 'pre production', '2022-02-18 08:20:06', 'pre_production_18Feb2022(1)(1)(1)', 0),
(28, 'pre production', '2022-02-18 08:23:01', 'pre_production_18Feb2022(1)(1)(1)(1)', 0),
(29, 'pre production', '2022-02-18 08:36:13', 'pre_production_18Feb2022(1)(1)(1)(1)(1)', 0),
(30, 'production', '2022-02-21 01:18:57', 'production_21Feb2022', 0),
(31, 'production', '2022-02-21 01:23:04', 'production_21Feb2022(1)', 0),
(32, 'production', '2022-02-21 01:24:57', 'production_21Feb2022(1)(1)', 0),
(33, 'production', '2022-02-21 01:27:12', 'production_21Feb2022(1)(1)(1)', 0),
(34, 'production', '2022-02-21 01:28:38', 'production_21Feb2022(1)(1)(1)(1)', 0),
(35, 'production', '2022-02-21 01:30:56', 'production_21Feb2022(1)(1)(1)(1)(1)', 0),
(36, 'production', '2022-02-21 08:23:46', 'production_21Feb2022(1)(1)(1)(1)(1)(1)', 0),
(37, 'production', '2022-02-22 00:51:34', 'production_22Feb2022', 0),
(38, 'production', '2022-02-22 01:41:29', 'production_22Feb2022(1)', 0),
(39, 'production', '2022-02-22 01:44:57', 'production_22Feb2022(1)(1)', 0),
(40, 'production', '2022-02-22 01:53:38', 'production_22Feb2022(1)(1)(1)', 0),
(41, 'production', '2022-02-22 02:42:29', 'production_22Feb2022(1)(1)(1)(1)', 0),
(42, 'pre production', '2022-02-22 02:43:23', 'pre_production_22Feb2022', 0),
(43, 'pre production', '2022-02-22 04:41:13', 'pre_production_22Feb2022(1)', 0),
(44, 'pre production', '2022-02-22 04:41:58', 'pre_production_22Feb2022(1)(1)', 0),
(45, 'production', '2022-02-22 04:42:33', 'production_22Feb2022(1)(1)(1)(1)(1)', 0),
(46, 'production', '2022-02-22 04:45:49', 'production_22Feb2022(1)(1)(1)(1)(1)(1)', 0),
(47, 'post production', '2022-02-25 07:50:58', 'post_production_25Feb2022', 0),
(48, 'production', '2022-02-25 08:05:37', 'production_25Feb2022', 0),
(49, 'production', '2022-02-25 08:07:47', 'production_25Feb2022(1)', 0),
(50, 'pre production', '2022-02-28 00:55:15', 'pre_production_28Feb2022', 1),
(51, 'pre production', '2022-02-28 00:56:27', 'pre_production_28Feb2022', 0),
(52, 'production', '2022-02-28 01:03:37', 'production_28Feb2022', 0),
(53, 'post production', '2022-02-28 01:07:14', 'post_production_28Feb2022', 0),
(54, 'post production', '2022-02-28 01:12:49', 'post_production_28Feb2022(1)', 0),
(55, 'production', '2022-02-28 01:16:13', 'production_28Feb2022(1)', 0),
(56, 'post production', '2022-03-01 02:18:45', 'post_production_1Mar2022', 0);

-- --------------------------------------------------------

--
-- Table structure for table `app_reportvalues`
--

CREATE TABLE `app_reportvalues` (
  `id` int(11) NOT NULL,
  `file_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `fields` longtext COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_reportvalues`
--

INSERT INTO `app_reportvalues` (`id`, `file_name`, `fields`) VALUES
(6, 'production_21Feb2022', '[{\"variable\": \"lot or drum number\", \"value\": \"1\"}, {\"variable\": \"vacuum pressure serial no\", \"value\": \"\"}, {\"variable\": \"vessel temp serial no\", \"value\": \"\"}, {\"variable\": \"heater set serial no\", \"value\": \"\"}, {\"variable\": \"nitrogen flow serial no\", \"value\": \"\"}]'),
(7, 'production_21Feb2022(1)(1)(1)(1)(1)(1)', '[{\"variable\": \"lot or drum number\", \"value\": \"Y20200620D4\"}, {\"variable\": \"vacuum pressure serial no\", \"value\": \"12345678\"}, {\"variable\": \"vessel temp serial no\", \"value\": \"12345678\"}, {\"variable\": \"heater set serial no\", \"value\": \"12345678\"}, {\"variable\": \"nitrogen flow serial no\", \"value\": \"12345678\"}]'),
(8, 'post_production_18Feb2022', '[{\"variable\": \"day 1 cleaning temp set point\", \"value\": \"65DegC\"}, {\"variable\": \"day 2 cleaning temp set point\", \"value\": \"65DegC\"}, {\"variable\": \"day 3 drying temp set point\", \"value\": \"65DegC\"}]'),
(9, 'pre_production_28Feb2022', '[{\"variable\": \"lot or drum number\", \"value\": \"Y20200620\"}, {\"variable\": \"pre operation n2 pallet pressure\", \"value\": \"180\"}, {\"variable\": \"pre operation 2nd n2 pallet pressure\", \"value\": \"na\"}, {\"variable\": \"after operation n2 pallet pressure\", \"value\": \"100\"}, {\"variable\": \"after operation 2nd n2 pallet pressure\", \"value\": \"na\"}, {\"variable\": \"vacuum pump\", \"value\": \"1\"}, {\"variable\": \"weighing balance serial no\", \"value\": \"123456\"}, {\"variable\": \"empty 220L drum\", \"value\": \"23456\"}, {\"variable\": \"filled 220L drum with HTPB Treated\", \"value\": \"23456\"}, {\"variable\": \"amount of HTPB Treated collected\", \"value\": \"123456\"}]'),
(10, 'post_production_28Feb2022', '[{\"variable\": \"day 1 cleaning temp set point\", \"value\": \"80.0degC\"}, {\"variable\": \"day 2 cleaning temp set point\", \"value\": \"\"}, {\"variable\": \"day 3 drying temp set point\", \"value\": \"\"}]'),
(11, 'production_28Feb2022(1)', '[{\"variable\": \"lot or drum number\", \"value\": \"Y20200620\"}, {\"variable\": \"vacuum pressure serial no\", \"value\": \"123456\"}, {\"variable\": \"vessel temp serial no\", \"value\": \"123456\"}, {\"variable\": \"heater set serial no\", \"value\": \"123456\"}, {\"variable\": \"nitrogen flow serial no\", \"value\": \"123456\"}]'),
(12, 'post_production_28Feb2022(1)', '[{\"variable\": \"day 1 cleaning temp set point\", \"value\": \"80DegC\"}, {\"variable\": \"day 2 cleaning temp set point\", \"value\": \"80DegC\"}, {\"variable\": \"day 3 drying temp set point\", \"value\": \"80DegC\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `app_rtusetting`
--

CREATE TABLE `app_rtusetting` (
  `id` int(11) NOT NULL,
  `rtu_id` int(11) NOT NULL,
  `rtu_name` varchar(264) COLLATE utf8_unicode_ci NOT NULL,
  `rtu_location` varchar(264) COLLATE utf8_unicode_ci NOT NULL,
  `moist_threshold` double NOT NULL,
  `wet_threshold` double NOT NULL,
  `min_tag_read` int(11) NOT NULL,
  `average` int(11) NOT NULL,
  `data_sampling_interval` int(11) NOT NULL,
  `alarm` int(11) NOT NULL,
  `reboot` int(11) NOT NULL,
  `last_connected` datetime(6) NOT NULL,
  `sent` int(11) NOT NULL,
  `enabled` int(11) NOT NULL,
  `status` varchar(264) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_rtusetting`
--

INSERT INTO `app_rtusetting` (`id`, `rtu_id`, `rtu_name`, `rtu_location`, `moist_threshold`, `wet_threshold`, `min_tag_read`, `average`, `data_sampling_interval`, `alarm`, `reboot`, `last_connected`, `sent`, `enabled`, `status`) VALUES
(1, 1, 'monitoring_sys', 'location_name', 2, 1, 1, 1, 10, 0, 0, '2021-10-26 00:00:00.000000', 1, 1, 'idle');

-- --------------------------------------------------------

--
-- Table structure for table `app_savefile`
--

CREATE TABLE `app_savefile` (
  `id` int(11) NOT NULL,
  `username` varchar(264) COLLATE utf8_unicode_ci NOT NULL,
  `layout` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `device` longtext COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_savefile`
--

INSERT INTO `app_savefile` (`id`, `username`, `layout`, `device`) VALUES
(1, 'nick', '[]', '[]'),
(2, 'guest', '[]', '[]'),
(3, 'steng', '[]', '[]'),
(4, 'steng', '[]', '[]');

-- --------------------------------------------------------

--
-- Table structure for table `app_sensorreading`
--

CREATE TABLE `app_sensorreading` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `value` decimal(10,3) NOT NULL,
  `unit` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `set_point` decimal(10,3) DEFAULT NULL,
  `status` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_sensorreading`
--

INSERT INTO `app_sensorreading` (`id`, `name`, `value`, `unit`, `set_point`, `status`) VALUES
(9, 'pressure', '0.000', 'kPa', NULL, NULL),
(10, 'n2 flow rate', '0.000', 'L/min', '0.000', '0'),
(11, 'temperature', '0.000', '°C', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `app_userdetail`
--

CREATE TABLE `app_userdetail` (
  `id` int(11) NOT NULL,
  `role` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `phone_number` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_userdetail`
--

INSERT INTO `app_userdetail` (`id`, `role`, `phone_number`, `user_id`) VALUES
(1, 'Super Admin', '', 1),
(4, 'Guest', '', 4),
(5, 'Engineer', '', 5);

-- --------------------------------------------------------

--
-- Table structure for table `app_variabledefault`
--

CREATE TABLE `app_variabledefault` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `value` decimal(10,3) NOT NULL,
  `value_set` decimal(10,3) NOT NULL,
  `unit` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `process` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `prompt` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `check` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `enable_set` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `app_variabledefault`
--

INSERT INTO `app_variabledefault` (`id`, `name`, `value`, `value_set`, `unit`, `process`, `prompt`, `check`, `enable_set`) VALUES
(1, 'n2 flow rate', '20.000', '20.000', 'L/min', 'pre production', 'true', 'true', 'true'),
(2, 'purging duration', '5.000', '0.500', 'min', 'pre production', 'true', 'false', 'true'),
(3, 'n2 flow rate', '50.000', '50.000', 'L/min', 'production part 1', 'true', 'true', 'true'),
(4, 'target temperature', '63.000', '28.000', '°C', 'production part 1', 'true', 'true', 'true'),
(5, 'logging interval', '30.000', '30.000', 'min', 'production part 1', 'true', 'false', 'true'),
(6, 'heater set point', '80.000', '80.000', '°C', 'production part 1', 'true', 'false', 'true'),
(7, 'pressure', '1.800', '1.800', 'kPa', 'production part 1', 'false', 'true', 'true'),
(8, 'n2 flow rate tolerance', '10.000', '10.000', 'L/min', 'production part 1', 'false', 'false', 'true'),
(9, 'pressure tolerance', '0.500', '0.500', 'kPa', 'production part 1', 'false', 'false', 'true'),
(13, 'logging interval', '30.000', '0.200', 'min', 'production part 2', 'true', 'false', 'true'),
(14, 'process duration', '240.000', '1.000', 'min', 'production part 2', 'true', 'false', 'true'),
(15, 'heater set point', '67.500', '67.500', '°C', 'production part 2', 'true', 'false', 'true'),
(16, 'n2 flow rate', '150.000', '150.000', 'L/min', 'production part 3', 'true', 'true', 'true'),
(17, 'process duration', '240.000', '1.000', 'min', 'production part 3', 'true', 'false', 'true'),
(18, 'heater set point', '67.500', '67.500', '°C', 'production part 3', 'true', 'false', 'true'),
(19, 'n2 flow rate tolerance', '10.000', '10.000', 'L/min', 'production part 2', 'false', 'false', 'true'),
(20, 'pressure tolerance', '0.500', '0.500', 'kPa', 'production part 2', 'false', 'false', 'true'),
(21, 'temperature tolerance', '2.000', '2.000', '°C', 'production part 2', 'true', 'false', 'true'),
(22, 'n2 flow rate tolerance', '10.000', '10.000', 'L/min', 'production part 3', 'false', 'false', 'true'),
(23, 'pressure tolerance', '5.000', '5.000', 'kPa', 'production part 3', 'false', 'false', 'true'),
(24, 'temperature tolerance', '2.000', '2.000', '°C', 'production part 3', 'true', 'false', 'true'),
(25, 'logging interval', '60.000', '0.200', 'min', 'production part 3', 'true', 'false', 'true'),
(26, 'process duration', '480.000', '0.200', 'min', 'post production day 1', 'true', 'false', 'true'),
(27, 'logging interval', '120.000', '0.100', 'min', 'post production day 1', 'true', 'false', 'true'),
(28, 'process duration', '480.000', '0.300', 'min', 'post production day 2', 'true', 'false', 'true'),
(29, 'logging interval', '120.000', '0.100', 'min', 'post production day 2', 'true', 'false', 'true'),
(30, 'process duration', '360.000', '0.300', 'min', 'post production day 3', 'true', 'false', 'true'),
(31, 'logging interval', '120.000', '0.100', 'min', 'post production day 3', 'true', 'false', 'true'),
(32, 'pressure', '1.800', '1.800', 'kPa', 'production part 2', 'false', 'true', 'true'),
(33, 'pressure', '6.000', '6.000', 'kPa', 'production part 3', 'false', 'false', 'true'),
(34, 'n2 flow rate', '50.000', '50.000', 'L/min', 'production part 2', 'false', 'false', 'true'),
(35, 'n2 flow rate tolerance', '5.000', '5.000', 'L/min', 'pre production', 'false', 'false', 'true'),
(36, 'set temperature', '65.000', '65.000', '°C', 'production part 2', 'true', 'false', 'true'),
(37, 'set temperature', '65.000', '65.000', '°C', 'production part 3', 'true', 'false', 'true');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add rtu setting', 7, 'add_rtusetting'),
(26, 'Can change rtu setting', 7, 'change_rtusetting'),
(27, 'Can delete rtu setting', 7, 'delete_rtusetting'),
(28, 'Can view rtu setting', 7, 'view_rtusetting'),
(29, 'Can add user detail', 8, 'add_userdetail'),
(30, 'Can change user detail', 8, 'change_userdetail'),
(31, 'Can delete user detail', 8, 'delete_userdetail'),
(32, 'Can view user detail', 8, 'view_userdetail'),
(33, 'Can add save file', 9, 'add_savefile'),
(34, 'Can change save file', 9, 'change_savefile'),
(35, 'Can delete save file', 9, 'delete_savefile'),
(36, 'Can view save file', 9, 'view_savefile'),
(37, 'Can add log data', 10, 'add_logdata'),
(38, 'Can change log data', 10, 'change_logdata'),
(39, 'Can delete log data', 10, 'delete_logdata'),
(40, 'Can view log data', 10, 'view_logdata'),
(41, 'Can add process list', 11, 'add_processlist'),
(42, 'Can change process list', 11, 'change_processlist'),
(43, 'Can delete process list', 11, 'delete_processlist'),
(44, 'Can view process list', 11, 'view_processlist'),
(45, 'Can add report', 12, 'add_report'),
(46, 'Can change report', 12, 'change_report'),
(47, 'Can delete report', 12, 'delete_report'),
(48, 'Can view report', 12, 'view_report'),
(49, 'Can add variable default', 13, 'add_variabledefault'),
(50, 'Can change variable default', 13, 'change_variabledefault'),
(51, 'Can delete variable default', 13, 'delete_variabledefault'),
(52, 'Can view variable default', 13, 'view_variabledefault'),
(53, 'Can add log data type', 14, 'add_logdatatype'),
(54, 'Can change log data type', 14, 'change_logdatatype'),
(55, 'Can delete log data type', 14, 'delete_logdatatype'),
(56, 'Can view log data type', 14, 'view_logdatatype'),
(57, 'Can add process layout', 15, 'add_processlayout'),
(58, 'Can change process layout', 15, 'change_processlayout'),
(59, 'Can delete process layout', 15, 'delete_processlayout'),
(60, 'Can view process layout', 15, 'view_processlayout'),
(61, 'Can add progress', 16, 'add_progress'),
(62, 'Can change progress', 16, 'change_progress'),
(63, 'Can delete progress', 16, 'delete_progress'),
(64, 'Can view progress', 16, 'view_progress'),
(65, 'Can add sensor reading', 17, 'add_sensorreading'),
(66, 'Can change sensor reading', 17, 'change_sensorreading'),
(67, 'Can delete sensor reading', 17, 'delete_sensorreading'),
(68, 'Can view sensor reading', 17, 'view_sensorreading'),
(69, 'Can add report values', 18, 'add_reportvalues'),
(70, 'Can change report values', 18, 'change_reportvalues'),
(71, 'Can delete report values', 18, 'delete_reportvalues'),
(72, 'Can view report values', 18, 'view_reportvalues');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$150000$qFy3Ea1BCE06$Kw0OjRBP7SZIOTyuiATj5diUb+xXCfhIVLAOEmkT50U=', '2022-01-03 03:35:52.779837', 1, 'nick', 'nick', 'hoo', 'n1ck940712@gmail.com', 1, 1, '2021-10-26 14:17:35.641145'),
(4, 'pbkdf2_sha256$150000$GckdIqROJNYi$ujCq0fhDjXTZR2QW4Sj98T0XW7RlGRGcfTDc9OFufFU=', '2022-02-25 07:44:35.663336', 0, 'guest', '', '', '', 0, 1, '2021-11-04 13:56:02.818682'),
(5, 'pbkdf2_sha256$150000$eHIDlIjzEWtT$hdISJ27tjj5f1pS8TiOWKevPzxw0e1Z1V2JoNk7qP6I=', NULL, 0, 'steng', '', '', 'steng@steng.com', 0, 1, '2021-11-26 05:57:04.542807');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(10, 'app', 'logdata'),
(14, 'app', 'logdatatype'),
(15, 'app', 'processlayout'),
(11, 'app', 'processlist'),
(16, 'app', 'progress'),
(12, 'app', 'report'),
(18, 'app', 'reportvalues'),
(7, 'app', 'rtusetting'),
(9, 'app', 'savefile'),
(17, 'app', 'sensorreading'),
(8, 'app', 'userdetail'),
(13, 'app', 'variabledefault'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-10-26 14:14:43.389679'),
(2, 'auth', '0001_initial', '2021-10-26 14:14:44.203028'),
(3, 'admin', '0001_initial', '2021-10-26 14:14:44.925073'),
(4, 'admin', '0002_logentry_remove_auto_add', '2021-10-26 14:14:45.144542'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2021-10-26 14:14:45.195291'),
(6, 'app', '0001_initial', '2021-10-26 14:14:45.378951'),
(7, 'app', '0002_pressuretransmitter_unit', '2021-10-26 14:14:45.546120'),
(8, 'app', '0003_auto_20211012_1550', '2021-10-26 14:14:45.693780'),
(9, 'app', '0004_auto_20211012_1552', '2021-10-26 14:14:45.774739'),
(10, 'app', '0005_auto_20211012_1553', '2021-10-26 14:14:45.862009'),
(11, 'app', '0006_auto_20211012_1734', '2021-10-26 14:14:45.951237'),
(12, 'app', '0007_auto_20211012_1737', '2021-10-26 14:14:46.154801'),
(13, 'app', '0008_device_control', '2021-10-26 14:14:46.200696'),
(14, 'app', '0009_auto_20211018_1520', '2021-10-26 14:14:46.274266'),
(15, 'app', '0010_auto_20211022_1556', '2021-10-26 14:14:46.312938'),
(16, 'app', '0011_auto_20211022_1559', '2021-10-26 14:14:46.352354'),
(17, 'app', '0012_devicesetpoint', '2021-10-26 14:14:46.420795'),
(18, 'app', '0013_auto_20211026_2214', '2021-10-26 14:14:46.660995'),
(19, 'contenttypes', '0002_remove_content_type_name', '2021-10-26 14:14:46.865094'),
(20, 'auth', '0002_alter_permission_name_max_length', '2021-10-26 14:14:46.960934'),
(21, 'auth', '0003_alter_user_email_max_length', '2021-10-26 14:14:47.072969'),
(22, 'auth', '0004_alter_user_username_opts', '2021-10-26 14:14:47.121495'),
(23, 'auth', '0005_alter_user_last_login_null', '2021-10-26 14:14:47.214133'),
(24, 'auth', '0006_require_contenttypes_0002', '2021-10-26 14:14:47.222862'),
(25, 'auth', '0007_alter_validators_add_error_messages', '2021-10-26 14:14:47.267968'),
(26, 'auth', '0008_alter_user_username_max_length', '2021-10-26 14:14:47.392986'),
(27, 'auth', '0009_alter_user_last_name_max_length', '2021-10-26 14:14:47.651449'),
(28, 'auth', '0010_alter_group_name_max_length', '2021-10-26 14:14:50.966513'),
(29, 'auth', '0011_update_proxy_permissions', '2021-10-26 14:14:51.119556'),
(30, 'sessions', '0001_initial', '2021-10-26 14:14:51.580718'),
(31, 'app', '0002_logdata_processlist_report', '2021-10-27 02:11:30.283254'),
(32, 'app', '0003_processlist_category', '2021-10-27 02:14:25.138493'),
(33, 'app', '0004_variabledefault', '2021-10-27 09:37:29.150265'),
(34, 'app', '0005_auto_20211027_1740', '2021-10-27 09:40:58.323504'),
(35, 'app', '0006_processlist_order', '2021-10-27 13:29:03.434410'),
(36, 'app', '0007_logdatatype', '2021-10-28 05:11:52.053298'),
(37, 'app', '0008_processlayout', '2021-10-28 09:23:31.986828'),
(38, 'app', '0009_variabledefault_value_set', '2021-10-29 04:53:55.635574'),
(39, 'app', '0010_variabledefault_prompt', '2021-10-29 06:07:14.633978'),
(40, 'app', '0011_variabledefault_check', '2021-10-29 07:21:39.836026'),
(41, 'app', '0012_auto_20211101_1724', '2021-11-01 09:24:32.156959'),
(42, 'app', '0013_report_file_name', '2021-11-04 07:16:04.135910'),
(43, 'app', '0014_variabledefault_enable_set', '2021-11-04 07:59:23.612382'),
(44, 'app', '0015_progress', '2021-11-16 02:50:48.071523'),
(45, 'app', '0016_progress_percentage', '2021-11-16 02:55:01.348129'),
(46, 'app', '0015_sensorreading', '2021-11-24 08:16:06.374488'),
(47, 'app', '0016_auto_20211124_1618', '2021-11-24 08:18:24.922321'),
(48, 'app', '0017_progress', '2021-11-25 02:24:51.960867'),
(49, 'app', '0018_report_deleted', '2022-02-15 09:01:00.277379'),
(50, 'app', '0019_reportvalues', '2022-02-18 03:34:20.131379'),
(51, 'app', '0020_auto_20220218_1201', '2022-02-18 04:01:25.702373');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('34cc98hmex3k3w0zeklr5z2rx1jypblk', 'ZmNjNjUzN2E4ZmExOTYxYTEzOGM1MDhlNzE0ZjUxODJmZWZmYTEzNzp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyNjYxMTQ0LjcxMDgzOTd9', '2022-02-03 06:45:45.053720'),
('46r7i84uz3ndzcpwnq0n4ma6bf4a40jh', 'YzhkODE4MGUzMjA3ZjRkMTI4ZTY0YzY4NDVmZGIzZDgzMDBjNWRmZTp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ0ODAwNzM1LjYwMjQ4Mn0=', '2022-02-28 01:05:35.635966'),
('4ied8y1gm7cpu5kalikpaio632h1t8cj', 'MTJlMzA3MGY4NDI3NGE2YzQwYTRjNmQwNmY1ZDczMTQyOTM4MDQwMjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ0OTcxNTgyLjc1NDE2Njh9', '2022-03-02 00:33:02.787543'),
('55s908vfufi2uz554rg93c77k63ixok1', 'MmY0MGVkZGY0MGZlMTk4NDY4OGNlZDM2MzdlODJjN2NkNzBjMWQyMzp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMTQxNTcwLjIxOTA0OTV9', '2022-01-28 06:26:10.325767'),
('59zwf9tiz670sbgqk8qprkazqjqs2lch', 'NTNkOTljZWI4Yzc1ODNiODBjNTY1NDIzODJkZWRlMDU4ODAzNzAxMjp7Il9zZXNzaW9uX2luaXRfdGltZXN0YW1wXyI6MTY0NDU3MDUxMS45NDMxODYzLCJfYXV0aF91c2VyX2lkIjoiNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzJkNDUxMjQwZDYyZmNmZWNjMTE0MDhlZWQyODNkNjFhZjhhNjg0YyJ9', '2022-02-25 09:08:40.655593'),
('728yfgds8srphnlu7diy5ipu93wv7cci', 'MjRiMTE5ZTRmNTQ2NTg4OWE5MGFkNWI3OTNlYTNmNmU0YmVmOWNiOTp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ0Mzg1OTcyLjM2Mzk1NjJ9', '2022-02-23 05:52:52.398996'),
('81hbl28qb7pgxzqxxqpjknuy7fm7stsm', 'MTY4NDRhMGExZmUwNmFjZmUyZjhlZWZmMmZkNTJkYzU1OTg2ZjJhMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMzkwOTExLjE5ODA4OX0=', '2022-01-31 03:41:51.276193'),
('8hnzscplzt8tj04ypuphcpf4ewzr72fd', 'NzdjNDdkN2I0ZjU2NDkzZDVkNmYxNDlkOTAzODNjZGVjYTk2MzZmNTp7Il9zZXNzaW9uX2luaXRfdGltZXN0YW1wXyI6MTY0NTE1MTc1OC4yODcwNjUsIl9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIn0=', '2022-03-04 02:35:59.267688'),
('8ydw7ly9zrryw4xljrg8if6ajjiqznou', 'NjE4NzgyYzlhMjQyZjAwOGEwNDg2ZWYxMDA2NDBmNzMyMmIwM2RkZjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ0OTkwMjIwLjMzNDk3NjR9', '2022-03-02 05:43:40.606374'),
('afmutxj7qupz3ufdacux9iguxyo6znie', 'MzU3NjdlYjRlMzBjZDQ1YTczZDViNDNjOTY2ZTU0NmI2ZjAyMmI5Nzp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMzkzODkxLjY5ODYzODd9', '2022-01-31 04:31:31.735344'),
('czughprzu0knl1a2w3y370djd3wbpfjf', 'NjkxZTkwM2NhN2M2MDUzZmZkODViOWQwYWNhYTM0NzBmYWQ4NTBkZDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMzgzNTk3LjQwNzc5NTd9', '2022-01-31 01:39:57.460075'),
('fzrlrqw41ksh7uoarcbol9cfyh669f3r', 'NTBlMDI0MDZhNTE4NDk1NzA0MDM3OTI1YWFiMGE4MDQ4NzQxNDU2Yjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQxMTgxMzA0LjUzNTAxOTZ9', '2022-01-17 03:41:44.597814'),
('iokyyq6xqao42vw8bfyk41xohctlcbbf', 'ZTg0ODJhMzhiMzQ0YTEzMjNkN2M3NGE4ZDgxYTFkNzdjNTAwNWI2MTp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMzk0OTUzLjY3MjUyNjZ9', '2022-01-31 04:49:13.717224'),
('o495t1qxf0zvl4zdbnyvdt6bk0zoabwk', 'NmJhMWRmOWJmZDE4NmI5MjJmMDU1Yzk3ZTFjYWM1ODE5ZjUzOGJjNjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ1Nzc1MDgyLjE0MjQ4NjN9', '2022-03-11 07:44:42.194040'),
('scvmh6xy227y8th3iq8weiwgqarah0mk', 'NTkzNmFlM2ZiZWZjZDFhNmFkYzk1ODczNzM2YTllZGFmYjM5N2FjYjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyMzk0ODkwLjQwNzcxMjJ9', '2022-01-31 04:48:10.447761'),
('sewxe4izlom0w9drfx2tfe6i8tp0j4wm', 'MmZhOWZkYmU0NTliY2U1NTg1OTU3NzEyNzFjOGIxMjZiZTJhNzFiZjp7Il9zZXNzaW9uX2luaXRfdGltZXN0YW1wXyI6MTY0NDU3MDUxMC44ODQ5NzMzfQ==', '2022-02-25 09:08:31.630203'),
('uo6bw27yleqq0bzi3t2c1yyt99r5k3cr', 'OWE2YmVmMjM5ZmI2Y2MyODA4MjBmM2Q5MzQzMzI0ODhmMmIxYmIwZDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ0MzgzMzI4Ljg0MzQzMzR9', '2022-02-23 05:08:48.966908'),
('x18ft2q2ber78knryt6nn1b27xk4g2ch', 'ZWY2OTAxYmYxYzlhMzMzZWI4ODhmODRjY2VkYjE0ZTQ5YjYzNjBkMjp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQyNzMwMzM5LjAzN30=', '2022-02-04 01:58:59.105502'),
('zrve37ls3qxjjpqbs5dhz0au73cn79vt', 'YTA5NTljNTBjMGY0ZGM4MDg1OTA4MjY2MDdkNjUzNjU0OGIyM2JlMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzMmQ0NTEyNDBkNjJmY2ZlY2MxMTQwOGVlZDI4M2Q2MWFmOGE2ODRjIiwiX3Nlc3Npb25faW5pdF90aW1lc3RhbXBfIjoxNjQ1MDY1ODU3LjE0NzY1Mzh9', '2022-03-03 02:44:17.184420');

-- --------------------------------------------------------

--
-- Table structure for table `test_sensor_reading`
--

CREATE TABLE `test_sensor_reading` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `unit` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `test_sensor_reading`
--

INSERT INTO `test_sensor_reading` (`id`, `name`, `value`, `unit`) VALUES
(1, 'temperature', '80.00', '°C'),
(2, 'n2 flow rate', '2.56', 'L/min'),
(3, 'pressure', '12.90', 'Bar');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_logdata`
--
ALTER TABLE `app_logdata`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_logdatatype`
--
ALTER TABLE `app_logdatatype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_processlayout`
--
ALTER TABLE `app_processlayout`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_processlist`
--
ALTER TABLE `app_processlist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_progress`
--
ALTER TABLE `app_progress`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_report`
--
ALTER TABLE `app_report`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_reportvalues`
--
ALTER TABLE `app_reportvalues`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_rtusetting`
--
ALTER TABLE `app_rtusetting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_savefile`
--
ALTER TABLE `app_savefile`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_sensorreading`
--
ALTER TABLE `app_sensorreading`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_userdetail`
--
ALTER TABLE `app_userdetail`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `app_variabledefault`
--
ALTER TABLE `app_variabledefault`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `test_sensor_reading`
--
ALTER TABLE `test_sensor_reading`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_logdata`
--
ALTER TABLE `app_logdata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=193;
--
-- AUTO_INCREMENT for table `app_logdatatype`
--
ALTER TABLE `app_logdatatype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `app_processlayout`
--
ALTER TABLE `app_processlayout`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `app_processlist`
--
ALTER TABLE `app_processlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
--
-- AUTO_INCREMENT for table `app_progress`
--
ALTER TABLE `app_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4044;
--
-- AUTO_INCREMENT for table `app_report`
--
ALTER TABLE `app_report`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;
--
-- AUTO_INCREMENT for table `app_reportvalues`
--
ALTER TABLE `app_reportvalues`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `app_rtusetting`
--
ALTER TABLE `app_rtusetting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `app_savefile`
--
ALTER TABLE `app_savefile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `app_sensorreading`
--
ALTER TABLE `app_sensorreading`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `app_userdetail`
--
ALTER TABLE `app_userdetail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `app_variabledefault`
--
ALTER TABLE `app_variabledefault`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
--
-- AUTO_INCREMENT for table `test_sensor_reading`
--
ALTER TABLE `test_sensor_reading`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `app_userdetail`
--
ALTER TABLE `app_userdetail`
  ADD CONSTRAINT `app_userdetail_user_id_02aec821_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
