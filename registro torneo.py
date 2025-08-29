import tkinter as tk
from tkinter import messagebox, simpledialog

# Listas globales 
# listas de canchass,reservas,jugadores
canchas_disponibles = []     
reservas_realizadas = []     
jugadores_registrados = []   

# Funciones del Organizador 

def registrar_canchas():
    
   # Permite al organizador registrar las canchas disponibles.
   # Se pregunta la cantidad total de canchas y cuántas serán de 2 jugadores.
   # El resto serán de 1 jugador. Se guardan en la lista canchas_disponibles.
    
    total_canchas = simpledialog.askinteger("Canchas", "Ingrese la cantidad total de canchas:")
    if total_canchas is None or total_canchas <= 0:
        return
    
    canchas_dos_jugadores = simpledialog.askinteger("Canchas", "Cantidad de canchas para 2 jugadores:")
    canchas_uno_jugador = total_canchas - canchas_dos_jugadores
    
    # Validación de cantidades
    if canchas_dos_jugadores < 0 or canchas_uno_jugador < 0:
        messagebox.showerror("Error", "Cantidad inválida")
        return
    
    # Limpiar y registrar nuevamente
    canchas_disponibles.clear()
    for i in range(1, canchas_dos_jugadores + 1):
        canchas_disponibles.append({"id": i, "tipo": "dos", "disponible": True})
    for i in range(canchas_dos_jugadores + 1, total_canchas + 1):
        canchas_disponibles.append({"id": i, "tipo": "uno", "disponible": True})
    
    # Confirmación
    messagebox.showinfo("Éxito", f"Canchas registradas.\n2 jugadores: {canchas_dos_jugadores}\n1 jugador: {canchas_uno_jugador}")


def ver_reservas_generales():
    
#Muestra todas las reservas que se han realizado.
# Si no hay reservas, se muestra un mensaje.
    
    if not reservas_realizadas:
        messagebox.showinfo("Reservas generales", "No hay reservas registradas")
        return
    
    texto = ""
    for r in reservas_realizadas:
        equipo = ", ".join(r.get("equipo", [])) if r.get("equipo") else "Sin equipo"
        texto += (f"Jugador: {r['usuario']}\nEquipo: {equipo}\nCancha: {r['id_cancha']}\n"
                  f"Fecha: {r['fecha']}\nHora: {r['hora']}\nBotellas de agua: {r['botellas']}\n---\n")
    
    messagebox.showinfo("Reservas generales", texto)


def abrir_ventana_organizador():
    
   # Abre una ventana secundaria para el organizador
  #  con opciones de registrar canchas y ver reservas generales.
    
    ventana_org = tk.Toplevel(root)
    ventana_org.title("Organizador")
    
    tk.Label(ventana_org, text="Menú Organizador").pack(pady=10)
    tk.Button(ventana_org, text="Registrar canchas", width=25, command=registrar_canchas).pack(pady=5)
    tk.Button(ventana_org, text="Ver reservas generales", width=25, command=ver_reservas_generales).pack(pady=5)
    tk.Button(ventana_org, text="Cerrar", width=25, command=ventana_org.destroy).pack(pady=5)

# Funciones de Jugador 

def registrar_nuevo_jugador():
    
    # Registra un nuevo jugador con usuario, contraseña y su equipo.
    # Valida que el usuario no esté previamente registrado.
    
    usuario = simpledialog.askstring("Registro", "Ingrese usuario:")
    
    # Verificar que no esté duplicado
    if any(j["usuario"] == usuario for j in jugadores_registrados):
        messagebox.showerror("Error", "Usuario ya registrado")
        return
    
    contrasena = simpledialog.askstring("Registro", "Ingrese contraseña:")
    equipo = simpledialog.askstring("Registro", "Ingrese miembros de su equipo separados por comas:")
    
    # Transformar string a lista de jugadores
    lista_equipo = [x.strip() for x in equipo.split(",")] if equipo else []
    
    # Registrar jugador
    jugadores_registrados.append({"usuario": usuario, "contrasena": contrasena, "equipo": lista_equipo})
    messagebox.showinfo("Éxito", f"Jugador registrado: {usuario}")


def login_jugador():
    
   # Realiza el login de un jugador solicitando usuario y contraseña.
  #  Si coincide, devuelve el jugador (diccionario).
    
    usuario = simpledialog.askstring("Login", "Usuario:")
    contrasena = simpledialog.askstring("Login", "Contraseña:")
    
    for j in jugadores_registrados:
        if j["usuario"] == usuario and j["contrasena"] == contrasena:
            return j
    
    messagebox.showerror("Error", "Usuario o contraseña incorrecta")
    return None


def seleccionar_fecha():
    
  #  Permite seleccionar la fecha de entrenamiento: hoy o mañana.
    
    opcion_fecha = simpledialog.askstring("Reserva", "Seleccione fecha: 'hoy' o 'mañana'").lower()
    while opcion_fecha not in ["hoy", "mañana"]:
        messagebox.showerror("Error", "Debe seleccionar 'hoy' o 'mañana'")
        opcion_fecha = simpledialog.askstring("Reserva", "Seleccione fecha: 'hoy' o 'mañana'").lower()
    
    return "Hoy" if opcion_fecha == "hoy" else "Mañana"


