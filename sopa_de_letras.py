"""
The MIT License (MIT)

Copyright (c) 2015 Paul Olivera

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Sopa de letras.
    - Idea del programa:
        El procesamiento de las palabras y el tablero esta pensado como vectores dentro de una matriz.
        Las palabras como vectores tienen un sentido y direccion. Los cuales se posicionan en una matriz de NxN.
        Sentido, direccion y ubicacion de las palabras es semi-aleatorio (Mas detalles en la funcion "procesar_palabras")

    - Funcionamiento del programa:
        Al principio de la ejecucion se muestra un "Splash Screen" (Apendice -1-)

        Al iniciar el usuario ("Jugador" de ahora en delante) tiene un menu ("Menu Inicial" de ahora en delante)con 3 opciones.

        1) Iniciar juego nuevo:
            a) Se le pide al jugador indicar que cantidad de filas/columnas ("N" de ahora en mas) desea que tenga el tablero (Apendice -2-)
            b) Se le pide al jugador indicar que cantidad de palabras ("P" de ahora en mas) desea incluir en el tablero (Apendice -3-)
            c) Se le pide al jugador introducir las P palabras (Apendice -4-)
            d) Se muestra el tablero con las opciones anteriormente ingresadas
            e) Se le pide al jugar ingresar las coordenadas de Inicio y Final de la palabra que encontro (Apendice -5-)
            f) Terminado el juego se muestra un mensaje acorde y se muestra de nuevo el Menu Inicial.

        2) Acerca de: Se muestra un mensaje acerca del juego y del desarrollador

        3) Salir: Termina el programa

    APENDICE
        1) http://en.wikipedia.org/wiki/Splash_screen
        2) N debe estar entre 10 y 20
        3) P debe ser menor o igual a N/2 y estar compuesta unicamente de letras
        4) Las palabras ingresadas deben tener una longitud minima de 3 caracteres, y una longitud maxima de N/2 caracteres
        5) Las coordenadas tienen el formato de "AN,AN" donde A es una letra y N un entero
"""

# CODE START
import time
import random
import platform
import os
import string


#============== CLASS VARIABLES
# Splash 10x10
splash =[
     [ "","","","","","","","","","" ],
     [ "","","","","","","","","","" ],
     [ "","S","U","P","E","R","","","","" ],
     [ "","","","","","","","","","" ],
     [ "","","","S","O","P","A","","","" ],
     [ "","","","","","","","","","" ],
     [ "","","","","D","E","","","","" ],
     [ "","","","","","","","","","" ],
     [ "","","L","E","T","R","A","S","","" ],
     [ "","","","","","","","","","" ]
     ]

# Almacena cadenas, cada una compuesta por numeros que representan la ubicacion de las palabras en la matriz
# una vez formada la cadena, sirve para comparar si existe una palabra en tal posicion.
posiciones = []

# A.K.A Tablero
matrix = []

# Comando de sistema para "limpiar" la consola. Varia dependiendo el sistema
clear_command = ""

# Cantidad de palabras en el tablero
n_palabras = 0

# Cantidad de filas/columnas del tablero
nxn = 0

# ...
palabra_min_caracteres = 3
palabras_restantes = 0
palabras = []

# True para mostrar las palabras en MAYUSCULAS en el tablero y completar con asteriscos
debug_palabras = False

#============== Utilidad

def show_msg(msg) :
    """
    Para darle un formato particular a todos los mensajes
    """
    print "#" * 5, msg


def show_title(msg):
    """
    Para darle un formato particular a todos los titulos
    """
    # Valor 70 elegido completamente a gusto
    # (70/2)-1 = 34
    print "="*70
    print "=" * ( 34 - (len(msg)/2) ), msg, "=" * ( 34 - (len(msg)/2) )
    print "="*70

