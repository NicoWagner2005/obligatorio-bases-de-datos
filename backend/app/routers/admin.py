from datetime import date, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..database import close_connection, get_connection
from ..models.admin import *
from ..utils.hash import hash_password
from ..utils.jwt import require_admin

router = APIRouter(prefix="/admin", tags=["Administrativo"], dependencies=[Depends(require_admin)])



def _validar_ci(user_id: str) -> None:
    if not user_id or not user_id.isdigit() or len(user_id) not in (7, 8):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La cédula debe tener 7 u 8 dígitos")


def _obtener_participante(cursor, user_id: str) -> Optional[Dict]:
    cursor.execute(
        """
        SELECT p.ci,
               p.nombre,
               p.apellido,
               p.email,
               p.user_id,
               ppa.id_programa,
               ppa.rol,
               prog.tipo AS tipo_programa
        FROM participante p
                 LEFT JOIN participante_programa_academico ppa
                           ON p.ci = ppa.ci_participante
                 LEFT JOIN programa_academico prog
                           ON prog.id_programa = ppa.id_programa
        WHERE p.ci = %s
        LIMIT 1
        """,
        (user_id,),
    )
    return cursor.fetchone()


def _obtener_programa(cursor, programa_id: int) -> Optional[Dict]:
    cursor.execute("SELECT id_programa, tipo FROM programa_academico WHERE id_programa = %s", (programa_id,))
    return cursor.fetchone()


def _obtener_sala(cursor, sala_id: int) -> Optional[Dict]:
    cursor.execute(
        "SELECT id_sala, nombre_sala, id_edificio, capacidad, tipo_sala FROM sala WHERE id_sala = %s",
        (sala_id,),
    )
    return cursor.fetchone()


def _turno_valido(cursor, turno_id: int) -> bool:
    cursor.execute("SELECT 1 FROM turno WHERE id_turno = %s", (turno_id,))
    return cursor.fetchone() is not None


def _hay_sancion(cursor, user_id: str, fecha_objetivo: date) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM sancion_participante
        WHERE ci_participante = %s
          AND %s BETWEEN fecha_inicio AND fecha_fin
        LIMIT 1
        """,
        (user_id, fecha_objetivo),
    )
    return cursor.fetchone() is not None


def _reserva_solapada(cursor, user_id: str, fecha_objetivo: date, turno: int) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM reserva r
                 JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
        WHERE rp.ci_participante = %s
          AND r.fecha = %s
          AND r.id_turno = %s
          AND r.estado = 'activa'
        LIMIT 1
        """,
        (user_id, fecha_objetivo, turno),
    )
    return cursor.fetchone() is not None


def _limite_diario(cursor, user_id: str, fecha_objetivo: date) -> int:
    cursor.execute(
        """
        SELECT COUNT(*) AS cantidad
        FROM reserva r
                 JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
        WHERE rp.ci_participante = %s
          AND r.fecha = %s
          AND r.estado = 'activa'
        """,
        (user_id, fecha_objetivo),
    )
    return cursor.fetchone()["cantidad"]


def _limite_semanal(cursor, user_id: str, fecha_objetivo: date) -> int:
    inicio = fecha_objetivo - timedelta(days=6)
    cursor.execute(
        """
        SELECT COUNT(*) AS cantidad
        FROM reserva r
                 JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
        WHERE rp.ci_participante = %s
          AND r.fecha BETWEEN %s AND %s
          AND r.estado = 'activa'
        """,
        (user_id, inicio, fecha_objetivo),
    )
    return cursor.fetchone()["cantidad"]


def _requiere_limite(sala: Dict, participante: Dict) -> bool:
    tipo = sala["tipo_sala"]
    rol = participante.get("rol")
    programa = participante.get("tipo_programa")
    if tipo == "docente" and rol == "docente":
        return False
    if tipo == "posgrado" and (rol == "docente" or programa == "posgrado"):
        return False
    return True


def _validar_sala_para_participante(user_id: str, sala: Dict, participante: Dict) -> None:
    tipo = sala["tipo_sala"]
    rol = participante.get("rol")
    programa = participante.get("tipo_programa")
    if tipo == "docente" and rol != "docente":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sala exclusiva para docentes")
    if tipo == "posgrado" and rol != "docente" and programa != "posgrado":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sala exclusiva para posgrado o docentes")


