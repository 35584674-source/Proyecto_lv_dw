from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text


from database import SessionLocal


# ==================================================
# CONFIGURACIÓN DE LA API
# ==================================================

app = FastAPI(
    title="La Virginia API",
    description="API para la gestión de clientes, facturación, cuentas corrientes y rutas de entrega",
    version="1.0.0"
)


# ==================================================
# CONEXIÓN A LA BASE DE DATOS
# ==================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==================================================
# INICIO
# ==================================================

@app.get("/")
def inicio():
    return {
        "mensaje": "API La Virginia funcionando correctamente"
    }


# ==================================================
# CLIENTES - GET
# ==================================================

@app.get("/clientes")
def obtener_clientes(db: Session = Depends(get_db)):

    consulta = text("""
        SELECT
            id_cliente,
            nombre,
            denominacion,
            cuit,
            estado,
            id_zona
        FROM cliente
        ORDER BY id_cliente
    """)

    resultado = db.execute(consulta)

    clientes = []

    for fila in resultado:
        clientes.append({
            "id_cliente": fila.id_cliente,
            "nombre": fila.nombre,
            "denominacion": fila.denominacion,
            "cuit": fila.cuit,
            "estado": fila.estado,
            "id_zona": fila.id_zona
        })

    return clientes


@app.get("/clientes/{id_cliente}")
def obtener_cliente(
    id_cliente: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            id_cliente,
            nombre,
            denominacion,
            cuit,
            estado,
            id_zona
        FROM cliente
        WHERE id_cliente = :id_cliente
    """)

    resultado = db.execute(
        consulta,
        {"id_cliente": id_cliente}
    )

    fila = resultado.fetchone()

    if fila is None:
        return {
            "mensaje": "Cliente no encontrado"
        }

    return {
        "id_cliente": fila.id_cliente,
        "nombre": fila.nombre,
        "denominacion": fila.denominacion,
        "cuit": fila.cuit,
        "estado": fila.estado,
        "id_zona": fila.id_zona
    }


# ==================================================
# CLIENTES - POST
# ==================================================

@app.post("/clientes")
def crear_cliente(
    nombre: str,
    denominacion: str,
    cuit: str,
    estado: str = "activo",
    id_zona: int = None,
    db: Session = Depends(get_db)
):

    # Verificar que el CUIT no exista

    consulta_existente = text("""
        SELECT id_cliente
        FROM cliente
        WHERE cuit = :cuit
    """)

    existente = db.execute(
        consulta_existente,
        {"cuit": cuit}
    ).fetchone()

    if existente is not None:
        return {
            "mensaje": "Ya existe un cliente con ese CUIT"
        }

    # Verificar zona si fue informada

    if id_zona is not None:

        consulta_zona = text("""
            SELECT id_zona
            FROM zona_entrega
            WHERE id_zona = :id_zona
        """)

        zona = db.execute(
            consulta_zona,
            {"id_zona": id_zona}
        ).fetchone()

        if zona is None:
            return {
                "mensaje": "La zona indicada no existe"
            }

    # Insertar cliente

    consulta = text("""
        INSERT INTO cliente (
            nombre,
            denominacion,
            cuit,
            estado,
            id_zona
        )
        VALUES (
            :nombre,
            :denominacion,
            :cuit,
            :estado,
            :id_zona
        )
        RETURNING id_cliente
    """)

    resultado = db.execute(
        consulta,
        {
            "nombre": nombre,
            "denominacion": denominacion,
            "cuit": cuit,
            "estado": estado,
            "id_zona": id_zona
        }
    )

    id_nuevo = resultado.scalar()

    db.commit()

    return {
        "mensaje": "Cliente creado correctamente",
        "id_cliente": id_nuevo
    }


# ==================================================
# CLIENTES - PUT
# ==================================================

@app.put("/clientes/{id_cliente}")
def modificar_cliente(
    id_cliente: int,
    nombre: str,
    denominacion: str,
    cuit: str,
    estado: str,
    id_zona: int = None,
    db: Session = Depends(get_db)
):

    # Verificar que exista el cliente

    consulta_cliente = text("""
        SELECT id_cliente
        FROM cliente
        WHERE id_cliente = :id_cliente
    """)

    cliente = db.execute(
        consulta_cliente,
        {"id_cliente": id_cliente}
    ).fetchone()

    if cliente is None:
        return {
            "mensaje": "Cliente no encontrado"
        }

    # Verificar zona

    if id_zona is not None:

        consulta_zona = text("""
            SELECT id_zona
            FROM zona_entrega
            WHERE id_zona = :id_zona
        """)

        zona = db.execute(
            consulta_zona,
            {"id_zona": id_zona}
        ).fetchone()

        if zona is None:
            return {
                "mensaje": "La zona indicada no existe"
            }

    # Actualizar

    consulta = text("""
        UPDATE cliente
        SET
            nombre = :nombre,
            denominacion = :denominacion,
            cuit = :cuit,
            estado = :estado,
            id_zona = :id_zona
        WHERE id_cliente = :id_cliente
    """)

    db.execute(
        consulta,
        {
            "id_cliente": id_cliente,
            "nombre": nombre,
            "denominacion": denominacion,
            "cuit": cuit,
            "estado": estado,
            "id_zona": id_zona
        }
    )

    db.commit()

    return {
        "mensaje": "Cliente modificado correctamente",
        "id_cliente": id_cliente
    }


# ==================================================
# CLIENTES - DELETE
# ==================================================

@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(
    id_cliente: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        DELETE FROM cliente
        WHERE id_cliente = :id_cliente
        RETURNING id_cliente
    """)

    resultado = db.execute(
        consulta,
        {"id_cliente": id_cliente}
    )

    eliminado = resultado.fetchone()

    if eliminado is None:
        db.rollback()

        return {
            "mensaje": "Cliente no encontrado"
        }

    db.commit()

    return {
        "mensaje": "Cliente eliminado correctamente",
        "id_cliente": id_cliente
    }


