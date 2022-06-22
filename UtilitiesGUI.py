import PySimpleGUI as sg
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


radio_unchecked = b'iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAEwElEQVR4nI1W3W9URRT/nZm7ZXdpbajdWpCAjcFEqw88+CACrgaBmFBIwI3fPPpPaJYND/wjYsxFYgwP+BV2kY9gNCIJIhEIBZSWLl3aprvde2fOOT7c3W27fNSTTO7cMzO/35wz55wZYAVRVVMuaxCGoV2qD8PQlsvlQFXNShhPAqduYEr0lrrmhmFoVbVbvWzdQxKGoS0UCgwAFy6PvySx27cQRVvY80YGZyHaIKJbPUHqvCF8k3/tlb+61z2RJAzVFgrE5QuX1q9K9x6Oouj9TCazKmUBawiAglkQO0bsPOqNejOw9qsoan62Z8eWfx9FRMsJkgnnfrv6FgXBUWOD4UzAWJsb8L3ZNFlrCQSwZ8TO6excXe/eux/UY0EcuQkXRx/t3fX6qW6iDomqGiKS87///QaM/Q7K6efXD7rBgf5AVcl7hgBQEYgqVAQEgqroZLXmb9yeTLGgKRztHtu5/XQbr0NSVDU4dAhvj703LGouBpaGXhwZ5v6nem0cO2gCB002AxGBiICZwSwIrEVtZpav3LhjneN76YxsvnDq1D0AKJVKYgBg9NgxKpVKIkpH0ulVQyPrBvxTfb02ih2ICESAdp2darJHIkIUx+jrXW03rB30PT09zzTm5UipVJLR0VECAGqb9csfV16oN3H56f60Hd20gZzzRJR4UzvAusySxBoBi8A5DyLolWvjOv1gjldnUqN7duavFYtFYyoVGACIvd2fzWZSw4P9IqKkLfBugu4GKFSSr4hSbqBfMplMaiFyBwAgn88bU60eUwCI43hbYIBsJk2e+bHAiQVL/xWiSTB4ZmQzabKG4B1vBYBqtapBoVBgVaUfz13aaI3CEBGzgAjouEuXg3bARSG6pImADJEhwLN/TlWJiDhoecOqSHYpUIJPHYclY4CqdBElZ6Otfse9otlKBRaAb5OwqjbaYSnatqKzpEXQAleFsIAlCWERBbfyR4TBwlDVRj4PBgAThqElIgVhPPaicew02R0vi6ClESWcALEkkbV0bhQ7dZ4VpONEpGEYWpPL5QgArLVnYsc0N99QAuC5nWy8JPEYvtW4PS6LfVXFfL2hznkyxv4MALlcjkwlnxcACCj4ul6fjyeqNeOZ1Xu/COoXwX0XkbDAs8B7BjPrVLVm6vVGDOXjAFCpVMSUiCQMQ/vmlpevE+nRyJOZul9jYwix84sEfrG1d94h9A5EQHW6xrEXYwhffFLYe/3dMLSlUkmS2lUsGgB4Nf/OEIleJEPDI88Ocl/vauu8b5UQdA69nS/t2mWIMDM3x+P/TFp2flKM3Tz+569T7dr1UBU+8dPZbWRS30M4s25ojVvT3xcIlNpRpCpd+cI6XZvxd6emUyrUEPW7DhbGzi6twp37mVpu27Nj65lmo7lbgDsT9+dSV2/cotqDWR/HMYt4ERHx7CWKIq7NzPrrN2/TVG0uBcVt56PdBwtjZ1sRKx3sruLaubiOnzy51tq+wy6KP0j19GSsAQwtlnrPjNgxmgvNBWvNl41m8/NPP94/seLN2E0EACd+qGxyse5runi7Zz+iLL2imLcGN1PWnhYNvv3wwM5r3ev+lzzqtdLSB926lV4rK0qxWDTlcvmx7652ZD5J/gNoDCDS80MCGwAAAABJRU5ErkJggg=='