def _participantes_reserva(cursor, reserva_id: int) -> List[str]:
    cursor.execute("SELECT ci_participante FROM reserva_participante WHERE id_reserva = %s", (reserva_id,))
    return [row["ci_participante"] for row in cursor.fetchall()]


def _sumar_meses(fecha: date, meses: int) -> date:
    total = fecha.month - 1 + meses
    year = fecha.year + total // 12
    month = total % 12 + 1
    dias = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(fecha.day, dias[month - 1])
    return date(year, month, day)


def _insertar_sancion(cursor, user_id: str, inicio: date, fin: date) -> None:
    cursor.execute(
        "INSERT INTO sancion_participante(ci_participante, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)",
        (user_id, inicio, fin),
    )


def _sancion_solapada(cursor, user_id: str, inicio: date, fin: date) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM sancion_participante
        WHERE ci_participante = %s
          AND fecha_inicio <= %s
          AND fecha_fin >= %s
        LIMIT 1
        """,
        (user_id, fin, inicio),
    )
    return cursor.fetchone() is not None


def _validar_reserva(cursor, sala: Dict, fecha_reserva: date, id_turno: int, participantes: List[str]) -> List[str]:
    if not participantes:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Debe indicar al menos un participante")
    if len(participantes) > sala["capacidad"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La sala no admite esa cantidad de personas")
    if not _turno_valido(cursor, id_turno):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "El turno no existe")

    for user_id in participantes:
        _validar_ci(user_id)
        datos = _obtener_participante(cursor, user_id)
        if not datos:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "El participante no existe")
        _validar_sala_para_participante(user_id, sala, datos)
        if _hay_sancion(cursor, user_id, fecha_reserva):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "El participante tiene una sanción vigente")
        if _reserva_solapada(cursor, user_id, fecha_reserva, id_turno):
            raise HTTPException(status.HTTP_409_CONFLICT, "El participante ya tiene una reserva en ese horario")
        if _requiere_limite(sala, datos):
            if _limite_diario(cursor, user_id, fecha_reserva) >= 2:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Supera el límite diario")
            if _limite_semanal(cursor, user_id, fecha_reserva) >= 3:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Supera el límite semanal")

    return participantes


def _guardar_participantes(cursor, reserva_id: int, participantes: List[str]) -> None:
    hoy = date.today()
    for user_id in participantes:
        cursor.execute(
            "INSERT INTO reserva_participante(id_reserva, fecha_solicitud_reserva, ci_participante) VALUES (%s, %s, %s)",
            (reserva_id, hoy, user_id),
        )



@router.get("/participantes")
def obtener_participantes():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT p.ci,
               p.nombre,
               p.apellido,
               p.email,
               p.user_id,
               ppa.id_programa,
               ppa.rol,
               prog.tipo AS tipo_programa
        FROM participante p
                 LEFT JOIN participante_programa_academico ppa
                           ON p.ci = ppa.ci_participante
                 LEFT JOIN programa_academico prog
                           ON prog.id_programa = ppa.id_programa""")
        return cursor.fetchall()
    finally:
        close_connection(cursor, conn)


# Participantes
@router.post("/participantes/crear", status_code=status.HTTP_201_CREATED)
def crear_participante(payload: ParticipanteCreate):
    _validar_ci(payload.ci)
    if payload.rol not in ("alumno", "docente"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Rol inválido")
    if not payload.password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La contraseña es obligatoria")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not _obtener_programa(cursor, payload.id_programa):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Programa académico inexistente")

        hashed = hash_password(payload.password)
        cursor.execute("INSERT INTO login (contrasena) VALUES (%s)", (hashed,))
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO participante (ci, nombre, apellido, email, user_id) VALUES (%s, %s, %s, %s, %s)",
            (payload.ci, payload.nombre, payload.apellido, payload.email, user_id),
        )

        cursor.execute(
            "INSERT INTO participante_programa_academico(ci_participante, id_programa, rol) VALUES (%s, %s, %s)",
            (payload.ci, payload.id_programa, payload.rol),
        )

        conn.commit()
        return {"message": "Participante creado"}
    finally:
        close_connection(cursor, conn)


