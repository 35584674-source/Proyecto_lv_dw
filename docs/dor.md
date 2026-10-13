# Definition of Ready (DoR) — Historias de Usuario

## 1. DoR general (aplica a todas las historias)

| # | Criterio | Descripción |
|---|---|---|
| 1 | Formato de historia | Redactada como: *Como [actor] quiero [acción] para [beneficio]*. |
| 2 | Cumple INVEST | Independiente, negociable, valiosa, estimable, pequeña y testeable (ver verificación en `casos_de_uso.md`). |
| 3 | Criterios de aceptación | Definidos en formato Dado/Cuando/Entonces, cubriendo camino feliz y excepciones principales. |
| 4 | Dependencias identificadas | Dependencias con otras historias, equipos o sistemas externos listadas y con fecha/plan de resolución. |
| 5 | Cambios de base de datos | Migraciones necesarias (tablas, columnas, constraints) identificadas y revisadas. |
| 6 | Contratos de integración | Para SAP, Cygnus y EmailService: endpoints, payloads y errores conocidos, o mock acordado. |
| 7 | Reglas de negocio y estados | Valores de `estado`, `clase_doc` y reglas de transición definidos y acordados. |
| 8 | Datos de prueba | Datos en `seed.sql` (o equivalentes) que permitan probar los criterios de aceptación. |
| 9 | Diseño de UI | Mockup o wireframe disponible para las pantallas involucradas. |
| 10 | Requisitos no funcionales | Seguridad, performance y comportamiento offline relevantes especificados. |
| 11 | Estimación | Estimada por el equipo de desarrollo (puntos o talle relativo). |
| 12 | Tamaño | Cabe en un sprint; si no, fue dividida (ver `slicing_historias_usuario.md`). |
| 13 | Preguntas abiertas resueltas | No quedan dudas bloqueantes con los integrantes del proyecto. |
| 14 | Priorización | El equipo ya priorizó las cosas en el backlog. |

---

## 2. DoR específico por historia

**Referencias de estado:** *Cumplido* = ya definido con la información disponible.
*Pendiente* = falta decisión o trabajo previo antes de entrar a sprint.

### HU-01 — Login

**Historia:** Como vendedor quiero iniciar sesión con mi usuario y contraseña para acceder de forma segura a mis clientes, documentos y rutas.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Mecanismo de sesión definido (JWT, cookie, etc.) | Pendiente | Decidir con el equipo. |
| Algoritmo de hash de contraseña acordado | Pendiente | Ej. bcrypt; debe coincidir con `password_hash` ya cargado. |
| Política de bloqueo por intentos fallidos | Pendiente | Definir N intentos y tiempo de bloqueo. |
| Datos de prueba | Cumplido | Vendedores en `seed.sql`. |
| Criterios de aceptación | Cumplido | Definidos en `casos_de_uso.md`. |

### HU-02 — Consultar Facturas

**Historia:** Como vendedor quiero consultar las facturas de un cliente para conocer su situación comercial y de cobranza.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Convención `clase_doc = 2` para facturas confirmada | Pendiente | Validar con el front y con SAP. |
| Contrato de `SAPAPI.obtenerFacturas()` | Pendiente | Campos y frecuencia de sincronización. |
| Campos a mostrar en lista y detalle | Pendiente | Confirmar con mockup. |
| Esquema de BD necesario | Cumplido | Tablas `documento` y `factura` existentes. |
| Datos de prueba | Cumplido | Facturas en `seed.sql`. |

### HU-03 — Consultar Comodatos

**Historia:** Como vendedor quiero consultar los comodatos de un cliente para saber qué objetos tiene prestados y bajo qué condiciones.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Convención `clase_doc = 1` para comodatos confirmada | Pendiente | Validar con el front y con SAP. |
| Contrato de `SAPAPI.obtenerComodatos()` | Pendiente | Campos y frecuencia de sincronización. |
| Esquema de BD necesario | Cumplido | Tablas `documento` y `comodato` existentes. |
| Datos de prueba | Cumplido | Comodato en `seed.sql` (agregar uno vencido para probar el resaltado). |

### HU-04 — Generar Remito

**Historia:** Como vendedor quiero generar un remito durante mi ruta para dejar constancia de la mercadería entregada al cliente.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Detalle de mercadería del remito | Pendiente | El esquema no tiene tabla de ítems/líneas de remito; definir si se necesita (ej. `remito_item`). |
| Estados del remito acordados | Pendiente | `generado`, `entregado`, `rechazado`, `pendiente de sincronizar`, etc. |
| Contrato con CygnusAPI (`actualizarStock`, `notificarMovimientoStock`) | Pendiente | Payload, autenticación y manejo de errores. |
| Regla de numeración de remitos | Pendiente | Quién genera `numero` (sistema, SAP, secuencia propia). |
| Definición de "ruta activa" | Pendiente | Valores de `ruta_entrega.estado` que la habilitan. |
| Esquema de BD necesario | Cumplido | `documento`, `remito`, `ruta_entrega_documento` existentes. |
| Datos de prueba | Cumplido | Ruta y remito en `seed.sql`. |

