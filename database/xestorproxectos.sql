-- Adminer 4.8.1 MySQL 5.7.23 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `asignacions`;
CREATE TABLE `asignacions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persoa_id` int(11) NOT NULL,
  `tarefa_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persoa_id` (`persoa_id`),
  KEY `tarefa_id` (`tarefa_id`),
  CONSTRAINT `asignacions_ibfk_1` FOREIGN KEY (`persoa_id`) REFERENCES `persoas` (`id`),
  CONSTRAINT `asignacions_ibfk_2` FOREIGN KEY (`tarefa_id`) REFERENCES `tarefas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


DROP TABLE IF EXISTS `intervencions`;
CREATE TABLE `intervencions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persoa_id` int(11) NOT NULL,
  `tarefa_id` int(11) NOT NULL,
  `inicio` datetime NOT NULL,
  `fin` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persoa_id` (`persoa_id`),
  KEY `tarefa_id` (`tarefa_id`),
  CONSTRAINT `intervencions_ibfk_1` FOREIGN KEY (`persoa_id`) REFERENCES `persoas` (`id`),
  CONSTRAINT `intervencions_ibfk_2` FOREIGN KEY (`tarefa_id`) REFERENCES `tarefas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


DROP TABLE IF EXISTS `participacion`;
CREATE TABLE `participacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persoa_id` int(11) NOT NULL,
  `proxecto_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persoa_id` (`persoa_id`),
  KEY `proxecto_id` (`proxecto_id`),
  CONSTRAINT `participacion_ibfk_1` FOREIGN KEY (`persoa_id`) REFERENCES `persoas` (`id`),
  CONSTRAINT `participacion_ibfk_2` FOREIGN KEY (`proxecto_id`) REFERENCES `proxectos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


DROP TABLE IF EXISTS `persoas`;
CREATE TABLE `persoas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` char(15) COLLATE utf8mb4_bin NOT NULL,
  `nome` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


DROP TABLE IF EXISTS `proxectos`;
CREATE TABLE `proxectos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `descricion` text COLLATE utf8mb4_bin NOT NULL,
  `inicio` date NOT NULL,
  `fin` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


DROP TABLE IF EXISTS `tarefas`;
CREATE TABLE `tarefas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `inicio` date NOT NULL,
  `fin` date DEFAULT NULL,
  `vencimento` date NOT NULL,
  `proxecto_id` int(11) NOT NULL,
  `tarefa_superior_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `proxecto_id` (`proxecto_id`),
  KEY `tarefa_superior_id` (`tarefa_superior_id`),
  CONSTRAINT `tarefas_ibfk_1` FOREIGN KEY (`proxecto_id`) REFERENCES `proxectos` (`id`),
  CONSTRAINT `tarefas_ibfk_2` FOREIGN KEY (`tarefa_superior_id`) REFERENCES `tarefas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


-- 2022-02-02 19:39:30
