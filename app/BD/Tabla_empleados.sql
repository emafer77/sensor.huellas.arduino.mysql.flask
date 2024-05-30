
CREATE TABLE `registro_huella` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `sexo` varchar(10) DEFAULT NULL, -- Asume que el sexo será un varchar, ajusta el tamaño según sea necesario
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;