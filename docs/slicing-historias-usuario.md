# Slicing de Historias de Usuario

## Técnicas de slicing aplicadas

| Técnica | Cómo se aplicó |
|---|---|
| Camino feliz primero | El primer slice de cada historia cubre el flujo principal sin excepciones. |
| Separar excepciones | Errores, validaciones y casos borde se mueven a slices posteriores. |
| Diferir integraciones externas | SAP, Cygnus y EmailService van en slices propios; el slice local se entrega antes. |
| Variaciones de datos | Listados básicos antes que filtros, orden o resaltados. |
| Operaciones (CRUD) | Ver y editar separados, y campos simples antes que campos con reglas (usuario, contraseña). |
| Diferir lo no esencial | Modo offline y registros de auditoría quedan como slices opcionales. |

**Talle relativo:** S = pequeño (1–2 días), M = mediano (3–5 días). Ningún slice
debería superar M; si ocurre, se vuelve a dividir.

---

## HU-01 — Login

*Como vendedor quiero iniciar sesión con mi usuario y contraseña para acceder de forma segura a mis clientes, documentos y rutas.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 01.1 | Login básico | Validar `usuario` + contraseña contra `vendedor.password_hash`, crear sesión y mostrar pantalla principal. | S | — |
| 01.2 | Errores de credenciales | Mensaje genérico para usuario inexistente o contraseña incorrecta, sin crear sesión. | S | 01.1 |
| 01.3 | Bloqueo y cuenta inactiva | Bloqueo temporal tras N intentos fallidos y rechazo de cuentas inactivas (requiere columna de estado). | S | 01.2 |
| 01.4 | Sincronización post-login | Disparar `sincronizarDatos()` al ingresar. | M | 01.1, integración SAP |
| 01.5 | Login offline (opcional) | Continuar con datos de la última sincronización cuando no hay conexión. | M | 01.4 |

## HU-02 — Consultar Facturas

*Como vendedor quiero consultar las facturas de un cliente para conocer su situación comercial y de cobranza.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 02.1 | Listado de facturas | Listar facturas del cliente desde la BD local, ordenadas por fecha descendente. | S | 01.1 |
| 02.2 | Detalle de factura | Ver todos los campos de una factura (incluye `tipo_factura`). | S | 02.1 |
| 02.3 | Estado vacío y filtros | Mensaje sin facturas y filtros por estado y rango de fechas. | S | 02.1 |
| 02.4 | Sincronización con SAP | Traer facturas con `obtenerFacturas()` y avisar si los datos están desactualizados. | M | 02.1, contrato SAP |

## HU-03 — Consultar Comodatos

*Como vendedor quiero consultar los comodatos de un cliente para saber qué objetos tiene prestados y bajo qué condiciones.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 03.1 | Listado de comodatos | Listar comodatos del cliente desde la BD local con objeto, fecha programada y condición. | S | 01.1 |
| 03.2 | Detalle de comodato | Ver el detalle completo de un comodato. | S | 03.1 |
| 03.3 | Resaltado de vencidos | Marcar visualmente comodatos vencidos o incumplidos. | S | 03.1, definición de "vencido" |
| 03.4 | Sincronización con SAP | Traer comodatos con `obtenerComodatos()` y manejar errores de sync. | M | 03.1, contrato SAP |

## HU-04 — Generar Remito

*Como vendedor quiero generar un remito durante mi ruta para dejar constancia de la mercadería entregada al cliente.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 04.1 | Generar remito local | Crear `documento` (`clase_doc = 3`) + `remito` en una sola transacción con estado `generado`. | M | 01.1 |
| 04.2 | Asociar remito a la ruta | Insertar en `ruta_entrega_documento` con el siguiente `orden`. | S | 04.1 |
| 04.3 | Validaciones y errores | Bloquear si no hay ruta activa, datos incompletos o error de escritura. | S | 04.1 |
| 04.4 | Notificar stock a Cygnus | Llamar a `notificarMovimientoStock()` / `actualizarStock()` tras generar el remito. | M | 04.1, contrato Cygnus |
| 04.5 | Reintento ante falla de Cygnus | Marcar el remito como pendiente de sincronizar y reintentar más tarde. | M | 04.4 |

## HU-05 — Firmar Confirmación de Entrega

*Como vendedor quiero validar el código de seguridad del cliente al entregar para confirmar de forma fehaciente que la entrega se realizó.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 05.1 | Generar código de seguridad | Crear el registro en `codigo_seguridad` con estado `generado`. | S | 04.1 |
| 05.2 | Enviar código por email | Enviar el código al cliente con `enviarCodigoSeguridad()`. | S | 05.1, 09.1 |
| 05.3 | Validar código (camino feliz) | Código correcto: documento pasa a `entregado` y código a `validado`. | S | 05.1 |
| 05.4 | Código incorrecto o expirado | Rechazo, límite de reintentos y reenvío de un nuevo código. | S | 05.3 |
| 05.5 | Rechazo de la entrega | Registrar el remito como `rechazado` sin validar código. | S | 05.3 |
| 05.6 | Validación offline (opcional) | Guardar la validación localmente y sincronizar al recuperar conexión. | M | 05.3 |