# ==================================================
# VENDEDORES
# ==================================================

@app.get("/vendedores")
def obtener_vendedores(db: Session = Depends(get_db)):

    consulta = text("""
        SELECT
            id_vendedor,
            nombre,
            usuario,
            dispositivo,
            id_zona
        FROM vendedor
        ORDER BY id_vendedor
    """)

    resultado = db.execute(consulta)

    vendedores = []

    for fila in resultado:
        vendedores.append({
            "id_vendedor": fila.id_vendedor,
            "nombre": fila.nombre,
            "usuario": fila.usuario,
            "dispositivo": fila.dispositivo,
            "id_zona": fila.id_zona
        })

    return vendedores


@app.get("/vendedores/{id_vendedor}")
def obtener_vendedor(
    id_vendedor: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            id_vendedor,
            nombre,
            usuario,
            dispositivo,
            id_zona
        FROM vendedor
        WHERE id_vendedor = :id_vendedor
    """)

    resultado = db.execute(
        consulta,
        {"id_vendedor": id_vendedor}
    )

    fila = resultado.fetchone()

    if fila is None:
        return {
            "mensaje": "Vendedor no encontrado"
        }

    return {
        "id_vendedor": fila.id_vendedor,
        "nombre": fila.nombre,
        "usuario": fila.usuario,
        "dispositivo": fila.dispositivo,
        "id_zona": fila.id_zona
    }


# ==================================================
# CUENTAS CORRIENTES
# ==================================================

@app.get("/cuentas-corrientes")
def obtener_cuentas_corrientes(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            id_cuenta,
            numero_cuenta,
            estado,
            id_cliente
        FROM cuenta_corriente
        ORDER BY id_cuenta
    """)

    resultado = db.execute(consulta)

    cuentas = []

    for fila in resultado:
        cuentas.append({
            "id_cuenta": fila.id_cuenta,
            "numero_cuenta": fila.numero_cuenta,
            "estado": fila.estado,
            "id_cliente": fila.id_cliente
        })

    return cuentas


