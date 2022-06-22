from Calculadora import *


def taylor(ecuacion,valor_x_final,valor_x_inicial,valor_y_inicial, orden,h = None, n= None):

    if h == None:
        if n == None:
            n = 10
        h = (valor_x_final - valor_x_inicial)/n

    iteraciones = int((valor_x_final - valor_x_inicial)/h)
    print(iteraciones)
    derivadas_implicitas = []
    ecuacion,variables = transform_fx(ecuacion)
    #Obteniendo las derivadas implicitas
    for i in range(orden-1):

        if i == 0:
            diff_i = sp.diff(ecuacion,x) + sp.diff(ecuacion,y) * ecuacion
        else:
            diff_i = sp.diff(derivadas_implicitas[i-1],x) + sp.diff(derivadas_implicitas[i-1],y) * ecuacion

        derivadas_implicitas.append(diff_i)     

    salida = [["i", "Xi", "Yi"]]
    salida.append([0,valor_x_inicial,valor_y_inicial])
    for  i in range(iteraciones):   

        y_i = valor_y_inicial + (h*ecuacion.subs([(x, valor_x_inicial), (y, valor_y_inicial)]).evalf())

        for j in range(len(derivadas_implicitas)):
            if j == 0:
                y_i += (h**(2+j)*(derivadas_implicitas[j].subs([(x, valor_x_inicial), (y, valor_y_inicial)]).evalf()))/2
            else:
                y_i += (h**(2+j)*(derivadas_implicitas[j].subs([(x, valor_x_inicial), (y, valor_y_inicial)]).evalf()))/math.factorial(orden)

        
        valor_x_inicial += h
        valor_y_inicial = y_i
        salida.append([(i+1),valor_x_inicial,valor_y_inicial])

    return salida

def solve_taylor():

    # MainLayout
    main_layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.pin(sg.Text("Orden:", key="-TXT|ORDEN-")), sg.pin(sg.Input(enable_events=True, key="-IN|ORDEN-", size=(13, 1)))],
        [sg.pin(sg.Text("Valor inicial de x:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALX-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("Valor inicial de y:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALY-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("h:", key="-TXT|H-")), sg.pin(sg.Input(enable_events=True, key="-IN|H-", size=(13, 1)))],
        [sg.pin(sg.Text("Valor de x a encontrar:", key="-TXT|VALXI-")), sg.pin(sg.Input(enable_events=True, key="-IN|VALXI-", size=(13, 1)))],
        [sg.Table(values=[],headings=["n","Xn","Yn"], key="-TXT|RES-",auto_size_columns=True,expand_x=True, justification="center")],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    taylor_window = sg.Window('', main_layout, no_titlebar=True, margins=(0,0))

    while True:
        event, values = taylor_window.read()

        if event == "-BTN|FX-":
            taylor_window["-IN|FX-"].update(showCalculator())

            
        if event == "-BTN|SOLVE-":
            
            if values["-IN|H-"] != "":
                respuesta = taylor(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), h=float(values['-IN|H-']),valor_x_final=float(values['-IN|VALXI-']), orden=int(values['-IN|ORDEN-']))
            else:
                respuesta = taylor(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), valor_x_final=float(values['-IN|VALXI-']), orden=int(values['-IN|ORDEN-']))
            
            taylor_window['-TXT|RES-'].update(values=respuesta)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    
    taylor_window.close()

