
from UtilitiesGUI import *
from Calculadora import *
from RungeKutta import runge_kutta

def adams_moulton(ecuacion, paso, xi, yi, h):
    FORMULAS_ADAMS_MOULTON = {
        "1": lambda yi: yi[0] + ((1/2)*h) * (ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) + ecuacion.subs([(x, xi[0]), (y, yi[0])])),
        "3": lambda yi: yi[2] + ((1/24)*h) * (9*ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) + 19*ecuacion.subs([(x, xi[2]), (y, yi[2])]) - 5*ecuacion.subs([(x, xi[1]), (y, yi[1])]) + ecuacion.subs([(x, xi[0]), (y, yi[0])])),
        "4": lambda yi: yi[3] + ((1/720)*h) * (251*ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) + 646*ecuacion.subs([(x, xi[3]), (y, yi[3])]) - 264*ecuacion.subs([(x, xi[2]), (y, yi[2])]) + 106*ecuacion.subs([(x, xi[1]), (y, yi[1])]) - 19*ecuacion.subs([(x, xi[0]), (y, yi[0])]))
    }

    return FORMULAS_ADAMS_MOULTON[paso](yi)

def adams_bashforth(ecuacion, paso, valor_y_inicial, valor_x_inicial, h):
    print("BASHFORT")
    
    FORMULAS_ADAMS_BASHFORTH = {
        "2": lambda yi: yi[-1] + ((1/2)*h) * (3*ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) - ecuacion.subs([(x, xi[0]), (y, yi[0])])),
        "3": lambda yi: yi[-1] + ((1/12)*h) * (23*ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) - 16*ecuacion.subs([(x, xi[1]), (y, yi[1])]) + 5*ecuacion.subs([(x, xi[0]), (y, yi[0])])),
        "4": lambda yi: yi[-1] + ((1/24)*h) * (55*ecuacion.subs([(x, xi[-1]), (y, yi[-1])]) - 59*ecuacion.subs([(x, xi[2]), (y, yi[2])]) + 37*ecuacion.subs([(x, xi[1]), (y, yi[1])]) - 9*ecuacion.subs([(x, xi[0]), (y, yi[0])]))
        }

    #INICIALIZADOR
    salida = ""
    salida = f"__________________________________________________________\n1-Aplicamos Runge-Kutta y obtenemos:\n"
    d, yi = runge_kutta(ecuacion, valor_y_inicial=valor_y_inicial, valor_x_inicial=valor_x_inicial,orden=paso,h=h)
    yi = yi[:int(paso[0])-1]

    for i in range(len(yi)):
        salida += f"\n\ty{i+1}= {yi[i]}"

    ecuacion,variables = transform_fx(ecuacion)
    salida += f"\n\n2-Obtenemos los valores de X para aplicar la primer predicción\n"
    xi = [valor_x_inicial]
    #Obteniendo valores de x
    for i in range(int(paso[0])-1):
        xi.append(valor_x_inicial + (i+1)*h)
    
    for i in range(len(xi)):
        salida += f"\n\tX{i+1}: {xi[i]}"

    

    #Calculo de la prediccion
    yi.insert(0, valor_y_inicial)
    yi_1 = FORMULAS_ADAMS_BASHFORTH[paso[0]](yi)
    salida += f"\n\n3-Aplicamos Método ADAM-BASHFORTH\n"
    salida += f"\n\tY*{paso[0]} = {yi_1}\t"

    xi_4 = valor_x_inicial + (4*h)
    salida += f"\n\n\tGeneramos el valor de X{paso[0]} = {xi_4}"
    yprima_i1 = ecuacion.subs([(x, xi_4), (y, yi_1)])
    salida += f"\n\tY'{paso[0]} = {yprima_i1}"

    yi.append(yi_1)
    xi.append(xi_4)
    xi.pop(0)
    yi.pop(0)

    #Usamos el corrector

    resultado = adams_moulton(ecuacion, (str(int(paso[0])-1)), xi,yi,h)
    salida += f"\n\n4-Aplicamos corrección de ADAMS-MOULTON\n"
    salida += f"\n\t\tY{paso[0]} = {resultado}\t"

    return salida

