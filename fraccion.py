import PySimpleGUI as sg

def fraccion(x1, n1):
    ess = (0.5)*(10**(2-n1))
    x = x1
    ea = 100
    real = (1)/(1+x**2)
    aprox = 1
    it = 1
    while ea>ess:
        ant = aprox
        aprox = aprox + ((-1) ** (it)) * (x ** (2 * it))
        ea = abs(((aprox - ant) / aprox) * 100)
        it = it+1
    valor = aprox
    error1 = ea

    return real, valor, error1

def submenufraccion():
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
    windowfrac = sg.Window('Serie de Taylor para 1/1+x^2', layout)

    while True:
        event , values = windowfrac.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            x0 = float(values[0])
            n0 = int(values[1])

        if x0 <= -1 or x0 >= 1:
                sg.popup("Ha ingresado un numero que no se encuentra en el intervalo", no_titlebar=True)
        else:
            r,v,e =fraccion(x0,n0)
            windowfrac['-REAL-'].update(visible=True)
            windowfrac['-REAL1-'].update(r,visible=True)
            windowfrac['-METODO-'].update(visible= True)
            windowfrac['-METODO1-'].update(v,visible=True)
            windowfrac['-ERROR-'].update(visible=True)
            windowfrac['-ERROR1-'].update(e,visible=True)

    windowfrac.close()
