import PySimpleGUI as sg
import sympy as sp
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def funsecante(funcion, x1, x2, n):
    ess = (0.5)*(10**(2-n))
    x = sp.Symbol('x')
    f = sp.sympify(funcion)
    fx1 = f.subs(x, x1)
    fx2 = f.subs(x,x2)
    convergencia = fx1*fx2
    ea = 100
    posicion = 1
    iteracion = []
    x1sub = []
    x2sub = []
    fx1sub = []
    fx2sub = []
    xnm1sub = []
    easub = ['---']

    iteracion.append(posicion)
    x1sub.append(x1)
    x2sub.append(x2)
    fx1 = f.subs(x, x1)
    fx2 = f.subs(x,x2)
    fx1sub.append(fx1)
    fx2sub.append(fx2)
    xnm1 = x2-(fx2*((x2-x1)/(fx2-fx1)))
    xnm1sub.append(xnm1)


    if convergencia < 0:

        while ess <=ea:
            posicion = posicion+1
            xnm1ant = xnm1
            x1=x2
            x2 = xnm1
            iteracion.append(posicion)
            x1sub.append(x1)
            x2sub.append(x2)
            fx1 = f.subs(x, x1)
            fx2 = f.subs(x,x2)
            fx1sub.append(fx1)
            fx2sub.append(fx2)
            xnm1 = x2-(fx2*((x2-x1)/(fx2-fx1)))
            xnm1sub.append(xnm1)
            ea = (abs((xnm1-xnm1ant)/(xnm1)))
            easub.append(ea)

        data = [iteracion, x1sub, x2sub, fx1sub, fx2sub, xnm1sub,easub]
        matriz = np.array(data).T
        raiz = xnm1sub[-1]
        erro = easub[-1]

        return matriz, raiz, erro, convergencia
    
    else:

        return None, None, None, convergencia
        
cabeza = ['Iteracion', 'Xn-1', 'Xn', 'F(xn-1)', 'F(xn)', 'Xn+1', 'EA']

def submenusecante():
    layout = [
        [sg.Text('Ingrese su Funcion')],
        [sg.Input()],
        [sg.Text('Ingrese su X1')],
        [sg.Input()],
        [sg.Text('Ingrese su X2')],
        [sg.Input()],
        [sg.Text('Ingrese su cantidad de cifars significativas "n"')],
        [sg.Input()],
        [sg.Table(values=[], headings=cabeza, key='-TABLE-', justification='center', visible=False, expand_x=True )],
        [sg.Text('Convergencia: ', key='-CONVERGENCIA-', visible= False)]+
        [sg.Text('', key='-CONVERGENCIA1-', visible=False)],
        [sg.Text('Raiz', key='-RAIZ-', visible=False)]+
        [sg.Text('', key='-RAIZ1-', visible=False)],
        [sg.Text('Error' , key='-ERROR-', visible=False)]+
        [sg.Text('', key='-ERROR1-', visible=False)],
        [sg.Text('No converge' , key='-CONV-', visible=False)]+
        [sg.Text('', key='-CONV1-', visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')],
    ]
    windowse = sg.Window('Metodo de la Secante', layout, size=(1000,600) )
    while True:
        event, values = windowse.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            fun = parse_expr(values[0],transformations=transformations)
            x11 = float(values[1])
            x22 = float(values[2])
            n = int(values[3])
            # return matriz, raiz, erro, convergencia
            m, r, e, c = funsecante(fun, x11, x22, n)

            if c < 0:
                windowse['-TABLE-'].update(values=m.tolist(), visible=True)
                windowse['-RAIZ-'].update(visible=True)
                windowse['-RAIZ1-'].update(r, visible=True)
                windowse['-CONVERGENCIA-'].update(visible=True)
                windowse['-CONVERGENCIA1-'].update(c, visible=True)
                windowse['-ERROR-'].update(visible=True)
                windowse['-ERROR1-'].update(e, visible=True)

                windowse['-CONV-'].update(visible=False)
                windowse['-CONV1-'].update(visible=False)
                
            else:
                windowse['-TABLE-'].update(visible=False)
                windowse['-RAIZ-'].update(visible=False)
                windowse['-RAIZ1-'].update(visible=False)
                windowse['-ERROR-'].update(visible=False)
                windowse['-ERROR1-'].update(visible=False)
                windowse['-CONVERGENCIA-'].update(visible=False)
                windowse['-CONVERGENCIA1-'].update(c, visible=False)

                windowse['-CONV-'].update(visible=True)
                windowse['-CONV1-'].update(c, visible=True)

    windowse.close()



