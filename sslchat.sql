-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Ноя 04 2024 г., 13:57
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
-- Структура таблицы `admin_code`
--

DROP TABLE IF EXISTS `admin_code`;
CREATE TABLE IF NOT EXISTS `admin_code` (
  `admin_code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `admin_code`
--

INSERT INTO `admin_code` (`admin_code`) VALUES
('fb656fee878f875a7b3fea9eb693982563c4abb66eec9a482de282e27bfa6b99');

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
) ENGINE=MyISAM AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `messages`
--

INSERT INTO `messages` (`id`, `body`, `msg_by`, `msg_to`, `msg_time`) VALUES
(188, 0x7d730f88be5afc8cdcb57ef2e253a3740a9518a339bee9fb6cbbca8dbc8c1dda, 13, 14, '2024-10-21 16:24:29'),
(187, 0x495913f41ba1a1d4e1dd7dd69c0beff16ecb31f235b10b1234d9c0f64774e50e, 14, 13, '2024-10-21 16:24:12'),
(189, 0x7e3776b7bb1edf8458e9f1146be2371fa7234048575d0a07a6cfde8904fd417e, 14, 20, '2024-11-04 10:40:03'),
(190, 0x5cbc4a4f84f3d9a533a79760559ba0db53315f32ab7671c1188ef0f9fd59594a3d8779659177e71ef06069addd325d6c, 14, 20, '2024-11-04 10:40:11'),
(191, 0x2f2ac3d1616243aedfcb2743f840c7954bdf1ab176e7492cab949468981f8eced28b21ba42a550689d9ddd0c6f739d7a, 13, 20, '2024-11-04 10:40:25'),
(192, 0x22982a5bfc39740145666cca2d8fd007150ee7b86cf6cbd3f845805ebbf9ee9b00016c4d183458ae0c815babefc592c8, 13, 20, '2024-11-04 10:40:34'),
(193, 0x2b94c49cae0e6c7810a9069435ddfcee1fd7d614a7ecf2265395e9cc1fb8e0edde5734075d09a447336fcc18e0b382d2, 20, 21, '2024-11-04 10:46:49'),
(194, 0xfc09dfbaf9554941a100f98fe209cb059d97f1e2ee68f3a374a99ba81b52c8b33e00c71d04f0e65292517b3c07d3ce3b, 21, 20, '2024-11-04 10:47:02');

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
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `reg_time`, `online`) VALUES
(20, 'Администратор', 'grebnev-alexey@mail.ru', 'Администратор', '$5$rounds=535000$qSt1GcocfSNNm16x$rCkTx2XoUhNN3tSwXi2ItyInCY9RRpKsudv74upYsS4', '2024-11-04 10:38:51', '0'),
(21, 'Тест2', 'beotrix3@mail.ru', 'Тест2', '$5$rounds=535000$laXrc.M49BKLpdKo$Ggvy8X..RhAIypmDgzXkGK9DNrMzQY8gskabDliwns/', '2024-11-04 10:45:48', '0');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
