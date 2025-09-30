-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.41 - MySQL Community Server - GPL
-- Server OS:                    Linux
-- HeidiSQL Version:             12.4.0.6659
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for task_management
CREATE DATABASE IF NOT EXISTS `task_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `task_management`;

-- Dumping structure for table task_management.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text,
  `status` enum('PENDING','IN_PROGRESS','COMPLETED','CANCELLED') NOT NULL,
  `priority` enum('LOW','MEDIUM','HIGH','URGENT') NOT NULL,
  `created_by` varchar(100) NOT NULL,
  `assigned_to` varchar(100) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_tasks_status` (`status`),
  KEY `ix_tasks_id` (`id`),
  KEY `ix_tasks_title` (`title`),
  KEY `ix_tasks_user_id` (`user_id`),
  CONSTRAINT `fk_tasks_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table task_management.tasks: ~0 rows (approximately)
INSERT INTO `tasks` (`id`, `title`, `description`, `status`, `priority`, `created_by`, `assigned_to`, `user_id`, `created_at`, `updated_at`, `due_date`, `completed_at`, `is_deleted`) VALUES
	(1, 'Setup Database Schema', 'Create and configure the database schema for the new project', 'COMPLETED', 'HIGH', 'john_doe', 'bob_wilson', 3, '2025-09-29 06:24:06', NULL, '2024-01-15 17:00:00', NULL, 0),
	(2, 'Code Review Process', 'Establish code review guidelines and process', 'IN_PROGRESS', 'MEDIUM', 'john_doe', 'jane_smith', 2, '2025-09-29 06:24:06', NULL, '2024-01-20 12:00:00', NULL, 0),
	(3, 'Security Audit', 'Conduct comprehensive security audit', 'PENDING', 'URGENT', 'john_doe', 'alice_brown', 4, '2025-09-29 06:24:06', NULL, '2024-01-25 09:00:00', NULL, 0),
	(4, 'Team Meeting Preparation', 'Prepare agenda and materials for weekly team meeting', 'COMPLETED', 'MEDIUM', 'jane_smith', 'jane_smith', 2, '2025-09-29 06:24:06', NULL, '2024-01-10 14:00:00', NULL, 0),
	(5, 'Performance Reviews', 'Complete Q4 performance reviews for team members', 'IN_PROGRESS', 'HIGH', 'jane_smith', 'jane_smith', 2, '2025-09-29 06:24:06', NULL, '2024-01-30 17:00:00', NULL, 0),
	(6, 'Budget Planning', 'Plan budget for next quarter', 'PENDING', 'HIGH', 'jane_smith', 'john_doe', 1, '2025-09-29 06:24:06', NULL, '2024-02-05 16:00:00', NULL, 0),
	(7, 'API Development', 'Develop REST API endpoints for user management', 'IN_PROGRESS', 'HIGH', 'bob_wilson', 'bob_wilson', 3, '2025-09-29 06:24:06', NULL, '2024-01-22 18:00:00', NULL, 0),
	(8, 'Unit Testing', 'Write comprehensive unit tests for new features', 'PENDING', 'MEDIUM', 'bob_wilson', 'alice_brown', 4, '2025-09-29 06:24:06', NULL, '2024-01-28 15:00:00', NULL, 0),
	(9, 'UI/UX Design', 'Design user interface for dashboard', 'IN_PROGRESS', 'MEDIUM', 'alice_brown', 'alice_brown', 4, '2025-09-29 06:24:06', NULL, '2024-01-26 12:00:00', NULL, 0),
	(10, 'Documentation Update', 'Update user documentation with new features', 'PENDING', 'LOW', 'alice_brown', 'mike_davis', 5, '2025-09-29 06:24:06', NULL, '2024-02-01 10:00:00', NULL, 0),
	(11, 'Legacy System Migration', 'Migrate data from legacy system', 'CANCELLED', 'LOW', 'mike_davis', 'bob_wilson', 3, '2025-09-29 06:24:06', NULL, '2024-01-12 16:00:00', NULL, 0);

-- Dumping structure for table task_management.task_details
CREATE TABLE IF NOT EXISTS `task_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `detail_type` enum('COMMENT','ATTACHMENT','LOG','NOTE','CHECKLIST_ITEM') NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `content` text,
  `file_path` varchar(500) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_size` bigint DEFAULT NULL,
  `mime_type` varchar(100) DEFAULT NULL,
  `metadata` json DEFAULT NULL,
  `created_by` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `order_index` int DEFAULT NULL,
  `is_completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_task_details_task_id` (`task_id`),
  KEY `ix_task_details_detail_type` (`detail_type`),
  KEY `ix_task_details_created_by` (`created_by`),
  KEY `ix_task_details_created_at` (`created_at`),
  KEY `ix_task_details_id` (`id`),
  CONSTRAINT `fk_task_details_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table task_management.task_details: ~0 rows (approximately)
