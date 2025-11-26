## FUNCIONALIDADES PRINCIPALES

- Página web para cargar un archivo CSV.
  El usuario selecciona un archivo .csv con registros de asistencia.

- Lectura y procesamiento del CSV.
  La aplicación interpreta los datos del CSV según su estructura definida.

- Flujo guiado por pasos (con botón “Siguiente”).

- Paso 1: Mostrar lista de empleados con horarios editables. Permitir agregar, eliminar o modificar empleados y sus horarios laborales (HH:MM – HH:MM).

- Paso 2: Selección del rango de fechas (Inicio y Fin en formato dd/mm/yyyy).
  Se excluyen sábados y domingos del análisis laboral, aunque pueden aparecer en reporte con etiqueta "Fin de semana".

- Paso 3: Para cada empleado, generar un “Análisis de Empleado” día por día.

- Paso 4: Mostrar un “Resumen General” consolidado por empleado.
-

## ESTRUCTURA DEL CSV

El archivo CSV tiene cabecera y posee el siguiente formato:

Número,Nombre,Tiempo,Estado,Dispositivos,Tipo de Registro
1,Elizabeth 1,03/11/2025 08:02:31,Entrada,Asistencia,0
1,Elizabeth 1,03/11/2025 18:58:51,Salida,Asistencia,0

- Número: ID del empleado.
- Nombre: nombre del empleado.
- Tiempo: fecha y hora en formato dd/mm/yyyy HH:MM:SS.
- Estado: Entrada o Salida.
- Dispositivos: texto fijo.
- Tipo de Registro: número entero (no se usa por ahora).

## LISTA DE EMPLEADOS Y HORARIOS

Los empleados tienen horarios laborales fijos definidos como:

"Elizabeth 1": ("08:00", "18:00"),
"Principe 2": ("07:00", "19:00"),
"Orlando 3": ("08:00", "18:00"),
"Chino 4": ("07:00", "19:00"),
"Mendez 6": ("07:00", "19:00"),
"Vallejo 7": ("07:00", "19:00"),
"Juan 10": ("07:00", "19:00"),
"Teofilo 11": ("07:00", "19:00"),
"Nicole 13": ("08:00", "18:00"),
"Edgar 14": ("07:00", "19:00"),

Se permite agregar o quitar empleados.
Se permite modificar los horarios laborales de cada empleado.
El horario se expresa en formato HH:MM.

## RANGO DE FECHAS

Formato: dd/mm/yyyy.

Se excluyen sábados y domingos del análisis laboral.

Ejemplo:
Inicio: 01/11/2025
Fin: 30/11/2025

La fecha de fin es inclusiva.

## MÉTODO DE “ANÁLISIS DE EMPLEADO”

Para cada empleado y cada día del rango:

Si es sábado o domingo:

- No se realizan validaciones.
- Se coloca observación: “Fin de semana”.

Si es día laboral:

- Entrada: se toma la hora más temprana registrada.
- Salida: se toma la hora más tardía registrada.
- Si falta entrada → observación: “Faltó entrada”.
- Si falta salida → observación: “Faltó salida”.

Estado (entrada):

- “tarde” si la hora de entrada es posterior al horario laboral del empleado.

Tiempo Total:

- Diferencia entre hora de salida y hora de entrada.

Horas extra:

- Tiempo por encima de la hora de salida del empleado.

Horas perdidas:

- Tiempo que el empleado ingresó después de su hora de entrada.

Observaciones adicionales:

- “Fin de semana”
- “Faltó entrada”
- “Faltó salida”
- (Opcional) “Sin registros”

## ESTRUCTURA DEL “ANÁLISIS DE EMPLEADO”

Fecha | Hora Entrada | Estado | Hora Salida | Tiempo Total | Horas Extras | Horas Perdidas | Observaciones
03/11/2025 | — | — | 19:53 | — | — | — | Faltó entrada
04/11/2025 | 07:03 | — | 22:14 | 15:11 | 03:14 | 00:03 | —
05/11/2025 | 06:47 | — | — | — | — | — | Faltó salida

## RESUMEN GENERAL

- Días totales: número de días laborales en el rango.
- Inasistencias: registros con observaciones “Faltó entrada” o “Faltó salida”.
- Tardanzas: entradas marcadas como “tarde”.
- Días cumplidos: días con entrada y salida correctas.
- Horas extra: suma total del empleado.
- Horas perdidas: suma total del empleado.
- Diferencia: Horas extra − Horas perdidas.

## ESTRUCTURA DEL RESUMEN GENERAL

Trabajador | Días Totales | Inasistencias | Tardanzas | Días Cumplidos | Horas Extra | Horas Perdidas | Diferencia
Mendez 6 | 3 | 0 | 7 | 5 | 5h 52m | 0h 0m | +5h 52m