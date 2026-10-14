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
| 05.2 | Enviar código por email | Enviar el código al cliente con `enviarCodigoSeguridad()`. | S | 05.1, 06.1 |
| 05.3 | Validar código (camino feliz) | Código correcto: documento pasa a `entregado` y código a `validado`. | S | 05.1 |
| 05.4 | Código incorrecto o expirado | Rechazo, límite de reintentos y reenvío de un nuevo código. | S | 05.3 |
| 05.5 | Rechazo de la entrega | Registrar el remito como `rechazado` sin validar código. | S | 05.3 |
| 05.6 | Validación offline (opcional) | Guardar la validación localmente y sincronizar al recuperar conexión. | M | 05.3 |


## HU-07 — Consultar Cuenta Corriente

*Como vendedor quiero consultar la cuenta corriente de un cliente para ver su saldo y movimientos antes de gestionar entregas o cobranzas.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 07.1 | Listado de movimientos | Mostrar movimientos de la cuenta con documento origen e importe. | S | 01.1 |
| 07.2 | Saldo | Calcular y mostrar el saldo de la cuenta. | S | 07.1, definición de saldo |
| 07.3 | Cuenta inexistente o bloqueada | Mensaje si no hay cuenta; advertencia si está inactiva. | S | 07.1 |
| 07.4 | Sincronización con SAP | Traer datos con `obtenerCuentaCorriente()` y avisar si están desactualizados. | M | 07.1, contrato SAP |

## HU-08 — Dar de alta Cliente

*Como vendedor quiero registrar un nuevo cliente desde la app para poder gestionarle documentos y entregas sin depender del back-office.*

| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 08.1 | Alta local con validación | Formulario (nombre, CUIT, dirección), validar formato y unicidad de CUIT, insertar en `cliente`. | S | 01.1, columna dirección |
| 08.2 | Cuenta corriente inicial | Crear la `cuenta_corriente` activa junto con el cliente, en la misma transacción. | S | 08.1 |
| 08.3 | Alta en SAP | Llamar a `altaCliente()` tras el alta local. | M | 08.1, contrato SAP |
| 08.4 | Pendiente de sincronizar | Si SAP falla, dejar el cliente como pendiente y reintentar. | M | 08.3 |
## HU-09 — Editar información de Perfil de Vendedor

*Como vendedor quiero editar los datos de mi perfil para mantener actualizados mis datos de acceso y mi dispositivo.*


| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 09.1 | Ver perfil | Mostrar los datos actuales del vendedor logueado. | S | 01.1 |
| 09.2 | Editar datos simples | Actualizar nombre y dispositivo. | S | 09.1 |
| 09.3 | Cambiar usuario | Actualizar `usuario` validando unicidad. | S | 09.2 |
| 09.4 | Cambiar contraseña | Validar política de contraseñas y actualizar `password_hash`. | S | 09.2, política definida |

## HU-06 — Enviar documentos por email

*Como vendedor quiero enviar por email los documentos de un cliente para que reciba su documentación sin depender de otro canal.*


| ID | Slice | Alcance | Talle | Depende de |
|---|---|---|---|---|
| 06.1 | Email del cliente | Migración para agregar `email` a `cliente` y permitir cargarlo/editarlo. | S | — |
| 06.2 | Enviar una factura | Enviar una factura por `enviarDocumento()` y confirmar al vendedor. | M | 06.1, 02.1, contrato EmailService |
| 06.3 | Otros tipos y envío múltiple | Soportar remitos y comodatos, y selección de varios documentos. | S | 06.2 |
| 06.4 | Errores y reintento | Cliente sin email, falla del servicio, documento inaccesible y reintento. | S | 06.2 |
| 06.5 | Registro de envíos (opcional) | Persistir un log de envíos solicitados y su resultado. | S | 06.2 |


## Secuencia de entrega propuesta


| Iteración | Foco | Slices |
|---|---|---|
| 1 | Acceso y lecturas locales | 01.1, 01.2, 02.1, 02.2, 03.1, 03.2, 07.1, 09.1 |
| 2 | Lecturas completas y perfil | 02.3, 03.3, 07.2, 07.3, 09.2, 09.3, 09.4, 01.3, 06.1 |
| 3 | Operación de entrega y alta de clientes | 04.1, 04.2, 04.3, 05.1, 05.3, 05.4, 05.5, 08.1, 08.2 |
| 4 | Comunicación por email | 05.2, 06.2, 06.3, 06.4 |
| 5 | Integraciones externas | 01.4, 02.4, 03.4, 07.4, 04.4, 04.5, 08.3, 08.4 |
| Opcionales | Mejoras posteriores | 01.5, 05.6, 06.5 |


## Resumen


## Resumen

