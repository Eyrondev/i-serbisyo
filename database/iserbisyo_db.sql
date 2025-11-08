-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 08, 2025 at 03:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iserbisyo_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `announcements`
--

CREATE TABLE `announcements` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `slug` varchar(250) DEFAULT NULL,
  `excerpt` text DEFAULT NULL,
  `category` varchar(50) DEFAULT 'general',
  `tags` text DEFAULT NULL,
  `status` varchar(20) DEFAULT 'draft',
  `priority` varchar(20) DEFAULT 'normal',
  `created_by` int(11) NOT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `is_published` tinyint(1) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `view_count` int(11) DEFAULT 0,
  `like_count` int(11) DEFAULT 0,
  `comment_count` int(11) DEFAULT 0,
  `share_count` int(11) DEFAULT 0,
  `send_sms` tinyint(1) DEFAULT 0,
  `send_email` tinyint(1) DEFAULT 1,
  `post_on_website` tinyint(1) DEFAULT 1,
  `notify_residents` tinyint(1) DEFAULT 0,
  `featured_image` varchar(255) DEFAULT NULL,
  `attachment_path` varchar(255) DEFAULT NULL,
  `attachment_name` varchar(255) DEFAULT NULL,
  `attachment_size` int(11) DEFAULT NULL,
  `event_date` datetime DEFAULT NULL,
  `event_time` time DEFAULT NULL,
  `event_location` varchar(200) DEFAULT NULL,
  `event_organizer` varchar(100) DEFAULT NULL,
  `event_contact` varchar(50) DEFAULT NULL,
  `registration_required` tinyint(1) DEFAULT 0,
  `registration_deadline` datetime DEFAULT NULL,
  `max_participants` int(11) DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT NULL,
  `is_pinned` tinyint(1) DEFAULT 0,
  `publish_date` datetime DEFAULT NULL,
  `expiry_date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `announcements`
--

INSERT INTO `announcements` (`id`, `title`, `content`, `slug`, `excerpt`, `category`, `tags`, `status`, `priority`, `created_by`, `updated_by`, `approved_by`, `approved_at`, `is_published`, `published_at`, `view_count`, `like_count`, `comment_count`, `share_count`, `send_sms`, `send_email`, `post_on_website`, `notify_residents`, `featured_image`, `attachment_path`, `attachment_name`, `attachment_size`, `event_date`, `event_time`, `event_location`, `event_organizer`, `event_contact`, `registration_required`, `registration_deadline`, `max_participants`, `is_featured`, `is_pinned`, `publish_date`, `expiry_date`, `created_at`, `updated_at`) VALUES
(21, 'Community Vaccination Drive - COVID-19 Booster Shots', 'The Barangay Health Center will conduct a vaccination drive for COVID-19 booster shots. All residents 18 years old and above are encouraged to participate. Please bring your vaccination card and valid ID.', 'community-vaccination-drive---covid-19-booster-shots', 'Free COVID-19 booster shots available for all residents 18+ at the Barangay Health Center.', 'health', 'vaccination, covid-19, health, booster, free', 'published', 'high', 1, 1, NULL, NULL, 1, '2025-09-26 15:44:54', 245, 89, 0, 23, 1, 1, 1, 1, NULL, NULL, NULL, NULL, '2025-10-01 15:44:54', NULL, 'Barangay Health Center', 'Barangay Health Office', '09123456789', 0, NULL, NULL, 1, 1, '2025-09-26 15:44:54', '2025-11-07 00:00:00', '2025-09-28 07:44:54', '2025-11-08 10:48:51'),
(22, 'New Online Barangay Certificate System Launch', 'We are excited to announce the launch of our new online barangay certificate system. Residents can now apply for various certificates online through our website. This includes barangay clearance, certificates of residency, indigency certificates, and more.', 'new-online-barangay-certificate-system-launch', 'Apply for barangay certificates online through our new digital system.', 'services', 'online, certificates, digital, services, convenience', 'published', 'high', 1, 1, NULL, NULL, 1, '2025-09-23 15:44:54', 356, 127, 0, 45, 0, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, 0, '2025-09-23 15:44:54', '2025-11-20 00:00:00', '2025-09-28 07:44:54', '2025-11-08 10:48:39'),
(23, 'Community Clean-Up Drive - \"Linis Kalikasan\"', 'Join our monthly community clean-up drive! Let\'s work together to keep our barangay clean and green. Participants will receive free snacks and certificates of participation. Bring your own cleaning materials or get them from the registration booth.', NULL, 'Monthly community clean-up drive with free snacks and certificates for participants.', 'events', 'clean-up, environment, community, volunteer, participation', 'published', 'medium', 1, NULL, NULL, NULL, 1, '2025-09-27 15:44:54', 189, 67, 0, 19, 1, 0, 1, 1, NULL, NULL, NULL, NULL, '2025-10-03 15:44:54', '06:00:00', 'Barangay Plaza', 'Barangay Environmental Committee', '09876543210', 1, '2025-10-01 15:44:54', 100, 0, 0, '2025-09-27 15:44:54', '2025-10-12 15:44:54', '2025-09-28 07:44:54', '2025-09-28 07:44:54'),
(24, 'Senior Citizens Monthly Pension Distribution', 'All senior citizens are reminded that the monthly pension distribution will be held at the Barangay Hall. Please bring your senior citizen ID and a face mask. Distribution will follow health protocols.', NULL, 'Monthly pension distribution for senior citizens at the Barangay Hall.', 'government', 'senior citizens, pension, monthly, distribution, government', 'published', 'high', 1, NULL, NULL, NULL, 1, '2025-09-25 15:44:54', 298, 45, 0, 12, 1, 0, 1, 1, NULL, NULL, NULL, NULL, '2025-09-29 15:44:54', '08:00:00', 'Barangay Hall', 'Barangay Secretary', '09567890123', 0, NULL, NULL, 0, 0, '2025-09-25 15:44:54', '2025-09-30 15:44:54', '2025-09-28 07:44:54', '2025-09-28 07:44:54'),
(25, 'Emergency: Water Service Interruption Notice', 'URGENT: Water service will be temporarily interrupted tomorrow from 8:00 AM to 6:00 PM due to emergency pipe repairs on the main distribution line. Residents are advised to store water in advance. We apologize for the inconvenience.', NULL, 'Emergency water service interruption tomorrow 8AM-6PM for pipe repairs.', 'emergency', 'emergency, water, interruption, repairs, urgent', 'published', 'urgent', 1, NULL, NULL, NULL, 1, '2025-09-28 13:44:54', 523, 23, 0, 67, 1, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, 1, '2025-09-28 13:44:54', '2025-09-29 15:44:54', '2025-09-28 07:44:54', '2025-09-28 07:44:54'),
(27, 'awdaw', 'awda', 'awdaw', 'awda', 'health', NULL, 'published', 'normal', 1, NULL, NULL, NULL, 1, '2025-11-08 11:03:35', 0, 0, 0, 0, 0, 1, 1, 0, NULL, NULL, NULL, NULL, NULL, NULL, '', '', '', 0, NULL, NULL, 0, 0, '2025-11-08 00:00:00', '2025-11-11 00:00:00', '2025-11-08 11:03:35', '2025-11-08 11:03:35');

-- --------------------------------------------------------

--
-- Table structure for table `barangay_info`
--

CREATE TABLE `barangay_info` (
  `id` int(11) NOT NULL,
  `barangay_name` varchar(100) NOT NULL,
  `municipality` varchar(100) NOT NULL,
  `province` varchar(100) NOT NULL,
  `region` varchar(100) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `street_address` varchar(200) DEFAULT NULL,
  `barangay_hall_address` text DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `fax_number` varchar(20) DEFAULT NULL,
  `email_address` varchar(120) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `facebook_page` varchar(200) DEFAULT NULL,
  `captain_name` varchar(100) DEFAULT NULL,
  `captain_term_start` date DEFAULT NULL,
  `captain_term_end` date DEFAULT NULL,
  `secretary_name` varchar(100) DEFAULT NULL,
  `treasurer_name` varchar(100) DEFAULT NULL,
  `office_hours` text DEFAULT NULL,
  `service_days` varchar(50) DEFAULT NULL,
  `emergency_hotline` varchar(20) DEFAULT NULL,
  `total_population` int(11) DEFAULT NULL,
  `total_households` int(11) DEFAULT NULL,
  `total_area_hectares` decimal(10,2) DEFAULT NULL,
  `logo_filename` varchar(200) DEFAULT NULL,
  `seal_filename` varchar(200) DEFAULT NULL,
  `mission_statement` text DEFAULT NULL,
  `vision_statement` text DEFAULT NULL,
  `brief_history` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `barangay_info`
--

INSERT INTO `barangay_info` (`id`, `barangay_name`, `municipality`, `province`, `region`, `zip_code`, `street_address`, `barangay_hall_address`, `phone_number`, `mobile_number`, `fax_number`, `email_address`, `website`, `facebook_page`, `captain_name`, `captain_term_start`, `captain_term_end`, `secretary_name`, `treasurer_name`, `office_hours`, `service_days`, `emergency_hotline`, `total_population`, `total_households`, `total_area_hectares`, `logo_filename`, `seal_filename`, `mission_statement`, `vision_statement`, `brief_history`, `created_at`, `updated_at`) VALUES
(1, 'Partida', 'Norzagaray', 'Bulacan', '3', '3013', 'hi-way', 'Hi-way, Partida, Norzagaray, Bulacan', '09123456789', '09876543213', NULL, 'partida@gmail.com', '', '', '', NULL, NULL, '', '', '', 'Monday to Friday', '911', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-09-28 15:50:57', '2025-09-28 17:08:54');

-- --------------------------------------------------------

--
-- Table structure for table `blotter_records`
--

CREATE TABLE `blotter_records` (
  `id` int(11) NOT NULL,
  `case_number` varchar(50) NOT NULL,
  `complainant_name` varchar(100) NOT NULL,
  `complainant_address` varchar(200) DEFAULT NULL,
  `complainant_contact` varchar(20) DEFAULT NULL,
  `respondent_name` varchar(100) NOT NULL,
  `respondent_address` varchar(200) DEFAULT NULL,
  `respondent_contact` varchar(20) DEFAULT NULL,
  `incident_date` datetime NOT NULL,
  `incident_time` time DEFAULT NULL,
  `incident_place` varchar(200) DEFAULT NULL,
  `incident_type` varchar(50) DEFAULT NULL,
  `incident_description` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `resolution_date` datetime DEFAULT NULL,
  `resolution_details` text DEFAULT NULL,
  `resolved_by` int(11) DEFAULT NULL,
  `witnesses` text DEFAULT NULL,
  `evidence` text DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `priority` varchar(20) DEFAULT 'medium',
  `recorded_by` int(11) NOT NULL,
  `reported_by` varchar(100) DEFAULT NULL,
  `reporter_type` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `blotter_records`
--

INSERT INTO `blotter_records` (`id`, `case_number`, `complainant_name`, `complainant_address`, `complainant_contact`, `respondent_name`, `respondent_address`, `respondent_contact`, `incident_date`, `incident_time`, `incident_place`, `incident_type`, `incident_description`, `status`, `resolution_date`, `resolution_details`, `resolved_by`, `witnesses`, `evidence`, `remarks`, `priority`, `recorded_by`, `reported_by`, `reporter_type`, `created_at`, `updated_at`) VALUES
(1, 'BLOT-2025-001', 'Juan Santos', 'Block 1, Lot 15, Sitio A', '09123456789', 'Maria Cruz', 'Block 2, Lot 8, Sitio B', '09123456790', '2025-09-27 15:05:28', '23:30:00', 'Block 2, Lot 8, Sitio B', 'noise_complaint', 'Loud music and party until late night disturbing the neighborhood.', 'under_investigation', NULL, NULL, NULL, 'Pedro Garcia (neighbor), Ana Lopez (nearby resident)', 'Video recording of loud music, witness testimonies', 'Multiple complaints received from different neighbors', 'medium', 1, 'Barangay Tanod', 'barangay_tanod', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(2, 'BLOT-2025-002', 'Ana Reyes', 'Block 3, Lot 22, Sitio C', '09123456791', 'Unknown', 'Unknown', NULL, '2025-09-26 15:05:28', '15:15:00', 'Block 3, Lot 22 front yard', 'theft', 'Bicycle stolen from front yard while owner was inside the house.', 'referred_to_police', NULL, NULL, NULL, 'Carlos Martinez (saw suspicious person)', 'CCTV footage from nearby house', 'Case referred to barangay police for further investigation', 'high', 1, 'Ana Reyes', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(3, 'BLOT-2025-003', 'Pedro Garcia', 'Block 1, Lot 5, Sitio A', '09123456792', 'Lisa Garcia', 'Block 1, Lot 5, Sitio A', '09123456793', '2025-09-25 15:05:28', '07:45:00', 'Block 1, Lot 5 - Garcia Family Home', 'domestic_dispute', 'Family argument between husband and wife escalated to verbal altercation.', 'mediation_scheduled', NULL, NULL, NULL, 'Child witnesses (names withheld)', 'Statement from family member', 'Mediation scheduled for next week. Both parties agreed to counseling.', 'medium', 1, 'Maria Garcia', 'family_member', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(4, 'BLOT-2025-004', 'Carlos Lopez', 'Block 4, Lot 12, Sitio D', '09123456794', 'Construction Workers', 'Block 4, Lot 13 Construction Site', NULL, '2025-09-24 15:05:28', '14:20:00', 'Block 4, Lot 13 - Road in front of construction site', 'public_disturbance', 'Construction materials blocking the road, preventing residents from passing.', 'resolved', '2025-09-25 15:05:28', 'Construction company cleared the road and agreed to proper traffic management.', 1, 'Other affected residents', 'Photos of blocked road', 'Construction company agreed to clear the road immediately. Issue resolved.', 'low', 1, 'Carlos Lopez', 'neighbor', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(5, 'BLOT-2025-005', 'Rosa Dela Cruz', 'Block 2, Lot 18, Sitio B', '09123456795', 'Group of teenagers', 'Various addresses in Sitio B', NULL, '2025-09-23 15:05:28', '20:30:00', 'Barangay Basketball Court', 'vandalism', 'Graffiti painted on basketball court walls and benches.', 'active', NULL, NULL, NULL, 'Security guard on duty', 'Photos of vandalized property, CCTV footage', 'Investigation ongoing to identify the perpetrators', 'medium', 1, 'Rosa Dela Cruz', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(6, 'BLOT-2025-006', 'Miguel Fernandez', 'Block 5, Lot 7, Sitio E', '09123456796', 'Jenny Fernandez', 'Block 5, Lot 7, Sitio E', '09123456797', '2025-09-22 15:05:28', '16:00:00', 'Block 5, Lot 7 - Fernandez Family Home', 'domestic_dispute', 'Disagreement over household expenses led to heated argument.', 'resolved', '2025-09-23 15:05:28', 'Couple attended counseling and resolved their differences amicably.', 1, 'Adjacent neighbors', 'Statements from both parties', 'Both parties reconciled after barangay mediation.', 'low', 1, 'Neighbor', 'neighbor', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(7, 'BLOT-2025-007', 'Store Owner - Sari-Sari Store', 'Block 3, Lot 1, Sitio C', '09123456798', 'Mark Gonzales', 'Block 3, Lot 15, Sitio C', '09123456799', '2025-09-21 15:05:28', '11:30:00', 'Sari-Sari Store, Block 3, Lot 1', 'theft', 'Customer took merchandise without paying and left the store.', 'closed', '2025-09-22 15:05:28', 'Mark Gonzales returned and paid for the items. Both parties settled amicably.', 1, 'Other customers in the store', 'Store CCTV footage, witness statements', 'Respondent paid for the merchandise and apologized. Case closed.', 'medium', 1, 'Store Owner', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(8, 'BLOT-2025-008', 'Multiple Residents', 'Block 1, Various Lots', '09123456800', 'Stray Dogs', 'Various locations in Block 1', NULL, '2025-09-20 15:05:28', '05:00:00', 'Block 1, Various streets', 'public_disturbance', 'Pack of stray dogs causing noise and mess in the neighborhood.', 'under_investigation', NULL, NULL, NULL, 'Various residents', 'Photos and videos of stray dogs', 'Coordinating with animal control services for proper handling.', 'medium', 1, 'Multiple Residents', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(9, 'BLOT-2025-009', 'Elena Morales', 'Block 6, Lot 9, Sitio F', '09123456801', 'Taxi Driver', 'Unknown', NULL, '2025-09-19 15:05:28', '22:15:00', 'Corner of Main Street and Sitio F entrance', 'others', 'Taxi driver refused to give back correct change and used foul language.', 'dismissed', '2025-09-21 15:05:28', 'Investigation concluded with insufficient evidence to proceed.', 1, 'Other passengers', 'Receipt from taxi ride', 'Unable to identify the taxi driver. Case dismissed due to lack of evidence.', 'low', 1, 'Elena Morales', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(10, 'BLOT-2025-010', 'Roberto Silva', 'Block 4, Lot 20, Sitio D', '09123456802', 'Teenage Group', 'Various addresses in Sitio D', NULL, '2025-09-18 15:05:28', '19:45:00', 'Barangay Covered Court', 'noise_complaint', 'Group of teenagers playing loud music and making noise at the covered court.', 'resolved', '2025-09-19 15:05:28', 'Group leaders spoke with teenagers about proper noise levels and curfew hours.', 1, 'Other nearby residents', 'Audio recording of loud noise', 'Teenagers apologized and agreed to observe proper hours for recreational activities.', 'low', 1, 'Roberto Silva', 'resident', '2025-09-28 07:05:28', '2025-09-28 07:05:28'),
(0, 'BLOT-2025-011', 'jorgen', 'diliman', NULL, 'aaron', 'diliman', NULL, '2025-10-30 00:00:00', '01:54:00', 'diliman', 'noise_complaint', 'maingay ehh', 'active', NULL, NULL, NULL, NULL, NULL, NULL, 'medium', 1, 'clerk', 'witness', '2025-10-31 04:53:44', '2025-10-31 04:53:44');

-- --------------------------------------------------------

--
-- Table structure for table `certificates`
--

CREATE TABLE `certificates` (
  `id` int(11) NOT NULL,
  `resident_id` int(11) NOT NULL,
  `certificate_type` varchar(50) NOT NULL,
  `purpose` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `processed_by` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  `processed_date` datetime DEFAULT NULL,
  `claimed_date` datetime DEFAULT NULL,
  `fee` decimal(10,2) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `payment_date` datetime DEFAULT NULL,
  `certificate_number` varchar(50) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `rejection_reason` text DEFAULT NULL,
  `payment_completed` tinyint(1) DEFAULT 0,
  `moved_to_payment_list` tinyint(1) DEFAULT 0,
  `completed_date` datetime DEFAULT NULL,
  `moved_to_payment_list_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `certificates`
