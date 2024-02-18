# -*- coding: utf-8 -*-
import win32api
import customtkinter
import os
import re
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
from subprocess import *
import speedtest
import requests
from PIL import Image
from pathlib import Path
import win32com.shell.shell as shell
import sys
from pyqadmin import admin


# Функция именения темы приложения
def custom(app_theme):
    customtkinter.set_appearance_mode(app_theme)

# Настройки по умолчанию
customtkinter.set_appearance_mode('dark')
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
            response = requests.get('https://github.com/Stepan-Ryzhov/CaPi-Manager/blob/main/test_server_capi.txt')
            a = response.text.split('{')
            b = a[57].split(':')
            c = str(b[1]).split(',')
            c.pop(-1)
            self.server_sign = c
            if c == ['[]'] or c == '' or c == [] or c == [''] or c == ['["\\r"]']:
                logging.error(">>> Новые сигнатуры не найдены на GitHub. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))
            else:
                self.new_signatures = True
                self.init_start_GUI()
                logging.info(">>> Программа подключилась к серверу. День: %s; Точная дата и время запуска: %s",
                             current_weekday,
                             now_dt.strftime(date_format))
        except:
            logging.error(">>> Сервер отключен. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))

    # Метод начальной отрисовки
    def init_start_GUI(self):
        self.th = 'Темная'
        # self.rh = 1
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.sidebar_button_1.place(x=30, y=20)

        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value='Темная')
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Темная", "Светлая"],
                                                  command=self.combobox_callback2,  variable=self.combobox_var)

        self.combobox.place(x=30, y=300)
        self.image_path = 'image/Capi_game_dark.jpg'
        self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
        self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='', )
        self.ico_label.place(x=250, y=50)
        self.vers_label_font = customtkinter.CTkFont('Monotype Corsiva', size=24, weight='bold')
        self.vers_label = customtkinter.CTkLabel(self.sidebar_frame, text='GAMING\nEDITION', font=self.vers_label_font, text_color='#1e90ff')
        self.vers_label.place(x=45, y=340)
        logging.info(">>> Первая отрисовка боковой панели. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Метод повторной отрисовки начального экрана
    def init_GUI(self):
        # self.rh = self.rh
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Загруженность ПК",
                                                        command=self.system_monitoring, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Выделение RAM",
                                                        command=self.ram, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Максимальная\nпроизводительнсть",
                                                        command=self.procc, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')

        self.sidebar_button_2.place(x=30, y=80)
        self.sidebar_button_3.place(x=30, y=120)
        self.sidebar_button_4.place(x=30, y=160)
        self.sidebar_button_5.place(x=30, y=200)
        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value=self.th)
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Светлая", "Темная"],
                                             command=self.combobox_callback, variable=self.combobox_var)
        self.combobox.place(x=30, y=300)
        self.vers_label_font = customtkinter.CTkFont('Monotype Corsiva', size=24, weight='bold')
        self.vers_label = customtkinter.CTkLabel(self.sidebar_frame, text='GAMING\nEDITION', font=self.vers_label_font,
                                                 text_color='#1e90ff')
        self.vers_label.place(x=45, y=340)
        logging.info(">>> Повторная отрисовка боковой панели. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Метод вторичной выбора темы приложения
    def combobox_callback(self, choice):
        self.combobox_var.set(choice)
        if choice == 'Светлая':
            custom('light')


            logging.info(">>> Установленна светлая тема. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        else:
            custom('dark')

            logging.info(">>> Установленна темная тема. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

    # Метод первичного выбора темы приложения
    def combobox_callback2(self, choice):
        self.combobox_var.set(choice)
        if choice == 'Темная':
            custom('dark')
            self.image_path = 'image/Capi_game_dark.jpg'
            self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
            self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='')
            self.ico_label.place(x=250, y=50)
            self.th = 'Темная'

            logging.info(">>> Установленна светлая тема с капибарой. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        else:
            custom('light')
            self.image_path = 'image/Capi_game_light.jpg'
            self.ico1 = customtkinter.CTkImage(light_image=Image.open(self.image_path), size=(300, 300))
            self.ico_label = customtkinter.CTkLabel(self, image=self.ico1, text='')
            self.ico_label.place(x=250, y=50)
            logging.info(">>> Установленна темная тема с капибарой. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
            self.th = 'Светлая'

    # Метод экрана приветствия
    def starting(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.faq_button_1 = customtkinter.CTkButton(app, text="FAQ", command=self.faq, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.faq_button_1.place(x=230, y=340)
        self.report_button_1 = customtkinter.CTkButton(app, text="Сообщить об ошибке", command=self.reported, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.report_button_1.place(x=400, y=340)
        self.textbox_start = customtkinter.CTkTextbox(master=self, width=410, height=300, corner_radius=0)
        self.textbox_start.insert("0.0", "Спасибо за приобретение CaPi Manager GAMING EDITION!\n\nВ колонке слева вы можете "
                                         "выбрать необходимые вкладки\nс различными функциями, например:\n\n"
                                         "\t* Удаление повторяющихся файлов\n\t* Удаление КЭШа\n\t* Удаление временных файлов "
                                         "\n\t* Проверка загруженности ПК\n\t* Выделение оперативной памяти "
                                         "\n\t* Функция Максимальной производительности\n\n"
                                         "С новыми обновлениями появятся новые функции :)\n\n"
                                         "Если у вас остались какие-то вопросы, кликните по кнопке\n'FAQ' ниже\n\n"
                                         "Если во время работы программы вы столкнулись с ошибкой,\nпросим сообщить "
                                         "через кнопку 'Сообщить об ошибке'")
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

        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить временные файлы",
                                                         command=self.recent, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.del_povtor_button.place(x=250, y=50)
        self.del_cash_button.place(x=250, y=100)
        self.del_recent_button.place(x=250, y=150)
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
                                       "системы удаляться ли важные для меня файлы?\n\n"
                                       "Безусловно, нет! Наша программа удалит ненужные\n"
                                       "системные файлы, которые загружают память и процессор\n"
                                       "вашего компьютера\n\n\n3. Что выполняет кнопка 'Удалить повторяющиется файлы'?"
                                       "\n\nЭта функция удаляет скачанные несколько раз файлы в\n"
                                       "папке Загрузки, и оставляет только одну копию этого файла.\n\n\n"
                                       "4. Не опасно ли удалять системные файлы? Вдруг программа\n"
                                       "удалит что-то не то, и компьютер перестанет работать?\n\n"
                                       "Программа не удаляет необходимые для работы файлы\nсистемы\n\n\n"
                                       "5. Что находится во вкладке ‘Загруженность ПК’?\n\n"
                                       "В этой вкладке вы можете получить необходимые данные о загруженности "
                                       "компонентов вашего компьютера в данный момент. Нажав на кнопку "
                                       "‘Обновить данные’ "
                                       "вы увидите\nобновленные сведения о нагрузке на узлы вашего\nустройства.\n\n\n"
                                       "6. Что такое RAM?\n\nRAM - это оперативная память, за счет которой компьютер\n"
                                       "может выполнять поставленную ему задачу.\n\n\n"
                                       "7. Программа зависает во время выделения RAM,\nчто делать?\n\n"
                                       "Ничего страшного! Программа выделяет дополнительную\n"
                                       "RAM за счет блокировки фоновых процессов. Обычно это\n"
                                       "занимает примерно 30 секунд.\nСтоит просто немного подождать :)\n\n\n"
                                       "8. Что за окошко расположено над кнопкой ‘Запустить\nпроверку на вирусы’?\n\n"
                                       "Это окошко позволяет выбрать диск, который будет\n"
                                       "проверятся на вирусы. По умолчанию в программе\n"
                                       "происходит проверка диска С:/, который и находится внутри компьютера. "
                                       "Другие диски, которые вы можете выбрать в\n"
                                       "списке, это подключенные устройства(флешки, жесткие\n"
                                       "диски и др.). Их вы тоже можете проверить на наличие\n"
                                       "вирусов через наше приложение.\n\n\n"
                                       "9. Как долго программа будет проверять мой ПК на вирусы?\n\n"
                                       "Все зависит от количества файлов на вашем компьютере и\n"
                                       "их размера. Чем их количество больше, тем дольше CaPi\n"
                                       "Manager будет проводить проверку.\n\n\n"
                                       "10. Кружочки с цифрами под вкладкой ‘Проверка на вирусы’. Что они делают?\n\n"
                                       "Если навести курсор мышки внутрь кружочка, рядом с\n"
                                       "которым указана цифра 2, то вы откроете вторую страницу\n"
                                       "функционала нашего приложения. Повторив те же действия с кружочком 1, "
                                       "вы вернете все на исходное место.\n\n\n"
                                       "11. Как работает проверка скорости интернета?\n\n"
                                       "Если вам надо получить данные о скорости интернета, то\n"
                                       "в это вам поможет CaPi Manager. После нажатия на кнопку\n"
                                       "‘Запустить проверку скорости интернета’, примерно через\n"
                                       "20-30 секунд вы получите необходимые данные.\n"
                                       "Строчка ‘Скорость загрузки’ указывает на скорость, с которой\n"
                                       "данные из интернета загружаются на ваш компьютер.\n"
                                       "Вторая строка ‘Скорость выгрузки’ включает в себя значение\n"
                                       "скорости, с которой данные с вашего компьютера\n"
                                       "загружаются в интернет.\n\n\n"
                                       "12. Программа работает неправильно, что делать?\n\n"
                                       "Нажмите кнопку ‘Начало’, затем ‘Сообщить об ошибке’,\n"
                                       "укажите ваше имя, электронную почту и кратко опишите\n"
                                       "проблему в нижнем окне. После нажатия кнопки\n‘Отправить’, "
                                       "данные моментально будут получены\nразработчиками.")
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.abort_faq.place(x=310, y=340)
        logging.info(">>> Экран помощи отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    #Метод экрана обратной связи
    def reported(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
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
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.report_abort.place(x=230, y=340)
        self.report_send = customtkinter.CTkButton(app, text="Отправить", command=self.sending, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.report_send.place(x=400, y=340)
        logging.info(">>> Экран репорта отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    # Бекэнд отправки репорта
    def sending(self):
        try:
            ops = platform.platform()
            proc = platform.processor()
            build_inf = str([os.name, ops, proc, 'ver = 3.0.3g']).encode()
            self.h = base64.b64encode(build_inf)
            logging.info(">>> Токен сгенерирован. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            dt = str(datetime.datetime.now())[:-5].replace(' ', '--').replace(':', '-')
            tt = dt + '.txt'
            t = open(tt, 'w+')
            f = open('../../Downloads/capi_log.log')
            if '@' not in self.email.get():
                self.textbox_rep2.delete("0.0", '100.0')
                self.textbox_rep2.insert("0.0", 'E-Mail введен не корректно.\nОтсутствует символ => @\nПроверьте правильность запонения формы')
                logging.error(">>> Пользователь ввел некорректный e-mail. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
                return
            else:
                t.write(self.name.get() + '\n')
                t.write(self.email.get() + '\n')
                t.write(str(self.h) + '\n')
                t.write(self.textbox_rep2.get(0.0, 500.0))
                for i in f:
                    t.write(i)
                t.close()
                y = yadisk.YaDisk(token="y0_AgAAAABKnExBAAsEDwAAAAD1S9dHi9THbXzmRQaPuSWMbRjv_LJ4XyY")
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
            try:
                subprocess.check_call(["ping", "-c 1", "www.google.ru"])
                logging.info(">>> Проверка подключение к WWW успешно пройдена. День: %s; Точная дата и время запуска: %s",
                             current_weekday, now_dt.strftime(date_format))
            except subprocess.CalledProcessError:
                logging.error(">>> Отсутствует подключение ПК к WWW. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))

    # Бекенд удаления повторяющихся файлов из загрузок
    def povtor(self):
        self.stroka_sostoyaniya = customtkinter.CTkLabel(app, text='Выполнение запущено')
        self.stroka_sostoyaniya.place(x=250, y=200)
        try:
            def remove_duplicates(directory):
                for root, dirs, files in os.walk(directory):
                    filedict = {}
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        match = re.search(r'^(.*?)\((\d+)\)(\.[^.]*)?$', filename)
                        if match:
                            name = match.group(1)
                            number = int(match.group(2))
                            ext = match.group(3) or ''
                            if name not in filedict:
                                filedict[name] = [(number, filepath, ext)]
                            else:
                                filedict[name].append((number, filepath, ext))
                    for name in filedict:
                        files = filedict[name]
                        files.sort(key=lambda x: x[0])
                        latest = files[-1][1]
                        ext = files[-1][2]
                        for number, filepath, _ in files[:-1]:
                            os.remove(filepath)
                        os.rename(latest, os.path.join(root, f"{name}{ext}"))
            remove_duplicates(os.path.expanduser("~/Downloads"))
            self.stroka_sostoyaniya.destroy()
            self.stroka_sostoyaniya1 = customtkinter.CTkLabel(app, text='Повтряющиеся файлы удалены')
            self.stroka_sostoyaniya1.place(x=250, y=200)
            logging.info(">>> Повторяющиеся файлы удалены. День: %s; Точная дата и время запуска: %s", current_weekday,
                          now_dt.strftime(date_format))
        except Exception as e:
            self.stroka_sostoyaniya.destroy()
            self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Не найдено файлов для удаления')
            self.stroka_sostoyaniya2.place(x=250, y=200)
            logging.warning(">>> Файлов для удаления не найдено. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))

    # Бекэнд уудаления КЭШа
    def cash(self):
        try:
            self.stroka_sostoyaniya2.destroy()
            self.stroka_sostoyaniya1.destroy()
        except Exception as e:
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
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
                        print(e)
            logging.info(
                        ">>> Кэш системы удален при помощи Python. День: %s; Точная дата и время запуска: %s",
                        current_weekday,
                        now_dt.strftime(date_format))
        except Exception as e:
            os.system('del /f /s /q %temp%\*')
            logging.info(">>> Кэш системы удален при помощи консоли Windows. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='КЭШ системы удален')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    # Бекэнд удаления недавних файлов
    def recent(self):
        try:
            self.stroka_sostoyaniya2.destroy()
            self.stroka_sostoyaniya1.destroy()
        except Exception as e:
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
        self.stroka_sostoyaniya = customtkinter.CTkLabel(app, text='Выполнение запущено')
        self.stroka_sostoyaniya.place(x=250, y=200)
        try:
            temp_folders = [Path(os.environ["USERPROFILE"]) / "AppData\Local|Temp"]
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
                        pass
            logging.info(
                        ">>> Недавние файлы удалены при помощи Python. День: %s; Точная дата и время запуска: %s",
                        current_weekday,
                        now_dt.strftime(date_format))
        except Exception as e:
            os.system('del /f /s /q %systemroot%\temp\*')
            logging.info(">>> Недавние файлы удалены при помощи консоли Windows. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Недавние файлы удалены')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    # Метод вызова экрана загруженности
    def system_monitoring(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
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
        self.obnova_button = customtkinter.CTkButton(app, text="Обновить данные", command=self.system_monitoring, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.obnova_button.place(x= 300, y=220)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        logging.info(">>> Отрисовано окно мониторига системы. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update()

    # Фронтед функции выделения оперативки
    def ram(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.ram_button = customtkinter.CTkButton(app, text="Запустить выделение RAM",
                                                   command=self.allocate_memory, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
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
            d2 = list(range(10 ** 8))
            del d
            del d2
        elif ram >= 6.0 and ram <= 10.0:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            d3 = list(range(10 ** 8))
            del d
            del d2
            del d3
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

    # Максимальная производительность
    def procc(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        self.max_button = customtkinter.CTkButton(app, text="Режим Максимальной производительности",
                                                   command=self.max_boost, fg_color='#1e90ff', text_color='black', hover_color='#FF0000')
        self.max_button.place(x=260, y=100)
        self.label_max_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для включения\nмаксимальной производительности своего компьюетра')
        self.label_max_turbo.place(x=225, y=150)
        self.label_max_turbo2 = customtkinter.CTkLabel(app,
                                                      text='ВНИМАНИЕ!\nПОСЛЕ ВЫПОЛНЕНИЯ ДАННОЙ ФУНКЦИИ ПК\n'
                                                           'АВТОМАТИЧЕСКИ ОТПРАВИТСЯ В РЕЖИМ ПЕРЕЗАГРУЗКИ!\n'
                                                           'Рекомендуем закрыть все сторонние приложения')
        self.label_max_turbo2.place(x=225, y=220)

    def max_boost(self):
        subprocess.run("bcdedit /set hypervisorlaunchtype off", capture_output=True, text=True, shell=True)
        subprocess.run("Fsutil behavior set memoryusage 2", capture_output=True, text=True, shell=True)
        subprocess.run("shutdown /r /t 5", capture_output=True, text=True, shell=True)


# Запуск порграммы
if __name__ == "__main__":
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