@app.get("/cuentas-corrientes/{id_cuenta}")
def obtener_cuenta_corriente(
    id_cuenta: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            cc.id_cuenta,
            cc.numero_cuenta,
            cc.estado,
            cc.id_cliente,
            c.nombre AS cliente,
            c.denominacion,
            c.cuit
        FROM cuenta_corriente cc
        INNER JOIN cliente c
            ON cc.id_cliente = c.id_cliente
        WHERE cc.id_cuenta = :id_cuenta
    """)

    resultado = db.execute(
        consulta,
        {"id_cuenta": id_cuenta}
    )

    fila = resultado.fetchone()

    if fila is None:
        return {
            "mensaje": "Cuenta corriente no encontrada"
        }

    return {
        "id_cuenta": fila.id_cuenta,
        "numero_cuenta": fila.numero_cuenta,
        "estado": fila.estado,
        "id_cliente": fila.id_cliente,
        "cliente": fila.cliente,
        "denominacion": fila.denominacion,
        "cuit": fila.cuit
    }


# ==================================================
# RUTAS - GET
# ==================================================

@app.get("/rutas")
def obtener_rutas(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            r.id_ruta,
            r.fecha,
            r.estado,
            r.id_vendedor,
            v.nombre AS vendedor
        FROM ruta_entrega r
        LEFT JOIN vendedor v
            ON r.id_vendedor = v.id_vendedor
        ORDER BY r.fecha, r.id_ruta
    """)

    resultado = db.execute(consulta)

    rutas = []

    for fila in resultado:
        rutas.append({
            "id_ruta": fila.id_ruta,
            "fecha": fila.fecha,
            "estado": fila.estado,
            "id_vendedor": fila.id_vendedor,
            "vendedor": fila.vendedor
        })

    return rutas


@app.get("/rutas/{id_ruta}")
def obtener_ruta(
    id_ruta: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            r.id_ruta,
            r.fecha,
            r.estado,
            r.id_vendedor,
            v.nombre AS vendedor,
            v.usuario,
            v.id_zona
        FROM ruta_entrega r
        LEFT JOIN vendedor v
            ON r.id_vendedor = v.id_vendedor
        WHERE r.id_ruta = :id_ruta
    """)

    resultado = db.execute(
        consulta,
        {"id_ruta": id_ruta}
    )

    fila = resultado.fetchone()

    if fila is None:
        return {
            "mensaje": "Ruta no encontrada"
        }

    return {
        "id_ruta": fila.id_ruta,
        "fecha": fila.fecha,
        "estado": fila.estado,
        "id_vendedor": fila.id_vendedor,
        "vendedor": fila.vendedor,
        "usuario_vendedor": fila.usuario,
        "id_zona": fila.id_zona
    }


# ==================================================
# RUTAS - POST
# ==================================================

@app.post("/rutas")
def crear_ruta(
    fecha: str,
    estado: str = "pendiente",
    id_vendedor: int = None,
    db: Session = Depends(get_db)
):

    # Verificar vendedor

    if id_vendedor is not None:

        consulta_vendedor = text("""
            SELECT id_vendedor
            FROM vendedor
            WHERE id_vendedor = :id_vendedor
        """)

        vendedor = db.execute(
            consulta_vendedor,
            {"id_vendedor": id_vendedor}
        ).fetchone()

        if vendedor is None:
            return {
                "mensaje": "El vendedor indicado no existe"
            }

    consulta = text("""
        INSERT INTO ruta_entrega (
            fecha,
            estado,
            id_vendedor
        )
        VALUES (
            :fecha,
            :estado,
            :id_vendedor
        )
        RETURNING id_ruta
    """)

    resultado = db.execute(
        consulta,
        {
            "fecha": fecha,
            "estado": estado,
            "id_vendedor": id_vendedor
        }
    )

    id_nueva_ruta = resultado.scalar()

    db.commit()

    return {
        "mensaje": "Ruta creada correctamente",
        "id_ruta": id_nueva_ruta
    }


# ==================================================
# RUTAS - PUT
# ==================================================

@app.put("/rutas/{id_ruta}")
def modificar_ruta(
    id_ruta: int,
    fecha: str,
    estado: str,
    id_vendedor: int = None,
    db: Session = Depends(get_db)
):

    consulta_ruta = text("""
        SELECT id_ruta
        FROM ruta_entrega
        WHERE id_ruta = :id_ruta
    """)

    ruta = db.execute(
        consulta_ruta,
        {"id_ruta": id_ruta}
    ).fetchone()

    if ruta is None:
        return {
            "mensaje": "Ruta no encontrada"
        }

    if id_vendedor is not None:

        consulta_vendedor = text("""
            SELECT id_vendedor
            FROM vendedor
            WHERE id_vendedor = :id_vendedor
        """)

        vendedor = db.execute(
            consulta_vendedor,
            {"id_vendedor": id_vendedor}
        ).fetchone()

        if vendedor is None:
            return {
                "mensaje": "El vendedor indicado no existe"
            }

    consulta = text("""
        UPDATE ruta_entrega
        SET
            fecha = :fecha,
            estado = :estado,
            id_vendedor = :id_vendedor
        WHERE id_ruta = :id_ruta
    """)

    db.execute(
        consulta,
        {
            "id_ruta": id_ruta,
            "fecha": fecha,
            "estado": estado,
            "id_vendedor": id_vendedor
        }
    )

    db.commit()

    return {
        "mensaje": "Ruta modificada correctamente",
        "id_ruta": id_ruta
    }


# ==================================================
# RUTAS - DELETE
# ==================================================

@app.delete("/rutas/{id_ruta}")
def eliminar_ruta(
    id_ruta: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        DELETE FROM ruta_entrega
        WHERE id_ruta = :id_ruta
        RETURNING id_ruta
    """)

    resultado = db.execute(
        consulta,
        {"id_ruta": id_ruta}
    )

    eliminado = resultado.fetchone()

    if eliminado is None:
        db.rollback()

        return {
            "mensaje": "Ruta no encontrada"
        }

    db.commit()

    return {
        "mensaje": "Ruta eliminada correctamente",
        "id_ruta": id_ruta
    }


