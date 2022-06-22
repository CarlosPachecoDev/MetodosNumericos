from UtilitiesGUI import *
from Calculadora import *
    
def lagrange(expresion = None, grado_polinomio = None , intervalo = None ,datos = None, valor_eval= None):

    #Significa que el usuario ingresó una expresión matemática
    if expresion != None:

        #Si el usuario proporciona un intervalo
        if intervalo != None:
            puntos_totales = grado_polinomio + 1
            puntos_restantes = puntos_totales - 2
            
            #Convertimos la cadena de texto en una expresión matemática evaluable
            expresion, variables = transform_fx(expresion)

            if puntos_restantes == 1:
                salto = (int(intervalo[1])-int(intervalo[0]))/2 
            else:
                salto = (int(intervalo[1])-int(intervalo[0]))/puntos_restantes

            xi = list()
            fi = list()
            xi.append(int(intervalo[0]))
            fi.append(expresion.subs(variables[0],xi[0]))

            i = 0
            while len(xi) < puntos_totales:
                xi.append(xi[i]+salto)
                fi.append(expresion.subs(variables[0],xi[i]+salto).evalf())
                i += 1

            polinomio = 0

            for i in range (0,grado_polinomio+1,1):
                numerador = 1
                denominador = 1
                for j in range (0,grado_polinomio+1,1):
                    if (i != j):
                        numerador = numerador*(variables[0]-xi[j])
                        denominador = denominador*(xi[i]-xi[j])
                    termino = (numerador/denominador)*fi[i]

                polinomio = polinomio+termino
            polisimple = sp.expand(polinomio)
            respuesta = f"El polinomio resultante es {polisimple}"

            if valor_eval != None:
                #Obteniendo el resultado de evaluar el polinomio en el valor ingresado por el usuario
                #Õbteniendo el error porcentual
                valor_verdadero = expresion.subs(x,valor_eval).evalf()
                resultado_evaluacion = polisimple.subs(x,valor_eval).evalf()
                respuesta += f"\n Evaluando  el valor de {valor_eval} en el polinomio obtenemos {resultado_evaluacion}"
                error_porcentual = f"\nEl error porcentual es: {math.fabs((valor_verdadero - resultado_evaluacion)/valor_verdadero)*100}"

                #Calculando error teórico
                #Dividimos la formula del error en 2 expresiones

                n = len(xi)-1
                numerador = sp.diff(expresion,x,n+1)

                segunda_expresion= 1
                for i in range(len(xi)):
                    segunda_expresion *= (valor_eval-xi[i])

                error_teorico = f"\nEl error teórico es: {math.fabs(((numerador.subs(variables[0],valor_eval).evalf())/(math.factorial(n+1)))*segunda_expresion)}"


                return respuesta, xi, fi, polisimple, resultado_evaluacion, error_porcentual, error_teorico

            else:
                return respuesta, xi, fi, polisimple

        #Si ha proporcioonado valores de x
        else:
            expresion, variables = transform_fx(expresion)
            print(datos)
            xi = [float(number) for number in datos[0]]
            fi = list()
            n = len(xi)

            for i in range(len(xi)):
                fi.append(expresion.subs(x,xi[i]).evalf())

            polinomio = 0
            for i in range (0,n,1):
                numerador = 1
                denominador = 1
                for j in range (0,n,1):
                    if (i != j):
                        numerador = numerador*(x-xi[j])
                        denominador = denominador*(xi[i]-xi[j])
                    termino = (numerador/denominador)*fi[i]
                polinomio = polinomio+termino
            polisimple = sp.expand(polinomio)
            respuesta = f"El polinomio resultante es {polisimple}"

            if valor_eval != None:
                #Obteniendo el resultado de evaluar el polinomio en el valor ingresado por el usuario
                #Õbteniendo el error porcentual
                valor_verdadero = expresion.subs(x,valor_eval).evalf()
                resultado_evaluacion = polisimple.subs(x,valor_eval).evalf()
                respuesta += f"\n Evaluando  el valor de {valor_eval} en el polinomio obtenemos {resultado_evaluacion}"
                error_porcentual = f"\nEl error porcentual es: {math.fabs((valor_verdadero - resultado_evaluacion)/valor_verdadero)*100}"

                #Calculando error teórico
                #Dividimos la formula del error en 2 expresiones

                n = len(xi)-1
                numerador = sp.diff(expresion,x,n+1)

                segunda_expresion= 1
                for i in range(len(xi)):
                    segunda_expresion *= (valor_eval-xi[i])

                error_teorico = f"\nEl error teórico es: {math.fabs(((numerador.subs(variables[0],valor_eval).evalf())/(math.factorial(n+1)))*segunda_expresion)}"

                return respuesta, xi, fi, polisimple, resultado_evaluacion, error_porcentual, error_teorico
            else:
                return respuesta, xi, fi, polisimple

    #El usuario ingresó una tabla de datos
    else:
        xi = [float(number) for number in datos[0]]
        fi = [float(number) for number in datos[1]]
        n = len(xi)

        polinomio = 0
        for i in range (0,n,1):
            numerador = 1
            denominador = 1
            for j in range (0,n,1):
                if (i != j):
                    
                    numerador = numerador*(x-xi[j])
                    denominador = denominador*(xi[i]-xi[j])
                termino = (numerador/denominador)*fi[i]
            polinomio = polinomio+termino
        polisimple = sp.expand(polinomio)
        respuesta = f"El polinomio resultante es {polisimple}"

        if valor_eval != None:
            resultado_evaluacion = polisimple.subs(x,valor_eval).evalf()
            respuesta += f"\n Evaluandop  el valor de {valor_eval} en el polinomio obtenemos {resultado_evaluacion}"
            return respuesta, xi, fi, polisimple, resultado_evaluacion
        else:
            return respuesta, xi, fi, polisimple
        
        
        