| Historia | Slices principales | Slices opcionales | Total |
|---|---|---|---|
| HU-01 Login | 4 | 1 | 5 |
| HU-02 Consultar Facturas | 4 | 0 | 4 |
| HU-03 Consultar Comodatos | 4 | 0 | 4 |
| HU-04 Generar Remito | 5 | 0 | 5 |
| HU-05 Firmar Confirmación | 5 | 1 | 6 |
| HU-06 Documentos por Email | 4 | 1 | 5 |
| HU-07 Consultar Cuenta Corriente | 4 | 0 | 4 |
| HU-08 Dar de alta Cliente | 4 | 0 | 4 |
| HU-09 Editar Perfil | 4 | 0 | 4 |
| **Total** | **38** | **3** | **41** |

# Parte A — Slicing vertical de una épica

## Épica seleccionada: Gestión de rutas y entregas

**Descripción:** Como responsable de logística, quiero organizar y supervisar las rutas de entrega para asegurar que los pedidos lleguen a los clientes y que cada entrega quede registrada digitalmente.

**Objetivo del slicing:** Dividir la épica en seis historias de usuario pequeñas, independientes en la medida de lo posible y con valor funcional. Se prioriza el camino feliz, luego las excepciones y finalmente las integraciones externas.

### HU-R01 — Consultar ruta asignada

**Historia:** Como vendedor, quiero consultar mi ruta asignada para conocer los clientes que debo visitar y el orden de las entregas.

**Criterios de aceptación:**

- **CA1:** Dado que tengo una ruta asignada, cuando ingreso al módulo de rutas, entonces el sistema muestra los clientes y el orden de visita.
- **CA2:** Dado que no tengo una ruta asignada, cuando ingreso al módulo de rutas, entonces el sistema muestra un mensaje informativo.

**Valor entregado:** El vendedor puede organizar su jornada sin depender de una planilla en papel.

### HU-R02 — Consultar documentos de una parada

**Historia:** Como vendedor, quiero consultar los documentos asociados a una parada para identificar qué documentación corresponde al cliente antes de realizar la entrega.

**Criterios de aceptación:**

- **CA1:** Dado que una parada tiene documentos asociados, cuando selecciono la parada, entonces visualizo los documentos correspondientes.
- **CA2:** Dado que una parada no tiene documentos asociados, cuando consulto su detalle, entonces el sistema informa que no hay documentación disponible.

**Valor entregado:** El vendedor dispone de la información necesaria para preparar la entrega.

### HU-R03 — Generar remito digital

**Historia:** Como vendedor, quiero generar un remito digital para registrar la mercadería que debo entregar sin utilizar formularios en papel.

**Criterios de aceptación:**

- **CA1:** Dado que tengo una ruta activa y los datos de la entrega son válidos, cuando confirmo la generación, entonces el sistema registra el remito con estado generado.
- **CA2:** Dado que faltan datos obligatorios, cuando intento generar el remito, entonces el sistema informa los errores y no registra un remito incompleto.

**Valor entregado:** Se digitaliza la documentación de la entrega.

### HU-R04 — Confirmar entrega mediante código

**Historia:** Como vendedor, quiero validar el código de seguridad proporcionado por el cliente para confirmar que recibió la mercadería.

**Criterios de aceptación:**

- **CA1:** Dado que existe un remito pendiente y el cliente proporciona un código válido para esa entrega, cuando ingreso el código, entonces el remito cambia a estado entregado.
- **CA2:** Dado que el código es incorrecto, cuando intento confirmar la entrega, entonces el sistema muestra un error y mantiene el remito pendiente.

**Valor entregado:** La entrega queda confirmada digitalmente y puede consultarse posteriormente.

### HU-R05 — Registrar rechazo de entrega

**Historia:** Como vendedor, quiero registrar el rechazo de una entrega para informar a logística que el cliente no recibió la mercadería.

**Criterios de aceptación:**

- **CA1:** Dado que el cliente rechaza la mercadería, cuando registro el rechazo, entonces el sistema guarda la entrega con estado rechazado.
- **CA2:** Dado que intento registrar un rechazo sin seleccionar una entrega, cuando confirmo la operación, entonces el sistema solicita seleccionar una entrega válida.

**Valor entregado:** Logística puede identificar las entregas no realizadas.

### HU-R06 — Consultar seguimiento de entregas

**Historia:** Como responsable de logística, quiero consultar el estado de las entregas de una ruta para controlar cuáles se completaron y cuáles siguen pendientes.

**Criterios de aceptación:**

- **CA1:** Dado que una ruta tiene entregas registradas, cuando consulto su seguimiento, entonces visualizo las entregas pendientes, entregadas y rechazadas.
- **CA2:** Dado que una ruta no tiene entregas registradas, cuando consulto su seguimiento, entonces el sistema muestra un mensaje indicando que no existen entregas disponibles.

**Valor entregado:** Logística puede realizar el seguimiento de la jornada de reparto.

## Orden de implementación propuesto

| Orden | Historia | Técnica de slicing |
|---|---|---|
| 1 | HU-R01 | Camino feliz primero |
| 2 | HU-R02 | Consulta de información |
| 3 | HU-R03 | Operación de creación |
| 4 | HU-R04 | Confirmación y validación |
| 5 | HU-R05 | Separación de excepciones |
| 6 | HU-R06 | Seguimiento y consulta |