# ==================================================
# DOCUMENTOS DE UNA RUTA
# ==================================================

@app.get("/rutas/{id_ruta}/documentos")
def obtener_documentos_ruta(
    id_ruta: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            d.id_documento,
            d.numero,
            d.referencia,
            d.fecha_emision,
            d.fecha_vencimiento,
            d.clase_doc,
            d.importe,
            d.explicacion,
            d.estado,
            red.orden,
            c.id_cliente,
            c.nombre AS cliente,
            c.denominacion
        FROM ruta_entrega_documento red
        INNER JOIN documento d
            ON red.id_documento = d.id_documento
        LEFT JOIN cliente c
            ON d.id_cliente = c.id_cliente
        WHERE red.id_ruta = :id_ruta
        ORDER BY red.orden
    """)

    resultado = db.execute(
        consulta,
        {"id_ruta": id_ruta}
    )

    documentos = []

    for fila in resultado:
        documentos.append({
            "id_documento": fila.id_documento,
            "numero": fila.numero,
            "referencia": fila.referencia,
            "fecha_emision": fila.fecha_emision,
            "fecha_vencimiento": fila.fecha_vencimiento,
            "clase_doc": fila.clase_doc,
            "importe": fila.importe,
            "explicacion": fila.explicacion,
            "estado": fila.estado,
            "orden": fila.orden,
            "id_cliente": fila.id_cliente,
            "cliente": fila.cliente,
            "denominacion": fila.denominacion
        })

    return documentos


# ==================================================
# DOCUMENTOS - GET
# ==================================================

@app.get("/documentos")
def obtener_documentos(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            d.id_documento,
            d.numero,
            d.referencia,
            d.fecha_emision,
            d.fecha_vencimiento,
            d.clase_doc,
            d.importe,
            d.explicacion,
            d.texto_ref,
            d.clave_referencia,
            d.estado,
            d.id_cliente,
            c.nombre AS cliente,
            d.id_vendedor,
            v.nombre AS vendedor
        FROM documento d
        LEFT JOIN cliente c
            ON d.id_cliente = c.id_cliente
        LEFT JOIN vendedor v
            ON d.id_vendedor = v.id_vendedor
        ORDER BY d.fecha_emision DESC, d.id_documento
    """)

    resultado = db.execute(consulta)

    documentos = []

    for fila in resultado:
        documentos.append({
            "id_documento": fila.id_documento,
            "numero": fila.numero,
            "referencia": fila.referencia,
            "fecha_emision": fila.fecha_emision,
            "fecha_vencimiento": fila.fecha_vencimiento,
            "clase_doc": fila.clase_doc,
            "importe": fila.importe,
            "explicacion": fila.explicacion,
            "texto_ref": fila.texto_ref,
            "clave_referencia": fila.clave_referencia,
            "estado": fila.estado,
            "id_cliente": fila.id_cliente,
            "cliente": fila.cliente,
            "id_vendedor": fila.id_vendedor,
            "vendedor": fila.vendedor
        })

    return documentos