--

INSERT INTO `certificates` (`id`, `resident_id`, `certificate_type`, `purpose`, `status`, `processed_by`, `request_date`, `processed_date`, `claimed_date`, `fee`, `payment_status`, `payment_date`, `certificate_number`, `notes`, `rejection_reason`, `payment_completed`, `moved_to_payment_list`, `completed_date`, `moved_to_payment_list_date`) VALUES
(41, 3, 'barangay_clearance', 'Employment requirement', 'ready', NULL, '2025-09-15 06:09:03', '2025-09-18 06:09:03', NULL, 50.00, 'paid', '2025-10-31 07:30:49', 'CERT-2025-0001', NULL, NULL, 1, 0, NULL, NULL),
(44, 3, 'certificate_of_residency', 'Bank account opening', 'ready', 1, '2025-09-20 06:09:03', '2025-09-28 10:58:54', '2025-09-25 06:09:03', 30.00, 'unpaid', '2025-09-23 06:09:03', 'CERT-2025-0004', NULL, NULL, 0, 0, NULL, NULL),
(45, 4, 'barangay_clearance', 'Scholarship application', 'approved', 1, '2025-09-14 06:09:03', '2025-09-28 14:15:29', NULL, 50.00, 'unpaid', '2025-09-15 06:09:03', 'CERT-2025-0005', NULL, NULL, 0, 0, '2025-09-28 12:51:05', NULL),
(47, 3, 'certificate_of_indigency', 'Educational assistance', 'pending', NULL, '2025-09-04 06:09:03', NULL, NULL, 25.00, 'unpaid', NULL, NULL, NULL, NULL, 0, 0, NULL, NULL),
(49, 2, 'certificate_of_residency', 'Passport application', 'processing', 1, '2025-09-11 06:09:03', '2025-09-28 14:15:34', '2025-09-13 06:09:03', 30.00, 'unpaid', '2025-09-12 06:09:03', 'CERT-2025-0009', NULL, NULL, 0, 0, NULL, NULL),
(50, 1, 'barangay_clearance', 'Job application', 'processing', 1, '2025-09-21 06:09:03', '2025-09-28 10:51:02', NULL, 50.00, 'unpaid', '2025-09-21 09:09:03', NULL, 'Incomplete requirements submitted', NULL, 0, 0, NULL, NULL),
(51, 3, 'tribal_membership', 'Cultural identification', 'processing', 1, '2025-09-24 06:09:03', '2025-09-28 10:56:39', NULL, 20.00, 'unpaid', '2025-09-27 06:09:03', 'CERT-2025-0011', NULL, NULL, 0, 0, NULL, NULL),
(52, 4, 'certificate_of_indigency', 'Housing assistance', 'processing', 1, '2025-09-26 06:09:03', '2025-09-28 10:57:27', NULL, 25.00, 'unpaid', '2025-09-28 06:09:03', 'CERT-2025-0012', NULL, NULL, 0, 0, NULL, NULL),
(53, 2, 'barangay_clearance', 'Travel requirement', 'pending', NULL, '2025-09-11 06:09:03', NULL, NULL, 50.00, 'unpaid', NULL, NULL, NULL, NULL, 0, 0, NULL, NULL),
(54, 1, 'business_permit', 'Online selling business', 'processing', 1, '2025-09-03 06:09:03', '2025-10-07 11:11:38', NULL, 100.00, 'unpaid', '2025-09-04 06:09:03', NULL, 'Under review - verification in progress', NULL, 0, 0, NULL, NULL),
(55, 2, 'certificate_of_residency', 'School enrollment', 'ready', NULL, '2025-09-17 06:09:03', '2025-09-20 06:09:03', '2025-09-22 06:09:03', 30.00, 'unpaid', '2025-09-20 06:09:03', 'CERT-2025-0015', NULL, NULL, 1, 1, NULL, '2025-09-28 13:21:25'),
(57, 1, 'barangay_clearance', 'awdawd', 'pending', NULL, '2025-09-30 15:54:22', NULL, NULL, 50.00, 'unpaid', NULL, NULL, NULL, NULL, 0, 0, NULL, NULL),
(58, 1, 'business permit', 'bank_requirements', 'ready', 1, '2025-10-01 01:28:51', '2025-10-07 13:20:11', NULL, 50.00, 'unpaid', NULL, 'CT-2025-000001', NULL, NULL, 0, 0, NULL, NULL),
(59, 1, 'Certificate of Indigency', 'employment', 'pending', NULL, '2025-10-08 20:48:24', NULL, NULL, 0.00, 'unpaid', NULL, NULL, NULL, NULL, 0, 0, NULL, NULL),
(60, 1, 'Certificate of Residency', 'bank_requirements', 'rejected', 1, '2025-10-08 20:58:00', '2025-11-03 15:52:13', NULL, 30.00, 'unpaid', NULL, NULL, NULL, 'need more detailed', 0, 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `certificate_types`
--

CREATE TABLE `certificate_types` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `fee` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_available_online` tinyint(1) DEFAULT NULL,
  `requires_approval` tinyint(1) DEFAULT NULL,
  `processing_days` int(11) DEFAULT NULL,
  `requirements` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `certificate_types`
--

INSERT INTO `certificate_types` (`id`, `name`, `code`, `description`, `fee`, `is_active`, `is_available_online`, `requires_approval`, `processing_days`, `requirements`, `created_at`, `updated_at`) VALUES
(1, 'Barangay Clearance', 'barangay_clearance', 'Standard clearance certificate for various purposes', 50.00, 1, 1, 1, 3, '[\"Valid ID\", \"Proof of Residency\"]', '2025-09-28 15:03:58', '2025-09-28 15:03:58'),
(2, 'Certificate of Residency', 'certificate_of_residency', 'Certificate proving residency in the barangay', 30.00, 1, 1, 1, 2, '[\"Valid ID\", \"Proof of Address\"]', '2025-09-28 15:03:58', '2025-09-28 15:03:58'),
(3, 'Certificate of Indigency', 'certificate_of_indigency', 'Certificate for indigent residents', 0.00, 1, 1, 1, 5, '[\"Valid ID\", \"Proof of Income\", \"Social Case Study\"]', '2025-09-28 15:03:58', '2025-10-01 12:48:57'),
(4, 'Business Permit', 'business_permit', 'Permit for small business operations', 200.00, 1, 1, 1, 7, '[\"Business Registration\", \"Valid ID\", \"Location Map\"]', '2025-09-28 15:03:58', '2025-09-28 15:03:58');

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT 'Full name of the message sender',
  `email` varchar(120) NOT NULL COMMENT 'Email address of the sender',
  `phone` varchar(20) DEFAULT NULL COMMENT 'Optional phone number',
  `subject` varchar(200) NOT NULL COMMENT 'Subject/title of the message',
  `message` text NOT NULL COMMENT 'Main message content',
  `status` enum('unread','read','replied','archived') DEFAULT 'unread' COMMENT 'Current status of the message',
  `priority` enum('low','normal','high','urgent') DEFAULT 'normal' COMMENT 'Priority level assigned to message',
  `response` text DEFAULT NULL COMMENT 'Admin response to the message',
  `responded_by` int(11) DEFAULT NULL COMMENT 'User ID of admin who responded',
  `responded_at` datetime DEFAULT NULL COMMENT 'Timestamp when response was sent',
  `ip_address` varchar(45) DEFAULT NULL COMMENT 'IP address of sender (supports IPv6)',
  `user_agent` text DEFAULT NULL COMMENT 'Browser user agent string',
  `created_at` datetime DEFAULT current_timestamp() COMMENT 'When message was submitted',
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last modification time'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Contact form messages from website visitors';

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `phone`, `subject`, `message`, `status`, `priority`, `response`, `responded_by`, `responded_at`, `ip_address`, `user_agent`, `created_at`, `updated_at`) VALUES
(1, 'John Doe', 'john.doe@email.com', '+63 912 345 6789', 'Inquiry about Barangay Clearance', 'Hello, I would like to know the requirements for getting a barangay clearance certificate. How long does the process usually take?', 'unread', 'normal', NULL, NULL, NULL, '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2025-10-01 21:12:39', '2025-10-01 21:12:39'),
(2, 'Maria Santos', 'maria.santos@gmail.com', NULL, 'Certificate Processing Time', 'Good day! I submitted my certificate request last week but haven\'t received any updates. Can you please check the status?', 'read', 'high', NULL, NULL, NULL, '192.168.1.101', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '2025-10-01 21:12:39', '2025-10-01 21:12:39'),
(3, 'Pedro Cruz', 'pedro.cruz@yahoo.com', '+63 998 765 4321', 'Question about Business Permit', 'I want to start a small sari-sari store in our barangay. What are the requirements and fees for getting a business permit?', 'replied', 'normal', 'Thank you for your inquiry about the business permit. Please visit our office during business hours (8AM-5PM, Monday-Friday) and bring the following requirements: Valid ID, Proof of residence, Location sketch of your business, and the permit fee of ₱200. The processing time is typically 7 business days.', 1, '2025-10-01 21:12:39', '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)', '2025-10-01 21:12:39', '2025-10-01 21:12:39'),
(4, 'aaron', 'admin@iserbisyo.com', '1231231', 'awdaw', 'awdaadawdaawda', 'unread', 'normal', NULL, NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 13:15:03', '2025-10-01 13:15:03'),
(5, 'te', 'student@test.com', '1231', 'awdaw', 'awdawdawdaw', 'unread', 'normal', NULL, NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 15:35:20', '2025-10-01 15:35:20'),
(6, 'Aaron Joseph Mandita Jimenez', 'admin@gmail.com', '09932326567', 'button', 'awdaawdawdwaw', 'unread', 'normal', NULL, NULL, NULL, '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-02 03:27:21', '2025-11-02 03:27:21');

-- --------------------------------------------------------

--
-- Stand-in structure for view `contact_messages_summary`
-- (See below for the actual view)
--
CREATE TABLE `contact_messages_summary` (
`id` int(11)
,`name` varchar(100)
,`email` varchar(120)
,`subject` varchar(200)
,`status` enum('unread','read','replied','archived')
,`priority` enum('low','normal','high','urgent')
,`created_at` datetime
,`responded_at` datetime
,`responded_by_name` varchar(100)
,`time_category` varchar(10)
,`message_length` int(10)
);

-- --------------------------------------------------------

--
-- Table structure for table `officials`
--

CREATE TABLE `officials` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `position` varchar(50) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `term_start` date DEFAULT NULL,
  `term_end` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `committee` varchar(100) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT 'no-picture.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `officials`
--

INSERT INTO `officials` (`id`, `name`, `position`, `email`, `phone`, `term_start`, `term_end`, `is_active`, `created_at`, `updated_at`, `committee`, `profile_picture`) VALUES
(34, 'Santiago R. Malubay Jr.', 'Barangay Captain', 'captain@barangay.gov.ph', '+63 912 345 6789', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:13:36', 'Presiding Officer', 'e1ba7e6133e440b6818e4b93bcbc83a1_login_bg.png'),
(35, 'Roberto A. Hermogenes', 'Barangay Kagawad', 'r.hermogenes@barangay.gov.ph', '+63 917 123 4567', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:11', 'Committee on Appropriation', '6537dc591ce543109f36c5e226ac5bfb_no-picture.jpg'),
(36, 'Jocelyn H. Acosta', 'Barangay Kagawad', 'j.acosta@barangay.gov.ph', '+63 918 234 5678', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:50', 'Committee on Peace & Order', '6bb4ad42693c4368a5db5a02d99e7b6e_no-picture.jpg'),
(37, 'Jaime R. Celestino', '', 'j.celestino@barangay.gov.ph', '+63 919 345 6789', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:14:00', 'Committee on Health', 'eee5b34b0000407383747b7ee68077b4_no-picture.jpg'),
(38, 'Guillerma S. Cruz', 'Barangay Kagawad', 'g.cruz@barangay.gov.ph', '+63 920 456 7890', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:18', 'Committee on Education', 'dc0373b6fa6b46c183bb51be3127db73_no-picture.jpg'),
(39, 'Efren S. Reyes', 'Barangay Kagawad', 'e.reyes@barangay.gov.ph', '+63 921 567 8901', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:59', 'Committee on Health', '6beb8f5c24474b6d96f28c8531cff8a8_no-picture.jpg'),
(40, 'Reynaldo DL. Santos', '', 'r.santos@barangay.gov.ph', '+63 922 678 9012', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:14:07', 'Committee on Health', '5119847a2af5464e9c9091b605678a5b_no-picture.jpg'),
(41, 'Mary Rose C. Lavarias', 'Barangay Kagawad', 'm.lavarias@barangay.gov.ph', '+63 923 789 0123', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:40', 'Committee on Health', '0da4743e296c4bd2a1f204794facdf0b_no-picture.jpg'),
(42, 'Jayzel G. Reyes', 'SK Chairman', 'sk.chairman@barangay.gov.ph', '+63 924 890 1234', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:16:05', 'Committee on Sports', '98776f00b37b4cd2bb5e4aa0c228b8f9_no-picture.jpg'),
(43, 'Hezelyn J. Santos', 'Secretary', 'secretary@barangay.gov.ph', '+63 925 901 2345', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:14:35', 'No Chairmanship', '32530828263e4df1aad53a90b60af5b3_no-picture.jpg'),
(44, 'Reynaldo D. Gonzales', 'Treasurer', 'treasurer@barangay.gov.ph', '+63 926 012 3456', '2023-06-30', '2026-06-30', 1, '2025-10-01 14:49:20', '2025-10-01 16:15:33', 'No Chairmanship', 'f94e52eb419f4328ad1e8cb6689889d5_no-picture.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `payment_number` varchar(50) NOT NULL,
  `reference_number` varchar(100) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `resident_id` int(11) NOT NULL,
  `payer_name` varchar(200) NOT NULL,
  `payer_email` varchar(120) DEFAULT NULL,
  `payer_phone` varchar(20) DEFAULT NULL,
  `service_type` varchar(100) NOT NULL,
  `service_description` text DEFAULT NULL,
  `certificate_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(3) DEFAULT NULL,
  `payment_method` varchar(50) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `payment_gateway` varchar(50) DEFAULT NULL,
  `gateway_transaction_id` varchar(100) DEFAULT NULL,
  `gateway_response` text DEFAULT NULL,
  `receipt_number` varchar(50) DEFAULT NULL,
  `receipt_issued` tinyint(1) DEFAULT NULL,
  `receipt_issued_at` datetime DEFAULT NULL,
  `receipt_issued_by` int(11) DEFAULT NULL,
  `processed_by` int(11) DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `verification_status` varchar(20) DEFAULT NULL,
  `verification_notes` text DEFAULT NULL,
  `base_fee` decimal(10,2) DEFAULT NULL,
  `additional_fees` decimal(10,2) DEFAULT NULL,
  `discount_amount` decimal(10,2) DEFAULT NULL,
  `discount_reason` varchar(200) DEFAULT NULL,
  `tax_amount` decimal(10,2) DEFAULT NULL,
  `refund_amount` decimal(10,2) DEFAULT NULL,
  `refund_reason` varchar(500) DEFAULT NULL,
  `refund_date` datetime DEFAULT NULL,
  `refunded_by` int(11) DEFAULT NULL,
  `payment_category` varchar(50) DEFAULT NULL,
  `priority` varchar(20) DEFAULT NULL,
  `is_recurring` tinyint(1) DEFAULT NULL,
  `recurring_period` varchar(20) DEFAULT NULL,
  `notification_sent` tinyint(1) DEFAULT NULL,
  `notification_sent_at` datetime DEFAULT NULL,
  `reminder_count` int(11) DEFAULT NULL,
  `last_reminder_sent` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `internal_notes` text DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_certificate_payment` tinyint(1) DEFAULT 0,
  `moved_to_payment_list` tinyint(1) DEFAULT 0,
  `moved_to_payment_list_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `payment_number`, `reference_number`, `transaction_id`, `resident_id`, `payer_name`, `payer_email`, `payer_phone`, `service_type`, `service_description`, `certificate_id`, `amount`, `currency`, `payment_method`, `payment_status`, `payment_date`, `due_date`, `payment_gateway`, `gateway_transaction_id`, `gateway_response`, `receipt_number`, `receipt_issued`, `receipt_issued_at`, `receipt_issued_by`, `processed_by`, `processed_at`, `verification_status`, `verification_notes`, `base_fee`, `additional_fees`, `discount_amount`, `discount_reason`, `tax_amount`, `refund_amount`, `refund_reason`, `refund_date`, `refunded_by`, `payment_category`, `priority`, `is_recurring`, `recurring_period`, `notification_sent`, `notification_sent_at`, `reminder_count`, `last_reminder_sent`, `notes`, `internal_notes`, `created_by`, `updated_by`, `created_at`, `updated_at`, `is_certificate_payment`, `moved_to_payment_list`, `moved_to_payment_list_date`) VALUES
