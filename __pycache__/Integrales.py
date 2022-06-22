import PySimpleGUI as sg
from Calculadora import showCalculator, transform_fx
from UtilitiesGUI import *
from Notify import notify


def Integrate():
    
    sg.theme('DarkBlue3')
    
    def create_table(cols, rows):
        sg.theme('DarkBlue3')
        layout = [[sg.T(r, size=(4, 1)), ] + [sg.Input(justification='r', key=(r, c)) for c in range(cols)] for r in range(rows)] + \
         [[sg.Button('Ok')]]

        
        window = sg.Window("", layout, default_element_size=(12, 1), element_padding=(1, 1), return_keyboard_events=True)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Salir'):
                break
            
            if event == "Ok":
                break

        window.close()
        return [[values[(row, col)] for col in range(cols)] for row in range(rows)]

    def trapecio_simple(expresion= None, a= None, b= None, datos = None):

        if expresion != None:
            fx = transform_fx(expresion)
            return (b - a)*((fx(a) + fx(b))/2)

        else:
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            a = xi[0]
            b = xi[1]
    
            return (b - a)*((fxi[0] + fxi[1])/2)

    def trapecio_compuesto(a = None, b = None, n = None,expresion = None, datos= None):
        
        xi = []
        fxi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:

            #Se convierte la expresión para poder evaluar valores en ella
            fx = transform_fx(expresion)
            #Se obtiene el valor de h
            h = (b-a)/n
            #Se asigna el primer valor de x
            xi.append(a)

            #Se generan todos los demás valores de x
            for i in range(n-1):
                xi.append(xi[i] + h)
            xi.append(b)

            #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
            for i in xi:
                fxi.append(fx(i))

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

    def simpson_1_tercio_simple(expresion= None, a= None, b= None, datos = None):
        
        if expresion != None:
            fx = transform_fx(expresion)
            Xm = (a + b)/2

            return (b - a)*((fx(a) + 4*fx(Xm) +fx(b))/6)

        else:
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            a = xi[0]
            b = xi[-1]
    
            return (b - a)*((fxi[0] + 4*fxi[1] + fxi[2])/6)

    def simpson_1_tercio_compuesto(a = None, b = None, n = None,expresion = None, datos= None):

        xi = []
        fxi = []
        Xmi = []
        fxmi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:

            #Se convierte la expresión para poder evaluar valores en ella
            fx = transform_fx(expresion)
            #se genera el valor de h para generar los intervalos
            h = (b-a)/n
            #se añade el primer valor de x
            xi.append(a)

            #Se generan todos los ddemás valores de x
            for i in range(n-1):
                xi.append(xi[i] + h)
            xi.append(b)

            #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
            for i in xi:
                fxi.append(fx(i))
            
            #Generando los puntos medios de cada intervalos 
            for i in range(len(xi)-1):
                Xmi.append((xi[i] + xi[i+1])/2)

            #Se evaluan todos los puntos medios en la función
            for i in Xmi:
                fxmi.append(fx(i))

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
                fxmi.append(fx(i))

        #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
        return (b - a)*((fxi[0] + 4*sum(fxmi) + 2*sum(fxi[1:n]) + fxi[n])/(6*n))

    def simpson_3_8_simple(a = None, b = None,expresion = None, datos= None):

        xi = []
        fxi = []

        if expresion != None:

            #Se convierte la expresión para poder evaluar valores en ella
            fx = transform_fx(expresion)
            h = (b-a)/3
            xi.append(a)

            #Se generan todos los valores de x
            for i in range(2):
                xi.append(xi[i] + h)
            xi.append(b)

            #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
            for i in xi:
                fxi.append(fx(i))
        
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]

        #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
        return (b - a)*((fxi[0] + 3*fxi[1] + 3*fxi[2] + fxi[3])/8)

    def simpson_3_8_compuesto(a = None, b = None, n = None,expresion = None, datos= None, paso = None):

        xi = []
        fxi = []
        Xsi = []
        fxsi = []

        #Comprobamos si se ha pasado alguna expresion para resolver
        if expresion != None:

            #Se convierte la expresión para poder evaluar valores en ella
            fx = transform_fx(expresion)
            #se genera el valor de h para generar los intervalos
            h = (b-a)/n
            #se añade el primer valor de x
            xi.append(a)

            #Se generan todos los demás valores de x
            for i in range(n-1):
                xi.append(xi[i] + h)
            xi.append(b)

            #Se evaluan todos los valores de x en la expresión transformada y se almacenan los valores en una lista
            for i in xi:
                fxi.append(fx(i))
            
            #Generando subintervalos intervalos 
            for i in range(len(xi)-1):
                for j in range(2):
                    Xsi.append(xi[i] + (h/3)*(j+1))

            #Se evaluan todos los puntos de los subintervalos en la función
            for i in Xsi:
                fxsi.append(fx(i))

            #print(f"h: {h}\nValores de x: {xi}\nValores de Fxi: {fxi}\nSubintervalos: {Xsi}\nFuncion evaluada en subintervalos: {fxsi}")
        #Si se ha pasado una serie de datos se procede a resolver
        else:

            #Se convierten a numero los datos de las filas correspondientes para xi y fxi 
            xi = [float(num) for num in datos[0]]
            fxi = [float(num) for num in datos[1]]
            h = paso

            #Generando subintervalos intervalos 
            for i in range(len(xi)-1):
                for i in range(2):
                    Xsi.append(xi[i] + (h/3))

            #Se evaluan todos los puntos de los subintervalos en la función
            for i in Xsi:
                fxsi.append(fx(i))

        #Se sustituyen todos los valores en la fórmula y se retorna el valor encontrado
        return (b - a)*((fxi[0] + 3*sum(fxsi) + 2*sum(fxi[1:n]) + fxi[n])/(8*n))

    

    # MainLayout
    main_layout = [
        
        [sg.Text('Seleccione la opción de datos a ingresar'), sg.Combo(["Función Matemática", "Tabla de datos"], default_value="", enable_events=True, readonly=True, key='-COMBO|DATOS-')], 
        [sg.pin(sg.Text('Función matemática: ', key="-LBL|FUNCION-", visible=False)), sg.pin(sg.Text('', key="-TXT|FUNCION-", visible=False))],
        [sg.pin(sg.Text('Método de integración', key="-TXT|MTD-")), sg.pin(sg.Combo(['Trapecio Simple', 'Trapecio Compuesto','Simpson 1/3 Simple', 'Simpson 1/3 Compuesto', 'Simpson 3/8 Simple', 'Simpson 3/8 Compuesto'], default_value="", enable_events=True, readonly=True, key='-COMBO|MTD-'))],
        [sg.pin(sg.Text("Numero de intervalos:", key="-TXT|ITV-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|ITV-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text("Limite inferior:", key="-TXT|A-", visible= False)), sg.pin(sg.Input(enable_events=True, key="-IN|A-", size=(13, 1), visible= False))],
        [sg.pin(sg.Text("Limite superior:", key="-TXT|B-", visible= False)),sg.pin(sg.Input(enable_events=True, key="-IN|B-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Cantidad de puntos: ', key="-LBL|CANT-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|CANT-", size=(13, 1), visible=False)),sg.pin(sg.Button('Llenar Tabla', key="-BTN|TABLE-", visible=False))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    window = sg.Window('', main_layout)
    inputs = ["-IN|LVL-", "-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-", "-IN|Y2-",
              "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-IN|PASO-", "-IN|VALIN-", "-IN|VV1-", "-IN|VV2-", "-IN|VV3-", "-IN|VV4-"]

    #Bucle de eventos
    while True:

        event, values = window.read()
        print(f"Event: {event}")

        #Se ha seleccionado una forma de ingrerso de datos
        if event == "-COMBO|DATOS-":

            #Si se selecciona la opción "Función Matemática" mostramos la función ingresada por el usuario
            if values["-COMBO|DATOS-"] == "Función Matemática":
                window['-TXT|FUNCION-'].update(showCalculator())
                show(["-LBL|FUNCION-", "-TXT|FUNCION-"], window)

            #En caso contrario no se muestra
            else:
                hide(["-LBL|FUNCION-", "-TXT|FUNCION-"], window)


        #Se ha seleccionado un método 
        if event == '-COMBO|MTD-':

            #Si el usuario ha seleccionado la opción "Tabla de datos"
            if values["-COMBO|DATOS-"] == "Tabla de datos":
                #Ocultamos las opciones requeridas para el ingreso de datos mediante función matemática
                hide(["-TXT|ITV-", "-IN|ITV-","-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)
                #Mostramos las opciones requeridas para el ingreso de datos mediante tablas
                show(["-LBL|CANT-", "-IN|CANT-","-BTN|TABLE-"], window)


            #Si el usuario ha seleccionado la opción "Función Matemática"     
            else:
                #Ocultamos las opciones requeridas para el ingreso de datos mediante tablas
                hide(["-LBL|CANT-", "-IN|CANT-","-BTN|TABLE-"], window)

                #Se oculta la opción de añadir intervalo si se ha seleccionado algún método simple
                if values['-COMBO|MTD-'] in ['Trapecio Simple','Simpson 1/3 Simple','Simpson 3/8 Simple']:
                    hide(["-TXT|ITV-", "-IN|ITV-"], window)
                    show(["-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)

                #Si el método es compuesto se muestra la opción de intervalo junto a las demás opciones requeridas
                else:
                    show(["-TXT|ITV-", "-IN|ITV-","-TXT|A-","-IN|A-","-TXT|B-","-IN|B-"], window)


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


            if values['-COMBO|MTD-'] == 'Trapecio Compuesto':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida = f"Aplicando el método de Trapecio Compuesto se obtine como resultado {trapecio_compuesto(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']), n=int(values['-IN|ITV-']))}"
                else:
                    salida = f"Aplicando el método de Trapecio Compuesto se obtine como resultado {trapecio_compuesto(datos= datos)}"

            elif values['-COMBO|MTD-'] == 'Trapecio Simple':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Trapecio Simple se obtine como resultado {trapecio_simple(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']))}"

                else:
                    salida += f"Aplicando el método de Trapecio Simple se obtine como resultado {trapecio_simple(datos= datos)}"

            elif values['-COMBO|MTD-'] == 'Simpson 1/3 Simple':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 1/3 Simple se obtine como resultado {simpson_1_tercio_simple(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Simple se obtine como resultado {simpson_1_tercio_simple(datos= datos)}"

            elif values['-COMBO|MTD-'] == 'Simpson 1/3 Compuesto':
                
                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_1_tercio_compuesto(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']), n=int(values['-IN|ITV-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_1_tercio_compuesto(datos= datos)}"

            elif values['-COMBO|MTD-'] == 'Simpson 3/8 Simple':
                
                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 3/8 Compuesto se obtine como resultado {simpson_3_8_simple(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_3_8_simple(datos= datos)}"

            else:

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    salida += f"Aplicando el método de Simpson 3/8 Compuesto se obtine como resultado {simpson_3_8_compuesto(expresion=window['-TXT|FUNCION-'].get(), a=float(values['-IN|A-']), b=float(values['-IN|B-']), n=int(values['-IN|ITV-']))}"

                else:
                    salida += f"Aplicando el método de Simpson 1/3 Compuesto se obtine como resultado {simpson_3_8_compuesto(datos= datos)}"
            sg.popup(salida, no_titlebar=True)


        if event == "Salir" or event == sg.WIN_CLOSED:
            break

    window.close()


Integrate()
