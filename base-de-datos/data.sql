-- =====================================================
--  DATA - SISTEMA DE GESTIÓN DE SALAS DE ESTUDIO (UCU)
--  Adaptado al nuevo esquema con user_id en PARTICIPANTE
-- =====================================================


-- LOGINS
INSERT INTO login (correo, contrasena) VALUES
('fmachado@ucu.edu.uy', 'admin123'),
('afernandez@ucu.edu.uy', 'ana123'),
('cperez@ucu.edu.uy', 'carlos123'),
('mrodriguez@ucu.edu.uy', 'maria123');


-- PARTICIPANTES
-- Vinculamos cada participante con el user_id correspondiente
INSERT INTO participante (ci, nombre, apellido, email, user_id) VALUES
('10000001', 'Felipe', 'Machado', 'fmachado@ucu.edu.uy', 1),
('10000002', 'Ana', 'Fernández', 'afernandez@ucu.edu.uy', 2),
('10000003', 'Carlos', 'Pérez', 'cperez@ucu.edu.uy', 3),
('10000004', 'María', 'Rodríguez', 'mrodriguez@ucu.edu.uy', 4);


-- FACULTADES
INSERT INTO facultad (nombre) VALUES
('Ingeniería y Tecnologías'),
('Ciencias de la Salud'),
('Derecho y Artes Liberales'),
('Postgrados');


-- PROGRAMAS ACADÉMICOS
INSERT INTO programa_academico (nombre_programa, id_facultad, tipo) VALUES
('Ingeniería en Informática', 1, 'grado'),
('Medicina', 2, 'grado'),
('Derecho', 3, 'grado'),
('Doctorado en ingeniería', 4, 'posgrado');


-- PARTICIPANTE_PROGRAMA_ACADEMICO
INSERT INTO participante_programa_academico (ci_participante, id_programa, rol) VALUES
('10000001', 1, 'alumno'),
('10000002', 2, 'alumno'),
('10000003', 3, 'docente'),
('10000004', 4, 'alumno');


-- EDIFICIOS
INSERT INTO edificio (nombre_edificio, direccion, departamento) VALUES
('Mullin', 'Comandante Braga 2745', 'Montevideo'),
('San Ignacio', 'Cornelio Cantera 2731', 'Montevideo'),
('San Fernando', 'Av. Roosevelt y Oslo', 'Punta del Este'),
('Candelaria', 'Av. Roosevelt y Oslo', 'Punta del Este');


-- SALAS
INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala) VALUES
('Sala 101', 1, 8, 'libre'),
('Sala 102', 2, 6, 'libre'),
('Sala 201', 3, 10, 'posgrado'),
('Sala 202', 4, 12, 'docente');


-- TURNOS
INSERT INTO turno (hora_inicio, hora_fin) VALUES
('08:00:00', '09:00:00'),
('09:00:00', '10:00:00'),
('10:00:00', '11:00:00'),
('11:00:00', '12:00:00');


-- RESERVAS
INSERT INTO reserva (id_sala, fecha, id_turno, estado) VALUES
(1, '2025-10-25', 1, 'activa'),
(2, '2025-10-25', 2, 'cancelada'),
(3, '2025-10-26', 3, 'activa'),
(4, '2025-10-26', 4, 'finalizada');


-- RESERVA_PARTICIPANTE
INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
('10000001', 1, '2025-10-20', TRUE),
('10000002', 1, '2025-10-20', TRUE),
('10000003', 2, '2025-10-21', FALSE),
('10000004', 3, '2025-10-22', TRUE);


-- SANCIONES
INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin) VALUES
('10000003', '2025-09-01', '2025-10-01'),
('10000004', '2025-08-15', '2025-09-15'),
('10000002', '2025-06-10', '2025-07-10'),
('10000001', '2025-04-01', '2025-05-01');
