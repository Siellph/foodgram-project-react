![example workflow](https://github.com/Siellph/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram Project

Сервис позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в  избранное, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Стэк технологий  
**Клиент:** React  

**СУБД:** Postgresql

**Framework:** DRF

**Сервер:** NGINX, Gunicorn

[Сайт](http://siellph-foodgram.hopto.org/recipeshttp://siellph-foodgram.hopto.org/recipes)

[Админ-зона](http://siellph-foodgram.hopto.org/admin/login/?next=/admin/)

[Документация](http://siellph-foodgram.hopto.org/api/docs/)

[API DRF](http://siellph-foodgram.hopto.org/api/)

В файле `demoroles.txt` можно найти демострационные авторизационные данные

## Запуск проекта на сервере 👨🏼‍💻

⬇ Скачайте и распакуйте проект на локальную машину

[Скачать](https://github.com/Siellph/foodgram-project-react/archive/refs/heads/master.zip)

🔄 Подключитесь к своему серверу

~~~bash
ssh <server user>@<server IP>
~~~

✔ Установите Docker, если не установлен

~~~bash
sudo apt install docker.io
~~~

✔ Установите Docker Compose (Linux), если не установлен

~~~bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
~~~

🔐 Выдайте разрешения для docker-compose

~~~bash
sudo chmod +x /usr/local/bin/docker-compose
~~~

📂 Создайте в домашней директории папку проекта и перейдите в неё

~~~bash
mkdir foodgram && cd foodgram/
~~~

📂 Создайте дополнительные каталоги

~~~bash
mkdir docs frontend
~~~

🔏 Создайте файл `.env` с секретными ключами

~~~bash
touch .env
~~~

📝 Заполните `.env` файл любым удобным вам способом

~~~bash
DEBUG=False
SECRET_KEY=<Любой длинный серкретный ключ>
ALLOWED_HOSTS=<Укажите разрешенные хосты>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Пароль от пользователя БД>
DB_HOST=db
DB_PORT=5432
~~~

💽 Скопируйте файлы из папки `/infra` на сервер в созданную ранее директорию. А так же скопируйте папки `/docs` и `/frontend`

:warning:Данное действие выполнятеся из терминала/командной строки локального компьютера

~~~bash
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
scp -r docs/* <server user>@<server IP>:/home/<server user>/foodgram/docs/
scp -r frontend/* <server user>@<server IP>:/home/<server user>/foodgram/frontend/
~~~

🆙 Запустите Docker Compose на сервере из директории с файлом `docker-compose.yml`

~~~bash
sudo docker-compose up -d
~~~

📚 После запуска сервера можно создать администратора и выполнить наполнение БД тэгами и ингредиентами

~~~bash
sudo docker exec -it app python manage.py createsuperuser
sudo docker exec -it app python manage.py upload_data
~~~

## Локальный запуск API проекта 👨🏼‍💻
🔗 Склонируйте проект на свой ПК 

~~~bash  
  git clone https://github.com/Siellph/foodgram-project-react.githttps://github.com/Siellph/foodgram-project-react.git
~~~

⤵️ Перейдите в бэкэнд часть проекта (туда где лежит файл manage.py)  

~~~bash  
  cd foodgram-project-react/backend
~~~

🔮 Создайте виртуальное окружение  

~~~bash  
python -m venv .venv #Windows
python3 -m venv .venv #Linux, MacOS
~~~

⚡ Активируйте виртуальное окружение

~~~bash  
. .venv/Scripts/Activate #Windows
. .venv/bin/activate #Linux, MacOS
~~~  

🔄 Обновите pip и установите зависимости

~~~bash
pip install --upgrade pip
pip install -r requirements.txt
~~~

*По умолчанию в проекте используется СУБД Postgresql*

>~~~
>DATABASES = {
>    'default': {
>        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
>        'NAME': os.getenv('DB_NAME', default='postgres'),
>        'USER': os.getenv('POSTGRES_USER', default='postgres'),
>        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
>        'HOST': os.getenv('DB_HOST', default='db'),
>        'PORT': os.getenv('DB_PORT', default='5432')
>    }
>}
>~~~

*В тестовых целях возможно использовать встроенную в Django СУБД SQLite*

*Для этого в в файле backend/foodgram/setting.py замените БД на встроенную SQLite*

>~~~
>DATABASES = {
>    'default': {
>        'ENGINE': 'django.db.backends.sqlite3',
>        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
>    }
>}
>~~~

✏️Создайте в папке `backend` файл `.env` и пропишите следующее

*Если используете Postgresql*
~~~bash
ALLOWED_HOSTS= #укажите через запятую разрешенные хосты
DB_ENGINE= #Укажите движок используемой СУБД (по умолчанию django.db.backends.postgresql)
DB_NAME= #название базы данных (по умолчанию postgres)
POSTGRES_USER= #пользователь базы данных (по умолчанию postgres)
POSTGRES_PASSWORD= #пароль от созданной базы данных (по умолчанию postgres)
DB_HOST= #хост базы данных (по умолчанию db)
DB_PORT= #порт базы данных (по умолчанию для postgresql 5432)
SECRET_KEY= #секретный ключ (по умолчанию django-secret-key)
DEBUG= #включение или отключение режима отладки (True (по умолчанию) or False)
TIME_ZONE= #Часовой пояс (например UTC, Europe/Moscow (по умолчанию), Asia/Yekaterinburg)
~~~

*Если используете встроенную БД SQLite*

~~~
ALLOWED_HOSTS= #укажите через запятую разрешенные хосты
SECRET_KEY= #секретный ключ (по умолчанию django-secret-key)
DEBUG= #включение или отключение режима отладки (True (по умолчанию) or False)
TIME_ZONE= #Часовой пояс (например UTC, Europe/Moscow (по умолчанию), Asia/Yekaterinburg)
~~~

🔀 Создайте и выполните миграции, соберите статику

~~~bash
python manage.py makemigrations #Windows
python manage.py migrate #Windows
python manage.py collectstatic --noinput #Windows

python3 manage.py makemigrations #Linux, MacOS
python3 manage.py migrate #Linux, MacOS
python3 manage.py collectstatic --noinput #Linux, MacOS
~~~

📚 Загрузите предустановленные таблицы ингердиентов и тегов

~~~bash
python manage.py upload_data #Windows

python3 manage.py upload_data #Linux, MacOS
~~~

:octocat:Создайте администратора

~~~bash
python manage.py createsuperuser #Windows

python3 manage.py createsuperuser #Linux, MacOS
~~~

🚀 Запустите сервер

~~~bash
python manage.py runserver #Windows

python3 manage.py runserver #Linux, MacOS
~~~

🎉 Сервер с api backend запущен

Доступны следующие ссылки

http://127.0.0.1:8000/api/v1/ - взаимодействие с API

http://127.0.0.1:8000/admin/ - админ-зона

Для просмотра спецификации API воспользуйтесь следующим:

Перейдите в папку infra проекта foodgram-project-react

~~~
cd <путь_до_проекта>/foodgram-project-react/infra
~~~

Выполните команду

~~~
docker-compose up
~~~

При выполнении этой команды сервис frontend, описанный в docker-compose.yml подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу. 
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/redoc.html

## Что доступно в проекте

### Для неавторизованных пользователей
* Доступна главная страница.
* Доступна страница отдельного рецепта.
* Доступна и работает форма авторизации.
* Доступна и работает система восстановления пароля.
* Доступна и работает форма регистрации.

### Администратор и админ-зона
* Все модели выведены в админ-зону.
* Для модели пользователей включена фильтрация по имени и email.
* Для модели рецептов включена фильтрация по названию, автору и тегам.
* На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
* Для модели ингредиентов включена фильтрация по названию.

### Для авторизованных пользователей
* Доступна главная страница.
* Доступна страница другого пользователя.
* Доступна страница отдельного рецепта.
* Доступна страница «Мои подписки».
    * Можно подписаться и отписаться на странице рецепта.
    * Можно подписаться и отписаться на странице автора.
    * При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
* Доступна страница «Избранное».
    * На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
    * На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
* Доступна страница «Список покупок».
    * На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
    * На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
    * Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
    * Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
* Доступна страница «Создать рецепт».
    * Есть возможность опубликовать свой рецепт.
    * Есть возможность отредактировать и сохранить изменения в своём рецепте.
    * Есть возможность удалить свой рецепт.
* Доступна и работает форма изменения пароля.
* Доступна возможность выйти из системы (разлогиниться).
