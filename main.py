

def main_menu():
    from Derivadas import Derivate
    from Integrales import Integrate
    from Lagrange import solve_lagrange
    from HermiteDiffDivididas import solve_hermite
    from DiffDivididas import solve_diff_divididas
    from Grafico import submenugrafico
    from Biseccion import submenubiseccion
    from FalsaPosicion import submenufalsa
    from PuntoFijo import submenupuntofijo
    from NewtoonRaphson import submenunewtoon
    from secante import submenusecante
    from Bairstow import solve_bairstow
    from Muller import submenumuller
    from EulerAdelante import solve_euler_adelante
    from EulerAtras import solve_euler_atras
    from EulerCentrado import solve_euler_centrado
    from EulerMejorado import solve_euler_mejorado
    from Taylor import solve_taylor
    from RungeKutta import solve_rungekutta
    from senx import submenusen
    from cosx import submenucos
    from ex import submenuexp
    from shx import submenusenhiperbolico
    from chx import submenucosehiperbolico
    from arsenx import submenuarsen
    from arctgx import submenuarctang
    from lnx1 import submenulnxm1
    from fraccion import submenufraccion
    from AdamsBashforth import solve_multipasos 
    from Newton import solve_newton

    menu_def = [['&Unidad 1', ['&Series de Taylor',['sen x', 'cos x',"℮ˣ","sh x","ch x","arcsen x", "ln(1+x)", "1/(1 + x²)", "arctg x"]]],
                ['&Unidad 2', ['Gráfico', 'Bisección', 'Falsa posición',"Punto fijo", 'Newthon raphson',"Secante","Bairstow", "Muller"]],
                ['&Unidad 3', ['Polinomio de Lagrange', 'Polinomio de Newton', 'Diferencias Divididas', 'Polinomio de Hermite']],
                ['&Unidad 4', ['---', '&Derivadas','---', '&Integrales']],
                ['Unidad 5', ['Método de Euler',['Euler hacia adelante', 'Euler hacia atrás', "Euler centrado", "Euler mejorado"],"Método de Taylor", "Método de Runge Kutta", "Método adaptativo"]]]

    layout = [[sg.MenubarCustom(menu_def, pad=(0,0), k='-CUST MENUBAR-')],[sg.Image(filename="portada4.png")]
    ]

    main_window = sg.Window("", layout)

    while True:
        event, values = main_window.read()
        # convert ButtonMenu event so they look like Menu events

        if event == "Salir" or event == sg.WIN_CLOSED:
            break
        elif event == 'Derivadas':
            Derivate()
        elif event == 'Integrales':
            Integrate()
        elif event == 'Polinomio de Lagrange':
            solve_lagrange()
        elif event == 'Polinomio de Hermite':
            solve_hermite()
        elif event == 'Diferencias Divididas':
            solve_diff_divididas() 
        elif event == "sen x":
            submenusen()
        elif event == "cos x":
            submenucos()
        elif event == "℮ˣ":
            submenuexp()
        elif event == "sh x":
            submenusenhiperbolico()
        elif event == "ch x":
            submenucosehiperbolico()
        elif event == "arcsen x":
            submenuarsen()
        elif event == "ln(1+x)":
            submenulnxm1()
        elif event == "1/(1 + x²)":
            submenufraccion()

        elif event == "arctg x":
            submenuarctang()
        elif event == "Gráfico":
            submenugrafico()
        elif event == "Bisección":
            submenubiseccion()
        elif event == 'Falsa posición':
            submenufalsa()
        elif event == "Punto fijo":
            submenupuntofijo()
        elif event == 'Newthon raphson':
            submenunewtoon()
        elif event == "Secante":
            submenusecante()
        elif event == "Bairstow":
            solve_bairstow()
        elif event == "Muller":
            submenumuller()
        elif event == 'Euler hacia adelante':
            solve_euler_adelante()
        elif event == 'Euler hacia atrás':
            solve_euler_atras()
        elif event == 'Euler centrado':
            solve_euler_centrado()
        elif event == 'Euler mejorado':
            solve_euler_mejorado()
        elif event == "Método de Taylor":
            solve_taylor()
        elif event == "Método de Runge Kutta":
            solve_rungekutta()
        elif event == "Método adaptativo":
            solve_multipasos()
        elif event == 'Polinomio de Hermite':
            solve_hermite()
        elif event == 'Polinomio de Newton':
            solve_newton()
        else:
            continue

    main_window.close()


if __name__ == '__main__':
    import PySimpleGUI as sg
    import numpy
    import matplotlib
    import pandas
    import sympy
    main_menu()
    