def seleccionar_hora():
    
   # Permite seleccionar la hora de inicio de entrenamiento (7 a 21 hrs).
    
    hora = simpledialog.askinteger("Hora de entrenamiento", "Ingrese la hora de inicio (7-21):")
    while hora is None or hora < 7 or hora > 21:
        messagebox.showerror("Error", "Debe ingresar una hora entre 7 y 21")
        hora = simpledialog.askinteger("Hora de entrenamiento", "Ingrese la hora de inicio (7-21):")
    return hora


def mostrar_canchas_disponibles(tipo_cancha, fecha_entrenamiento, hora_entrenamiento, duracion=2):
    
 #   Devuelve una lista con las canchas disponibles según el tipo, fecha y hora.
 #  Verifica que no haya cruce de horarios con reservas existentes.
    
    disponibles = []
    
    for c in canchas_disponibles:
        if c["tipo"] == tipo_cancha:
            ocupada = False
            for r in reservas_realizadas:
                if r["id_cancha"] == c["id"] and r["fecha"] == fecha_entrenamiento:
                    # Verificar cruce de horario
                    inicio_reserva = r["hora"]
                    fin_reserva = inicio_reserva + r["duracion"]
                    fin_nueva = hora_entrenamiento + duracion
                    if (inicio_reserva < fin_nueva) and (hora_entrenamiento < fin_reserva):
                        ocupada = True
            if not ocupada:
                disponibles.append(c["id"])
    return disponibles


def crear_reserva(jugador):
    
#  Crea una reserva para un jugador:
# - Pide fecha, hora y tipo de cancha
#- Verifica límite de 3 reservas por día
#- Pregunta cantidad de botellas de agua
    
    fecha_entrenamiento = seleccionar_fecha()
    hora_entrenamiento = seleccionar_hora()
    
    # Validación: máximo 3 reservas al día
    contador_reservas = sum(1 for r in reservas_realizadas if r["usuario"] == jugador["usuario"] and r["fecha"] == fecha_entrenamiento)
    if contador_reservas >= 3:
        messagebox.showerror("Error", "Ya tiene 3 reservas ese día")
        return
    
    # Tipo de cancha
    tipo_opcion = simpledialog.askinteger("Reserva", "Tipo de cancha: 1. cancha compartida 2. sesión privada")
    tipo_cancha = "dos" if tipo_opcion == 1 else "uno"
    
    # Canchas disponibles
    disponibles = mostrar_canchas_disponibles(tipo_cancha, fecha_entrenamiento, hora_entrenamiento)
    if not disponibles:
        messagebox.showerror("Error", "No hay canchas disponibles")
        return
    
    id_cancha = simpledialog.askinteger("Reserva", f"Canchas disponibles: {disponibles}\nIngrese nro de la cancha:")
    botellas_agua = simpledialog.askinteger("Agua", "Número de botellas de agua necesarias:")
    
    # Guardar la reserva
    reservas_realizadas.append({
        "usuario": jugador["usuario"],
        "fecha": fecha_entrenamiento,
        "hora": hora_entrenamiento,
        "duracion": 2,
        "id_cancha": id_cancha,
        "botellas": botellas_agua,
        "equipo": jugador.get("equipo", [])
    })
    
    messagebox.showinfo("Éxito", f"Reserva creada para {jugador['usuario']} en la cancha {id_cancha}.\nEquipo: {', '.join(jugador.get('equipo', []))}\nBotellas de agua: {botellas_agua}")


def ver_reservas(jugador):
    
  #  Muestra todas las reservas del jugador que inició sesión.
    
    texto = ""
    for r in reservas_realizadas:
        if r["usuario"] == jugador["usuario"]:
            equipo = ", ".join(r.get("equipo", [])) if r.get("equipo") else "Sin equipo"
            texto += (f"Jugador: {r['usuario']}\nEquipo: {equipo}\nCancha: {r['id_cancha']}\n"
                      f"Hora: {r['hora']}\nBotellas de agua: {r['botellas']} \n")
    if texto == "":
        texto = "No tiene reservas"
    messagebox.showinfo("Mis Reservas", texto)


def abrir_ventana_jugador():
    
  #  Abre la ventana de jugador tras hacer login.
  #  Contiene opciones para crear reservas y ver sus reservas.
    
    jugador = login_jugador()
    if not jugador:
        return
    
    ventana_j = tk.Toplevel(root)
    ventana_j.title(f"Jugador: {jugador['usuario']}")
    
    tk.Button(ventana_j, text="Crear reserva", width=25, command=lambda: crear_reserva(jugador)).pack(pady=5)
    tk.Button(ventana_j, text="Ver mis reservas", width=25, command=lambda: ver_reservas(jugador)).pack(pady=5)
    tk.Button(ventana_j, text="Cerrar", width=25, command=ventana_j.destroy).pack(pady=5)

#ventana principal

root = tk.Tk()
root.title("Sistema de Reservas - Torneo Challenger ATP")
root.geometry("400x300")

tk.Label(root, text="Menú Principal").pack(pady=10)
tk.Button(root, text="Organizador", width=25, command=abrir_ventana_organizador).pack(pady=5)
tk.Button(root, text="Registrar nuevo jugador", width=25, command=registrar_nuevo_jugador).pack(pady=5)
tk.Button(root, text="Jugador", width=25, command=abrir_ventana_jugador).pack(pady=5)
tk.Button(root, text="Salir", width=25, command=root.destroy).pack(pady=5)

# Mantener la ventana abierta
root.mainloop()
