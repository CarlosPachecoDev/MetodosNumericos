

import PySimpleGUI as sg
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import sympy as sp
import numpy as np

tabla = ['Iteracion','X','g(x)','EA']

def devfuncion(fx,xs,n):
    x = sp.Symbol('x')
    f = sp.sympify(fx)
    derivada = sp.diff(f)
    convergencia = derivada.subs(x, xs)
    ess = (0.5)*(10**(2-n))
    
    if convergencia >1:
        convergencia1 = "NO CONVERGE"
        return None,None,None, derivada, convergencia
    else:

        fx1 = f.subs(x,xs)
        ea = (abs((fx1-xs)/(fx1)))*100
        posicion =1
        iteracionsubs = [posicion]
        xsubs = [xs]
        gxsubs = [fx1]
        easubs = [ea]

        while ess<=ea:
            xs = fx1
            fx1 = f.subs(x,xs)
            ea = (abs((fx1-xs)/(fx1)))*100
            posicion = posicion + 1
            iteracionsubs.append(posicion)
            xsubs.append(xs)
            gxsubs.append(fx1)
            easubs.append(ea)
        data = [iteracionsubs,xsubs,gxsubs,easubs]
        matriz = np.array(data).T
        raiz = gxsubs[-1]
        erro = easubs[-1]
        return matriz,raiz,erro,derivada,convergencia


def submenupuntofijo():
    layout = [
        [sg.Text('Ingrese su funcion "DESPEJADA SEGUN SU CRITERIO"')],
        [sg.Input()],
        [sg.Text('Ingrese su valor inicial "Xo"')],
        [sg.Input()],
        [sg.Text('Ingrese su numero de cifra significativas "n"')],
        [sg.Input()],
        [sg.Table(values=[], headings=tabla , key='-TABLE-', justification='center', col_widths=15, expand_x=True, visible=False)],
        [sg.Text('NO CONVERGE :' , key='-CONV-', visible=False)]+
        [sg.Text('CONVERGENCIA: ', key='-PCONVERGENCIA-', visible=False)],
        [sg.Text('', key='-CONVERGENCIA-',visible=False)],
        [sg.Text('CONVERGENCIA: ', key='-PCONVERGENCIA-', visible=False)],
        [sg.Text('Su derivada es', key='-DERIVADA-', visible=False)]+
        [sg.Text('', key='-Deivada1-', visible=False)],
        [sg.Text('Raiz = ', key='-RAIZ-', visible=False)]+
        [sg.Text('', key='-RAIZ1-', visible=False)],
        [sg.Text('Error = ', key='-ERROR-', visible=False)]+
        [sg.Text('', key='-ERROR1-', visible=False)]+
        [sg.Text('%', key='-ERROR2-', visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')],
    ]
    window = sg.Window('Metodo Punto Fijo',layout, size=(800,600))
    while True:
        event, values = window.read()
        if event =='Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            f1 = parse_expr(values[0],transformations=transformations)
            # f1 = values[0]
            x1 = float(values[1])
            n1 = int(values[2])
            #return matriz,raiz,erro,derivada,convergencia
            m,r,e,d,c =devfuncion(f1,x1,n1)
            
            if c <= 1:
                window['-DERIVADA-'].update(visible=True)
                window['-Deivada1-'].update(d,visible=True)
                window['-TABLE-'].update(values=m.tolist(),visible=True)
                window['-PCONVERGENCIA-'].update(visible=True)
                window['-CONVERGENCIA-'].update(c,visible=True)
                window['-RAIZ-'].update(visible=True)
                window['-RAIZ1-'].update(r,visible=True)
                window['-ERROR-'].update(visible=True)
                window['-ERROR1-'].update(e,visible=True)
                window['-ERROR2-'].update(visible=True)

                window['-CONV-'].update(visible=False)

            else:
                window['-DERIVADA-'].update(visible=True)
                window['-Deivada1-'].update(d,visible=True)
                window['-CONV-'].update(visible=True)
                window['-CONVERGENCIA-'].update(c,visible=True)


                window['-TABLE-'].update(visible=False)
                window['-PCONVERGENCIA-'].update(visible=False)
                window['-RAIZ-'].update(visible=False)
                window['-RAIZ1-'].update(r,visible=False)
                window['-ERROR-'].update(visible=False)
                window['-ERROR1-'].update(e,visible=False)
                window['-ERROR2-'].update(visible=False)

    window.close()