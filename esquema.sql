-- Estructura de tabla para: Rol
DROP TABLE IF EXISTS `rol`;
CREATE TABLE IF NOT EXISTS `rol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- Estructura de tabla para: Usuario
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contrasena` varchar(20) NOT NULL,
  `estado` boolean NOT NULL,
  `token` varchar(255) NULL,
  `estado_token` boolean NULL,
  `nombre` varchar(60) NOT NULL,
  `ape_completo` varchar(60) NOT NULL,
  `fecha_nac` date NOT NULL,
  `dni` varchar(8) NOT NULL,
  `sexo` boolean NOT NULL,
  `direccion` varchar(100) NULL,
  `telefono` varchar(15) NULL,
  `foto` varchar(255) NULL,
  `rol_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Seguro_Dental
DROP TABLE IF EXISTS `seguro_dental`;
CREATE TABLE IF NOT EXISTS `seguro_dental` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_compania` varchar(50) NOT NULL,
  `tipo_cobertura` varchar(30) NOT NULL,
  `telefono_compania` varchar(15) NOT NULL,
  `paciente_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`paciente_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Especialidad
DROP TABLE IF EXISTS `especialidad`;
CREATE TABLE IF NOT EXISTS `especialidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Atencion
DROP TABLE IF EXISTS `atencion`;
CREATE TABLE IF NOT EXISTS `atencion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `odontologo_id` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `motivo_consulta` varchar(150) NOT NULL,
  `diagnostico` varchar(100) NOT NULL,
  `anotacion` varchar(100) NULL,
  `costo` decimal(5,2) NOT NULL,
  `estado` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`paciente_id`) REFERENCES `usuario` (`id`),
  FOREIGN KEY (`odontologo_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Detalle_Especialidad
DROP TABLE IF EXISTS `detalle_especialidad`;
CREATE TABLE IF NOT EXISTS `detalle_especialidad` (
  `odontologo_id` int NOT NULL,
  `especialidad_id` int NOT NULL,
  PRIMARY KEY (`odontologo_id`, `especialidad_id`),
  FOREIGN KEY (`odontologo_id`) REFERENCES `usuario` (`id`),
  FOREIGN KEY (`especialidad_id`) REFERENCES `especialidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Tratamiento  
DROP TABLE IF EXISTS `tratamiento`;
CREATE TABLE IF NOT EXISTS `tratamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `costo` decimal(6,2) NOT NULL,
  `atencion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`atencion_id`) REFERENCES `atencion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para: Pago
DROP TABLE IF EXISTS `pago`;
CREATE TABLE IF NOT EXISTS `pago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `monto` decimal(5,2) NOT NULL,
  `estado` char(1) NOT NULL,
  `atencion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`atencion_id`) REFERENCES `atencion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

