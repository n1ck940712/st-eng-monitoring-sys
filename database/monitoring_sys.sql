-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 03, 2022 at 03:57 PM
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
CREATE DATABASE IF NOT EXISTS `monitoring_sys` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `monitoring_sys`;

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

--
-- Dumping data for table `app_logdatatype`
--

INSERT INTO `app_logdatatype` (`id`, `type`, `unit`) VALUES
(1, 'n2 flow rate', 'L/min'),
(2, 'temperature', '°C'),
(3, 'pressure', 'bar');

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

--
-- Dumping data for table `app_rtusetting`
--

INSERT INTO `app_rtusetting` (`id`, `rtu_id`, `rtu_name`, `rtu_location`, `moist_threshold`, `wet_threshold`, `min_tag_read`, `average`, `data_sampling_interval`, `alarm`, `reboot`, `last_connected`, `sent`, `enabled`, `status`) VALUES
(1, 1, 'monitoring_sys', 'location_name', 2, 1, 1, 1, 10, 0, 0, '2021-10-26 00:00:00.000000', 1, 1, 'idle');

--
-- Dumping data for table `app_savefile`
--

INSERT INTO `app_savefile` (`id`, `username`, `layout`, `device`) VALUES
(1, 'nick', '[]', '[]'),
(2, 'guest', '[]', '[]'),
(3, 'steng', '[]', '[]'),
(4, 'steng', '[]', '[]');

--
-- Dumping data for table `app_sensorreading`
--

INSERT INTO `app_sensorreading` (`id`, `name`, `value`, `unit`, `set_point`, `status`) VALUES
(9, 'pressure', '0.000', 'kPa', NULL, NULL),
(10, 'n2 flow rate', '0.000', 'L/min', '0.000', '0'),
(11, 'temperature', '0.000', '°C', NULL, NULL);

--
-- Dumping data for table `app_userdetail`
--

INSERT INTO `app_userdetail` (`id`, `role`, `phone_number`, `user_id`) VALUES
(1, 'Super Admin', '', 1),
(4, 'Guest', '', 4),
(5, 'Engineer', '', 5);

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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
