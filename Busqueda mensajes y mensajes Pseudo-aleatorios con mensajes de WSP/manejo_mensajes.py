import csv
import random

SEPARADOR_TIEMPO_MENSAJE = ']'
SEPARADOR_EMISOR_MENSAJE = ':'

INDICE_CREACION_GRUPO_1 = 'creó'
INDICE_CREACION_GRUPO_2 = 'el'
INDICE_CREACION_GRUPO_3 = 'grupo'
INDICE_CREACION_GRUPO_4 = 'añadió'

INDICE_MEDIA = '[\u200esticker'
INDICE_MEDIA_2 = 'omitido'

LLAVE_PALABRA_INICIALES = 'palabra_iniciales'
LLAVE_CONTADOR_PALABRA = 'contador_palabra'

FIN_DE_LINEA = '\n'

INDICE_EMISOR_Y_MENSAJE = 1

INDICE_PALABRA_INICIAL = 0

INDICE_EMISOR = 0
INDICE_MENSAJE = 1

MENSAJE_REPETIDO_EMISOR = 0
MENSAJE_REPETIDO_PALABRA = 1
MENSAJE_REPETIDO_CONTADOR = 2

INICIO_DE_ORACION = 'IO'
CONECTOR_DE_ORACION = 'CO'
FIN_DE_ORACION = 'FO'

PALABRA = 0
PROBABILIDADES = 1
CONTINUIDAD = 2
CONTINUIDAD_GENERADAS = 1

CABECERA = ('Contacto','Palabra','Frencuencia')

def recuperar_emisor_y_mensaje(mensaje:str) -> str|list[str]:
    """
    Dado un mensaje WSP codificado en un dispositivo de Apple, devuelve el nombre del emisor del mensaje y el mensaje separado en una lista palabra por palabra.

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado en dispositivo Apple.

    POSTCONDICION:
        - Retorna dos valores, primero el nombre del emisor del mensaje y despues una lista con cada palabra que tenia el mensaje que estaba separada por un espacio
    """
    
    emisor = mensaje.rstrip(FIN_DE_LINEA).split(SEPARADOR_TIEMPO_MENSAJE)[INDICE_EMISOR_Y_MENSAJE].split(SEPARADOR_EMISOR_MENSAJE)[INDICE_EMISOR].strip()
    mensaje = mensaje.rstrip(FIN_DE_LINEA).split(SEPARADOR_TIEMPO_MENSAJE)[INDICE_EMISOR_Y_MENSAJE].split(SEPARADOR_EMISOR_MENSAJE)[INDICE_MENSAJE].split()
    
    return emisor, mensaje

def mensaje_creacion(mensaje:str) -> bool:
    """
    Dado un mensaje, indica si esta linea de mensaje es de creacion de un grupo de WSP de un dispositivo Apple

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado en dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje.

    POSTCONDICION:
        - Retorna un valor de True si es un mensaje de creacion de grupo
    """
    
    return INDICE_CREACION_GRUPO_1 in mensaje and INDICE_CREACION_GRUPO_2 in mensaje and INDICE_CREACION_GRUPO_3 in mensaje or INDICE_CREACION_GRUPO_4 in mensaje

def mensaje_sticker(mensaje:str) -> bool:
    """
    Dado un mensaje, indica si esta linea de mensaje es de tipo sticker

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado en dispositivo Apple y haber pasado por la funcion de recuperar_emisor_mensaje.

    POSTCONDICION:
        - Retorna un valor de True si es un mensaje es de tipo sticker
    """
    
    return INDICE_MEDIA in mensaje or INDICE_MEDIA_2 in mensaje

def agregar_emisores(emisor:str, lista_palabra:list, mensajes_repetidos:list[list[str|int]]) -> None:
    """
    Dada una lista de palabras a buscar, el emisor del mensaje y una matriz donde se almacenan los mensajes repetidos, la funcion agregara a todos los emisores que aparezcan en el archivo .txt y los vinculara a cada palabra a buscar de la lista, posteriormente lo agregara a la matriz de mensajes repetidos, a cada uno se le adjuntara un valor de 0 en la columna de aparicion. Si dicho emisor ya fue agregado se lo omitira.

    PRECONDICIONES: 
        - El emisor tiene que ser extraido de un chat WSP de un dispositivo Apple y haber pasado por la funcion de recuperar_emisor_mensaje.

    POSTCONDICION:
        - A la matriz mensajes_repetidos se le agregara un emisor si este no fue agregado anteriormente
    """

    for mensajes in mensajes_repetidos:
        
        if emisor in mensajes:
            return
    
    for palabra in lista_palabra:
        mensajes_repetidos.append([emisor,palabra,0])

