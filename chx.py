import PySimpleGUI as sg
import math

def cosenohiperbolico(x1,n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    real = math.cosh(x)
    print(real)
    ea = 100
    aprox = 1
    n = 1

    while ea>ess:
        ant = aprox
        aprox = aprox + (((1) ) * (x ** (2 * n)) / math.factorial(2 * n))
        ea = abs(((aprox - ant) / aprox) * 100)
        n = n + 1
    valor = aprox
    error1 = ea

    return real, valor, error1


def submenucosehiperbolico():
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

    windowcoseh = sg.Window('Serie de Taylor para cos(x)', layout)

    while True:
        event , values = windowcoseh.read()
        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])

            r,v,e = cosenohiperbolico(x0, n0)
            windowcoseh['-REAL-'].update(visible=True)
            windowcoseh['-REAL1-'].update(r,visible=True)
            windowcoseh['-METODO-'].update(visible= True)
            windowcoseh['-METODO1-'].update(v,visible=True)
            windowcoseh['-ERROR-'].update(visible=True)
            windowcoseh['-ERROR1-'].update(e,visible=True)

    windowcoseh.close()