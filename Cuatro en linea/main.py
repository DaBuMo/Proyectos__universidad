from cuatro_en_linea import crear_tablero,tablero_completo,insertar_simbolo,es_turno_de_x,obtener_ganador,imprimir_tablero,FICHA_JUGADOR_1,FICHA_JUGADOR_2,CELDAS,CARACTER_SALIDA

def validacion_comando(comando_usuario,ancho_tablero):
    if comando_usuario == "":
        print(f"La entrada esta vacia, recuerda ingresar un valor numerico\n")
        return False
    
    elif not comando_usuario.isdigit():
        print(f"La entrada {comando_usuario} no es un entero\n")
        return False
    
    elif int(comando_usuario) < 0 or int(comando_usuario) >= ancho_tablero:
        print(f"La entrada {comando_usuario} no esta dentro de las columnas del tablero\n")
        return False
    
    return True

def main():
    
    alto =  input("Ingrese el alto del tablero (Entre 4 y 10): ")
    while alto == "" or (not alto.isdigit()) or int(alto) <= 3 or int(alto) > 10:
        alto = input("Porfavor ingrese un alto valido, recuerda que tiene que ser un numero y tiene que estar entre 4 y 10: ")
    
    ancho = input("Ingrese el ancho del tablero (Entre 4 y 10): ")
    while ancho == "" or (not ancho.isdigit()) or int(ancho) <= 3 or int(ancho) > 10:
        ancho = input("Porfavor ingrese un ancho valido, recuerda que tiene que ser un numero y tiene que estar entre 4 y 10: \n")
    
    alto = int(alto)
    ancho = int(ancho)

    print("")
    tablero_juego = crear_tablero(alto,ancho)
    imprimir_tablero(tablero_juego)

    while not tablero_completo(tablero_juego):
        
        if es_turno_de_x(tablero_juego):
            comando_usuario = input(f"Turno de {FICHA_JUGADOR_1}, elegir una columna entre 0 y {ancho-1} o introduce el caracter \"{CARACTER_SALIDA}\" si deseas salir: ")
        else:
            comando_usuario = input(f"Turno de {FICHA_JUGADOR_2}, elegir una columna entre 0 y {ancho-1} o introduce el caracter \"{CARACTER_SALIDA}\" si deseas salir: ")
        print("")

        if comando_usuario.lower() == CARACTER_SALIDA:
            print(f"Se introdujo el comando \"{comando_usuario.lower()}\", no hubieron ganadores.")
            print("Cerrando Juego".center(48, "-"))
            break
        
        elif not validacion_comando(comando_usuario,ancho):
            continue

        if not insertar_simbolo(tablero_juego,int(comando_usuario)):
            print(f"Porfavor elije otra columna, la columna {comando_usuario} esta llena\n")
            continue
        else:
            imprimir_tablero(tablero_juego)

        ganador = obtener_ganador(tablero_juego)
        
        if ganador != CELDAS:
            imprimir_tablero(tablero_juego)
            print(f" GANO {ganador} ".center(48,"-"))
            break

    ganador = obtener_ganador(tablero_juego)
    if ganador == CELDAS and comando_usuario.lower() != CARACTER_SALIDA:
        print("Tablero lleno, no hubo ganador")

main()