-- LOGIN
CREATE TABLE login (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL
);

-- PARTICIPANTE
CREATE TABLE participante (
    ci VARCHAR(8) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES login(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- FACULTAD
CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- PROGRAMA_ACADEMICO
CREATE TABLE programa_academico (
    id_programa INT AUTO_INCREMENT PRIMARY KEY,
    nombre_programa VARCHAR(50) UNIQUE NOT NULL,
    id_facultad INT NOT NULL,
    tipo ENUM('grado', 'posgrado') NOT NULL,
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- PARTICIPANTE_PROGRAMA_ACADEMICO
CREATE TABLE participante_programa_academico (
    id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
    ci_participante VARCHAR(8) NOT NULL,
    id_programa INT NOT NULL,
    rol ENUM('alumno', 'docente') NOT NULL,
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- EDIFICIO
CREATE TABLE edificio (
    id_edificio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_edificio VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    UNIQUE (nombre_edificio, direccion)
);

-- SALA
CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(50) NOT NULL,
    id_edificio INT NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    tipo_sala ENUM('libre', 'posgrado', 'docente'),
    UNIQUE (nombre_sala, id_edificio),
    FOREIGN KEY (id_edificio) REFERENCES edificio(id_edificio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- TURNO
CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    CHECK (hora_fin > hora_inicio)
);

-- RESERVA
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT NOT NULL,
    fecha DATE NOT NULL,
    id_turno INT NOT NULL,
    estado ENUM('activa', 'cancelada', 'sin_asistencia', 'finalizada'),
    UNIQUE (id_sala, fecha, id_turno),
    FOREIGN KEY (id_sala) REFERENCES sala(id_sala)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- RESERVA_PARTICIPANTE
CREATE TABLE reserva_participante (
    ci_participante VARCHAR(8),
    id_reserva INT,
    fecha_solicitud_reserva DATE NOT NULL,
    asistencia BOOLEAN,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- SANCION_PARTICIPANTE
CREATE TABLE sancion_participante (
    ci_participante VARCHAR(8),
    fecha_inicio DATE,
    fecha_fin DATE,
    CHECK (fecha_fin > fecha_inicio),
    PRIMARY KEY (ci_participante, fecha_inicio, fecha_fin),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