radio_checked = b'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'


def hide(keys, window):

    for i in keys:
        window[i].update(visible=False)


def show(keys, window):

    for i in keys:
        window[i].update(visible=True)


def reset(keys, window):

    for i in keys:
        window[i].update(value="")

def update(keys, window, values):

    j = 0
    for i in keys:
        window[i].update(value= values[j])
        j += 1


def reset_radio(keys, window):

    for i in keys:
        window[i].update(source=radio_unchecked)


def uncheck(key, window, orden=None):

    if orden != None:
        if key in orden:
            orden.remove(key)

    window[key].update(radio_unchecked)
    window[key].metadata = False


def check(key, window, orden= None):

    if orden != None:
        orden.append(key)
        
    window[key].update(radio_checked)
    window[key].metadata = True


#Función encargada de mostrar un modal y generar una tabla dinámica para que el usuario ingrese los datos
def create_table(cols, rows, headings = None):
        sg.theme('DarkBlue3')

        if headings != None:
            
            #Definimos el diseño de la tabla con encabezados
            layout = [[sg.Button(heading, size=(10,1), button_color=('white', 'black'), disabled=True) for heading in headings], 
            [[sg.Input(justification='center', key=(r, c)) for c in range(cols)] for r in range(rows)],
            [[sg.Button('Ok')]]]
        
        else:
            ROW_LABELS = {
                1: "x",
                2: "y"
            }
            #Definimos el diseño de la tabla sin encabezados
            layout = [[[sg.Text(ROW_LABELS[r+1], size=(4, 1))] + [sg.Input(justification='center', key=(r, c)) for c in range(cols)] for r in range(rows)],
            [[sg.Button('Ok')]]]

        
        modal_table = sg.Window("", layout, default_element_size=(12, 1), element_padding=(1, 1), return_keyboard_events=True, no_titlebar=True)
        
        while True:
            event, values = modal_table.read()
            if event in (sg.WIN_CLOSED, 'Salir'):
                break
            
            if event == "Ok":
                break

        modal_table.close()

        #Retornamos en una matriz los datos que ingresó el usuario
        return [[values[(row, col)] for col in range(cols)] for row in range(rows)]



def clear_canvas(canvas,window, key):
    canvas.get_tk_widget().pack_forget()
    fig = plt.figure(figsize=(0,0))
    canvas = FigureCanvasTkAgg(fig, window[key].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    
#Función para graficar
def generate_grafic(metodo, xi, fi, window, key, canvas = None,expresion = None, valor_eval= None, result = None, raices = None, img_raices = None):

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')

    fig = plt.figure()
    ax = plt.axes()
    ax.set_title(metodo)
    if expresion == None:
        ax.plot(xi, fi, label= metodo)
    else:
        ax.plot(xi, fi, label= str(expresion))


    if raices != None: 
        #Los metodos axhline y axvline generan los ejes en forma de cruz
        ax.spines.left.set_position('zero')
        ax.spines.right.set_color('none')
        ax.spines.bottom.set_position('zero')
        ax.spines.top.set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')    
        for i in range(len(raices)):
            ax.plot(raices[i], img_raices[i], "r.", label= f"Raíz {i+1}: {raices[i]}")

    else:
        ax.plot(xi, fi, "r.", label="puntos")
        ax.grid()
        ax.set_xlabel('xi')
        ax.set_ylabel("f(xi)")
    
    if valor_eval != None:
        ax.plot(valor_eval,result,"g.", label="Valor evaluado")

    ax.legend()

    # create the form and show it without the plot
    # add the plot to the window
    try:
        canvas.get_tk_widget().pack_forget()
    except:
        pass
    figure_canvas_agg = FigureCanvasTkAgg(fig, window[key].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
    return figure_canvas_agg