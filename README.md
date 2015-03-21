podfmdog
========
Инструмент для автоматической загрузки свежих подкастов с сайта http://podfm.ru/

Установка и запуск
------------------
Для работы с утилитой вам потребуется установить python3 а так же 
модуль python3-nofity2. Установка в дистрибутивах debian/ubuntu
будет выглядеть следующим образом:

```bash
sudo apt-get install python3 python3-notify2
```

Использование утилиты
---------------------
```bash
$ podfmdog_ctl.py
=== podfmdog cotrol v.0.1.0 ===
Usage:
    podfmdog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    channel add <rss_url> <subdir>  -- add the podcast
    channel edit <rss_url> <subdir> -- add the podcast
    channel remove <rss_url>        -- remove the podcast
    channel list                    -- show the podcast list
```

Перед началом работы вам необходимо задать путь к каталогу, в который будут
сохраняться скаченные аудиофайлы. Для этого выполните следующую команду:
```bash
$ podfmdog_ctl.py set download_directory /home/username/your_download_directory
```

После этого вам потребуется добавить каналы, которые вы хотите автоматически загружать,
следующей командой: 
```bash
$ podfmdog_ctl.py channel add http://some-channel.podfm.ru/some-path/rss.xml
```

Файл настроек представляет из себя файл базы данных SQLite, который располагается по
адресу ~/.config/podfmdog/podfmdog.db

Для запуска загрузки новых выпусков необходимо запустить скрипт podfmdog_execute.py 
без параметров.

Так же этот скрипт можно запускать по расписанию с помощью cron. Для этого выполните
команду 
```bash
$ crontab -e
```

И пропишите приблизительно следующее:
```bash
00 * * * * ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/podfmdog/podfmdog_execute.py
@reboot sleep 600 ; ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/podfmdog/podfmdog_execute.py
```
Согласно этим правилам проверка свежих подкастов будет производиться 
каждый час, а так же через 10 минут после включения компьютера.

run_script_with_lock-dbus_in_crontab.sh решает проблему с отображением уведомлений
на рабочий стол при запуске скрипта из cron. Подробнее об этом 
можно прочитать по ссылке http://alekseydurachenko.github.io/2015/03/12/python-notify2-crontab.html
а сам скрипт находится по адресу https://gist.github.com/AlekseyDurachenko/2027114608e4863eb038

