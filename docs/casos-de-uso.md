# Casos de Uso

## Actores
- **Vendedor**: usuario principal del sistema, gestiona pedidos, facturas y clientes.
- **Cliente**: recibe documentación y confirma entregas.
- **Sistema**: ejecuta procesos automáticos de sincronización (SAP, Cygnus, Email).

## Listado de Casos de Uso (a desarrollar en detalle la próxima clase)
- CU01: Login
---
**Actor principal:** Vendedor
 
### Precondiciones
- El vendedor existe en la tabla `vendedor` con `usuario` y `password_hash` válidos.
- El dispositivo tiene la app instalada y conectividad a internet (o modo offline soportado).
### Postcondiciones
- Se crea una sesión/token asociado a `id_vendedor`.
- Se dispara `Sistema.sincronizarDatos()` para traer clientes, documentos y rutas actualizadas.
### Secuencia principal
1. El vendedor ingresa `usuario` y `password` en la pantalla de login.
2. El sistema busca el `usuario` en la tabla `vendedor`.
3. El sistema valida el `password` contra `password_hash`.
4. Si es válido, `Sistema.login(usuario, password)` genera la sesión.
5. El sistema ejecuta `sincronizarDatos()` en segundo plano.
6. El vendedor accede a la pantalla principal.
### Excepciones
- **E1 — Usuario inexistente:** se muestra "usuario o contraseña incorrectos" (mensaje genérico, sin revelar cuál campo falló).
- **E2 — Contraseña incorrecta:** mismo mensaje genérico que E1.
- **E3 — Vendedor inactivo/bloqueado:** se informa que la cuenta está deshabilitada y se sugiere contactar al administrador.
- **E4 — Sin conexión:** se permite reintentar o continuar con datos de la última sincronización, marcando la sesión como "offline".
- **E5 — Múltiples intentos fallidos:** tras N intentos, se bloquea el login temporalmente.
### Criterios de aceptación
```gherkin
Dado que un vendedor activo ingresa usuario y contraseña correctos
Cuando presiona "Ingresar"
Entonces el sistema lo autentica y muestra la pantalla principal
Y dispara la sincronización de datos
 
Dado que un vendedor ingresa una contraseña incorrecta
Cuando presiona "Ingresar"
Entonces el sistema muestra un mensaje de error genérico
Y no crea sesión
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | No depende de otros casos de uso para ejecutarse. |
| Negotiable | Sí | El mecanismo de bloqueo por intentos y el modo offline son detalles a definir con el equipo. |
| Valuable | Sí | Sin login no hay acceso al resto del sistema. |
| Estimable | Sí | Alcance acotado (autenticación + disparo de sync). |
| Small | Sí | Se implementa en un sprint corto. |
| Testable | Sí | Los criterios Gherkin son verificables automáticamente. |
 
---
- CU02: Consultar Facturas
---
**Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
- El cliente consultado existe en `cliente`.
- Existen registros en `documento` con `clase_doc = 2` (Factura) para ese cliente, sincronizados desde `SAPAPI.obtenerFacturas()`.
### Postcondiciones
- Se muestra el listado de facturas del cliente (número, fecha de emisión, vencimiento, importe, estado).
### Secuencia principal
1. El vendedor selecciona un cliente.
2. El sistema consulta `documento` JOIN `factura` filtrando `id_cliente` y `clase_doc = 2`.
3. Se muestra el listado ordenado por fecha de emisión descendente.
4. El vendedor selecciona una factura para ver el detalle completo.
### Excepciones
- **E1 — Cliente sin facturas:** se muestra un estado vacío ("no hay facturas registradas").
- **E2 — Datos desactualizados:** si la última sincronización con SAP falló, se advierte que la información puede no estar al día.
- **E3 — Sin conexión:** se muestran las últimas facturas cacheadas localmente, si el dispositivo lo soporta.
### Criterios de aceptación
```gherkin
Dado que un cliente tiene 3 facturas cargadas
Cuando el vendedor entra a "Consultar Facturas" para ese cliente
Entonces se listan las 3 facturas ordenadas por fecha, más reciente primero
 
