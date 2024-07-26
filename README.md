**Опиание проекта:** 

 

На сайте **Foodgram** пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, которые необходимы для приготовления одного или нескольких выбранных блюд. 

 

**Проект доступен по адресу:**

``` 

https://kotletka.zapto.org/

```

**Админка:**

- Логин: superuser@mail.ru
- Пароль: Superuser

  

**Инструкция по установке локально:** 

 

- Клонируйте репозиторий: 

 

``` 

git clone https://github.com/Ksenia-Katrechko/foodgram 

``` 

 

- Установите и активируйте виртуальное окружение: 

 

``` 

python -m venv venv 

source venv/Scripts/activate 

``` 

 

- Установите зависимости из файла requirements.txt: 

 

``` 

pip install -r requirements.txt 

``` 

 

- Примените миграции: 

 

``` 

python manage.py migrate 

``` 

 

- В папке с файлом manage.py выполните команду для запуска локально: 

 

``` 

python manage.py runserver 

``` 

 

- Локально документация доступна по [адресу](http://127.0.0.1/api/docs/) 

 

**Инструкция по установке на удаленный сервер:** 

 

- Выполните вход на свой удаленный сервер 

 

``` 

ssh <USERNAME>@<IP_ADDRESS> 

``` 

 

- Установите docker на сервер: 

 

``` 

sudo apt install docker.io 

``` 

 

- Установите docker-compose на сервер: 

 

``` 

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 

sudo chmod +x /usr/local/bin/docker-compose 

``` 

 

 

- Локально отредактируйте файл nginx.conf 

 

``` 

Локально отредактируйте файл infra/nginx/default.conf и в строке server_name впишите свой IP 

``` 

 

- Скопируйте подготовленные файлы из каталога infra: 

 

``` 

scp docker-compose.yml <username>@<host>:/home/<username>/foodgram-project-react/infra/docker-compose.yml 

scp default.conf <username>@<host>:/home/foodgram-project-react/infra/nginx/default.conf 

``` 

 

- Cоздайте .env файл: 

 

``` 

SECRET_KEY=<SECRET_KEY> 

DB_ENGINE=django.db.backends.postgresql 

DB_NAME=postgres 

POSTGRES_USER=postgres 

POSTGRES_PASSWORD=postgres 

DB_HOST=db 

DB_PORT=5432 

``` 

 

- Добавьте переменные окружения в Secrets GitHub: 

 

``` 

DB_ENGINE=django.db.backends.postgresql 

DB_NAME=postgres 

POSTGRES_USER=postgres 

POSTGRES_PASSWORD=postgres 

DB_HOST=db 

DB_PORT=5432 

DOCKER_PASSWORD=<пароль DockerHub> 

DOCKER_USERNAME=<имя пользователя DockerHub> 

USER=<username для подключения к серверу> 

HOST=<IP сервера> 

PASSPHRASE=<пароль для сервера, если он установлен> 

SSH_KEY=<ваш SSH ключ (команда для получения ключа: cat ~/.ssh/id_rsa)> 

TELEGRAM_TO=<ID своего телеграм-аккаунта> 

TELEGRAM_TOKEN=<токен вашего бота> 

``` 

 

- На сервере соберите docker-compose: 

 

``` 

sudo docker-compose up -d --build 

``` 

 

- Создайте и примените миграции: 

 

``` 

sudo docker-compose exec backend python manage.py makemigrations --noinput 

sudo docker-compose exec backend python manage.py migrate --noinput 

``` 

 

- Подгрузите статику 

 

``` 

sudo docker-compose exec backend python manage.py collectstatic --noinput 

``` 

 

- Заполните базу данных: 

 

``` 

sudo docker-compose exec backend python manage.py loaddata data/ingredients_data.json 

``` 

 

- Создайте суперпользователя Django: 

 

``` 

sudo docker-compose exec backend python manage.py createsuperuser 

``` 

 

 

**Стек технологий:** 

- Python 

- Django 

- Django REST Framework 

- PostgreSQL 

- Nginx 

- Gunicorn 

- Docker 

- GitHub%20Actions 

- Yandex.Cloud 

 

**Автор проекта [Ксения Катречко](https://github.com/Ksenia-Katrechko)** 

