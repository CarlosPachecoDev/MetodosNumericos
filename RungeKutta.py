
from UtilitiesGUI import *
from Calculadora import *

def runge_kutta(ecuacion, valor_y_inicial, valor_x_inicial, valor_x_final = None, orden = None, h = None):
    
    FORMULAS_RUNGE_KUTTA = {
        "2": {
            "k": {
                1: lambda ecuacion: ecuacion.subs([(x, xi), (y, yi)]).evalf(),
                2: lambda ecuacion: ecuacion.subs([(x, xi + h), (y, yi + (k_values[k-1]*h))]).evalf()
            },
            "y": lambda yi: yi + ((1/2)*h) * (k_values[0] + k_values[1])
        },
        "3": {
            "k": {
                1: lambda ecuacion: ecuacion.subs([(x, xi), (y, yi)]).evalf(),
                2: lambda ecuacion: ecuacion.subs([(x, xi + (0.5*h)), (y, yi + (0.5*k_values[k-1]*h))]).evalf(),
                3: lambda ecuacion: ecuacion.subs([(x, xi + h), (y, yi - (k_values[k-2]*h) + 2*(k_values[k-1]*h))]).evalf()
                
            },
            "y": lambda yi: yi + (h/6) * (k_values[0] + 4*k_values[1] + k_values[2])
        },
        "4": {
            "k": {
                1: lambda ecuacion: ecuacion.subs([(x, xi), (y, yi)]).evalf(),
                2: lambda ecuacion: ecuacion.subs([(x, xi + (h/2)), (y, yi + ((h*k_values[k-1])/2))]).evalf(),
                3: lambda ecuacion: ecuacion.subs([(x, xi + (h/2)), (y, yi + ((h*k_values[k-1])/2))]).evalf(),
                4: lambda ecuacion: ecuacion.subs([(x, xi + h), (y, yi + h*k_values[k-1])]).evalf()
            },

            "y": lambda yi: yi + (h/6) * (k_values[0] + 2*k_values[1] + 2*k_values[2] + k_values[3])
        }
    }
    ecuacion,variables = transform_fx(ecuacion)
    xi = valor_x_inicial
    yi = valor_y_inicial
    respuestas = list()
    salida = ""

    itc = round(((valor_x_final- valor_x_inicial) / h))

    if h == None:
        h = (valor_x_final - valor_x_inicial)/5

    for i in orden:
        salida += "\n____________________________________"
        salida += f"\n\nOrden {i}"

        for j in range(itc+1):
            salida += f"\n\n\tIteracion {j+1}:"
            k_values = list()
            
            salida += f"\n\n\t\tValores de K:"

            for k in range(len(FORMULAS_RUNGE_KUTTA[i]["k"])):
                
                k_values.append(FORMULAS_RUNGE_KUTTA[i]["k"][k+1](ecuacion))
                salida += f"\n\n\t\t\t{k+1}- {k_values[k]}"
        
            salida += f"\n\n\t\ty{j+1}= {yi}\n"
            yi = FORMULAS_RUNGE_KUTTA[i]["y"](yi)
            respuestas.append(yi)
            xi += h
        

    
    return salida, respuestas 


def solve_rungekutta():

    # MainLayout
    main_layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.Text('Orden: ', key="-TXT|ORDEN-"), sg.Image(radio_unchecked, enable_events=True, k='2', metadata=False), sg.T('Orden 2', k="T2"), sg.Image(radio_unchecked, enable_events=True, k='3', metadata=False), sg.T('Orden 3', k="T3"), sg.Image(radio_unchecked, enable_events=True, k='4', metadata=False), sg.T('Orden 4', k="T4")],
        [sg.pin(sg.Text("Valor inicial de x:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALX-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("Valor inicial de y:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALY-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("h:", key="-TXT|H-")), sg.pin(sg.Input(enable_events=True, key="-IN|H-", size=(13, 1)))],
        [sg.pin(sg.Text("Valor de x a encontrar:", key="-TXT|VALXI-")), sg.pin(sg.Input(enable_events=True, key="-IN|VALXI-", size=(13, 1)))],
        [sg.pin(sg.Multiline(disabled=False,visible=False, key="-TXT|RES-", auto_size_text= True, auto_refresh= True, size= (60,15)))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    rungekutta_window = sg.Window('', main_layout)

    #Definimos la lista de inputs que solo admitirán  valores numéricos ya sea enteros o flotantes positivos o negativos
    FLOAT_INPUTS = ["-IN|VALX-", "-IN|VALY-", "-IN|VALXI-"]

    radio_keys = ('2', '3', '4')
    radio_keys2 = ('YES', 'NO')

    orden = list()

    def check_radio(key):
            for k in radio_keys2:
                rungekutta_window[k].update(radio_unchecked)
                rungekutta_window[k].metadata = False
            rungekutta_window[key].update(radio_checked)
            rungekutta_window[key].metadata = True
            
    #Bucle de eventos
    while True:

        
        event, values = rungekutta_window.read()
        print(values)
        
        # Eventos para los radiobuttom
        if event in radio_keys:
            if rungekutta_window[event].metadata:
                uncheck(event, rungekutta_window, orden)
                
            else:
                check(event, rungekutta_window, orden)

        if event in radio_keys2:
            check_radio(event)

        if event == "-BTN|FX-":
            rungekutta_window["-IN|FX-"].update(showCalculator())

        # Validando ingreso unicamente de numeros en inputs
        if event in FLOAT_INPUTS and len(values[event]) and values[event][-1] not in ('-0123456789.'):
            rungekutta_window[event].update(values[event][:-1])

            
        if event == "-BTN|SOLVE-":
            orden.sort()
            
            if values["-IN|H-"] != None:
                respuesta,yi = runge_kutta(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), h=float(values['-IN|H-']), orden=orden, valor_x_final=float(values['-IN|VALXI-']))
            else:
                respuesta,yi = runge_kutta(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), valor_x_final=float(values['-IN|VALXI-']), orden=orden)
            rungekutta_window['-TXT|RES-'].update(value=respuesta, visible = True)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    
    rungekutta_window.close()