INSERT INTO `task_details` (`id`, `task_id`, `detail_type`, `title`, `content`, `file_path`, `file_name`, `file_size`, `mime_type`, `metadata`, `created_by`, `created_at`, `updated_at`, `is_deleted`, `order_index`, `is_completed`) VALUES
	(1, 1, 'COMMENT', NULL, 'Started working on the database schema design', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(2, 1, 'COMMENT', NULL, 'Tables created successfully, running initial tests', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(3, 1, 'ATTACHMENT', 'Database Schema Diagram', 'Attached the ER diagram for review', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(4, 1, 'LOG', NULL, 'Task completed successfully', NULL, NULL, NULL, NULL, NULL, 'john_doe', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(5, 2, 'CHECKLIST_ITEM', 'Create review guidelines document', 'Draft the initial guidelines', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 1, 1),
	(6, 2, 'CHECKLIST_ITEM', 'Setup review tools', 'Configure GitHub PR templates', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 2, 1),
	(7, 2, 'CHECKLIST_ITEM', 'Train team on process', 'Conduct training session', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 3, 0),
	(8, 2, 'COMMENT', NULL, 'Guidelines document is ready for review', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(9, 3, 'NOTE', 'Audit Scope', 'Focus on authentication, authorization, and data encryption', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(10, 3, 'CHECKLIST_ITEM', 'Review authentication system', 'Check JWT implementation', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, 1, 0),
	(11, 3, 'CHECKLIST_ITEM', 'Check database security', 'Review SQL injection prevention', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, 2, 0),
	(12, 3, 'CHECKLIST_ITEM', 'Audit API endpoints', 'Test all endpoints for vulnerabilities', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, 3, 0),
	(13, 4, 'COMMENT', NULL, 'Agenda prepared and sent to team', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(14, 4, 'ATTACHMENT', 'Meeting Minutes', 'Minutes from the last meeting', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(15, 4, 'LOG', NULL, 'Meeting completed successfully', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(16, 5, 'CHECKLIST_ITEM', 'Review John Doe', 'Complete performance review', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 1, 1),
	(17, 5, 'CHECKLIST_ITEM', 'Review Bob Wilson', 'Complete performance review', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 2, 0),
	(18, 5, 'CHECKLIST_ITEM', 'Review Alice Brown', 'Complete performance review', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, 3, 0),
	(19, 5, 'COMMENT', NULL, 'Started with individual review sessions', NULL, NULL, NULL, NULL, NULL, 'jane_smith', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(20, 7, 'COMMENT', NULL, 'Started with user authentication endpoints', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(21, 7, 'COMMENT', NULL, 'Implemented CRUD operations for users', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(22, 7, 'NOTE', 'Technical Notes', 'Using FastAPI with SQLAlchemy ORM', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(23, 7, 'ATTACHMENT', 'API Documentation', 'Swagger documentation exported', NULL, NULL, NULL, NULL, NULL, 'bob_wilson', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(24, 9, 'COMMENT', NULL, 'Created initial wireframes for dashboard', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(25, 9, 'ATTACHMENT', 'Design Mockups', 'Figma mockups for review', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, NULL, NULL),
	(26, 9, 'CHECKLIST_ITEM', 'Create color palette', 'Define brand colors', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, 1, 1),
	(27, 9, 'CHECKLIST_ITEM', 'Design responsive layout', 'Mobile-first approach', NULL, NULL, NULL, NULL, NULL, 'alice_brown', '2025-09-29 06:24:36', NULL, 0, 2, 0);

-- Dumping structure for table task_management.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('ADMIN','MANAGER','USER','GUEST') NOT NULL,
  `status` enum('ACTIVE','INACTIVE','SUSPENDED') NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table task_management.users: ~0 rows (approximately)
INSERT INTO `users` (`id`, `username`, `email`, `full_name`, `password_hash`, `role`, `status`, `created_at`, `updated_at`, `last_login`, `is_deleted`, `email_verified`) VALUES
	(1, 'john_doe', 'john.doe@company.com', 'John Doe', '$2b$12$hashed_password_here', 'ADMIN', 'ACTIVE', '2025-09-29 06:22:35', NULL, NULL, 0, 1),
	(2, 'jane_smith', 'jane.smith@company.com', 'Jane Smith', '$2b$12$hashed_password_here', 'MANAGER', 'ACTIVE', '2025-09-29 06:22:35', NULL, NULL, 0, 1),
	(3, 'bob_wilson', 'bob.wilson@company.com', 'Bob Wilson', '$2b$12$hashed_password_here', 'USER', 'ACTIVE', '2025-09-29 06:22:35', NULL, NULL, 0, 1),
	(4, 'alice_brown', 'alice.brown@company.com', 'Alice Brown', '$2b$12$hashed_password_here', 'USER', 'ACTIVE', '2025-09-29 06:22:35', NULL, NULL, 0, 1),
	(5, 'mike_davis', 'mike.davis@company.com', 'Mike Davis', '$2b$12$hashed_password_here', 'USER', 'INACTIVE', '2025-09-29 06:22:35', NULL, NULL, 0, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
