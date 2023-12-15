import customtkinter
import os
import re
from pathlib import *
import shutil
import smtplib
from email.message import EmailMessage
import subprocess
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Toplelewindow(customtkinter.CTkToplevel):
    def __init__(self, *args):
        super().__init__(*args)
        self.title("Успешное удаление")
        self.geometry(f"{300}x{300}")
        self.resizable(False, False)
        self.tlw_frame = customtkinter.CTkFrame(self, width=300, height=300, corner_radius=1)
        self.tlw_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.tlw_frame.grid_rowconfigure(4, weight=1)
        if args == 1:
            self.text_good = customtkinter.CTkLabel(self.tlw_frame, text='Повторяющиеся файлы удалены')
        elif args == 2:
            self.text_good = customtkinter.CTkLabel(self.tlw_frame, text='Временные файлы удалены')
        elif args == 3:
            self.text_good = customtkinter.CTkLabel(self.tlw_frame, text='КЭШ системы удален')
        else:
            self.text_good = customtkinter.CTkLabel(self.tlw_frame, text='Файлов для удаления не найдено\n или возникла '
                                                                         'oшибка во время удаления')
        self.ok_but = customtkinter.CTkButton(self.tlw_frame, text="Завершить", command=self.dest_tlw)
        self.well()

    def well(self):
        self.text_good.place(x=20, y=40)
        self.ok_but.place(x=80, y=160)

    def dest_tlw(self):
        self.destroy()


class GUI(customtkinter.CTk):
    def __init__(self,):
        self.deleted_files = []
        super().__init__()
        self.title("Space Manager")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting)
        self.sidebar_button_1.place(x=30, y=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean)

        # Дополнить методом
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Ускорение", command='')

        self.count_povtors, self.count_time_deleted, count_cash = 'povtors', 'time_del', 'kash'
        self.error_del = 'error_del'

    def destoryuing(self):
        try:
            self.textbox_start.destroy()
            self.faq_button_1.destroy()
            self.report_button_1.destroy()

            self.textbox_faq.destroy()
            self.abort_faq.destroy()

            self.label_report.destroy()
            self.name.destroy()
            self.email.destroy()
            self.textbox_rep.destroy()
            self.report_send.destroy()
            self.report_abort.destroy()

            self.del_povtor_button.destroy()
            self.del_cash_button.destroy()
            self.del_recent_button.destroy()
        except:
            pass

    def starting(self):
        self.destoryuing()
        self.sidebar_button_2.place(x=30, y=80)
        self.sidebar_button_3.place(x=30, y=120)
        self.faq_button_1 = customtkinter.CTkButton(app, text="FAQ", command=self.faq)
        self.faq_button_1.place(x=230, y=340)
        self.report_button_1 = customtkinter.CTkButton(app, text="Сообщить об ошибке", command=self.reported)
        self.report_button_1.place(x=400, y=340)
        self.textbox_start = customtkinter.CTkTextbox(master=self, width=400, height=300, corner_radius=0)
        self.textbox_start.insert("0.0", "Добро пожаловать в Space Manager\nЗдесь находится небольшой туториал "
                                   "по правильному\nиспользованию нашего софта :)\n\nВ колонке слева вы можете выбрать "
                                   "Необходимые вкладки\nс различными функциями, напрмер:\n\n   * Удаление повторяющихся "
                                   "файлов\n   * Удаление КЭШа\n   "
                                   "* Удаление недавних файлов\n   * Ускорение процессора\n   * Разгон Видеокарты\n   "
                                   "* - - - -\n\nС новыми обновлениями появятся новые "
                                   "функции :)\nЕсли у вас остались какие-то вопросы кликните по кнопке \n'FAQ' "
                                   "ниже\n\n"
                                   "P.S.Приложение находится на стадии разработки, поэтому\nпросим сообщать обо всех "
                                   "ошибках разработчикам через\nкнопку 'Сообщить об ошибке'")
        self.textbox_start.place(x=200, y=0)

    def clean(self):
        self.destoryuing()
        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor)
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                         command=self.cash)
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить недавние файлы",
                                                         command=self.recent)
        self.del_povtor_button.place(x=250, y=50)
        self.del_cash_button.place(x=250, y=100)
        self.del_recent_button.place(x=250, y=150)

    def faq(self):
        self.destoryuing()
        self.textbox_faq = customtkinter.CTkTextbox(master=self, width=400, height=300, corner_radius=0)
        self.textbox_faq.insert("0.0", "Проба faq")
        self.textbox_faq.place(x=200, y=0)
        self.abort_faq = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.abort_faq.place(x=310, y=340)

    def reported(self):
        self.destoryuing()
        self.label_report = customtkinter.CTkLabel(app, text='Сообщение о проблеме:')
        self.label_report.place(x=300, y=10)
        self.name = customtkinter.CTkEntry(app, placeholder_text="Ваше имя")
        self.name.place(x=300, y=50)
        self.email = customtkinter.CTkEntry(app, placeholder_text="Ваш e-mail")
        self.email.place(x=300, y=80)
        self.textbox_rep = (customtkinter.CTkTextbox(app, width=300, height=200))
        self.textbox_rep.insert("0.0", "Опишите свою проблему")
        self.textbox_rep.place(x=230, y=120)
        self.report_send = customtkinter.CTkButton(app, text="Отправить", command=self.sending)
        self.report_send.place(x=400, y=340)
        self.report_abort = customtkinter.CTkButton(app, text="Назад", command=self.starting)
        self.report_abort.place(x=230, y=340)
    #         stepan.2006.dip@gmail.com

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
            self.top_lvl = Toplelewindow(1)
        except:
            self.top_lvl = Toplelewindow(0)

    def cash(self):
        del_dir = r'c:\windows\temp'
        pObj = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        rCod = pObj.returncode
        if rCod == 0:
            self.top_lvl = Toplelewindow(2)
            self.top_lvl.focus()
        else:
            self.top_lvl = Toplelewindow(0)
            self.top_lvl.focus()

    def recent(self):
        try:
            os.remove(r'C:\Users' + '\\' + str(os.getlogin()) + '\AppData\Local\Temp')
            self.top_lvl = Toplelewindow(3)
            self.top_lvl.focus()
        except:
            self.top_lvl = Toplelewindow(0)
            self.top_lvl.focus()


if __name__ == "__main__":
    app = GUI()
    app.mainloop()