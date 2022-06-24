
from Calculadora import *
from UtilitiesGUI import *
from Notify import notify


def Integrate():
    
    def trapecio_simple(tipo, expresion= None, limites_inferiores= None, limites_superiores= None, datos = None):

        if expresion != None:
            fx, variables = transform_fx(expresion)
            for i in range(tipo):
                
                expresion = (limites_superiores[i] - limites_inferiores[i])*((fx.subs(variables[i],limites_inferiores[i]).evalf() + fx.subs(variables[i],limites_superiores[i]).evalf())/2)
                fx = sp.sympify(expresion)

            return expresion

        else:
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            a = xi[0]
            b = xi[1]
    
            return (b - a)*((fxi[0] + fxi[1])/2)

    def trapecio_compuesto(tipo, limites_inferiores = None, limites_superiores = None, n = None,expresion = None, datos= None, nivel= None):
        
        xi = []
        fxi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:
            fx, variables = transform_fx(expresion)
            for i in range(tipo):
                #Se obtiene el valor de h
                h = (limites_superiores[i]-limites_inferiores[i])/n
                #Se asigna el primer valor de x
                xi.append(limites_inferiores[i])

                #Se generan todos los demás valores de x
                for j in range(n-1):
                    xi.append(xi[j] + h)
                xi.append(limites_superiores[i])

                #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
                for j in xi:
                    fxi.append(fx.subs(variables[i],j).evalf())


                #Si se llama al método del trapecio desde Rosemberg
                if nivel != None:
                    expresion = (limites_superiores[i] - limites_inferiores[i])*((fxi[0] + 2*sum(fxi[1:n]) + fxi[n])/(2**(nivel)))
                    
                
                else: 
                    expresion = (limites_superiores[i] - limites_inferiores[i])*((fxi[0] + 2*sum(fxi[1:n]) + fxi[n])/(2*n))
                    
                fx = sp.sympify(expresion)
                xi.clear()
                fxi.clear()
            print(expresion)
            return expresion


        #Si se ha pasado una serie de datos se procede a resolver
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]

            b = xi[-1]
            a = xi[0]
            n = len(xi) - 1

            #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
            return (b - a)*((fxi[0] + 2*sum(fxi[1:n]) + fxi[n])/(2*n))

    def simpson_1_tercio_simple(tipo, expresion= None, limites_inferiores= None, limites_superiores= None, datos = None):
        
        if expresion != None:
            fx, variables = transform_fx(expresion)
            for i in range(tipo):
                Xm = (limites_inferiores[i] + limites_superiores[i])/2
                expresion =  (limites_superiores[i] - limites_inferiores[i])*((fx.subs(variables[i],limites_inferiores[i]).evalf() + 4*fx.subs(variables[i],Xm).evalf() +fx.subs(variables[i],limites_superiores[i]).evalf())/6)
                fx = sp.sympify(expresion)
            return expresion
        else:
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
    
            return (xi[0] - xi[-1])*((fxi[0] + 4*fxi[1] + fxi[2])/6)

    def simpson_1_tercio_compuesto(tipo, limites_inferiores = None, limites_superiores = None, n = None,expresion = None, datos= None):

        xi = []
        fxi = []
        Xmi = []
        fxmi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:
            fx, variables = transform_fx(expresion)
            
            for i in range(tipo):
                
                #se genera el valor de h para generar los intervalos
                h = (limites_superiores-limites_inferiores)/n
                #se añade el primer valor de x
                xi.append(limites_inferiores)

                #Se generan todos los ddemás valores de x
                for j in range(n-1):
                    xi.append(xi[j] + h)
                xi.append(limites_superiores)

                #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
                for j in xi:
                    fxi.append(fx.subs(variables[i],j).evalf())
            
                #Generando los puntos medios de cada intervalos 
                for j in range(len(xi)-1):
                    Xmi.append((xi[j] + xi[j+1])/2)

                #Se evaluan todos los puntos medios en la función
                for j in Xmi:
                    fxmi.append(fx.subs(variables[i],j).evalf())

                expresion = (limites_superiores - limites_inferiores)*((fxi[0] + 4*sum(fxmi) + 2*sum(fxi[1:n]) + fxi[n])/(6*n))
            
                fx = sp.sympify(expresion)
            

            return expresion
        #Si se ha pasado una serie de datos se procede a resolver
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            
            #Generando los puntos medios de cada intervalos 
            for i in range(len(xi)-1):
                Xmi.append((xi[i] + xi[i+1])/2)

            #Se evaluan todos los puntos medios en la función
            for i in Xmi:
                fxmi.append(fx.subs(variables[0],i).evalf())

            #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
            return (xi[-1] - xi[0])*((fxi[0] + 4*sum(fxmi) + 2*sum(fxi[1:n]) + fxi[n])/(6*n))

    def simpson_3_8_simple(tipo, limites_inferiores = None, limites_superiores = None,expresion = None, datos= None):

        xi = []
        fxi = []

        if expresion != None:
            
            #Se convierte la expresión para poder evaluar valores en ella
            fx, variables = transform_fx(expresion)
            
            for i in range(tipo):
                h = (limites_superiores[i] - limites_inferiores[i])/3
                xi.append(limites_inferiores[i])

                #Se generan todos los valores de x
                for j in range(2):
                    xi.append(xi[j] + h)
                xi.append(limites_superiores[i])

                 #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
                for j in xi:
                    fxi.append(fx.subs(variables[i],j).evalf())

                expresion = (limites_superiores[i] - limites_inferiores[i])*((fxi[0] + 3*fxi[1] + 3*fxi[2] + fxi[3])/8)
                
                fx = sp.sympify(expresion)
            return expresion
        
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]

            #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
            return (xi[-1] - xi[0])*((fxi[0] + 3*fxi[1] + 3*fxi[2] + fxi[3])/8)

    def simpson_3_8_compuesto(tipo, limites_inferiores = None, limites_superiores = None, n = None,expresion = None, datos= None, paso = None):

        xi = []
        fxi = []
        Xsi = []
        fxsi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:

            fx, variables = transform_fx(expresion)
            
            for i in range(tipo):
                #se genera el valor de h para generar los intervalos
                h = (limites_superiores[i]-limites_inferiores[i])/n
                #se añade el primer valor de x
                xi.append(limites_inferiores[i])

                #Se generan todos los demás valores de x
                for j in range(n-1):
                    xi.append(xi[j] + h)
                xi.append(limites_superiores[i])

                #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
                for j in xi:
                    fxi.append(fx.subs(variables[i],j).evalf())
            
                #Generando subintervalos intervalos 
                for j in range(len(xi)-1):
                    for t in range(2):
                        Xsi.append(xi[j] + (h/3)*(t+1))

                #Se evaluan todos los puntos de los subintervalos en la función
                for j in Xsi:
                    fxsi.append(fx.subs(variables[i],j).evalf())

                expresion = (limites_superiores[i] - limites_inferiores[i])*((fxi[0] + 3*sum(fxsi) + 2*sum(fxi[1:n]) + fxi[n])/(8*n))
                
                fx = sp.sympify(expresion)

            return expresion

            #print(f"h: {h}\nValores de x: {xi}\nValores de Fxi: {fxi}\nSubintervalos: {Xsi}\nFuncion evaluada en subintervalos: {fxsi}")
        
        #Si se ha pasado una serie de datos se procede a resolver
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            h = paso

            #Generando subintervalos intervalos 
            for i in range(len(xi)-1):
                for j in range(2):
                    Xsi.append(xi[i] + (h/3)*(j+1))

            #Se evaluan todos los puntos de los subintervalos en la función
            for i in Xsi:
                fxsi.append(fx.subs(variables[0],i).evalf())

            #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
            return (xi[-1] - xi[0])*((fxi[0] + 3*sum(fxsi) + 2*sum(fxi[1:n]) + fxi[n])/(8*n))

    
    def rosemberg(expresion, limites_inferiores, limites_superiores, nivel):

        j = 1
        matriz = []

        for i in range(nivel):
            matriz.append([])

        # nivel 1
        for i in range(nivel):
            if i == 0:
                respuesta = trapecio_simple(tipo= 1, expresion= expresion, limites_inferiores= limites_inferiores, limites_superiores= limites_superiores)
            else:
                respuesta = trapecio_compuesto(tipo= 1,limites_inferiores= limites_inferiores, limites_superiores= limites_superiores, n= j, nivel= (i+1), expresion= expresion)
            
            j *= 2
            matriz[0].append(round(float(respuesta), 9))
        
        #Nivel >= 2
        for i in range(nivel - 1):
            k = i + 1
            for j in range(nivel - (i+1)):
                I_k = (4**k * matriz[i][j+1] - matriz[i][j])/(4**k - 1)
                matriz[i+1].append(round(I_k, 9))

        for i in matriz:
            if len(i) < nivel:
                for j in range(nivel - len(i)):
                    i.append(0)


        return matriz[nivel - 1][0], matriz

    def cuadratura_gaussiana(puntos, expresion, limite_inferior , limite_superior):
        Wk = {
            1: {
                1: 2.0
            },
            2: {
                1: 1.0,
                2: 1.0
            },  
            3: {
                1: 0.555556,
                2: 0.888889,
                3: 0.555556
            },
            4: {
                1: 0.347855,
                2: 0.652145,
                3: 0.652145,
                4: 0.347855
            },
            5: {
                1: 0.236926885,
                2: 0.478628671,  
                3: 0.56888888,
                4: 0.478628671,
                5: 0.236926885
            },
            6: {
                1: 0.171324,
                2: 0.360762,  
                3: 0.467914,
                4: 0.467914,
                5: 0.360762,
                6: 0.171324
            }

        }

        Tk = {
            1: {
                1: 0.0
            },
            2: {
                1: -0.57735,
                2: 0.57735
            },  
            3: {
                1: -0.774597,
                2: 0.0,
                3: 0.774597
            },
            4: {
                1: -0.861136,
                2: -0.339981,
                3: 0.339981,
                4: 0.861136
            },
            5: {
                1: -0.906179846,
                2: -0.538469310,  
                3: 0.0,
                4: 0.538469310,
                5: 0.906179846
            }
            ,
            6: {
                1: -0.932469,
                2: -0.661209,  
                3: -0.238619,
                4: 0.238619,
                5: 0.906179846,
                6: 0.932469
            }
        }

        
        fx, variables = transform_fx(expresion)

        resultado1 = (limite_superior[0] - limite_inferior[0])/2
        resultado2 = 0

        for i in range(puntos):
            resultado2 += Wk[puntos][i+1] * (fx.subs(variables[0],((((limite_superior[0] - limite_inferior[0])*Tk[puntos][i+1]) + (limite_superior[0] + limite_inferior[0]))/2)).evalf())
            
        return resultado1*resultado2

    def boole(expresion, limite_inferior , limite_superior):
        fx, variables = transform_fx(expresion)
        h = (limite_superior[0] - limite_inferior[0])/4
        print(h)
        print(f"(2*{h})/45  * (7*f({limite_inferior[0]}) + 32*f({limite_inferior[0] + h}) + 12*f({limite_inferior[0] + 2*h}) + 32*f({limite_inferior[0] + 3*h}) + 7*f({limite_inferior[0] + 4*h}))")
        print(f"({(2*h)/45})  * ({7*fx.subs(variables[0],limite_inferior[0]).evalf()} + {32*fx.subs(variables[0],limite_inferior[0]+h)} + {12*fx.subs(variables[0],limite_inferior[0]+2*h)} + {32*fx.subs(variables[0], limite_inferior[0] + 3*h)} + {7*fx.subs(variables[0], limite_inferior[0]+ 3*h)})")
        return ((2*h)/45) * (7*fx.subs(variables[0],limite_inferior[0]).evalf() + 32*fx.subs(variables[0],limite_inferior[0]+h) + 12*fx.subs(variables[0],limite_inferior[0]+2*h) + 32*fx.subs(variables[0], limite_inferior[0] + 3*h) + 7*fx.subs(variables[0], limite_inferior[0]+ 3*h))

    # MainLayout
    main_layout = [
        [sg.Image(radio_unchecked, enable_events=True, k='1', metadata=False), sg.T('Integral Simple', k="-INT|SP-"), sg.Image(radio_unchecked, enable_events=True, k='2', metadata=False), sg.T('Integral Doble', k="-INT|DB-"), sg.Image(radio_unchecked, enable_events=True, k='3', metadata=False), sg.T('Integral Triple', k="-INT|TP-")],
        [sg.Text('Seleccione la opción de datos a ingresar'), sg.Combo(["Función Matemática", "Tabla de datos"], default_value="", enable_events=True, readonly=True, key='-COMBO|DATOS-')], 
        [sg.pin(sg.Text('Función matemática: ', key="-LBL|FUNCION-", visible=False)), sg.pin(sg.Text('', key="-TXT|FUNCION-", visible=False))],
        [sg.pin(sg.Text("Limite inferior:", key="-TXT|A-", visible= False)), sg.pin(sg.Input(enable_events=True, key="-IN|A-", size=(13, 1), visible= False)),sg.pin(sg.Text("Limite superior:", key="-TXT|B-", visible= False)),sg.pin(sg.Input(enable_events=True, key="-IN|B-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Limite inferior 1:", key="-TXT|A1-", visible= False)), sg.pin(sg.Input(enable_events=True, key="-IN|A1-", size=(13, 1), visible= False)),sg.pin(sg.Text("Limite superior 1:", key="-TXT|B1-", visible= False)),sg.pin(sg.Input(enable_events=True, key="-IN|B1-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Limite inferior 2:", key="-TXT|A2-", visible= False)), sg.pin(sg.Input(enable_events=True, key="-IN|A2-", size=(13, 1), visible= False)),sg.pin(sg.Text("Limite superior 2:", key="-TXT|B2-", visible= False)),sg.pin(sg.Input(enable_events=True, key="-IN|B2-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Limite inferior 3:", key="-TXT|A3-", visible= False)), sg.pin(sg.Input(enable_events=True, key="-IN|A3-", size=(13, 1), visible= False)),sg.pin(sg.Text("Limite superior 3:", key="-TXT|B3-", visible= False)),sg.pin(sg.Input(enable_events=True, key="-IN|B3-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Método de integración', key="-TXT|MTD-")), sg.pin(sg.Combo(['Trapecio Simple', 'Trapecio Compuesto','Simpson 1/3 Simple', 'Simpson 1/3 Compuesto', 'Simpson 3/8 Simple', 'Simpson 3/8 Compuesto', "Rosemberg", "Cuadratura Guassiana", "Boole"], default_value="", enable_events=True, readonly=True, key='-COMBO|MTD-'))],
        [sg.pin(sg.Text('Cantidad de puntos: ', key="-LBL|CANT-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|CANT-", size=(13, 1), visible=False)),sg.pin(sg.Button('Llenar Tabla', key="-BTN|TABLE-", visible=False))],
        [sg.pin(sg.Text("Nivel:", key="-TXT|LVL-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|LVL-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Puntos:", key="-TXT|PT-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|PT-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Numero de intervalos:", key="-TXT|ITV-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|ITV-", size=(13, 1), visible=False))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    window = sg.Window('', main_layout)
    inputs = ["-IN|LVL-", "-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-", "-IN|Y2-",
              "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-IN|PASO-", "-IN|VALIN-", "-IN|VV1-", "-IN|VV2-", "-IN|VV3-", "-IN|VV4-"]
    radio_keys = ('1', '2', '3')

    def check_radio(key):
        for k in radio_keys:
            window[k].update(radio_unchecked)
            window[k].metadata = False
        window[key].update(radio_checked)
        window[key].metadata = True

    #Bucle de eventos
    while True:

        event, values = window.read()
        print(f"Event: {event}")
        
        if event in radio_keys:
            check_radio(event)
            tipo = int(event)


        #Se ha seleccionado una forma de ingrerso de datos
        if event == "-COMBO|DATOS-":

            #Si se selecciona la opción "Función Matemática" mostramos la función ingresada por el usuario
            if values["-COMBO|DATOS-"] == "Función Matemática":
                #Ocultamos las opciones requeridas para el ingreso de datos mediante tablas
                hide(["-LBL|CANT-", "-IN|CANT-","-BTN|TABLE-"], window)
                window['-TXT|FUNCION-'].update(showCalculator())
                show(["-TXT|FUNCION-"], window)
                show(["-LBL|FUNCION-"], window)
                
                #Mostrando los campos de limites dependiendo el tipo de integral que el usuario haya ingresado
                reset(["-IN|A-","-IN|B-","-IN|A1-","-IN|B1-","-IN|A2-","-IN|B2-","-IN|A3-","-IN|B3-"], window)
                if tipo == None:
                    pass
                elif tipo == 1:
                    show(["-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)
                elif tipo == 2:
                    hide(["-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)
                    show(["-TXT|A1-","-IN|A1-","-TXT|B1-","-IN|B1-", "-TXT|A2-","-IN|A2-","-TXT|B2-","-IN|B2-"], window)
                elif tipo == 3:
                    hide(["-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)
                    show(["-TXT|A1-","-IN|A1-","-TXT|B1-","-IN|B1-", "-TXT|A2-","-IN|A2-","-TXT|B2-","-IN|B2-", "-TXT|A3-","-IN|A3-","-TXT|B3-","-IN|B3-"], window)
            

            #En caso contrario no se muestra
            else:
                hide(["-LBL|FUNCION-", "-TXT|FUNCION-","-TXT|A-","-IN|A-","-TXT|B-","-IN|B-","-TXT|A1-","-IN|A1-","-TXT|B1-","-IN|B1-", "-TXT|A2-","-IN|A2-","-TXT|B2-","-IN|B2-", "-TXT|A3-","-IN|A3-","-TXT|B3-","-IN|B3-"], window)
                
                #Mostramos las opciones requeridas para el ingreso de datos mediante tablas
                show(["-LBL|CANT-", "-IN|CANT-","-BTN|TABLE-"], window)


        #Se ha seleccionado un método 
        if event == '-COMBO|MTD-':

            #Si el usuario ha seleccionado la opción "Tabla de datos"
            if values["-COMBO|DATOS-"] == "Tabla de datos":
                hide(["-TXT|A-","-IN|A-","-TXT|B-","-IN|B-","-TXT|A1-","-IN|A1-","-TXT|B1-","-IN|B1-", "-TXT|A2-","-IN|A2-","-TXT|B2-","-IN|B2-", "-TXT|A3-","-IN|A3-","-TXT|B3-","-IN|B3-"], window)
                #Ocultamos las opciones requeridas para el ingreso de datos mediante función matemática
                hide(["-TXT|ITV-", "-IN|ITV-","-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)
                #Mostramos las opciones requeridas para el ingreso de datos mediante tablas
                show(["-LBL|CANT-", "-IN|CANT-","-BTN|TABLE-"], window)


            #Si el usuario ha seleccionado la opción "Función Matemática"     
            else:

                #Se oculta la opción de añadir intervalo si se ha seleccionado algún método simple
                if values['-COMBO|MTD-'] in ['Trapecio Simple','Simpson 1/3 Simple','Simpson 3/8 Simple']:
                    hide(["-TXT|ITV-", "-IN|ITV-"], window)

                #Si el método es compuesto se muestra la opción de intervalo junto a las demás opciones requeridas
                else:
                    show(["-TXT|ITV-", "-IN|ITV-"], window)

                if values['-COMBO|MTD-'] == "Rosemberg":
                    hide(["-TXT|ITV-", "-IN|ITV-"], window)
                    show(["-TXT|LVL-", "-IN|LVL-"], window)

                else:
                    hide(["-TXT|LVL-", "-IN|LVL-"], window)

                if values['-COMBO|MTD-'] == "Cuadratura Guassiana":
                    hide(["-TXT|ITV-", "-IN|ITV-"], window)
                    show(["-TXT|PT-", "-IN|PT-"], window)

                else:
                    hide(["-TXT|PT-", "-IN|PT-"], window)

                if values['-COMBO|MTD-'] == "Boole":
                    hide(["-TXT|ITV-", "-IN|ITV-"], window)


                


                


        #Se presiona el botón crear tabla
        if event == "-BTN|TABLE-":
            
            #Si se van a ingresar solo 2 puntos y se ha seleccionado otro método que no sea "Trapecio Simple" se le notifica al usuario que debe seleccionar "Trapecio Simple"
            if int(values['-IN|CANT-']) == 2 and values['-COMBO|MTD-'] != 'Trapecio Simple':
                notify(f"No se puede realizar el método de {values['-COMBO|MTD-']} con {int(values['-IN|CANT-'])} puntos \nSe recomienda usar el método Trapecio Simple")

            #Si se van a ingresar solo 3 puntos y se ha seleccionado otro método que no sea "Trapecio Simple" se le notifica al usuario que debe seleccionar "Trapecio Simple"
            elif int(values['-IN|CANT-']) == 3 and values['-COMBO|MTD-'] != 'Simpson 1/3 Simple':
                notify(f"No se puede realizar el método de {values['-COMBO|MTD-']} con {int(values['-IN|CANT-'])} puntos \nSe recomienda usar el método Simpson 1/3 Simple")

            else:
                
                #Se verifica que los datos sean correctos y de no serlo se le notifica al usuario
                while True:

                    datos = create_table(cols= int(values['-IN|CANT-']), rows= 2)
                    h  = []
                    xi = [float(num) for num in datos[0]]

                    for i in range(len(xi)-1):
                        #se añade un nuevo valor de h
                        h.append(round(xi[i+1] - xi[i], 3))
            
                    flag = True
                    #se comprueba que todos los valores de h encontrados sean iguales
                    for i in range(len(h)-1):
                        if h[i] != h[i+1]:
                            #Hay un valor de h distinto a los anteriores por lo tanto salimos de la comprobación
                            flag = False
                            break

                    #Se notifica que los datos no son correctos
                    if flag == False:
                        notify("Los valores de X deben tener la misma distancia h entre ellos")
                    #Los datos son correctos, se procede a resolver la integral
                    else:
                        break

        #Se presiona el botón resolver
        if event == "-BTN|SOLVE-":
            salida = ""

            #Obteniendo los intervalos ingresados
            limites_inferiores = list()
            limites_superiores = list()
            
            if values['-COMBO|DATOS-'] == 'Función Matemática':

                if tipo == 1:
                    limites_inferiores.append(float(values["-IN|A-"]))
                    limites_superiores.append(float(values["-IN|B-"]))

                else:

                    for i in range(tipo):    
                        limites_inferiores.append(float(values[f"-IN|A{i+1}-"]))
                        limites_superiores.append(float(values[f"-IN|B{i+1}-"]))


            if values['-COMBO|MTD-'] == 'Trapecio Compuesto':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida = f"Aplicando el método de Trapecio Compuesto se obtine como resultado {trapecio_compuesto(expresion=window['-TXT|FUNCION-'].get(), limites_inferiores=limites_inferiores, limites_superiores= limites_superiores, n=int(values['-IN|ITV-']), tipo= tipo)}"
                else:
                    salida = f"Aplicando el método de Trapecio Compuesto se obtine como resultado {trapecio_compuesto(datos= datos, tipo=1)}"

            elif values['-COMBO|MTD-'] == 'Trapecio Simple':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    resultado = trapecio_simple(expresion=window['-TXT|FUNCION-'].get(), limites_inferiores= limites_inferiores, limites_superiores= limites_superiores, tipo=tipo)
                    if resultado != None:
                        salida += f"Aplicando el método de Trapecio Simple se obtine como resultado {resultado}"

                else:
                    salida += f"Aplicando el método de Trapecio Simple se obtine como resultado {trapecio_simple(datos= datos, tipo=1)}"

            elif values['-COMBO|MTD-'] == 'Simpson 1/3 Simple':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 1/3 Simple se obtine como resultado {simpson_1_tercio_simple(tipo, expresion=window['-TXT|FUNCION-'].get(), limites_inferiores= limites_inferiores, limites_superiores= limites_superiores)}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Simple se obtine como resultado {simpson_1_tercio_simple(datos= datos, tipo=1)}"

            elif values['-COMBO|MTD-'] == 'Simpson 1/3 Compuesto':
                
                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_1_tercio_compuesto(tipo= tipo,expresion=window['-TXT|FUNCION-'].get(), limites_inferiores=float(values['-IN|A-']), limites_superiores=float(values['-IN|B-']), n=int(values['-IN|ITV-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_1_tercio_compuesto(datos= datos, tipo=1)}"

            elif values['-COMBO|MTD-'] == 'Simpson 3/8 Simple':
                
                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 3/8 Compuesto se obtine como resultado {simpson_3_8_simple(tipo= tipo, expresion=window['-TXT|FUNCION-'].get(), limites_inferiores= limites_inferiores, limites_superiores= limites_superiores)}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_3_8_simple(datos= datos, tipo=1)}"

            elif values['-COMBO|MTD-'] == 'Simpson 3/8 Compuesto':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 3/8 Compuesto se obtine como resultado {simpson_3_8_compuesto(tipo= tipo, expresion=window['-TXT|FUNCION-'].get(), limites_inferiores= limites_inferiores, limites_superiores= limites_superiores, n=int(values['-IN|ITV-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 3/8 Compuesto se obtine como resultado {simpson_3_8_compuesto(datos= datos, tipo=1)}"
            
            elif values['-COMBO|MTD-'] == 'Rosemberg':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    respuesta, matriz = rosemberg(expresion=window['-TXT|FUNCION-'].get(), limites_inferiores= limites_inferiores, limites_superiores= limites_superiores, nivel= int(values['-IN|LVL-']))
                    salida += f"Aplicando el método de Rosemberg se obtine como resultado {respuesta}"
                
            elif values['-COMBO|MTD-'] == "Cuadratura Guassiana":

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    respuesta= cuadratura_gaussiana(expresion=window['-TXT|FUNCION-'].get(), limite_inferior= limites_inferiores, limite_superior= limites_superiores, puntos= int(values['-IN|PT-']))
                    salida += f"Aplicando el método de Cuadratura Guassiana se obtine como resultado {respuesta}"

            elif values['-COMBO|MTD-'] == "Boole":

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    respuesta= boole(expresion=window['-TXT|FUNCION-'].get(), limite_inferior= limites_inferiores, limite_superior= limites_superiores)
                    salida += f"Aplicando el método de Boole se obtine como resultado {respuesta}"

            if len(salida) != 0:
                sg.popup(salida, no_titlebar=True)


        if event == "Salir" or event == sg.WIN_CLOSED:
            break

    window.close()



