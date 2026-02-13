
SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- Access denied for user &#039;umsnh&#039;@&#039;%&#039; to database &#039;umsnh&#039;
SET NAMES utf8mb4;

CREATE TABLE `Administrativos` (
  `id_administrativo` int unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario` int unsigned NOT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_administrativo`),
  KEY `Administrativos_Usuarios_FK` (`id_usuario`),
  CONSTRAINT `Administrativos_Usuarios_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Administrativos
INSERT INTO `Administrativos` (`id_usuario`, `departamento`) VALUES
(4, 'Recursos Humanos'); -- Laura (ID 4)

CREATE TABLE `Bibliotecas` (
  `id_biblioteca` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `ubicacion` varchar(250) NOT NULL,
  PRIMARY KEY (`id_biblioteca`),
  UNIQUE KEY `Bibliotecas_UNIQUE_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde contendra las bibliotecas de la universidad';

INSERT INTO `Bibliotecas` (`id_biblioteca`, `nombre`, `ubicacion`) VALUES
(1,	'Biblioteca Central',	'Edificio Principal'),
(2,	'Biblioteca de Ingeniería',	'Edificio B');

CREATE TABLE `Carreras` (
  `id_carrera` int unsigned NOT NULL AUTO_INCREMENT,
  `carrera` varchar(120) NOT NULL,
  `facultad` varchar(250) NOT NULL,
  PRIMARY KEY (`id_carrera`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla para las carreras de la universidad';

INSERT INTO `Carreras` (`id_carrera`, `carrera`, `facultad`) VALUES
(1,	'Ingeniería Eléctrica',	'Facultad de Ingeniería Eléctrica'),
(2,	'Ingeniería Electrónica',	'Facultad de Ingeniería Eléctrica'),
(3,	'Ingeniería en Computación',	'Facultad de Ingeniería Eléctrica');

CREATE TABLE `Catalogo` (
  `id_catalogo` int unsigned NOT NULL AUTO_INCREMENT,
  `tipo` enum('herramienta','libro','equipo') NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `autor` varchar(200) DEFAULT NULL,
  `isbn` varchar(30) DEFAULT NULL COMMENT 'Se trata de un código numérico de 13 dígitos que identifica de forma única cada edición de un libro publicado',
  `descripcion` text,
  PRIMARY KEY (`id_catalogo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde contendra el catalogo es decir libro,herramient, equipo';

INSERT INTO `Catalogo` (`id_catalogo`, `tipo`, `nombre`, `autor`, `isbn`, `descripcion`) VALUES
(1,	'libro',	'Cien años de soledad',	'Gabriel García Márquez',	'9780307474728',	'Novela clásica del realismo mágico'),
(2,	'libro',	'Clean Code',	'Robert C. Martin',	'9780132350884',	'Principios de código limpio'),
(3,	'herramienta',	'Multímetro Digital',	NULL,	NULL,	'Rango 0-1000V'),
(4,	'herramienta',	'Microscopio Óptico',	NULL,	NULL,	'Aumento 1000x'),
(5,	'libro',	'Cien años de soledad',	'Gabriel García Márquez',	'9780307474728',	'Novela clásica del realismo mágico'),
(6,	'libro',	'Clean Code',	'Robert C. Martin',	'9780132350884',	'Principios de código limpio'),
(7,	'herramienta',	'Multímetro Digital',	NULL,	NULL,	'Rango 0-1000V'),
(8,	'herramienta',	'Microscopio Óptico',	NULL,	NULL,	'Aumento 1000x'),
(9,	'libro',	'Cien años de soledad',	'Gabriel García Márquez',	'9780307474728',	'Novela clásica del realismo mágico'),
(10,	'libro',	'Clean Code',	'Robert C. Martin',	'9780132350884',	'Principios de código limpio'),
(11,	'herramienta',	'Multímetro Digital',	NULL,	NULL,	'Rango 0-1000V'),
(12,	'herramienta',	'Microscopio Óptico',	NULL,	NULL,	'Aumento 1000x'),
(13,	'libro',	'Cien años de soledad',	'Gabriel García Márquez',	'9780307474728',	'Novela clásica del realismo mágico'),
(14,	'libro',	'Clean Code',	'Robert C. Martin',	'9780132350884',	'Principios de código limpio'),
(15,	'herramienta',	'Multímetro Digital',	NULL,	NULL,	'Rango 0-1000V'),
(16,	'herramienta',	'Microscopio Óptico',	NULL,	NULL,	'Aumento 1000x');

CREATE TABLE `Ciclos` (
  `id_ciclo` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico de la tabla',
  `ciclo` varchar(16) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  PRIMARY KEY (`id_ciclo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde estaran los ciclos escolares';

INSERT INTO `Ciclos` (`id_ciclo`, `ciclo`, `fecha_inicio`, `fecha_final`) VALUES
(1,	'2023-2024',	'2023-08-14',	'2024-02-05'),
(2,	'2024-2024',	'2024-02-06',	'2024-08-11'),
(3,	'2024-2025',	'2024-08-12',	'2025-02-03'),
(4,	'2025-2025',	'2025-02-04',	'2025-08-10');

CREATE TABLE `Ejemplares` (
  `id_ejemplar` int unsigned NOT NULL AUTO_INCREMENT,
  `id_catalogo` int unsigned NOT NULL,
  `codigo_inventario` varchar(50) NOT NULL,
  `ubicacion` enum('laboratorio','biblioteca') NOT NULL,
  `id_laboratorio` int unsigned DEFAULT NULL,
  `id_biblioteca` int unsigned DEFAULT NULL,
  `estado` enum('no_disponible','disponible','prestado','mantenimiento','perdido') DEFAULT 'disponible',
  PRIMARY KEY (`id_ejemplar`),
  UNIQUE KEY `Ejemplares_UNIQUE_codigo_inventario` (`codigo_inventario`),
  KEY `Ejemplares_Catalogo_FK` (`id_catalogo`),
  KEY `Ejemplares_Laboratorios_FK` (`id_laboratorio`),
  KEY `Ejemplares_Bibliotecas_FK` (`id_biblioteca`),
  CONSTRAINT `Ejemplares_Bibliotecas_FK` FOREIGN KEY (`id_biblioteca`) REFERENCES `Bibliotecas` (`id_biblioteca`),
  CONSTRAINT `Ejemplares_Catalogo_FK` FOREIGN KEY (`id_catalogo`) REFERENCES `Catalogo` (`id_catalogo`),
  CONSTRAINT `Ejemplares_Laboratorios_FK` FOREIGN KEY (`id_laboratorio`) REFERENCES `Laboratorios` (`id_laboratorio`),
  CONSTRAINT `Ejemplares_CHECK_ubicacion` CHECK ((((`ubicacion` = _utf8mb4'laboratorio') and (`id_laboratorio` is not null)) or ((`ubicacion` = _utf8mb4'biblioteca') and (`id_biblioteca` is not null))))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde se encontraran los ejemplares  del catalogo, es decir cada herramienta libro';

INSERT INTO `Ejemplares` (`id_catalogo`, `codigo_inventario`, `ubicacion`, `id_laboratorio`, `id_biblioteca`, `estado`) VALUES
(1, 'LIB-1001', 'biblioteca', NULL, 1, 'disponible'),
(3, 'HER-3001', 'laboratorio', 2, NULL, 'disponible');


CREATE TABLE `Estudiantes` (
  `id_estudiante` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'identificador unico para la tabla',
  `id_usuario` int unsigned NOT NULL,
  `id_carrera` int unsigned NOT NULL,
  PRIMARY KEY (`id_estudiante`),
  UNIQUE KEY `Estudiantes_UNIQUE_id_usuario` (`id_usuario`),
  KEY `Estudiantes_Carreras_FK` (`id_carrera`),
  CONSTRAINT `Estudiantes_Carreras_FK` FOREIGN KEY (`id_carrera`) REFERENCES `Carreras` (`id_carrera`),
  CONSTRAINT `Estudiantes_Usuarios_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla especifica para el rol estudiante';

-- Estudiantes
INSERT INTO `Estudiantes` (`id_usuario`, `id_carrera`) VALUES
(1, 3), -- Juan (ID 1) en Computación
(2, 2); -- María (ID 2) en Electrónica


CREATE TABLE `Inscripciones` (
  `id_inscripcion` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'identificador unico de la tabla',
  `id_usuario` int unsigned NOT NULL,
  `id_ciclo` int unsigned NOT NULL,
  `fecha_inscripcion` date DEFAULT (curdate()),
  `estado` enum('activa','en_proceso','finalizada') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'en_proceso',
  PRIMARY KEY (`id_inscripcion`),
  KEY `Inscripciones_Ciclos_FK` (`id_ciclo`),
  KEY `Inscripciones_Usuarios_FK` (`id_usuario`),
  CONSTRAINT `Inscripciones_Ciclos_FK` FOREIGN KEY (`id_ciclo`) REFERENCES `Ciclos` (`id_ciclo`),
  CONSTRAINT `Inscripciones_Usuarios_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde estaran las incripciones de los usuarios';

-- Inscripción de Juan al ciclo 2024-2025
INSERT INTO `Inscripciones` (`id_usuario`, `id_ciclo`, `fecha_inscripcion`, `estado`) VALUES
(1, 3, '2024-08-10', 'activa');

CREATE TABLE `Laboratorios` (
  `id_laboratorio` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `ubicacion` varchar(250) NOT NULL,
  `responsable_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id_laboratorio`),
  UNIQUE KEY `Laboratorios_UNIQUE_nombre` (`nombre`),
  KEY `Laboratorios_Usuarios_FK` (`responsable_id`),
  CONSTRAINT `Laboratorios_Usuarios_FK` FOREIGN KEY (`responsable_id`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde estaran los laboratorios de la universidad';

INSERT INTO `Laboratorios` (`nombre`, `ubicacion`, `responsable_id`) VALUES
('Laboratorio de Cómputo A', 'Edificio C', 3), -- Roberto (ID 3) es el encargado
('Laboratorio de Electrónica', 'Edificio B', 3);


CREATE TABLE `Prestamos` (
  `id_prestamo` int unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario` int unsigned NOT NULL,
  `id_ejemplar` int unsigned NOT NULL,
  `fecha_prestamo` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_devolucion_esperada` date NOT NULL,
  `fecha_devolucion_real` datetime DEFAULT NULL,
  `estado` enum('activo','completado','retrasado') DEFAULT 'activo',
  PRIMARY KEY (`id_prestamo`),
  KEY `Prestamos_Usuarios_FK` (`id_usuario`),
  KEY `Prestamos_Ejemplares_FK` (`id_ejemplar`),
  CONSTRAINT `Prestamos_Ejemplares_FK` FOREIGN KEY (`id_ejemplar`) REFERENCES `Ejemplares` (`id_ejemplar`),
  CONSTRAINT `Prestamos_Usuarios_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde se registraran los prestamos';

-- Préstamo activo para Juan
INSERT INTO `Prestamos` (`id_usuario`, `id_ejemplar`, `fecha_devolucion_esperada`, `estado`) VALUES
(1, 1, '2026-02-15', 'activo');

CREATE TABLE `Roles` (
  `id_rol` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'identificador unico para la tabla',
  `tipo_rol` varchar(30) NOT NULL COMMENT 'Ej: ''Estudiante'', ''Administrativo'', ''Maestro''',
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `Roles_UNIQUE` (`tipo_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla para los roles/cargos';

INSERT INTO `Roles` (`id_rol`, `tipo_rol`) VALUES
(3,	'Administrativo'),
(4,	'Bibliotecario'),
(1,	'Estudiante'),
(2,	'Maestro');

CREATE TABLE `Usuarios` (
  `id_usuario` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'identificador unico de la tabla Usuarios',
  `nombre` varchar(40) NOT NULL,
  `apellidoP` varchar(40) NOT NULL,
  `apellidoM` varchar(40) NOT NULL,
  `matricula` varchar(15) NOT NULL,
  `email` varchar(200) NOT NULL,
  `contraseña` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_rol` int unsigned NOT NULL,
  `status` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `Usuarios_UNIQUE_matricula` (`matricula`),
  UNIQUE KEY `Usuarios_UNIQUE_email` (`email`),
  KEY `Usuarios_Roles_FK` (`id_rol`),
  CONSTRAINT `Usuarios_Roles_FK` FOREIGN KEY (`id_rol`) REFERENCES `Roles` (`id_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla donde iran los usuarios registrados';

INSERT INTO `Usuarios` (`nombre`, `apellidoP`, `apellidoM`, `matricula`, `email`, `contraseña`, `id_rol`, `status`) VALUES
('Juan', 'Pérez', 'García', '1800001A', 'juan.perez@umich.mx', '$2a$10$lOrG92cP5bh5Yp155aRb2.fbGsEXjcemhuxAkeAxuPkCGUf5aIBzC', 1, 'activo'),
('María', 'Rodríguez', 'López', '1800002B', 'maria.rod@umich.mx', '$2a$10$lOrG92cP5bh5Yp155aRb2.fbGsEXjcemhuxAkeAxuPkCGUf5aIBzC', 1, 'activo'),
('Roberto', 'Sánchez', 'Mena', 'M001', 'roberto.maestro@umich.mx', '$2a$10$lOrG92cP5bh5Yp155aRb2.fbGsEXjcemhuxAkeAxuPkCGUf5aIBzC', 2, 'activo'),
('Laura', 'Torres', 'Nava', 'A001', 'laura.admin@umich.mx', '$2a$10$lOrG92cP5bh5Yp155aRb2.fbGsEXjcemhuxAkeAxuPkCGUf5aIBzC', 3, 'activo'),
('Pedro', 'Gómez', 'Diaz', 'B001', 'pedro.biblio@umich.mx', '$2a$10$lOrG92cP5bh5Yp155aRb2.fbGsEXjcemhuxAkeAxuPkCGUf5aIBzC', 4, 'activo');


CREATE TABLE `QR` (
  `id_usuario` INT UNSIGNED NOT NULL COMMENT 'Identificador del usuario que tiene asociado el QR',
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del QR',
  `fecha_expiracion` DATETIME NOT NULL COMMENT 'Fecha en que expira el QR',
  `status` ENUM('valido', 'no_valido') DEFAULT 'valido' COMMENT 'Estado del QR',
  PRIMARY KEY (`id_usuario`), -- Cada usuario solo puede tener un QR asociado
  CONSTRAINT `QR_Usuarios_FK` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla que almacena el QR asociado a cada usuario';