def contar_aparicion_palabra(palabra_usuario:str, archivo_busqueda:str, archivo_guardado:str) -> None:
    """
    Dada una cadena de palabras separadas por espacios, la direccion de un archivo del tipo .txt donde esta almacenado un chat de wsp codificado desde un disposivo APPLE y por ultimo la direccion de un archivo .csv vacio donde se guardaran los datos recolectados (En caso de no existir el programa creara uno en la direccion indicada). 
    La funcion contara cuantas veces aparecen las palabra de la cadena y lo vincularan a su emisor, para luego escribir esta informacion en el archivo CSV.

    El formato de las columnas de nuestro archivo CSV en el que se guarda la informacion sera el siguiente:
    
    'Contacto','Palabra','Frencuencia'

    Las diferentes variaciones de una palabra contara como una palabra diferente a la hora de ser buscada, es decir, Hola != hola != hOla != hola?

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado de un dispositivo Apple.
        - La cadena de palabras que deseamos buscar debera estar separada unicamente por espacios entre palabra y palabra.

    POSTCONDICION:
        - Un archivo del tipo CSV el cual contendra la cantidad de veces que aparece cada palabra que este en la cadena, vinculada a cada emisor que aparezca en el archivo .txt.
    """
    
    with open(archivo_busqueda,'r',encoding='utf8') as chat, open(archivo_guardado,'w',newline='',encoding='utf-8') as resultados:
        
        mensajes_repetidos = []
        palabra_a_buscar = palabra_usuario.split()
        
        encriptado_wsp = chat.readline()

        resultados_csv = csv.writer(resultados)
        resultados_csv.writerow(CABECERA)
        
        for linea in chat:

            emisor, mensaje = recuperar_emisor_y_mensaje(linea)

            if not mensaje_creacion(mensaje) and not mensaje_sticker(mensaje):

                agregar_emisores(emisor, palabra_a_buscar, mensajes_repetidos)
            
            for palabra in mensaje:

                if palabra in palabra_a_buscar and not mensaje_creacion(mensaje) and not mensaje_sticker(mensaje):

                    for mensaje_repetido in mensajes_repetidos:

                        if palabra in mensaje_repetido and emisor in mensaje_repetido:

                            mensaje_repetido[MENSAJE_REPETIDO_CONTADOR] += 1

        for mensaje_repetido in mensajes_repetidos:
            resultados_csv.writerow(mensaje_repetido)

def agregar_nueva_palabra(usuarios:dict ,emisor:str ,largo_mensaje:int ,palabra_actual:str ,siguiente_palabra:str ,contador_palabra:int) -> None:
    """
    Dado un diccionario, emisor obtenido con la funcion recuperar_emisor_mensaje, el largo del un mensaje usando el mensaje de la funcion recuperar_emisor_mensaje, la palabra actual de nuestro ciclo y la que le sigue, y el contador del largo del mensaje.
    En nuestra funcion usaremos nuestro diccionario en la llave del emisor seguido de la LLAVE_CONTADOR_PALABRA seguido de la llave palabra_actual y la vinculara con siguiente_palabra, si la palabra que le sigue es un fin de linea (Esto lo verificaremos con el contador de palabra y el largo del mensaje), lo vinculara un 'FI' caso contrario vinculara un 'CO'

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado de un dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje para obtener tambien asi su emisor
        - Un diccionario compuesto por 2 llaves, LLAVE_CONTADOR_PALABRA y LLAVE_PALABRA_INICIALES

    POSTCONDICION:
        - Al diccionario brindado se le agregara correctamente a la llave de emisor en la LLAVE_CONTADOR_PALABRA una nueva palabra
    """

    if contador_palabra+2 == largo_mensaje:
        usuarios[emisor][LLAVE_CONTADOR_PALABRA][palabra_actual] = [[siguiente_palabra,1,FIN_DE_ORACION]]
    else:  
        usuarios[emisor][LLAVE_CONTADOR_PALABRA][palabra_actual] = [[siguiente_palabra,1,CONECTOR_DE_ORACION]]

def agregar_aumentar_palabra_inicial(usuarios:dict, emisor:str, palabra_actual:str) -> None:
    """
    Dado un diccionario con las llaves de LLAVE_CONTADOR_PALABRA y LLAVE_PALABRA_INICIALES, emisor obtenido con la funcion recuperar_emisor_mensaje, y la palabra actual.
    Nuestra funcion agrega a nuestro diccionario en la llave de emisor seguido de LLAVE_PALABRA_INCIALES el valor de palabra actual si no a sido agregado previamente, caso contrario le aumenta el valor en 1 al valor de la llave vinculado a palabra_actual.

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado de un dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje para obtener tambien asi su emisor
        - Un diccionario compuesto por 2 llaves, LLAVE_CONTADOR_PALABRA y LLAVE_PALABRA_INICIALES

    POSTCONDICION:
        - Al diccionario brindado se le agregara correctamente a la llave de emisor en la LLAVE_PALABRA_INICIALES una nueva palabra, o se aumentara el valor de apariciones de esta
    """
    
    if palabra_actual in usuarios[emisor][LLAVE_PALABRA_INICIALES]:
        usuarios[emisor][LLAVE_PALABRA_INICIALES][palabra_actual] += 1
    else:
        usuarios[emisor][LLAVE_PALABRA_INICIALES][palabra_actual] = 1

