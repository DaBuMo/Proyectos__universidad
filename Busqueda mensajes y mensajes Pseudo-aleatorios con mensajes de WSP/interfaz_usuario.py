from manejo_mensajes import generador_palabras_personajes,generador_mensajes,contar_aparicion_palabra

FORMATO_CHAT = 'txt'
FORMATO_GUARDADO = 'csv'
CENTRADO_MENSAJE = 150
COMANDO_MINIMO = 0
CONTAR_PALABRAS = 1
GENERAR_MENSAJES = 2
SALIR = 3

def verificacion_comando_valido(comando_usuario:str) -> bool:
    """
    Dado un input por el usuario, la funcion verifica si se encuentra dentro del rango de comandos validos.

    PRECONDICIONES: 
    POSTCONDICION:
        - Retona un booleano segun cumple o incumple la condicion
    """

    if not comando_usuario.isdigit() or int(comando_usuario) < CONTAR_PALABRAS or int(comando_usuario) > SALIR:
       
        print('Error Comando no valido, ingrese un comando valido que se encuentre dentro de la lista dada previamente\n')
        return False
    
    return True

def verificar_existencia_archivo(archivo:str,tipo:str) -> bool:
    """
    Dada la direccion de un archivo y el tipo de archivo que es, verifica que este archivo exista y sea del tipo indicado

    PRECONDICIONES: 
    POSTCONDICION:
        - Si el archivo existe y es del tipo indicado nos devolvera True
    """

    try:
        if len(archivo.split('.')) == 2 and tipo != archivo.split('.')[1] or len(archivo.split('.')) == 1:
            raise FileExistsError
        
        if tipo == FORMATO_GUARDADO:
            with open(archivo,'w') as archivo:
                if tipo == FORMATO_CHAT:
                    print(' Abriendo archivo '.center(CENTRADO_MENSAJE,'-'))
                return True
            
        else: 
            with open(archivo,'r') as archivo:
                if tipo == FORMATO_CHAT:
                    print(' Abriendo archivo '.center(CENTRADO_MENSAJE,'-'))
                return True  
             
    except FileNotFoundError:
        print('Lo siento, Archivo no encontrado, intenta nuevamente')

    except FileExistsError:
        print('El formato de archivo no es el correcto, intenta nuevamente')

def imprimir_usuarios(usuarios:dict) -> str:
    """
    Dado un diccionario creado con la funcion de generador_palabras_personajes, llena la lista con los usuarios que se encuentran en el diccionario, imprime los usuarios y devuelve la lista con todas las llaves que se encuentran en el diccionario y un valor igual a la longitud de la lista de usuarios mas 1 y lo vincula al comando salir

    PRECONDICIONES: 
        - Un diccionario creado con la funcion de generador_palabras_personajes

    POSTCONDICION:
        - Imprime a todos los usuarios presentes en el diccionario y los vincula a un numero
        - Vincula al comando salir a un numero
    """
    
    lista_usuarios = [] 
    print('Contactos:\n')
    
    for comando,llave in enumerate(usuarios.keys()):
       
        print(f'{comando}. {llave}.')
        max_comando = comando
        lista_usuarios.append(llave)
        salir = max_comando+1

    print(f'{salir}. Salir.\n')
    
    return salir, lista_usuarios

def generar_mensaje(usuarios:dict) -> None:
    """
    Dado un diccionario creado con la funcion de generador_palabras_personajes, le pide al usuario que ingrese un comando vinculado a un usuario (Estos se imprimen con la funcion imprimir un usuario), si el comando se encuentra dentro de los impresos, genera un mensaje pseudo-aleatorio del usuario elegido usando la funcion generador_mensajes

    PRECONDICIONES: 
        - Un diccionario creado con la funcion de generador_palabras_personajes.

    POSTCONDICION:
        - Imprime un mensaje pseudo-aleatorio del usuario elegido con el comando.
    """

    while True:

        salir,lista_usuarios = imprimir_usuarios(usuarios)
        
        comando_usuario_generar = input('Ingrese el contacto para generar el mensaje: ')
        print('')
        
        if not comando_usuario_generar.isdigit() or int(comando_usuario_generar) < COMANDO_MINIMO or int(comando_usuario_generar) > salir:
            print('Error Comando no valido, ingrese un comando valido que se encuentre dentro de la lista dada previamente\n')
            continue

        if int(comando_usuario_generar) == salir:
            print('Saliendo del modulo generar mensaje-pseudoaleatorio')
            return
        
        usuario_elegido = lista_usuarios[int(comando_usuario_generar)]
        print(f'MENSAJE: {usuario_elegido}: {generador_mensajes(usuarios,usuario_elegido)}',end='\n\n')

def contar_palabras(direccion_chat:str) -> None:
    """
    Dada la direccion de un archivo de chat de WSP en un dispositivo de Apple, le pide al usuario que introduzca una direccion de guardado para un archivo .csv, despues le pide una cadena de palabras al usuario y despues ejecuta y guarda los resultados de la funcion contar_aparicion_palabra en dicho archivo

    PRECONDICIONES: 
        - La direccion debe ser de un archivo de chat de WSP en un dispositivo de Apple y debe terminar en .txt
        - La direccion del archivo de guardado debera terminar en .csv

    POSTCONDICION:
        - Cuenta cuantas veces los participantes del chat dijeron la palabra o palabra indicadas y guarda los resultados en el archivo .csv
    """

    while True:
    
        direccion_guardado = input('Porfavor ingrese la direccion del archivo de guardado, si el nombre del archivo no es encontrado se creara uno con el nombre indicado en la direccion ingresada (Recuerda que el formato del archivo debera ser .csv): ')

        if verificar_existencia_archivo(direccion_guardado,FORMATO_GUARDADO):
            break

    palabras_buscadas = input('Porfavor ingrese las palabras con las que desea buscar su aparicion en el chat (Recuerde separar cada palabra con un espacio): ')

    contar_aparicion_palabra(palabras_buscadas,direccion_chat,direccion_guardado)

    print('')
    print('Archivo guardado correctamente\n')


def main():

    while True:
        direccion_chat = input('Porfavor ingrese la direccion del archivo que desea abrir (Recuerda que el formato del archivo debera ser .txt): ')
        
        if verificar_existencia_archivo(direccion_chat,FORMATO_CHAT):
            break

    while True:
        
        comando_usuario = input(f'Que desea hacer con el chat.\n\n1.Contar cuantas veces aparece una palabra o un conjunto de palabras.\n\n2.Generar un mensaje pseudo-aleatorio apartir de un contacto.\n\n3.Salir.\n\n')
        
        if not verificacion_comando_valido(comando_usuario):
            continue 

        if int(comando_usuario) == CONTAR_PALABRAS:
            
            contar_palabras(direccion_chat)

        elif int(comando_usuario) == GENERAR_MENSAJES:

            usuarios = {}

            if not usuarios:
                usuarios = generador_palabras_personajes(direccion_chat)
            
            generar_mensaje(usuarios)
            
        elif int(comando_usuario) == SALIR:
            print(' Cerrando archivo '.center(CENTRADO_MENSAJE,'-'))
            break

main()