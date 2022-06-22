
import math
import cmath
import numpy as np
from UtilitiesGUI import *

def cuadratica(r,s): 
    discrim = math.pow(r,2)+(4*s)
    raices = []
    if discrim > 0: 
        raices.append((r+math.sqrt(discrim))/(2))
        raices.append((r-math.sqrt(discrim))/(2))
    else: 
        raices.append((r-cmath.sqrt(discrim))/2)
        raices.append((r+cmath.sqrt(discrim))/2)
    return raices

def cuadratica2(a,b,c):
    discrim = math.pow(b,2)-(4*a*c)
    raices = []
    if discrim > 0:
        raices.append((-b+math.sqrt(discrim))/(2*a))
        raices.append((-b-math.sqrt(discrim))/(2*a))
    else:
        raices.append((-b-cmath.sqrt(discrim))/(2*a))
        raices.append((-b+cmath.sqrt(discrim))/(2*a))
    return raices

def generateb(a, r, s): 
    b = []
    b.append(a[0])
    b.append(a[1]+(r*b[-1]))
    for i in a[2:]:
        b.append(i+(r*b[-1])+(s*b[-2]))
    return b

def generatec(b, r, s): 
    c = []
    c.append(b[0])
    c.append(b[1]+(r*c[-1]))
    for i in b[2:-1]:
        c.append(i+(r*c[-1])+(s*c[-2]))
    return c

def bairstow(r,s,a,nivel_tolerancia):
    grado_polinomio = len(a)-1
    noIter = 1
    raices = []
    b = []
    while grado_polinomio > 0:
        noIter=0
        rerror = 100
        serror = 100
        if grado_polinomio == 1:
            
            if len(b) != 0:
                raices.append(-b[1]/b[0])
            else:
                raices.extend(cuadratica2(a[0],a[1],a[2]))
            grado_polinomio -= 1
        elif grado_polinomio == 2:
            
            if len(b) != 0:
                raices.extend(cuadratica2(b[0],b[1],b[2]))
            else:
                raices.extend(cuadratica2(a[0],a[1],a[2]))
            grado_polinomio -= 2
        else:
            
            while rerror>nivel_tolerancia or serror>nivel_tolerancia:
                b = generateb(a,r,s) 
                c = generatec(b,r,s) 
                eq1 = np.array([[c[-2],c[-3]],[c[-1],c[-2]]])
                eq2 = np.array([-b[-2],-b[-1]])
                solEq = np.linalg.solve(eq1,eq2) 
                rdelta = solEq[0]
                sdelta = solEq[1]
                r += rdelta
                s += sdelta
                rerror = abs(rdelta/r)*100 
                serror = abs(sdelta/s)*100
                noIter+=1
            raices.extend(cuadratica(r,s))
            a = b[:-2]
            grado_polinomio -= 2

    return raices

def solve_bairstow():

    main_layout = [

            [sg.pin(sg.Text('Ro: ', key="-LBL|RO-")), sg.pin(sg.Input(key="-IN|RO-", size=(10, 1))), sg.pin(sg.Text('So: ', key="-LBL|SO-")), sg.pin(sg.Input(key="-IN|SO-", size=(10, 1)))],
            [sg.pin(sg.Text("Cifras significativas:", key="-TXT|CS-")), sg.pin(sg.Input(key="-IN|CS-", size=(10, 1)))],
            [sg.pin(sg.Text("Grado del polinomio:", key="-TXT|GRD-")), sg.pin(sg.Input(enable_events=True, key="-IN|GRD-", size=(13, 1))),sg.Button('Ingresar coeficientes',key="-BTN|FILL-", visible=False)],
            [sg.Text("",key="-TXT|RES-", visible=False)],
            [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-"), sg.Button('Borrar', key="-BTN|CLR-")]
        ]

    bairstow_window = sg.Window("", main_layout)
    inputs = ["-IN|GRD-"]
    while True:
        event, values = bairstow_window.read()
        print(values)
        print(event)
        if event in inputs and len(values[event]) and values[event][-1] not in ('456789'):
            bairstow_window[event].update(values[event][:-1])

        else:

            if values["-IN|GRD-"] != None:
                show(["-BTN|FILL-"], bairstow_window)
            else:
                hide(["-BTN|FILL-"], bairstow_window)

        if event == "-BTN|FILL-":
            coeff = create_table(cols=int(values["-IN|GRD-"])+1,rows=1)
            coeff = [float(num) for num in coeff[0]]
        
        if event == "-BTN|SOLVE-":

            raices = bairstow(r=float(values["-IN|RO-"]),s=float(values["-IN|SO-"]),a=coeff,nivel_tolerancia=0.5*10**(2-int(values["-IN|CS-"])))
            respuesta = "Raíces:\n"
            for i in range(len(raices)):
                respuesta  += f"\n\tRaíz no.{i}: {raices[i]}"
            bairstow_window["-TXT|RES-"].update(value=respuesta, visible=True)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    bairstow_window.close()


