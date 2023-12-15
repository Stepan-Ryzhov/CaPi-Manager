import time
import customtkinter
import os
import re
import smtplib
from email.message import EmailMessage
import subprocess
import psutil
import gc
import platform
import base64
import shutil


def custom(a):
    customtkinter.set_appearance_mode(a)
    # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(customtkinter.CTk):
    def __init__(self,):
        self.deleted_files = []
        super().__init__()
        self.init_start_GUI()
        self.title("Windows Manager")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)

    def init_start_GUI(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting)
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean)

        # Дополнить методом
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Загруженность ПК",
                                                        command=self.system_monitoring)

        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value="Светлая")
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Светлая", "Темная", "Как в системе"],
                                                  command=self.combobox_callback, variable=self.combobox_var)
        self.combobox_var.set("Светлая")
        self.combobox.place(x=30, y=300)

    def init_GUI(self):

        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting)
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean)
        self.sidebar_button_2.place(x=30, y=80)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Загруженность ПК",
                                                        command=self.system_monitoring)
        self.sidebar_button_3.place(x=30, y=120)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Выделение RAM",
                                                        command=self.ram)
        self.sidebar_button_4.place(x=30, y=160)

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Разгон процессора",
                                                        command=self.procc)
        self.sidebar_button_5.place(x=30, y=200)

        self.theme_lable = customtkinter.CTkLabel(self.sidebar_frame, text='Тема приложения:')
        self.theme_lable.place(x=30, y=270)

        self.combobox_var = customtkinter.StringVar(value="Светлая")
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=["Светлая", "Темная", "Как в системе"],
                                             command=self.combobox_callback, variable=self.combobox_var)
        self.combobox_var.set("Светлая")
        self.combobox.place(x=30, y=300)

    def combobox_callback(self, choice):
        self.combobox_var.set(choice)
        if choice == 'Светлая':
            custom('Light')
        elif choice == 'Как в системе':
            custom('System')
        else:
            custom('Dark')


    def starting(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.faq_button_1 = customtkinter.CTkButton(app, text="FAQ", command=self.faq)
        self.faq_button_1.place(x=230, y=340)
        self.report_button_1 = customtkinter.CTkButton(app, text="Сообщить об ошибке", command=self.reported)
        self.report_button_1.place(x=400, y=340)
        self.textbox_start = customtkinter.CTkTextbox(master=self, width=410, height=300, corner_radius=0)
        self.textbox_start.insert("0.0", "Добро пожаловать в Windows Manager\nЗдесь находится небольшой туториал "
                                   "по правильному\nиспользованию нашего софта :)\n\nВ колонке слева вы можете выбрать "
                                   "Необходимые вкладки \nс различными функциями, напрмер:\n\n   * Удаление повторяющихся "
                                   "файлов\n   * Удаление КЭШа\n   "
                                   "* Удаление недавних файлов\n   * Проверка загруженности ПК\n   * Выделение оперативной памяти\n   "
                                    "* Ускорение процессора\n   "
                                   "\nС новыми обновлениями появятся новые "
                                   "функции :)\nЕсли у вас остались какие-то вопросы кликните по кнопке \n'FAQ' "
                                   "ниже\n\n"
                                   "P.S.Приложение находится на стадии разработки, поэтому\nпросим сообщать обо всех "
                                   "ошибках разработчикам через\nкнопку 'Сообщить об ошибке'")
        self.textbox_start.place(x=200, y=0)

    def clean(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor)
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash)
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить недавние файлы",
                                                         command=self.recent)
        self.del_povtor_button.place(x=250, y=50)
        self.del_cash_button.place(x=250, y=100)
        self.del_recent_button.place(x=250, y=150)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)


    def faq(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.textbox_faq = customtkinter.CTkTextbox(master=self, width=400, height=300, corner_radius=0)
        self.textbox_faq.insert("0.0", "1. Безопастно ли использовать это приложение?\n\n"
                                       "Наше приложение проверенно двумя известными\nантивирусами и не содержит "
                                       "каких-либо вредоностных\nскриптов. Команда разработчиков уверяет, "
                                       "что приложение\nбезопастно на все 100%\n\n\n"
                                       "2. Если я проведу очистку недавних файлов и КЭШа системы\nудаляться ли "
                                       "важные для меня файлы?\n\n"
                                       "Безусловно, нет! Наша программа удалит ненужные\nсистемные файлы, "
                                       "которые загружают память и процессор\nвашего компьютера\n\n\n"
                                       "3. Не опасно ли удалять системные файлы? Вдруг программа\nудалит что-то не то, "
                                       "и компьютер перестанет работать?\n\n"
                                       "Программа не удаляет необходимые для работы файлы\nОперационной системы\n\n\n"
                                       "4. Что такое RAM?\n\n"
                                       "RAM - это оперативная память, за счет которой компьютер\nможет что-либо выполнять\n\n\n"
                                       "5. Программа зависла во время выделения RAM, что делать?\n\n"
                                       "Ничего страшного! Программа выделяет дополнительную\nRAM за счет блокировки фоновых процессов."
                                       "Обычно это\nзанимает примерно 30 секунд. Стоит просто немного\nподождать :)\n\n\n"
                                       "6. Не опасно выполнять ускорение процессора для моего\nкомпьютера?\n\n"
                                       "Ускорение процессора не приведет ни к чему плохому.\n"
                                       "Программа была протестированна множество раз и не\n"
                                       "вызывала никаких технических нареканий")
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.abort_faq.place(x=310, y=340)

    def reported(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        build_inf = str([os.name, platform.platform(), platform.processor(), 'ver = 0.1.6']).encode()
        h = base64.b64encode(build_inf)

        self.label_report = customtkinter.CTkLabel(app, text='Пока мы работаем над созданием формы обратной связи,\nвы '
                                                             'можете отправить сообщение о возникшей у вас ошибке\nна '
                                                             'электронную почту capi.manager.sup@gmail.com.\n'
                                                             'В тексте письма просим указать токен\n(который вы можете скопировть ниже)\n'
                                                             'и краткое описание проблемы, с которой вы столкнулись')
        self.label_report.place(x=210, y=10)
        self.textbox_rep = (customtkinter.CTkTextbox(app, width=300, height=200))
        self.textbox_rep.insert("0.0", h)
        self.textbox_rep.place(x=230, y=120)
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.report_abort.place(x=310, y=340)

    def sending(self):
        # Доделать !!!
        msg = EmailMessage()
        print(self.textbox_rep.get(0.0, 200.0))
        msg.set_content(self.textbox_rep.get(0.0, 200.0))
        msg['Subject'] = f'Репорт от пользователя'
        msg['From'] = self.email.get()
        msg['To'] = 'stepan.2006.dip@yandex.ru'
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    def povtor(self):
        try:
            self.stroka_sostoyaniya2.destroy()
            self.stroka_sostoyaniya1.destroy()
        except:
            pass
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
                            print(f"Deleted duplicate file: {filepath}")
                            os.remove(filepath)
                        os.rename(latest, os.path.join(root, f"{name}{ext}"))
                        print(f"Renamed {latest} to {name}{ext}")
            remove_duplicates(os.path.expanduser("~/Downloads"))
            self.stroka_sostoyaniya.destroy()
            self.stroka_sostoyaniya1 = customtkinter.CTkLabel(app, text='Повтряющиеся файлы удалены')
            self.stroka_sostoyaniya1.place(x=250, y=200)
        except:
            self.stroka_sostoyaniya.destroy()
            self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Не найдено файлов для удаления')
            self.stroka_sostoyaniya2.place(x=250, y=200)


    def cash(self):
        try:
            self.stroka_sostoyaniya2.destroy()
            self.stroka_sostoyaniya1.destroy()
        except:
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
                        print(e)
        except:
            os.system('del /f /s /q %temp%\*')
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='КЭШ системы удален')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    def recent(self):
        try:
            self.stroka_sostoyaniya2.destroy()
            self.stroka_sostoyaniya1.destroy()
        except:
            pass
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
                        print(e)
        except:
            os.system('del /f /s /q %systemroot%\temp\*')
        self.stroka_sostoyaniya.destroy()
        self.stroka_sostoyaniya2 = customtkinter.CTkLabel(app, text='Недавние файлы удалены')
        self.stroka_sostoyaniya2.place(x=250, y=200)

    def system_monitoring(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        cpu_usage = 'Загрузка процессора:' + str(psutil.cpu_percent()) + '%'
        memory_usage = 'Загрузка оперативной памяти:' + str(psutil.virtual_memory().percent) + '%'
        disk_usage = 'Загрузка жесткого диска:' + str(psutil.disk_usage("/").percent) + '%'
        self.label_cpu_usage = customtkinter.CTkLabel(app, text=cpu_usage)
        self.label_cpu_usage.place(x=250, y=50)
        self.label_memory_usage = customtkinter.CTkLabel(app, text=memory_usage)
        self.label_memory_usage.place(x=250, y=100)
        self.label_disk_usage = customtkinter.CTkLabel(app, text=disk_usage)
        self.label_disk_usage.place(x=250, y=150)
        self.obnova_button = customtkinter.CTkButton(app, text="Обновить данные", command=self.system_monitoring)
        self.obnova_button.place(x= 300, y=220)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

    def ram(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.ram_button = customtkinter.CTkButton(app, text="Запустить выделение RAM",
                                                   command=self.allocate_memory)
        self.ram_button.place(x=300, y=100)
        self.label_ram_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для выделения оперативной памяти')
        self.label_ram_turbo2 = customtkinter.CTkLabel(app, text='Успешно выделена дополнительная RAM')
        self.label_ram_turbo.place(x=215, y=150)

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
        gc.collect()
        self.label_ram_turbo.destroy()
        self.ram_button.destroy()
        self.label_ram_turbo2.place(x=265, y=150)

    def procc(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)

        self.procc_button = customtkinter.CTkButton(app, text="Запустить ускорение процессора",
                                                   command=self.adskiy_razgon)
        self.procc_button.place(x=280, y=100)

        self.label_procc_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для ускорения процессора')
        self.label_procc_turbo2 = customtkinter.CTkLabel(app, text='Успешное ускорение работы процессора')
        self.label_procc_turbo.place(x=250, y=150)

    def adskiy_razgon(self):
        psutil.cpu_times_percent(interval=1)
        self.label_procc_turbo.destroy()
        self.procc_button.destroy()
        self.label_procc_turbo2.place(x=265, y=150)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()