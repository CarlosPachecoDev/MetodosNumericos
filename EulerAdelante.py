
from Calculadora import *


def euler(valor_y_inicial, ecuacion, valor_x_inicial, valor_x_final, h = None):

    if h == None:
        h = (valor_x_final - valor_x_inicial)/10

    i = 0
    salida = [[i,valor_x_inicial,valor_y_inicial]]
    ecuacion, variables = transform_fx(ecuacion)
    while valor_x_inicial < valor_x_final:
        i += 1
        y_n = valor_y_inicial + h*ecuacion.subs([(y, valor_y_inicial), (x, valor_x_inicial)]).evalf()
        valor_x_inicial = round(valor_x_inicial + h,2)
        valor_y_inicial = y_n
        salida.append([i,valor_x_inicial,valor_y_inicial])
    
    return salida

def solve_euler_adelante():

    # MainLayout
    main_layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.pin(sg.Text("Valor inicial de x:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALX-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("Valor inicial de y:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALY-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("h:", key="-TXT|H-")), sg.pin(sg.Input(enable_events=True, key="-IN|H-", size=(13, 1)))],
        [sg.pin(sg.Text("Valor de x a encontrar:", key="-TXT|VALXI-")), sg.pin(sg.Input(enable_events=True, key="-IN|VALXI-", size=(13, 1)))],
        [sg.Table(values=[],headings=["n","Xn","Yn"], key="-TXT|RES-",auto_size_columns=True,expand_x=True, justification="center")],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    adelante_euler_window = sg.Window('', main_layout, no_titlebar=True, margins=(0,0))

    while True:

        event, values = adelante_euler_window.read()
        if event == "-BTN|FX-":
            adelante_euler_window["-IN|FX-"].update(showCalculator())

            
        if event == "-BTN|SOLVE-":
            
            if values["-IN|H-"] != "":
                respuesta = euler(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), h=float(values['-IN|H-']),valor_x_final=float(values['-IN|VALXI-']))
            else:
                respuesta = euler(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), valor_x_final=float(values['-IN|VALXI-']))
            
            adelante_euler_window['-TXT|RES-'].update(values=respuesta)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    
    adelante_euler_window.close()