def aumentar_palabra(usuarios:dict ,emisor:str ,largo_mensaje:int ,palabra_actual:str ,siguiente_palabra:str ,contador_palabra:int) -> None:    
    """
    Dado un diccionario, emisor obtenido con la funcion recuperar_emisor_mensaje, el largo del un mensaje usando el mensaje de la funcion recuperar_emisor_mensaje, la palabra actual de nuestro ciclo y la que le sigue, y el contador del largo del mensaje.
    En nuestra funcion usaremos nuestro diccionario en la llave del emisor seguido la LLAVE_CONTADOR_PALABRA y usando la llave 'palabra_actual' conseguiremos una matriz vinculada, en esta verificaremos si se encuntra siguiente_palabra, si esta se encuentra, aumentaremos en 1 su cantidad de apariciones, caso contrario agregaremos siguiente_palabra a la matriz, si la siguiente_palabra es un fin de linea (Esto lo vericaremos con el contador de palabra y el largo del mensaje), lo vinculara a un 'FI' caso contrario vinculara un 'CO'

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp de un dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje para obtener tambien asi su emisor
        - Un diccionario compuesto por 2 llaves, LLAVE_CONTADOR_PALABRA y LLAVE_PALABRA_INICIALES
        - El diccionario debera contar con la como llave a la palabra_actual que se introduzca

    POSTCONDICION:
        - Al diccionario brindado se le aumentara la aparicion de la siguiente palabra si esta se encuentra presente, caso contrario se agregara a dicha palabra a la matriz que le corresponda
    """

    matriz_palabra = usuarios[emisor][LLAVE_CONTADOR_PALABRA].get(palabra_actual)
    se_agrego_palabra = False

    for palabra_matriz in range(len(matriz_palabra)):
        
        if siguiente_palabra in matriz_palabra[palabra_matriz]:
            
            matriz_palabra[palabra_matriz][1] += 1
            se_agrego_palabra = True

    if not se_agrego_palabra:

        if contador_palabra + 2 != largo_mensaje:
            matriz_palabra.append([siguiente_palabra,1,CONECTOR_DE_ORACION])
        
        else:
            matriz_palabra.append([siguiente_palabra,1,FIN_DE_ORACION])

def generador_palabras_personajes(archivo_busqueda:str) -> dict:
    """
    Dada la direccion de un archivo del tipo .txt donde esta almacenado un chat de WSP codificado desde un disposivo APPLE.
    La funcion creara un diccionario que estara compuesto por todos los miembros del chat.
    Este diccionario estara compuesto de la siguientre manera, diccionario principal tendra de llaves los nombres de los participantes del grupo y por valores tendremos 2 diccionarios mas.

    - LLAVE: LLAVE_PALABRAS_INICIALES. El primero tendra de llaves la primera palabra que dijeron en cada mensaje del chat que enviaron, y de valor tendran vinculado la cantidad de veces que aparece como primera palabra.
    - LLAVE: LLAVE_CONTADOR_PALABRA. El segundo tendra de llaves las palabra por las que estuvieron compuestos sus mensajes, y de valor tendran una matriz que contendra las palabra que le siguen, la cantidad de veces que aparecieron despues de nuestra palabra 'llave' y si la palabra que le sigue conecta con otra palabra o es una palabra de fin de oracion.
    
    Glosario:
        Inicio de oracion = IO
        Conector de oracion = CO
        Fin de oracion = FO

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado en un dispositivo Apple.

    POSTCONDICION:
        - Un diccionario con todos los usuarios del chat como llaves, conteniendo 2 diccionarios: 1 - Conteniendo cuantas veces dijeron cada palabra, cual les continuo a estas. 2 - Cuales fueron sus palabra iniciales 
    """

    usuarios = {}

    with open(archivo_busqueda,'r',encoding='utf8') as chat:

        encriptado_wsp = chat.readline()
        
        for linea in chat:

            emisor, mensaje = recuperar_emisor_y_mensaje(linea)
            cantidad_mensajes = range(len(mensaje))
            largo_mensaje = len(mensaje)
            
            if not mensaje_creacion(mensaje) and not mensaje_sticker(mensaje):
                
                if not emisor in usuarios:
                    
                    usuarios[emisor] = {LLAVE_PALABRA_INICIALES:{},LLAVE_CONTADOR_PALABRA:{}}
                    
                for contador_palabra in cantidad_mensajes:
                    
                    if contador_palabra + 1 < len(mensaje):

                        palabra_actual = mensaje[contador_palabra]
                        siguiente_palabra = mensaje[contador_palabra+1]
                        
                        if contador_palabra == INDICE_PALABRA_INICIAL:
                            agregar_aumentar_palabra_inicial(usuarios,emisor,palabra_actual)

                        if palabra_actual in usuarios[emisor][LLAVE_CONTADOR_PALABRA]:
                            aumentar_palabra(usuarios,emisor,largo_mensaje,palabra_actual,siguiente_palabra,contador_palabra)
                        else:
                            agregar_nueva_palabra(usuarios,emisor,largo_mensaje,palabra_actual,siguiente_palabra,contador_palabra)

    return usuarios

