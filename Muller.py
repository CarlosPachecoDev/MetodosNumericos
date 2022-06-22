from cmath import sqrt
import PySimpleGUI as sg
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import sympy  as sp

def resolucion(f, x0,x1,n):
    ess = (0.5)*(10**(2-n))
    x = sp.Symbol('x')
    f1 = sp.sympify(f)
    ea = 100
    xv0 = x0
    xv1 = x1
    xv2 = (x0 + x1) /2

    while ea>ess:
        h0 = xv1-xv0
        h1 = xv2-xv1

        # X2 = (x0+x1)/2

        fx1 = f1.subs(x,xv1)
        fx0 = f1.subs(x,xv0)
        fx2 = f1.subs(x,xv2)
        D0 = (fx1-fx0)/(h0)
        D1 = (fx2-fx1)/(h1)

        a = (D1-D0)/(h1+h0)
        b = (a*h1)+D1
        c = fx2

        D = sqrt((b**2)-(4*a*c))

        if abs(b+D)> abs(b-D):
            xr = xv2+((-2*c)/(b+D))
        else: 
            xr = xv2+((-2*c)/(b-D))
        
        ea = (abs((xr-xv2)/(xr)))
        xv0 = xv1
        xv1 = xv2
        xv2 = xr

    return xr , ea




def submenumuller():
    
    layout=[
        [sg.Text('Ingrese su Funcion')],
        [sg.Input()],
        [sg.Text('Ingrese su valor de "Xo"')],
        [sg.Input()],
        [sg.Text('Ingrese el valor de "X1"')],
        [sg.Input()],
        [sg.Text('Ingrese el valor de  cifras significativas "n"')],
        [sg.Input()],
        [sg.Text('Raiz : ', key='-RAIZ-', visible=False)]+
        [sg.Text('', key='-RAIZ1-', visible=False)],
        [sg.Text('Error : ', key='-ERROR-', visible=False)]+
        [sg.Text('', key='-ERROR1-', visible=False)],
        [sg.Button('Evaluar')],
        [sg.Button('Salir')]

    ]
    
    windowmuller = sg.Window('Metodo de Muller', layout)
    while True:
        event, values = windowmuller.read()

        if event == 'Salir' or event == sg.WIN_CLOSED:
            break
        if event == 'Evaluar':
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            func = parse_expr(values[0],transformations=transformations)
            x0 = float(values[1])
            x1 = float(values[2])
            n1 = int(values[3])

            r,e = resolucion(func,x0,x1,n1)

            windowmuller['-RAIZ-'].update(visible=True)
            windowmuller['-RAIZ1-'].update(r,visible=True)
            windowmuller['-ERROR-'].update(visible=True)
            windowmuller['-ERROR1-'].update(e,visible=True)

    windowmuller.close()
