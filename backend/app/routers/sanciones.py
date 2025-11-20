from fastapi import APIRouter, HTTPException
from datetime import date
from app.database import get_connection, close_connection
from mysql.connector import Error

router = APIRouter(prefix="/sanciones", tags=["Sanciones"])

# ============================================================
#   1) CONSULTAR SANCIONES DE UN USUARIO
# ============================================================
@router.get("/{ci_participante}")
def get_sanciones(ci_participante: str):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT fecha_inicio, fecha_fin
                       FROM sancion_participante
                       WHERE ci_participante = %s
                       ORDER BY fecha_inicio DESC;
                       """, (ci_participante,))
        sanciones = cursor.fetchall()

        if not sanciones:
            return {"message": "El usuario no tiene sanciones"}

        return {"sanciones": sanciones}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)


# ============================================================
#   2) VALIDAR SI UN USUARIO TIENE SANCIÓN ACTIVA
# ============================================================
@router.get("/validar_sancion/{ci_participante}")
def validar_sancion(ci_participante: str):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hoy = date.today()

        cursor.execute("""
                       SELECT COUNT(*) AS activas
                       FROM sancion_participante
                       WHERE ci_participante = %s
                         AND %s BETWEEN fecha_inicio AND fecha_fin;
                       """, (ci_participante, hoy))

        activas = cursor.fetchone()["activas"]

        return {
            "bloqueado": activas > 0,
            "message": "Sanción activa" if activas > 0 else "Sin sanciones activas"
        }

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)


# ============================================================
#   3) CREAR SANCION MANUAL (ALTA)
# ============================================================
@router.post("/crear")
def crear_sancion(ci_participante: str, fecha_inicio: date, fecha_fin: date):
    conn = None
    cursor = None
    try:
        if fecha_fin <= fecha_inicio:
            raise HTTPException(400, "La fecha fin debe ser mayor a fecha inicio")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
                       VALUES (%s, %s, %s);
                       """, (ci_participante, fecha_inicio, fecha_fin))

        conn.commit()
        return {"message": "Sanción creada correctamente"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)


# ============================================================
#   4) BORRAR SANCION (BAJA)
# ============================================================
@router.delete("/{ci}/{fecha_inicio}")
def borrar_sancion(ci: str, fecha_inicio: date):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       DELETE FROM sancion_participante
                       WHERE ci_participante = %s AND fecha_inicio = %s;
                       """, (ci, fecha_inicio))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(404, "Sanción no encontrada")

        return {"message": "Sanción eliminada"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)


# ============================================================
#   5) MODIFICAR SANCION (MODIFICACIÓN)
# ============================================================
@router.put("/modificar")
def modificar_sancion(ci_participante: str, fecha_inicio: date, nueva_fecha_fin: date):
    conn = None
    cursor = None
    try:
        if nueva_fecha_fin <= fecha_inicio:
            raise HTTPException(400, "La nueva fecha fin debe ser mayor a fecha inicio")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE sancion_participante
                       SET fecha_fin = %s
                       WHERE ci_participante = %s AND fecha_inicio = %s;
                       """, (nueva_fecha_fin, ci_participante, fecha_inicio))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(404, "Sanción no encontrada")

        return {"message": "Sanción modificada correctamente"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_connection(cursor, conn)