def generador_palabra_inicial(diccionario_usuario:dict,usuario:str) -> str:
    """
    Dado un diccionario creado con la fgenerador, y un usuario que este como llave en dicho diccionario, esta funcion genera una palabra inicial al azar apartir del diccionario interno que se consigue usando la llave 'LLAVE_PALABRAS_INICIALES' 

    PRECONDICIONES: 
        - El diccionario tiene que ser generado con la fgenerador
        - El usuario tiene que ser una llave de dicho diccionario

    POSTCONDICION:
        - Devuelve una palabra inicial generada al azar con el diccionario conseguido usando LLAVE_PALABRAS_INICIALES
    """

    palabra_inicial = [[],[]]
    
    if usuario in diccionario_usuario:
    
        for palabra,probabilidad in diccionario_usuario[usuario][LLAVE_PALABRA_INICIALES].items():
    
            palabra_inicial[PALABRA].append(palabra)
            palabra_inicial[PROBABILIDADES].append(probabilidad)
    
    palabra = random.choices(palabra_inicial[0],weights=palabra_inicial[1])[0]
    
    return palabra

def generador_siguiente_palabra(diccionario_usuario,usuario,palabra_anterior):
    """
    Dado un diccionario creado con la fgenerador, un usuario que este como llave en dicho diccionario y palabra_anterior generada anteriormente con la funcion generador_palabra_inicial si es la primera vez que se ejecuta, o caso contrario, palabra_anterior generada por esta funcion. Esta funcion genera una palabra al azar apartir del diccionario interno que se consigue usando la llave 'LLAVE_CONTADOR_PALABRA' seguido de usar de llave palabra_anterior.

    PRECONDICIONES: 
        - El diccionario tiene que ser generado con la fgenerador
        - El usuario tiene que ser una llave de dicho diccionario
        - palabra_anterior tiene que haber sido generada con generador_palabra_inicial o con generador_siguiente_palabra (apartir de ya haber inicializado 1 vez la funcion)

    POSTCONDICION:
        - Una palabra generada al azar apartir de las posibles palabras que se pueden generar despues de la palabra anterior a esta
    """
    siguiente_palabra = [[],[],[]]
    
    for palabra in diccionario_usuario[usuario][LLAVE_CONTADOR_PALABRA][palabra_anterior]:
    
        siguiente_palabra[PALABRA].append(palabra[PALABRA])
        siguiente_palabra[PROBABILIDADES].append(palabra[PROBABILIDADES])
        siguiente_palabra[CONTINUIDAD].append(palabra[CONTINUIDAD])
    
    palabra_generada = random.choices(siguiente_palabra[PALABRA],weights=siguiente_palabra[PROBABILIDADES])
    palabra_generada.append(siguiente_palabra[CONTINUIDAD][siguiente_palabra[PALABRA].index(palabra_generada[0])])

    return palabra_generada

def generador_mensajes(diccionario_usuario,usuario):
    """
    Dado un diccionario creado con la funcion generador, un usuario que este como llave en dicho diccionario. Devuelve una frase al azar creada apartir de las palabras dichas por este usuario y que estan almacenadas en su diccionario vinculado.

    PRECONDICIONES: 
        - El diccionario tiene que ser generado con la fgenerador
        - El usuario tiene que ser una llave de dicho diccionario

    POSTCONDICION:
        - Devuelve una frase al azar generada a partir de las palabras dichas por el usuario elegido 
    """

    frase_completa = ''
    palabra_inicial = generador_palabra_inicial(diccionario_usuario,usuario)
    frase_completa += palabra_inicial
    
    palabra_generada = generador_siguiente_palabra(diccionario_usuario,usuario,palabra_inicial)
    frase_completa += ' ' + palabra_generada[PALABRA]

    while True:
        
        palabra_anterior = palabra_generada[PALABRA] 
        palabra_generada = generador_siguiente_palabra(diccionario_usuario,usuario,palabra_anterior)
        frase_completa += ' ' + palabra_generada[PALABRA]

        if palabra_generada[1] == FIN_DE_ORACION:
            return frase_completa
