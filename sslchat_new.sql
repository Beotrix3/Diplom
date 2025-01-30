-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Окт 22 2024 г., 17:03
-- Версия сервера: 8.3.0
-- Версия PHP: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `sslchat`
--

-- --------------------------------------------------------

--
-- Структура таблицы `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `body` varbinary(300) NOT NULL,
  `msg_by` int NOT NULL,
  `msg_to` int NOT NULL,
  `msg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `messages`
--

INSERT INTO `messages` (`id`, `body`, `msg_by`, `msg_to`, `msg_time`) VALUES
(188, 0x7d730f88be5afc8cdcb57ef2e253a3740a9518a339bee9fb6cbbca8dbc8c1dda, 13, 14, '2024-10-21 16:24:29'),
(187, 0x495913f41ba1a1d4e1dd7dd69c0beff16ecb31f235b10b1234d9c0f64774e50e, 14, 13, '2024-10-21 16:24:12');

-- --------------------------------------------------------

--
-- Структура таблицы `secret_key`
--

DROP TABLE IF EXISTS `secret_key`;
CREATE TABLE IF NOT EXISTS `secret_key` (
  `secret_key` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `secret_key`
--

INSERT INTO `secret_key` (`secret_key`) VALUES
('988b2b5b6c97de55d909972d988d46c40e95d0556faa9aae5beb642c1c77f6f444daf5c3a9b757f32cd42632b0127b5a9e17a75cf96540ae34a220d7897c6b88d6cb7752ac5b8127ceefd414a41555ad5c9c3d0b9a3edf309904179e68ae5d7bc15fb792567452b20b4d5aaf9743ebb8d0338f0b6ff1d563353a7ff07e331ce721aa3232b99165716561f959a73c81920a5203416b351af7d2f8603a8b7823483188dd7f0d470ec589756bd6199ae94237779607c1260dc871d2b3421f6841d829ad5a0c3f42a952c84430bf296bd12ae00beb07b8a64b8388a8e38dc2c176ac99e50c8cb64facdca3a02d90acfb219107f2b1de74f5f173d2e1e83cb7b90be4');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `reg_time`, `online`) VALUES
(13, 'user', 'user@mail.ru', 'username', '$5$rounds=535000$VW.fQofrQcPMoHhB$asHelbe9NZAaj.MI3tb1YpKQHfGz.thUBGBElbTT9UC', '2024-10-18 15:14:24', '0'),
(14, 'name2', 'name2@mail.ru', 'username2', '$5$rounds=535000$9zANuGjaW7pVBhAW$z7iTJc.U.8/3Ind.lYpyr1.ZTKAJvSuJEog0OE75GHA', '2024-10-18 15:14:54', '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
