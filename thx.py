# import PySimpleGUI as sg
import webbrowser
import PySimpleGUIWeb as sg
import PySimpleGUIWx as sg


# def win1():
# win2 = sg.Window('Сеть', layout2, no_titlebar=True) # Создается новое окно без титульного бара
# while True:
# event, values = win2.read(timeout=200) #
#  if not event:
#  break

def win2():
    layout1 = [[sg.Button("Win2")]]
    window = sg.Window("Win2", layout1)
    while True:
        event, values = window.read(timeout=200)
        if not event:
            break


net = True

sg.theme('Tan')  # Тема окна

layout0 = [[sg.Text('Hi!', key='key1')]]

layout = [[sg.Text('Some text on Row 1', key='sss')],
          [sg.Text('Enter something on Row 2'), sg.InputText()],
          [sg.Button('Ok', size=(10, 2)), sg.Button('Cancel')],
          [sg.Button('ffggg')]]

layout2 = [[sg.Radio(text='вкл', default=True, group_id='aa'), sg.Radio(text='выкл', group_id='aa')]]

# Создание окно без титулбара
window = sg.Window('Window Title', layout, location=(800, 600), no_titlebar=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:

    event, values = window.read()
    if not net:
        window['key1'].update('нет сооооол')
    if event == sg.WIN_CLOSED or event == 'Cancel':  # При нажании кнопки Cancel, закрывает окно
        break
    if event == 'Ok':
        print('chonibud')
        window['sss'].update('dddd', text_color='Red')
        webbrowser.open_new('http://google.com/')
    if event == 'ffggg':
        sg.Popup('нет инета ', no_titlebar=True)

window.close()
