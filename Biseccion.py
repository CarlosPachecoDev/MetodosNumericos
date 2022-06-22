
import PySimpleGUI as sg
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import numpy as np


cabeza = ['teracion', 'X1','X2','Xr', 'f(x1)','f(xr)','f(x1)(xr)', 'EA']

def conv(tt,x1,x2,n):
    x = sp.Symbol('x')
    tt1 = sp.sympify(tt)
    xr1 = x1
    xr2 = x2
    n1 = n
    print(tt1)

    ess = (0.5)*10**(2-n1)
    xr = (xr1+xr2)/2
    fx1 = tt1.subs(x,xr1)
    fxr = tt1.subs(x,xr)
    print(fx1)
    fx1fxr = fx1*fxr
    ea = 100
    posicion = 0
    iteracion = [posicion]
    xsub1 = [xr1]
    xsub2 = [xr2]
    xrsub = [xr]
    fx1sub = [fx1]
    fxrsub = [fxr]
    fx1fxrsub = [fx1fxr]
    easub = ['--']

    while ess<ea:
        
        if fx1fxr < 0 :
            xr2 = xr
            posicion=posicion+1
        else:
            xr1 = xr
            posicion=posicion+1
        
        xrant = xr
        xr = (xr1+xr2)/2
        fx1 = tt1.subs(x,xr1)
        fxr = tt1.subs(x,xr)
        fx1fxr = fx1*fxr
            
        ea = (abs((xr-xrant)/xr))*100
        iteracion.append(posicion)
        xsub1.append(xr1)
        xsub2.append(xr2)
        xrsub.append(xr)
        fx1sub.append(fx1)
        fxrsub.append(fxr)
        fx1fxrsub.append(fx1fxr)
        easub.append(ea)
        


    print("Termino")
    print(ea)
    print(xrsub[-1])
    print(xsub1)
    print(xsub2)
    data = [iteracion,xsub1,xsub2,xrsub,fx1sub,fxrsub,fx1fxrsub,easub]
    matriz = np.array(data).T
    finalraiz = xrsub[-1]
    finalerror = easub[-1]
    print(matriz)

    return matriz,finalraiz,finalerror
    
def submenubiseccion():
    layout = [
        [sg.Text('Ingrese Su Funcion')],
        [sg.Input()],
        [sg.Text('Ingrese el Valor de X1')],
        [sg.Input()],
        [sg.Text('Ingrese el valor de X2')],
        [sg.Input()],
        [sg.Text('Ingrese el Valor de "n"')],
        [sg.Input()],
        [sg.Table(values=[], headings=cabeza, justification="center", key="-TABLE-", col_widths=20, expand_x=True )],
        [sg.Text("Su Raiz es: ", key="-Raiz-", visible=False)]+
        [sg.Text("", key="-Raiz1-", visible=False)],
        [sg.Text("Su error es :", key = "-Error-", visible=False)]+
        [sg.Text("", key="-Error1-", visible=False)]+
        [sg.Text("%" , key="-porce-" , visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')]
    ]
    window = sg.Window('Metodo de la Biseccion', layout, size=(1000,600), )
    while True:
         event, value = window.read()
         if event == 'Salir' or event == sg.WIN_CLOSED:
            break
         if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            fuct = parse_expr(value[0],transformations=transformations)
            x1 = float(value[1])
            x2 = float(value[2])
            n = int(value[3])
            matriz, raiz, error = conv(fuct,x1,x2,n)
            window["-TABLE-"].update(values=matriz.tolist())
            window["-Raiz-"].update(visible=True)
            window["-Raiz1-"].update(raiz, visible=True)
            window["-Error-"].update(visible=True)
            window["-Error1-"].update(error, visible=True)
            window["-porce-"].update(visible=True)
    window.close()