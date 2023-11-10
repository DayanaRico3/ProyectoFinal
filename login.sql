-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-11-2023 a las 22:25:06
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `login`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lugares`
--

CREATE TABLE `lugares` (
  `id_lugar` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `latitud` decimal(10,6) DEFAULT NULL,
  `longitud` decimal(10,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `lugares`
--

INSERT INTO `lugares` (`id_lugar`, `nombre`, `latitud`, `longitud`) VALUES
(1, 'UDI', -73.857704, 7.062373),
(2, 'UDI', 7.062366, -73.857755),
(4, 'Cancha la Libertad', 7.077800, -73.853000),
(5, 'Cristo Petrolero', 7.063030, -73.869260),
(6, 'Planada del cerro', 7.042330, -73.840500),
(7, 'Estadio Daniel Villa', 7.073890, -73.864490),
(8, 'El muelle', 7.059680, -73.875490),
(9, 'Puente de Yondo', 7.080170, -73.895540),
(10, 'El Reten', 7.042830, -73.826380),
(11, 'Cancha Aguas Clara', 7.071500, -73.860800);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mediciones`
--

CREATE TABLE `mediciones` (
  `id_mediciones` int(11) NOT NULL,
  `puntodemed` varchar(50) NOT NULL,
  `medicion` float DEFAULT NULL,
  `Indiceuv` int(11) NOT NULL,
  `fecha_tomada` datetime DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `id_lugar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mediciones`
--

INSERT INTO `mediciones` (`id_mediciones`, `puntodemed`, `medicion`, `Indiceuv`, `fecha_tomada`, `usuario_id`, `id_lugar`) VALUES
(4, 'Udi', 35, 6, '2023-10-09 11:16:49', 4, 1),
(6, 'floresta', 33, 13, '2023-10-11 13:11:16', 4, 4),
(14, 'Cristo Petrolero', 34, 13, '2023-09-13 11:50:00', 4, 5),
(15, 'cancha la libertad', 35, 8, '2023-08-31 16:50:01', 31, 4),
(16, 'Aguas clara', 39, 10, '2023-09-01 16:50:25', 31, 11),
(20, 'Planada del cerro', 38, 6, '2023-09-02 11:34:24', 31, 6),
(21, 'El muelle', 33, 11, '2023-09-03 16:08:23', 4, 8),
(22, 'Puente de yondo', 34, 13, '2023-09-04 16:09:10', 31, 9),
(23, 'el reten', 37, 13, '2023-09-05 16:09:10', 31, 10),
(24, 'Cristo petrolero', 36, 8, '2023-09-08 16:19:05', 31, 5),
(25, 'UDI', 34, 13, '2023-09-09 16:19:47', 4, 1),
(26, 'Cancha la Libertad', 36, 12, '2023-09-11 16:19:47', 31, 4),
(27, 'UDI', 34, 13, '2023-09-09 16:19:47', 4, 1),
(28, 'Cancha la Libertad', 36, 12, '2023-09-11 13:19:47', 31, 4),
(29, 'Estadio daniel villa zapata', 33, 8, '2023-09-13 11:22:44', 31, 7),
(30, 'Cancha Aguas clara', 35, 7, '2023-11-15 11:22:44', 31, 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil`
--

CREATE TABLE `perfil` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfil`
--

INSERT INTO `perfil` (`id`, `usuario_id`, `nombre`, `correo`, `contraseña`) VALUES
(15, 17, 'Dayana Rico', 'daya0@gmail.com', NULL),
(16, 18, 'Felipe', 'felipe@gmail.com', NULL),
(17, 19, 'user3', 'user3@gmail.com', '1111'),
(19, 22, 'dayana rico', 'dayana23@gmail.com', '123456'),
(22, 24, 'Dayana', 'Daya0@gmail.com', '123456'),
(25, 26, 'Usario', 'user8@gmail.com', '123456'),
(27, 31, 'Harol Gelvez benitez', 'Harol2@gmail.com', '0000'),
(28, 32, 'Eder jair', 'Eder1@gmail.com', '1111'),
(29, NULL, 'Lizeth Rico', 'Lizeth23@gmail.com', '1111');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `descripcion`) VALUES
(1, 'Admin'),
(2, 'User');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Id` int(11) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `activo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Id`, `correo`, `password`, `id_rol`, `nombre`, `activo`) VALUES
(4, 'Rico1@gmail.com', '0000', 1, 'Ricoo', 1),
(17, 'daya0@gmail.com', '1111', 2, 'Dayana Rico', 1),
(18, 'felipe@gmail.com', '12345', 2, 'Felipe', 0),
(19, 'user3@gmail.com', '1111', 1, 'user3', 1),
(22, 'dayana23@gmail.com', '123456', 1, 'dayana rico', 1),
(24, 'Daya0@gmail.com', '123456', 1, 'Dayana', 1),
(26, 'user8@gmail.com', '123456', 2, 'Usuarioo', 1),
(31, 'Harol2@gmail.com', '1111', 1, 'Harol Gelvez benitez', 1),
(32, 'Eder1@gmail.com', '1111', 2, 'Eder Agamez', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `lugares`
--
ALTER TABLE `lugares`
  ADD PRIMARY KEY (`id_lugar`);

--
-- Indices de la tabla `mediciones`
--
ALTER TABLE `mediciones`
  ADD PRIMARY KEY (`id_mediciones`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `lugar_id` (`id_lugar`);

--
-- Indices de la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD PRIMARY KEY (`id`),
  ADD KEY `perfil_ibfk_1` (`usuario_id`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `lugares`
--
ALTER TABLE `lugares`
  MODIFY `id_lugar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `mediciones`
--
ALTER TABLE `mediciones`
  MODIFY `id_mediciones` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `perfil`
--
ALTER TABLE `perfil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `mediciones`
--
ALTER TABLE `mediciones`
  ADD CONSTRAINT `mediciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`Id`),
  ADD CONSTRAINT `mediciones_ibfk_2` FOREIGN KEY (`id_lugar`) REFERENCES `lugares` (`id_lugar`);

--
-- Filtros para la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD CONSTRAINT `perfil_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`Id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
