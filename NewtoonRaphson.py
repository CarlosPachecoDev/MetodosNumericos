
import PySimpleGUI as sg
import sympy as sp
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def evaluacion(f,x1,n):
    x = sp.Symbol('x')
    xr = x1
    f1 = sp.sympify(f)
    ess = (0.5)*(10**(2-n))
    ea = 100
    posicion = 1
    derivada = sp.diff(f1)
    segundaderivada = sp.diff(derivada)
    fx = f1.subs(x, xr)
    fxdev = derivada.subs(x, xr)
    fxsegundadev = segundaderivada.subs(x, xr)
    xn1 = xr - ((fx)/(fxdev))
    convergencia = abs((fx*fxsegundadev)/(fxdev**2))
    iteracion = []
    xnsub = []
    fxsub = []
    fxdevsub = []
    xn1sub = []
    easub = []

    
    if convergencia < 1 :
        while ess <=ea:
            iteracion.append(posicion)
            xnsub.append(xr)
            fxsub.append(fx)
            fxdevsub.append(fxdev)
            xn1sub.append(xn1)
            ea = (abs((xn1-xr)/(xn1)))*100
            easub.append(ea)
            posicion = posicion+1
            xr = xn1
            fx = f1.subs(x, xr)
            fxdev = derivada.subs(x, xr)
            fxsegundadev = segundaderivada.subs(x, xr)
            xn1 = xr - ((fx)/(fxdev))
        
        data = [iteracion,xnsub,fxsub,fxdevsub,xn1sub,easub]
        matriz = np.array(data).T

        raiz = xn1sub[-1]
        error = easub[-1]
        return matriz, raiz, error, convergencia

    else: 
        return None,None,None,convergencia

        

cabeza = ['Itreacion', 'Xn', 'F(xn)', "F'(xn)", 'Xn+1', 'EA']
def submenunewtoon():
    layout=[ 
        [sg.Text('Ingrese su Funcion')],
        [sg.pin(sg.Input())],
        [sg.pin(sg.Text('Ingrese su Valor Inicial "X0"'))],
        [sg.pin(sg.Input())],
        [sg.pin(sg.Text('Ingrese Cantida Cifras Significativas "n"'))],
        [sg.pin(sg.Input())],
        [sg.Table(values=[], headings=cabeza, key='-TABLE-', justification='center', visible=False, expand_x=True)],
        [sg.pin(sg.Text('Convergencia: ', key='-CONVERGENCIA-',visible= False))]+
        [sg.pin(sg.Text('', key='-CONVERGENCIA1-', visible=False))],
        [sg.pin(sg.Text('NO CONVERGE :', key='-CONV-', visible=False))]+
        [sg.pin(sg.Text('', key='-CONV1-', visible=False))],
        [sg.pin(sg.Text('Raiz = ', key='-RAIZ-', visible=False))]+
        [sg.pin(sg.Text('', key='-RAIZ1-', visible=False))],
        [sg.pin(sg.Text('Error :' , key='-ERROR-', visible=False))]+
        [sg.pin(sg.Text('', key='-ERROR1-', visible=False))],
        [sg.pin(sg.Button('Evaluar')), sg.pin(sg.Button('Salir'))],

    ]

    window1 = sg.Window('Metodo Newtoon Raphson', layout, size=(1000,500))
    while True:
        event, values = window1.read()
        if event =='Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            f1 =  parse_expr(values[0],transformations=transformations)
            xo = float(values[1])
            no = int(values[2])
            m,r,e,c = evaluacion(f1,xo,no)

            if c < 1:
                window1['-TABLE-'].update(values=m.tolist(), visible=True)
                window1['-CONVERGENCIA-'].update(visible=True)
                window1['-CONVERGENCIA1-'].update(c , visible=True)
                window1['-RAIZ-'].update(visible=True)
                window1['-RAIZ1-'].update(r, visible=True)
                window1['-ERROR-'].update(visible=True)
                window1['-ERROR1-'].update(e, visible=True)
                window1['-CONV-'].update(visible=False)
                window1['-CONV1-'].update(visible=False)

            
            else:
                window1['-RAIZ-'].update(visible=False)
                window1['-RAIZ1-'].update(visible=False)
                window1['-ERROR-'].update(visible=False)
                window1['-ERROR1-'].update(visible=False)
                window1['-CONVERGENCIA-'].update(visible=False)
                window1['-CONVERGENCIA1-'].update(visible=False)
                window1['-TABLE-'].update(visible=False)
                window1['-CONV-'].update(visible=True)
                window1['-CONV1-'].update(c, visible=True)
    window1.close()

                