@app.get("/documentos/{id_documento}")
def obtener_documento(
    id_documento: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            d.id_documento,
            d.numero,
            d.referencia,
            d.fecha_emision,
            d.fecha_vencimiento,
            d.clase_doc,
            d.importe,
            d.explicacion,
            d.texto_ref,
            d.clave_referencia,
            d.estado,
            d.id_cliente,
            c.nombre AS cliente,
            d.id_vendedor,
            v.nombre AS vendedor
        FROM documento d
        LEFT JOIN cliente c
            ON d.id_cliente = c.id_cliente
        LEFT JOIN vendedor v
            ON d.id_vendedor = v.id_vendedor
        WHERE d.id_documento = :id_documento
    """)

    resultado = db.execute(
        consulta,
        {"id_documento": id_documento}
    )

    fila = resultado.fetchone()

    if fila is None:
        return {
            "mensaje": "Documento no encontrado"
        }

    return {
        "id_documento": fila.id_documento,
        "numero": fila.numero,
        "referencia": fila.referencia,
        "fecha_emision": fila.fecha_emision,
        "fecha_vencimiento": fila.fecha_vencimiento,
        "clase_doc": fila.clase_doc,
        "importe": fila.importe,
        "explicacion": fila.explicacion,
        "texto_ref": fila.texto_ref,
        "clave_referencia": fila.clave_referencia,
        "estado": fila.estado,
        "id_cliente": fila.id_cliente,
        "cliente": fila.cliente,
        "id_vendedor": fila.id_vendedor,
        "vendedor": fila.vendedor
    }


# ==================================================
# DOCUMENTOS - POST
# ==================================================

@app.post("/documentos")
def crear_documento(
    numero: str,
    fecha_emision: str,
    clase_doc: int,
    importe: float = 0,
    referencia: str = None,
    fecha_vencimiento: str = None,
    explicacion: str = None,
    texto_ref: str = None,
    clave_referencia: str = None,
    estado: str = "pendiente",
    id_cliente: int = None,
    id_vendedor: int = None,
    db: Session = Depends(get_db)
):

    # Verificar cliente

    if id_cliente is not None:

        consulta_cliente = text("""
            SELECT id_cliente
            FROM cliente
            WHERE id_cliente = :id_cliente
        """)

        cliente = db.execute(
            consulta_cliente,
            {"id_cliente": id_cliente}
        ).fetchone()

        if cliente is None:
            return {
                "mensaje": "El cliente indicado no existe"
            }

    # Verificar vendedor

    if id_vendedor is not None:

        consulta_vendedor = text("""
            SELECT id_vendedor
            FROM vendedor
            WHERE id_vendedor = :id_vendedor
        """)

        vendedor = db.execute(
            consulta_vendedor,
            {"id_vendedor": id_vendedor}
        ).fetchone()

        if vendedor is None:
            return {
                "mensaje": "El vendedor indicado no existe"
            }

    consulta = text("""
        INSERT INTO documento (
            numero,
            referencia,
            fecha_emision,
            fecha_vencimiento,
            clase_doc,
            importe,
            explicacion,
            texto_ref,
            clave_referencia,
            estado,
            id_cliente,
            id_vendedor
        )
        VALUES (
            :numero,
            :referencia,
            :fecha_emision,
            :fecha_vencimiento,
            :clase_doc,
            :importe,
            :explicacion,
            :texto_ref,
            :clave_referencia,
            :estado,
            :id_cliente,
            :id_vendedor
        )
        RETURNING id_documento
    """)

    resultado = db.execute(
        consulta,
        {
            "numero": numero,
            "referencia": referencia,
            "fecha_emision": fecha_emision,
            "fecha_vencimiento": fecha_vencimiento,
            "clase_doc": clase_doc,
            "importe": importe,
            "explicacion": explicacion,
            "texto_ref": texto_ref,
            "clave_referencia": clave_referencia,
            "estado": estado,
            "id_cliente": id_cliente,
            "id_vendedor": id_vendedor
        }
    )

    id_documento = resultado.scalar()

    db.commit()

    return {
        "mensaje": "Documento creado correctamente",
        "id_documento": id_documento
    }


# ==================================================
# FACTURAS
# ==================================================

@app.get("/facturas")
def obtener_facturas(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            d.id_documento,
            d.numero,
            d.referencia,
            d.fecha_emision,
            d.fecha_vencimiento,
            d.importe,
            d.estado,
            f.tipo_factura,
            d.id_cliente,
            c.nombre AS cliente
        FROM factura f
        INNER JOIN documento d
            ON f.id_documento = d.id_documento
        LEFT JOIN cliente c
            ON d.id_cliente = c.id_cliente
        ORDER BY d.fecha_emision DESC, d.id_documento
    """)

    resultado = db.execute(consulta)

    facturas = []

    for fila in resultado:
        facturas.append({
            "id_documento": fila.id_documento,
            "numero": fila.numero,
            "referencia": fila.referencia,
            "fecha_emision": fila.fecha_emision,
            "fecha_vencimiento": fila.fecha_vencimiento,
            "importe": fila.importe,
            "estado": fila.estado,
            "tipo_factura": fila.tipo_factura,
            "id_cliente": fila.id_cliente,
            "cliente": fila.cliente
        })

    return facturas


