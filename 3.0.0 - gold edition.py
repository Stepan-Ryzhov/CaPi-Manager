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
import socket
from speedtest import Speedtest
from PIL import Image


def custom(app_theme):
    customtkinter.set_appearance_mode(app_theme)


customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme("dark-blue")


class GUI(customtkinter.CTk):
    def __init__(self,):
        self.new_signatures = False
        self.deleted_files = []
        super().__init__()
        self.init_start_GUI()
        self.title("CaPi Manager")
        self.geometry(f"{605}x{400}")
        self.resizable(False, False)
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect(('127.0.0.1', 53210))
            client_sock.sendall(b'test')
            data = client_sock.recv(333)
            if data == b'true':
                t = open('_internal/signatures.txt', 'a')
                t.write('\n')
                self.new_signatures = True
                self.init_start_GUI()
        except:
            pass
            logging.error(">>> Сервер отключен. День: %s; Точная дата и время запуска: %s",
                              current_weekday, now_dt.strftime(date_format))


    def init_start_GUI(self):
        self.th = 'Светлая'
        self.rh = 1
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting, fg_color='gold', text_color='black', hover_color='#CCCC00')
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
        self.vers_label = customtkinter.CTkLabel(self.sidebar_frame, text='GOLD EDITION', font=self.vers_label_font, text_color='#CCCC00')
        self.vers_label.place(x=15, y=340)
        logging.info(">>> Первая отрисовка боковой панели. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    def init_GUI(self):
        self.rh = self.rh
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean, fg_color='gold', text_color='black', hover_color='#CCCC00')

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Загруженность ПК",
                                                        command=self.system_monitoring, fg_color='gold', text_color='black', hover_color='#CCCC00')

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Выделение RAM",
                                                        command=self.ram, fg_color='gold', text_color='black', hover_color='#CCCC00')

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Проверка на вирусы",
                                                        command=self.procc, fg_color='gold', text_color='black', hover_color='#CCCC00')

        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Проверка скорости\nинтернета",
                                                        command=self.www_check, fg_color='gold', text_color='black',
                                                        hover_color='#CCCC00')


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

    def radiobutton_callback(self):
        a = self.radio_var.get()
        if a == 1:
            try:
                self.sidebar_button_6.place_forget()
                self.sidebar_button_2.place(x=30, y=80)
                self.sidebar_button_3.place(x=30, y=120)
                self.sidebar_button_4.place(x=30, y=160)
                self.sidebar_button_5.place(x=30, y=200)
                self.rh = 1
            except:
                pass
        elif a == 2:
            try:
                self.sidebar_button_2.place_forget()
                self.sidebar_button_3.place_forget()
                self.sidebar_button_4.place_forget()
                self.sidebar_button_5.place_forget()
                self.sidebar_button_6.place(x=30, y=80)
                self.rh = 2
            except:
                pass

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


    def starting(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.faq_button_1 = customtkinter.CTkButton(app, text="FAQ", command=self.faq, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.faq_button_1.place(x=230, y=340)
        self.report_button_1 = customtkinter.CTkButton(app, text="Сообщить об ошибке", command=self.reported, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.report_button_1.place(x=400, y=340)
        self.textbox_start = customtkinter.CTkTextbox(master=self, width=410, height=300, corner_radius=0)
        self.textbox_start.insert("0.0", "Спасибо за преобретение CaPi Manager GOLD EDITION\n"
                                   "\nВ колонке слева вы можете выбрать "
                                   "необходимые вкладки \nс различными функциями, напрмер:\n\n   * Удаление повторяющихся "
                                   "файлов\n   * Удаление КЭШа\n   "
                                   "* Удаление временных файлов\n   * Проверка загруженности ПК\n   * Выделение оперативной памяти\n   "
                                    "* Проверка на вирусы\n   "
                                   "\nС новыми обновлениями появятся новые "
                                   "функции :)\nЕсли у вас остались какие-то вопросы кликните по кнопке \n'FAQ' "
                                   "ниже\n\n"
                                   "P.S.Приложение находится на стадии разработки, поэтому\nпросим сообщать обо всех "
                                   "ошибках разработчикам через\nкнопку 'Сообщить об ошибке'")
        self.textbox_start.place(x=200, y=0)

        logging.info(">>> Начальный экран с текстом отрисован. День: %s; Точная дата и время запуска: %s",
                     current_weekday, now_dt.strftime(date_format))

    def clean(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить временные файлы",
                                                         command=self.recent, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.del_povtor_button.place(x=250, y=50)
        self.del_cash_button.place(x=250, y=100)
        self.del_recent_button.place(x=250, y=150)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        logging.info(">>> Экран очистки отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    def faq(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.textbox_faq = customtkinter.CTkTextbox(master=self, width=400, height=300, corner_radius=0)
        self.textbox_faq.insert("0.0", "1. Безопасно ли использовать это приложение?\n\n"
                               "Наше приложение проверено двумя известными\nантивирусами и не содержит "
                               "каких-либо вредоносных\nскриптов. Команда разработчиков уверяет,"
                               "что приложение\nбезопасно на все 100%\n\n\n"
                               "2. Если я проведу очистку недавних файлов и КЭШа \nсистемы удаляться ли"
                               "важные для меня файлы?\n\n"
                               "Безусловно, нет! Наша программа удалит ненужные\nсистемные файлы,"
                               "которые загружают память и процессор\nвашего компьютера\n\n\n"
                               "3. Не опасно ли удалять системные файлы? Вдруг\nпрограмма удалит что-то не то, "
                               "и компьютер перестанет\nработать?\n\n"
                               "Программа не удаляет необходимые для работы файлы\nОперационной системы\n\n"
                               "4. Что такое RAM?\n\n"
                               "RAM - это оперативная память, за счет которой компьютер\nможет что-либо выполнять.\n\n\n"
                               "5. Программа зависла во время выделения RAM,\nчто делать?\n\n"
                               "Ничего страшного! Программа выделяет дополнительную\nRAM за счет блокировки фоновых процессов."
                               "Обычно это\nзанимает примерно 30 секунд. Стоит просто немного\nподождать :)\n\n\n"
                               "6. Как долго программа будет проверять мой ПК на вирусы?\n\n"
                                "Все зависит от количества файлов на вашем компьютере.\nЧем их больше, тем дольше CaPi "
                                       "Manager будет проводить\nпроверку\n\n\n"
                                "7. "
)
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.abort_faq.place(x=310, y=340)
        logging.info(">>> Экран помощи отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

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
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.report_abort.place(x=230, y=340)
        self.report_send = customtkinter.CTkButton(app, text="Отправить", command=self.sending, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.report_send.place(x=400, y=340)
        logging.info(">>> Экран репорта отрисован. День: %s; Точная дата и время запуска: %s", current_weekday,
                     now_dt.strftime(date_format))

    def sending(self):
        try:
            ops = platform.platform()
            proc = platform.processor()
            build_inf = str([os.name, ops, proc, 'ver = 2.0.7']).encode()
            self.h = base64.b64encode(build_inf)
            logging.info(">>> Токен сгенерирован. День: %s; Точная дата и время запуска: %s", current_weekday,
                         now_dt.strftime(date_format))
            dt = str(datetime.datetime.now())[:-5].replace(' ', '--').replace(':', '-')
            tt = dt + '.txt'
            t = open(tt, 'w+')
            f = open('capi_log.log')
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
            temp_folders = ['C:\\Users\\admin\\AppData\\Local\\Temp']
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

    def system_monitoring(self):
        for widget in app.winfo_children():
            widget.destroy()
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        self.init_GUI()
        self.system_mon_2()

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
        self.obnova_button = customtkinter.CTkButton(app, text="Обновить данные", command=self.system_monitoring, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.obnova_button.place(x= 300, y=220)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        logging.info(">>> Отрисовано окно мониторига системы. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update()

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
                                                   command=self.allocate_memory, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.ram_button.place(x=300, y=100)
        self.label_ram_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для выделения оперативной памяти')
        self.end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.label_ram_turbo2 = customtkinter.CTkLabel(app, text='Успешно выделена дополнительная RAM', font=self.end_font)
        self.label_ram_turbo.place(x=215, y=150)
        logging.info(">>> Отрисовано окно выделения RAM. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    def allocate_memory(self):
        ram = str(psutil.virtual_memory()[0])
        ram = int(ram)/1024/1024/1024
        if ram > 1.7 and ram < 2.2:
            d = list(range(10**8))
            del d
        elif ram > 3.7 and ram < 4.2:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            del d
            del d2
        elif ram > 7.7 and ram < 8.2:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            d3 = list(range(10 ** 8))
            del d
            del d2
            del d3
        elif ram > 15.7 and ram < 16.2:
            d = list(range(10 ** 8))
            d2 = list(range(10 ** 8))
            d3 = list(range(10 ** 8))
            d4 = list(range(10 ** 8))
            del d
            del d2
            del d3
            del d4
        elif ram > 30.0 and ram < 34.0:
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
        self.label_ram_turbo2.place(x=265, y=150)
        logging.info(">>> RAM выделена. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    def procc(self):
        for widget in app.winfo_children():
            widget.destroy()
        try:
            self.label_final_scan.destroy()
        except:
            pass
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.procc_button = customtkinter.CTkButton(app, text="Запустить проверку на вирусы",
                                                   command=self.start_scanning, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.procc_button.place(x=280, y=100)

        self.label_procc_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для проверки\nПК на '
                                                                  'наличие вирусов')

        self.label_procc_turbo.place(x=270, y=150)
        self.drives = win32api.GetLogicalDriveStrings()
        self.dirs = self.drives.split('\000')[:-1]

        self.combo_vars = customtkinter.StringVar(value="C:/")
        self.combobox11 = customtkinter.CTkComboBox(app, values=self.dirs, variable=self.combo_vars)
        self.combobox11.place(x=310, y=40)

        if self.new_signatures:
            self.supdate_button = customtkinter.CTkButton(app, text="Обновить вирусную базу",
                                                            command=self.signatures_update, fg_color='gold',
                                                            text_color='black', hover_color='#CCCC00')
            self.supdate_button.place(x=300, y=300)
            self.supdate_label = customtkinter.CTkLabel(app, text='Рекoмендуем обновить вирусную базу')

            self.supdate_label.place(x=270, y=260)
        logging.info(">>> Окно антивируса отрисовано. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        app.update()

    def start_scanning(self):
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
        self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}.'
                                                                   f' Найдено вирусов:{self.counter1}')
        self.label_procc_turbo2.place(x=250, y=240)

        self.scan_end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.scan_end = customtkinter.CTkLabel(app, text='Сканирование завершено', font=self.scan_end_font)
        self.scan_abort = customtkinter.CTkLabel(app, text='Сканирование прервано', font=self.scan_end_font)
        self.procc_button.destroy()
        self.abort_button = customtkinter.CTkButton(app, text="Остановить проверку на вирусы",
                                                    command=self.abort_scanning, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.abort_button.place(x=280, y=100)
        self.aborting = False

        logging.info(">>> Сканирование запущенно. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))
        self.scan_directory(self.combobox11.get())
        self.abort_button.destroy()
        self.label_procc_turbo2.destroy()
        self.label_final_scan = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}. '
                                                                 f'Найдено вирусов:{self.counter1}')
        self.label_final_scan.place(x=250, y=240)
        self.scan_end.place(x=300, y=200)
        logging.info(">>> Сканирование завершенно системой. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    def scan_file(self):
        if self.aborting:
            self.label_final_scan = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}. '
                                                                     f'Найдено вирусов:{self.counter1}')
            self.label_procc_turbo2.place_forget()
            self.abort_button.destroy()
            self.label_final_scan.place(x=250, y=240)
            self.scan_abort.place(x=300, y=200)
            return
        print(self.file_path)
        try:
            self.label_procc_turbo2.destroy()
            self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}.'
                                                                       f' Найдено вирусов:{self.counter1}')

            self.label_procc_turbo2.place(x=250, y=210)
            with open(self.file_path, 'rb') as file:
                content = file.read()
                hash_sum = hashlib.md5(content).hexdigest()
            if hash_sum in self.malicious_hashes:
                self.counter1 += 1
            else:
                self.counter2 += 1
            if self.counter1 == 1:
                self.danger_path = self.file_path
                self.virus_label = customtkinter.CTkLabel(app, text='Найден файл с вирусом', text_color='red')

                self.virus_label.place(x=310, y=260)
                self.virus_button = customtkinter.CTkButton(app, text="Удалить файл с вирусом",
                                                            command=self.virus_remove, fg_color='gold', text_color='black', hover_color='#CCCC00')
                self.virus_button.place(x=300, y=300)
                self.virus_path = self.file_path
        except Exception as e:
            logging.error(">>>" + str(e) + ". День: %s; Точная дата и время запуска: %s",
                          current_weekday, now_dt.strftime(date_format))
            self.counter2 += 0
        app.update()

    def scan_directory(self, directory):
        if self.aborting:
            return
        for root, dirs, files in os.walk(directory):
            for file in files:
                self.file_path = os.path.join(root, file)
                self.scan_file()
                app.update()

    def virus_remove(self):
        os.remove(self.danger_path)
        self.counter1 = 0
        self.danger_path = ''

    def abort_scanning(self):
        self.aborting = True
        logging.info(">>> Сканирование приостановленно пользователем. День: %s; Точная дата и время запуска: %s",
                     current_weekday,
                     now_dt.strftime(date_format))

    def signatures_update(self):
        self.supdate_button.place_forget()
        self.supdate_label.place_forget()
        self.supdate_label = customtkinter.CTkLabel(app, text='Обновление началось\nНе закрывайте вкладку '
                                                              '"Проверка на вирусы"')

        self.supdate_label.place(x=280, y=260)
        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect(('127.0.0.1', 53210))
            client_sock.sendall(b'connection')
            t = open('_internal/signatures.txt', 'a')
            for i in range(2000):
                try:
                    data = client_sock.recv(333)
                    d = str(data)[2:-1]
                    if data != b'':
                        t.write(d + '\n')
                except:
                    client_sock.close()
            client_sock.close()
            t.close()
            self.supdate_label.place_forget()
            self.supdate_label = customtkinter.CTkLabel(app, text='Обновление завершено')
            self.supdate_label.place(x=310, y=260)
            logging.info(">>> Сигнатуры обновлены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))
        except:
            self.supdate_label.place_forget()
            self.supdate_label = customtkinter.CTkLabel(app,
                                                        text='Невозможно установить обновления.\nПопробуйте позже')

            self.supdate_label.place(x=310, y=260)
            logging.error(">>> Хз, но не обновяться сигнатурки :(. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

    def www_check(self):
        for widget in app.winfo_children():
            widget.destroy()
        try:
            self.label_final_scan.destroy()
        except:
            pass
            logging.info(">>> Виджеты удалены. День: %s; Точная дата и время запуска: %s",
                         current_weekday,
                         now_dt.strftime(date_format))

        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.www_button = customtkinter.CTkButton(app, text="Запустить проверку скорости интернета",
                                                   command=self.start_check_www, fg_color='gold', text_color='black', hover_color='#CCCC00')
        self.www_button.place(x=265, y=100)

        self.www_label = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для проверки\nскорости интернета и '
                                                          'подождите появления результатов')

        self.www_label.place(x=220, y=150)

    def start_check_www(self):
        try:
            st = Speedtest()
            ds = round(int(st.download()) / 1000000, 2)
            us = round(int(st.upload()) / 1000000, 2)
            self.dont_con_label = customtkinter.CTkLabel(app, text=f'Нет подключения к интернету :(')
            self.www_label.place_forget()
            self.www_button.place_forget()
            try:
                self.dont_con_label.place_forget()
            except:
                pass
            self.ds_label = customtkinter.CTkLabel(app, text=f'Скорость загрзки:{ds} Мбит/с')
            self.us_label = customtkinter.CTkLabel(app, text=f'Скорость выгрузки:{us} Мбит/с')
            self.ds_label.place(x=300, y=100)
            self.us_label.place(x=300, y=130)
        except Exception as e:
            self.dont_con_label.place(x=300, y=200)


if __name__ == "__main__":
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
    app = GUI()
    app.mainloop()
    app.quit()
