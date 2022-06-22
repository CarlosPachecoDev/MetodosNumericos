
import PySimpleGUI as sg
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import sympy as sp
import numpy as np



def evaluada(f1,xs1,xs2,n1):
    x = sp.Symbol('x')
    ess = (0.5)*(10**(2-n1))
    xr1 = xs1
    xr2 = xs2
    ft = sp.sympify(f1)
    posicion = 1
    fx1 = ft.subs(x,xr1)
    fx2 = ft.subs(x,xr2)
    xr = xr1-(((fx1)*(xr1-xr2))/(fx1-fx2))
    fxr = ft.subs(x,xr)
    fx1fxr = fx1*fxr
    ea = 100
    iteracion = [posicion]
    x1sub = [xr1]
    x2sub =  [xr2]
    fx1sub = [fx1]
    fx2sub = [fx2]
    xrsub = [xr]
    fxrsub = [fxr]
    fx1fxrsub = [fx1fxr]
    easub = ['---']

    while ess<=ea:
        
        if fx1fxr < 0:
            xr2 = xr
        if fx1fxr > 0:
            xr1 = xr
        if fx1fxr == 0:
            break

        xrant = xr
        posicion = posicion + 1
        fx1 = ft.subs(x,xr1)
        fx2 = ft.subs(x,xr2)
        xr = xr1-(((fx1)*(xr1-xr2))/(fx1-fx2))
        fxr = ft.subs(x,xr)
        fx1fxr = fx1*fxr
        ea = (abs((xr-xrant)/xr))*100

        iteracion.append(posicion)
        x1sub.append(xr1)
        x2sub.append(xr2)
        fx1sub.append(fx1)
        fx2sub.append(fx2)
        xrsub.append(xr)
        fxrsub.append(fxr)
        fx1fxrsub.append(fx1fxr)
        easub.append(ea)
    
    raiz = xrsub[-1]
    error = easub[-1]
    data = [iteracion,x1sub,x2sub,fx1sub,fx2sub,xrsub,fxrsub,fx1fxrsub,easub]
    matriz = np.array(data).T

    return matriz,raiz,error

cabeza = ['Iteracion', 'X1','X2', 'f(x1)','f(x2)','Xr', 'f(xr)', 'f(x1)(xr)','EA']

def submenufalsa():
    layout = [
        [sg.Text('Ingrese su Funcion')],
        [sg.Input()],
        [sg.Text('Ingrese X1')],
        [sg.Input()],
        [sg.Text('Ingrese X2')],
        [sg.Input()],
        [sg.Text('Ingrese Cantidad de Cifras Significativas "n" ')],
        [sg.Input()],
        [sg.Table(values=[], headings=cabeza, key='-TABLE-', expand_x=True, col_widths=16, justification='center')],
        [sg.Text("Raiz: ",key='-Raiz-',visible=False)]+
        [sg.Text("",key='-Raiz1-', visible=False)],
        [sg.Text("Error :" , key='-Error-', visible=False)]+
        [sg.Text("",key='-Error1-', visible=False)]+
        [sg.Text("%", key='-Error2-', visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')]
    ]
    window = sg.Window('Metodo Falsa Posicion', layout, size=(1000,600))

    while True:
        event, values = window.read()

        if event== 'Salir' or event == sg.WIN_CLOSED:
            break

        if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            f = parse_expr(values[0],transformations=transformations) 
            x1 = float(values[1])
            x2 = float(values[2])
            n = int(values[3])
            matre,rai,error = evaluada(f,x1,x2,n)
            window['-TABLE-'].update(values=matre.tolist())
            window['-Raiz-'].update(visible=True)
            window['-Raiz1-'].update(rai, visible=True)
            window['-Error-'].update(visible=True)
            window['-Error1-'].update(error, visible=True)
            window['-Error2-'].update(visible=True)
    
    window.close()