def show_menu(items):
    """
    Muestra los items que le son pasados y devuelve un entero en representacion de la opcion seleccionada

    Params:
        - items: lista de cadenas para mostrar como items
    Return: Entero
    """
    for i in range(len(items)):
        print "[" + str(i+1) +"]", items[i]
            
    while True:
        item = str(raw_input("<<< "))

        if not item.isdigit() :
            show_msg("Opcion Incorrecta")
            continue
        
        item = int(item)-1
        if item > -1 and item < len(items) :
            return item
        else:
            show_msg("Opcion Incorrecta")

def clear_window():
    """
    "Limpia" la ventana de comando
    """
    if clear_command != "" :
        os.system(clear_command)

def letra_aleatoria():
    """
    Devuelve una letra minuscula al azar
    """
    return random.choice(string.ascii_lowercase)

def obtener_mensaje(identificador):
    if identificador == "rawinput_coordenadas" : return "Ingrese Celdas de Inicio y Final de la palabra (EJ: A3,C4): "
    if identificador == "entrada_incorrecta" : return "Entrada incorrecta. (EJ: A3,C4)"
    if identificador == "rango_fila" : return "Fila fuera de rango"
    if identificador == "rango_columna" : return "Columna fuera de rango"
    if identificador == "fila_o_columa_igual" : return "Al menos fila o columna, inicial y final deben coincidir."
    if identificador == "error_coordenadas" : return "Mmm.. No se encontro ninguna palabra nueva en ese par de coordenadas"
    
#============== Matriz

def crear_matrix():
    """
    Crea la matriz de N filas/columnas
    """
    global matrix
    matrix =[]
    for i in range(nxn):
        matrix.append([])
        for e in range(nxn):
            matrix[i].append("")
    return True

def completar_matrix(mtx, n, randomChar=True):
    """
    Completa la matriz con letras aleatorias o con asteriscos

    Params:
        - mtx: matriz a completar
        - n: entero de filas/columnas a completar
        - randomChar: define si son letras aleatorias o asteriscos
    """
    for i in range(n):
        for e in range(n):
            if randomChar :
                if mtx[i][e] == "" : mtx[i][e] = letra_aleatoria()
            else:
                if mtx[i][e] == "" : mtx[i][e] = "*"

def valores_posicion(isrow, pos):
    """
    Devuelve una lista con informacion acerca de una fila/columna de la matriz tablero

    Params:
    - isrow: Bool -> True para Fila | False para Columna
    - pos: Int indicando fila/columna

    Return:
    - valores: Lista formada de a pares. Primer valor -> Int de la cantidad de espacios en blanco en la fila/columna hasta la primer letra encontrada.
                                         Segundo valor -> Letra encontrada
    """
    
    valores = []
    espacios = 0

    for i in range(nxn):

        if isrow:
            if matrix[pos][i] != "":
                valores.append(espacios)
                valores.append(matrix[pos][i])
            else:
                espacios+=1
        else:
            if matrix[i][pos] != "":
                valores.append(espacios)
                valores.append(matrix[i][pos])
                espacios = 0
            else:
                espacios+=1

    # Si la fila/columna esta vacia, indicar que existen nxn espacios vacios
    if espacios == nxn :
        valores.append(espacios)
        valores.append("0")

    return valores

