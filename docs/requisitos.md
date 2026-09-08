# Requisitos del Sistema

## Requisitos Funcionales (RF)

| ID | Descripción |
|----|-------------|
| RF01 | El sistema debe permitir el login de vendedores mediante usuario y contraseña. |
| RF02 | El sistema debe permitir consultar facturas asociadas al vendedor. |
| RF03 | El sistema debe permitir consultar comodatos (préstamo de máquinas de café) asociados a un cliente. |
| RF04 | El sistema debe permitir generar un remito digital al momento de la entrega. |
| RF05 | El sistema debe permitir al cliente firmar la entrega mediante un código de seguridad de 4 dígitos. |
| RF06 | El sistema debe enviar los documentos (factura, remito) al cliente por email. |
| RF07 | El sistema debe permitir consultar el estado de cuenta corriente del cliente. |
| RF08 | El sistema debe permitir dar de alta nuevos clientes mediante un formulario. |
| RF09 | El sistema debe validar los datos cargados en el alta de cliente antes de confirmarla. |
| RF10 | El sistema debe permitir editar la información de perfil del vendedor. |
| RF11 | El sistema debe integrarse con SAP para sincronizar facturas, comodatos y cuenta corriente. |
| RF12 | El sistema debe integrarse con Cygnus para notificar movimientos de stock. |

## Requisitos No Funcionales (RNF)

| ID | Descripción |
|----|-------------|
| RNF01 | El sistema debe responder las consultas en menos de 3 segundos. |
| RNF02 | El sistema debe ser accesible desde dispositivos móviles (celular/tablet). |
| RNF03 | El sistema debe garantizar la integridad de los documentos digitales generados. |
| RNF04 | El sistema debe mantener un registro (log) de las operaciones críticas (login, generación de remito, firma). |
| RNF05 | El sistema debe cumplir con la integración fiscal vigente (ARCA) a través de SAP. |