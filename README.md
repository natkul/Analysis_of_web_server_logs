# Analysis_of_web_server_logs

**КАК ЗАПУСТИТЬ**

Укажите имя интерпретатора (python3), имя исполняемого файла (parser_web_server_log.py), укажите путь до файла для параметра (-p),
принимаются только log-файлы.

[//]: # (python3 parser_web_server_logs.py -p 'access.log')
[//]: # (python3 parser_web_server_logs.py -p /home/nat/projects/OTUS/Analysis_of_web_server_logs/)

**КАК РАБОТАЕТ**
1. Функция prepare_list_files() парсит командную строку и, в зависимости от переданного параметра, возвращает список файлов для парсинга
2. parse_files() построчно читает файлы, парсит строки и заполняет массив словарей по требуемым ключам
3. collect_json() записывает словари в json файл statistics.json