# ==================================================
# MOVIMIENTOS DE CUENTA CORRIENTE
# ==================================================

@app.get("/cuentas-corrientes/{id_cuenta}/movimientos")
def obtener_movimientos_cuenta(
    id_cuenta: int,
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            mc.id_movimiento,
            mc.id_cuenta,
            mc.id_documento,
            mc.importe,
            cc.numero_cuenta,
            d.numero AS numero_documento,
            d.fecha_emision,
            d.estado
        FROM movimiento_cuenta mc
        INNER JOIN cuenta_corriente cc
            ON mc.id_cuenta = cc.id_cuenta
        LEFT JOIN documento d
            ON mc.id_documento = d.id_documento
        WHERE mc.id_cuenta = :id_cuenta
        ORDER BY mc.id_movimiento
    """)

    resultado = db.execute(
        consulta,
        {"id_cuenta": id_cuenta}
    )

    movimientos = []

    for fila in resultado:
        movimientos.append({
            "id_movimiento": fila.id_movimiento,
            "id_cuenta": fila.id_cuenta,
            "numero_cuenta": fila.numero_cuenta,
            "id_documento": fila.id_documento,
            "numero_documento": fila.numero_documento,
            "fecha_emision": fila.fecha_emision,
            "importe": fila.importe,
            "estado_documento": fila.estado
        })

    return movimientos


# ==================================================
# MOVIMIENTOS - POST
# ==================================================

@app.post("/movimientos")
def crear_movimiento(
    id_cuenta: int,
    importe: float,
    id_documento: int = None,
    db: Session = Depends(get_db)
):

    # Verificar cuenta

    consulta_cuenta = text("""
        SELECT id_cuenta
        FROM cuenta_corriente
        WHERE id_cuenta = :id_cuenta
    """)

    cuenta = db.execute(
        consulta_cuenta,
        {"id_cuenta": id_cuenta}
    ).fetchone()

    if cuenta is None:
        return {
            "mensaje": "La cuenta corriente no existe"
        }

    # Verificar documento si fue informado

    if id_documento is not None:

        consulta_documento = text("""
            SELECT id_documento
            FROM documento
            WHERE id_documento = :id_documento
        """)

        documento = db.execute(
            consulta_documento,
            {"id_documento": id_documento}
        ).fetchone()

        if documento is None:
            return {
                "mensaje": "El documento indicado no existe"
            }

    consulta = text("""
        INSERT INTO movimiento_cuenta (
            id_cuenta,
            id_documento,
            importe
        )
        VALUES (
            :id_cuenta,
            :id_documento,
            :importe
        )
        RETURNING id_movimiento
    """)

    resultado = db.execute(
        consulta,
        {
            "id_cuenta": id_cuenta,
            "id_documento": id_documento,
            "importe": importe
        }
    )

    id_movimiento = resultado.scalar()

    db.commit()

    return {
        "mensaje": "Movimiento creado correctamente",
        "id_movimiento": id_movimiento
    }


# ==================================================
# CÓDIGOS DE SEGURIDAD
# ==================================================

@app.get("/codigos-seguridad")
def obtener_codigos_seguridad(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            cs.id_codigo,
            cs.codigo,
            cs.estado,
            cs.id_ruta,
            r.fecha,
            r.estado AS estado_ruta
        FROM codigo_seguridad cs
        LEFT JOIN ruta_entrega r
            ON cs.id_ruta = r.id_ruta
        ORDER BY cs.id_codigo
    """)

    resultado = db.execute(consulta)

    codigos = []

    for fila in resultado:
        codigos.append({
            "id_codigo": fila.id_codigo,
            "codigo": fila.codigo,
            "estado": fila.estado,
            "id_ruta": fila.id_ruta,
            "fecha_ruta": fila.fecha,
            "estado_ruta": fila.estado_ruta
        })

    return codigos


