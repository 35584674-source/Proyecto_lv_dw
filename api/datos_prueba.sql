-- ZONAS

INSERT INTO zona_entrega (codigo_zona, descripcion)
VALUES
('Z01', 'Rosario Centro'),
('Z02', 'Rosario Norte');


-- VENDEDORES

INSERT INTO vendedor (
    nombre,
    usuario,
    password_hash,
    dispositivo,
    id_zona
)
VALUES
(
    'Juan Pérez',
    'jperez',
    'hash_prueba_123',
    'Celular Android',
    1
),
(
    'María Gómez',
    'mgomez',
    'hash_prueba_456',
    'Celular Android',
    2
);


-- CLIENTES

INSERT INTO cliente (
    nombre,
    denominacion,
    cuit,
    estado,
    id_zona
)
VALUES
(
    'Almacén El Sol',
    'El Sol SRL',
    '30-12345678-9',
    'activo',
    1
),
(
    'Kiosco La Esquina',
    'La Esquina',
    '30-98765432-1',
    'activo',
    1
),
(
    'Distribuidora Norte',
    'Distribuidora Norte SA',
    '30-11223344-5',
    'activo',
    2
);


-- CUENTAS CORRIENTES

INSERT INTO cuenta_corriente (
    numero_cuenta,
    estado,
    id_cliente
)
VALUES
(
    'CC-0001',
    'activa',
    1
),
(
    'CC-0002',
    'activa',
    2
),
(
    'CC-0003',
    'activa',
    3
);