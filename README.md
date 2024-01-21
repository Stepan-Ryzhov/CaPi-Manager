# CaPi-Manager

# Идея создания

Каждый из нас сталкивался с проблемой переполненого жесткого диска, большого количества мусора и не нужных файлов, нехваткой оперативной памяти, вирусами на своем ПК.

Приложение CaPi Manager поможет вам избавиться от большого количества мусора, нехватке оперативной памяти и возможных вирусах "живущих" внутри вашего компьютера

# Пару слов о разработке

Приложение CaPi Manager написано на языке Python,с использованием сторонних библиотек:
* pywin32
* customtkinter
* packaging
* psutil
* yadisk
* requests
* subprocess
* socket
* speedtest-cli
* pillow
* logging

А так же с использованием стандартных расширений:
* os
* re
* gc
* platform
* hashlib
* base64
* shutil
* datetime

# Функционал

С помощью нашего приложения вы можете:

* Удалить мусор с вашего ПК(нет, это не просто очистка корзины)
* Удалить повторы из папки Загрузки
* Отследить загруженность вашего ПК
* Выделить дополнительную оперативную память, путем блокировки ненужных процессов
* Проверит ваш компьютер на вирусы(вдруг у вас где-то майнер🤓)
* Проверить скорость интернета

# Контроль версий

#0.0.2

* Первый скелет приложения. 
* Создан графический интерфейс. 
* Бекэнд не предусмотрен.

#0.0.22

* Добавление первоначального функционала: очистка недавнийх файлов и КЭШа. 

#0.0.23

* Переработка функционала,добавленного в версии 0.0.22

#0.0.24

* Оптимизация удаления мусора.

#0.0.25

* Исправление ошибок графического интерфейса.
* Оптимизация работы программы

#0.0.26

* Создание нового экрана для уведомлений от приложения


#0.0.27

* Отказ от идеи в версии 0.0.26 в связи с большими энергозатратами и высокой сложности ее реализации. 
* Переработка графического интерфейса.

#0.0.28

* Внутренняя тестировка(не подлежит релизу)


#0.0.29

* Добавление экрана FAQ(тест).
* Попытка вернуть оконо уведомлений.

#0.0.30

* Добавлены исключения в тех местах, где они могут возникунть
* Добавлена для теста обратная связь
* Оптимизация существующего кода

#0.0.31

* Добавлена функция мониторинга загруженности ПК
* Заморожена система обратной связи
* Добавлен текст FAQ

#0.1.0

* Отлажены ошибки графического интерфейса
* Испрвлены ошибки бекэнда в функциях программы

#0.1.1

* Внутренняя тестировка(не подлежит релизу)

#0.1.2

* Добавлена возможность выбора темы приложения(темная, светлая)
* Функция отрисовки разделена на первичную и повторную

#0.1.3

* Оптимизация и ускорение работы программы
* Исправление незначительных ошибок

#0.1.4

* Внутренняя тестировка(не подлежит релизу)

#0.1.5

* Добавлена функция выделения оперативной памяти
* Ускорение работы графического интерфейса

#0.1.6

* Добавлено построение уникального токена, в котором зашифрована информация о компонентах компьютера,а так же информация, необходимая для отладки

#0.1.7

* Исправление незначительных ошибок

#0.1.8

* Переработан бекэнд выделения оперативной памяти
* Оптимизация работы программы

#0.1.9

* Полностью переделан алгоритм выделения оперативной памяти, повышена эффективность

#0.1.91

* Фикс мелких ошибок

#0.2.0

* Окончательный отказ от всплывающего окна уведомления
* Добавлена функция ускорения процессора(тест)

#1.0.0

* Добавлен альтернативный способ удаления мусора с ПК(в случае блокировки программы ОС компьютера)
* Исправление крупных ошибок графического интерфейса
* Исправление ошибок совместимости ОС и CaPi Manager
* Ускорение работы программы

#1.0.1
* Переписан текст FAQ
* Функция создания отладочного токена вынесена отдельно,для ускорения его формирования
* Исправление мелких ошибок отрисовки

#1.0.2
* Удалена функция ускорения процессора,из-за ее нефункциональности и сложности в дальнейшем развитии
* Добавлен антивирус
* Создана большая БД сигнатур вирусов
* Оптимизация бекэнда

#1.0.3

* Внутренняя тестировка(не подлежит релизу)

#1.0.4

* Незначительные исправления

#1.0.5

* Добалена фанкция прерывания сканирования на вирусы(для тестирования)

#1.0.6

* Добавлена возможность удаления вредоносного файла

#1.0.7

* Незначительные фиксы ошибок

#1.0.8

* Полностью переработан механизм отправки обратной связи

#1.0.9

* Добавлена возможность описать проьлему в соответствующем окне в репорте

#2.0.0

* Полностью отлажен и оптимизирован механзм обратной связи
* Доведена до ума функция удаления вирусов и функция прерывания сканирования
* Оптимизация производительности
* Фикс багов графического интерфейса

#2.0.1

* Внутренняя тестировка(не подлежит релизу)

#2.0.2

* Незначительные фиксы 

#2.0.3

* Добавлена система отслеживания ошибок(логирование)
* Внедрение механизмов исключения по необходимости

#2.0.4

* Введена "защита от дурака" в функции обратной связи

#2.0.5
* Полностью переработана БД сигнатур вирусов и механизм обнаружения зловредных файлов.
* Повышена скорость сканирования антивируса

#2.0.6

* Исправление багов графического интерфейса

#2.0.7

* Внутренняя тестировка(не подлежит релизу)

#2.0.8

* Добавлена эмблема на начальный экран
* Введено ограничение на количество выделений оперативной памяти
* Cоздана версия GOLD Edition - без каких-либо ограничений

#2.0.9

* Незначительные исправления

//НА ВЕРСИИ 2.0.9 ОБНОВЛЕНИЕ ОБЫЧНОЙ ВЕРСИИ БЫЛИ ОКОНЧЕНЫ. ПРИЛОЖЕНИЕ БЫЛО ДОВЕДЕНО ДО УМА. НА ДАННЫЙ МОМЕНТ 2.0.9 ЯВЛЯЕТСЯ ПРСЛЕДНИМ ОБНОВЛЕНИЕМ ОБЫЧНОЙ ВЕРСИИ//

#3.0.0 - gold edition

* Добавление функции проверки скорости интернета
* Оптимизация работы программы
* Добавление обновлений сигнатур "по воздуху"(на данный момент сервер является локальным и создан для предоставления концепта автоматического обновления сигнатур)

#3.0.1 - gold edition

* Исправление ошибок

#3.0.2

* Исправление неверного пути к необходимым для работы программы файлам

