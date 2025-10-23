-- === LOGIN ===
CREATE TABLE login (
    correo VARCHAR(30) PRIMARY KEY,
    contrasena VARCHAR(16) NOT NULL
);

-- === PARTICIPANTE ===
CREATE TABLE participante (
    ci VARCHAR(8) PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    email VARCHAR(30) NOT NULL
);

-- === FACULTAD ===
CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

-- === PROGRAMA_ACADEMICO ===
CREATE TABLE programa_academico (
    nombre_programa VARCHAR(30) PRIMARY KEY,
    id_facultad INT NOT NULL,
    tipo ENUM('grado', 'posgrado') NOT NULL,
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

-- === PARTICIPANTE_PROGRAMA_ACADEMICO ===
CREATE TABLE participante_programa_academico (
    id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
    ci_participante VARCHAR(8) NOT NULL,
    nombre_programa VARCHAR(30) NOT NULL,
    rol ENUM('alumno', 'docente') NOT NULL,
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

-- === EDIFICIO ===
CREATE TABLE edificio (
    nombre_edificio VARCHAR(20) PRIMARY KEY,
    direccion VARCHAR(30) NOT NULL,
    departamento VARCHAR(20) NOT NULL
);

-- === SALA ===
CREATE TABLE sala (
    nombre_sala VARCHAR(20),
    edificio VARCHAR(20),
    capacidad INT NOT NULL,
    tipo_sala ENUM('libre', 'posgrado', 'docente'),
    PRIMARY KEY (nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

-- === TURNO ===
CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- === RESERVA ===
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(20) NOT NULL,
    edificio VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    id_turno INT NOT NULL,
    estado ENUM('activa', 'cancelada', 'sin_asistencia', 'finalizada'),
    FOREIGN KEY (nombre_sala, edificio) REFERENCES sala(nombre_sala, edificio),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

-- === RESERVA_PARTICIPANTE ===
CREATE TABLE reserva_participante (
    ci_participante VARCHAR(8),
    id_reserva INT,
    fecha_solicitud_reserva DATE NOT NULL,
    asistencia BOOLEAN,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- === SANCION_PARTICIPANTE ===
CREATE TABLE sancion_participante (
    ci_participante VARCHAR(8),
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (ci_participante, fecha_inicio, fecha_fin),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);