Cada historia debe contemplar interfaz, lógica de negocio y persistencia o consulta de datos según corresponda. Las integraciones con SAP y Cygnus pueden planificarse posteriormente.

---

# Parte B — Análisis de situaciones excepcionales

## Caso 1 — Doble confirmación de una entrega

**Situación:** El vendedor ingresa el código de seguridad y confirma una entrega. Por una demora en la respuesta, vuelve a presionar el botón Confirmar.

**Problema:** El sistema podría procesar dos veces la misma operación.

**Decisión propuesta:** La confirmación debe ser idempotente. Si el remito ya está entregado, una segunda solicitud no debe generar otra confirmación ni duplicar movimientos.

**Responsables:**
- Analista funcional: definir el comportamiento esperado.
- Equipo técnico: implementar la protección contra duplicados.
- Negocio: validar que la regla respeta el proceso de entrega.

**Resultado esperado:** La entrega se registra una sola vez.

## Caso 2 — Falla de conexión entre guardar el remito y notificar a Cygnus

**Situación:** El remito se guarda correctamente en la base de datos, pero se interrumpe la conexión antes de notificar el movimiento de stock a Cygnus.

**Problema:** El documento existe, pero el sistema externo puede no haber recibido la actualización.

**Decisión propuesta:** Mantener el remito registrado y guardar el estado de sincronización como pendiente. Reintentar la notificación cuando se restablezca la comunicación, utilizando un identificador único para evitar movimientos duplicados.

**Responsables:**
- Analista funcional: definir los estados y el tratamiento de errores.
- Equipo técnico: implementar el registro de pendientes y los reintentos.
- Negocio: establecer cómo actuar mientras el stock no esté sincronizado.

**Resultado esperado:** No se pierde el remito y se evita duplicar movimientos de stock.

## Caso 3 — Pérdida de conexión durante la confirmación

**Situación:** El vendedor se encuentra en el domicilio del cliente, pero pierde la conexión a internet.

**Problema:** No puede comprobar inmediatamente el código de seguridad contra el servidor.

**Decisión propuesta:** No marcar la entrega como confirmada definitivamente sin una validación confiable. Definir con el área de negocio si se habilitará un procedimiento offline con sincronización posterior o un mecanismo alternativo de contingencia.

**Responsables:**
- Negocio: decidir si se permite la confirmación offline.
- Analista funcional: documentar las reglas.
- Equipo técnico: evaluar la seguridad y viabilidad de la solución.

**Resultado esperado:** Se mantiene la trazabilidad y se evita confirmar entregas sin validación.

## Caso 4 — Código de seguridad incorrecto o vencido

**Situación:** El cliente proporciona un código que no coincide o cuya vigencia terminó.

**Problema:** No puede verificarse la recepción de la mercadería.

**Decisión propuesta:** Rechazar la confirmación, mantener el remito pendiente y permitir un nuevo intento dentro de un límite definido. Si el código venció, solicitar uno nuevo.

**Responsables:**
- Negocio: definir la vigencia y cantidad máxima de intentos.
- Analista funcional: establecer el flujo de excepción.
- Equipo técnico: implementar las validaciones.

**Resultado esperado:** Solo se confirma una entrega con un código válido.

## Caso 5 — Cliente rechaza la mercadería

**Situación:** El vendedor llega al domicilio, pero el cliente no acepta la entrega.

**Problema:** La visita se realizó, pero la mercadería no fue recibida.

**Decisión propuesta:** Registrar la entrega como rechazada, solicitar el motivo y conservar la información para que logística determine cómo continuar.

**Responsables:**
- Negocio y logística: definir el procedimiento posterior.
- Analista funcional: documentar los estados.
- Equipo técnico: implementar el registro del rechazo.

**Resultado esperado:** La entrega no se registra como exitosa y queda disponible para seguimiento.

## Caso 6 — Modificación del orden de la ruta

**Situación:** Logística necesita modificar el orden de visita porque un cliente solicita cambiar el horario de entrega.

**Problema:** La ruta planificada ya tiene documentos asociados a sus paradas.

**Decisión propuesta:** Permitir modificar el orden de las paradas pendientes sin perder las asociaciones entre clientes, documentos y entregas. Las entregas ya confirmadas deben conservar su historial.

**Responsables:**
- Logística: definir las prioridades de visita.
- Analista funcional: establecer las restricciones.
- Equipo técnico: implementar la actualización del orden.

**Resultado esperado:** La ruta puede reorganizarse sin perder información.

## Conclusión

El slicing vertical permite implementar progresivamente el sistema de gestión de rutas y entregas de La Virginia. Se comienza con funcionalidades de consulta y registro, y posteriormente se incorporan excepciones e integraciones externas.

La división propuesta permite obtener resultados verificables en cada iteración y reducir los riesgos asociados a la comunicación con SAP, Cygnus y los dispositivos utilizados durante el reparto.