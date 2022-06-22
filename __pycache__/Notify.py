import PySimpleGUI as sg


def notify(msg):
    sg.theme('Topanga')
    layout = [
        [sg.Text(msg)],
        [sg.Button('Ok')]
        ]

    window_notify = sg.Window('', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True,finalize=True)

    event, values = window_notify.read()

    window_notify.close()