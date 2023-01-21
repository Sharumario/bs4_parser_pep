# Парсер документации python
Парсер документации python c https://docs.python.org/3/ и https://peps.python.org/

## Руководство пользователя
Склонируйте репозиторий
```
git@github.com:Sharumario/bs4_parser_pep.git
```
Создайте виртуальное окружение:
```
python -m venv venv
```
Активируйте виртуальное окружение:
```
. venv/bin/activate
```
Установите зависимости:
```
pip install -r requirements.txt
```
Парсер запускается из папки ./src/:

Команды парсера:
```
python main.py whats-new — нововведения Python;
```
```
python main.py latest-versions — информация о последних версиях;
```
```
python main.py download — загрузка документации;
```
```
python main.py pep — парсинг информации по каждому PEP
```
Опции:
```
python main.py -h — Вспомогательная информация
```
```
python main.py -c — Очистка кеша
```
```
python main.py -o {pretty,file} — 
   Дополнительные способы вывода данных(pretty(таблица), file(csv файл))
```

## Над проектом работали:
[Шайхнисламов Марат](https://github.com/Sharumario/) при поддержке ЯндексПрактикума
