# Сокращение ссылок с помощью сервиса Bitly

Консольная утилита, сокращающая ссылки с помощью сервиса bit.ly и предоставляющая информацию о количестве преходов по ссылкам.

### Установка

Python3 должен быть уже установлен. Для установки зависимостей воспользуйтесь командой:
```
pip install -r requirements.txt
```
### Запуск
```
main.py link
```
- если в качестве *link* передана ссылка, она сокращается через сервис bit.ly
- если в качестве *link* передан битлинк, отображается количество переходов по нему;

### Пример
```
$ python main.py https://docs.python.org/
Битлинк:  https://bit.ly/3LOyhO8

$ python main.py https://bit.ly/3LOyhO8  
По вашей ссылке прошли: 1 раз(а)
```

### Цели проекта

Код написан в образовательных целях для курса [dvmn.org](https://dvmn.org/).