Dado que un cliente no tiene facturas
Cuando el vendedor entra a "Consultar Facturas"
Entonces se muestra un mensaje de "sin facturas registradas"
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | Solo depende de tener clientes y facturas ya cargados, no de otros casos de uso. |
| Negotiable | Sí | El orden, filtros y paginación son negociables con UX. |
| Valuable | Sí | Es información clave para la gestión comercial del vendedor. |
| Estimable | Sí | Query + listado simple, esfuerzo conocido. |
| Small | Sí | Acotado a lectura/listado, sin lógica de escritura. |
| Testable | Sí | Se valida con datos de prueba y conteo de resultados. |
 
---
- CU03: Consultar Comodatos
---
  **Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
- El cliente existe.
- Existen registros en `documento` JOIN `comodato` (`clase_doc = 1`) para ese cliente.
### Postcondiciones
- Se muestra el listado de comodatos vigentes del cliente, con el objeto prestado y la condición de préstamo.
### Secuencia principal
1. El vendedor selecciona un cliente.
2. El sistema consulta `documento` JOIN `comodato` filtrando `id_cliente` y `clase_doc = 1`.
3. Se muestra el listado con `descripcion_objeto`, `fecha_entrega_programada`, `condicion_prestamo` y `estado`.
4. El vendedor puede ver el detalle de un comodato puntual.
### Excepciones
- **E1 — Cliente sin comodatos:** estado vacío.
- **E2 — Comodato vencido/incumplido:** se resalta visualmente el registro cuyo `estado` indique mora o incumplimiento.
- **E3 — Error de sincronización con SAP** (`obtenerComodatos()`): se informa y se ofrece reintentar.
### Criterios de aceptación
```gherkin
Dado que un cliente tiene un comodato con estado "vigente"
Cuando el vendedor consulta sus comodatos
Entonces ve el objeto prestado, la fecha programada y la condición del préstamo
 
Dado que un comodato tiene estado "vencido"
Cuando el vendedor consulta la lista
Entonces ese comodato aparece resaltado como alerta
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | Es análogo y paralelo a "Consultar Facturas", sin dependencia entre ambos. |
| Negotiable | Sí | El criterio de "resaltado por vencimiento" puede ajustarse con el equipo de producto. |
| Valuable | Sí | Permite al vendedor gestionar objetos prestados y su devolución. |
| Estimable | Sí | Mismo patrón que facturas, esfuerzo conocido. |
| Small | Sí | Solo lectura y presentación. |
| Testable | Sí | Verificable con comodatos de prueba en distintos estados. |
 
---
- CU04: Generar Remito
---
  **Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
- El vendedor tiene una `ruta_entrega` activa (`estado = 'pendiente'` o `'en curso'`).
- El cliente y los datos de la entrega (mercadería, cantidades) están definidos.
### Postcondiciones
- Se crea un nuevo registro en `documento` (`clase_doc = 3`) y su correspondiente fila en `remito`.
- El nuevo remito queda asociado a la ruta actual en `ruta_entrega_documento` con el siguiente número de `orden`.
- Se notifica el movimiento de stock a `CygnusAPI.actualizarStock()` / `notificarMovimientoStock()`.
### Secuencia principal
1. El vendedor selecciona el cliente dentro de su ruta activa.
2. Completa los datos del remito (mercadería entregada, referencia, importe si corresponde).
3. El sistema ejecuta `Remito.generar()`: inserta en `documento` y en `remito`.
4. El sistema asocia el remito a la ruta en `ruta_entrega_documento`.
5. El sistema notifica el movimiento de stock vía `CygnusAPI`.
6. El remito queda con `estado = 'generado'`, pendiente de confirmación de entrega.
### Excepciones
- **E1 — Vendedor sin ruta asignada:** no se permite generar el remito; se sugiere crear o asignarse una ruta primero.
- **E2 — Datos incompletos:** se bloquea el guardado y se marcan los campos faltantes.
- **E3 — Falla la notificación a CygnusAPI:** el remito se guarda igual localmente con `estado = 'generado - pendiente de sincronizar'`, y se reintenta la notificación más tarde.
- **E4 — Error de escritura en base de datos:** se informa el error y no se genera el remito (operación transaccional, todo o nada).
### Criterios de aceptación
```gherkin
Dado que el vendedor tiene una ruta activa con el cliente incluido
Cuando completa los datos del remito y confirma
Entonces se crea el documento y el remito con estado "generado"
Y queda asociado a la ruta con el orden correspondiente
 
