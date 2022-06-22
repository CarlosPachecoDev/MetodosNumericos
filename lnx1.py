import PySimpleGUI as sg
import math

def lnx(x1, n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    ea = 100
    real = math.log(1+x)
    aprox = x
    it = 1

    while ea>ess:
        ant = aprox
        aprox = aprox + (((-1) ** (it)) / (it + 1)) * (x ** (it + 1))
        ea = abs(((aprox - ant) / aprox) * 100)
        it = it+1
    valor = aprox
    error1 = ea

    return real , valor, error1




def submenulnxm1():
    
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

    windowln = sg.Window('Serie de Taylor para ln(x+1)', layout)

    while True:
        event , values = windowln.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])

            if x0 <= -1 or x0 >= 1:
                sg.popup("Ha ingresado un numero que no se encuentra en el intervalo", no_titlebar=True)
            else:
                r,v,e =  lnx(x0,n0)
                windowln['-REAL-'].update(visible=True)
                windowln['-REAL1-'].update(r,visible=True)
                windowln['-METODO-'].update(visible= True)
                windowln['-METODO1-'].update(v,visible=True)
                windowln['-ERROR-'].update(visible=True)
                windowln['-ERROR1-'].update(e,visible=True)

    windowln.close()