## HU-06 — Consultar Cuenta Corriente

*Como vendedor quiero consultar la cuenta corriente de un cliente para ver su saldo y movimientos antes de gestionar entregas o cobranzas.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 06.1 | Listado de movimientos | Mostrar movimientos de la cuenta con documento origen e importe. | S | 01.1 |
| 06.2 | Saldo | Calcular y mostrar el saldo de la cuenta. | S | 06.1, definición de saldo |
| 06.3 | Cuenta inexistente o bloqueada | Mensaje si no hay cuenta; advertencia si está inactiva. | S | 06.1 |
| 06.4 | Sincronización con SAP | Traer datos con `obtenerCuentaCorriente()` y avisar si están desactualizados. | M | 06.1, contrato SAP |

## HU-07 — Dar de alta Cliente

*Como vendedor quiero registrar un nuevo cliente desde la app para poder gestionarle documentos y entregas sin depender del back-office.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 07.1 | Alta local con validación | Formulario (nombre, CUIT, dirección), validar formato y unicidad de CUIT, insertar en `cliente`. | S | 01.1, columna dirección |
| 07.2 | Cuenta corriente inicial | Crear la `cuenta_corriente` activa junto con el cliente, en la misma transacción. | S | 07.1 |
| 07.3 | Alta en SAP | Llamar a `altaCliente()` tras el alta local. | M | 07.1, contrato SAP |
| 07.4 | Pendiente de sincronizar | Si SAP falla, dejar el cliente como pendiente y reintentar. | M | 07.3 |

## HU-08 — Editar información de Perfil de Vendedor

*Como vendedor quiero editar los datos de mi perfil para mantener actualizados mis datos de acceso y mi dispositivo.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 08.1 | Ver perfil | Mostrar los datos actuales del vendedor logueado. | S | 01.1 |
| 08.2 | Editar datos simples | Actualizar nombre y dispositivo. | S | 08.1 |
| 08.3 | Cambiar usuario | Actualizar `usuario` validando unicidad. | S | 08.2 |
| 08.4 | Cambiar contraseña | Validar política de contraseñas y actualizar `password_hash`. | S | 08.2, política definida |

## HU-09 — Consultar Documentos por Email

*Como vendedor quiero enviar por email los documentos de un cliente para que reciba su documentación sin depender de otro canal.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 09.1 | Email del cliente | Migración para agregar `email` a `cliente` y permitir cargarlo/editarlo. | S | — |
| 09.2 | Enviar una factura | Enviar una factura por `enviarDocumento()` y confirmar al vendedor. | M | 09.1, 02.1, contrato EmailService |
| 09.3 | Otros tipos y envío múltiple | Soportar remitos y comodatos, y selección de varios documentos. | S | 09.2 |
| 09.4 | Errores y reintento | Cliente sin email, falla del servicio, documento inaccesible y reintento. | S | 09.2 |
| 09.5 | Registro de envíos (opcional) | Persistir un log de envíos solicitados y su resultado. | S | 09.2 |

---

## Secuencia de entrega propuesta

Se prioriza primero el **esqueleto andante** (login + lecturas locales),
luego las escrituras, y al final las integraciones externas.

| Iteración | Foco | Slices |
|---|---|---|
| 1 | Acceso y lecturas locales | 01.1, 01.2, 02.1, 02.2, 03.1, 03.2, 06.1, 08.1 |
| 2 | Lecturas completas y perfil | 02.3, 03.3, 06.2, 06.3, 08.2, 08.3, 08.4, 01.3, 09.1 |
| 3 | Operación de entrega | 04.1, 04.2, 04.3, 05.1, 05.3, 05.4, 05.5, 07.1, 07.2 |
| 4 | Comunicación por email | 05.2, 09.2, 09.3, 09.4 |
| 5 | Integraciones externas | 01.4, 02.4, 03.4, 06.4, 04.4, 04.5, 07.3, 07.4 |
| Opcionales | Mejoras posteriores | 01.5, 05.6, 09.5 |

## Resumen

| Historia | Slices principales | Slices opcionales | Total |
|---|---|---|---|
| HU-01 Login | 4 | 1 | 5 |
| HU-02 Consultar Facturas | 4 | 0 | 4 |
| HU-03 Consultar Comodatos | 4 | 0 | 4 |
| HU-04 Generar Remito | 5 | 0 | 5 |
| HU-05 Firmar Confirmación | 5 | 1 | 6 |
| HU-06 Consultar Cuenta Corriente | 4 | 0 | 4 |
| HU-07 Dar de alta Cliente | 4 | 0 | 4 |
| HU-08 Editar Perfil | 4 | 0 | 4 |
| HU-09 Documentos por Email | 4 | 1 | 5 |
| **Total** | **38** | **3** | **41** |
