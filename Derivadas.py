import PySimpleGUI as sg
import sympy as sp
import math
import numpy as np
from Calculadora import *
from UtilitiesGUI import *

def Derivate():

    def get_datos(col):
        val_x = [float(diff_window[f"-IN|X{x+1}-"].get()) for x in range(col)]
        val_y = [float(diff_window[f"-IN|Y{x+1}-"].get()) for x in range(col)]

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


    def richardson(valor_inicial, metodo, diferencia, paso, orden, nivel, fx=None):
        j = 0
        error = None
        errores = list()
        matriz = []

        for i in range(nivel):
            matriz.append([])
            
        px, variables = transform_fx(fx)

        if len(variables) > 1:
                
            sg.popup(f'ERROR', no_titlebar=True,
                line_width=50)
            return None, None, None, None

        else:
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
                    orden, h, diferencia, valor_inicial, fx)
                errores.append(round(float(error[0]), 9))
                matriz[0].append(round(float(respuesta[0]), 9))
                h = h/2
                
            #Resto de niveles
            for i in range(nivel - 1):
                k = i + 1
                for j in range(nivel - (i+1)):
                    D_k = (4**k * matriz[i][j+1] - matriz[i][j])/(4**k - 1)
                    matriz[i+1].append(round(D_k, 9))

            for i in matriz:
                if len(i) < nivel:
                    for j in range(nivel - len(i)):
                        i.append(0)

            error = math.fabs((sp.diff(px, x).subs(x,valor_inicial) - matriz[nivel - 1][0])/sp.diff(px, x).subs(x,valor_inicial)) * 100

            return matriz[nivel - 1][0], error, errores[0], matriz


    def diff_cincopuntos(orden, paso, diferencia, valor_inicial=None, fx=None, yi=None, valores_verdaderos = None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:
            
            px, variables = transform_fx(fx)

            if len(variables) > 1:
                
                sg.popup(f'ERROR', no_titlebar=True,
                    line_width=50)

            else: 

                if diferencia == "Primera diferencia":

                    DIFERENCIAS = {
                        "1": lambda valor: (-25*px.subs(variables[0],valor).evalf() + 48*px.subs(variables[0],valor + paso).evalf() - 36*px.subs(variables[0],valor + 2*paso).evalf() + 16*px.subs(variables[0],valor + 3*paso).evalf() - 3*px.subs(variables[0],valor + 4*paso).evalf())/(12*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                elif diferencia == "Segunda diferencia":

                    DIFERENCIAS = {
                        "1": lambda valor: (-3*px.subs(variables[0],valor - paso).evalf() - 10*px.subs(variables[0],valor).evalf() + 18*px.subs(variables[0],valor + paso).evalf() - 6*px.subs(variables[0],valor + 2*paso).evalf() + px.subs(variables[0],valor + 3*paso).evalf())/(12*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                elif diferencia == "Tercera diferencia":

                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(variables[0],valor - 2*paso).evalf() - 8*px.subs(variables[0],valor - paso).evalf() + 8*px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor + 2*paso).evalf())/(12*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                elif diferencia == "Cuarta diferencia":

                    DIFERENCIAS = {
                        "1": lambda valor: (4*px.subs(variables[0],valor - 3*paso).evalf() + 6*px.subs(variables[0],valor - 2*paso).evalf() - 8*px.subs(variables[0],valor - paso).evalf() + 34*px.subs(variables[0],valor).evalf() + 3*px.subs(variables[0],valor + paso).evalf() + 34*px.subs(variables[0],valor + 2*paso).evalf())/(12*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                else:

                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(x,valor - 4*paso).evalf() - 3*px.subs(x,valor - 3*paso).evalf() + 4*px.subs(x,valor - 2*paso).evalf() - 36*px.subs(x,valor - paso).evalf() + 25*px.subs(x,valor).evalf())/(12*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1

        else:

            val_y = yi
            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (-25*val_y[0] + 48*val_y[1] - 36*val_y[2] + 16*val_y[3] - 3*val_y[4])/(12*paso)
                }
                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

            elif diferencia == "Segunda diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (-3*val_y[0] - 10*val_y[1] + 18*val_y[2] - 6*val_y[3] + val_y[4])/(12*paso)
                }
                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

            elif diferencia == "Tercera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[0] - 8*val_y[1] + 8*val_y[2] - val_y[3])/(12*paso)
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

            elif diferencia == "Cuarta diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (4*val_y[0] + 6*val_y[2] - 8*val_y[1] + 34*val_y[0] + 3*val_y[1] + 34*val_y[2])/(12*paso)
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

            else:

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[0] - 3*val_y[1] + 4*val_y[2] - 36*val_y[3] + 25*val_y[4])/(12*paso)
                }

                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_trespuntos(orden, paso, diferencia, valor_inicial=None, fx=None, yi=None, valores_verdaderos = None):
        resultados = list()
        errores = list()
        j = 0
        if fx != None:
            px, variables = transform_fx(fx)

            if len(variables) > 1:
                
                sg.popup(f'ERROR', no_titlebar=True,
                    line_width=50)

            else: 
                if diferencia == "Primera diferencia":

                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor - paso).evalf())/(2*paso)
                    }
                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                else:
                    DIFERENCIAS = {
                        "1": lambda valor: (-3*px.subs(variables[0],valor).evalf() + 4*px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor + 2*paso).evalf())/(2*paso)
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1
        else:
            val_y = yi
            if diferencia == "Primera diferencia":

                DIFERENCIAS = {
                    "1": lambda paso: (val_y[2] - val_y[0])/(2*paso)
                }
                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1
            else:

                DIFERENCIAS = {
                    "1": lambda paso: (-3*val_y[0] + 4*val_y[1] - val_y[2])/(2*paso)
                }
                for i in orden:
                    resultados.append(DIFERENCIAS[str(i)](paso))
                    errores.append(
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_centrada(orden, paso, diferencia, valor_inicial=None, fx=None, yi=None, valores_verdaderos = None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:

            px, variables = transform_fx(fx)

            if len(variables) > 1:
                
                sg.popup(f'ERROR', no_titlebar=True,
                    line_width=50)

            else: 

                if diferencia == "Primera diferencia":
                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor - paso).evalf())/(2*paso),
                        "2": lambda valor: (px.subs(variables[0],valor + paso).evalf() - 2*px.subs(variables[0],valor).evalf() + px.subs(variables[0],valor - paso).evalf())/paso**2,
                        "3": lambda valor: (px.subs(variables[0],valor + 2*paso).evalf() - 2*px.subs(variables[0],valor + paso).evalf() + 2*px.subs(variables[0],valor - paso).evalf() - px.subs(variables[0],valor - 2*paso).evalf())/(2*paso**3),
                        "4": lambda valor: (px.subs(variables[0],valor + 2*paso).evalf() - 4*px.subs(variables[0],valor + paso).evalf() + 6*px.subs(variables[0],valor).evalf() - 4*px.subs(variables[0],valor - paso).evalf() + px.subs(variables[0],valor - 2*paso).evalf())/paso**4
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                else:
                    DIFERENCIAS = {
                        "1": lambda valor: (-px.subs(variables[0],valor + 2*paso).evalf() + 8*px.subs(variables[0],valor + paso).evalf() - 8*px.subs(variables[0],valor - paso).evalf() + px.subs(variables[0],valor - 2*paso).evalf())/(12*paso),
                        "2": lambda valor: (-px.subs(variables[0],valor + 2*paso).evalf() + 16*px.subs(variables[0],valor + paso).evalf() - 30*px.subs(variables[0],valor).evalf() + 16*px.subs(variables[0],valor - paso).evalf() - px.subs(variables[0],valor - 2*paso).evalf())/(12*paso**2),
                        "3": lambda valor: (-px.subs(variables[0],valor + 3*paso).evalf() + 8*px.subs(variables[0],valor + 2*paso).evalf() - 13*px.subs(variables[0],valor + paso).evalf() + 13*px.subs(variables[0],valor - paso).evalf() - 8*px.subs(variables[0],valor - 2*paso).evalf() + px.subs(variables[0],valor - 3*paso).evalf())/(8*paso**3),
                        "4": lambda valor: (-px.subs(variables[0],valor + 3*paso).evalf() + 12*px.subs(variables[0],valor + 2*paso).evalf() - 39*px.subs(variables[0],valor + paso).evalf() + 56*px.subs(variables[0],valor).evalf() - 39*px.subs(variables[0],valor - paso).evalf() + 12*px.subs(variables[0],valor - 2*paso).evalf() - px.subs(variables[0],valor - 3*paso).evalf())/(6*paso**4)
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1


        return resultados, errores


    def diff_hacia_adelante(orden, paso, diferencia, valor_inicial=None, fx=None, yi=None, valores_verdaderos = None):
        resultados = list()
        errores = list()
        j = 0
        if fx != None:
            px, variables = transform_fx(fx)

            if len(variables) > 1:
                
                sg.popup(f'ERROR', no_titlebar=True,
                    line_width=50)

            else:

                if diferencia == "Primera diferencia":
                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor).evalf())/paso,
                        "2": lambda valor: (px.subs(variables[0],valor + 2*paso).evalf() - 2*px.subs(variables[0],valor + paso).evalf() + px.subs(variables[0],valor).evalf())/paso**2,
                        "3": lambda valor: (px.subs(variables[0],valor + 3*paso).evalf() - 3*px.subs(variables[0],valor + 2*paso).evalf() + 3*px.subs(variables[0],valor + paso).evalf() - px.subs(variables[0],valor).evalf())/(2*paso**3),
                        "4": lambda valor: (px.subs(variables[0],valor + 4*paso).evalf() - 4*px.subs(variables[0],valor + 3*paso).evalf() + 6*px.subs(variables[0],valor + 2*paso).evalf() - 4*px.subs(variables[0],valor + paso).evalf() + px.subs(variables[0],valor).evalf())/paso**4
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                else:
                    DIFERENCIAS = {
                        "1": lambda valor: (-px.subs(variables[0],valor + 2*paso).evalf() + 4*px.subs(variables[0],valor + paso).evalf() - 3*px.subs(variables[0],valor).evalf())/(2*paso),
                        "2": lambda valor: (-px.subs(variables[0],valor + 3*paso).evalf() + 4*px.subs(variables[0],valor + 2*paso).evalf() - 5*px.subs(variables[0],valor + paso).evalf() + 2*px.subs(variables[0],valor).evalf())/paso**2,
                        "3": lambda valor: (-3*px.subs(variables[0],valor + 4*paso).evalf() + 14*px.subs(variables[0],valor + 3*paso).evalf() - 24*px.subs(variables[0],valor + 2*paso).evalf() + 18*px.subs(variables[0],valor + paso).evalf() - 5*px.subs(variables[0],valor).evalf())/(2*paso**3),
                        "4": lambda valor: (-2*px.subs(variables[0],valor + 5*paso).evalf() + 11*px.subs(variables[0],valor + 4*paso).evalf() - 24*px.subs(variables[0],valor + 3*paso).evalf() + 26*px.subs(variables[0],valor + 2*paso).evalf() - 14*px.subs(variables[0],valor + paso).evalf() + 3*px.subs(variables[0],valor).evalf())/paso**4
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i+1).subs(variables[0],valor_inicial)) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
                    j += 1

        return resultados, errores


    def diff_hacia_atras(orden, paso, diferencia, valor_inicial=None, fx=None, yi=None, valores_verdaderos = None):
        j = 0
        resultados = list()
        errores = list()
        if fx != None:

            px, variables = transform_fx(fx)
            if len(variables) > 1:
                
                sg.popup(f'ERROR', no_titlebar=True,
                    line_width=50)

            else:
                if diferencia == "Primera diferencia":
                    DIFERENCIAS = {
                        "1": lambda valor: (px.subs(variables[0],valor).evalf() - px.subs(variables[0],valor - paso).evalf())/paso,
                        "2": lambda valor: (px.subs(variables[0],valor).evalf() - 2*px.subs(variables[0],valor - paso).evalf() + px.subs(variables[0],valor - 2*paso).evalf())/paso**2,
                        "3": lambda valor: (px.subs(variables[0],valor).evalf() - 3*px.subs(variables[0],valor - paso).evalf() + 3*px.subs(variables[0],valor - 2*paso).evalf() - px.subs(variables[0],valor - 3*paso).evalf())/(2*paso**3),
                        "4": lambda valor: (px.subs(variables[0],valor).evalf() - 4*px.subs(variables[0],valor - paso).evalf() + 6*px.subs(variables[0],valor - 2*paso).evalf() - 4*px.subs(variables[0],valor -3*paso).evalf() + px.subs(variables[0],valor - 4*paso).evalf())/paso**4
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
                        j += 1

                else:
                    DIFERENCIAS = {
                        "1": lambda valor: (3*px.subs(variables[0],valor).evalf() - 4*px.subs(variables[0],valor - paso).evalf() + px.subs(variables[0],valor - 2*paso).evalf())/(2*paso),
                        "2": lambda valor: (2*px.subs(variables[0],valor).evalf() - 5*px.subs(variables[0],valor - paso).evalf() + 4*px.subs(variables[0],valor - 2*paso).evalf() - px.subs(variables[0],valor - 3*paso).evalf())/paso**2,
                        "3": lambda valor: (5*px.subs(variables[0],valor).evalf() - 18*px.subs(variables[0],valor - paso).evalf() + 24*px.subs(variables[0],valor - 2*paso).evalf() - 14*px.subs(variables[0],valor - 3*paso).evalf() + 3*px.subs(variables[0],valor - 4*paso).evalf())/(2*paso**3),
                        "4": lambda valor: (3*px.subs(variables[0],valor).evalf() - 14*px.subs(variables[0],valor - paso).evalf() + 26*px.subs(variables[0],valor - 2*paso).evalf() - 24*px.subs(variables[0],valor - 3*paso).evalf() + 11*px.subs(variables[0],valor - 4*paso).evalf() - 2*px.subs(variables[0],valor - 5*paso).evalf())/paso**4
                    }

                    for i in orden:
                        resultados.append(DIFERENCIAS[str(i)](valor_inicial))
                        errores.append(
                            math.fabs((sp.diff(px, variables[0], i).subs(variables[0],valor_inicial) - DIFERENCIAS[str(i)](valor_inicial))/sp.diff(px, variables[0], i).subs(variables[0],valor_inicial)) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
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
                        math.fabs((valores_verdaderos[j] - DIFERENCIAS[str(i)](paso))/valores_verdaderos[j]) * 100)
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
        [sg.Text("Ingrese los valores verdaderos de las siguientes derivadas:", key="-TXT|VV-", visible=False)],
        [sg.pin(sg.Text("f'(x)", key="-TXT|VV1-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV1-", size=(13, 1), visible=False)), sg.pin(sg.Text("f''(x)", key="-TXT|VV2-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV2-", size=(13, 1), visible=False)), sg.pin(sg.Text("f'''(x)", key="-TXT|VV3-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV3-", size=(13, 1), visible=False)), sg.pin(sg.Text("fᴵⱽ(x)", key="-TXT|VV4-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VV4-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Función matemática: ', key="-LBL|FUNCION-", visible=False)), sg.pin(sg.Text('', key="-TXT|FUNCION-", visible=False))],
        [sg.pin(sg.Text('h: ', key="-TXT|PASO-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|PASO-", size=(13, 1), visible=False)), sg.pin(sg.Text('Valor inicial: ', key="-TXT|VALIN-", visible=False)), sg.pin(sg.Input(enable_events=True, key="-IN|VALIN-", size=(13, 1), visible=False))],
        [sg.pin(sg.Text('Xi', key="-TXT|X-", visible=False, pad=(1, 1))), sg.pin(sg.Input(enable_events=True, key="-IN|X1-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X2-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X3-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X4-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X5-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|X6-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0)))],
        [sg.pin(sg.Text('Yi', key="-TXT|Y-", visible=False, pad=(1, 1))), sg.pin(sg.Input(enable_events=True, key="-IN|Y1-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y2-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y3-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y4-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y5-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0))), sg.pin(sg.Input(enable_events=True, key="-IN|Y6-", size=(13, 1), visible=False, justification="center", border_width=3, pad=(0, 0)))],
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-")]
    ]

    # Iniciamos la ventana
    diff_window = sg.Window('', main_layout, no_titlebar=True, margins=(0,0))
    radio_keys = ('1', '2', '3', '4')
    orden = list()
    inputs = ["-IN|LVL-", "-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-", "-IN|Y2-",
            "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-IN|PASO-", "-IN|VALIN-", "-IN|VV1-", "-IN|VV2-", "-IN|VV3-", "-IN|VV4-"]

    while True:
        event, values = diff_window.read()
        print(f"Evento: {event}")

        # Validando ingreso unicamente de numeros en inputs
        if event in inputs and len(values[event]) and values[event][-1] not in ('0123456789.-'):
            diff_window[event].update(values[event][:-1])

        # Reiniciando componentes cuando se selecciona otro método
        if event == "-TABGROUP-":
            orden.clear()
            valores_verdaderos = []
            hide(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-',"-TXT|VV-"], diff_window)
            diff_window["-IN|VALIN-"].update(value="")
            diff_window["-IN|PASO-"].update(value="")
            diff_window["-TXT|FUNCION-"].update(value="")
            diff_window["-COMBO|DATOS-"].update(value="")
            diff_window["-COMBO|MTD-"].update(value="")
            diff_window["-COMBO|DIF-"].update(value="")
            diff_window["-COMBO|DIF2-"].update(value="")
            reset(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-",
                "-IN|Y1-", "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-"], diff_window)
            hide(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-",
                "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-TXT|X-", "-TXT|Y-"], diff_window)
            for i in radio_keys:
                uncheck(i, diff_window, orden)
                diff_window[f"-IN|VV{i}-"].update(value="")
                hide([f'-TXT|VV{i}-', f"-IN|VV{i}-"], diff_window)

            if values["-TABGROUP-"] == '-TAB4-' or values["-TABGROUP-"] == '-TAB5-':
                hide(["2", "3", "4", "T2", "T3", "T4", "-TXT|MTD-",
                    "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], diff_window)
                if values["-TABGROUP-"] == '-TAB5-':
                    hide(['-COMBO|DIF-'], diff_window)
                    show(['-COMBO|DIF2-'], diff_window)
                else:
                    hide(['-COMBO|DIF2-'], diff_window)
                    show(['-COMBO|DIF-'], diff_window)

            elif values["-TABGROUP-"] == '-TAB6-':
                hide(["2", "T2", "3", "T3", "4", "T4"], diff_window)
                show(["-TXT|MTD-", "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], diff_window)

            else:
                hide(["-TXT|MTD-", "-COMBO|MTD-", "-TXT|LVL-", "-IN|LVL-"], diff_window)
                show(["-TXT|ORDEN-", "1", "T1", "2", "T2", "3", "T3", "4", "T4"], diff_window)

        # Eventos para los radiobuttom
        if event in radio_keys:
            if diff_window[event].metadata:
                uncheck(event, diff_window, orden)
                diff_window[f"-IN|VV{event}-"].update(value="")
            else:
                check(event, diff_window, orden)
        
        # Añadiendo más opciones de diferencias para el método de 5 puntos
        if values['-COMBO|MTD-'] == '5 puntos':
            hide(['-COMBO|DIF-'], diff_window)
            show(['-COMBO|DIF2-'], diff_window)
        else:
            if values["-TABGROUP-"] == '-TAB5-':
                show(['-COMBO|DIF2-'], diff_window)
            else:
                hide(['-COMBO|DIF2-'], diff_window)
                show(['-COMBO|DIF-'], diff_window)


        if values["-TABGROUP-"] == '-TAB6-':
            diff_window['-COMBO|DATOS-'].update(values=["Función Matemática"])
        else:
            diff_window['-COMBO|DATOS-'].update(values=["Función Matemática","Tabla de datos"])

        if event == "-COMBO|DIF-" and values["-COMBO|DATOS-"] == "Tabla de datos":
            reset(["-IN|VV1-", "-IN|VV2-", "-IN|VV3-", "-IN|VV4-"], diff_window)
            show(["-TXT|VV-"], diff_window)
            for i in radio_keys:
                if diff_window[i].metadata:
                    show([f'-TXT|VV{i}-', f"-IN|VV{i}-"], diff_window)

            reset(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-",
                "-IN|Y1-", "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-"], diff_window)
            hide(["-IN|X1-", "-IN|X2-", "-IN|X3-", "-IN|X4-", "-IN|X5-", "-IN|X6-", "-IN|Y1-",
                "-IN|Y2-", "-IN|Y3-", "-IN|Y4-", "-IN|Y5-", "-IN|Y6-", "-TXT|X-", "-TXT|Y-"], diff_window)
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
            show(['-TXT|X-', '-TXT|Y-'], diff_window)
            for i in range(MAX_COL):
                show([f'-IN|X{i+1}-', f'-IN|Y{i+1}-'], diff_window)
        else:
            hide(["-TXT|VV-"], diff_window)

        if event == "-COMBO|DATOS-":
            if values["-COMBO|DATOS-"] == "Función Matemática":
                hide(['-TXT|X-', '-TXT|Y-'], diff_window)
                diff_window['-TXT|FUNCION-'].update(showCalculator())
                show(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                    "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-'], diff_window)
            else:
                hide(['-LBL|FUNCION-', '-TXT|FUNCION-', "-TXT|PASO-",
                    "-IN|PASO-", '-TXT|VALIN-', '-IN|VALIN-'], diff_window)

        # Validad ingreso de todos los datos necesarios para reolver el problema
        if event == "-BTN|SOLVE-":
            valores_verdaderos = []
            orden = [int(num) for num in orden]
            orden.sort()
            h = []

            if values["-COMBO|DATOS-"] == "Tabla de datos":
                #Obteniendo todos los valores verdaderos ingresados
                for i in orden:
                    valores_verdaderos.append(float(diff_window[f"-IN|VV{i}-"].get()))

            if values["-TABGROUP-"] == '-TAB1-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":
                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_hacia_atras(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, valores_verdaderos=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    print(
                        f"Orden: {orden}, Funcion: {diff_window['-TXT|FUNCION-'].get()}, valor inicial: {values['-IN|VALIN-']}, Diferencia: {values['-COMBO|DIF-']}")

                    if len(orden) > 0 and diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_hacia_atras(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            if values["-TABGROUP-"] == '-TAB2-':
                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_hacia_adelante(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, valores_verdaderos=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if len(orden) > 0 and diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_hacia_adelante(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            if values["-TABGROUP-"] == '-TAB3-':
                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_centrada(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, valores_verdaderos= valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if len(orden) > 0 and diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_centrada(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            if values["-TABGROUP-"] == '-TAB4-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":
                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_trespuntos(paso=float(
                            h[0]), orden=orden, diferencia=values['-COMBO|DIF-'], yi=val_y, valores_verdaderos=valores_verdaderos)
                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":

                    if diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF-'] != "":
                        resultados, errores = diff_trespuntos(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            if values["-TABGROUP-"] == '-TAB5-':

                if values["-COMBO|DATOS-"] == "Tabla de datos":

                    val_x, val_y = get_datos(MAX_COL)
                    h = fill_paso(val_x)

                    # comprobando que el valor de h sea uniforme
                    if comprobar_salto(h):
                        resultados, errores = diff_cincopuntos(paso=float(
                            h[0]), orden=1, diferencia=values['-COMBO|DIF2-'], yi=val_y, valores_verdaderos= valores_verdaderos)

                    else:
                        print(
                            "Los valores de X deben tener todos la misma distancia entre cada valor")

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    if diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and values['-COMBO|DIF2-'] != "":
                        resultados, errores = diff_cincopuntos(paso=float(values['-IN|PASO-']), orden=orden, diferencia=values['-COMBO|DIF2-'], valor_inicial=float(
                            values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            if values["-TABGROUP-"] == '-TAB6-':

                if values["-COMBO|DATOS-"] == "Función Matemática":
                    if diff_window['-TXT|FUNCION-'].get() != "" and values['-IN|VALIN-'] != "" and (values['-COMBO|DIF2-'] != "" or values['-COMBO|DIF-'] != ""):
                        resultado, error, errordiff, tabla = richardson(paso=float(values['-IN|PASO-']), orden=orden, metodo=values['-COMBO|MTD-'], nivel=int(
                            values['-IN|LVL-']), diferencia=values['-COMBO|DIF2-'], valor_inicial=float(values['-IN|VALIN-']), fx=diff_window['-TXT|FUNCION-'].get())

            texto = ""
            if values["-TABGROUP-"] != '-TAB6-':
                if len(resultados) != 0:
                    for i in range(len(orden)):
                        texto += f"La {values['-COMBO|DIF-'].lower()} de orden {orden[i]} es igual a {round(resultados[i], 9)}\ny presenta un error del {round(errores[i],9)}%\n\n"

                    sg.popup(f'Respuestas:\n\n{texto}', no_titlebar=True)

            else:

                if resultado != None:

                    for i in range(len(orden)):
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

    diff_window.close()
