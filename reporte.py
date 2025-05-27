import csv
import datetime

archivo_entrada = "asistencia.csv"
archivo_salida = "reporte_diario.csv"
archivo_intervalo = "intervalo.csv"
horarios = {
    "Elizabeth 1": ("08:00", "17:00"),
    "Orlando 3": ("08:00", "1:00"),
    "Principe 2": ("07:00", "19:00"),  # No confirmado
    "Juan 10": ("07:00", "19:00"),  # No confirmado
    "Chino 4": ("07:00", "19:00"),  # No confirmado
    "Vallejo 7": ("07:00", "19:00"),  # No confirmado
    "Mendez 6": ("07:00", "19:00"),  # No confirmado
    "Teofilo 11": ("07:00", "19:00"),  # No confirmado
}


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


# Funcion - retorna objeto con los trabajadores y sus registros
def crear_obj_trabajadores(tupla):
    return {item: {} for item in tupla}


# Funcion - retorna lista con dias trabajados
def dias_trabajables_desde_intervalo_csv():
    with open(archivo_intervalo, mode="r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        fila = next(lector)
        fecha_inicio = datetime.datetime.strptime(fila[0], "%d/%m/%Y").date()

    fecha_fin = datetime.date.today() - datetime.timedelta(days=1)  # Ayer

    dias_laborables = []
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() <= 5:  # lunes a sábado
            dias_laborables.append(fecha_actual.strftime("%d/%m/%Y"))
        fecha_actual += datetime.timedelta(days=1)

    return dias_laborables


# Main
trabajadores = obtener_trabajadores_con_exclusion()
obj_trabajadores = crear_obj_trabajadores(trabajadores)
# print(obj_trabajadores)
# print(dias_trabajables_desde_intervalo_csv())


# def cargar_registros_por_trabajador(archivo_csv, trabajadores):
# obj_trabajadores = {trabajador: [] for trabajador in trabajadores}
#
# with open(archivo_csv, newline="", encoding="utf-8") as archivo:
# lector = csv.DictReader(archivo)
#
# for fila in lector:
# nombre_fila = fila["Nombre"].strip()
#
# for trabajador in trabajadores:
# if nombre_fila == trabajador:
# registro = {
# "Tiempo": fila["Tiempo"],
# "Estado": fila["Estado"],
# }
# obj_trabajadores[trabajador].append(registro)
# break
#
# return obj_trabajadores
#
