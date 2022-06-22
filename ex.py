
import PySimpleGUI as sg
import math
from sympy import *

def resoexp(x1,n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    real = exp(x)
    ea = 100
    aprox = 1
    n = 1

    while ea > ess:
        ant = aprox
        aprox = aprox + (((x) ** n)  / math.factorial(n))
        ea = abs(((aprox - ant) / aprox) * 100)
        n = n + 1
    
    valor = aprox
    error1 = ea
    return real, valor, error1
    

def submenuexp():
    layout = [
        [sg.Text('Ingrese su valor de X')],
        [sg.Input()],
        [sg.Text('Ingrese cantidad de cifras significativas')],
        [sg.Input()],
        [sg.Text('Valor Real',key='-REAL-', visible= False)]+
        [sg.Text('', key='-REAL1-', visible=False)],
        [sg.Text('Valor Mediante el Metodo', key='-METODO-', visible= False)]+
        [sg.Text('', key='-METODO1-', visible=False)],
        [sg.Text('Error', key='-ERROR-', visible= False)]+
        [sg.Text('', key='-ERROR1-', visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')]

    ]

    windowexp = sg.Window('Serie de Taylor para e^x', layout)

    while True:
        event, values = windowexp.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])

            r,v,e =resoexp(x0,n0)
            windowexp['-REAL-'].update(visible=True)
            windowexp['-REAL1-'].update(r,visible=True)
            windowexp['-METODO-'].update(visible= True)
            windowexp['-METODO1-'].update(v,visible=True)
            windowexp['-ERROR-'].update(visible=True)
            windowexp['-ERROR1-'].update(e,visible=True)

    windowexp.close()     
