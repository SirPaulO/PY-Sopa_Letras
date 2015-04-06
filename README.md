# prog1-tp1-python-sopa_de_letras
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