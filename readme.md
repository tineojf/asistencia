- dame una pagina web para cargar un csv
- lee el csv y procesa los datos
- genera un reporte paso a paso, con la tecla "siguiente"
- primer paso: empleados editables con horarios editables
- segundo paso: seleccionar rango de fechas
- tercer paso: por cada empleado, mostrar la estructura de "analisis de empleado"
- cuarto paso: se muestra un resumen general con totales por empleado

- estructura del csv
  Número,Nombre,Tiempo,Estado,Dispositivos,Tipo de Registro
  1,Elizabeth 1,03/11/2025 08:02:31,Entrada,Asistencia,0
  1,Elizabeth 1,03/11/2025 18:58:51,Salida,Asistencia,0

- empleados (se pueden agregar o quitar empleados, cambiar horarios)
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

- input fecha inicio, fin (formato dd/mm/aaaa)
  No se cuentan sabados ni domingos
  Fecha Inicio: 01/11/2025
  Fecha Fin: 30/11/2025

- metodo de "analisis de empleado"
  Si es sabado o domingo, se cuenta horario de entrada y salida sin comprobaciones, se ignora horas perdidas y en observaciones se pone "Fin de semana"
  Si no hay registros de entrada o salida en un dia laboral, se cuenta como inasistencia, en observaciones se pone "Faltó entrada" o "Faltó salida"
  En hora de entrada, se escoge la hora minima registrada en ese dia
  En Estado, se pone "tarde" si la hora de entrada es mayor a la hora inicial del empleado
  En hora de salida, se escoge la hora maxima registrada en ese dia
  Tiempo total es la diferencia entre hora de salida y hora de entrada
  Horas extra es la diferencia entre la hora de salida y la hora final del empleado solo si la hora de salida es mayor a la hora final del empleado
  Horas perdidas es la diferencia entre la hora inicial del empleado y la hora de entrada solo si la hora de entrada es mayor a la hora inicial del empleado
  En observaciones se pone cualquier detalle relevante (faltó entrada, faltó salida, fin de semana)
  Se repite el proceso para cada dia en el rango de fechas seleccionado

- estructura "análisis de empleado"
  Fecha Hora Entrada Estado Hora Salida Tiempo Total Horas Extras Horas Perdidas Obs.
  03/11/2025 19:53 Faltó entrada
  04/11/2025 07:03 22:14 15:11:00 3:14:00 0:03:00
  05/11/2025 06:47 Faltó salida
  10/11/2025 07:06 0:06:00 Faltó salida
  13/11/2025 07:46 18:37 10:51:00 0:46:00

- metodo "resumen general"
  Dias totales en el periodo: Número de días entre la fecha inicio y fin
  Inasistencias: se cuenta cada registro de "analisis de empleado" en la columna de observaciones que indique falta de entrada o salida
  Tardanzas: se cuenta cada registro de "analisis de empleado" en la columna de estado que indique "tarde"
  Días cumplidos: días con registros completos de entrada y salida
  Horas extra: suma cada registro de "analisis de empleado" en la columna de horas extra
  Horas perdidas: suma cada registro de "analisis de empleado" en la columna de horas perdidas
  Diferencia: Horas extra menos horas perdidas

- estructura "resumen general"
  Trabajador Dias totales Inasistencias Tardanzas Días Cumplidos Horas Extra Horas Perdidas Diferencia
  Mendez 6 3 0 7 5h 52m 0h 0m +5h 52m

