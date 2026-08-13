# Requisitos del sistema

## Descripción del sistema

El sistema tiene como objetivo mejorar la gestión y el control de la facturación, las cuentas corrientes de los clientes y la planificación de las rutas de entrega para la sucursal Rosario de La Virginia.

Actualmente, parte de la gestión se realiza mediante documentación en papel, lo que genera demoras y dificultades para registrar y controlar los pagos realizados por los clientes. El sistema permitirá digitalizar estos procesos y facilitar el acceso a la información.

El sistema contará con acceso mediante usuario y contraseña y se integrará con sistemas externos de La Virginia, como SAP y Cygnus, para consultar y sincronizar información relacionada con facturación y stock.

## Requisitos funcionales

### Módulo 1 — Control de facturación

| ID | Requisito |
|----|-----------|
| RF-01 | El sistema deberá permitir el inicio de sesión mediante usuario y contraseña. |
| RF-02 | El sistema deberá permitir registrar nuevos clientes. |
| RF-03 | El sistema deberá permitir consultar facturas digitales. |
| RF-04 | El sistema deberá generar códigos de validación para confirmar entregas. |
| RF-07 | El sistema deberá integrarse con SAP para sincronizar la información de facturación. |

### Módulo 2 — Cuenta Corriente

| ID | Requisito |
|----|-----------|
| RF-05 | El sistema deberá permitir consultar las cuentas corrientes de los clientes. |
| RF-06 | El sistema deberá registrar los pagos realizados por los clientes. |
| RF-09 | El sistema deberá registrar el historial de operaciones realizadas por los usuarios. |
| RF-10 | El sistema deberá permitir la recuperación de contraseña. |

### Módulo 3 — Planificación de rutas

| ID | Requisito |
|----|-----------|
| RF-08 | El sistema deberá permitir visualizar las rutas de reparto asignadas. |

## Requisitos no funcionales

### Rendimiento y disponibilidad

| ID | Requisito |
|----|-----------|
| RNF-01 | El sistema deberá estar disponible las 24 horas. |
| RNF-03 | El sistema deberá responder en menos de 5 segundos ante consultas normales. |
| RNF-04 | El sistema deberá contar con copias de seguridad automáticas. |
| RNF-05 | El sistema deberá funcionar correctamente en tablets y dispositivos móviles. |

### Seguridad y usabilidad

| ID | Requisito |
|----|-----------|
| RNF-02 | La información deberá transmitirse mediante conexiones seguras HTTPS. |
| RNF-06 | El acceso al sistema deberá gestionarse mediante roles y permisos. |
| RNF-07 | El sistema deberá garantizar la integridad y confidencialidad de la información. |
| RNF-08 | La interfaz deberá ser intuitiva y fácil de utilizar. |

### Integridad y trazabilidad

| ID | Requisito |
|----|-----------|
| RNF-09 | El sistema deberá garantizar la integridad de las operaciones realizadas sobre las cuentas corrientes y los pagos registrados. |
| RNF-10 | El sistema deberá mantener un registro de auditoría de las operaciones realizadas por los usuarios, indicando usuario, fecha, hora y operación efectuada. |

### Integración y sincronización

| ID | Requisito |
|----|-----------|
| RNF-11 | El sistema deberá garantizar la sincronización de la información con los sistemas externos SAP y Cygnus. |
| RNF-12 | El sistema deberá informar y registrar los errores producidos durante la sincronización con los sistemas externos. |
