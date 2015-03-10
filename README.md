podfmspider
===========
Набор скриптов для автоматической загрузки свежих подкастов


Дополнения
----------

```bash
sudo apt-get install python3-notify2
```

Usage
-----

```bash
=== podfmdog cotrol v.0.1.0 ===
Usage:
    podfmdog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    channel add <rss_url> <subdir>  -- add the podcast
    channel edit <rss_url> <subdir>  -- add the podcast
    channel remove <rss_url>        -- remove the podcast
    channel list                    -- show the podcast list
```
