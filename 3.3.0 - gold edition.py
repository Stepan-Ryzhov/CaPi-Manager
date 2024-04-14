# -*- coding: utf-8 -*-
import threading
import time
import customtkinter
import os
import ctypes
import psutil
import gc
import platform
import base64
import shutil
import hashlib
import yadisk
import datetime
import logging
import subprocess
import speedtest
import requests
from PIL import Image
from pathlib import Path


# Функция изменения темы приложения
def custom(app_theme):
    customtkinter.set_appearance_mode(app_theme)
    logging.info(">>> Тема приложения была изменена. День: %s; Точная дата и время запуска: %s",
                 current_weekday,
                 now_dt.strftime(date_format))

# Настройки по умолчанию
customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme("dark-blue")


# Класс отвечающий за работу приложения
class GUI(customtkinter.CTk):
    # Конструктор класса, в котором объявляются настройки отрисовки приложения
    def __init__(self,):
        self.new_signatures = False
        self.deleted_files = []
        super().__init__()
        self.init_start_GUI()
        self.title("CaPi Manager")
        self.geometry(f"{605}x{400}")
        self.resizable(False, False)
        # Здесь происходит проверка активности к серверу для обновления сигнатур
        try:
            self.server_sign = ''
            response = requests.get('https://raw.githubusercontent.com/Stepan-Ryzhov/CaPi-Manager/'
                                    'main/test_server_capi.txt')

            b = response.text.split('\n')
            print(b)
            if b == ['[]'] or b == '' or b == [] or b == [''] or b == ['\r'] or b == ['404: Not Found'] or b == ['', '']:
                logging.warning(">>> Новые сигнатуры не найдены на GitHub. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))
            else:
                self.server_sign = b
                logging.info(">>> Программа подключилась к серверу. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
        except Exception as e:
            logging.exception(e)
            logging.error(">>> Сервер отключен. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))
        self.init_start_GUI()

    # Метод начальной отрисовки
    def init_start_GUI(self):
        self.th = 'Светлая'
        self.rh = 1
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting,
                                                        fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.sidebar_button_1.place(x=30, y=20)

        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value='Светлая')
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Светлая", "Темная"],
                                                  command=self.combobox_callback2,  variable=self.combobox_var)

        self.combobox.place(x=30, y=300)
        self.image_path = 'image/Capi_gold_light.jpg'
        self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
        self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='', )
        self.ico_label.place(x=250, y=50)
        self.vers_label_font = customtkinter.CTkFont('Monotype Corsiva', size=24, weight='bold')
        self.vers_label = customtkinter.CTkLabel(self.sidebar_frame, text='GOLD EDITION', font=self.vers_label_font,
                                                 text_color='#CCCC00')
        self.vers_label.place(x=15, y=340)
        logging.info(">>> Первая отрисовка боковой панели. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Метод повторной отрисовки начального экрана
    def init_GUI(self):
        self.stop_scan = True
        self.activity_potok = False
        try:
            self.stroka_sostoyaniya.place_forget() or self.file_damage_label_start.place_forget()
            self.stroka_sostoyaniya2.place_forget() 
        except Exception:
            pass
        self.rh = self.rh
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting,
                                                        fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean,
                                                        fg_color='gold', text_color='black', hover_color='#CCCC00')

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Загруженность ПК",
                                                        command=self.system_monitoring, fg_color='gold',
                                                        text_color='black', hover_color='#CCCC00')

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Выделение RAM",
                                                        command=self.ram, fg_color='gold', text_color='black',
                                                        hover_color='#CCCC00')

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Проверка на вирусы",
                                                        command=self.procc, fg_color='gold', text_color='black',
                                                        hover_color='#CCCC00')

        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Проверка скорости\nинтернета",
                                                        command=self.www_check, fg_color='gold', text_color='black',
                                                        hover_color='#CCCC00')
        self.sidebar_button_7=customtkinter.CTkButton(self.sidebar_frame, text = 'Проверка на\n поврежденные \nфайлы',
                                                      fg_color='gold',text_color='black', hover_color='#CCCC00',
                                                      command=self.file_damage_check)


        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value=self.th)
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Светлая", "Темная"],
                                             command=self.combobox_callback, variable=self.combobox_var)
        self.combobox.place(x=30, y=300)
        self.vers_label_font = customtkinter.CTkFont('Monotype Corsiva', size=24, weight='bold')
        self.vers_label = customtkinter.CTkLabel(self.sidebar_frame, text='GOLD EDITION', font=self.vers_label_font,
                                                 text_color='#CCCC00')
        self.vers_label.place(x=15, y=340)

        self.radio_var = customtkinter.IntVar(value=self.rh)
        self.radio_button = customtkinter.CTkRadioButton(self.sidebar_frame, text='1', variable=self.radio_var, value=1,
                                                         fg_color='gold', hover_color='#CCCC00',
                                                         command=self.radiobutton_callback)
        self.radio_button.place(x=40, y=240)

        self.radio_button2 = customtkinter.CTkRadioButton(self.sidebar_frame, text='2', variable=self.radio_var, value=2,
                                                          fg_color='gold', hover_color='#CCCC00',
                                                          command=self.radiobutton_callback)
        self.radio_button2.place(x=120, y=240)
        self.radiobutton_callback()
        logging.info(">>> Повторная отрисовка боковой панели. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))
        app.update_idletasks()

    # Метод страниц с функционалом
    def radiobutton_callback(self):
        a = self.radio_var.get()
        if a == 1:
            try:
                self.sidebar_button_6.place_forget()
                self.sidebar_button_7.place_forget()
                self.sidebar_button_2.place(x=30, y=80)
                self.sidebar_button_3.place(x=30, y=120)
                self.sidebar_button_4.place(x=30, y=160)
                self.sidebar_button_5.place(x=30, y=200)

                self.rh = 1
                logging.info(">>> Отрисована 1 страница левого sidebar. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
            except Exception as e:
                logging.error('>>> ' + str(e) + "День: %s; Точная дата и время запуска: %s", current_weekday,
                              now_dt.strftime(date_format))
                logging.exception(e)
        elif a == 2:
            try:
                self.sidebar_button_2.place_forget()
                self.sidebar_button_3.place_forget()
                self.sidebar_button_4.place_forget()
                self.sidebar_button_5.place_forget()
                self.sidebar_button_6.place(x=30, y=80)
                self.sidebar_button_7.place(x=30, y=125)
                self.rh = 2
                logging.info(">>> Отрисована 2 страница левого sidebar. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
            except Exception as e:
                logging.error('>>> ' + str(e) + "День: %s; Точная дата и время запуска: %s", current_weekday,
                              now_dt.strftime(date_format))
                logging.exception(e)

    # Метод вторичной выбора темы приложения
    def combobox_callback(self, choice):
        self.combobox_var.set(choice)
        if choice == 'Светлая':
            custom('light')
            self.th = 'Светлая'
            logging.info(">>> Установленна светлая тема. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        else:
            custom('dark')
            self.th = 'Темная'
            logging.info(">>> Установленна темная тема. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

    # Метод первичного выбора темы приложения
    def combobox_callback2(self, choice):
        self.combobox_var.set(choice)
        if choice == 'Светлая':
            custom('light')
            self.image_path = 'image/Capi_gold_light.jpg'
            self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
            self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='')
            self.ico_label.place(x=250, y=50)
            self.th = 'Светлая'

            logging.info(">>> Установленна светлая тема с капибарой. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        else:
            custom('dark')
            self.image_path = 'image/Capi_gold_dark.jpg'
            self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
            self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='')
            self.ico_label.place(x=250, y=50)
            logging.info(">>> Установленна темная тема с капибарой. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
            self.th = 'Темная'

    # Метод экрана приветствия
    def starting(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

        self.init_GUI()

        self.faq_button_1 = customtkinter.CTkButton(app, text="FAQ", command=self.faq, fg_color='gold',
                                                    text_color='black', hover_color='#CCCC00')
        self.faq_button_1.place(x=230, y=340)
        self.report_button_1 = customtkinter.CTkButton(app, text="Сообщить об ошибке", command=self.reported,
                                                       fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.report_button_1.place(x=400, y=340)
        self.textbox_start = customtkinter.CTkTextbox(master=self, width=410, height=300, corner_radius=0)
        self.textbox_start.insert("0.0", "Спасибо за приобретение CaPi Manager GOLD EDITION!\n\nВ колонке слева "
                                         "вы можете "
                                         "выбрать необходимые вкладки\nс различными функциями, например:\n\n"
                                         "\t* Удаление повторяющихся файлов\n\t* Удаление КЭШа\n\t* Удаление временных "
                                         "файлов \n\t* Проверка загруженности ПК\n\t* Выделение оперативной памяти "
                                         "\n\t* Проверка на вирусы\n\t* Проверка скоррости интернета\n\t"
                                         "* Проверка повреждения файлов\n\n"
                                         "Если у вас остались какие-то вопросы, кликните по кнопке\n'FAQ' ниже\n\n"
                                         "Если во время работы программы вы столкнулись \nс ошибкой, просим сообщить о ней "
                                         "через кнопку \n'Сообщить об ошибке'")
        self.textbox_start.place(x=200, y=0)
        logging.info(">>> Начальный экран с текстом отрисован. День: %s; Точная дата и время запуска: %s",
                     current_weekday, now_dt.strftime(date_format))

    # Метод экрана очищения от мусора
    def clean(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        self.init_GUI()
        self.activity_potok = False
        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor1, fg_color='gold', text_color='black',
                                                         hover_color='#CCCC00')
        self.stroka_sostoyaniya1 = customtkinter.CTkLabel(app, text='Повтряющиеся файлы удалены')
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Не найдено файлов для удаления')

        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:")]
        drives[0] = '~\\Downloads'
        self.combo_vars1 = customtkinter.StringVar(value="~\\Downloads")
        self.combobox_povtors = customtkinter.CTkComboBox(app, values=drives, variable=self.combo_vars1)
        self.combobox_povtors.place(x=450, y=50)
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash, fg_color='gold', text_color='black',
                                                       hover_color='#CCCC00')
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить временные файлы",
                                                         command=self.recent, fg_color='gold', text_color='black',
                                                         hover_color='#CCCC00')
        self.del_povtor_button.place(x=220, y=50)
        self.del_cash_button.place(x=220, y=100)
        self.del_recent_button.place(x=220, y=150)
        self.pov_dirs = customtkinter.CTkLabel(app, text='Выберите папку\nудаления повторов')
        self.pov_dirs.place(x=450, y=90)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        logging.info(">>> Экран очистки отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Метод экрана FAQ
    def faq(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.textbox_faq = customtkinter.CTkTextbox(master=self, width=400, height=300, corner_radius=0)
        self.textbox_faq.insert("0.0", "1. Безопасно ли использовать приложение CaPi Manager?\n\n"
                                       "Наше приложение проверено двумя известными\n"
                                       "антивирусами и не содержит каких-либо вредоносных\nфайлов"
                                       ". Команда разработчиков уверяет, что приложение\nабсолютно безопасно.\n\n\n"
                                       "2. Если я проведу очистку недавних файлов и(или) КЭШа\n"
                                       "системы удалятся ли важные для меня файлы?\n\n"
                                       "Безусловно, нет! Наша программа удалит ненужные\n"
                                       "системные файлы, которые загружают память и\nпроцессор "
                                       "вашего компьютера.\n\n\n3. Что выполняет кнопка 'Удалить повторяющиеся файлы?"
                                       "\n\nЭта функция удаляет скачанные несколько раз файлы в\n"
                                       "папке Загрузки, и оставляет только одну копию\nэтого файла.\n\n\n"
                                       "4. Не опасно ли удалять системные файлы? Вдруг \nпрограмма "
                                       "удалит что-то не то, и компьютер перестанет \nработать?\n\n"
                                       "Программа не удаляет необходимые для работы \nсистемные файлы.\n\n\n"
                                       "5. Что находится во вкладке ‘Загруженность ПК’?\n\n"
                                       "В этой вкладке вы можете получить необходимые данные о загруженности "
                                       "компонентов вашего компьютера в \nданный момент. Нажав на кнопку "
                                       "‘Обновить данные’, "
                                       "вы \nувидите обновленные сведения о нагрузке на ваше\nустройство.\n\n\n"
                                       "6. Что такое RAM?\n\nRAM - это оперативная память, за счет которой компьютер\n"
                                       "может выполнять поставленную ему задачу.\n\n\n"
                                       "7. Программа зависает во время выделения RAM,\nчто делать?\n\n"
                                       "Ничего страшного! Программа выделяет дополнительную\n"
                                       "RAM за счет блокировки фоновых процессов. Обычно это\n"
                                       "занимает примерно 30 секунд.\n\n\n"
                                       "8. Что за окошко расположено над кнопкой ‘Запустить\nпроверку на вирусы’?\n\n"
                                       "Это окошко позволяет выбрать диск, который будет\n"
                                       "проверятся на вирусы. По умолчанию в программе\n"
                                       "происходит проверка диска С:/, который и находится\nвнутри компьютера. "
                                       "Другие диски, которые вы можете\nвыбрать в списке, это подключенные устройства\n"
                                       "(флешки, жесткие диски и др.). Их вы тоже можете \nпроверить на наличие "
                                       "вирусов.\n\n\n"
                                       "9. Как долго программа будет проверять мой ПК на \nналичие вирусов?\n\n"
                                       "Все зависит от количества файлов на вашем компьютере и "
                                       "их размера. Чем больше их количество, тем дольше \nCaPi "
                                       "Manager будет проводить проверку.\n\n\n"
                                       "10. Что делают кружочки с цифрами под вкладкой \n‘Проверка на вирусы’?\n\n"
                                       "Если нажать на кружочек, рядом с "
                                       "которым указана \nцифра 2, то вы откроете вторую страницу "
                                       "функционала \nнашего приложения. Нажав на кружочек 1, "
                                       "вы вернетесь\nна первую страницу приложения.\n\n\n"
                                       "11. Как работает проверка скорости интернета?\n\n"
                                       "После нажатия на кнопку\n‘Запустить проверку скорости интернета’, "
                                       "примерно\nчерез 20-30 секунд вы получите необходимые данные.\n"
                                       "Строчка ‘Скорость загрузки’ указывает на скорость,\nс которой "
                                       "данные из интернета загружаются\nна ваш компьютер.\n"
                                       "Вторая строчка ‘Скорость выгрузки’ показывает скорость,\n"
                                       "с которой данные с вашего компьютера\n"
                                       "загружаются в интернет.\n\n\n"
                                       "12. Что делает функция\n'Проверка на поврежденные файлы?'\n\n"
                                       "Эта функция просканирует все системные файлы \nи, в случае "
                                       "необходимости, заменит их. Это необходимо\nдля правильной "
                                       "работы вашего компьютера.\n\n\n"
                                       "13. CaPi Manager работает неправильно, что делать?\n\n"
                                       "Нажмите кнопку ‘Начало’, затем ‘Сообщить об ошибке’,\n"
                                       "укажите ваше имя, электронную почту и кратко опишите\n"
                                       "проблему в нижнем окне. После нажатия кнопки\n‘Отправить’, "
                                       "данные моментально будут получены\nразработчиками.")
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='gold',
                                                 text_color='black', hover_color='#CCCC00')
        self.abort_faq.place(x=310, y=340)
        logging.info(">>> Экран помощи отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    #Метод экрана обратной связи
    def reported(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()
        self.label_report = customtkinter.CTkLabel(app, text='Впишите ваше Имя и E-Mail в соответствующие поля,\n'
                                                             'кратко опишите возникшую проблему'
                                                             ' и отправьте\n'
                                                             'обращение разработчикам,кликнув кнопку "Отправить"')
        self.label_report.place(x=210, y=10)
        self.label_name = customtkinter.CTkLabel(app, text='Ваше имя:')
        self.label_name.place(x=260, y=90)
        self.label_mail = customtkinter.CTkLabel(app, text='Ваш e-mail:')
        self.label_mail.place(x=260, y=120)
        self.name = customtkinter.CTkEntry(app, placeholder_text="Ваше имя")
        self.name.place(x=350, y=90)
        self.email = customtkinter.CTkEntry(app, placeholder_text="Ваш e-mail")
        self.email.place(x=350, y=120)
        self.textbox_rep2 = (customtkinter.CTkTextbox(app, width=300, height=110))
        self.textbox_rep2.place(x=230, y=210)
        self.textbox_rep2.insert("0.0", '*кратко опишите возникшую проблему*')
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='gold',
                                                    text_color='black', hover_color='#CCCC00')
        self.report_abort.place(x=230, y=340)
        self.report_send = customtkinter.CTkButton(app, text="Отправить", command=self.sending1, fg_color='gold',
                                                   text_color='black', hover_color='#CCCC00')
        self.report_send.place(x=400, y=340)
        logging.info(">>> Экран репорта отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    def sending1(self):
        s = threading.Thread(target=self.sending2)
        s.start()
        logging.info(">>> Поток на репорт запущен. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Бекэнд отправки репорта
    def sending2(self):
        try:
            ops = platform.platform()
            proc = platform.processor()
            build_inf = str([os.name, ops, proc, 'ver = 3.2.0ge']).encode()
            self.h = base64.b64encode(build_inf)
            logging.info(">>> Токен сгенерирован. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            dt = str(datetime.datetime.now())[:-5].replace(' ', '--').replace(':', '-')
            tt = dt + '.txt'
            t = open(tt, 'w+')
            f = open('capi_log.log')
            if '@' not in self.email.get():
                self.textbox_rep2.delete("0.0", '100.0')
                self.textbox_rep2.insert("0.0", 'E-Mail введен не корректно.\nОтсутствует символ => @\n'
                                                'Проверьте правильность запонения формы')
                logging.warning(">>> Пользователь ввел некорректный e-mail. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))
                return
            else:
                t.write(self.name.get() + '\n')
                t.write(self.email.get() + '\n')
                t.write(str(self.h) + '\n')
                t.write(self.textbox_rep2.get(0.0, 500.0))
                for i in f:
                    t.write(i)
                t.close()
                f = open('yandex_api.txt', 'r')
                report_token = f.readline()
                f.close()
                y = yadisk.YaDisk(token=report_token)
                y.upload(tt, "/test/"+str(tt))
                self.textbox_rep2.delete("0.0", '100.0')
                self.textbox_rep2.insert("0.0", 'Сообщение успешно отправлено')
                self.report_send.destroy()
                logging.info(">>> Репорт отправлен. День: %s; Точная дата и время запуска: %s", current_weekday,
                             now_dt.strftime(date_format))
        except Exception as e:
            self.textbox_rep2.delete('0.0', '500.0')
            self.textbox_rep2.insert("0.0", 'Возникла ошибка при отправке сообщения.\nПопробуйте позднее')
            logging.error('>>> ' + str(e) + "День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            logging.exception(e)
            try:
                subprocess.check_call(["ping", "-c 1", "www.google.ru"])
                logging.info(">>> Проверка подключение к WWW успешно пройдена. День: %s; Точная дата и время запуска: %s",
                             current_weekday, now_dt.strftime(date_format))
            except subprocess.CalledProcessError:
                logging.error(">>> Отсутствует подключение ПК к WWW. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))

    #Создание потока, отслеживание прогресса бекэнда и дальнейшая отрисовка результатов работы функции
    def povtor1(self):
        self.stroka_sostoyaniya1.place_forget()
        self.stroka_sostoyaniya2.place_forget()
        p = threading.Thread(target=self.povtor2)
        p.start()
        self.activity_potok = True
        logging.info(">>> Поток очистки повторяющихся файлов создан. День: %s; Точная дата и время запуска: %s",
                     current_weekday, now_dt.strftime(date_format))
        while p.is_alive() and self.activity_potok == True:
            for i in range(1, 4):
                time.sleep(1)
                try:
                    self.stroka_sostoyaniya.place_forget()
                except:
                    pass
                self.stroka_sostoyaniya = customtkinter.CTkLabel(app, text='Выполнение началось' + '.' * i)
                if p.is_alive():
                    self.stroka_sostoyaniya.place(x=250, y=200)
                    app.update()
        if self.pov and self.count_dublicates != 0:
            try:
                self.stroka_sostoyaniya.destroy()
            except:
                pass
            self.stroka_sostoyaniya1.place(x=250, y=200)
            logging.info(">>> Повторяющиеся файлы удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
        elif self.count_dublicates == 0:
            try:
                self.stroka_sostoyaniya.place_forget()
            except:
                pass
            self.stroka_sostoyaniya2.place(x=250, y=200)

    # Бекенд удаления повторяющихся файлов из загрузок
    def povtor2(self):
        logging.info(">>> Поток очистки повторяющихся файлов начал работу. День: %s; Точная дата и время запуска: %s",
                     current_weekday, now_dt.strftime(date_format))
        while self.activity_potok:
            try:
                self.pov = False
                self.count_dublicates = 0
                def remove_duplicates():
                    downloads_folder = os.path.expanduser(self.combobox_povtors.get())
                    def get_file_hash(file_path):
                        with open(file_path, 'rb') as file:
                            return hashlib.sha256(file.read()).hexdigest()
                    files_list = [os.path.join(downloads_folder, f) for f in os.listdir(downloads_folder) if
                                os.path.isfile(os.path.join(downloads_folder, f))]
                    duplicates = []
                    file_hashes = {}
                    for file_path in files_list:
                        file_hash = get_file_hash(file_path)
                        if file_hash in file_hashes:
                            duplicates.append(file_path)
                            self.count_dublicates += 1
                        else:
                            file_hashes[file_hash] = file_path
                    for duplicate in duplicates:
                        os.remove(duplicate)
                remove_duplicates()
                self.pov = True
                self.activity_potok = False
            except Exception as e:
                self.pov = False
                logging.warning(">>> Файлов для удаления не найдено. День: %s; Точная дата и время запуска: %s",
                                current_weekday, now_dt.strftime(date_format))
                logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                            current_weekday, now_dt.strftime(date_format))
                logging.exception(e)
        else:
            self.stroka_sostoyaniya.place_forget()
            return

    # Бекэнд уудаления КЭШа
    def cash(self):
        try:
            self.stroka_sostoyaniya2.place_forget()
        except Exception:
            pass
        self.stroka_sostoyaniya = customtkinter.CTkLabel(app, text='Выполнение запущено')
        self.stroka_sostoyaniya.place(x=250, y=200)
        try:
            temp_folders = ['C:\\Windows\\Temp']
            for folder in temp_folders:
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                                      current_weekday, now_dt.strftime(date_format))
                        logging.exception(e)
            logging.info(">>> Кэш системы удален при помощи Python. День: %s; Точная дата и время запуска: %s",
                        current_weekday,
                        now_dt.strftime(date_format))
        except Exception as e:
            os.system('del /f /s /q %temp%\*')
            logging.warning(">>> Кэш системы удален при помощи консоли Windows. День: %s; Точная дата и время запуска: %s",
                         current_weekday, now_dt.strftime(date_format))
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
            logging.exception(e)
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='КЭШ системы удален')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    # Бекэнд удаления недавних файлов
    def recent(self):
        try:
            self.stroka_sostoyaniya2.place_forget()
        except Exception:
            pass
        self.stroka_sostoyaniya = customtkinter.CTkLabel(app, text='Выполнение запущено')
        self.stroka_sostoyaniya.place(x=250, y=200)
        try:
            temp_folders = [Path(os.environ["USERPROFILE"]) / "AppData\Local\Temp"]
            for folder in temp_folders:
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                                      current_weekday, now_dt.strftime(date_format))
                        logging.exception(e)
            logging.info(">>> Недавние файлы удалены при помощи Python. День: %s; Точная дата и время запуска: %s",
                        current_weekday,
                        now_dt.strftime(date_format))
        except Exception as e:
            logging.error(">>> Питон не смог удалить временные файлы пользователя:" + str(e) + ". День: %s; "
                            "Точная дата и время запуска: %s", current_weekday, now_dt.strftime(date_format))
            logging.exception(e)
            try:
                os.system('del /f /s /q %systemroot%/temp\*')
                logging.info(">>> Недавние файлы пользователя удалены при помощи консоли Windows. День: %s; "
                    "Точная дата и время запуска: %s", current_weekday, now_dt.strftime(date_format))
            except Exception as e:
                logging.error(">>> Недавние файлы не были удалены при помощи консоли Windows. День: %s; "
                              "Точная дата и время запуска: %s", current_weekday, now_dt.strftime(date_format))
                logging.exception(e)
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Недавние файлы удалены')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    # Метод вызова экрана загруженности
    def system_monitoring(self):
        for widget in app.winfo_children():
            widget.destroy()    
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
        self.init_GUI()
        self.system_mon_2()

    # Метод загруженности пк
    def system_mon_2(self):
        cpu_usage = 'Загрузка процессора:' + str(psutil.cpu_percent()) + '%'
        memory_usage = 'Загрузка оперативной памяти:' + str(psutil.virtual_memory().percent) + '%'
        disk_usage = 'Загрузка жесткого диска:' + str(psutil.disk_usage("/").percent) + '%'
        self.label_cpu_usage = customtkinter.CTkLabel(app, text=cpu_usage)
        self.label_cpu_usage.place(x=250, y=50)
        self.label_memory_usage = customtkinter.CTkLabel(app, text=memory_usage)
        self.label_memory_usage.place(x=250, y=100)
        self.label_disk_usage = customtkinter.CTkLabel(app, text=disk_usage)
        self.label_disk_usage.place(x=250, y=150)
        self.obnova_button = customtkinter.CTkButton(app, text="Обновить данные", command=self.system_monitoring,
                                                     fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.obnova_button.place(x= 300, y=220)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        logging.info(">>> Отрисовано окно мониторига системы. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update_idletasks()

    # Фронтед функции выделения оперативки
    def ram(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
        self.init_GUI()
        self.activity_potok = False
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        self.ram_button = customtkinter.CTkButton(app, text="Запустить выделение RAM",
                                                   command=self.allocate_memory, fg_color='gold', text_color='black',
                                                  hover_color='#CCCC00')
        self.ram_button.place(x=300, y=100)
        self.label_ram_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для выделения оперативной памяти\nи '
                                                                'подождите. Обычно это занимает от 30 до 80 секунд')
        self.end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.label_ram_turbo2 = customtkinter.CTkLabel(app, text='Успешно выделена дополнительная RAM', font=self.end_font)
        self.label_ram_turbo.place(x=215, y=150)

        logging.info(">>> Отрисовано окно выделения RAM. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    # Бекэнд выделения оперативки
    def allocate_memory(self):
        ram = str(psutil.virtual_memory()[0])
        ram = int(ram)/1024/1024/1024
        if ram > 1.0 and ram < 3.0:
            d = list(range(10**8))
            del d
        elif ram >= 3.0 and ram <= 5.0:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 4))
            del d
            del d2
        elif ram >= 6.0 and ram <= 10.0:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            del d
            del d2
        elif ram >= 12.0 and ram <= 18.0:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            d3 = list(range(10 ** 8))
            d4 = list(range(10 ** 8))
            del d
            del d2
            del d3
            del d4
        elif ram >= 20.0 and ram < 34.0:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            d3 = list(range(10 ** 8))
            d4 = list(range(10 ** 8))
            d5 = list(range(10 ** 8))
            d6 = list(range(10 ** 8))
            del d
            del d2
            del d3
            del d4
            del d5
            del d6
        gc.collect()
        self.label_ram_turbo.destroy()
        self.ram_button.destroy()
        self.label_ram_turbo2.place(x=255, y=150)
        logging.info(">>> RAM выделена. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    # Фронтенд антивируса
    def procc(self):
        self.deeps_scan = 1
        try:
            p = set()
            t = open('_internal/signatures.txt', 'r')
            for i in t:
                i = i.replace('\n', '')
                p.add(i)
            a = str(self.server_sign[0].split(' ')[0])
            if a in p:
                self.new_signatures = False
            else:
                self.new_signatures = True
        except Exception as e:
            logging.error(">>> Не удалось сверить сигнатуры. День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
            logging.error(">>> " + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
            logging.exception(e)
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
        self.init_GUI()
        self.stop_scan = False
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        self.procc_button = customtkinter.CTkButton(app, text="Запустить проверку на вирусы",
                                                   command=self.start_scanning, fg_color='gold', text_color='black',
                                                    hover_color='#CCCC00')
        self.procc_button.place(x=290, y=100)
        self.label_procc_turbo = customtkinter.CTkLabel(app, text='Выберете тип сканирования\nи нажмите кнопку '
                                                                  'выше для запуска функции')
        self.label_procc_turbo.place(x=250, y=150)
        self.dirs = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:")]
        self.combo_vars = customtkinter.StringVar(value="C:/")
        self.combobox11 = customtkinter.CTkComboBox(app, values=self.dirs, variable=self.combo_vars)
        self.combobox11.place(x=320, y=40)
        self.scan_var = customtkinter.IntVar(value=self.deeps_scan)
        self.scan_button1 = customtkinter.CTkRadioButton(app, text='Полное', variable=self.scan_var, value=1,
                                                         fg_color='gold', hover_color='#CCCC00',
                                                         command=self.scan_callback)
        self.scan_button1.place(x=300, y=200)

        self.scan_button2 = customtkinter.CTkRadioButton(app, text='Быстрое', variable=self.scan_var, value=2,
                                                          fg_color='gold', hover_color='#CCCC00',
                                                          command=self.scan_callback)
        self.scan_button2.place(x=400, y=200)
        self.scan_callback()
        if self.new_signatures:
            self.supdate_button = customtkinter.CTkButton(app, text="Обновить вирусную базу",
                                                            command=self.signatures_update, fg_color='gold',
                                                            text_color='black', hover_color='#CCCC00')
            self.supdate_button.place(x=300, y=300)
            self.supdate_label = customtkinter.CTkLabel(app, text='Рекoмендуем обновить вирусную базу')

            self.supdate_label.place(x=270, y=260)
            logging.info(">>> Кнопка обновления отрисована. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        logging.info(">>> Окно антивируса отрисовано. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update()

    def scan_callback(self):
        a = self.scan_var.get()
        if a == 1:
            try:
                self.deeps_scan = 1
                logging.info(">>> Отрисована 1 страница левого sidebar. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
            except Exception as e:
                logging.error('>>> ' + str(e) + "День: %s; Точная дата и время запуска: %s", current_weekday,
                              now_dt.strftime(date_format))
                logging.exception(e)
        elif a == 2:
            try:
                self.deeps_scan = 2
                logging.info(">>> Отрисована 2 страница левого sidebar. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
            except Exception as e:
                logging.error('>>> ' + str(e) + "День: %s; Точная дата и время запуска: %s", current_weekday,
                              now_dt.strftime(date_format))
                logging.exception(e)


    # Метод начала сканирования
    def start_scanning(self):
        self.scan_button1.place_forget()
        self.scan_button2.place_forget()
        self.label_procc_turbo.place_forget()
        self.label_procc_turbo = customtkinter.CTkLabel(app, text='Для остановки сканирования\nнажмите кнопку выше')
        self.label_procc_turbo.place(x=310, y=150)
        try:
            self.supdate_label.place_forget()
        except:
            pass
        self.counter2 = 0
        self.counter1 = 0
        f = open('_internal/signatures.txt')
        self.malicious_hashes = []
        for i in f:
            self.malicious_hashes.append(i)
        f.close()
        self.label_procc_turbo1 = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:')
        self.label_procc_turbo1.place(x=250, y=200)
        self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'{self.counter2}')
        self.label_procc_turbo2.place(x=450, y=200)
        self.label_procc_turbo3 = customtkinter.CTkLabel(app, text='Найдено вирусов:')
        self.label_procc_turbo3.place(x=250, y=220)
        self.label_procc_turbo4 = customtkinter.CTkLabel(app, text=f'{self.counter1}')
        self.label_procc_turbo4.place(x=450, y=220)
        self.scan_end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.scan_end = customtkinter.CTkLabel(app, text='Сканирование завершено', font=self.scan_end_font)
        self.scan_abort = customtkinter.CTkLabel(app, text='Сканирование прервано', font=self.scan_end_font)
        self.procc_button.destroy()
        self.abort_button = customtkinter.CTkButton(app, text="Остановить проверку на вирусы",
                                                    command=self.abort_scanning, fg_color='gold', text_color='black',
                                                    hover_color='#CCCC00')
        self.abort_button.place(x=290, y=100)
        self.aborting = False

        logging.info(">>> Сканирование запущенно. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        self.scan_directory(self.combobox11.get())
        self.abort_button.destroy()
        self.scan_end.place(x=300, y=100)
        logging.info(">>> Сканирование завершенно системой. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        # Метод сканирующий файл

    def scan_file(self):
        if self.stop_scan:
            self.label_procc_turbo1.place_forget()
            self.label_procc_turbo2.place_forget()
            self.label_procc_turbo3.place_forget()
            self.label_procc_turbo4.place_forget()
            return
        if self.aborting:
            self.abort_button.destroy()
            self.scan_abort.place(x=300, y=100)
            return
        try:
            if self.deeps_scan == 2 and os.path.getsize(self.file_path) <= 104857600:
                self.label_procc_turbo2.destroy()
                self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'{self.counter2}')
                self.label_procc_turbo2.place(x=450, y=200)
                with open(self.file_path, 'rb') as file:
                    content = file.read()
                    hash_sum = hashlib.sha256(content).hexdigest() + '/n'
                if hash_sum in self.malicious_hashes:
                    self.counter1 += 1
                else:
                    self.counter2 += 1
                if self.counter1 >= 1:
                    self.label_procc_turbo4.destroy()
                    self.label_procc_turbo4 = customtkinter.CTkLabel(app, text=f'{self.counter1}')
                    self.label_procc_turbo4.place(x=450, y=220)
                    logging.warning(">>>" + 'Найден вирус:' + ". День: %s; Точная дата и время запуска: %s",
                                    current_weekday, now_dt.strftime(date_format))
                    logging.warning('>>>' + hash_sum)
                    self.danger_path = self.file_path
                    self.virus_label = customtkinter.CTkLabel(app, text='Найден файл с вирусом', text_color='red')

                    self.virus_label.place(x=310, y=260)
                    self.virus_button = customtkinter.CTkButton(app, text="Удалить файл с вирусом",
                                                                command=self.virus_remove, fg_color='gold',
                                                                text_color='black', hover_color='#CCCC00')
                    self.virus_button.place(x=300, y=300)
                    self.virus_path = self.file_path
            elif self.deeps_scan == 1:
                self.label_procc_turbo2.destroy()
                self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'{self.counter2}')
                self.label_procc_turbo2.place(x=450, y=200)
                with open(self.file_path, 'rb') as file:
                    content = file.read()
                    hash_sum = hashlib.sha256(content).hexdigest() + '/n'
                if hash_sum in self.malicious_hashes:
                    self.counter1 += 1
                else:
                    self.counter2 += 1
                if self.counter1 >= 1:
                    self.label_procc_turbo4.destroy()
                    self.label_procc_turbo4 = customtkinter.CTkLabel(app, text=f'{self.counter1}')
                    self.label_procc_turbo4.place(x=450, y=220)
                    logging.warning(">>>" + 'Найден вирус:' + ". День: %s; Точная дата и время запуска: %s",
                                    current_weekday, now_dt.strftime(date_format))
                    logging.warning('>>>' + hash_sum)
                    self.danger_path = self.file_path
                    self.virus_label = customtkinter.CTkLabel(app, text='Найден файл с вирусом', text_color='red')

                    self.virus_label.place(x=310, y=260)
                    self.virus_button = customtkinter.CTkButton(app, text="Удалить файл с вирусом",
                                                                command=self.virus_remove, fg_color='gold',
                                                                text_color='black', hover_color='#CCCC00')
                    self.virus_button.place(x=300, y=300)
                    self.virus_path = self.file_path
        except Exception as e:
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s", current_weekday,
                          now_dt.strftime(date_format))
            logging.exception(e)
            self.counter2 += 0
        app.update()

        # Метод для прогулки по диреториям

    def scan_directory(self, directory):
        if self.aborting or self.stop_scan:
            return
        for root, dirs, files in os.walk(directory):
            for file in files:
                self.file_path = os.path.join(root, file)
                self.scan_file()
                app.update()

        # Метод удаления вирусов

    def virus_remove(self):
        os.remove(self.danger_path)
        self.counter1 = 0
        self.danger_path = ''
        logging.info(">>> Вирус удален. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

        # Метод принудительной остановки сканирования

    def abort_scanning(self):
        self.aborting = True
        logging.info(">>> Сканирование приостановленно пользователем. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

        # Метод обновления сигнатур

    def signatures_update(self):
        self.supdate_button.place_forget()
        self.supdate_label.place_forget()
        self.supdate_label = customtkinter.CTkLabel(app, text='Обновление началось\nНе закрывайте вкладку '
                                                              '"Проверка на вирусы"')

        self.supdate_label.place(x=280, y=260)
        try:
            w = []
            for j in self.server_sign:
                c = j.replace('[', '').replace(']', '').replace('"', '').replace(' ', '').replace('\\r', '')
                w.append(c)
            t = open('_internal/signatures.txt', 'a')
            t.write('\n')
            for i in w:
                t.write(i + '\n')
            t.close()
            self.supdate_label.place_forget()
            self.supdate_label = customtkinter.CTkLabel(app, text='Обновление завершено')
            self.supdate_label.place(x=310, y=260)
            logging.info(">>> Сигнатуры обновлены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        except Exception as e:
            self.supdate_label.place_forget()
            self.supdate_label = customtkinter.CTkLabel(app,
                                                        text='Невозможно установить обновления.\nПопробуйте позже')

            self.supdate_label.place(x=310, y=260)
            logging.error(">>> Ошибка при обновлении сигнатур :(. День: %s; Точная дата и время запуска: %s",
                          current_weekday,
                          now_dt.strftime(date_format))
            logging.exception(e)

    # Метод окна замера скорости интернета
    def www_check(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        self.www_button = customtkinter.CTkButton(app, text="Запустить проверку скорости интернета",
                                                   command=self.start_check_www3, fg_color='gold', text_color='black',
                                                  hover_color='#CCCC00')
        self.www_button.place(x=265, y=100)
        self.www_label = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для проверки\nскорости интернета и '
                                                'подождите появления результатов.\nОбычно это занимает 20-30 секунд.')
        self.www_label.place(x=220, y=150)
        logging.info(">>> Окно проверки скорости интернета отрисовано. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update()

    def start_check_www3(self):
        timeout = 1
        try:
            requests.head("http://www.google.com/", timeout=timeout)
            self.start_check_www1()
        except requests.ConnectionError:
            self.dont_con_label = customtkinter.CTkLabel(app, text=f'Нет подключения к интернету :(')
            self.dont_con_label.place(x=300, y=240)
            logging.error(
                ">>> Не удалость выполнить проверку скорости интернета :(. День: %s; Точная дата и время запуска: %s",
                current_weekday, now_dt.strftime(date_format))
            logging.error(">>> Отсутствует подключение ПК к WWW. День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))

    def start_check_www1(self):
        try:
            self.dont_con_label.place_forget()
        except Exception as e:
            pass
        t = threading.Thread(target=self.start_check_www2)
        self.activity_potok = True
        t.start()
        logging.info(">>> Поток замера скорости интернета создан. День: %s; Точная дата и время запуска: %s",
                current_weekday, now_dt.strftime(date_format))
        while t.is_alive() and self.activity_potok:
            for i in range(1, 4):
                time.sleep(1)
                try:
                    self.www_check_label_start.destroy()
                except:
                    pass
                self.www_check_label_start = customtkinter.CTkLabel(app, text='Выполнение началось' + '.' * i)
                if self.activity_potok:
                    self.www_check_label_start.place(x=325, y=200)
                    app.update()
        self.www_label.place_forget()
        self.www_button.place_forget()
        self.www_check_label_start.place_forget()
        self.end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.ds_label = customtkinter.CTkLabel(app, text=f'Скорость загрзки:{self.ds} Мбит/с', font=self.end_font)
        self.us_label = customtkinter.CTkLabel(app, text=f'Скорость выгрузки:{self.us} Мбит/с', font=self.end_font)
        self.ds_label.place(x=270, y=100)
        self.us_label.place(x=270, y=130)
        app.update()

    # Метод замера скорости и вывода результатов
    def start_check_www2(self):
        while self.activity_potok:
            logging.info(">>> Поток замера скорости интернета начал работу. День: %s; Точная дата и время запуска: %s",
                        current_weekday, now_dt.strftime(date_format))
            st = speedtest.Speedtest()
            self.ds = round(int(st.download()) / 1000000, 2)
            self.us = round(int(st.upload()) / 1000000, 2)
            logging.info(">>> Скорость интернета проверена. День: %s; Точная дата и время запуска: %s",
                            current_weekday,
                            now_dt.strftime(date_format))
            app.update()
            return
        else:
            self.ds_label.place_forget()
            self.us_label.place_forget()
            return

    # Метод для исправления файлов
    def file_damage_check(self):
        for widget in app.winfo_children():
            widget.destroy()
        logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))
        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.file_damage_button = customtkinter.CTkButton(app, text="Запустить проверку на повреждённые файлы",
                                                          command=self.damage_check1, fg_color='gold',
                                                          text_color='black',
                                                          hover_color='#CCCC00')
        self.file_damage_button.place(x=250, y=100)

        self.file_damage_label = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для проверки и замены\n'
                                                                  'поврежденных системных файлов.\n'
                                                                  'Обычно это занимает 90-130 секунд.')
        self.file_damage_label.place(x=250, y=150)

        logging.info(">>> Окно проверки на поврежденные файлы отрисовано. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    def damage_check1(self):
        def is_admin():
            try:
                logging.info(">>> Проверка на админа пройдена. День: %s; Точная дата и время запуска: %s",
                             current_weekday, now_dt.strftime(date_format))
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                logging.warning(">>> Пользователь пытался запустить проверку на повреждения без админки."
                                " День: %s; Точная дата и время запуска: %s", current_weekday,
                                now_dt.strftime(date_format))
                return False

        if is_admin():
            self.t2 = threading.Thread(target=self.damage_check2)
            self.t2.start()
            self.activity_potok = True
            logging.info(">>> Поток проверка на повреждения создан. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        else:
            self.file_damage_label.place_forget()
            self.file_damage_end = customtkinter.CTkLabel(app,
                                                          text='Возникла ошибка при сканировании :(\n '
                                                               'Попробуйте запустить CaPi от имени администратора')
            self.file_damage_end.place(x=230, y=150)
            logging.error(">>> Ошибка scannow. День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
        while self.t2.is_alive() and self.activity_potok:
            for i in range(1, 4):
                time.sleep(1)
                try:
                    self.file_damage_label_start.place_forget()
                except:
                    pass
                self.file_damage_label_start = customtkinter.CTkLabel(app, text='Выполнение началось' + '.' * i)
                if self.activity_potok:
                    self.file_damage_label_start.place(x=325, y=200)
                    app.update()
        self.file_damage_label.place_forget()
        self.file_damage_button.place_forget()
        self.file_damage_label_start.place_forget()
        self.end_font = customtkinter.CTkFont(size=14, weight='bold')
        f = open('scannow_feedback.txt', 'r')
        scannow_feedback = f.readline()
        f.close()
        with open('./OUTPUT_INFO/output_Damaged_Files.log', 'r', encoding='cp1251') as file1:
            text1 = file1.readlines()
        if str(text1[-4]) == scannow_feedback:
            self.file_damage_end = customtkinter.CTkLabel(app,
                                                text='Защита ресурсов Windows не обнаружила\nнарушений целостности.',
                                                font=self.end_font)
            self.file_damage_end.place(x=243, y=150)

        else:
            self.file_damage_end = customtkinter.CTkLabel(app,
                                                          text='Успешно проверены и заменены необходимые\nсистемные файлы',
                                                          font=self.end_font)
            self.file_damage_end.place(x=233, y=150)
        logging.info(">>> Системные файлы проверены на повреждения. День: %s; Точная дата и время запуска: %s",
                     current_weekday, now_dt.strftime(date_format))
        app.update()

    def damage_check2(self):
        while self.activity_potok:
            with Path('./OUTPUT_INFO/output_Damaged_Files.log').expanduser().open('wb', 0) as file:
                subprocess.run('powershell sfc /scannow', stdout=file, check=True)
                # encoding = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
                text = subprocess.check_output('powershell sfc /scannow',
                                            encoding='cp866')
                Path('./OUTPUT_INFO/output_Damaged_Files.log').expanduser().write_text(text, encoding='cp1251')

            logging.info(">>> Проверка на поврежденные системные файлы. День: %s; Точная дата и время запуска: %s",
                        current_weekday,
                        now_dt.strftime(date_format))
            return
        else:
            return


# Запуск порграммы
if __name__ == "__main__":
    # Создание директории для output-ов
    path = './OUTPUT_INFO'
    if not os.path.exists(path):
        os.mkdir(path)
    # Все объявление логирования
    logger = logging.getLogger(__name__)
    fileHandler = logging.FileHandler(filename='capi_log.log')
    logging.basicConfig(format='[%(levelname)-10s] %(asctime)-25s - %(message)s', handlers=[fileHandler],
                        level=logging.INFO)
    days = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
    now_dt = datetime.datetime.now()
    current_weekday = days[now_dt.weekday()]
    date_format = "%d.%m.%Y %H:%M:%S.%f"
    logging.info(">>> Программа запущена. День: %s; Точная дата и время запуска: %s", current_weekday,
                 now_dt.strftime(date_format))
    #  Запаковка приложения
    app = GUI()
    app.mainloop()
    app.quit()
