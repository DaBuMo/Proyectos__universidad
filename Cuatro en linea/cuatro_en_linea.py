from typing import List

CELDAS = " "
INICIO_FILAS_Y_COLUMNAS = 0
POSICION_COLUMNAS = 0
FICHA_JUGADOR_1 = 'X'
POSICION_JUGADOR_1 = 0
FICHA_JUGADOR_2 = 'O'
POSICION_JUGADOR_2 = 1
FICHAS_PARA_GANAR = 4
CARACTER_SALIDA = 's'

def crear_tablero(n_filas: int, n_columnas: int) -> List[List[str]]:
    """Crea un nuevo tablero de cuatro en línea, con dimensiones
    n_filas por n_columnas.
    Para todo el módulo `cuatro_en_linea`, las cadenas reconocidas para los
    valores de la lista de listas son las siguientes:
        - Celda vacía: ' '
        - Celda con símbolo X: 'X'
        - Celda con símbolo O: 'O'

    PRECONDICIONES:
        - n_filas y n_columnas son enteros positivos mayores a tres.

    POSTCONDICIONES:
        - la función devuelve un nuevo tablero lleno de casilleros vacíos
          que se puede utilizar para llamar al resto de las funciones del
          módulo.

    EJEMPLO:
        >>> crear_tablero(4, 5)
        [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']
        ]
    """

    tablero = []

    for fila in range(n_filas):
        lista_aux = []
        for columna in range(n_columnas):
            lista_aux.append(CELDAS)
        tablero.append(lista_aux)
    return tablero

def contador_filas_y_columnas(tablero:List[list[str]]) -> tuple:
    """
    Recibe un tablero y devuelve una tupla con la cantidad de filas y columnas que tiene

     PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    POSTCONDICIONES:
        - la funcion devolvera 1 tupla con 2 valores enteros, primero la cantidad de filas del tablero y despues la cantidad de columnas en el tablero.
    """

    cantidad_filas = len(tablero)
    cantidad_columnas = len(tablero[POSICION_COLUMNAS])

    return cantidad_filas,cantidad_columnas

def contador_fichas(tablero:List[list[str]]) -> tuple:
    """
    Dado un tablero cuenta cuantas celdas son vacias y cuantas estan con el simbolo del jugador 1 o el simbolo jugador 2.
    
    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    POSTCONDICIONES:
        - la funcion devolvera 3 valores, primero la cantidad fichas del jugador 1 en el tablero, despues la cantidad de fichas del jugador 2 en el tablero y por ultimo la cantidad de celdas vacias en el tablero.
    """
    
    contador_jugador_1 = 0
    contador_jugador_2 = 0

    for fila in tablero:
        for celda in fila:
            if celda == FICHA_JUGADOR_1:
                contador_jugador_1 += 1
            elif celda == FICHA_JUGADOR_2:
                contador_jugador_2 += 1

    return contador_jugador_1,contador_jugador_2
def tablero_completo(tablero: List[List[str]]) -> bool:
    """Dado un tablero, indica si se encuentra completo. Un tablero se considera
    completo cuando no hay más espacio para insertar un nuevo símbolo, en tal
    caso la función devuelve `True`.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    POSTCONDICIONES:
        - la funcion devolvera el valor de true si es que el 'tablero' se encuentra sin ninguna casilla vacia
    """

    for fila in tablero:
        for celda in fila:
            if celda == CELDAS:
                return False

    return True

def insertar_simbolo(tablero: List[List[str]], columna: int) -> bool:
    """Dado un tablero y un índice de columna, se intenta colocar el símbolo del
    turno actual en dicha columna.
    Un símbolo solo se puede colocar si el número de columna indicada por
    parámetro es válido, y si queda espacio en dicha columna.
    El número de la columna se encuentra indexado en 0, entonces `0` corresponde
    a la primer columna.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    POSTCONDICIONES:
        - si la función devolvió `True`, se modificó el contenido del parámetro
          `tablero`. Caso contrario, el parámetro `tablero` no se vio modificado
    """

    cantidad_columnas = len(tablero[0])
    
    if columna >= cantidad_columnas or columna < INICIO_FILAS_Y_COLUMNAS:
        return False

    for fila in reversed(tablero):
        if fila[columna] == CELDAS:
            if es_turno_de_x(tablero):
                fila[columna] = FICHA_JUGADOR_1
            else:
                fila[columna] = FICHA_JUGADOR_2
            return True
        
    return False

def es_turno_de_x(tablero: List[List[str]]) -> bool:
    """Dado un tablero, devuelve True si el próximo turno es de X. Si, en caso
    contrario, es el turno de O, devuelve False.
    - Dado un tablero vacío, dicha función debería devolver `True`, pues el
      primer símbolo a insertar es X.
    - Luego de insertar el primer símbolo, esta función debería devolver `False`
      pues el próximo símbolo a insertar es O.
    - Luego de insertar el segundo símbolo, esta función debería devolver `True`
      pues el próximo símbolo a insertar es X.
    - ¿Qué debería devolver si hay tres símbolos en el tablero? ¿Y con cuatro
      símbolos?

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
        - los símbolos del tablero fueron insertados previamente insertados con
          la función `insertar_simbolo`"""
    
    fichas_jugador_1 = contador_fichas(tablero)[POSICION_JUGADOR_1]
    fichas_jugador_2 = contador_fichas(tablero)[POSICION_JUGADOR_2]

    return fichas_jugador_1 == fichas_jugador_2

