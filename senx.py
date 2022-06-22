import PySimpleGUI as sg
import math

def senoo(x1,n1):
    ess = (0.5)*(10**(2-n1))
    cifras = -1
    ea = 1000
    x = x1
    real = math.sin(x)
    aprox = x
    n = 1
    while (ea > ess):
        ant = aprox
        aprox = aprox + (((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1))
        # Calculamos el Ea
        ea = abs(((aprox - ant) / aprox) * 100)
        n = n + 1
    valor  = aprox
    error1 = ea

    return real, valor, error1



def submenusen():
    layout = [
        [sg.Text('Ingrese su valor de X')],
        [sg.Input()],
        [sg.Text('Ingrese cantidad de cifras significativas ')],
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

    windowsen = sg.Window('Serie de Taylor para Sen(X)', layout)
    while True:
        event, values = windowsen.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])
            r,v,e = senoo(x0, n0)

            windowsen['-REAL-'].update(visible=True)
            windowsen['-REAL1-'].update(r,visible=True)
            windowsen['-METODO-'].update(visible= True)
            windowsen['-METODO1-'].update(v,visible=True)
            windowsen['-ERROR-'].update(visible=True)
            windowsen['-ERROR1-'].update(e,visible=True)
            
    windowsen.close()