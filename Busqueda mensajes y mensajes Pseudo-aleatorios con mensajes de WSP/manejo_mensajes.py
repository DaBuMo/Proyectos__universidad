import csv
import random

SEPARADOR_TIEMPO_MENSAJE = ']'
SEPARADOR_EMISOR_MENSAJE = ':'

INDICE_CREACION_GRUPO_1 = 'creó'
INDICE_CREACION_GRUPO_2 = 'el'
INDICE_CREACION_GRUPO_3 = 'grupo'
INDICE_CREACION_GRUPO_4 = 'añadió'

INDICE_MEDIA = '[\u200esticker]'
INDICE_MEDIA_2 = 'omitido'

FIN_DE_LINEA = '\n'

INDICE_PALABRA_INICIAL = 0
INDICE_EMISOR_Y_MENSAJE = 1

INDICE_EMISOR = 0
INDICE_MENSAJE = 1

CANTIDAD_APARICIONES = 'APA' 
TIPO_CONEXION = 'TC'
SIGUIENTES_PALABRAS = 'SP'

INICIO_DE_ORACION = 'IO'
CONECTOR_DE_ORACION = 'CO'
FIN_DE_ORACION = 'FO'

PALABRA = 0
PROBABILIDADES = 1
CONTINUIDAD = 2


CABECERA = ('Contacto','Palabra','Frencuencia')

def recuperar_emisor_y_mensaje(mensaje:str) -> str|list[str]:
    """
    Dado un mensaje WSP codificado en un dispositivo de Apple, devuelve el nombre del emisor del mensaje y el mensaje separado en una lista palabra por palabra.

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado en dispositivo Apple.

    POSTCONDICION:
        - Retorna dos valores, primero el nombre del emisor del mensaje y despues una lista con cada palabra que tenia el mensaje que estaba separada por un espacio
    """
    
    cadena = mensaje.rstrip(FIN_DE_LINEA).split(SEPARADOR_TIEMPO_MENSAJE)[INDICE_EMISOR_Y_MENSAJE:]

    if len(cadena) > 1:

        mensaje_emisor = cadena[INDICE_EMISOR]

        for i in range(INDICE_EMISOR_Y_MENSAJE, len(cadena)):
            mensaje_emisor = mensaje_emisor + ']' + str(cadena[i])
        
        mensaje_emisor = mensaje_emisor.strip().split(SEPARADOR_EMISOR_MENSAJE)

        if len(mensaje_emisor) > 2:

            emisor = mensaje_emisor[INDICE_EMISOR]
            mensaje = mensaje_emisor[INDICE_MENSAJE].strip()

            for i in range(INDICE_MENSAJE + 1,len(mensaje_emisor)):
                mensaje = mensaje + ':' + mensaje_emisor[i]      

            mensaje = mensaje.split()
    else:
        emisor = mensaje.rstrip(FIN_DE_LINEA).split(SEPARADOR_TIEMPO_MENSAJE)[INDICE_EMISOR_Y_MENSAJE].split(SEPARADOR_EMISOR_MENSAJE)[INDICE_EMISOR].strip()
        mensaje = mensaje.rstrip(FIN_DE_LINEA).split(SEPARADOR_TIEMPO_MENSAJE)[INDICE_EMISOR_Y_MENSAJE].split(SEPARADOR_EMISOR_MENSAJE)[INDICE_MENSAJE].split()    
    
    return emisor, mensaje