def calcular_traza(tablero,fila,columna,ficha_jugador) -> bool:
    """Dado un tablero y una ficha valida junto a su fila y columna, devuelve si la traza de esta ficha es igual a 4 en forma de booleano

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
        - los símbolos del tablero fueron insertados previamente insertados con
          la función `insertar_simbolo`
        - la ficha_jugador tiene que ser una de las definidas en las constantes
        - la fila y columna tienen que estar asociadas a la ficha_jugador dada
        
    POSTCONDICIONES:
        - si la funcion devolvio 'True' es porque alguna de las trazas de rango 4 de esa ficha es verdadera, caso contrario, la traza de esa ficha no es igual a 4    
    """
    
    cantidad_filas, cantidad_columnas = contador_filas_y_columnas(tablero)
    contador_traza_positiva = 0
    contador_traza_inversa = 0
    
    for i in range(FICHAS_PARA_GANAR):
        
        if (fila + i < cantidad_filas and columna + i <cantidad_columnas) and tablero[fila + i ][columna + i] == ficha_jugador:
            contador_traza_positiva += 1

        if(fila + i < cantidad_filas and columna - i >= INICIO_FILAS_Y_COLUMNAS) and tablero[fila + i][columna - i] == ficha_jugador:
            contador_traza_inversa += 1

    return contador_traza_positiva == FICHAS_PARA_GANAR or contador_traza_inversa == FICHAS_PARA_GANAR 

  
def calcular_vertical_horizontal(tablero,fila,columna,ficha_jugador) -> bool:
    """Dado un tablero y una ficha valida junto a su fila y columna, devuelve si la horizontal o vertical de dicha ficha es igual a 4 en forma de booleano

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
        - los símbolos del tablero fueron insertados previamente insertados con
          la función `insertar_simbolo`
        - la ficha_jugador tiene que ser una de las definidas en las constantes
        - la fila y columna tienen que estar asociadas a la ficha_jugador dada
        
    POSTCONDICIONES:
        - si la funcion devolvio 'True' es porque alguna de las trazas de rango 4 de esa ficha es verdadera, caso contrario, la traza de esa ficha no es igual a 4    
    """

    contador_horizontal = 0
    contador_vertical = 0
    cantidad_filas, cantidad_columnas = contador_filas_y_columnas(tablero)

    for i in range(FICHAS_PARA_GANAR):
        
        if (columna + i < cantidad_columnas) and tablero[fila][columna + i] == ficha_jugador:
            contador_horizontal += 1

        if (fila + i < cantidad_filas) and tablero[fila + i ][columna] == ficha_jugador:
            contador_vertical += 1
    
    return contador_horizontal == FICHAS_PARA_GANAR or contador_vertical == FICHAS_PARA_GANAR

def obtener_ganador(tablero: List[List[str]]) -> str:
    """Dado un tablero, devuelve el símbolo que ganó el juego.
    El símbolo ganador estará dado por aquel que tenga un cuatro en línea. Es
    decir, por aquel símbolo que cuente con cuatro casilleros consecutivos
    alineados de forma horizontal, vertical, o diagonal.
    En el caso que el juego no tenga ganador, devuelve el símbolo vacío.
    En el caso que ambos símbolos cumplan con la condición de cuatro en línea,
    la función devuelve cualquiera de los dos.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`

    EJEMPLO: para el siguiente tablero, el ganador es 'X' por tener un cuatro en
    línea en diagonal
        [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'X', 'O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'X', ' ', ' ', ' '],
            [' ', ' ', 'X', 'O', 'X', ' ', ' '],
            [' ', 'O', 'O', 'X', 'X', 'X', 'O'],
        ]
    """

    cantidad_filas, cantidad_columnas = contador_filas_y_columnas(tablero)

    for fila in range(cantidad_filas):

        for columna in range(cantidad_columnas):

            if tablero[fila][columna] == FICHA_JUGADOR_1:
                
                if calcular_traza(tablero,fila,columna,FICHA_JUGADOR_1) or calcular_vertical_horizontal(tablero,fila,columna,FICHA_JUGADOR_1):
                    return FICHA_JUGADOR_1
                
            elif tablero[fila][columna] == FICHA_JUGADOR_2:
                
                if calcular_traza(tablero,fila,columna,FICHA_JUGADOR_2) or calcular_vertical_horizontal(tablero,fila,columna,FICHA_JUGADOR_2):
                    return FICHA_JUGADOR_2
                
    return CELDAS

def imprimir_tablero(tablero: List[List[str]]):
    """
    Dado un tablero, imprime el tablero de una manera en la cual indica cual es cada una de sus columnas y lo hace mas visible y entendible para el usuario.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    """

    cantidad_columnas = len(tablero[0])
    
    print("|",end="")
    for e in range(cantidad_columnas):
        valor_columna = str(e).ljust(2,"|")
        if e+1 == cantidad_columnas:
            print(valor_columna)
        else:
            print(valor_columna,end ="")
            
    print("-".ljust(cantidad_columnas*2+1,"-"))
    for i in range(len(tablero)):
        
        print("|",end="")
        
        for j in range(len(tablero[INICIO_FILAS_Y_COLUMNAS])):
            valor = tablero[i][j].ljust(2,"|")
            print(valor,end = "")
        print("")
    print("")
