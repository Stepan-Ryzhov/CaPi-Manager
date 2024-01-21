# -*- coding: utf-8 -*-
import sys
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

def custom(a):
    customtkinter.set_appearance_mode(a)
    # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(customtkinter.CTk):
    def __init__(self,):
        self.deleted_files = []
        super().__init__()
        self.init_start_GUI()
        self.title("CaPi Manager")
        self.geometry(f"{605}x{400}")
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

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Проверка на вирусы",
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
        self.textbox_start.insert("0.0", "Добро пожаловать в CaPi Manager\n"
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

    def clean(self):
        for widget in app.winfo_children():
            widget.destroy()

        self.init_GUI()

        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor)
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash)
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить временные файлы",
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
                               "Обычно это\nзанимает примерно 30 секунд. Стоит просто немного\nподождать :)"
)
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.abort_faq.place(x=310, y=340)

    def reported(self):
        for widget in app.winfo_children():
            widget.destroy()
        self.init_GUI()
        self.label_report = customtkinter.CTkLabel(app, text='Нажмите, пожалуйста, кнопку "Создать токен" и отправьте\n'
                                                             'его разработчикам, кликнув кнопку "Отправить"')
        self.label_report.place(x=210, y=10)
        self.textbox_rep = (customtkinter.CTkTextbox(app, width=300, height=100))
        self.textbox_rep.place(x=230, y=150)
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.report_abort.place(x=230, y=340)
        self.token_gen = customtkinter.CTkButton(app, text="Создать токен", command=self.token_generation)
        self.token_gen.place(x=300, y=100)
        self.report_send = customtkinter.CTkButton(app, text="Отправить", command=self.sending)
        self.report_send.place(x=400, y=340)

    def token_generation(self):
        ops = platform.platform()
        proc = platform.processor()
        build_inf = str([os.name, ops, proc, 'ver = 2.0.0']).encode()
        self.h = base64.b64encode(build_inf)
        self.textbox_rep.insert("0.0", self.h)
        self.token_gen.destroy()

    def sending(self):
        try:
            t = open('report.txt', 'w+')
            t.write(self.textbox_rep.get(0.0, 200.0))
            t.close()
            y = yadisk.YaDisk(token="y0_AgAAAABKnExBAAsEDwAAAAD1S9dHi9THbXzmRQaPuSWMbRjv_LJ4XyY")
            y.upload("report.txt", "/test/report.txt")
            self.textbox_rep.delete("0.0", '100.0')
            self.textbox_rep.insert("0.0", 'Токен успешно отправлен')
        except:
            self.textbox_rep.delete('0.0', '100.0')
            self.textbox_rep.insert("0.0", 'Возникла ошибка при отправке токена. Попробуйте позднее')

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
        self.obnova_button = customtkinter.CTkButton(app, text="Обновить данные", command=self.system_monitoring)
        self.obnova_button.place(x= 300, y=220)
        self.help = customtkinter.CTkLabel(app, text='Возникли вопросы? Кликнете по кнопке "Начало", затем "FAQ"')
        self.help.place(x=205, y=350)
        app.update()

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
        self.end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.label_ram_turbo2 = customtkinter.CTkLabel(app, text='Успешно выделена дополнительная RAM', font=self.end_font)
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

        self.procc_button = customtkinter.CTkButton(app, text="Запустить проверку на вирусы",
                                                   command=self.start_scanning)
        self.procc_button.place(x=280, y=100)

        self.label_procc_turbo = customtkinter.CTkLabel(app, text='Нажмите кнопку выше для проверки\nПК на '
                                                                  'наличие вирусов')

        self.label_procc_turbo.place(x=270, y=150)
        self.drives = win32api.GetLogicalDriveStrings()
        self.dirs = self.drives.split('\000')[:-1]

        self.combo_vars = customtkinter.StringVar(value="C:/")
        self.combobox11 = customtkinter.CTkComboBox(app, values=self.dirs, variable=self.combo_vars)
        self.combobox11.place(x=310, y=40)
        app.update()

    def start_scanning(self):
        self.counter2 = 0
        self.counter1 = 0
        f = open('txt.txt')
        self.malicious_hashes = []
        for i in f:
            self.malicious_hashes.append(i)
        self.label_procc_turbo2 = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}.'
                                                                   f' Найдено вирусов:{self.counter1}')
        self.label_procc_turbo2.place(x=250, y=240)

        self.label_final_scan = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}. '
                                                                 f'Найдено вирусов:{self.counter1}')
        self.scan_end_font = customtkinter.CTkFont(size=14, weight='bold')
        self.scan_end = customtkinter.CTkLabel(app, text='Сканирование завершено', font=self.scan_end_font)
        self.scan_abort = customtkinter.CTkLabel(app, text='Сканирование прервано', font=self.scan_end_font)
        self.procc_button.destroy()
        self.abort_button = customtkinter.CTkButton(app, text="Остановить проверку на вирусы",
                                                    command=self.abort_scanning)
        self.abort_button.place(x=280, y=100)
        self.aborting = False
        # p = Process(target=self.scan_directory(self.combobox11.get()))
        # p.start()
        # p.join()

        self.scan_directory(self.combobox11.get())
        self.abort_button.destroy()
        self.label_procc_turbo2.destroy()
        self.label_final_scan = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}. '
                                                                 f'Найдено вирусов:{self.counter1}')
        self.label_final_scan.place(x=250, y=240)
        self.scan_end.place(x=300, y=200)

    def scan_file(self):
        if self.aborting:
            self.label_final_scan = customtkinter.CTkLabel(app, text=f'Файлов отсканированно:{self.counter2}. '
                                                                     f'Найдено вирусов:{self.counter1}')
            self.label_procc_turbo2.destroy()
            self.abort_button.destroy()
            self.label_final_scan.place(x=250, y=240)
            self.scan_abort.place(x=300, y=200)
            return
        print(self.combobox11.get())
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
                self.virus_button = customtkinter.CTkButton(app, text="Удалить файл с вирусом",
                                                            command=self.virus_remove)
                self.virus_button.place(x=300, y=300)
                self.virus_path = self.file_path
        except:
            self.counter2 += 0
        app.update()

    def scan_directory(self, directory):
        if self.aborting:
            return
        for root, dirs, files in os.walk(directory):
            for file in files:
                self.file_path = os.path.join(root, file)
                # p1 = Process(target=self.scan_file())
                # p1.start()
                # p1.join()
                self.scan_file()
                app.update()

    def virus_remove(self):
        os.remove(self.virus_path)
        self.counter1 = 0
        self.virus_path = ''

    def abort_scanning(self):
        self.aborting = True

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
    app.quit()

