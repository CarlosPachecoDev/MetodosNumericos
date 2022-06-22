import pandas as pd
import math
import numpy as np
import PySimpleGUI as sg
from UtilitiesGUI import *
from Calculadora import x
import matplotlib.pyplot as plt

def show_table(df, respuesta):

    fig, ax =plt.subplots(1,1)
    column_labels=["Column 1", "Column 2", "Column 3", "Column 3", "Column 3"]
    df=pd.DataFrame(df,columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    ax.set_title(respuesta)
    ax.table(cellText=df.values,colLabels=column_labels,loc="center")
    plt.show()

#Función encargada de mostrar la respuesta
def show_respuesta(df, n, respuesta):

    #Definimos y generamos dinámicamente los encabezados de la tabla de diferencias divididas
    header_list = list()
    data = df.tolist()
    header_list.append("X")
    header_list.append("f(x)")
    header_list.extend([f"{i+1}" for i in range(n-1)])

    #Definimos el layout del modal de respuestas
    layout = [
        [sg.Table(values=data, headings=header_list, auto_size_columns=False, display_row_numbers=True)],
        [sg.Text(respuesta)],
        [sg.Button("Ok")]
    ]


    modal_respuestas = sg.Window('', layout, grab_anywhere=False, no_titlebar=True)
    event, values = modal_respuestas.read()
    modal_respuestas.close()

#Función encargada de llenar las primeras 2 columnas de la tabla de diferencias divididas con los valores de x e y
def llenarprimerasdoscolumnas(xi,y,matriz):
    matriz.T[0]=xi
    matriz.T[1]=y

    #Una vez se hayan llenado las primeras 2 columnas retornamos la matriz
    return matriz


#Funcion encargada de llenar las columnas restantes de la tabla de diferencias divididas
def diferencias(xi,y,n,b, derivadas):
    
    #Inicializamos la lista de los encabezados
    headings = ["X", "f(x)"]

    #Dimensionar dinamicamente la matriz
    matriz = np.array([[0]*(n+1)]*(n),dtype=float)
    
    #Llamamos a la función encargada de llenas las primeras 2 columnas
    matriz = llenarprimerasdoscolumnas(xi,y,matriz)

    for i in range(n-1):

        #Llenamos las primeras (i+1) filas del nivel i de la tabla con ceros
        new_col = [0]*(i+1)

        #LLenamos el restos de celdas con los valores obtenidos mediante las diferencias divididas
        for j in range(n-(i+1)):
            if (matriz[j+(i+1)][i+1]-matriz[j+i][i+1] == 0) and (matriz[j+(i+1)][0]-matriz[j][0] == 0):
                key = str(xi[j])
                diffs = derivadas.get(key)
                new_col.append(round(diffs[(i)]/math.factorial(i+1),4))
            else:    
                new_col.append(round((matriz[j+(i+1)][i+1]-matriz[j+i][i+1])/(matriz[j+(i+1)][0]-matriz[j][0]),4))

        #añadimos la nueva columna a la matriz y obtenemos el valor b sub i
        b.append(new_col[i+1])    
        matriz[:,(i+2)] = new_col
        headings.append(f"{i+1}")

    #Generamos un dataframe con la matriz obtenida en las diferencias divididas y la retornamos

    return matriz

    
def hermite_diff(datos): 

    #Lista para almacenas los valores de b
    b = [ ]
    #Lista para almacenas los valores de x inggresados por el usuario
    xi = []
    #Lista para almacenar los valores de y ingresados por el usuario
    y = []

    #Diccionario para almacenar los valores de las derivadas correspondientes a cada valor de x
    #    ejemplo:
    #    "valor x": [primera derivada, segunda derivada, tercera derrivada, .... ,derivada enésima)]
    
    derivadas = {}
    
    #Obtenemos los valores de x ingresados por el usuario
    for fila in datos:
        xi.append(float(fila[0]))

    #Obtenemos los valores de y ingresados por el usuario
    for fila in datos:
        y.append(float(fila[1]))

    #Obtenemos los valores de las derivadas ingresadas por el usuario
    #Para eso recorremos las filas de la matriz de datos
    for i in range(len(datos)):
        #Instanceamos la lista que almacenará los valores de las derivadas de cada valor de x
        diff = []

        #Recorremos cada celda de la fila iniciando desde la tercera porque las primeras 2 columnas son para los valores de x e y
        for j in range(2,len(datos[i])):

            #Si el valor en esa celda es una cadena vacía indica que no hay derivada de orden n para la función f(X) en el valor de x
            if datos[i][j] != "":
                #Si existe una derivada la añadimos a la lista
                diff.append(float(datos[i][j]))

        #Generamos el par clave_valor de las derivadas obtenidas en la fila iterada
        derivadas[str(xi[i])] = diff

    #Creamos una copia de las listas xi e y
    xi2 = list(xi)
    y2 = list(y)

    #Borramos el contenido de las listas xi e y
    xi.clear()
    y.clear()

    #Volvemos a llenar las listas xi e y pero ahora nos encargamos de ir repitiendo los valores de x e y que contienen derivadas
    for i in range(len(xi2)):

        #Obtenemos la cantidad de derivadas que hay en la fila con el valor de Xi y sumamos 1, esto nos indicará la cantidad de veces a repetir los valor de Xi e y
        repeticiones = len(derivadas[str(xi2[i])]) + 1

        #Obtenemos los valores que vamos a repetir
        valor = xi2[i]
        valor2 = y2[i]

        #Añadimos todas las repeticiones a la lista original de Xi e y que previamente habíamos limpiado
        for j in range(repeticiones):
            xi.append(valor)
            y.append(valor2)

    #Obtenemos la cantidad  valores de x
    n = len(xi)

    #Llamamos a la función encargada de realizar las diferencias divdidas
    df = diferencias(xi=xi,y=y,n=n,b=b,derivadas=derivadas)

    #Formamos el polinomio
    polinomio = y[0]
    for i in range(1,n):
        factor = b[i-1]
        termino = 1
        for k in range(i):
            termino = termino*(x-xi[k])
        polinomio = polinomio + termino*factor

    #Simplificamos el polinomio obtenido
    polisimple = polinomio.expand()
    respuesta = f"El polinomio es: {polisimple}"
    return respuesta, df, n, polisimple

#Función principal con la que interactúa el usuario
def solve_hermite():

    # MainLayout
    main_layout = [
        [sg.pin(sg.Text("Cantidad de valores de X:", key="-TXT|VX-")), sg.pin(sg.Input(enable_events=True, key="-IN|VX-", size=(30, 1)))], 
        [sg.pin(sg.Text("Cantidad de valores de Y:", key="-TXT|VY-")), sg.pin(sg.Input(enable_events=True, key="-IN|VY-", size=(30, 1)))],
        [sg.pin(sg.Text("Orden mayor de las derivadas:", key="-TXT|DIFF-")), sg.pin(sg.Input(enable_events=True, key="-IN|DIFF-", size=(13, 1))), sg.pin(sg.Button('Llenar tabla',key="-BTN|FILL-", visible=False))],
        [sg.pin(sg.Text("¿Desea evaluar algún punto?", key="-TXT|EVAL-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='YES', metadata=False, visible=False)), sg.pin(sg.Text('Si', k="-YES-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='NO', metadata=False, visible=False)), sg.pin(sg.Text('No', k="-NO-", visible=False))],
        [sg.pin(sg.Text("Ingrese el valor a evaluar:", key="-TXT|VAL-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VAL-", size=(13, 1), visible=False))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-", visible=False)],
        [sg.pin(sg.Canvas(key='-CANVAS-'))]
    ]

    # Iniciamos la ventana
    hermitediff_window = sg.Window('', main_layout)

    #Definimos la lista de inputs que solo admitirán  valores enteros positivos
    INT_INPUTS = ["-IN|VX-", "-IN|VY-", "-IN|DIFF-"]

    #Definimos la lista de inputs que solo admitirán  valores numéricos ya sea enteros o flotantes positivos o negativos
    FLOAT_INPUTS = ["-IN|VAL-"]

    radio_keys = ('YES', 'NO')

    def check_radio(key):
        for k in radio_keys:
            hermitediff_window[k].update(radio_unchecked)
            hermitediff_window[k].metadata = False
        hermitediff_window[key].update(radio_checked)
        hermitediff_window[key].metadata = True
    
    #Variable booleana para determinar si se han obtenido todos los datos para asi mostrar el botón de resolver
    Buttom_flag = False

    #Bucle de eventos
    while True:

        
        event, values = hermitediff_window.read()
        if event in radio_keys:
            check_radio(event)


        # Validando ingreso unicamente de numeros en inputs
        if event in INT_INPUTS and len(values[event]) and values[event][-1] not in ('123456789'):
            hermitediff_window[event].update(values[event][:-1])

        elif event in FLOAT_INPUTS and len(values[event]) and values[event][-1] not in ('-123456789.'):
            hermitediff_window[event].update(values[event][:-1])

        else:
            if values["-IN|DIFF-"] != "" and values["-IN|VX-"] != "" and values["-IN|VY-"] != "":
                show(["-BTN|FILL-"], hermitediff_window)
            else:
                hide(["-BTN|FILL-"], hermitediff_window)


        if event == "-BTN|FILL-":
            headings = []
            headings.append("x")
            headings.append("y")
            headings.extend([f"f"+"'"*orden+"(x)" for orden in range(1,int(values["-IN|DIFF-"])+1)])
            datos = create_table(cols=(2+int(values["-IN|DIFF-"])), rows= int(values["-IN|VX-"]), headings= headings)
            respuesta, tabla, n, polinomio = hermite_diff(datos=datos)
            show(["-TXT|EVAL-","YES","NO","-YES-","-NO-"], hermitediff_window)

        #Si el usuario dice que si, se le muestra el input para ingresar el valor a evaluar
        if event == "YES":
            show(["-TXT|VAL-","-IN|VAL-"], hermitediff_window)
            hide(["-BTN|SOLVE-"], hermitediff_window)
            Buttom_flag = False

        #Si el usuario dice que no, se oculta el input para ingresar el valor a evaluar
        elif event == "NO":
            hide(["-TXT|VAL-","-IN|VAL-"], hermitediff_window)
            show(["-BTN|SOLVE-"], hermitediff_window)
            Buttom_flag = True
            
        #Si ha ingresado el valor a evaluar se le muestra el botón de resolver
        if values["-IN|VAL-"] != "":
            Buttom_flag = True

        #Todo está correcto, asi que se muestra el botón de resolver    
        if Buttom_flag:
            show(["-BTN|SOLVE-"], hermitediff_window)

        #En caso contrario se oculta
        else:
            hide(["-BTN|SOLVE-"], hermitediff_window)

        if event == "-BTN|SOLVE-":
            if values["-IN|VAL-"] != "":
                respuesta += f"\nAl evaluar {values['-IN|VAL-']} en el plonimio se obtiene: {polinomio.subs(x, float(values['-IN|VAL-'])).evalf()}"
            show_respuesta(tabla, n, respuesta)
            #show_table(df=tabla, respuesta=respuesta)


        if event == "Salir" or event == sg.WIN_CLOSED:
            break

    hermitediff_window.close()