Dado que falla la notificación a CygnusAPI
Cuando se genera el remito
Entonces el remito se guarda igual localmente
Y queda marcado como pendiente de sincronizar stock
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Parcial | Depende de que exista una ruta activa (caso de uso previo de gestión de rutas), pero es ejecutable de forma aislada dado ese dato. |
| Negotiable | Sí | El comportamiento ante falla de Cygnus (reintento automático vs. manual) es negociable. |
| Valuable | Sí | Es la operación central de la entrega física de mercadería. |
| Estimable | Sí | Alcance definido: alta de documento + subtipo + notificación externa. |
| Small | Sí | Se puede dividir en "generar remito local" y "sincronizar con Cygnus" si creciera. |
| Testable | Sí | Se valida verificando las filas creadas en `documento`, `remito` y `ruta_entrega_documento`. |
 
---
- CU05: Firmar Confirmación de Entrega
---
  **Actor principal:** Vendedor (con el Cliente presente)
 
### Precondiciones
- Existe un remito generado y pendiente de entrega (`documento.estado = 'generado'`).
- Existe un `codigo_seguridad` generado y enviado previamente al cliente por email.
- El vendedor está físicamente en la entrega (dentro del flujo de la ruta).
### Postcondiciones
- El `estado` del documento (remito) pasa a `'entregado'`.
- El `codigo_seguridad` queda marcado como `'validado'` (o `'usado'`).
- Queda registrada la confirmación de entrega para trazabilidad.
### Secuencia principal
1. El vendedor le pide al cliente el código de seguridad recibido por email.
2. El vendedor ingresa el código en la app.
3. El sistema valida el código contra `codigo_seguridad` (mismo `id_ruta` / entrega correspondiente).
4. Si coincide, el sistema actualiza `estado` del documento a `'entregado'` y el código a `'validado'`.
5. Se confirma visualmente la entrega al vendedor.
### Excepciones
- **E1 — Código incorrecto:** se informa el error y se permite reintentar (con límite de intentos).
- **E2 — Código expirado:** se ofrece reenviar un nuevo código por email.
- **E3 — Cliente rechaza la entrega:** se registra el remito con `estado = 'rechazado'` en vez de `'entregado'`, sin validar código.
- **E4 — Sin conexión al momento de validar:** se guarda la validación localmente y se sincroniza cuando vuelva la conexión, evitando bloquear al vendedor en el punto de entrega.
### Criterios de aceptación
```gherkin
Dado que el cliente recibió un código de seguridad válido por email
Cuando el vendedor lo ingresa correctamente en la app
Entonces el remito pasa a estado "entregado"
Y el código queda marcado como validado
 
Dado que el vendedor ingresa un código incorrecto
Cuando confirma
Entonces el sistema muestra un error
Y el remito permanece en estado "generado"
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Parcial | Depende de "Generar Remito" y del envío previo del código, pero su lógica de validación es independiente. |
| Negotiable | Sí | El límite de intentos y el comportamiento offline son ajustables. |
| Valuable | Sí | Es la prueba de entrega, crítica para la trazabilidad y la cuenta corriente. |
| Estimable | Sí | Acotado a validar un código y cambiar dos estados. |
| Small | Sí | Cabe en una única historia de sprint. |
| Testable | Sí | Se prueba con códigos válidos, inválidos y expirados. |
 
---
- CU06: Consultar Cuenta Corriente
---
  **Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
- El cliente tiene una `cuenta_corriente` asociada (relación 1 a 1).
### Postcondiciones
- Se muestra el saldo y el detalle de movimientos (`movimiento_cuenta`) del cliente.
### Secuencia principal
1. El vendedor selecciona un cliente.
2. El sistema consulta `cuenta_corriente` por `id_cliente`.
3. El sistema consulta `movimiento_cuenta` asociados a esa cuenta, con el documento origen de cada movimiento.
4. Se muestra el listado de movimientos y el saldo (calculado o almacenado, según se defina) ordenado por fecha.
### Excepciones
- **E1 — Cliente sin cuenta corriente:** se informa que el cliente no tiene cuenta habilitada.
- **E2 — Error de sincronización con SAP** (`obtenerCuentaCorriente()`): se muestra la última información disponible localmente con aviso de desactualización.
- **E3 — Cuenta con estado inactiva/bloqueada:** se muestra igual el historial, pero con una advertencia visible.
### Criterios de aceptación
```gherkin
Dado que un cliente tiene una cuenta corriente con 2 movimientos
Cuando el vendedor consulta la cuenta corriente
Entonces se muestran los 2 movimientos con su documento origen e importe
 