def procesar_palabras():
    """
    Acomoda las palabras en la matriz tablero de manera semi-aleatoria: 

        Para acomodar las palabras se les asigna un sentido, una direccion y una posicion aleatoria dentro de la matriz.
        Se pide informacion de tal fila/columna a la funcion "valores_posicion" hasta que la palabra en cuestion pueda ser correctamente acomodada dentro de la matriz.
        Si la palabra no puede ser acomodada en la fila/columna random, con la direccion random, se prueba en la siguiente fila/columna con la misma direccion; una vez
        recorridas todas las filas/columnas, cambia la direccion y prueba nuevamente una por una. Si tampoco sirve, se saltea la palabra

    Las primeras dos palabras cumplen con ciertas condiciones:
        1) La primer palabra debe tener direccion vertical y estar posicionada de arriba hacia abajo
        2) La segunda palabra debe tener direccion horizontal y estar posicionada de derecha a izquierda

    Vars:
        - direccion: False para horizontal | True para vertical
        - posicion: fila o columna en la que colocar la palabra
        - sentido_inverso: False para normal | True para invertir la palabra

    Return:
        - None: Si se ubicaron todas las palabras
        - Int: Si hubieron palabras que no fueron ubicadas
    """

    salteadas = 0
    for i in range(len(palabras)):

        posicion_inicial = random.randint(0,nxn-1)
        sentido_inverso = bool(random.randint(0,1))

        if i == 0:
            direccion_inicial = False # Primer palabra siempre Vertical
        elif i == 1:
            direccion_inicial = True  # Segunda palabra siempre Horizontal
            sentido_inverso = True    # Segunda palabra siempre Invertida
        else:
            direccion_inicial = bool(random.randint(0,1))

        posicion = posicion_inicial
        direccion = direccion_inicial

        if sentido_inverso:
            palabras[i] = palabras[i][::-1]

        while(True):

            # Siempre Par
            valores_en_posicion = valores_posicion(direccion, posicion)
            colocada = False
            for e in range(len(valores_en_posicion)/2):
                # Si el espacio para acomodar la palabra es mayor en longitud, se le agrega un margen random a la palabra
                if int(valores_en_posicion[e*2]) >= len(palabras[i]) :
                    margen = int(valores_en_posicion[e*2]) - len(palabras[i])
                    if margen > 0:
                        inicio = random.randint(0,margen)

                    if colocar_palabra(palabras[i], direccion, posicion, margen) :

                        if direccion :
                            fila_inicio = posicion
                            columna_inicio = margen

                            fila_final = posicion
                            columna_final = margen + len(palabras[i])-1
                        else:
                            columna_inicio = posicion
                            fila_inicio = margen

                            columna_final = posicion
                            fila_final = margen + len(palabras[i])-1

                        if sentido_inverso :
                            aux = fila_final
                            fila_final = fila_inicio
                            fila_inicio = aux

                            aux = columna_final
                            columna_final = columna_inicio
                            columna_inicio = aux
                            
                        # Alternativa para hacer "legible" las posiciones
                        # posiciones.append(str(columna_inicio)+","+str(fila_inicio)+":"+str(columna_final)+","+str(fila_final))
                        posiciones.append(str(columna_inicio)+str(fila_inicio)+str(columna_final)+str(fila_final))
                        colocada = True
                        break

            if not colocada:
                # Si en esa posicion no entra, probar en la siguiente
                if posicion < nxn-1: posicion += 1
                else: posicion = 0

                # Cuando prueba todas las posiciones, cambiar direccion y probar de nuevo
                if posicion == posicion_inicial :
                    direccion = not direccion

                    # Si cambiar la direccion y probar en todas las posiciones tampoco sirve, entonces saltear palabra
                    if direccion == direccion_inicial:
                        salteadas+=1
                        # Si, "Break" porque el while esta dentro del For.
                        break

    if salteadas != 0 : return salteadas
    else: return None

def colocar_palabra(palabra, esfila, pos, inicio) :
    """
    Coloca la palabra dentro de la matriz en la fila/columna especificada.

    Params:
        - palabra: cadena a ubicar
        - esfila: determina si es fila o columna
        - pos: posicion de la fila/columna
        - inicio: margen que tiene desde el inicio de la fila/columna
    """
    if debug_palabras :
        palabra = palabra.upper()

    for x in range(inicio, inicio+len(palabra) ) :
        if esfila:
            matrix[pos][x] = palabra[x-inicio]
        else:
            matrix[x][pos] = palabra[x-inicio]
    return True

def mostrar_tablero(mtx, n):
    """
    Muestra la matriz en forma de tablero, con letras para indicar las columnas y numeros para indicar las filas
    """
    # Cabecera de Columnas
    fila = "/ |"
    for i in range(n):
        fila = fila + " " + chr(65+i)
    print fila
    print "-"*(2*n+3)
    # Cabecera de Filas
    for i in range(n):
        fila = str(i+1)
        if i < 9 : fila += " |"
        else:
            fila+="|"
        for e in range(n):
            fila = fila+" "+mtx[i][e]
        print fila
        fila = ""

    # Nueva linea
    print ""