def mensaje_creacion(mensaje:str) -> bool:
    """
    Dado un mensaje, indica si esta linea de mensaje es de creacion de un grupo o si es un mensaje que añade miembros a dicho grupo de WSP de un dispositivo Apple

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

def agregar_emisor(emisor:str, lista_palabra:list, mensajes_repetidos:dict) -> None:
    """
    Dada una lista de palabras a buscar, el emisor del mensaje y diccionario donde se almacenan los mensajes repetidos, la funcion agregara a todos los emisores que aparezcan en el archivo .txt y los vinculara a cada palabra a buscar de la lista, posteriormente lo agregara a la matriz de mensajes repetidos, a cada uno se le adjuntara un valor de 0 en la columna de aparicion. Si dicho emisor ya fue agregado se lo omitira.

    PRECONDICIONES: 
        - El emisor tiene que ser extraido de un chat WSP de un dispositivo Apple y haber pasado por la funcion de recuperar_emisor_mensaje.

    POSTCONDICION:
        - Al diccionario mensajes_repetidos se le agregara un emisor si este no fue agregado anteriormente
    """

    if emisor in mensajes_repetidos:
        return
    
    mensajes_repetidos[emisor] = {}
    for palabra in lista_palabra:
        mensajes_repetidos[emisor][palabra] = 0

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
        
        mensajes_repetidos = {}
        palabras_a_buscar = palabra_usuario.split()
        
        encriptado_wsp = chat.readline()

        resultados_csv = csv.writer(resultados)
        resultados_csv.writerow(CABECERA)
        
        for linea in chat:
            
            emisor, mensaje = recuperar_emisor_y_mensaje(linea)

            if not mensaje_creacion(mensaje) and not mensaje_sticker(mensaje):

                agregar_emisor(emisor, palabras_a_buscar, mensajes_repetidos)
            
            for palabra in mensaje:

                if palabra in palabras_a_buscar and not mensaje_creacion(mensaje) and not mensaje_sticker(mensaje):
                    
                    mensajes_repetidos[emisor][palabra] += 1
        
        for emisor in mensajes_repetidos:
            for palabra in palabras_a_buscar:
                resultados_csv.writerow([emisor,palabra,mensajes_repetidos[emisor][palabra]])

def agregar_aumentar_palabra(usuarios:dict, emisor:str, palabra_actual:str, tipo_palabra:str) -> None:
    """
    Dado un diccionario con la emisor, emisor obtenido con la funcion recuperar_emisor_mensaje, la palabra actual y el TIPO_CONEXION de esta palabra en el texto.
    Nuestra funcion agrega a nuestro diccionario en la llave de emisor seguido de palabra_actual con los valores de CANTIDAD_APARICIONES,TIPO_DE_CONEXION asociado a tipo_palabra y SIGUIENTES_PALABRAS asociado a un diccionario vacio si palabra_actual no se encuentra, caso contrario le aumenta el valor en 1 al valor de CANTIDAD_APARICIONES a palabra_actual.

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp codificado de un dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje para obtener tambien asi su emisor
        - Un diccionario compuesto por los emisores del chat.

    POSTCONDICION:
        - Al diccionario brindado se le agregara correctamente a la llave de emisor en la llave palabra_actual una nueva palabra, o se aumentara el valor de apariciones de esta.
    """
    
    if palabra_actual in usuarios[emisor]:
        usuarios[emisor][palabra_actual][CANTIDAD_APARICIONES] += 1
    else:
        usuarios[emisor][palabra_actual] = {CANTIDAD_APARICIONES:1,TIPO_CONEXION:tipo_palabra,SIGUIENTES_PALABRAS: {}}

def agregar_conectores_palabra(usuarios:dict ,emisor:str ,largo_mensaje:int ,palabra_actual:str ,siguiente_palabra:str ,contador_palabra:int) -> None: 
    """
    Dado un diccionario, emisor obtenido con la funcion recuperar_emisor_mensaje, el largo del un mensaje recuperado con la funcion recuperar_emisor_mensaje, la palabra actual de nuestro ciclo y la que le sigue, y el contador del largo del mensaje.
    En nuestra funcion usaremos nuestro diccionario en la llave del emisor seguido llave 'palabra_actual' y despues la llave SIGUIENTES_PALABRAS agregaremos siguiente_palabra como la palabra que le sigue a nuestra palabra actual. Si siguiente_palabra es un fin de linea (Esto lo vericaremos con el contador de palabra y el largo del mensaje), lo vinculara a un 'FI' caso contrario vinculara un 'CO'

    PRECONDICIONES: 
        - El mensaje tiene que ser extraido de un chat de wsp de un dispositivo Apple y haber pasado por la funcion recuperar_emisor_mensaje para obtener tambien asi su emisor
        - Un diccionario emisores del chat
        - El diccionario debera contar con la llave palabra_actual que se introduzca

    POSTCONDICION:
        - Al diccionario brindado se agregara el diccionario de siguiente_palabra en el diccionario de SIGUIENTE_PALABRA con el conector que le corresponda
    """

    if contador_palabra + 2 != largo_mensaje:
        usuarios[emisor][palabra_actual][SIGUIENTES_PALABRAS][siguiente_palabra] = {CANTIDAD_APARICIONES:1,TIPO_CONEXION:CONECTOR_DE_ORACION}
    else:  
        usuarios[emisor][palabra_actual][SIGUIENTES_PALABRAS][siguiente_palabra] = {CANTIDAD_APARICIONES:1,TIPO_CONEXION:FIN_DE_ORACION}

def generador_palabras_personajes(archivo_busqueda:str) -> dict:
    """
    Dada la direccion de un archivo del tipo .txt donde esta almacenado un chat de WSP codificado desde un disposivo APPLE.
    La funcion creara un diccionario que estara compuesto por todos los miembros del chat.
    Este diccionario estara compuesto de la siguientre manera, diccionario principal tendra de llaves los nombres de los participantes del grupo.

    - LLAVE: emisor/res. Cada emisor que aparecio en el chat tendra una llave relacionada a su nombre. Cada emisor estara asociado a cada palabra que dijo como una llave (Exceptuando los FO). 
    Cada palabra estara asociada a 3 llaves:
        - CANTIDAD_APARICIONES = Cantidad de veces que aparecio esta palabra
        - TIPO_CONEXION = Indicara si es un IO o un CO
        - SIGUIENTES_PALABRAS = Un diccionario que tendra como llaves diccionarios de las palabras que le siguen a nuestra palabra llave, estos diccionarios tendran 2 llaves:
            * CANTIDAD_APARICIONES = Cantidad de veces que aparecio esta palabra despues de nuestra palabra llave
            * TIPO_DE_CONEXION = Si es un CO o FO
    
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
                    
                    usuarios[emisor] = {}
                    
                for contador_palabra in cantidad_mensajes:
                    
                    if contador_palabra + 1 < largo_mensaje:

                        palabra_actual = mensaje[contador_palabra]
                        siguiente_palabra = mensaje[contador_palabra+1]
                        
                        if contador_palabra == INDICE_PALABRA_INICIAL:
                            agregar_aumentar_palabra(usuarios,emisor,palabra_actual,INICIO_DE_ORACION)
                        else:
                            agregar_aumentar_palabra(usuarios,emisor,palabra_actual,CONECTOR_DE_ORACION)
                        
                        if siguiente_palabra not in usuarios[emisor][palabra_actual][SIGUIENTES_PALABRAS]:
                            agregar_conectores_palabra(usuarios,emisor,largo_mensaje,palabra_actual,siguiente_palabra,contador_palabra)
                        else:
                            usuarios[emisor][palabra_actual][SIGUIENTES_PALABRAS][siguiente_palabra][CANTIDAD_APARICIONES] += 1

    return usuarios