Dado que un cliente no tiene cuenta corriente
Cuando el vendedor intenta consultarla
Entonces se muestra un mensaje indicando que no tiene cuenta habilitada
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | Solo requiere datos de cliente y cuenta ya existentes. |
| Negotiable | Sí | La forma de calcular el saldo (acumulado vs. consultado en tiempo real a SAP) es negociable. |
| Valuable | Sí | Es información financiera clave para el vendedor y el cliente. |
| Estimable | Sí | Query de lectura con joins ya definidos. |
| Small | Sí | Solo lectura, sin mutaciones. |
| Testable | Sí | Verificable con los movimientos de `seed.sql`. |
 
---
- CU07: Dar de Alta Cliente
---
  **Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
- Los datos del nuevo cliente están disponibles (nombre, CUIT, dirección — vía `FormularioAltaCliente`).
- El CUIT no debe existir previamente en `cliente`.
### Postcondiciones
- Se crea un nuevo registro en `cliente`.
- Se registra el alta en SAP vía `SAPAPI.altaCliente()`.
- Se crea la `cuenta_corriente` inicial asociada al nuevo cliente.
### Secuencia principal
1. El vendedor completa el `FormularioAltaCliente` (nombre, CUIT, dirección).
2. El sistema valida que el CUIT no exista ya en `cliente`.
3. El sistema inserta el nuevo cliente en la base local.
4. El sistema llama a `SAPAPI.altaCliente()` para sincronizar el alta.
5. El sistema crea la `cuenta_corriente` inicial en estado `'activa'`.
6. Se confirma el alta al vendedor.
### Excepciones
- **E1 — CUIT duplicado:** se rechaza el alta y se informa que el cliente ya existe.
- **E2 — Datos inválidos** (CUIT mal formado, campos obligatorios vacíos): se bloquea el guardado y se marcan los errores.
- **E3 — Falla la comunicación con SAP:** el cliente queda creado localmente con `estado = 'pendiente de sincronizar'`, y se reintenta el alta en SAP más tarde.
### Criterios de aceptación
```gherkin
Dado que se completa el formulario con un CUIT que no existe
Cuando el vendedor confirma el alta
Entonces se crea el cliente
Y se crea su cuenta corriente inicial
 
Dado que se intenta dar de alta un CUIT ya existente
Cuando el vendedor confirma
Entonces el sistema rechaza la operación
Y muestra que el cliente ya está registrado
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | No depende de otro caso de uso para ejecutarse. |
| Negotiable | Sí | El comportamiento ante falla de SAP (bloquear vs. crear localmente) es un punto a acordar con el equipo. |
| Valuable | Sí | Habilita que el vendedor incorpore nuevos clientes sin depender de un back-office. |
| Estimable | Sí | Alcance claro: validación + alta local + alta remota + cuenta inicial. |
| Small | Sí | Si creciera, se puede separar "alta local" de "sincronización con SAP". |
| Testable | Sí | Se prueba con CUITs válidos, duplicados e inválidos. |
 
---
- CU08: Editar Información de Perfil
---
  **Actor principal:** Vendedor
 
### Precondiciones
- Sesión iniciada.
### Postcondiciones
- Se actualizan los campos editables del vendedor (`nombre`, `usuario`, `password_hash`, `dispositivo`, `id_zona`) en la tabla `vendedor`.
### Secuencia principal
1. El vendedor accede a la sección de perfil.
2. Edita los campos que desea modificar.
3. El sistema valida los datos (por ejemplo, unicidad de `usuario`).
4. El sistema actualiza el registro en `vendedor`.
5. Se confirma el cambio al vendedor.
### Excepciones
- **E1 — Usuario ya en uso por otro vendedor:** se rechaza el cambio de `usuario` y se informa el conflicto.
- **E2 — Contraseña no cumple política mínima:** se bloquea el guardado con el detalle del requisito faltante.
- **E3 — Sin conexión:** se guarda el cambio localmente y se sincroniza cuando vuelva la conectividad (si la app lo soporta), o se bloquea la edición hasta reconectar.
### Criterios de aceptación
```gherkin
Dado que el vendedor cambia su dispositivo registrado
Cuando guarda los cambios
Entonces el campo "dispositivo" se actualiza en la base
 
