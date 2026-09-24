CREATE TABLE zona_entrega (
    id_zona SERIAL PRIMARY KEY,
    codigo_zona VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    dispositivo VARCHAR(150),
    id_zona INTEGER REFERENCES zona_entrega(id_zona)
);

CREATE INDEX idx_vendedor_zona
ON vendedor(id_zona);


CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    denominacion VARCHAR(150),
    cuit VARCHAR(20) NOT NULL UNIQUE,
    estado VARCHAR(30) NOT NULL DEFAULT 'activo',
    id_zona INTEGER REFERENCES zona_entrega(id_zona)
);

CREATE INDEX idx_cliente_zona
ON cliente(id_zona);


CREATE TABLE cuenta_corriente (
    id_cuenta SERIAL PRIMARY KEY,
    numero_cuenta VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(30) NOT NULL DEFAULT 'activa',
    id_cliente INTEGER NOT NULL UNIQUE REFERENCES cliente(id_cliente)
);


CREATE TABLE ruta_entrega (
    id_ruta SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'pendiente',
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor)
);

CREATE INDEX idx_ruta_vendedor
ON ruta_entrega(id_vendedor);


CREATE TABLE codigo_seguridad (
    id_codigo SERIAL PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'generado',
    id_ruta INTEGER REFERENCES ruta_entrega(id_ruta)
);

CREATE INDEX idx_codigo_ruta
ON codigo_seguridad(id_ruta);


CREATE TABLE documento (
    id_documento SERIAL PRIMARY KEY,
    numero VARCHAR(50) NOT NULL,
    referencia VARCHAR(100),
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE,
    clase_doc INTEGER NOT NULL,
    importe DECIMAL(15,2) NOT NULL DEFAULT 0,
    explicacion TEXT,
    texto_ref TEXT,
    clave_referencia VARCHAR(100),
    estado VARCHAR(30) NOT NULL DEFAULT 'pendiente',
    id_cliente INTEGER REFERENCES cliente(id_cliente),
    id_vendedor INTEGER REFERENCES vendedor(id_vendedor)
);

CREATE INDEX idx_documento_cliente
ON documento(id_cliente);

CREATE INDEX idx_documento_vendedor
ON documento(id_vendedor);

CREATE INDEX idx_documento_clase
ON documento(clase_doc);


CREATE TABLE comodato (
    id_documento INTEGER PRIMARY KEY
        REFERENCES documento(id_documento)
        ON DELETE CASCADE,
    descripcion_objeto VARCHAR(255) NOT NULL,
    fecha_entrega_programada DATE,
    condicion_prestamo VARCHAR(255)
);


CREATE TABLE factura (
    id_documento INTEGER PRIMARY KEY
        REFERENCES documento(id_documento)
        ON DELETE CASCADE,
    tipo_factura VARCHAR(10) NOT NULL
);


CREATE TABLE remito (
    id_documento INTEGER PRIMARY KEY
        REFERENCES documento(id_documento)
        ON DELETE CASCADE
);


CREATE TABLE ruta_entrega_documento (
    id_ruta INTEGER NOT NULL
        REFERENCES ruta_entrega(id_ruta)
        ON DELETE CASCADE,
    id_documento INTEGER NOT NULL
        REFERENCES documento(id_documento)
        ON DELETE CASCADE,
    orden INTEGER NOT NULL,
    PRIMARY KEY (id_ruta, id_documento),
    UNIQUE (id_ruta, orden)
);


CREATE TABLE movimiento_cuenta (
    id_movimiento SERIAL PRIMARY KEY,
    id_cuenta INTEGER NOT NULL
        REFERENCES cuenta_corriente(id_cuenta)
        ON DELETE CASCADE,
    id_documento INTEGER REFERENCES documento(id_documento),
    importe DECIMAL(15,2) NOT NULL
);

CREATE INDEX idx_movimiento_cuenta
ON movimiento_cuenta(id_cuenta);

CREATE INDEX idx_movimiento_documento
ON movimiento_cuenta(id_documento);