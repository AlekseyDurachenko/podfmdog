# podfmdog
Набор скриптов позволяющий автоматически загружать новые подкасты с сайта http://podfm.ru/.

Информация о новых загруженных подкастах появляется в области уведомлений.

Настройки программы хранятся в файле базы данных SQLite: **$HOME/.config/podfmdog/podfmdog.db**

## Зависимости
* python3
* python3-notify2

## Использование
```bash
$ podfmdog_ctl.py
=== podfmdog control v.0.1.0 ===
Usage:
    podfmdog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    channel add <rss_url> <subdir>  -- add the podcast
    channel edit <rss_url> <subdir> -- change the podcast directory
    channel remove <rss_url>        -- remove the podcast
    channel list                    -- show the podcast list
```

* сначала проинициализируйте базу данных:
```bash
$ podfmdog_ctl.py init
```

* затем вам необходимо задать путь к каталогу, в который будут сохраняться скачанные аудиофайлы:
```bash
$ podfmdog_ctl.py set download_directory /home/username/your_download_directory
```

* после этого вы можете добавлять каналы(укажите ссылку на rss ленту канала): 
```bash
$ podfmdog_ctl.py channel add http://some-channel.podfm.ru/some-path/rss.xml some-channel-directory
```

**Примечание: подкасты будут сохраняться в "/home/username/your_download_directory/some-channel-directory"**

Для запуска процесса загрузки подкастов используйте:
```bash
$ podfmdog_execute.py
```

Для удобства скрипт можно запускать автоматически. Для этого
отредактируйте crontab(crontab -e) приблизительно следующим образом:
```bash
# проверять наличие новых подкастов каждый час
00 * * * * ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/podfmdog/podfmdog_execute.py
# проверить наличие новых подкастов через 600 секунд после включения компьютера
@reboot sleep 600 ; ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/podfmdog/podfmdog_execute.py
```

**run_script_with_lock-dbus_in_crontab.sh решает проблему с отображением уведомлений
на рабочий стол при запуске скрипта из cron. (Подробнее об этом 
можно прочитать по ссылке http://alekseydurachenko.github.io/2015/03/12/python-notify2-crontab.html
а сам скрипт находится по адресу https://gist.github.com/AlekseyDurachenko/2027114608e4863eb038)**
