import PySimpleGUI as sg
import math


def coss(x1, n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    real = math.cos(x)
    ea = 100
    aprox = 1
    n = 1

    while ea>ess:
        ant = aprox
        aprox = aprox + (((-1) ** n) * (x ** (2 * n)) / math.factorial(2 * n))
        ea = abs(((aprox - ant) / aprox) * 100)
        n = n + 1

    valor = aprox
    error1  = ea

    return real, valor, error1



def submenucos():
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

    windowcos = sg.Window('Serie de Taylor para Cos(X)', layout)
    while True:
        event, values = windowcos.read()
        if event == 'Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])
            
            r,v,e = coss(x0,n0 )
            windowcos['-REAL-'].update(visible=True)
            windowcos['-REAL1-'].update(r,visible=True)
            windowcos['-METODO-'].update(visible= True)
            windowcos['-METODO1-'].update(v,visible=True)
            windowcos['-ERROR-'].update(visible=True)
            windowcos['-ERROR1-'].update(e,visible=True)

    windowcos.close()

        
        