def generador_palabra_inicial(diccionario_usuario:dict,usuario:str) -> str:
    """
    Dado un diccionario creado con la fgenerador, y un usuario que este como llave en dicho diccionario. Esta funcion genera una palabra al azar apartir del diccionario interno que se consigue usando la llave del usuario, y revisando cuales palabras usando la llave TIPO_CONEXION son del tipo IO

    PRECONDICIONES: 
        - El diccionario tiene que ser generado con la fgenerador
        - El usuario tiene que ser una llave de dicho diccionario

    POSTCONDICION:
        - Devuelve una palabra inicial generada al azar con el diccionario conseguido usando LLAVE_PALABRAS_INICIALES
    """

    palabra_inicial = [[],[]]
    
    if usuario in diccionario_usuario:
    
        for palabra in diccionario_usuario[usuario]:
            
            if diccionario_usuario[usuario][palabra][TIPO_CONEXION] == INICIO_DE_ORACION:
                palabra_inicial[PALABRA].append(palabra)
                palabra_inicial[PROBABILIDADES].append(diccionario_usuario[usuario][palabra][CANTIDAD_APARICIONES])

    palabra = random.choices(palabra_inicial[PALABRA],weights=palabra_inicial[PROBABILIDADES])[0]
    return palabra


def generador_siguiente_palabra(diccionario_usuario,usuario,palabra_anterior):
    """
    Dado un diccionario creado con la fgenerador, un usuario que este como llave en dicho diccionario y palabra_anterior generada anteriormente con la funcion generador_palabra_inicial si es la primera vez que se ejecuta, o caso contrario, palabra_anterior generada por esta funcion. Esta funcion genera una palabra al azar apartir del diccionario interno que se consigue usando la llave del usuario, seguido de 'palabra_anterior' seguido de usar de llave SIGUIENTES_PALABRAS.

    PRECONDICIONES: 
        - El diccionario tiene que ser generado con la fgenerador
        - El usuario tiene que ser una llave de dicho diccionario
        - palabra_anterior tiene que haber sido generada con generador_palabra_inicial o con generador_siguiente_palabra (apartir de ya haber inicializado 1 vez la funcion)

    POSTCONDICION:
        - Una palabra generada al azar apartir de las posibles palabras que se pueden generar despues de la palabra anterior a esta
    """
    siguiente_palabra = [[],[],[]]

    for palabra in diccionario_usuario[usuario][palabra_anterior][SIGUIENTES_PALABRAS]:
                
            siguiente_palabra[PALABRA].append(palabra)
            siguiente_palabra[PROBABILIDADES].append(diccionario_usuario[usuario][palabra_anterior][SIGUIENTES_PALABRAS][palabra][CANTIDAD_APARICIONES])
            siguiente_palabra[CONTINUIDAD].append(diccionario_usuario[usuario][palabra_anterior][SIGUIENTES_PALABRAS][palabra][TIPO_CONEXION])
    
    palabra_generada = random.choices(siguiente_palabra[PALABRA],weights=siguiente_palabra[PROBABILIDADES])
    palabra_generada.append(siguiente_palabra[CONTINUIDAD][siguiente_palabra[PALABRA].index(palabra_generada[PALABRA])])

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

    while palabra_generada[1] != FIN_DE_ORACION:
        
        palabra_anterior = palabra_generada[PALABRA] 
        palabra_generada = generador_siguiente_palabra(diccionario_usuario,usuario,palabra_anterior)
        frase_completa += ' ' + palabra_generada[PALABRA]

    return frase_completa