#============== Ingreso de datos

def pedir_entero(msg, min, max):
    """
    Muestra un mensaje y solo acepta enteros entre param:min y param:max

    Params:
        - msg: Mensaje para mostrar
        - min: entero minimo para aceptar
        - max: entero maximo para aceptar
    """
    while True:
        n = str(raw_input(msg))

        if not n.isdigit() :
            show_msg("Oops! Parece que eso no era un numero entero")
            continue
        
        n = int(n)

        if n <= max and n >= min :
            return n
        else:
            show_msg("Numero fuera de rango")
            continue

def pedir_palabra(msg, min, max):
    """
    Muestra un mensaje y solo acepta palabras con longitud entre param:min y param:max

    Params:
        - msg: Mensaje para mostrar
        - min: longitud entera minimo para aceptar
        - max: longitud entera maxima para aceptar
    """

    while True:
        txt = str(raw_input(msg))

        if not txt.isalpha() :
            show_msg("Oops! Parece que eso no era una palabra valida")
            continue

        if len(txt) > max:
            show_msg("Palabra muy larga (Max %d caracteres)"%max)
            continue
        elif len(txt) < min :
            show_msg("Palabra muy corta (Min %d caracteres)"%min)
            continue
        else:
            return txt.lower()

def procesar_juego(salteadas):
    """
    Una vez iniciado el juego, se toman las entradas del jugador para procesar y determinar si pertenecen a coordenadas validas de palabras

    Params:
        - Salteadas: cantidad de palabras salteadas para mostrar en un mensaje
    """

    global palabras_restantes
    msg_to_show = ""
    
    while palabras_restantes > 0:

        clear_window()

        show_title("Encuentre las palabras")

        # Si por parametro se indica que existen palabras salteadas, mostramos un mensaje

        if salteadas != None:
            show_msg("Palabras restantes: %d Salteadas: %d \n"%(palabras_restantes, salteadas))
        else:
            show_msg("Palabras restantes: %d \n"%palabras_restantes)

        mostrar_tablero(matrix, nxn)

        # Mostramos el mensaje y le agregamos una linea nueva
        if msg_to_show != "":
            show_msg(msg_to_show+"\n")
            msg_to_show = ""


        #============== Entrada y filtrado de texto

        entrada = raw_input(obtener_mensaje("rawinput_coordenadas"))

        if len(entrada) < 5 or len(entrada) > 7 or not "," in entrada:
            msg_to_show = obtener_mensaje("entrada_incorrecta")
            continue

        entradas = entrada.split(",")

        if len(entradas) != 2 :
            msg_to_show = obtener_mensaje("entrada_incorrecta")
            continue

        if not str(entradas[0][1:]).isdigit() or not entradas[1][1:].isdigit() :
            msg_to_show = obtener_mensaje("entrada_incorrecta")
            continue

        #============== Parseo y filtrado de coordenadas

        columna_inicio = entradas[0][0]
        fila_inicio    = int(entradas[0][1:])-1

        columna_final = entradas[1][0]
        fila_final    = int(entradas[1][1:])-1

        if fila_final >= nxn or fila_inicio >= nxn :
            msg_to_show = obtener_mensaje("rango_fila")
            continue

        if ord(columna_inicio.upper())-65 >= nxn or ord(columna_final.upper())-65 >= nxn :
            msg_to_show = obtener_mensaje("rango_columna")
            continue
        else:
            columna_inicio = ord(columna_inicio.upper())-65
            columna_final  = ord(columna_final.upper())-65

        if columna_inicio != columna_final and fila_inicio != fila_final :
            msg_to_show = obtener_mensaje("fila_o_columa_igual")
            continue

        if columna_inicio == columna_final :
            vertical = True
        else:
            vertical = False

        # Se arma una cadena con las coordenadas de la misma forma como fue agregada anteriormente a la lista "posiciones"
        cadena_de_posicion = str(columna_inicio)+str(fila_inicio)+str(columna_final)+str(fila_final)

        #============== Comprobar si existe la palabra. Removerla en caso afirmativo

        if not cadena_de_posicion in posiciones :
            msg_to_show = obtener_mensaje("error_coordenadas")
            continue

        posiciones.remove(cadena_de_posicion)

        #============== Mostrar la palabra en mayuscula

        if vertical :
            for fila in range(min(fila_inicio, fila_final),max(fila_inicio, fila_final)+1) : 
                matrix[fila][columna_final] = str(matrix[fila][columna_final]).upper()
        else:
            for columna in range(min(columna_inicio, columna_final),max(columna_inicio, columna_final)+1) :
                matrix[fila_inicio][columna] = str(matrix[fila_inicio][columna]).upper()


        palabras_restantes -=1
        msg_to_show = "Muy Bien! Encontraste una palabra!"


    #============== FIN DEL JUEGO

    clear_window()

    show_title("FELICIDADES! GANASTE!")
    show_msg("Muy bien, encontraste las %d palabras!" % n_palabras)
    raw_input("Enter para menu principal ")

    return True