def solve_lagrange():

    main_layout = [
            [sg.Text('Seleccione la opción de datos a ingresar'), sg.Combo(["Función Matemática", "Tabla de datos"], default_value="", enable_events=True, readonly=True, key='-COMBO|DATOS-')], 
            [sg.pin(sg.Text('Función matemática: ', key="-LBL|FUNCION-", visible=False)), sg.pin(sg.Text('', key="-TXT|FUNCION-", visible=False))],
            [sg.pin(sg.Text("Delimitar función por:", key="-TXT|LIMIT-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='INTERVALO', metadata=False, visible=False)), sg.pin(sg.Text('Intervalo', k="-INTERVALO-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='VALORES', metadata=False, visible=False)), sg.pin(sg.Text('Valores', k="-VALORES-", visible=False))],
            [sg.pin(sg.Text("Limite inferior:", key="-TXT|LIMITI-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|LIMITI-", size=(13, 1), visible=False)),sg.pin(sg.Text("Limite superior:", key="-TXT|LIMITS-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|LIMITS-", size=(13, 1), visible=False))],
            [sg.pin(sg.Text("Grado del polinomio:", key="-TXT|GRD-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|GRD-", size=(13, 1), visible=False))],
            [sg.pin(sg.Text("Ingrese la cantidad de puntos:", key="-TXT|VX-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VX-", size=(10, 1), visible= False)), sg.pin(sg.Button('Llenar tabla',key="-BTN|FILL-", visible=False))], 
            [sg.pin(sg.Text("¿Desea evaluar algún punto?", key="-TXT|EVAL-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='YES', metadata=False, visible=False)), sg.pin(sg.Text('Si', k="-YES-", visible=False)), sg.pin(sg.Image(radio_unchecked, enable_events=True, k='NO', metadata=False, visible=False)), sg.pin(sg.Text('No', k="-NO-", visible=False))],
            [sg.pin(sg.Text("Ingrese el valor a evaluar:", key="-TXT|VAL-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VAL-", size=(13, 1), visible=False))],
            [sg.pin(sg.Canvas(key='-CANVAS-',visible=False))],
            [sg.pin(sg.Text("", key="-TXT|RES-", visible=False))],
            [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-", visible=False), sg.Button('Borrar', key="-BTN|CLR-", visible=False)]
        ]

    lagrange_window = sg.Window('', main_layout)
    radio_keys_1 = ('YES', 'NO')
    radio_keys_2 = ("INTERVALO", "VALORES")

    def check_radio(key,buttomgroup):
        for k in buttomgroup:
            lagrange_window[k].update(radio_unchecked)
            lagrange_window[k].metadata = False
        lagrange_window[key].update(radio_checked)
        lagrange_window[key].metadata = True
    
    #Variable booleana para determinar si se han obtenido todos los datos para asi mostrar el botón de resolver
    Buttom_flag = False
    
    #Definimos la lista de inputs que solo admitirán  valores enteros positivos
    INT_INPUTS = ["-IN|VX-", "-IN|GRD-"]
    
    #Definimos la lista de inputs que solo admitirán  valores numéricos ya sea enteros o flotantes positivos o negativos
    REAL_INPUTS = ["-IN|VAL-","-IN|LIMITI-","-IN|LIMITS-"]

    #Variables Booleanas para saber si se ingresó intervalo o valores de x y si quiere evaluar o no el pòlinomio en un punto específico
    intervalo = False
    valores = False

    #Variable que determina si en el canvas hay o no un gráfico
    grafico = False

    #Bucle de eventos
    while True:
        

        event, values = lagrange_window.read()

        if event == "Salir" or event == sg.WIN_CLOSED:
            break   
        else:
        
            if event in radio_keys_1:
                check_radio(event,radio_keys_1)
        
            if event in radio_keys_2:
                check_radio(event,radio_keys_2)

            if event in INT_INPUTS and len(values[event]) and values[event][-1] not in ('1234567890'):
                lagrange_window[event].update(values[event][:-1])

            elif event in REAL_INPUTS and len(values[event]) and values[event][-1] not in ('-1234567890.'):
                lagrange_window[event].update(values[event][:-1])

            else:

                #Si ha ingresado alguna cantidad de puntos se muestra el botón para poder llenar la tabla de datos
                if values["-IN|VX-"] != "":
                    show(["-BTN|FILL-"], lagrange_window)
            
                #Sino no se muestra hasta que haya ingresado algún valor
                else:
                    hide(["-BTN|FILL-"], lagrange_window)
            
                #Si ha ingresado el valor a evaluar se le muestra el botón de resolver
                if values["-IN|VAL-"] != "":
                    Buttom_flag = True
                else:
                    Buttom_flag = False

            if event == "-COMBO|DATOS-":

                #Se muestran los campos necesarios para la opción seleccionada "Función Matemática"
                if values["-COMBO|DATOS-"] == "Función Matemática":
                    Buttom_flag = False
                    reset(["-IN|VAL-","-TXT|RES-"], lagrange_window)
                    hide(["-BTN|FILL-","-TXT|VX-", "-IN|VX-","-TXT|VAL-","-IN|VAL-","-TXT|EVAL-","YES","NO","-YES-","-NO-","-CANVAS-"], lagrange_window)
                    reset_radio(["YES","NO","INTERVALO", "VALORES"], lagrange_window)
                    try:
                        clear_canvas(canvas,lagrange_window,"-CANVAS-")
                    except:
                        pass
                    show(['-LBL|FUNCION-', '-TXT|FUNCION-',"-TXT|LIMIT-","INTERVALO","VALORES","-INTERVALO-","-VALORES-"], lagrange_window)
                    lagrange_window['-TXT|FUNCION-'].update(showCalculator())

                #Se muestran los campos necesarios para la opción seleccionada "Tabla de datos"
                else:
                    Buttom_flag = False
                    reset_radio(["YES","NO","INTERVALO", "VALORES"], lagrange_window)
                    try:
                        clear_canvas(canvas,lagrange_window,"-CANVAS-")
                    except:
                        pass
                    reset(["-IN|VX-", "-IN|GRD-","-IN|VAL-","-IN|LIMITI-","-IN|LIMITS-","-TXT|RES-","-TXT|FUNCION-"], lagrange_window)
                    hide(["-BTN|FILL-","-CANVAS-","-IN|VX-", "-IN|GRD-","-IN|VAL-","-IN|LIMITI-","-IN|LIMITS-","-TXT|RES-","-TXT|FUNCION-","YES","NO","INTERVALO", "VALORES","-LBL|FUNCION-","-TXT|LIMIT-","-INTERVALO-","-VALORES-","-YES-","-NO-","-TXT|LIMITI-","-TXT|LIMITS-","-TXT|GRD-","-TXT|VX-","-TXT|EVAL-", "-TXT|VAL-","-TXT|RES-"], lagrange_window)
                    show(["-TXT|VX-", "-IN|VX-","-BTN|FILL-"], lagrange_window)



            if event == "-BTN|FILL-":
                if valores:
                    datos_usuario = create_table(cols=int(values["-IN|VX-"]), rows= 1)
                else:
                    datos_usuario = create_table(cols=int(values["-IN|VX-"]), rows= 2)
                show(["-TXT|EVAL-","YES","NO","-YES-","-NO-"], lagrange_window)
        

            #Si el usuario dice que si, se le muestra el input para ingresar el valor a evaluar
            if event == "YES":
                show(["-TXT|VAL-","-IN|VAL-"], lagrange_window)
                hide(["-BTN|SOLVE-"], lagrange_window)
                Buttom_flag = False

            #Si el usuario dice que no, se oculta el input para ingresar el valor a evaluar
            elif event == "NO":
                hide(["-TXT|VAL-","-IN|VAL-"], lagrange_window)
                show(["-BTN|SOLVE-"], lagrange_window)
                Buttom_flag = True

        

            if event == "INTERVALO":  
                Buttom_flag = False   
                intervalo = True
                valores = False
                reset(["-IN|VX-","-IN|VAL-","-TXT|RES-"], lagrange_window)
                hide(["-TXT|VX-", "-IN|VX-","-BTN|FILL-","-CANVAS-"], lagrange_window)
                try:
                    clear_canvas(canvas,lagrange_window,"-CANVAS-")
                except:
                    pass
                uncheck("YES",lagrange_window)
                uncheck("NO",lagrange_window)
                show(["-TXT|LIMITI-","-IN|LIMITI-","-TXT|LIMITS-","-IN|LIMITS-","-TXT|GRD-","-IN|GRD-","-TXT|EVAL-","YES","NO","-YES-","-NO-"], lagrange_window)
            

            elif event == "VALORES":
                Buttom_flag = False
                valores = True
                intervalo = False
                reset(["-IN|LIMITI-","-IN|LIMITS-","-IN|GRD-","-IN|VAL-","-TXT|RES-"], lagrange_window)
                hide(["-CANVAS-","-TXT|LIMITI-","-TXT|LIMITS-","-IN|LIMITI-","-IN|LIMITS-","-TXT|GRD-","-IN|GRD-","-TXT|EVAL-","YES","NO","-YES-","-NO-","-TXT|VAL-","-IN|VAL-"], lagrange_window)
                try:
                    clear_canvas(canvas,lagrange_window,"-CANVAS-")
                except:
                    pass
                uncheck("YES",lagrange_window)
                uncheck("NO",lagrange_window)
                show(["-TXT|VX-", "-IN|VX-"], lagrange_window)
            
        

            #Todo está correcto, asi que se muestra el botón de resolver    
            if Buttom_flag:
                show(["-BTN|SOLVE-"], lagrange_window)

            #En caso contrario se oculta
            else:
                hide(["-BTN|SOLVE-"], lagrange_window)


            if event == "-BTN|CLR-":
                reset(["-IN|VX-", "-IN|GRD-","-IN|VAL-","-IN|LIMITI-","-IN|LIMITS-",'-COMBO|DATOS-',"-TXT|RES-","-TXT|FUNCION-"], lagrange_window)
                hide(["-BTN|FILL-","-CANVAS-","-IN|VX-", "-IN|GRD-","-IN|VAL-","-IN|LIMITI-","-IN|LIMITS-","-TXT|RES-","-TXT|FUNCION-","YES","NO","INTERVALO", "VALORES","-LBL|FUNCION-","-TXT|LIMIT-","-INTERVALO-","-VALORES-","-YES-","-NO-","-TXT|LIMITI-","-TXT|LIMITS-","-TXT|GRD-","-TXT|VX-","-TXT|EVAL-", "-TXT|VAL-","-TXT|RES-"], lagrange_window)
                reset_radio(["YES","NO","INTERVALO", "VALORES"], lagrange_window)
                clear_canvas(canvas,lagrange_window,"-CANVAS-")

            if event == "-BTN|SOLVE-":


                show(["-BTN|CLR-"], lagrange_window)

            
                #Si el ingreso es através de tabla de datos
                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    #Si hay un dato para evaluar se pasa a la función lagrange
                    if values["-IN|VAL-"] != "":
                        respuesta, xi, fi, polinomio, result_eval = lagrange(datos=datos_usuario, valor_eval= float(values["-IN|VAL-"]))
                        if grafico:
                            canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-",canvas=canvas)
                        else:
                            canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-")
                        update(["-TXT|RES-"], lagrange_window, [respuesta])

                    #Si no lo hay solo se pasan los datos ingresados por el usuario
                    else:
                        respuesta, xi, fi, polinomio = lagrange(datos=datos_usuario)
                        if grafico:
                            canvas = generate_grafic(xi= xi,fi= fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-", canvas=canvas)
                        else:
                            canvas = generate_grafic(xi= xi,fi= fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-")

                        update(["-TXT|RES-"], lagrange_window, [respuesta])
                        show(["-TXT|RES-"], lagrange_window)

                #Si el ingreso de datos es atraves de una función matemática
                else:

                    #Si el usuario proporcionó un intervalo para acotar la función matemática
                    if intervalo:

                        if values["-IN|VAL-"] != "":
                            respuesta, xi, fi, polinomio, result_eval, error_porcentual, error_teorico = lagrange(expresion=lagrange_window['-TXT|FUNCION-'].get(), valor_eval= float(values["-IN|VAL-"]), intervalo=[values["-IN|LIMITI-"],values["-IN|LIMITS-"]], grado_polinomio=int(values["-IN|GRD-"]))
                            if grafico:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-", canvas= canvas)
                            else:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-")
                            update(["-TXT|RES-"], lagrange_window, [respuesta+error_porcentual+error_teorico])
                    
                        else:
                            respuesta, xi, fi, polisimple = lagrange(expresion=lagrange_window['-TXT|FUNCION-'].get(),  intervalo=[values["-IN|LIMITI-"],values["-IN|LIMITS-"]], grado_polinomio=int(values["-IN|GRD-"]))
                            if grafico:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-", canvas=canvas)
                            else:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-")
                            update(["-TXT|RES-"], lagrange_window, [respuesta])

                    #Si no lo hay solo se pasan los datos ingresados por el usuario
                    else:

                        if values["-IN|VAL-"] != "":
                            respuesta, xi, fi, polisimple, result_eval, error_porcentual, error_teorico = lagrange(expresion=lagrange_window['-TXT|FUNCION-'].get(), valor_eval= float(values["-IN|VAL-"]), datos=datos_usuario)
                            if grafico:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-", canvas= canvas)
                            else:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, valor_eval=float(values["-IN|VAL-"]), result= result_eval, key="-CANVAS-")
                            update(["-TXT|RES-"], lagrange_window, [respuesta+error_porcentual+error_teorico])
                    
                        else:
                            respuesta, xi, fi, polisimple = lagrange(expresion=lagrange_window['-TXT|FUNCION-'].get(), datos=datos_usuario)
                            if grafico:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-", canvas=canvas)
                            else:
                                canvas = generate_grafic(xi=xi,fi=fi, metodo="Polinomio de Lagrange", window= lagrange_window, key="-CANVAS-")
                            update(["-TXT|RES-"], lagrange_window, [respuesta])
                show(["-TXT|RES-","-CANVAS-"], lagrange_window)

                #Como ya se graficó minimo 1 vez entonces si hay un gráfico para borrar
                grafico = True  

            else:
                hide(["-BTN|CLR-"], lagrange_window) 
    lagrange_window.close()

