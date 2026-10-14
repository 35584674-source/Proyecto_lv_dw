# Modelo Entidad-Relación

## Diagrama

El Modelo Entidad-Relación (MER) del sistema de gestión de facturación y rutas de entrega de La Virginia se encuentra desarrollado en el archivo [`diagramas/er.puml`](../diagramas/er.puml).

El modelo representa las 12 tablas definidas en `api/schema.sql`, incluyendo sus atributos principales, claves primarias (PK), claves foráneas (FK) y cardinalidades.

El diagrama puede visualizarse utilizando PlantUML.

## Entidades

| Entidad | Descripción | Relaciones clave |
|---|---|---|
| `zona_entrega` | Define las zonas geográficas utilizadas para organizar clientes y vendedores. | Se relaciona con `cliente` y `vendedor`. |
| `vendedor` | Almacena los datos de los vendedores y sus credenciales de acceso. | Se relaciona con `zona_entrega`, `ruta_entrega` y `documento`. |
| `cliente` | Registra los datos comerciales de los clientes. | Se relaciona con `zona_entrega`, `cuenta_corriente` y `documento`. |
| `cuenta_corriente` | Representa la cuenta corriente comercial de cada cliente. | Se relaciona con `cliente` y `movimiento_cuenta`. |
| `ruta_entrega` | Registra las rutas de reparto asignadas a los vendedores. | Se relaciona con `vendedor`, `codigo_seguridad` y `ruta_entrega_documento`. |
| `codigo_seguridad` | Almacena códigos utilizados para validar entregas. | Se relaciona con `ruta_entrega`. |
| `documento` | Centraliza los datos comunes de facturas, remitos y comodatos. | Se relaciona con `cliente`, `vendedor`, `factura`, `remito`, `comodato`, `ruta_entrega_documento` y `movimiento_cuenta`. |
| `factura` | Contiene los datos específicos de las facturas. | Es una especialización de `documento`. |
| `remito` | Identifica los documentos correspondientes a remitos. | Es una especialización de `documento`. |
| `comodato` | Contiene información sobre los bienes entregados en préstamo. | Es una especialización de `documento`. |
| `ruta_entrega_documento` | Relaciona los documentos con las rutas y establece su orden de visita. | Se relaciona con `ruta_entrega` y `documento`. |
| `movimiento_cuenta` | Registra los importes asociados a los movimientos de cuenta corriente. | Se relaciona con `cuenta_corriente` y, opcionalmente, con `documento`. |

## Descripción de atributos principales

### Zona de entrega

- `id_zona` (PK): identificador único de la zona.
- `codigo_zona` (UNIQUE): código utilizado para identificarla.
- `descripcion`: información descriptiva de la zona.

### Vendedor

- `id_vendedor` (PK): identificador único del vendedor.
- `nombre`: nombre del vendedor.
- `usuario` (UNIQUE): identificador utilizado para iniciar sesión.
- `password_hash`: contraseña almacenada mediante un hash.
- `dispositivo`: dispositivo asociado al vendedor.
- `id_zona` (FK): zona asignada, cuando corresponda.

### Cliente

- `id_cliente` (PK): identificador único del cliente.
- `nombre`: nombre del cliente.
- `denominacion`: denominación comercial.
- `cuit` (UNIQUE): identificación tributaria.
- `estado`: situación del cliente, con valor inicial `activo`.
- `id_zona` (FK): zona de entrega asociada.

### Cuenta corriente

- `id_cuenta` (PK): identificador único de la cuenta.
- `numero_cuenta` (UNIQUE): número comercial de la cuenta.
- `estado`: situación de la cuenta.
- `id_cliente` (FK, UNIQUE, NOT NULL): cliente propietario de la cuenta.

### Ruta de entrega

- `id_ruta` (PK): identificador de la ruta.
- `fecha`: fecha programada de reparto.
- `estado`: estado de la ruta.
- `id_vendedor` (FK): vendedor asignado.

### Código de seguridad

- `id_codigo` (PK): identificador del código.
- `codigo`: valor utilizado para la validación.
- `estado`: estado del código.
- `id_ruta` (FK): ruta asociada.

### Documento

- `id_documento` (PK): identificador único.
- `numero`: número del documento.
- `referencia`: referencia comercial.
- `fecha_emision`: fecha de emisión.
- `fecha_vencimiento`: fecha de vencimiento, cuando corresponda.
- `clase_doc`: clasificación del documento.
- `importe`: importe registrado.
- `explicacion` y `texto_ref`: información descriptiva adicional.
- `clave_referencia`: identificador de referencia.
- `estado`: estado del documento.
- `id_cliente` (FK): cliente asociado.
- `id_vendedor` (FK): vendedor asociado.

### Factura

- `id_documento` (PK, FK): identifica la factura y referencia al documento general.
- `tipo_factura`: tipo de comprobante.

### Remito

- `id_documento` (PK, FK): identifica el remito y referencia al documento general.

### Comodato

- `id_documento` (PK, FK): identifica el comodato y referencia al documento general.
- `descripcion_objeto`: descripción del bien entregado.
- `fecha_entrega_programada`: fecha prevista de entrega.
- `condicion_prestamo`: condiciones del préstamo.