Dado que el vendedor intenta cambiar su usuario por uno ya existente
Cuando guarda los cambios
Entonces el sistema rechaza la actualización
Y muestra que el usuario ya está en uso
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Sí | No depende de otros casos de uso. |
| Negotiable | Sí | El comportamiento offline es un detalle a definir. |
| Valuable | Sí | Permite mantener actualizados los datos de acceso y contacto del vendedor. |
| Estimable | Sí | Update simple sobre una sola tabla. |
| Small | Sí | Acotado a un formulario de edición. |
| Testable | Sí | Se valida con casos de usuario único, duplicado y contraseña inválida. |
 
---
- CU09: Consultar Documentos por Email
---
  **Actor principal:** Vendedor (solicita el envío) / Cliente (lo recibe)
 
### Precondiciones
- Sesión iniciada.
- Existen uno o más documentos (`factura`, `comodato` o `remito`) asociados al cliente.
- El cliente tiene una dirección de email válida registrada.
### Postcondiciones
- Se envía al cliente, por email, el o los documentos seleccionados (`EmailService.enviarDocumento()`).
- Queda un registro de que el envío fue solicitado (y, opcionalmente, de si fue exitoso).
### Secuencia principal
1. El vendedor selecciona el cliente y el o los documentos a enviar.
2. El sistema arma el contenido a enviar según el tipo de documento (factura, comodato o remito).
3. El sistema llama a `EmailService.enviarDocumento()` con el email del cliente.
4. El sistema confirma al vendedor que el envío fue realizado.
### Excepciones
- **E1 — Cliente sin email registrado:** se bloquea el envío y se solicita completar el dato antes de continuar.
- **E2 — Falla el envío de email** (servicio caído, dirección inválida): se informa el error y se permite reintentar.
- **E3 — Documento inexistente o inaccesible para ese cliente:** se rechaza la selección con un mensaje claro.
### Criterios de aceptación
```gherkin
Dado que un cliente tiene email registrado y una factura disponible
Cuando el vendedor solicita enviarla por email
Entonces el sistema envía el documento
Y confirma el envío exitoso al vendedor
 
Dado que un cliente no tiene email registrado
Cuando el vendedor intenta enviar un documento
Entonces el sistema bloquea la acción
Y solicita completar el email del cliente primero
```
 
### Verificación INVEST
| Criterio | Cumple | Justificación |
|---|---|---|
| Independent | Parcial | Depende de que el cliente tenga email, pero la lógica de envío en sí es independiente. |
| Negotiable | Sí | El formato del email (adjunto PDF vs. link) es un detalle a definir con el equipo. |
| Valuable | Sí | Le da autonomía al vendedor para reenviar documentación sin depender de otro canal. |
| Estimable | Sí | Acotado a: validar email + armar contenido + invocar servicio de envío. |
| Small | Sí | Cabe en una sola historia, incluso separando por tipo de documento si creciera. |
| Testable | Sí | Se prueba con clientes con y sin email, y con fallas simuladas del servicio de envío. |
 
---
