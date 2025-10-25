-- =====================================================
--  DATOS MAESTROS - SISTEMA DE GESTIÓN DE SALAS DE ESTUDIO
--  Universidad Católica del Uruguay - Segundo Semestre 2025
--  Autor: Nicolás Wagner
-- =====================================================


-- === 🏢 EDIFICIOS ===
INSERT INTO edificio(nombre_edificio, direccion, departamento) VALUES
('Mullin', 'Comandante Braga 2745', 'Montevideo'),
('San Ignacio', 'Cornelio Cantera 2731', 'Montevideo'),
('San Fernando', 'Av. Roosevelt y Oslo', 'Punta del Este'),
('Candelaria', 'Av. Roosevelt y Oslo', 'Punta del Este');


-- === 🎓 FACULTADES ===
INSERT INTO facultad(nombre) VALUES
('Ingeniería y Tecnologías'),
('Ciencias de la Salud'),
('Derecho y Artes Liberales'),
('Postgrados');


-- === 📚 PROGRAMAS ACADÉMICOS ===
INSERT INTO programa_academico(nombre_programa, id_facultad, tipo) VALUES
('Ingeniería en Informática', 1, 'grado'),
('Medicina', 2, 'grado'),
('Derecho', 3, 'grado'),
('Doctorado en ingeniería', 4, 'posgrado');


-- === 👥 PARTICIPANTES ===
INSERT INTO participante(ci, nombre, apellido, email) VALUES
('10000001', 'Felipe', 'Machado', 'fmachado@ucu.edu.uy'),
('10000002', 'Ana', 'Fernández', 'afernandez@ucu.edu.uy'),
('10000003', 'Carlos', 'Pérez', 'cperez@ucu.edu.uy'),
('10000004', 'María', 'Rodríguez', 'mrodriguez@ucu.edu.uy');


-- === 🔐 LOGINS ===
INSERT INTO login(correo, contrasena) VALUES
('fmachado@ucu.edu.uy', 'admin123'),
('afernandez@ucu.edu.uy', 'ana123'),
('cperez@ucu.edu.uy', 'carlos123'),
('mrodriguez@ucu.edu.uy', 'maria123');


-- === 🎓 PARTICIPANTE_PROGRAMA_ACADEMICO ===
INSERT INTO participante_programa_academico(ci_participante, nombre_programa, rol) VALUES
('10000001', 'Ingeniería en Informática', 'alumno'),
('10000002', 'Medicina', 'alumno'),
('10000003', 'Derecho', 'docente'),
('10000004', 'Doctorado en ingeniería', 'alumno');


-- === 🏫 SALAS ===
INSERT INTO sala(nombre_sala, edificio, capacidad, tipo_sala) VALUES
('Sala 101', 'Mullin', 8, 'libre'),
('Sala 102', 'San Ignacio', 6, 'libre'),
('Sala 201', 'San Fernando', 10, 'posgrado'),
('Sala 202', 'Candelaria', 12, 'docente');


-- === ⏰ TURNOS ===
INSERT INTO turno(hora_inicio, hora_fin) VALUES
('08:00:00', '09:00:00'),
('09:00:00', '10:00:00'),
('10:00:00', '11:00:00'),
('11:00:00', '12:00:00');


-- === 📅 RESERVAS ===
INSERT INTO reserva(nombre_sala, edificio, fecha, id_turno, estado) VALUES
('Sala 101', 'Mullin', '2025-10-25', 1, 'activa'),
('Sala 102', 'San Ignacio', '2025-10-25', 2, 'cancelada'),
('Sala 201', 'San Fernando', '2025-10-26', 3, 'activa'),
('Sala 202', 'Candelaria', '2025-10-26', 4, 'finalizada');


-- === 👥 RESERVA_PARTICIPANTE ===
INSERT INTO reserva_participante(ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
('10000001', 1, '2025-10-20', TRUE),
('10000002', 1, '2025-10-20', TRUE),
('10000003', 2, '2025-10-21', FALSE),
('10000004', 3, '2025-10-22', TRUE);


-- === ⚠️ SANCION_PARTICIPANTE ===
INSERT INTO sancion_participante(ci_participante, fecha_inicio, fecha_fin) VALUES
('10000003', '2025-09-01', '2025-10-01'),
('10000004', '2025-08-15', '2025-09-15'),
('10000002', '2025-06-10', '2025-07-10'),
('10000001', '2025-04-01', '2025-05-01');
