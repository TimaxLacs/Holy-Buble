import PySimpleGUIWx as sg

# Функции и кнопки окон
layout = [[sg.Text('Вас приветствует мобильное приложение библиотеки!', size=(150, 50)), ],
          [sg.Button('Поиск книги', size=(10,50))],
          # [sg.Text('Enter something on Row 2'), sg.InputText()],  # InputText - небольшое окно для ввода текста
          [sg.Button('Закрыть приложение')],
#[sg.Button('')],
          [sg.Button('очко товарища')]]
# TODO доделать кнопки, понять как поставить местоположение текста и кнопок(выполняется

layout2 = [[sg.Radio(text='вкл', default=True, group_id='aa'),
            sg.Radio(text='выкл', group_id='aa')], [sg.Cancel()]]


def win1():  # Создаем и открываем доп окна
    win1 = sg.Window('Сеть', layout2, no_titlebar=True, grab_anywhere=True, size=(120, 500))
    while True:
        event, values = win1.read(timeout=200)  # Пауза обновления окна в мc  0,2 сек
        if event == 'Закрыть приложение':
            break
        if not event:  # Если нет событии
            break  # Закрыть окно
    win1.close()


def win2():  # Создаем и открываем доп окна
    layout1 = [[sg.Button("Win2")]]  # Кнопка Win2
    window = sg.Window("Win2", layout1)
    while True:
        event, values = window.read(timeout=200)
        if not event:
            break


net = True

sg.theme('Tan')  # Тема окна

layout0 = [[sg.Text('Hi!', key='key1')]]

# Создание окно без титулбара
window = sg.Window('Window Title', layout, location=(800, 600), no_titlebar=True, grab_anywhere=True,
                   size=(400, 600))  # Создается основное окно
# новое окно без титульного бара

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Закрыть приложение':  # При нажании кнопки Cancel, закрывает окно
        break
    if event == 'Ok':  # Если нажимаете кнопку OK
        print("chonibud")  # В cmd выводиться текст ок
        # window['sss'].update('dddd', text_color='Red')  # При нажатии кнопки Ok, текст "Какой-то текст" изменяется на
        # 'dddd' и краситься в красный
        # webbrowser.open_new('http://google.com/') Открытие сайта в браузере
    if event == 'ffggg':  # Если нажата кнопка 'ffggg' то появляется всплывающиеся окно с текстом 'нет инета'
        # sg.Popup('нет инета ', no_titlebar=True) всплывающее окно с текстом
        win1()

window.close()  # Закрыть окно
