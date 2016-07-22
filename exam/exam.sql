CREATE DATABASE IF NOT EXISTS examdb;

USE examdb;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `alias` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `birthdate` date,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `quotes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quoted_by` varchar(200) DEFAULT NULL,
  `message` varchar(300) DEFAULT NULL,
  `poster_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `favorites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quote_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);
