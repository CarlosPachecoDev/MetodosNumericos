
from Calculadora import *

def euler(valor_y_inicial, ecuacion,valor_x_inicial, valor_x_final, n=None, h = None):

    if h == None:
        if n == None:
            n = 10
        h = (valor_x_final - valor_x_inicial)/n
    
    ecuacion, variables = transform_fx(ecuacion)
    salida = []
    n = 0
    salida.append([n,valor_x_inicial,valor_y_inicial," - "])
    
    while valor_x_inicial < valor_x_final:
        new_row = []
        n += 1
        new_row.append(n)

        #Formula de euler centrado
        y_n1_centrado = valor_y_inicial + h*ecuacion.subs([(y, valor_y_inicial), (x, valor_x_inicial)]).evalf()

        #Eulker mejorado
        y_n1 = valor_y_inicial + h*((ecuacion.subs([(y, valor_y_inicial), (x, valor_x_inicial)]).evalf() + ecuacion.subs([(y, y_n1_centrado), (x, round(valor_x_inicial + h,3))]).evalf())/2)
        
        
        valor_x_inicial = round(valor_x_inicial + h,3)
        new_row.append(valor_x_inicial)
        new_row.append(y_n1)
        new_row.append(y_n1_centrado)
        salida.append(new_row)
        valor_y_inicial = y_n1
    return salida


def solve_euler_mejorado():

    # MainLayout
    main_layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.pin(sg.Text("Valor inicial de x:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALX-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("Valor inicial de y:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALY-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("h:", key="-TXT|H-")), sg.pin(sg.Input(enable_events=True, key="-IN|H-", size=(13, 1)))],
        [sg.pin(sg.Text("Valor de x a encontrar:", key="-TXT|VALXI-")), sg.pin(sg.Input(enable_events=True, key="-IN|VALXI-", size=(13, 1)))],
        [sg.Table(values=[],headings=["n","Xn","Yn","Euler centrado"], key="-TXT|RES-",auto_size_columns=True,expand_x=True, justification="center")],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    mejorado_euler_window = sg.Window('', main_layout, no_titlebar=True, margins=(0,0))

    while True:
        event, values = mejorado_euler_window.read()
        if event == "-BTN|FX-":
            mejorado_euler_window["-IN|FX-"].update(showCalculator())

            
        if event == "-BTN|SOLVE-":
            
            if values["-IN|H-"] != "":
                respuesta = euler(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), h=float(values['-IN|H-']),valor_x_final=float(values['-IN|VALXI-']))
            else:
                respuesta = euler(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), valor_x_final=float(values['-IN|VALXI-']))
            
            mejorado_euler_window['-TXT|RES-'].update(values=respuesta)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
        
    mejorado_euler_window.close()