(18, 'PAY-2025-000001', NULL, NULL, 3, 'Unique User', 'unique@example.com', '09123456789', 'barangay_clearance', 'Barangay Clearance - Employment requirement', 41, 50.00, 'PHP', 'cash', 'paid', '2025-10-31 07:30:49', NULL, NULL, NULL, NULL, 'RCP-202510-000001', 1, '2025-10-31 07:30:49', 1, 1, '2025-10-31 07:30:49', 'verified', NULL, 50.00, 0.00, 0.00, NULL, 0.00, 0.00, NULL, NULL, NULL, 'service_fee', 'normal', 0, NULL, 0, NULL, 0, NULL, 'Payment for certificate #CERT-2025-0001', NULL, 1, NULL, '2025-10-31 07:30:49', '2025-10-31 07:30:49', 1, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `purok_info`
--

CREATE TABLE `purok_info` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('Purok','Sitio') DEFAULT 'Purok',
  `description` text DEFAULT NULL,
  `leader_name` varchar(100) DEFAULT NULL,
  `leader_contact` varchar(20) DEFAULT NULL,
  `leader_address` varchar(200) DEFAULT NULL,
  `boundaries` text DEFAULT NULL,
  `area_hectares` decimal(10,4) DEFAULT NULL,
  `population_count` int(11) DEFAULT 0,
  `household_count` int(11) DEFAULT 0,
  `barangay_id` int(11) DEFAULT 1,
  `is_active` tinyint(1) DEFAULT 1,
  `coordinates_lat` decimal(10,8) DEFAULT NULL,
  `coordinates_lng` decimal(11,8) DEFAULT NULL,
  `landmark` varchar(200) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `purok_info`
--

INSERT INTO `purok_info` (`id`, `name`, `type`, `description`, `leader_name`, `leader_contact`, `leader_address`, `boundaries`, `area_hectares`, `population_count`, `household_count`, `barangay_id`, `is_active`, `coordinates_lat`, `coordinates_lng`, `landmark`, `zip_code`, `created_by`, `updated_by`, `created_at`, `updated_at`) VALUES
(1, 'Diliman', 'Sitio', '', '', '09123456789', NULL, NULL, NULL, 120, 25, 1, 1, NULL, NULL, NULL, NULL, NULL, 1, '2025-09-29 01:37:37', '2025-10-31 06:33:34'),
(5, 'Lingunan', 'Sitio', '', '', NULL, NULL, NULL, NULL, 0, 0, 1, 1, NULL, NULL, NULL, NULL, 1, NULL, '2025-10-31 06:33:25', '2025-10-31 06:33:25');

-- --------------------------------------------------------

--
-- Table structure for table `residents`
--

CREATE TABLE `residents` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `suffix` varchar(10) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `house_number` varchar(20) DEFAULT NULL,
  `sitio_id` int(11) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `purok` varchar(50) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `birth_place` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `civil_status` varchar(20) DEFAULT NULL,
  `occupation` varchar(100) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `valid_id_document` varchar(255) DEFAULT NULL,
  `proof_of_residency` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `is_voter` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `residents`
--

INSERT INTO `residents` (`id`, `user_id`, `first_name`, `middle_name`, `last_name`, `suffix`, `email`, `phone`, `house_number`, `sitio_id`, `street`, `purok`, `birth_date`, `birth_place`, `gender`, `civil_status`, `occupation`, `profile_picture`, `valid_id_document`, `proof_of_residency`, `status`, `is_voter`, `created_at`, `updated_at`) VALUES
(1, 2, 'try', 'try', 'try', 'Jr.', 'aaronjosephjimenezz@gmail.com', '1231231', 'awdaw', 5, 'awdaw', 'Purok 2', '2022-06-28', 'dadaw', 'Male', 'Single', '12312', NULL, NULL, NULL, 'approved', 0, '2025-09-27 18:20:20', '2025-10-31 06:46:35'),
(2, 3, 'Test', NULL, 'User', NULL, 'test@example.com', '09123456789', '123', 5, 'Test Street', 'Zone 1', '1990-01-01', 'Test City', '', '', 'Student', NULL, NULL, NULL, 'approved', 0, '2025-09-27 18:23:22', '2025-10-31 06:46:31'),
(3, 4, 'Unique', NULL, 'User', NULL, 'unique@example.com', '09123456789', '999', 5, 'Unique Street', 'Zone 9', '1990-01-01', 'Test City', '', '', 'Doctor', NULL, NULL, NULL, 'approved', 0, '2025-09-27 18:24:07', '2025-10-31 06:46:28'),
(4, NULL, 'FileTesta', NULL, 'User', NULL, 'filetest@example.com', '09123456789', '123', 1, 'Test Street', 'Zone 1', '1990-01-01', 'Test City', '', '', 'Student', 'uploads/profiles/c07e3830-191c-4fe7-9626-8de861fd4c85.png', 'uploads/documents/b417affa-7dae-4f90-adc1-2d178dfaef36.png', 'uploads/documents/fff69a8c-928d-4bc9-bcd8-e60b67455ff6.png', 'approved', 0, '2025-09-27 18:27:48', '2025-11-04 12:41:57'),
(5, 6, 'Test', NULL, 'User', NULL, 'testuser@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'pending', 0, '2025-09-30 16:18:08', '2025-09-30 16:18:08'),
(6, 8, 'Pending', NULL, 'User', NULL, 'pending@test.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'pending', 0, '2025-09-30 16:18:08', '2025-09-30 16:18:08'),
(7, 10, 'try', 'rtyur', 'wtwe', '', 'try111@gmail.com', '09932326567', '2011', 1, NULL, NULL, '2005-06-03', 'bulacan', 'Male', 'Single', 'Student', NULL, 'uploads/documents/3f5d0002-67c1-43de-a0f2-7cd8ea4fbf2b.png', 'uploads/documents/3f8b1068-b2ff-4c45-8606-3c88ae5f194a.png', 'rejected', 0, '2025-11-03 15:22:13', '2025-11-03 15:28:20'),
(8, NULL, 'awweda', 'awda', 'wadaw', NULL, 'awdawd@gmail.com', '12312312312', '12', NULL, NULL, NULL, '2025-11-03', 'awdawda', 'Female', 'Single', 'awdwa', NULL, NULL, NULL, 'inactive', 1, '2025-11-06 04:41:25', '2025-11-06 04:41:37'),
(9, NULL, 'awdaw', 'aawda', 'awdaw', NULL, 'awdaw@gmail.com', '12312312312', 'awda', 1, NULL, NULL, '2021-02-11', 'awdwadwa', 'Male', 'Single', 'awda', NULL, NULL, NULL, 'inactive', 1, '2025-11-06 04:45:53', '2025-11-06 04:46:03');

-- --------------------------------------------------------

--
-- Table structure for table `system_activities`
--

CREATE TABLE `system_activities` (
  `id` int(11) NOT NULL,
  `activity_type` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  `target_type` varchar(50) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `system_activities`
--

INSERT INTO `system_activities` (`id`, `activity_type`, `description`, `user_id`, `target_id`, `target_type`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 'document_uploaded', 'Sample document_uploaded activity', 1, 9, 'sample', NULL, NULL, '2025-09-27 12:17:29'),
(2, 'resident_registration', 'Sample resident_registration activity', 1, 10, 'sample', NULL, NULL, '2025-09-24 12:17:29'),
(3, 'document_uploaded', 'Sample document_uploaded activity', 1, 6, 'sample', NULL, NULL, '2025-09-21 12:17:29'),
(4, 'payment_received', 'Sample payment_received activity', 1, 9, 'sample', NULL, NULL, '2025-09-22 12:17:29'),
(5, 'document_uploaded', 'Sample document_uploaded activity', 1, 4, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(6, 'certificate_claimed', 'Sample certificate_claimed activity', 1, 5, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(7, 'payment_received', 'Sample payment_received activity', 1, 1, 'sample', NULL, NULL, '2025-09-22 12:17:29'),
(8, 'document_uploaded', 'Sample document_uploaded activity', 1, 5, 'sample', NULL, NULL, '2025-09-24 12:17:29'),
(9, 'certificate_claimed', 'Sample certificate_claimed activity', 1, 9, 'sample', NULL, NULL, '2025-09-24 12:17:29'),
(10, 'document_uploaded', 'Sample document_uploaded activity', 1, 8, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(11, 'document_uploaded', 'Sample document_uploaded activity', 1, 9, 'sample', NULL, NULL, '2025-09-21 12:17:29'),
(12, 'certificate_request', 'Sample certificate_request activity', 1, 7, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(13, 'resident_registration', 'Sample resident_registration activity', 1, 8, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(14, 'document_uploaded', 'Sample document_uploaded activity', 1, 1, 'sample', NULL, NULL, '2025-09-25 12:17:29'),
(15, 'certificate_request', 'Sample certificate_request activity', 1, 9, 'sample', NULL, NULL, '2025-09-27 12:17:29'),
(16, 'payment_received', 'Sample payment_received activity', 1, 10, 'sample', NULL, NULL, '2025-09-22 12:17:29'),
(17, 'resident_registration', 'Sample resident_registration activity', 1, 4, 'sample', NULL, NULL, '2025-09-27 12:17:29'),
(18, 'resident_registration', 'Sample resident_registration activity', 1, 5, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(19, 'payment_received', 'Sample payment_received activity', 1, 4, 'sample', NULL, NULL, '2025-09-25 12:17:29'),
(20, 'resident_registration', 'Sample resident_registration activity', 1, 9, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(21, 'resident_registration', 'Sample resident_registration activity', 1, 4, 'sample', NULL, NULL, '2025-09-28 12:17:29'),
(22, 'document_uploaded', 'Sample document_uploaded activity', 1, 4, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(23, 'certificate_request', 'Sample certificate_request activity', 1, 8, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(24, 'certificate_claimed', 'Sample certificate_claimed activity', 1, 10, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(25, 'payment_received', 'Sample payment_received activity', 1, 8, 'sample', NULL, NULL, '2025-09-27 12:17:29'),
(26, 'certificate_request', 'Sample certificate_request activity', 1, 1, 'sample', NULL, NULL, '2025-09-23 12:17:29'),
(27, 'certificate_request', 'Sample certificate_request activity', 1, 9, 'sample', NULL, NULL, '2025-09-24 12:17:29'),
(28, 'resident_approval', 'Sample resident_approval activity', 1, 8, 'sample', NULL, NULL, '2025-09-21 12:17:29'),
(29, 'resident_approval', 'Sample resident_approval activity', 1, 7, 'sample', NULL, NULL, '2025-09-28 12:17:29'),
(30, 'certificate_request', 'Sample certificate_request activity', 1, 4, 'sample', NULL, NULL, '2025-09-26 12:17:29'),
(31, 'document_upload', 'Document uploaded by resident', 1, 8, 'resident', '192.168.1.175', NULL, '2025-09-13 04:16:05'),
(32, 'payment_received', 'Payment received for certificate fee', 1, NULL, 'announcement', '192.168.1.199', NULL, '2025-09-16 15:16:05'),
(33, 'resident_approval', 'Resident Jose Rizal approved', NULL, 9, 'resident', '192.168.1.142', NULL, '2025-09-20 07:44:05'),
(34, 'login', 'User Admin logged in successfully', 1, 7, 'certificate', '192.168.1.100', NULL, '2025-09-05 20:25:05'),
(35, 'certificate_payment', 'Payment received: barangay_clearance for Jose Rizal', 1, NULL, NULL, '192.168.1.136', NULL, '2025-09-15 05:22:05'),
(36, 'payment_received', 'Payment received for certificate fee', NULL, NULL, 'resident', '192.168.1.146', NULL, '2025-09-26 21:27:05'),
(37, 'resident_registration', 'New resident Jose Rizal registered', NULL, NULL, 'certificate', '192.168.1.126', NULL, '2025-09-26 02:13:05'),
(38, 'system_backup', 'System backup completed successfully', NULL, NULL, NULL, '192.168.1.146', NULL, '2025-09-12 01:22:05'),
(39, 'certificate_request', 'Certificate request: barangay_clearance for Ana Garcia', 1, 7, 'resident', '192.168.1.149', NULL, '2025-08-31 14:45:05'),
(40, 'payment_received', 'Payment received for certificate fee', NULL, 1, 'certificate', '192.168.1.129', NULL, '2025-09-13 03:01:05'),
(41, 'login', 'User Admin logged in successfully', NULL, NULL, NULL, '192.168.1.189', NULL, '2025-09-26 05:50:05'),
(42, 'certificate_payment', 'Payment received: barangay_clearance for Maria Santos', NULL, 9, 'certificate', '192.168.1.200', NULL, '2025-09-27 04:24:05'),
(43, 'announcement_create', 'Announcement created: Barangay Assembly Meeting', 1, 8, NULL, '192.168.1.156', NULL, '2025-09-05 22:13:05'),
(44, 'login', 'User Admin logged in successfully', 1, NULL, 'announcement', '192.168.1.154', NULL, '2025-09-03 01:35:05'),
(45, 'resident_registration', 'New resident Jose Rizal registered', NULL, 7, 'resident', '192.168.1.128', NULL, '2025-09-26 16:49:05'),
(46, 'certificate_request', 'Certificate request: barangay_clearance for Jose Rizal', 1, 7, 'announcement', '192.168.1.122', NULL, '2025-09-27 19:42:05'),
(47, 'login', 'User Admin logged in successfully', NULL, 1, 'announcement', '192.168.1.193', NULL, '2025-09-03 20:26:05'),
(48, 'announcement_create', 'Announcement created: Barangay Assembly Meeting', NULL, 6, NULL, '192.168.1.163', NULL, '2025-09-18 07:45:05'),
(49, 'document_upload', 'Document uploaded by resident', NULL, NULL, NULL, '192.168.1.101', NULL, '2025-08-31 03:41:05'),
(50, 'payment_received', 'Payment received for certificate fee', 1, 5, 'announcement', '192.168.1.190', NULL, '2025-09-07 18:24:05'),
(51, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Maria Santos', 1, NULL, 'resident', '192.168.1.196', NULL, '2025-09-20 19:31:05'),
(52, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Juan Cruz', NULL, 7, NULL, '192.168.1.107', NULL, '2025-09-20 19:46:05'),
(53, 'document_upload', 'Document uploaded by resident', 1, 6, 'announcement', '192.168.1.177', NULL, '2025-09-12 21:21:05'),
(54, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Ana Garcia', NULL, NULL, 'announcement', '192.168.1.135', NULL, '2025-09-28 10:07:05'),
(55, 'system_backup', 'System backup completed successfully', 1, NULL, NULL, '192.168.1.193', NULL, '2025-09-17 22:27:05'),
(56, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Ana Garcia', NULL, NULL, NULL, '192.168.1.168', NULL, '2025-09-27 22:54:05'),
(57, 'certificate_payment', 'Payment received: barangay_clearance for Jose Rizal', 1, NULL, 'certificate', '192.168.1.175', NULL, '2025-09-12 05:55:05'),
(58, 'resident_registration', 'New resident Jose Rizal registered', 1, 4, 'announcement', '192.168.1.157', NULL, '2025-09-10 14:49:05'),
(59, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Juan Cruz', 1, NULL, 'certificate', '192.168.1.146', NULL, '2025-09-08 16:59:05'),
(60, 'resident_approval', 'Resident Juan Cruz approved', 1, NULL, 'announcement', '192.168.1.193', NULL, '2025-09-21 17:07:05'),
(61, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Maria Santos', 1, NULL, 'certificate', '192.168.1.170', NULL, '2025-09-22 19:45:05'),
(62, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Maria Santos', NULL, NULL, 'announcement', '192.168.1.153', NULL, '2025-09-03 07:49:05'),
(63, 'resident_registration', 'New resident Jose Rizal registered', 1, NULL, 'resident', '192.168.1.100', NULL, '2025-09-02 09:18:05'),
(64, 'document_upload', 'Document uploaded by resident', NULL, NULL, 'certificate', '192.168.1.104', NULL, '2025-09-15 13:29:05'),
(65, 'system_backup', 'System backup completed successfully', NULL, 4, 'resident', '192.168.1.160', NULL, '2025-09-24 07:08:05'),
(66, 'certificate_payment', 'Payment received: barangay_clearance for Jose Rizal', 1, NULL, NULL, '192.168.1.168', NULL, '2025-09-19 21:31:05'),
(67, 'certificate_payment', 'Payment received: barangay_clearance for Juan Cruz', 1, 9, 'certificate', '192.168.1.175', NULL, '2025-09-11 06:46:05'),
(68, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Jose Rizal', 1, 1, 'certificate', '192.168.1.115', NULL, '2025-09-08 01:23:05'),
(69, 'resident_registration', 'New resident Jose Rizal registered', 1, 8, 'certificate', '192.168.1.113', NULL, '2025-09-16 18:48:05'),
(70, 'system_backup', 'System backup completed successfully', NULL, NULL, 'resident', '192.168.1.111', NULL, '2025-09-10 03:47:05'),
(71, 'resident_registration', 'New resident Jose Rizal registered', 1, NULL, 'resident', '192.168.1.175', NULL, '2025-08-31 05:05:05'),
(72, 'announcement_create', 'Announcement created: Barangay Assembly Meeting', 1, 4, NULL, '192.168.1.150', NULL, '2025-09-21 11:45:05'),
(73, 'certificate_claimed', 'Certificate claimed: certificate_of_residency by Maria Santos', 1, NULL, NULL, '192.168.1.167', NULL, '2025-09-06 10:47:05'),
(74, 'announcement_create', 'Announcement created: Barangay Assembly Meeting', 1, NULL, NULL, '192.168.1.160', NULL, '2025-09-08 20:26:05'),
(75, 'document_upload', 'Document uploaded by resident', 1, NULL, 'announcement', '192.168.1.135', NULL, '2025-09-26 16:11:05'),
(76, 'certificate_payment', 'Payment received: barangay_clearance for Juan Cruz', NULL, NULL, NULL, '192.168.1.119', NULL, '2025-09-16 13:26:05'),
(77, 'certificate_request', 'Certificate request: barangay_clearance for Ana Garcia', 1, 3, NULL, '192.168.1.140', NULL, '2025-08-29 08:31:05'),
(78, 'certificate_request', 'Certificate request: barangay_clearance for Jose Rizal', NULL, 9, 'announcement', '192.168.1.190', NULL, '2025-09-14 10:31:05'),
(79, 'login', 'User Admin logged in successfully', 1, NULL, NULL, '192.168.1.141', NULL, '2025-09-19 21:34:05'),
(80, 'resident_registration', 'New resident Jose Rizal registered', 1, NULL, 'resident', '192.168.1.146', NULL, '2025-08-28 22:21:05'),
(81, 'logout', 'User System Administrator logged out', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-28 12:44:56'),
(82, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-28 12:45:04'),
(83, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-28 13:52:24'),
(84, 'logout', 'User System Administrator logged out', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-28 17:47:45'),
(85, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 10:33:29'),
(86, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 10:34:00'),
(87, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '127.0.0.1', 'python-requests/2.32.5', '2025-09-30 10:43:12'),
(88, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 10:44:17'),
(89, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 12:35:10'),
(90, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 12:35:22'),
(91, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 13:35:01'),
(92, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 13:35:11'),
(93, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 13:35:41'),
(94, 'failed_login', 'Failed login attempt for user System Clerk', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 13:35:53'),
(95, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 13:35:59'),
(96, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 14:21:22'),
(97, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 14:21:30'),
(98, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 14:21:48'),
(99, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:07:59'),
(100, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:08:14'),
(101, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:12:21'),
(102, 'failed_login', 'Failed login attempt for user System Administrator', 7, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:16:19'),
(103, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:16:24'),
(104, 'failed_login', 'Failed login attempt for user System Clerk', 7, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:16:43'),
(105, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 15:16:47'),
(106, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-30 15:34:16'),
(107, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:08:32'),
(108, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:09:30'),
(109, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:09:40'),
(110, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:09:47'),
(111, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:16:04'),
(112, 'login', 'User try try try logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:16:12'),
(113, 'logout', 'User try try try logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:17:21'),
(114, 'failed_login', 'Failed login attempt for user Pending Test User', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:32:12'),
(115, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:48:23'),
(116, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:52:40'),
(117, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:52:49'),
(118, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:59:32'),
(119, 'login', 'User try try try logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 16:59:41'),
(120, 'logout', 'User try try try logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-09-30 18:24:10'),
(121, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 11:51:37'),
(122, 'logout', 'User System Administrator logged out', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 11:51:54'),
(123, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-10-01 12:48:36'),
(124, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 15:42:08'),
(125, 'logout', 'User System Clerk logged out', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 16:13:42'),
(126, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 16:22:23'),
(127, 'logout', 'User System Clerk logged out', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-01 16:22:46'),
(128, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-07 11:05:48'),
(129, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 13:51:03'),
(130, 'logout', 'User System Clerk logged out', 7, 7, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:11:20'),
(131, 'failed_login', 'Failed login attempt for user test@gmail.com', NULL, NULL, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:11:32'),
(132, 'failed_login', 'Failed login attempt for user Test User', NULL, NULL, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:11:52'),
(133, 'failed_login', 'Failed login attempt for user try try try', NULL, NULL, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:12:10'),
(134, 'failed_login', 'Failed login attempt for user try try try', NULL, NULL, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:12:22'),
(135, 'login', 'User try try try logged in successfully', 2, 2, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-07 14:12:34'),
(136, 'login', 'User try try try logged in successfully', 2, 2, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-08 12:32:07'),
(137, 'logout', 'User try try try logged out', 2, 2, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-08 12:32:28'),
(138, 'login', 'User try try try logged in successfully', 2, 2, 'user', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-10-08 12:32:35'),
(139, 'failed_login', 'Failed login attempt for user System Administrator', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:24:56'),
(140, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:25:02'),
(141, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:32:34'),
(142, 'failed_login', 'Failed login attempt for user admin@@iserbisyo.com', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:34:25'),
(143, 'failed_login', 'Failed login attempt for user admin@@iserbisyo.com', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:34:32'),
(144, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-30 22:34:39'),
(145, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-31 04:54:41'),
(146, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-10-31 04:55:32'),
(147, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:12:02'),
(148, 'failed_login', 'Failed login attempt for user try try try Jr.', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:50:18'),
(149, 'failed_login', 'Failed login attempt for user try try try Jr.', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:50:28'),
(150, 'login', 'User try try try Jr. logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:56:00'),
(151, 'logout', 'User try try try Jr. logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:56:05'),
(152, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:58:26'),
(153, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 00:58:50'),
(154, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 01:21:53'),
(155, 'login', 'User try try try Jr. logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 02:14:29'),
(156, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 02:16:55'),
(157, 'announcement_update', 'Announcement updated: New Online Barangay Certificate System Launch', 1, 22, 'announcement', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 02:35:06'),
(158, 'announcement_create', 'Announcement created: try', 1, 0, 'announcement', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-01 02:39:04'),
(159, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-02 03:26:39'),
(160, 'login', 'User try try try Jr. logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1', '2025-11-02 03:45:38'),
(161, 'logout', 'User try try try Jr. logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-02 05:01:56'),
(162, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:00:39'),
(163, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:29:35'),
(164, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:29:56'),
(165, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:32:03'),
(166, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:32:25'),
(167, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:32:44'),
(168, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:33:48'),
(169, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:35:47'),
(170, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:35:58'),
(171, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 14:38:45'),
(172, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:14:52'),
(173, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:23:11'),
(174, 'resident_rejection', 'Resident try rtyur wtwe - Reason: awdawdawd rejected', 1, 7, 'resident', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:28:20'),
(175, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:30:37'),
(176, 'failed_login', 'Failed login attempt for user System Clerk', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:30:43'),
(177, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:30:45'),
(178, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:30:58'),
(179, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:31:04'),
(180, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:45:08'),
(181, 'failed_login', 'Failed login attempt for user try try try Jr.', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:46:34'),
(182, 'failed_login', 'Failed login attempt for user try try try Jr.', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:46:39'),
(183, 'failed_login', 'Failed login attempt for user try try try Jr.', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:46:48'),
(184, 'login', 'User try try try Jr. logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:47:21'),
(185, 'logout', 'User try try try Jr. logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:50:03'),
(186, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:50:13'),
(187, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:56:54'),
(188, 'failed_login', 'Failed login attempt for user aaronojosephjimenezz@gmail.com', NULL, NULL, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:57:13'),
(189, 'login', 'User try try try Jr. logged in successfully', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', '2025-11-03 15:58:37'),
(190, 'logout', 'User try try try Jr. logged out', 2, 2, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-04 12:30:16'),
(191, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-04 12:30:23'),
(192, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:29:04'),
(193, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:38:46'),
(194, 'login', 'User System Clerk logged in successfully', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:38:51'),
(195, 'resident_registration', 'New resident awweda wadaw registered', 7, 8, 'resident', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:41:25'),
(196, 'resident_registration', 'New resident awdaw awdaw registered', 7, 9, 'resident', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:45:53'),
(197, 'logout', 'User System Clerk logged out', 7, 7, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-06 04:54:02'),
(198, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-11-08 10:24:16'),
(199, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-11-08 11:36:28'),
(200, 'login', 'User System Administrator logged in successfully', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-11-08 11:37:02'),
(201, 'logout', 'User System Administrator logged out', 1, 1, 'user', '192.168.100.85', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0', '2025-11-08 11:37:39');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `id` int(11) NOT NULL,
  `system_name` varchar(100) NOT NULL,
  `system_version` varchar(20) DEFAULT NULL,
  `system_description` text DEFAULT NULL,
  `timezone` varchar(50) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `date_format` varchar(20) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `maintenance_mode` tinyint(1) DEFAULT NULL,
  `registration_enabled` tinyint(1) DEFAULT NULL,
  `email_notifications` tinyint(1) DEFAULT NULL,
  `sms_notifications` tinyint(1) DEFAULT NULL,
  `max_file_size_mb` int(11) DEFAULT NULL,
  `allowed_file_types` text DEFAULT NULL,
  `session_timeout_minutes` int(11) DEFAULT NULL,
  `password_min_length` int(11) DEFAULT NULL,
  `password_expiry_days` int(11) DEFAULT NULL,
  `failed_login_attempts` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`id`, `system_name`, `system_version`, `system_description`, `timezone`, `language`, `date_format`, `currency`, `maintenance_mode`, `registration_enabled`, `email_notifications`, `sms_notifications`, `max_file_size_mb`, `allowed_file_types`, `session_timeout_minutes`, `password_min_length`, `password_expiry_days`, `failed_login_attempts`, `created_at`, `updated_at`) VALUES
(1, 'iSerBisyo', '1.0.0', 'Barangay Management by i-serbisyo co.', 'Asia/Manila', 'en', 'YYYY-MM-DD', 'PHP', 0, 1, 1, 0, 16, 'png,jpg,jpeg,pdf,doc,docx', 60, 8, 90, 5, '2025-09-28 15:50:53', '2025-10-01 11:51:50');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `reset_token` varchar(100) DEFAULT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `otp_code` varchar(6) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `otp_verified` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `name`, `role`, `is_active`, `created_at`, `updated_at`, `reset_token`, `reset_token_expiry`, `otp_code`, `otp_expiry`, `otp_verified`) VALUES
(1, 'admin', 'admin@gmail.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'System Administrator', 'admin', 1, '2025-09-27 18:03:45', '2025-09-28 00:49:22', NULL, NULL, NULL, NULL, 0),
(2, 'awda', 'aaronjosephjimenezz@gmail.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'try try try Jr.', 'resident', 1, '2025-09-27 18:20:20', '2025-11-03 15:58:37', 'Ljnk8aqx1W4sQJNUNTVLO50-rJN6cLaBcbY3SUG1ssU', '2025-10-08 13:25:09', NULL, NULL, 1),
(3, 'testuser123', 'test@example.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'Test User', 'resident', 1, '2025-09-27 18:23:22', '2025-11-06 04:37:58', NULL, NULL, NULL, NULL, 0),
(4, 'uniqueuser789', 'unique@example.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'Unique User', 'resident', 1, '2025-09-27 18:24:07', '2025-09-30 16:14:14', NULL, NULL, NULL, NULL, 0),
(6, 'testuser', 'testuser@gmail.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'Test User', 'resident', 1, '2025-09-28 03:19:03', '2025-09-30 16:14:14', NULL, NULL, NULL, NULL, 0),
(7, 'clerk', 'clerk@gmail.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'System Clerk', 'clerk', 1, '2025-09-30 18:38:06', '2025-09-30 18:38:06', NULL, NULL, NULL, NULL, 0),
(8, 'pending_test', 'pending@test.com', 'scrypt:32768:8:1$hBzg9xu5uiWSqD9e$6fea6c19aaaba99da25febc591b073774aceb373e1ae1e82eadc450cf0aa39a9368775e60ac3faf8e613af20a398b5daf3e662477673c391b925da801d1735bc', 'Pending Test User', 'resident', 1, '2025-09-30 16:17:29', '2025-09-30 16:17:29', NULL, NULL, NULL, NULL, 0),
(10, 'johndoe1234', 'try111@gmail.com', 'scrypt:32768:8:1$pIyHmfaFFfflQmd5$f1b49e61d8830f496024999a97adbeb625908613188d1d8ffaaf6bb1773c942b4b720f4a6bf2b27f2eb20239028808cd070221b1fdfc0175790f5d7f05b1cf32', 'try rtyur wtwe', 'resident', 0, '2025-11-03 15:22:13', '2025-11-03 15:22:13', NULL, NULL, NULL, NULL, 0);

-- --------------------------------------------------------

--
-- Structure for view `contact_messages_summary`
--
DROP TABLE IF EXISTS `contact_messages_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `contact_messages_summary`  AS SELECT `cm`.`id` AS `id`, `cm`.`name` AS `name`, `cm`.`email` AS `email`, `cm`.`subject` AS `subject`, `cm`.`status` AS `status`, `cm`.`priority` AS `priority`, `cm`.`created_at` AS `created_at`, `cm`.`responded_at` AS `responded_at`, `u`.`name` AS `responded_by_name`, CASE WHEN `cm`.`created_at` >= current_timestamp() - interval 1 day THEN 'Today' WHEN `cm`.`created_at` >= current_timestamp() - interval 7 day THEN 'This Week' WHEN `cm`.`created_at` >= current_timestamp() - interval 30 day THEN 'This Month' ELSE 'Older' END AS `time_category`, char_length(`cm`.`message`) AS `message_length` FROM (`contact_messages` `cm` left join `users` `u` on(`cm`.`responded_by` = `u`.`id`)) ORDER BY `cm`.`created_at` DESC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `announcements`
--
ALTER TABLE `announcements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_created_by` (`created_by`),
  ADD KEY `idx_updated_by` (`updated_by`),
  ADD KEY `idx_approved_by` (`approved_by`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_category` (`category`),
  ADD KEY `idx_priority` (`priority`),
  ADD KEY `idx_published_at` (`published_at`),
  ADD KEY `idx_expiry_date` (`expiry_date`),
  ADD KEY `idx_slug` (`slug`);

--
-- Indexes for table `certificates`
--
ALTER TABLE `certificates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `certificate_number` (`certificate_number`),
  ADD KEY `resident_id` (`resident_id`),
  ADD KEY `processed_by` (`processed_by`);

--
-- Indexes for table `certificate_types`
--
ALTER TABLE `certificate_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_contact_status` (`status`),
  ADD KEY `idx_contact_priority` (`priority`),
  ADD KEY `idx_contact_created_at` (`created_at`),
  ADD KEY `idx_contact_email` (`email`),
  ADD KEY `idx_contact_responded_by` (`responded_by`),
  ADD KEY `idx_contact_status_created` (`status`,`created_at`),
  ADD KEY `idx_contact_priority_status` (`priority`,`status`);

--
-- Indexes for table `officials`
--
ALTER TABLE `officials`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_payments_payment_number` (`payment_number`),
  ADD UNIQUE KEY `ix_payments_reference_number` (`reference_number`),
  ADD UNIQUE KEY `ix_payments_receipt_number` (`receipt_number`),
  ADD KEY `resident_id` (`resident_id`),
  ADD KEY `certificate_id` (`certificate_id`),
  ADD KEY `receipt_issued_by` (`receipt_issued_by`),
  ADD KEY `processed_by` (`processed_by`),
  ADD KEY `refunded_by` (`refunded_by`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `ix_payments_transaction_id` (`transaction_id`);

--
-- Indexes for table `purok_info`
--
ALTER TABLE `purok_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_purok_name` (`name`),
  ADD KEY `idx_type` (`type`),
  ADD KEY `idx_active` (`is_active`),
  ADD KEY `idx_barangay` (`barangay_id`),
  ADD KEY `idx_created_by` (`created_by`),
  ADD KEY `idx_updated_by` (`updated_by`);

--
-- Indexes for table `residents`
--
ALTER TABLE `residents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_residents_sitio` (`sitio_id`);

--
-- Indexes for table `system_activities`
--
ALTER TABLE `system_activities`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD KEY `idx_users_otp_code` (`otp_code`),
  ADD KEY `idx_users_otp_expiry` (`otp_expiry`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `announcements`
--
ALTER TABLE `announcements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `certificates`
--
ALTER TABLE `certificates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `certificate_types`
--
ALTER TABLE `certificate_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `officials`
--
ALTER TABLE `officials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `purok_info`
--
ALTER TABLE `purok_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `residents`
--
ALTER TABLE `residents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `system_activities`
--
ALTER TABLE `system_activities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `announcements`
--
ALTER TABLE `announcements`
  ADD CONSTRAINT `fk_announcements_approved_by` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_announcements_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_announcements_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `certificates`
--
ALTER TABLE `certificates`
  ADD CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`resident_id`) REFERENCES `residents` (`id`),
  ADD CONSTRAINT `certificates_ibfk_2` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD CONSTRAINT `fk_contact_responded_by` FOREIGN KEY (`responded_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`resident_id`) REFERENCES `residents` (`id`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`certificate_id`) REFERENCES `certificates` (`id`),
  ADD CONSTRAINT `payments_ibfk_3` FOREIGN KEY (`receipt_issued_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_4` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_5` FOREIGN KEY (`refunded_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_6` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_7` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `residents`
--
ALTER TABLE `residents`
  ADD CONSTRAINT `fk_residents_sitio` FOREIGN KEY (`sitio_id`) REFERENCES `purok_info` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `residents_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `system_activities`
--
ALTER TABLE `system_activities`
  ADD CONSTRAINT `system_activities_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
