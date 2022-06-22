
from UtilitiesGUI import sg
import math


def arcsenx(x1, n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    ea = 1000
    real = math.asin(x)
    n = 2

    aprox = x + ((1 / 2) * (((x) ** 3) / 3))
    while (ea > ess):
        # la variable ant se iguala a la variable aprox, esto servira para el calculo del Ea
        ant = aprox
        # la aproximacion cambiara de valor, este valor viene dado a traves de serie de taylor
        aprox = aprox + (((math.factorial(2 * n)) / (((2 ** n) * math.factorial(n)) ** 2)) * ((x ** ((2 * n) + 1)) / ((2 * n) + 1)))
        # se calcula el error
        ea = abs(((aprox - ant) / aprox) * 100)
        n = n + 1
    valor = aprox
    error1 =  ea

    return real, valor, error1



def submenuarsen():
    layout = [
        [sg.Text('Ingrese su valor de X en el intervalo de ]-1,1[')],
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

    windowarc = sg.Window('Serie de Taylor para Arcsen(x)', layout)

    while True:
        event , values = windowarc.read()
        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])
            if x0 <= -1 or x0 >= 1:
                sg.popup("Ha ingresado un numero que no se encuentra en el intervalo", no_titlebar=True)
            else:
                r,v,e = arcsenx(x0,n0)
                windowarc['-REAL-'].update(visible=True)
                windowarc['-REAL1-'].update(r,visible=True)
                windowarc['-METODO-'].update(visible= True)
                windowarc['-METODO1-'].update(v,visible=True)
                windowarc['-ERROR-'].update(visible=True)
                windowarc['-ERROR1-'].update(e,visible=True)
    windowarc.close()