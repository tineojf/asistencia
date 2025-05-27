import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Archivos
archivo_entrada = "asistencia.csv"
archivo_salida_detalle = "reporte_diario.csv"
archivo_resumen = "resumen_trabajadores.csv"

# Leer datos del CSV
registros = []
with open(archivo_entrada, newline="", encoding="utf-8") as csvfile:
    lector = csv.DictReader(csvfile)
    for fila in lector:
        dt = datetime.strptime(fila["Tiempo"], "%d/%m/%Y %H:%M:%S")

        # Limpieza del nombre: tomar solo la primera palabra y capitalizarla
        nombre_limpio = fila["Nombre"].split()[0].capitalize()

        registros.append(
            {
                "fecha": dt.date(),
                "nombre": nombre_limpio,
                "hora": dt.time(),
                "estado": fila["Estado"],
                "orden": dt,
            }
        )


# Ordenar registros por fecha y hora
registros.sort(key=lambda x: x["orden"])

# Guardar reporte diario detallado
with open(archivo_salida_detalle, "w", newline="", encoding="utf-8") as csvfile:
    campos = ["Fecha", "Nombre", "Hora", "Estado"]
    escritor = csv.DictWriter(csvfile, fieldnames=campos)
    escritor.writeheader()
    for r in registros:
        escritor.writerow(
            {
                "Fecha": r["fecha"].strftime("%d/%m/%Y"),
                "Nombre": r["nombre"],
                "Hora": r["hora"].strftime("%H:%M:%S"),
                "Estado": r["estado"],
            }
        )

print(f"✅ Reporte diario generado: {archivo_salida_detalle}")

# --------- ANALISIS DE ASISTENCIA ---------

# Definir horarios de los trabajadores
horarios_trabajadores = {
    "Chino": ("07:00", "19:00"),
    "Javier": ("07:00", "19:00"),
    "Teofilo": ("07:00", "19:00"),
    "Juan": ("07:00", "19:00"),
    "Cesar": ("07:00", "19:00"),
    "Ronal": ("07:00", "19:00"),
    "Elizabeth": ("08:00", "17:00"),
    "Orlando": ("08:00", "17:00"),
    "Mendez": ("08:00", "17:00"),
    "Principe": ("08:00", "17:00"),
    "Vallejo": ("08:00", "17:00"),
    "Frank": ("08:00", "17:00"),
    "Miguel": ("08:00", "17:00"),
}


# Tolerancia de 15 minutos
tolerancia = timedelta(minutes=15)

# Construir diccionario de asistencias por trabajador y día
asistencias = defaultdict(lambda: defaultdict(list))
for r in registros:
    asistencias[r["nombre"]][r["fecha"]].append(r["hora"])

# Determinar rango de fechas (solo días laborables)
fechas_registradas = [r["fecha"] for r in registros]
fecha_inicio = min(fechas_registradas)
fecha_fin = max(fechas_registradas)
dias_laborables = [
    fecha_inicio + timedelta(days=i)
    for i in range((fecha_fin - fecha_inicio).days + 1)
    if (fecha_inicio + timedelta(days=i)).weekday() < 5
]

# Calcular resumen
resumen = defaultdict(
    lambda: {"asistencias": 0, "tardanzas": 0, "horas_extra": 0, "horas_perdidas": 0}
)

for trabajador, (h_entrada_str, h_salida_str) in horarios_trabajadores.items():
    hora_entrada = datetime.strptime(h_entrada_str, "%H:%M").time()
    hora_salida = datetime.strptime(h_salida_str, "%H:%M").time()

    for dia in dias_laborables:
        entradas = asistencias[trabajador].get(dia, [])
        if not entradas:
            resumen[trabajador]["horas_perdidas"] += 1
        else:
            hora_min = min(entradas)
            hora_max = max(entradas)

            # Construir datetime con fecha y hora para comparar con tolerancia
            dt_entrada_programada = datetime.combine(dia, hora_entrada) + tolerancia
            dt_salida_programada = datetime.combine(dia, hora_salida) + tolerancia
            dt_entrada_real = datetime.combine(dia, hora_min)
            dt_salida_real = datetime.combine(dia, hora_max)

            # Verificar asistencia o tardanza con tolerancia
            if dt_entrada_real <= dt_entrada_programada:
                resumen[trabajador]["asistencias"] += 1
            else:
                resumen[trabajador]["tardanzas"] += 1

            # Verificar horas extra con tolerancia
            if dt_salida_real > dt_salida_programada:
                resumen[trabajador]["horas_extra"] += 1

# Mostrar resumen en consola
print("\n📊 Resumen final por trabajador:")
for nombre, datos in resumen.items():
    print(f"{nombre}: {datos}")

# Guardar resumen en CSV
with open(archivo_resumen, "w", newline="", encoding="utf-8") as csvfile:
    campos = ["Nombre", "Asistencias", "Tardanzas", "Horas Extra", "Horas Perdidas"]
    escritor = csv.DictWriter(csvfile, fieldnames=campos)
    escritor.writeheader()
    for nombre, datos in resumen.items():
        escritor.writerow(
            {
                "Nombre": nombre,
                "Asistencias": datos["asistencias"],
                "Tardanzas": datos["tardanzas"],
                "Horas Extra": datos["horas_extra"],
                "Horas Perdidas": datos["horas_perdidas"],
            }
        )

print(f"✅ Resumen de trabajadores generado: {archivo_resumen}")