#============== Opciones del menu

def juego_nuevo():
    """
    Pedir al jugador la cantidad de filas/columnas, cantidad de palabras y las palabras.
    """
    show_title("Crear sopa de NxN letras")

    global nxn
    global n_palabras
    global palabras_restantes

    nxn         = pedir_entero("Ingrese un numero entero de la cantidad de\nfilas y columnas que desea (Entre 10 y 20):\n",10,20)
    n_palabras  = pedir_entero("Ingrese un numero entero de la cantidad de\npalabas que deasea agregar (Entre 0 y %d):\n"%(nxn/2),0,(nxn/2))

    palabras = []

    palabra_repetida = False
    while len(palabras)<n_palabras:

        if palabra_repetida :
            show_msg("Ingreso una palabra repetida")
            palabra_repetida = False

        # Pedir una palabra que cumpla con los requisitos
        palabra = pedir_palabra("[%d|%d]Ingrese una palabra entre %d y %d caracteres: "%(len(palabras)+1,n_palabras,palabra_min_caracteres,(nxn/2)),palabra_min_caracteres,(nxn/2))

        if palabra in palabras:
            palabra_repetida = True
        else :
            palabras.append(palabra)

    palabras_restantes = n_palabras

    crear_matrix()

    salteadas = procesar_palabras()

    completar_matrix(matrix, nxn, not debug_palabras)

    return procesar_juego(salteadas)

def mostrar_acerca_de():
    """
    Muestra un mensaje de parte del desarrollador.
    """

    show_title("Informacion del Juego")

    show_msg("""La sopa de letras es un pasatiempo inventado por Pedro Ocon de Oro\n
        que consiste en una cuadricula u otra forma geometrica rellena con\n
        diferentes letras para formar palabras.\n""")

    show_msg("http://es.wikipedia.org/wiki/Sopa_de_letras\n")

    show_msg("Creado por Hiamn Paul Olivera Piriz\n")

    show_msg("01/04/2015: TP Nro 1 Algoritmos y Programacion I\n")

    show_msg("Tiempo de creacion aproximado 12 horas (aka 2 tardes)\n")

    raw_input("Enter para menu principal ")

    return True

#============== Init

def menu_inicial():

    clear_window()
    items = ["Juego Nuevo", "Acerca de", "Salir"]

    while True:
        show_title("Menu Inicial")
        item = show_menu(items)
        clear_window()

        if item == 0 :
            juego_nuevo()
            clear_window()
        elif item==1 :
            mostrar_acerca_de()
            clear_window()
        elif item==2 :
            return
        else:
            print "Opcion invalida"

def main():
    show_title("BENVENID@ A")
    completar_matrix(splash, 10, False) # FIXED
    mostrar_tablero(splash, 10)  # FIXED

    global clear_command

    if platform.system()    == "Windows" : clear_command = "cls"
    elif platform.system() == "Linux"    : clear_command = "clear"

    time.sleep(3)                # Duerme 3 segundos

    clear_window()
    menu_inicial()

main()

