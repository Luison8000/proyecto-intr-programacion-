Algoritmo Pseudo_menu
	Definir opcion_menu,opcion_organizador,opcion_jugador Como Entero
	Definir usuario,contrasena Como Caracter
	Repetir
		Escribir '1 Organizador'
		Escribir '2 Jugador'
		Escribir '3 Salir'
		Leer opcion_menu
		Segun opcion_menu  Hacer
			1:
				Repetir
					Escribir 'Menu organizador'
					Escribir '1 Registrar cantidad de canchas'
					Escribir '2 Registrar sparrings disponibles'
					Escribir '4 Registrar jugadores (usuario y contraseña)'
					Escribir '5 Volver al menú principal'
					Leer opcion_organizador
					Segun opcion_organizador  Hacer
						1:
							Escribir 'Registrar canchas compartidas'
							Escribir 'Registrar canchas sesion privada'
						2:
							Escribir 'Registrar cantidad de sparrings'
						3:
							Escribir 'Registrar jugador con usuario y contraseña'
						4:
							Escribir 'regresar al menu principal'
					FinSegun
				Hasta Que opcion_organizador=4
			2:
				Repetir
					Escribir 'Menu Jugador'
					Escribir 'Ingrese su usuario y contraseña'
					Leer usuario
					Leer contrasena
					Escribir '1 Registrar entrenador'
					Escribir '2 Registrar invitado'
					Escribir '3 Reservar cancha'
					Escribir '4 Volver al menu principal'
					Leer opcion_jugador
					Segun opcion_jugador  Hacer
						1:
							Escribir 'Registrar entrenador'
						2:
							Escribir 'Registrar invitado'
						3:
							Escribir 'Reservar cancha (1 jugador o 2)'
						4:
							Escribir 'Indicar cuántas botellas de agua'
						5:
							Escribir 'regresar al menu pricipal'
					FinSegun
				Hasta Que opcion_jugador=5
			3:
				Escribir 'fin del programa'
			De Otro Modo:
				Escribir 'Error.'
		FinSegun
	Hasta Que opcion_menu=3
FinAlgoritmo

