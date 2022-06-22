
import numpy as np
import PySimpleGUI as sg
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from Calculadora import *
from UtilitiesGUI import generate_grafic 

def submenugrafico():
    layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.Button("Graficar")],
        [sg.pin(sg.Canvas(key='-CANVAS-', size = (400, 400), visible=False))],
        [sg.Button("Salir")],
    ]

    grafico_window = sg.Window('Metodo Grafico', layout)

    #Variable booleana que nos servirá para determinar si hay o no un grafico en el canvas
    grafico = False

    while True:
        event, values = grafico_window.read()
        
        if event == 'Salir' or event == sg.WIN_CLOSED:
            break
        if event == "Graficar":


            #Obtenemos la funcion ingresda por el usuario y la transformamos
            expresion,variables = transform_fx(values["-IN|FX-"])

            #Obtenemos las raices de la función
            roots = [float(num) for num in sp.solve(expresion)]

            #Obvtenemos los valores de las imagenes de cada raiz
            y_raices = [expresion.subs(variables[0],i).evalf() for i in roots]

            #Generamos los puntos en el eje x entre las raicess
            x = np.linspace(float(roots[0])-1,float(roots[-1])+1, 100)
            #Evaluamos los puntos de x para obtener los valores de y
            y = [expresion.subs(variables[0],i).evalf() for i in x]

            #generamos el grafico en el canvas

            #Si hay un grafico
            if grafico:
                canvas = generate_grafic(metodo="Método Gráfico",xi=x,fi=y,window=grafico_window,key="-CANVAS-",canvas=canvas,expresion=values["-IN|FX-"], raices=roots, img_raices=y_raices)

            #Si el canvas está vacío
            else:
                canvas = generate_grafic(metodo="Método Gráfico",xi=x,fi=y,window=grafico_window,key="-CANVAS-",expresion=values["-IN|FX-"], raices=roots, img_raices=y_raices)

            
            grafico_window["-CANVAS-"].update(visible=True)
            grafico = True

        if event == "-BTN|FX-":
            grafico_window["-IN|FX-"].update(showCalculator())

    grafico_window.close()
    