def solve_multipasos():

    # MainLayout
    main_layout = [
        [sg.Input(key="-IN|FX-", disabled=True),sg.Button("Ingresar función",key="-BTN|FX-")],
        [sg.Text('Orden: ', key="-TXT|ORDEN-"), sg.Image(radio_unchecked, enable_events=True, k='2', metadata=False), sg.T('Orden 2', k="T2"), sg.Image(radio_unchecked, enable_events=True, k='3', metadata=False), sg.T('Orden 3', k="T3"), sg.Image(radio_unchecked, enable_events=True, k='4', metadata=False), sg.T('Orden 4', k="T4")],
        [sg.pin(sg.Text("Valor inicial de x:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALX-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("Valor inicial de y:", key="-TXT|VALX-", visible=True)), sg.pin(sg.Input(enable_events=True, key="-IN|VALY-", size=(13, 1), visible=True))],
        [sg.pin(sg.Text("¿Ingresará valor para h?", key="-TXT|EVAL-")), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='YES', metadata=False)), sg.pin(sg.Text('Si', k="-YES-")), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='NO', metadata=False)), sg.pin(sg.Text('No', k="-NO-"))],
        [sg.pin(sg.Text("Valor de x a encontrar:", key="-TXT|VALXI-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VALXI-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("h:", key="-TXT|H-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|H-", size=(13, 1), visible=False))],
        [sg.pin(sg.Multiline(disabled=False,visible=False, key="-TXT|RES-", auto_size_text= True, auto_refresh= True, size= (60,15)))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    multipasos_window = sg.Window('', main_layout)

    #Definimos la lista de inputs que solo admitirán  valores numéricos ya sea enteros o flotantes positivos o negativos
    FLOAT_INPUTS = ["-IN|VALX-", "-IN|VALY-", "-IN|VALXI-"]

    radio_keys = ('2', '3', '4')
    radio_keys2 = ('YES', 'NO')

    paso = list()

    def check_radio(key):
            for k in radio_keys2:
                multipasos_window[k].update(radio_unchecked)
                multipasos_window[k].metadata = False
            multipasos_window[key].update(radio_checked)
            multipasos_window[key].metadata = True
            
    #Bucle de eventos
    while True:

        
        event, values = multipasos_window.read()
        
        # Eventos para los radiobuttom
        if event in radio_keys:
            if multipasos_window[event].metadata:
                uncheck(event, multipasos_window, paso)
                
            else:
                check(event, multipasos_window, paso)

        if event in radio_keys2:
            check_radio(event)

        if event == "-BTN|FX-":
            multipasos_window["-IN|FX-"].update(showCalculator())

        # Validando ingreso unicamente de numeros en inputs
        if event in FLOAT_INPUTS and len(values[event]) and values[event][-1] not in ('-0123456789.'):
            multipasos_window[event].update(values[event][:-1])

        else:
            pass


        #Si el usuario dice que si, se le muestra el input para ingresar el valor a evaluar
        if event == "YES":
            hide(["-TXT|VALXI-","-IN|VALXI-"], multipasos_window)
            show(["-TXT|H-","-IN|H-"], multipasos_window)

        #Si el usuario dice que no, se oculta el input para ingresar el valor a evaluar
        elif event == "NO":
            hide(["-TXT|H-","-IN|H-"], multipasos_window)
            show(["-TXT|VALXI-","-IN|VALXI-"], multipasos_window)
            
        if event == "-BTN|SOLVE-":
            paso.sort()
            
            if values["-IN|H-"] != None:
                respuesta = adams_bashforth(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), h=float(values['-IN|H-']), paso=paso)
            else:
                respuesta = adams_bashforth(ecuacion=values['-IN|FX-'], valor_y_inicial=float(values['-IN|VALY-']), valor_x_inicial= float(values['-IN|VALX-']), valor_x_final=float(values['-IN|VALXI-']), paso=paso)
            
            multipasos_window['-TXT|RES-'].update(value=respuesta, visible = True)
        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    
    multipasos_window.close()