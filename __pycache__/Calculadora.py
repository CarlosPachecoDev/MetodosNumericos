import PySimpleGUI as sg
import re
import sympy as sp
import math

# Calculadora para el ingreso de funciones

def rmve_2nd_grp(b):
    return b.group(1)

def transform_fx(fx):
        x = sp.Symbol("x")

        SYMBOLS = {
            "×": "*",
            "÷": "/",
            "℮": str(math.e),
            "π": str(math.pi),
            "^": "**",
            "√": "sqrt"
        }
        for key, value in SYMBOLS.items():
            if key in fx:
                """if "√" == key:
                    m = re.search(r'√\(.*\)', fx)
                    exchange = m.group().replace(key, "")+value
                    fx = fx.replace(m.group(), exchange)
                    continue"""
                fx = fx.replace(key, value)

        if 'cot' in fx:
            fx = fx.replace('cot', "1/tan")

        if 'sec' in fx:
            fx = fx.replace('sec', '1/cos')

        if 'csc' in fx:
            fx = fx.replace('csc', '1/sin')

        if 'logₑ' in fx:
            fx = fx.replace("logₑ", "log")

        if 'log₁₀' in fx:
            fx = fx.replace('log₁₀', 'log10')

        print(fx)
        return sp.lambdify(x, fx, modules=["math", "mpmath", "sympy"])

def showCalculator():

    theme_dict = {
        'BACKGROUND': '#2B475D',
        'TEXT': '#FFFFFF',
        'INPUT': '#F2EFE8',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#F2EFE8',
        'BUTTON': ('#000000', '#C2D4D8'),
        'PROGRESS': ('#FFFFFF', '#C7D5E0'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
    }

    sg.theme_add_new('Dashboard', theme_dict)
    sg.theme('Dashboard')

    BORDER_COLOR = '#C7D5E0'

    top = [[sg.Input('', size=(30, 1), key='input', expand_x=True)]]

    panel1 = [
        [sg.Button('7'), sg.Button('8'), sg.Button('9'), sg.Button('÷')],
        [sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('×')],
        [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('-')],
        [sg.Button('0'), sg.Button('.'), sg.Button('='), sg.Button('+')],
        [sg.Button('Submit'), sg.Button('Clear'), sg.Button('Del')]
    ]

    panel2 = [
        [sg.Button('('), sg.Button(')'), sg.Button('^'), sg.Button('√')],
        [sg.Button('π'), sg.Button('℮'), sg.Button('y'), sg.Button('x')],
        [sg.Button('z'), sg.Button('sin'), sg.Button('cos'), sg.Button('tan')],
        [sg.Button('cot'), sg.Button('sec'), sg.Button('csc'), sg.Button('arcsec')],
        [sg.Button('arccsc'), sg.Button('arcsin'), sg.Button('arccos'), sg.Button('arctan')],
        [sg.Button('arccot'), sg.Button('logₑ'), sg.Button('log₁₀')]
    ]

    layout = [
        [sg.Frame('', top, expand_x=True,  relief=sg.RELIEF_GROOVE)],
        [sg.Frame('', [[sg.Frame('', panel1, border_width=0)]]), sg.Column(panel2)],
        [sg.Sizegrip(background_color=BORDER_COLOR)]
    ]

    calculadora = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0), background_color=BORDER_COLOR, default_button_element_size=(5, 2), auto_size_buttons=False, grab_anywhere=False, no_titlebar=True)

    display_calculator = ''

    while True:

        event, values = calculadora.read()

        if event == 'Clear':
            display_calculator = ''

        elif event == 'Submit':
            calculadora.close()
            print(display_calculator)
            return display_calculator

        elif event == 'Del':
            display_calculator = re.sub("(.*)(.{1}$)", rmve_2nd_grp, display_calculator)

        else:
            display_calculator = values['input']
            display_calculator += event

        calculadora['input'].update(display_calculator)
