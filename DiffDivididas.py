
from UtilitiesGUI import *
import pandas as pd
import numpy as np

def show_respuesta(df, respuesta = ""):

    #Definimos y generamos dinámicamente los encabezados de la tabla de diferencias divididas
    header_list = list()
    data = df.to_numpy().tolist()
    print(data)
    n = len(data[0])-1
    header_list.append("X")
    header_list.append("f(x)")
    header_list.extend([f"{i+1}" for i in range(n-1)])

    #Definimos el layout del modal de respuestas
    layout = [
        [sg.Table(values=data, headings=header_list, justification="center", def_col_width= 12, pad=((10, 10), (10, 10)) )],
        [sg.Text(respuesta)],
        [sg.Button("Ok")]
    ]


    modal_respuestas = sg.Window('', layout, grab_anywhere=False, no_titlebar=True)
    event, values = modal_respuestas.read()
    modal_respuestas.close()

#llenar las columnas de x y f(x) en la tabla de diferencias divididas
def llenarprimerasdoscolumnas(xi,y,matriz):
    matriz.T[0]=xi
    matriz.T[1]=y

    return matriz

def diferencias(datos):
    xi = [float(number) for number in datos[0]]
    y = [float(number) for number in datos[1]]
    n = len(xi)
    b = list()
    columnas = ["X", "f(x)"]
    #Dimensionar dinamicamente la matriz
    matriz = np.array([[0]*(n+1)]*(n),dtype=float)
    
    matriz = llenarprimerasdoscolumnas(xi,y,matriz)
    b.append(y[0])
    for i in range(n-1):
        new_col = [0]*(i+1)
        for j in range(n-(i+1)):
            new_col.append(round((matriz[j+(i+1)][i+1]-matriz[j+i][i+1])/(matriz[j+(i+1)][0]-matriz[j][0]),9))
        b.append(new_col[i+1])    
        matriz[:,(i+2)] = new_col
        columnas.append(f"{i+1}")
    df = pd.DataFrame(matriz, columns=columnas)
    return df, b

def solve_diff_divididas():

    # MainLayout
    salida = "Lorem ipsum dolor sit amet, consectetuer adipiscing\nelit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus \net magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, \nfringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate \neleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. \nEtiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,\nquis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam \naccumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; \nIn ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, \nimperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, \nconsectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis vestibulum. Nullam nulla eros, ultricies sit amet, nonummy id, imperdiet feugiat, pede. Sed lectus. Donec mollis hendrerit risus. Phasellus nec sem in justo pellentesque facilisis. Etiam imperdiet imperdiet orci. Nunc nec neque. Phasellus leo dolor, tempus non, auctor et, hendrerit quis, nisi. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed aliquam, nisi quis porttitor congue, elit erat euismod orci, ac"
    main_layout = [
        [sg.pin(sg.Text("Cantidad de pares (x,y):", key="-TXT|VX-")), sg.pin(sg.Input(enable_events=True, key="-IN|VX-", size=(10, 1))), sg.pin(sg.Button('Llenar tabla',key="-BTN|FILL-", visible=False))], 
        [sg.Button('Salir'), sg.Button('Resolver', key="-BTN|SOLVE-", visible=False)]
    ]

    diff_divididas_window = sg.Window("", main_layout)

    while True:
        event, values = diff_divididas_window.read()

        if event == "-IN|VX-" and len(values[event]) and values[event][-1] not in ('1234567890'):
            diff_divididas_window[event].update(values[event][:-1])

        if values["-IN|VX-"] != "":
            show(["-BTN|FILL-"], diff_divididas_window)
        else:
            hide(["-BTN|FILL-"], diff_divididas_window)

        if event == "-BTN|FILL-":
            datos = create_table(cols=int(values["-IN|VX-"]),rows=2)
            show(["-BTN|SOLVE-"], diff_divididas_window)
        else:
            hide(["-BTN|SOLVE-"], diff_divididas_window)

        if event == "-BTN|SOLVE-":
            df, b = diferencias(datos)
            show_respuesta(df)

        if event == "Salir":
            break
    diff_divididas_window.close()       