### Ruta de entrega y documento

- `id_ruta` (PK, FK): ruta a la que pertenece el documento.
- `id_documento` (PK, FK): documento incluido en la ruta.
- `orden`: posición del documento dentro de la ruta.

La combinación de `id_ruta` e `id_documento` constituye la clave primaria compuesta. Además, existe una restricción `UNIQUE (id_ruta, orden)` para evitar que dos documentos ocupen la misma posición dentro de una ruta.

### Movimiento de cuenta

- `id_movimiento` (PK): identificador del movimiento.
- `id_cuenta` (FK, NOT NULL): cuenta corriente asociada.
- `id_documento` (FK): documento de origen, cuando exista.
- `importe`: importe del movimiento.

## Relaciones y cardinalidades

Las cardinalidades se establecen de acuerdo con las claves foráneas y restricciones del esquema SQL.

- **Zona de entrega y vendedor:** una zona puede tener varios vendedores. Un vendedor puede pertenecer a una zona o no tener ninguna asignada.
- **Zona de entrega y cliente:** una zona puede agrupar varios clientes. Un cliente puede tener una zona asignada.
- **Cliente y cuenta corriente:** un cliente puede tener cero o una cuenta corriente. Cada cuenta corriente pertenece obligatoriamente a un cliente.
- **Vendedor y ruta de entrega:** un vendedor puede tener varias rutas. Una ruta puede no tener vendedor asignado.
- **Ruta y código de seguridad:** una ruta puede tener varios códigos. Un código puede no estar asociado a una ruta.
- **Cliente y documento:** un cliente puede tener varios documentos. Un documento puede no tener cliente asociado.
- **Documento y factura, remito o comodato:** cada registro de una tabla especializada corresponde a un único documento general.
- **Ruta y documento:** relación de muchos a muchos resuelta mediante `ruta_entrega_documento`.
- **Cuenta corriente y movimiento:** una cuenta puede tener múltiples movimientos. Cada movimiento pertenece obligatoriamente a una cuenta.
- **Documento y movimiento:** un documento puede estar relacionado con varios movimientos. Un movimiento puede no tener documento asociado.

## Decisiones de diseño

### Decisión 1 — Especialización de documentos

**Problema:** el sistema debe administrar facturas, remitos y comodatos, que comparten atributos como número, fecha, cliente, vendedor y estado.

**Decisión adoptada:** utilizar una tabla general `documento` y tres tablas especializadas: `factura`, `remito` y `comodato`.

Las tablas especializadas utilizan `id_documento` como clave primaria y foránea, estableciendo una relación individual con el documento general.

**Alternativa considerada:** crear tres tablas completamente independientes, repitiendo los campos comunes.

**Motivo para descartarla:** produciría duplicación de atributos y dificultaría las consultas generales sobre documentos.

**Limitación:** el esquema actual no garantiza mediante restricciones que un documento pertenezca a un solo subtipo ni que `clase_doc` coincida con el subtipo registrado. Estas validaciones deberán contemplarse en la lógica de negocio o mediante restricciones adicionales.

### Decisión 2 — Código de seguridad asociado a la ruta

**Problema:** el sistema necesita validar digitalmente la recepción de mercadería.

**Decisión adoptada:** el modelo actual relaciona `codigo_seguridad` con `ruta_entrega` mediante `id_ruta`.

**Motivo:** permite organizar los códigos dentro del contexto de una ruta de reparto.

**Alternativa considerada:** asociar cada código directamente a un remito o a una entrega específica.

**Ventaja de la alternativa:** permitiría identificar inequívocamente qué entrega está siendo confirmada.

**Limitación del diseño actual:** una ruta puede contener varios documentos, por lo que el código asociado únicamente a la ruta no identifica directamente una entrega individual.

**Recomendación:** evaluar una relación directa entre el código y el remito o una entidad específica de entrega, antes de implementar la validación definitiva.

### Decisión 3 — Relación entre rutas y documentos

**Problema:** una ruta puede incluir varios documentos y el esquema necesita conservar el orden de las visitas.

**Decisión adoptada:** crear la tabla intermedia `ruta_entrega_documento`, con clave primaria compuesta y atributo `orden`.

**Alternativa considerada:** agregar `id_ruta` directamente a `documento`.

**Motivo para descartarla:** limitaría cada documento a una única ruta y reduciría la flexibilidad para reorganizar o reasignar documentos.

**Ventaja del diseño elegido:** permite asociar documentos con distintas rutas y conservar un orden específico para cada una.

## Conclusión

El MER representa la estructura de datos actual del sistema de facturación y planificación de rutas de entrega de La Virginia.

El modelo centraliza la información de clientes, vendedores, documentos, cuentas corrientes y rutas, utilizando claves primarias y foráneas para mantener la integridad referencial.

Las decisiones de diseño buscan evitar duplicaciones y facilitar futuras ampliaciones. También se identificaron limitaciones que deberán evaluarse durante el desarrollo, especialmente la asociación de los códigos de seguridad con las entregas individuales y la consistencia entre los tipos de documentos.