@router.put("/participantes/{user_id}")
def actualizar_participante(user_id: str, payload: ParticipanteUpdate):
    _validar_ci(user_id)
    if payload.model_dump(exclude_none=True) == {}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No se enviaron cambios")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        participante = _obtener_participante(cursor, user_id)
        if not participante:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Participante no encontrado")

        nuevo_nombre = payload.nombre or participante["nombre"]
        nuevo_apellido = payload.apellido or participante["apellido"]
        nuevo_email = payload.email or participante["email"]

        cursor.execute(
            """
            UPDATE participante
            SET nombre = %s, apellido = %s, email = %s
            WHERE ci = %s
            """,
            (nuevo_nombre, nuevo_apellido, nuevo_email, user_id),
        )

        if payload.password:
            hashed = hash_password(payload.password)
            cursor.execute(
                "UPDATE login SET contrasena = %s WHERE user_id = %s",
                (hashed, participante["user_id"]),
            )

        if payload.id_programa or payload.rol:
            nuevo_programa = payload.id_programa or participante.get("id_programa")
            nuevo_rol = payload.rol or participante.get("rol")
            if nuevo_rol not in ("alumno", "docente"):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Rol inválido")
            if not nuevo_programa or not _obtener_programa(cursor, nuevo_programa):
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Programa académico inexistente")
            cursor.execute(
                "UPDATE participante_programa_academico SET id_programa = %s, rol = %s WHERE ci_participante = %s",
                (nuevo_programa, nuevo_rol, user_id),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO participante_programa_academico(ci_participante, id_programa, rol) VALUES (%s, %s, %s)",
                    (user_id, nuevo_programa, nuevo_rol),
                )

        conn.commit()
        return {"message": "Participante actualizado"}
    finally:
        close_connection(cursor, conn)


@router.delete("/participantes/{user_id}")
def eliminar_participante(user_id: str):
    _validar_ci(user_id)
    hoy = date.today()
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not _obtener_participante(cursor, user_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Participante no encontrado")

        cursor.execute(
            """
            SELECT 1
            FROM reserva r
                     JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
            WHERE rp.ci_participante = %s AND r.estado = 'activa'
            LIMIT 1
            """,
            (user_id,),
        )
        if cursor.fetchone():
            raise HTTPException(status.HTTP_409_CONFLICT, "Tiene reservas activas")

        cursor.execute(
            "SELECT 1 FROM sancion_participante WHERE ci_participante = %s AND %s BETWEEN fecha_inicio AND fecha_fin",
            (user_id, hoy),
        )
        if cursor.fetchone():
            raise HTTPException(status.HTTP_409_CONFLICT, "Tiene sanciones vigentes")

        cursor.execute("DELETE FROM participante WHERE ci = %s", (user_id,))
        conn.commit()
        return {"message": "Participante eliminado"}
    finally:
        close_connection(cursor, conn)


# Salas
@router.post("/salas", status_code=status.HTTP_201_CREATED)
def crear_sala(payload: SalaCreate):
    if payload.capacidad <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La capacidad debe ser positiva")
    if payload.tipo_sala not in {"libre", "posgrado", "docente"}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tipo de sala inválido")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT 1 FROM edificio WHERE id_edificio = %s", (payload.id_edificio,))
        if cursor.fetchone() is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "El edificio no existe")

        cursor.execute(
            "SELECT 1 FROM sala WHERE nombre_sala = %s AND id_edificio = %s",
            (payload.nombre_sala, payload.id_edificio),
        )
        if cursor.fetchone():
            raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una sala con ese nombre")

        cursor.execute(
            "INSERT INTO sala(nombre_sala, id_edificio, capacidad, tipo_sala) VALUES (%s, %s, %s, %s)",
            (payload.nombre_sala, payload.id_edificio, payload.capacidad, payload.tipo_sala),
        )
        conn.commit()
        return {"message": "Sala creada"}
    finally:
        close_connection(cursor, conn)