### HU-05 — Firmar Confirmación de Entrega

**Historia:** Como vendedor quiero validar el código de seguridad del cliente al entregar para confirmar de forma fehaciente que la entrega se realizó.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Entidad a la que pertenece el código | Pendiente | Hoy está asociado a `ruta_entrega` (supuesto); puede requerir asociarse a cada remito. |
| Expiración y límite de intentos | Pendiente | `codigo_seguridad` no tiene fecha de expiración ni contador de intentos. |
| Formato y longitud del código | Pendiente | Ej. 6 dígitos numéricos. |
| Dependencia con HU-04 y envío por email | Pendiente | El código se envía por email (requiere email del cliente, ver HU-09). |
| Comportamiento offline | Pendiente | Decidir si se valida sin conexión. |
| Datos de prueba | Cumplido | Código `483920` en `seed.sql`. |

### HU-06 — Consultar Cuenta Corriente

**Historia:** Como vendedor quiero consultar la cuenta corriente de un cliente para ver su saldo y movimientos antes de gestionar entregas o cobranzas.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Definición de saldo | Pendiente | Calculado como suma de `movimiento_cuenta.importe` o provisto por SAP. |
| Signo de los movimientos | Pendiente | Distinguir débitos/créditos (hoy solo hay `importe`). |
| Contrato de `SAPAPI.obtenerCuentaCorriente()` | Pendiente | Campos y frecuencia. |
| Esquema de BD necesario | Cumplido | `cuenta_corriente` y `movimiento_cuenta` existentes. |
| Datos de prueba | Cumplido | Cuentas y movimientos en `seed.sql`. |

### HU-07 — Dar de alta Cliente

**Historia:** Como vendedor quiero registrar un nuevo cliente desde la app para poder gestionarle documentos y entregas sin depender del back-office.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Campo dirección en BD | Pendiente | `FormularioAltaCliente` captura `direccion`, pero la tabla `cliente` no tiene esa columna. |
| Validación del formato de CUIT | Pendiente | Con/sin guiones, dígito verificador. |
| Contrato de `SAPAPI.altaCliente()` | Pendiente | Campos requeridos y respuesta. |
| Regla ante falla de SAP | Pendiente | Crear localmente como pendiente o bloquear el alta. |
| Asignación de zona | Pendiente | Cómo se determina `id_zona` del nuevo cliente. |
| Datos de prueba | Cumplido | Clientes de ejemplo en `seed.sql`. |

### HU-08 — Editar información de Perfil de Vendedor

**Historia:** Como vendedor quiero editar los datos de mi perfil para mantener actualizados mis datos de acceso y mi dispositivo.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Campos editables acordados | Pendiente | Confirmar si `id_zona` y `dispositivo` los edita el vendedor o un administrador. |
| Política de contraseñas | Pendiente | Largo mínimo, complejidad, reutilización. |
| Cambio de contraseña: exigir la actual | Pendiente | Decisión de seguridad. |
| Esquema de BD necesario | Cumplido | Tabla `vendedor` existente con `usuario` único. |
| Mockup de pantalla de perfil | Pendiente | Diseño no disponible aún. |

### HU-09 — Consultar Documentos por Email

**Historia:** Como vendedor quiero enviar por email los documentos de un cliente para que reciba su documentación sin depender de otro canal.

| Criterio específico | Estado | Detalle |
|---|---|---|
| Campo `email` en `cliente` | Pendiente | No existe en el esquema; requiere migración (`ALTER TABLE`). |
| Formato del envío | Pendiente | PDF adjunto o enlace; generación del PDF por tipo de documento. |
| Proveedor y contrato de `EmailService` | Pendiente | SMTP/API, remitente, plantillas, límites. |
| Registro de envíos | Pendiente | Decidir si se persiste un log (tabla `envio_email`). |
| Regla de permisos | Pendiente | Qué documentos puede enviar cada vendedor (¿solo de sus clientes?). |
| Datos de prueba | Pendiente | Agregar emails de prueba a los clientes del `seed.sql`. |

---

## 3. Resumen de preparación

| Historia | Bloqueantes principales | Lista para sprint |
|---|---|---|
| HU-01 Login | Mecanismo de sesión, política de bloqueo, columna de estado | No |
| HU-02 Consultar Facturas | Contrato SAP, convención `clase_doc` | Casi (slice local sí) |
| HU-03 Consultar Comodatos | Definición de vencido, contrato SAP | Casi (slice local sí) |
| HU-04 Generar Remito | Ítems del remito, estados, contrato Cygnus | No |
| HU-05 Firmar Confirmación | Entidad del código, expiración, intentos | No |
| HU-06 Consultar Cuenta Corriente | Definición de saldo, signo de movimientos | Casi (slice local sí) |
| HU-07 Dar de alta Cliente | Columna dirección, contrato SAP, regla ante falla | No |
| HU-08 Editar Perfil | Campos editables, política de contraseñas, mockup | Casi |
| HU-09 Documentos por Email | Columna email, formato de envío, EmailService | No |
