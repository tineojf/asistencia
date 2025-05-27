import csv
import datetime

archivo_entrada = "asistencia2.csv"
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
    return {item: [] for item in tupla}


# Funcion - retorna lista con dias trabajados
def dias_trabajables_desde_intervalo_csv():
    with open(archivo_intervalo, mode="r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        fila = next(lector)
        fecha_inicio = datetime.datetime.strptime(fila[0], "%d/%m/%Y").date()

    fecha_fin = datetime.date.today() - datetime.timedelta(days=1)

    dias_laborables = []
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() <= 5:  # lunes a sábado
            dias_laborables.append(fecha_actual.strftime("%d/%m/%Y"))
        fecha_actual += datetime.timedelta(days=1)

    return dias_laborables


# Funcion - cargar registros por trabajador
def agregar_registros_a_obj(obj):
    with open(archivo_entrada, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            nombre = fila["Nombre"]
            if nombre in obj:
                registro_filtrado = {
                    "Tiempo": fila["Tiempo"],
                    "Estado": fila["Estado"],
                }
                obj[nombre].append(registro_filtrado)
    return obj


# Funcion - mostrar registros por trabajador
def mostrar_registros_por_trabajador(obj):
    for trabajador, registros in obj.items():
        print(f"\n🧑 Trabajador: {trabajador}")
        if not registros:
            print("  (Sin registros)")
        else:
            for fila in registros:
                tiempo = fila["Tiempo"]
                estado = fila["Estado"]
                print(f"  • {tiempo} | {estado}")


# Funcion - mostrar reporte
def generar_reporte_asistencia(obj_asistencia, dias_trabajables):
    reporte = {}

    for trabajador, registros in obj_asistencia.items():
        reporte[trabajador] = []

        for dia in dias_trabajables:
            entrada = None
            salida = None

            for reg in registros:
                try:
                    fecha_hora = datetime.datetime.strptime(
                        reg["Tiempo"], "%d/%m/%Y %H:%M:%S"
                    )
                except ValueError:
                    continue  # saltar registros mal formateados

                if fecha_hora.strftime("%d/%m/%Y") == dia:
                    if reg["Estado"] == "Entrada" and (
                        not entrada or fecha_hora < entrada
                    ):
                        entrada = fecha_hora
                    elif reg["Estado"] == "Salida" and (
                        not salida or fecha_hora > salida
                    ):
                        salida = fecha_hora

            observaciones = ""
            tiempo_total = ""

            if entrada and salida:
                diff = salida - entrada
                horas, rem = divmod(diff.seconds, 3600)
                minutos = rem // 60
                tiempo_total = f"{horas}h {minutos}m"
            elif not entrada and not salida:
                observaciones = "Sin marcas"
            elif not entrada:
                observaciones = "Faltó entrada"
            elif not salida:
                observaciones = "Faltó salida"

            reporte[trabajador].append(
                {
                    "Fecha": dia,
                    "Hora Entrada": entrada.strftime("%H:%M") if entrada else "",
                    "Hora Salida": salida.strftime("%H:%M") if salida else "",
                    "Tiempo Total": tiempo_total,
                    "Observaciones": observaciones,
                }
            )

    return reporte


# Main
trabajadores = obtener_trabajadores()
obj_trabajadores = crear_obj_trabajadores(trabajadores)
objt_trabajadores_asistencia = agregar_registros_a_obj(obj_trabajadores)
dias_laborables = dias_trabajables_desde_intervalo_csv()
reporte_final = generar_reporte_asistencia(objt_trabajadores_asistencia, dias_laborables)
print(reporte_final)
# Mostrar reporte formateado
for trabajador, dias in reporte_final.items():
    print(f"\n🧑 {trabajador}")
    for dia in dias:
        print(f"📅 {dia['Fecha']}: Entrada: {dia['Hora Entrada']} - Salida: {dia['Hora Salida']} - "
              f"Total: {dia['Tiempo Total']} - Obs: {dia['Observaciones']}")
