from UtilitiesGUI import sg
import math

def arctgx(x1,n1):
    
    ess = (0.5)*(10**(2-n1))
    x = x1
    ea = 100
    real = math.atan(x)
    aprox = x
    it = 1
    while ea>ess:
        ant = aprox
        aprox = aprox + (((-1) ** (it)) * (x ** ((2 * it) + 1))) / ((2 * it) + 1)
        ea = abs(((aprox - ant) / aprox) * 100)
        it = it+1

    error1 = ea
    valor = aprox

    return real, valor, error1
    
    



def submenuarctang():
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

    windowarctg = sg.Window('Serie de Taylor para Arctang(x)', layout)
    while True:
        event , values = windowarctg.read()
        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])

            if x0 <= -1 or x0 >= 1:
                sg.popup("Ha ingresado un numero que no se encuentra en el intervalo", no_titlebar=True)
            else:
                r,v,e =arctgx(x0,n0)
                windowarctg['-REAL-'].update(visible=True)
                windowarctg['-REAL1-'].update(r,visible=True)
                windowarctg['-METODO-'].update(visible= True)
                windowarctg['-METODO1-'].update(v,visible=True)
                windowarctg['-ERROR-'].update(visible=True)
                windowarctg['-ERROR1-'].update(e,visible=True)

    windowarctg.close()