@router.put("/salas/{id_sala}")
def actualizar_sala(id_sala: int, payload: SalaUpdate):
    if payload.model_dump(exclude_none=True) == {}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No se enviaron cambios")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sala = _obtener_sala(cursor, id_sala)
        if not sala:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sala no encontrada")

        nuevo_nombre = payload.nombre_sala or sala["nombre_sala"]
        nuevo_edificio = payload.id_edificio or sala["id_edificio"]
        nueva_capacidad = payload.capacidad if payload.capacidad is not None else sala["capacidad"]
        nuevo_tipo = payload.tipo_sala or sala["tipo_sala"]

        if nueva_capacidad <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "La capacidad debe ser positiva")
        if nuevo_tipo not in {"libre", "posgrado", "docente"}:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tipo de sala inválido")

        cursor.execute("SELECT 1 FROM edificio WHERE id_edificio = %s", (nuevo_edificio,))
        if cursor.fetchone() is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "El edificio no existe")

        cursor.execute(
            """
            UPDATE sala
            SET nombre_sala = %s, id_edificio = %s, capacidad = %s, tipo_sala = %s
            WHERE id_sala = %s
            """,
            (nuevo_nombre, nuevo_edificio, nueva_capacidad, nuevo_tipo, id_sala),
        )
        conn.commit()
        return {"message": "Sala actualizada"}
    finally:
        close_connection(cursor, conn)


@router.delete("/salas/{id_sala}")
def eliminar_sala(id_sala: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not _obtener_sala(cursor, id_sala):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sala no encontrada")

        cursor.execute(
            """
            SELECT 1 FROM reserva
            WHERE id_sala = %s AND fecha >= %s AND estado <> 'cancelada'
            LIMIT 1
            """,
            (id_sala, date.today()),
        )
        if cursor.fetchone():
            raise HTTPException(status.HTTP_409_CONFLICT, "La sala tiene reservas futuras")

        cursor.execute("DELETE FROM sala WHERE id_sala = %s", (id_sala,))
        conn.commit()
        return {"message": "Sala eliminada"}
    finally:
        close_connection(cursor, conn)

@router.get("/reservas")
def get_mis_reservas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
                SELECT *
                FROM reserva
            """)

        return cursor.fetchall()


    finally:
        close_connection(cursor, conn)

@router.get("/sanciones")
def get_sanciones():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM sancion_participante""")

        return cursor.fetchall()
    finally:
        close_connection(cursor, conn)

@router.put("/reservas/{id_reserva}")
def actualizar_reserva(id_reserva: int, payload: ReservaUpdate):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()
        if not reserva:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Reserva no encontrada")
        if reserva["estado"] != "activa":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Solo se modifican reservas activas")

        nueva_sala = payload.id_sala or reserva["id_sala"]
        nueva_fecha = payload.fecha or reserva["fecha"]
        nuevo_turno = payload.id_turno or reserva["id_turno"]
        sala = _obtener_sala(cursor, nueva_sala)
        if not sala:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "La sala no existe")

        participantes = payload.participantes or _participantes_reserva(cursor, id_reserva)
        participantes = _validar_reserva(cursor, sala, nueva_fecha, nuevo_turno, participantes)

        cursor.execute(
            """
            UPDATE reserva
            SET id_sala = %s, fecha = %s, id_turno = %s
            WHERE id_reserva = %s
            """,
            (nueva_sala, nueva_fecha, nuevo_turno, id_reserva),
        )

        actuales = _participantes_reserva(cursor, id_reserva)
        for user_id in actuales:
            if user_id not in participantes:
                cursor.execute(
                    "DELETE FROM reserva_participante WHERE id_reserva = %s AND ci_participante = %s",
                    (id_reserva, user_id),
                )
        for user_id in participantes:
            if user_id not in actuales:
                cursor.execute(
                    "INSERT INTO reserva_participante(id_reserva, fecha_solicitud_reserva, ci_participante) VALUES (%s, %s, %s)",
                    (id_reserva, date.today(), user_id),
                )

        conn.commit()
        return {"message": "Reserva actualizada"}
    finally:
        close_connection(cursor, conn)
