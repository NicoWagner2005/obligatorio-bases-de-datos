# 🎓 Base de Datos I – Universidad Católica del Uruguay  
## Segundo Semestre 2025  
### 🧾 Trabajo Obligatorio – Sistema de Gestión de Reserva de Salas de Estudio  

---


## 🚀 Ejecución rápida con Docker Compose

El repositorio incluye un `docker-compose` que levanta la base de datos MySQL (con schema y datos de prueba), el backend en FastAPI y el frontend en Vite. Para poner todo en marcha:

1. Instala Docker y Docker Compose.
2. Desde la raíz del proyecto ejecuta:

```bash
docker compose up --build
```

3. Accede al frontend en `http://localhost:5173`. La API queda publicada en `http://localhost:8000`.

Los contenedores exponen los puertos 3306 (MySQL), 8000 (API) y 5173 (frontend) para pruebas locales.

---


## 📘 Descripción del Proyecto

El objetivo de este trabajo es **diseñar e implementar un sistema de información** para la gestión de **salas de estudio en la universidad**.  
El sistema debe permitir:

- La **reserva de salas** por estudiantes y docentes.  
- El **control de asistencia** de los participantes.  
- La **generación de reportes** que apoyen la gestión académica y la toma de decisiones.

Actualmente, la administración de las reservas se realiza de forma manual (planillas de papel).  
Este proyecto busca **modernizar y unificar** ese proceso, garantizando control, trazabilidad y uso equilibrado de los espacios.

---

## 🏫 Contexto de Uso

La UCU cuenta con salas destinadas a reuniones, videoconferencias y trabajos grupales.  
Los turnos se extienden desde **08:00 a 23:00**, en **bloques de una hora**.

Por ejemplo, para reservar de 8:30 a 10:00, se deben seleccionar los bloques:  
- 08:00–09:00  
- 09:00–10:00

### Tipos de salas:
- **Uso libre** → accesible a profesores, estudiantes de grado y posgrado.  
- **Exclusivas de posgrado**  
- **Exclusivas de docentes**

### Reglas generales:
- No se pueden ocupar salas por más de **2 horas diarias**.  
- No se puede participar en más de **3 reservas activas por semana**.  
- Los docentes y estudiantes de posgrado **no tienen estas limitaciones** al usar salas exclusivas.  
- Si ningún participante asiste a una reserva, **se aplica una sanción de 2 meses** sin poder reservar.

---

## 🧩 Funcionalidades Solicitadas

El sistema deberá permitir a los administrativos realizar:

- ABM de **participantes**  
- ABM de **salas**  
- ABM de **reservas** (con todas las validaciones de negocio)  
- ABM de **sanciones**

---

## 📊 Consultas y Reportes Requeridos

El sistema deberá generar consultas para análisis y BI, incluyendo:

- Salas más reservadas  
- Turnos más demandados  
- Promedio de participantes por sala  
- Cantidad de reservas por carrera y facultad  
- Porcentaje de ocupación de salas por edificio  
- Cantidad de reservas y asistencias (por tipo de usuario)  
- Cantidad de sanciones (por tipo de usuario)  
- Porcentaje de reservas efectivamente utilizadas 
- **+3 consultas adicionales sugeridas por el equipo**

---

## 🗄️ Modelo de Base de Datos

Se deberá implementar una base de datos **relacional (MySQL)** con las siguientes tablas mínimas:

- `login (correo, contraseña)`  
- `participante (ci, nombre, apellido, email)`  
- `programa_academico (nombre_programa, id_facultad, tipo [grado, posgrado])`  
- `participante_programa_academico (id_alumno_programa, ci_participante, nombre_programa, rol [alumno, docente])`  
- `facultad (id_facultad, nombre)`  
- `sala (nombre_sala, edificio, capacidad, tipo_sala [libre, posgrado, docente])`  
- `edificio (nombre_edificio, direccion, departamento)`  
- `turno (id_turno, hora_inicio, hora_fin)`  
- `reserva (id_reserva, nombre_sala, edificio, fecha, id_turno, estado [activa, cancelada, sin_asistencia, finalizada])`  
- `reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia [true, false])`  
- `sancion_participante (ci_participante, fecha_inicio, fecha_fin)`

---

## ⚙️ Requisitos del Entregable

- 🧾 **Script SQL** completo para creación de la base de datos.  
- 🧠 **Base de datos cargada** con datos maestros para pruebas.  
- 🖥️ **Aplicación funcional** (compilable y con todos los requerimientos implementados).  
- 📚 **Instructivo completo** para correr la aplicación localmente.  
- 🧾 **Informe técnico** con:
  - Decisiones de implementación.
  - Mejoras o consideraciones en el modelo.
  - Bitácora de trabajo.
  - Bibliografía utilizada.

---

## 💻 Consideraciones Técnicas

- Backend desarrollado en **Python**.  
- Base de datos en **MySQL**.  
- Framework de **frontend libre** (opcional).  
- **No se permite el uso de ORMs.**  
- Validaciones en **todas las capas** (front, back y base de datos).  
- Se deben aplicar **restricciones de seguridad** en la base de datos.

---

## 🌟 Se valorará

- Uso de **repositorio público en GitHub**.  
- Instructivo de ejecución incluido en el **README.md**.  
- **Dockerización** completa del sistema con `docker-compose` (app + base de datos + servicios).

---

## 📅 Cronograma

| Entrega | Fecha |
|----------|--------|
| Letra del obligatorio | 26/09/2025 |
| Avance | 31/10/2025 |
| Entrega final | 23/11/2025 |
| Defensas | 05/12/2025 |



---

## 👨‍💻 Autores
**Nicolás Wagner**
Estudiante de Ingeniería en Informática – UCU
**Guillermo González**
Estudiante de Ingeniería en Informática – UCU
**Bruno Ocampo**
Estudiante de Ingeniería en Informática – UCU

---
