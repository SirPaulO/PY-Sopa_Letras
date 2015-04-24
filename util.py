import platform
import os

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
    if platform.system()    == "Windows" : os.system("cls")
    elif platform.system() == "Linux"    : os.system("clear")

def obtener_mensaje(identificador):
    if identificador == "rawinput_coordenadas" : return "Ingrese Celdas de Inicio y Final de la palabra (EJ: A3,C4): "
    if identificador == "entrada_incorrecta" : return "Entrada incorrecta. (EJ: A3,C4)"
    if identificador == "rango_fila" : return "Fila fuera de rango"
    if identificador == "rango_columna" : return "Columna fuera de rango"
    if identificador == "fila_o_columa_igual" : return "Al menos fila o columna, inicial y final deben coincidir."
    if identificador == "error_coordenadas" : return "Mmm.. No se encontro ninguna palabra nueva en ese par de coordenadas"