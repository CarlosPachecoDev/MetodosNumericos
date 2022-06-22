import PySimpleGUI as sg
import math
import numpy as np
from Calculadora import showCalculator, transform_fx
from UtilitiesGUI import *

def Derivate():

    def get_datos(col):
        val_x = [float(window[f"-IN|X{x+1}-"].get()) for x in range(col)]
        val_y = [float(window[f"-IN|Y{x+1}-"].get()) for x in range(col)]

        return val_x, val_y


    def fill_paso(val_x):

        for i in range(len(val_x) - 1):
            h.append(round(val_x[i+1] - val_x[i], 3))
        return h


    def comprobar_salto(h):

        flag = True
        for i in range(len(h)-1):
            if h[i] != h[i+1]:
                flag = False
                break
        return flag


    def richardson(vv, valor_inicial, metodo, diferencia, paso, orden, nivel, fx=None, yi=None):
        j = 0
        resultados = list()
        errores = list()
        matriz = []

        for i in range(nivel):
            matriz.append([])

        if fx != None:
            px = transform_fx(fx)
            METODOS = {
                'Diferencias Hacia Atrás': diff_hacia_atras,
                'Diferencias Hacia Adelante': diff_hacia_adelante,
                'Diferenciación centrada': diff_centrada,
                '3 puntos': diff_trespuntos,
                '5 puntos': diff_cincopuntos
            }
            # nivel 1
            h = paso
            for i in range(nivel):
                respuesta, error = METODOS[metodo](
                    vv, orden, h, diferencia, valor_inicial, fx)
                errores.append(round(float(error[0]), 9))
                matriz[0].append(round(float(respuesta[0]), 9))
                h = h/2

            for i in range(nivel - 1):
                k = i + 1
                for j in range(nivel - (i+1)):
                    D_k = (4**k * matriz[i][j+1] - matriz[i][j])/(4**k - 1)
                    matriz[i+1].append(round(D_k, 9))

            for i in matriz:
                if len(i) < nivel:
                    for j in range(nivel - len(i)):
                        i.append(0)

            error = math.fabs((vv[0] - matriz[nivel - 1][0])/vv[0]) * 100

        return matriz[nivel - 1][0], error, errores[0], matriz


    def diff_cincopuntos(vv, orden, paso, diferencia, valor_inicial=None, fx=None, yi=None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:
            px = transform_fx(fx)

            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda valor: (-25*px(valor) + 48*px(valor + paso) - 36*px(valor + 2*paso) + 16*px(valor + 3*paso) - 3*px(valor + 4*paso))/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Segunda diferencia":

                DIFERENCIAS = {
                    "1": lambda valor: (-3*px(valor - paso) - 10*px(valor) + 18*px(valor + paso) - 6*px(valor + 2*paso) + px(valor + 3*paso))/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Tercera diferencia":

                DIFERENCIAS = {
                    "1": lambda valor: (px(valor - 2*paso) - 8*px(valor - paso) + 8*px(valor + paso) - px(valor + 2*paso))/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Cuarta diferencia":

                DIFERENCIAS = {
                    "1": lambda valor: (4*px(valor - 3*paso) + 6*px(valor - 2*paso) - 8*px(valor - paso) + 34*px(valor) + 3*px(valor + paso) + 34*px(valor + 2*paso))/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

            else:

                DIFERENCIAS = {
                    "1": lambda valor: (px(valor - 4*paso) - 3*px(valor - 3*paso) + 4*px(valor - 2*paso) - 36*px(valor - paso) + 25*px(valor))/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

        else:

            val_y = yi
            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (-25*val_y[0] + 48*val_y[1] - 36*val_y[2] + 16*val_y[3] - 3*val_y[4])/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Segunda diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (-3*val_y[0] - 10*val_y[1] + 18*val_y[2] - 6*val_y[3] + val_y[4])/(12*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Tercera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[0] - 8*val_y[1] + 8*val_y[2] - val_y[3])/(12*paso)
                }

                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

            elif diferencia == "Cuarta diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (4*val_y[0] + 6*val_y[2] - 8*val_y[1] + 34*val_y[0] + 3*val_y[1] + 34*val_y[2])/(12*paso)
                }

                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

            else:

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[0] - 3*val_y[1] + 4*val_y[2] - 36*val_y[3] + 25*val_y[4])/(12*paso)
                }

                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_trespuntos(vv, orden, paso, diferencia, valor_inicial=None, fx=None, yi=None):
        resultados = list()
        errores = list()
        j = 0
        if fx != None:
            px = transform_fx(fx)
            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda valor: (px(valor + paso) - px(valor - paso))/(2*paso)
                }
                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1

            else:
                DIFERENCIAS = {
                    "1": lambda valor: (-3*px(valor) + 4*px(valor + paso) - px(valor + 2*paso))/(2*paso)
                }

                for i in range(orden):
                    resultados.append(DIFERENCIAS[str(i+1)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](valor_inicial))/vv[j]) * 100)
                    j += 1
        else:
            val_y = yi
            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[2] - val_y[0])/(2*paso)
                }
                for i in range(len(orden)):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1
            else:

                DIFERENCIAS = {
                    "1": lambda paso: (-3*val_y[0] + 4*val_y[1] - val_y[2])/(2*paso)
                }
                for i in range(len(orden)):
                    resultados.append(DIFERENCIAS[str(i+1)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i+1)](paso))/vv[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_centrada(vv, orden, paso, diferencia, valor_inicial=None, fx=None, yi=None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:

            px = transform_fx(fx)
            if diferencia == "Primera diferencia":
                DIFERENCIAS = {
                    "1": lambda valor: (px(valor + paso) - px(valor - paso))/(2*paso),
                    "2": lambda valor: (px(valor + paso) - 2*px(valor) + px(valor - paso))/paso**2,
                    "3": lambda valor: (px(valor + 2*paso) - 2*px(valor + paso) + 2*px(valor - paso) - px(valor - 2*paso))/(2*paso**3),
                    "4": lambda valor: (px(valor + 2*paso) - 4*px(valor + paso) + 6*px(valor) - 4*px(valor - paso) + px(valor - 2*paso))/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1

            else:
                DIFERENCIAS = {
                    "1": lambda valor: (-px(valor + 2*paso) + 8*px(valor + paso) - 8*px(valor - paso) + px(valor - 2*paso))/(12*paso),
                    "2": lambda valor: (-px(valor + 2*paso) + 16*px(valor + paso) - 30*px(valor) + 16*px(valor - paso) - px(valor - 2*paso))/(12*paso**2),
                    "3": lambda valor: (-px(valor + 3*paso) + 8*px(valor + 2*paso) - 13*px(valor + paso) + 13*px(valor - paso) - 8*px(valor - 2*paso) + px(valor - 3*paso))/(8*paso**3),
                    "4": lambda valor: (-px(valor + 3*paso) + 12*px(valor + 2*paso) - 39*px(valor + paso) + 56*px(valor) - 39*px(valor - paso) + 12*px(valor - 2*paso) - px(valor - 3*paso))/(6*paso**4)
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1
        else:

            if diferencia == "Primera diferencia":
                nmax = max([int(num) for num in orden])
                if nmax == 2:
                    mid = math.ceil((nmax + 1)/2)
                else:
                    mid = math.ceil((nmax + 2)/2)
                mid = mid - 1
                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (val_y[mid + 1] - val_y[mid - 1])/(2*paso),
                    "2": lambda paso: (val_y[mid + 1] - 2*val_y[mid] + val_y[mid - 1])/paso**2,
                    "3": lambda paso: (val_y[mid + 2] - 2*val_y[mid + 1] + 2*val_y[mid - 1] - val_y[mid - 2])/(2*paso**3),
                    "4": lambda paso: (val_y[mid + 2] - 4*val_y[mid + 1] + 6*val_y[mid] - 4*val_y[mid - 1] + val_y[mid - 2])/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

            else:

                if max([int(num) for num in orden]) <= 2:
                    mid = math.ceil(
                        (max([int(num) for num in orden]) + (5-max([int(num) for num in orden])))/2) - 1
                else:
                    mid = ((max([int(num) for num in orden]) +
                        (6-max([int(num) for num in orden])))/2) - 1

                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (-val_y[mid + 2] + 8*val_y[mid + 1] - 8*val_y[mid - 1] + val_y[mid - 2])/(12*paso),
                    "2": lambda paso: (-val_y[mid + 2] + 16*val_y[mid + 1] - 30*val_y[mid] + 16*val_y[mid - 1] - val_y[mid - 2])/(12*paso**2),
                    "3": lambda paso: (-val_y[mid + 3] + 8*val_y[mid + 2] - 13*val_y[mid + 1] + 13*val_y[mid - 1] - 8*val_y[mid - 2] + val_y[mid - 3])/(8*paso**3),
                    "4": lambda paso: (-val_y[mid + 3] + 12*val_y[mid + 2] - 39*val_y[mid + 1] + 56*val_y[mid] - 39*val_y[mid - 1] + 12*val_y[mid - 2] - val_y[mid - 3])/(6*paso**4)
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_hacia_adelante(vv, orden, paso, diferencia, valor_inicial=None, fx=None, yi=None):
        resultados = list()
        errores = list()
        j = 0
        if fx != None:
            px = transform_fx(fx)
            if diferencia == "Primera diferencia":
                DIFERENCIAS = {
                    "1": lambda valor: (px(valor + paso) - px(valor))/paso,
                    "2": lambda valor: (px(valor + 2*paso) - 2*px(valor + paso) + px(valor))/paso**2,
                    "3": lambda valor: (px(valor + 3*paso) - 3*px(valor + 2*paso) + 3*px(valor + paso) - px(valor))/(2*paso**3),
                    "4": lambda valor: (px(valor + 4*paso) - 4*px(valor + 3*paso) + 6*px(valor + 2*paso) - 4*px(valor + paso) + px(valor))/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1

            else:
                DIFERENCIAS = {
                    "1": lambda valor: (-px(valor + 2*paso) + 4*px(valor + paso) - 3*px(valor))/(2*paso),
                    "2": lambda valor: (-px(valor + 3*paso) + 4*px(valor + 2*paso) - 5*px(valor + paso) + 2*px(valor))/paso**2,
                    "3": lambda valor: (-3*px(valor + 4*paso) + 14*px(valor + 3*paso) - 24*px(valor + 2*paso) + 18*px(valor + paso) - 5*px(valor))/(2*paso**3),
                    "4": lambda valor: (-2*px(valor + 5*paso) + 11*px(valor + 4*paso) - 24*px(valor + 3*paso) + 26*px(valor + 2*paso) - 14*px(valor + paso) + 3*px(valor))/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1

        else:

            if diferencia == "Primera diferencia":
                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (val_y[1] - val_y[0])/paso,
                    "2": lambda paso: (val_y[2] - 2*val_y[1] + val_y[0])/paso**2,
                    "3": lambda paso: (val_y[3] - 3*val_y[2] + 3*val_y[1] - val_y[0])/(2*paso**3),
                    "4": lambda paso: (val_y[4] - 4*val_y[3] + 6*val_y[2] - 4*val_y[1] + val_y[0])/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

            else:

                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (-val_y[2] + 4*val_y[1] - 3*val_y[0])/(2*paso),
                    "2": lambda paso: (-val_y[3] + 4*val_y[2] - 5*val_y[1] + 2*val_y[0])/paso**2,
                    "3": lambda paso: (-3*val_y[4] + 14*val_y[3] - 24*val_y[2] + 18*val_y[1] - 5*val_y[0])/(2*paso**3),
                    "4": lambda paso: (-2*val_y[5] + 11*val_y[4] - 24*val_y[3] + 26*val_y[2] - 14*val_y[1] + 3*val_y[0])/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_hacia_atras(vv, orden, paso, diferencia, valor_inicial=None, fx=None, yi=None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:

            px = transform_fx(fx)
            if diferencia == "Primera diferencia":
                DIFERENCIAS = {
                    "1": lambda valor: (px(valor) - px(valor - paso))/paso,
                    "2": lambda valor: (px(valor) - 2*px(valor - paso) + px(valor - 2*paso))/paso**2,
                    "3": lambda valor: (px(valor) - 3*px(valor - paso) + 3*px(valor - 2*paso) - px(valor - 3*paso))/(2*paso**3),
                    "4": lambda valor: (px(valor) - 4*px(valor - paso) + 6*px(valor - 2*paso) - 4*px(valor - 3*paso) + px(valor - 4*paso))/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1

            else:
                DIFERENCIAS = {
                    "1": lambda valor: (3*px(valor) - 4*px(valor - paso) + px(valor - 2*paso))/(2*paso),
                    "2": lambda valor: (2*px(valor) - 5*px(valor - paso) + 4*px(valor - 2*paso) - px(valor - 3*paso))/paso**2,
                    "3": lambda valor: (5*px(valor) - 18*px(valor - paso) + 24*px(valor - 2*paso) - 14*px(valor - 3*paso) + 3*px(valor - 4*paso))/(2*paso**3),
                    "4": lambda valor: (3*px(valor) - 14*px(valor - paso) + 26*px(valor - 2*paso) - 24*px(valor - 3*paso) + 11*px(valor - 4*paso) - 2*px(valor - 5*paso))/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](valor_inicial))/vv[j]) * 100)
                    j += 1

        else:

            if diferencia == "Primera diferencia":
                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (val_y[0] - val_y[1])/paso,
                    "2": lambda paso: (val_y[0] - 2*val_y[1] + val_y[2])/paso**2,
                    "3": lambda paso: (val_y[0] - 3*val_y[1] + 3*val_y[2] - val_y[3])/(2*paso**3),
                    "4": lambda paso: (val_y[0] - 4*val_y[1] + 6*val_y[2] - 4*val_y[3] + val_y[4])/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

            else:
                val_y = yi
                DIFERENCIAS = {
                    "1": lambda paso: (3*val_y[0] - 4*val_y[1] + val_y[2])/(2*paso),
                    "2": lambda paso: (2*val_y[0] - 5*val_y[1] + 4*val_y[2] - val_y[3])/paso**2,
                    "3": lambda paso: (5*val_y[0] - 18*val_y[1] + 24*val_y[2] - 14*val_y[3] + 3*val_y[4])/(2*paso**3),
                    "4": lambda paso: (3*val_y[0] - 14*val_y[1] + 26*val_y[2] - 24*val_y[3] + 11*val_y[4] - 2*val_y[5])/paso**4
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((vv[j] - DIFERENCIAS[str(i)](paso))/vv[j]) * 100)
                    j += 1

        return resultados, errores


    # TabsLayout
    tabs_layout = [
        [
            sg.Tab('Diferencias Hacia Atrás', [], font='Courier 15', key='-TAB1-'),
            sg.Tab('Diferencias Hacia Adelante', [], key='-TAB2-'),
            sg.Tab('Diferenciación centrada', [], key='-TAB3-'),
            sg.Tab('3 puntos', [], key='-TAB4-'),
            sg.Tab('5 puntos', [], key='-TAB5-'),
            sg.Tab('Ricahrdson', [], key='-TAB6-')
        ]
    ]

    # MainLayout
    main_layout = [
        [sg.TabGroup(tabs_layout, enable_events=True, key='-TABGROUP-')],
        [sg.Text('Orden: ', key="-TXT|ORDEN-"), sg.Image(radio_unchecked, enable_events=True, k='1', metadata=False), sg.T('Orden 1', k="T1"), sg.Image(radio_unchecked, enable_events=True, k='2', metadata=False), sg.T('Orden 2', k="T2"), sg.Image(radio_unchecked, enable_events=True, k='3', metadata=False), sg.T('Orden 3', k="T3"), sg.Image(radio_unchecked, enable_events=True, k='4', metadata=False), sg.T('Orden 4', k="T4")],
        [sg.pin(sg.Text("Nivel", key="-TXT|LVL-")), sg.pin(sg.Input(enable_events=True, key="-IN|LVL-", size=(13, 1)))],
        [sg.pin(sg.Text('Método de diferenciación', key="-TXT|MTD-")), sg.pin(sg.Combo(['Diferencias Hacia Atrás', 'Diferencias Hacia Adelante','Diferenciación centrada', '3 puntos', '5 puntos'], default_value="", enable_events=True, readonly=True, key='-COMBO|MTD-'))],
        [sg.Text('Seleccione la opción de datos a ingresar'), sg.Combo(["Función Matemática","Tabla de datos"], default_value="", enable_events=True, readonly=True, key='-COMBO|DATOS-')],
        [sg.Text('Seleccione la diferencia'), sg.Combo(["Primera diferencia", "Segunda diferencia"], default_value="", enable_events=True, readonly=True, key='-COMBO|DIF-'), sg.Combo(["Primera diferencia","Segunda diferencia", "Tercera diferencia", "Cuarta diferencia", "Quinta diferencia"], default_value="", enable_events=True, readonly=True, key='-COMBO|DIF2-', visible=False)],
        [sg.Text("Ingrese los valores verdaderos de las siguientes derivadas:", key="-TXT|VV-")],
        [sg.pin(sg.Text("f'(x)", key="-TXT|VV1-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV1-", size=(13, 1), visible=False)), sg.pin(sg.Text("f''(x)", key="-TXT|VV2-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV2-", size=(13, 1), visible=False)), sg.pin(sg.Text("f'''(x)", key="-TXT|VV3-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV3-", size=(13, 1), visible=False)), sg.pin(sg.Text("fᴵⱽ(x)", key="-TXT|VV4-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV4-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Función matemática: ', key="-LBL|FUNCION-", visible=False)), sg.pin(sg.Text('', key="-TXT|FUNCION-", visible=False))],
        [sg.pin(sg.Text('h: ', key="-TXT|PASO-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|PASO-", size=(13, 1), visible=False)), sg.pin(sg.Text('Valor inicial: ', key="-TXT|VALIN-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VALIN-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Xi', key="-TXT|X-", visible=False, pad=(1, 1))), sg.pin(sg.Input(enable_events=True, key="-IN|X1-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X2-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X3-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X4-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X5-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X6-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0)))],
        [sg.pin(sg.Text('Yi', key="-TXT|Y-", visible=False, pad=(1, 1))), sg.pin(sg.Input(enable_events=True, key="-IN|Y1-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y2-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y3-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y4-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y5-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y6-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0)))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    window = sg.Window('', main_layout)
    radio_keys = ('1', '2', '3', '4')
    orden = list()
    inputs = ["-IN|LVL-", "-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-", "-IN|Y2-",
            "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-IN|PASO-", "-IN|VALIN-", "-IN|VV1-", "-IN|VV2-", "-IN|VV3-", "-IN|VV4-"]

    while True:
        event, values = window.read()
        print(f"Evento: {event}")

        # Validando ingreso unicamente de numeros en inputs
        if event in inputs and len(values[event]) and values[event][-1] not in ('0123456789.-'):
            window[event].update(values[event][:-1])

        # Reiniciando componentes cuando se selecciona otro método
        if event == "-TABGROUP-":
            valores_verdaderos = []
            hide(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-'], window)
            window["-IN|VALIN-"].update(value="")
            window["-IN|PASO-"].update(value="")
            window["-TXT|FUNCION-"].update(value="")
            window["-COMBO|DATOS-"].update(value="")
            window["-COMBO|MTD-"].update(value="")
            window["-COMBO|DIF-"].update(value="")
            window["-COMBO|DIF2-"].update(value="")
            reset(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-",
                "-IN|Y1-", "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-"], window)
            hide(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-",
                "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-TXT|X-", "-TXT|Y-"], window)
            for i in radio_keys:
                uncheck(i, window, orden)
                window[f"-IN|VV{i}-"].update(value="")
                hide([f'-TXT|VV{i}-', f"-IN|VV{i}-"], window)

            if values["-TABGROUP-"] == '-TAB4-' or values["-TABGROUP-"] == '-TAB5-':
                hide(["2", "3", "4", "T2", "T3", "T4", "-TXT|MTD-",
                    "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], window)
                if values["-TABGROUP-"] == '-TAB5-':
                    hide(['-COMBO|DIF-'], window)
                    show(['-COMBO|DIF2-'], window)
                else:
                    hide(['-COMBO|DIF2-'], window)
                    show(['-COMBO|DIF-'], window)

            elif values["-TABGROUP-"] == '-TAB6-':
                hide(["2", "T2", "3", "T3", "4", "T4"], window)
                show(["-TXT|MTD-", "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], window)

            else:
                hide(["-TXT|MTD-", "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], window)
                show(["-TXT|ORDEN-", "1", "T1", "2", "T2", "3", "T3", "4", "T4"], window)

        # Eventos para los radiobuttom
        if event in radio_keys:
            if window[event].metadata:
                uncheck(event, window, orden)
                hide([f'-TXT|VV{event}-', f"-IN|VV{event}-"], window)
                window[f"-IN|VV{event}-"].update(value="")
            else:
                show([f'-TXT|VV{event}-', f"-IN|VV{event}-"], window)
                check(event, window, orden)

        # Añadiendo más opciones de diferencias para el método de 5 puntos

        if values['-COMBO|MTD-'] == '5 puntos':
            hide(['-COMBO|DIF-'], window)
            show(['-COMBO|DIF2-'], window)
        else:
            if values["-TABGROUP-"] == '-TAB5-':
                show(['-COMBO|DIF2-'], window)
            else:
                hide(['-COMBO|DIF2-'], window)
                show(['-COMBO|DIF-'], window)

        if event == "-COMBO|DIF-" and values["-COMBO|DATOS-"] == "Tabla de datos":

            reset(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-",
                "-IN|Y1-", "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-"], window)
            hide(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-",
                "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-TXT|X-", "-TXT|Y-"], window)
            orden_maximo = max([int(num) for num in orden])

            if values["-TABGROUP-"] == '-TAB1-' or values["-TABGROUP-"] == '-TAB2-':
                if values["-COMBO|DIF-"] == "Primera diferencia":
                    MAX_COL = orden_maximo + 1

                if values["-COMBO|DIF-"] == "Segunda diferencia":
                    MAX_COL = orden_maximo + 2

            if values["-TABGROUP-"] == '-TAB3-':

                if values["-COMBO|DIF-"] == "Primera diferencia":

                    if orden_maximo % 2 == 0:
                        MAX_COL = orden_maximo + 1

                    else:
                        MAX_COL = orden_maximo + 2

                if values["-COMBO|DIF-"] == "Segunda diferencia":

                    if orden_maximo <= 2:
                        MAX_COL = orden_maximo + (5 - orden_maximo)

                    else:
                        MAX_COL = orden_maximo + (6 - orden_maximo)

            if values["-TABGROUP-"] == '-TAB4-':

                if values["-COMBO|DIF-"] == "Primera diferencia":
                    MAX_COL = 3

                if values["-COMBO|DIF-"] == "Segunda diferencia":
                    MAX_COL = 3

            if values["-TABGROUP-"] == '-TAB5-':

                if values["-COMBO|DIF-"] == "Primera diferencia":
                    MAX_COL = 5

                if values["-COMBO|DIF-"] == "Segunda diferencia":
                    MAX_COL = 5

                if values["-COMBO|DIF-"] == "Tercera diferencia":
                    MAX_COL = 4

                if values["-COMBO|DIF-"] == "Cuarta diferencia":
                    MAX_COL = 5

                if values["-COMBO|DIF-"] == "Quinta diferencia":
                    MAX_COL = 5

            # Mostrando los inputs para ingreso de datos
            show(['-TXT|X-', '-TXT|Y-'], window)
            for i in range(MAX_COL):
                show([f'-IN|X{i+1}-', f'-IN|Y{i+1}-'], window)

        if event == "-COMBO|DATOS-":
            if values["-COMBO|DATOS-"] == "Función Matemática":
                hide(['-TXT|X-', '-TXT|Y-'], window)
                window['-TXT|FUNCION-'].update(showCalculator())
                show(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                    "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-'], window)
            else:
                hide(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                    "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-'], window)

        # Validad ingreso de todos los datos necesarios para reolver el problema
        if event == "-BTN|SOLVE-":
            valores_verdaderos = []
            orden.sort()
            h = []

            for i in orden:
                valores_verdaderos.append(float(window[f"-IN|VV{i}-"].get()))

            if values["-TABGROUP-"] == '-TAB1-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":
                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_hacia_atras(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, vv=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    print(
                        f"Orden: {orden}, Funcion: {window['-TXT|FUNCION-'].get()}, valor inicial: {values['-IN|VALIN-']}, Diferencia: {values['-COMBO|DIF-']}")

                    if len(orden) > 0 and window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_hacia_atras(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            if values["-TABGROUP-"] == '-TAB2-':
                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_hacia_adelante(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, vv=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if len(orden) > 0 and window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_hacia_adelante(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            if values["-TABGROUP-"] == '-TAB3-':
                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_centrada(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, vv=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if len(orden) > 0 and window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_centrada(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            if values["-TABGROUP-"] == '-TAB4-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":
                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_trespuntos(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, vv=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_trespuntos(paso=float(values['-IN|PASO-']), orden=1, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            if values["-TABGROUP-"] == '-TAB5-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_cincopuntos(paso=float(
                            h[0]), orden=1, diferencia=values['-COMBO|DIF2-'], yi=val_y, vv=valores_verdaderos)

                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    if window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF2-'] != "":
                        resultados, errores = diff_cincopuntos(paso=float(values['-IN|PASO-']), orden=1, diferencia=values['-COMBO|DIF2-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            if values["-TABGROUP-"] == '-TAB6-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_cincopuntos(paso=float(
                            h[0]), orden=1, diferencia=values['-COMBO|DIF2-'], yi=val_y, vv=valores_verdaderos)

                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    if window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and (values['-COMBO|DIF2-'] != "" or values['-COMBO|DIF-'] != ""):
                        resultado, error, errordiff, tabla = richardson(paso=float(values['-IN|PASO-']), orden=orden, metodo=values['-COMBO|MTD-'], nivel=int(
                            values['-IN|LVL-']), diferencia=values['-COMBO|DIF2-'], valor_inicial=float(values['-IN|VALIN-']), fx=window['-TXT|FUNCION-'].get(), vv=valores_verdaderos)

            texto = ""
            if values["-TABGROUP-"] != '-TAB6-':

                for i in range(max([int(num) for num in orden])):
                    texto += f"La {values['-COMBO|DIF-'].lower()} de orden {i+1} es igual a {round(resultados[i], 9)}\ny presenta un error del {round(errores[i],9)}%\n\n"

                sg.popup(f'Respuestas:\n\n{texto}', no_titlebar=True)

            else:

                for i in range(max([int(num) for num in orden])):
                    texto += f"La primera derivada por extrapolación de Ricahrdson por el método de {values['-COMBO|MTD-'].lower()} es igual a {round(resultado,9)}\nEl error de Ricahrdson es {round(error, 9)}%\nEl error del método {values['-COMBO|MTD-'].lower()} es {errordiff}\n\n"

                texto += "\n\nTabla:\n\n"
                a = np.array(tabla)
                a = a.T
                for line in a:
                    for i in line:
                        if i == "0.0":
                            texto += f"{i}"+" "*(11-len(str(i)))
                        else:
                            texto += f"{i}\t"
                    texto += "\n"
                sg.popup(f'Respuestas:\n\n{texto}', no_titlebar=True,
                    line_width=int(values['-IN|LVL-'])*19)

        if event == "Salir" or event == sg.WIN_CLOSED:
            break

    window.close()

Derivate()