# ==================================================
# CÓDIGOS DE SEGURIDAD - POST
# ==================================================

@app.post("/codigos-seguridad")
def crear_codigo_seguridad(
    codigo: str,
    id_ruta: int,
    estado: str = "generado",
    db: Session = Depends(get_db)
):

    # Verificar ruta

    consulta_ruta = text("""
        SELECT id_ruta
        FROM ruta_entrega
        WHERE id_ruta = :id_ruta
    """)

    ruta = db.execute(
        consulta_ruta,
        {"id_ruta": id_ruta}
    ).fetchone()

    if ruta is None:
        return {
            "mensaje": "La ruta indicada no existe"
        }

    consulta = text("""
        INSERT INTO codigo_seguridad (
            codigo,
            estado,
            id_ruta
        )
        VALUES (
            :codigo,
            :estado,
            :id_ruta
        )
        RETURNING id_codigo
    """)

    resultado = db.execute(
        consulta,
        {
            "codigo": codigo,
            "estado": estado,
            "id_ruta": id_ruta
        }
    )

    id_codigo = resultado.scalar()

    db.commit()

    return {
        "mensaje": "Código de seguridad creado correctamente",
        "id_codigo": id_codigo
    }


# ==================================================
# ZONAS
# ==================================================

@app.get("/zonas")
def obtener_zonas(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            id_zona,
            codigo_zona,
            descripcion
        FROM zona_entrega
        ORDER BY id_zona
    """)

    resultado = db.execute(consulta)

    zonas = []

    for fila in resultado:
        zonas.append({
            "id_zona": fila.id_zona,
            "codigo_zona": fila.codigo_zona,
            "descripcion": fila.descripcion
        })

    return zonas


# ==================================================
# RESUMEN GENERAL
# ==================================================

@app.get("/resumen")
def obtener_resumen(
    db: Session = Depends(get_db)
):

    consulta = text("""
        SELECT
            (SELECT COUNT(*) FROM cliente) AS cantidad_clientes,
            (SELECT COUNT(*) FROM vendedor) AS cantidad_vendedores,
            (SELECT COUNT(*) FROM cuenta_corriente) AS cantidad_cuentas,
            (SELECT COUNT(*) FROM ruta_entrega) AS cantidad_rutas,
            (SELECT COUNT(*) FROM documento) AS cantidad_documentos,
            (SELECT COUNT(*) FROM factura) AS cantidad_facturas,
            (SELECT COUNT(*) FROM movimiento_cuenta) AS cantidad_movimientos
    """)

    resultado = db.execute(consulta)

    fila = resultado.fetchone()

    return {
        "clientes": fila.cantidad_clientes,
        "vendedores": fila.cantidad_vendedores,
        "cuentas_corrientes": fila.cantidad_cuentas,
        "rutas": fila.cantidad_rutas,
        "documentos": fila.cantidad_documentos,
        "facturas": fila.cantidad_facturas,
        "movimientos_cuenta": fila.cantidad_movimientos
    }