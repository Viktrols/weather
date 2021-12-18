# weather
### Техническое задание находится в файле tech_task.txt

## Запуск проекта

### Клонируйте данный репозиторий
```git clone https://github.com/Viktrols/weather.git```
### Создайте и активируйте виртуальное окружение
```
python -m venv venv
source ./venv/Scripts/activate  #для Windows
source ./venv/bin/activate      #для Linux и macOS
```
### Установите требуемые зависимости
```
pip install -r requirements.txt
```
### В терминале запустите проект
```
flask run
```
### Проект будет доступен по адресу http://127.0.0.1:5000/
### Документация АПИ http://127.0.0.1:5000/swagger-ui/
### Для тестирования проекта откройте второе окно терминала и запустите файл request_samples
```
python request_samples.py
```

#### Для запуска проекта с нуля с новой БД выполните те же пункты, но перед запуском проекта:
1. Создайте файл .env и внесите в него такие данные
```
DATABASE_URL = <адрес базы данных>
API_KEY = <Токен для работы с openweathermap.org>
```
2. Примените миграции:
```
lask db upgrade
```
3. Для наполнения БД данными запустите файл get_forecast
```
py get_forecasts.py
```
