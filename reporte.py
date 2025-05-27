import csv
from datetime import datetime, date, timedelta
import calendar

archivo_entrada = "asistencia.csv"
archivo_salida = "reporte_diario.csv"


# Funcion - excluir nombres
def obtener_trabajadores_con_exclusion():

    lista_trabajadores = obtener_trabajadores()
    nombres_excluidos = {"Frank 8", "Miguel 9"}

    trabajadores_filtrados = [
        nombre for nombre in lista_trabajadores if nombre not in nombres_excluidos
    ]
    return tuple(trabajadores_filtrados)


# Funcion - retorna una tupla con los trabajadores
def obtener_trabajadores():
    set_trabajadores = set()

    with open(archivo_entrada, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            set_trabajadores.add(fila["Nombre"])

    return tuple(set_trabajadores)


for i in obtener_trabajadores_con_exclusion():
    print(i)


# lista de fecha, hora, estado
# funcion para sumar asistencia, tardanza, dias, horas extra, horas perdidas

# modificar que saque los usuarios de un archivo csv - filtrando la columna
trabajadores = (
    "Elizabeth 1",
    "Principe 2",
    "Orlando 3",
    "Chino 4",
    "Wilmer 5",
    "Mendez 6",
    "Vallejo 7",
    "Frank 8",
    "Miguel 9",
    "Juan 10",
    "Teofilo 11",
)

obj_trabajadores = {
    trabajadores[0]: {},
    trabajadores[1]: {},
    trabajadores[2]: {},
    trabajadores[3]: {},
    trabajadores[4]: {},
    trabajadores[5]: {},
    trabajadores[6]: {},
    trabajadores[7]: {},
    trabajadores[8]: {},
    trabajadores[9]: {},
    trabajadores[10]: {},
}

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


def obtener_mes_actual():
    fecha_actual = datetime.now()
    return fecha_actual.month


def obtener_mes_actual_formato():
    fecha_actual = datetime.now()
    return fecha_actual.strftime("%m")


def obtener_dias_laborables(quincena):
    mes = obtener_mes_actual()
    anio = datetime.now().year

    if quincena == "primera":
        inicio = date(anio, mes, 1)
        fin = date(anio, mes, 15)
    elif quincena == "segunda":
        ultimo_dia = calendar.monthrange(anio, mes)[1]
        inicio = date(anio, mes, 16)
        fin = date(anio, mes, ultimo_dia)
    else:
        raise ValueError("La quincena debe ser 'primera' o 'segunda'.")

    dias_laborables = []
    dia = inicio
    while dia <= fin:
        # Lunes-0 a sabado-5
        if dia.weekday() < 6:
            dias_laborables.append(dia.strftime("%d/%m/%Y"))
        dia += timedelta(days=1)

    return dias_laborables


def obtener_dias_laborables_desde_dia(dia_inicio):
    mes = obtener_mes_actual()
    anio = datetime.now().year
    hoy = datetime.now().date()

    if dia_inicio > hoy.day:
        raise ValueError(
            f"El día de inicio ({dia_inicio}) no puede ser mayor que hoy ({hoy.day})."
        )

    if not (1 <= dia_inicio <= calendar.monthrange(anio, mes)[1]):
        raise ValueError(
            f"El día debe estar entre 1 y {calendar.monthrange(anio, mes)[1]}."
        )

    inicio = date(anio, mes, dia_inicio)
    fin = hoy

    dias_laborables = []
    dia = inicio
    while dia <= fin:
        if dia.weekday() < 6:  # Lunes a sábado
            dias_laborables.append(dia.strftime("%d/%m/%Y"))
        dia += timedelta(days=1)

    return dias_laborables


def obtener_total_dias_laborables(dias_laborables):
    return len(dias_laborables)


def cargar_registros_por_trabajador(archivo_csv, trabajadores):
    obj_trabajadores = {trabajador: [] for trabajador in trabajadores}

    with open(archivo_csv, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            nombre_fila = fila["Nombre"].strip()

            for trabajador in trabajadores:
                if nombre_fila == trabajador:
                    registro = {
                        "Tiempo": fila["Tiempo"],
                        "Estado": fila["Estado"],
                    }
                    obj_trabajadores[trabajador].append(registro)
                    break

    return obj_trabajadores
