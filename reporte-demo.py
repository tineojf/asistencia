import csv
from datetime import datetime

# Archivos
archivo_entrada = "asistencia.csv"
archivo_salida = "reporte_diario.csv"

# Leer datos del CSV
registros = []
with open(archivo_entrada, newline="", encoding="utf-8") as csvfile:
    lector = csv.DictReader(csvfile)
    for fila in lector:
        # Convertir string de fecha y hora
        dt = datetime.strptime(fila["Tiempo"], "%d/%m/%Y %H:%M:%S")
        registros.append(
            {
                "fecha": dt.strftime("%d/%m/%Y"),
                "nombre": fila["Nombre"],
                "hora": dt.strftime("%H:%M:%S"),
                "estado": fila["Estado"],
                "orden": dt,  # Para ordenar correctamente
            }
        )

# Ordenar por fecha y hora
registros.sort(key=lambda x: x["orden"])

# Escribir reporte
with open(archivo_salida, "w", newline="", encoding="utf-8") as csvfile:
    campos = ["Fecha", "Nombre", "Hora", "Estado"]
    escritor = csv.DictWriter(csvfile, fieldnames=campos)
    escritor.writeheader()
    for r in registros:
        escritor.writerow(
            {
                "Fecha": r["fecha"],
                "Nombre": r["nombre"],
                "Hora": r["hora"],
                "Estado": r["estado"],
            }
        )

print(f"✅ Reporte generado correctamente: {archivo_salida}")


# lista de trabajadores
# intervalo de fechas
# cantidad de dias laborables
# lista de horarios
# lista de fecha, hora, estado
# funcion para sumar asistencia, tardanza, dias, horas extra, horas perdidas

trabajadores = (
    "Elizabeth 1",
    "Principe 2",
    "Orlando 3",
    "Chino 4",
    "Mendez 6",
    "Vallejo 7",
    "Frank 8",
    "Miguel 9",
    "Juan 10",
    "Teofilo 11",
)

horarios = {
    "dia": {
        "hora_entrada": "08:00",
        "hora_salida": "18:00",
    },
    "noche": {
        "hora_entrada": "18:00",
        "hora_salida": "06:00",
    },
    "oficina": {
        "hora_entrada": "08:00",
        "hora_salida": "17:00",
    },
}


def obtener_mes_actual_formato():
    fecha_actual = datetime.now()
    return fecha_actual.strftime("%m")


dias_laborables = {}
