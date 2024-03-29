import pathlib

import customtkinter
import os
import re
import shutil
from pathlib import *
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Голосовой помощник")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=400, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Начало", command=self.starting)
        self.sidebar_button_1.place(x=30, y=20)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Очистка", command=self.clean)
        self.sidebar_button_2.place(x=30, y=80)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Ускорение", command='')
        self.sidebar_button_1.place(x=30, y=120)

    def starting(self):
        self.textbox = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.insert("0.0", "Добро пожаловать в приложение test\nЗдесь находится небольшой туториал "
                                   "по правильному\nиспользованию нашего софта :)\n\nВ колонке слева вы можете выбрать "
                                   "Необходимые вкладки\nс различными функциями, напрмер:\n   * test\n   * test\n   "
                                   "* test\n   * test\n   * test\n   * test\nС новыми обновлениями появятся новые "
                                   "функции :)\nЕсли у вас остались какие-то вопросы кликните по кнопке \n'FAQ' ниже\n\n"
                                   "P.S.Приложение находится на стадии разработки, посему\nпросим сообщать обо всех "
                                   "ошибках разработчикам через\nкнопку 'Сообщить об ошибке'")
        self.textbox.place(x=200, y=0)
        self.del_povtor_button = customtkinter.CTkButton(app, text="Удалить повторяющиеся файлы",
                                                         command=self.povtor)
        self.del_cash_button = customtkinter.CTkButton(app, text="Удалить кэш-файлы",
                                                       command=self.cash)
        self.del_recent_button = customtkinter.CTkButton(app, text="Удалить недавние файлы",
                                                         command=self.recent)

    def clean(self):
        try:
            self.textbox.destroy()
            self.del_povtor_button.place(x=250, y=50)
            self.del_cash_button.place(x=250, y=100)
            self.del_recent_button.place(x=250, y=150)
        except:
            self.del_povtor_button.place(x=250, y=50)
            self.del_cash_button.place(x=250, y=100)
            self.del_recent_button.place(x=250, y=150)

    def povtor(self):
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
                    print(files)
                    latest = files[-1][1]
                    ext = files[-1][2]
                    for number, filepath, _ in files[:-1]:
                        print(f"Deleted duplicate file: {filepath}")
                        os.remove(filepath)
                    os.rename(latest, os.path.join(root, f"{name}{ext}"))
                    print(f"Renamed {latest} to {name}{ext}")
        remove_duplicates(os.path.expanduser("~/Downloads"))

    def cash(self):
        temp_directories = [
            '/private/var/folders',
            '~/Library/Caches',
            '~/Library/Logs',
            '~/Downloads',
            '~/Desktop'
        ]
        extensions = [
            '.log',
            '.cache',
            '.tmp',
            '.dmg',
            '.pkg'
        ]
        for directory in temp_directories:
            for dirpath, dirnames, filenames in os.walk(os.path.expanduser(directory)):
                for filename in filenames:
                    if os.path.splitext(filename)[1].lower() in extensions:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            if os.path.isfile(filepath):
                                os.remove(filepath)
                            elif os.path.isdir(filepath):
                                shutil.rmtree(filepath)
                            print(f"Removed {filepath}")
                        except Exception as e:
                            print(f"Error deleting {filepath}: {e}")

    def recent(self):
        path1 = Path("C:", 'Users', 'Student', 'Recent')
        print(path1)
        os.remove(path1)
        path2 = Path('C:', 'Users', 'student', 'AppData', 'Local','Temp')
        print(path2)
        os.remove(path2)



if __name__ == "__main__":
    app = GUI()
    app.mainloop()