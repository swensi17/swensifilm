# FilmoraLands

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-lightblue)
![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub Repo Size](https://img.shields.io/github/repo-size/swensi17/FilmoraLands)
![GitHub stars](https://img.shields.io/github/stars/swensi17/FilmoraLands?style=social)

![FilmoraLands Banner](https://github.com/swensi17/FilmoraLands/raw/main/static/images/banner.png)

## О проекте

**FilmoraLands** — это современное веб-приложение, разработанное на основе Flask, предназначенное для поиска и просмотра информации о фильмах и сериалах. Приложение интегрировано с [The Movie Database (TMDb) API](https://www.themoviedb.org/), что позволяет пользователям находить подробную информацию о своих любимых фильмах, смотреть трейлеры и получать рекомендации.

## Особенности

- **Поиск фильмов:** Интуитивно понятный поиск по названию фильма с автодополнением.
- **Детальная страница фильма:** Просмотр информации о фильме, включая описание, рейтинг, жанры и актерский состав.
- **Трейлеры:** Возможность просмотра трейлеров на русском языке, а при их отсутствии — на английском.
- **Жанры:** Фильтрация фильмов по различным жанрам для удобного поиска.
- **Похожие фильмы:** Рекомендации на основе выбранного фильма.
- **Аниме раздел:** Специальный раздел для поиска и просмотра аниме.
- **Франшизы:** Просмотр других частей франшиз и связанных фильмов.
- **Модальные окна:** Стильные модальные окна для уведомлений и просмотра постеров.

## Технологии

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **API:** The Movie Database (TMDb) API
- **База данных:** (Если используется)
- **Контроль версий:** Git, GitHub

## Установка

### Предварительные требования

- Python 3.8+
- Git

### Шаги по установке

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/swensi17/FilmoraLands.git
    ```

2. **Перейдите в директорию проекта:**

    ```bash
    cd FilmoraLands
    ```

3. **Создайте и активируйте виртуальное окружение:**

    ```bash
    python -m venv venv
    ```

    - **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **macOS и Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Установите необходимые зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Настройте переменные окружения:**

    Создайте файл `.env` в корне проекта и добавьте следующие строки:

    ```env
    FLASK_APP=main.py
    FLASK_ENV=development
    API_KEY=ваш_tmdb_api_key
    ```

    Замените `ваш_tmdb_api_key` на ваш собственный API-ключ от [TMDb](https://www.themoviedb.org/documentation/api).

6. **Запустите приложение:**

    ```bash
    flask run
    ```

7. **Откройте приложение в браузере:**

    Перейдите по адресу [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Использование

- **Поиск фильмов:** Введите название фильма в поисковую строку и нажмите "Поиск".
- **Просмотр деталей:** Нажмите на постер фильма, чтобы открыть детальную страницу с информацией и трейлером.
- **Жанры:** Перейдите в раздел "Жанры" для фильтрации фильмов по категориям.
- **Аниме:** Специальный раздел для поиска и просмотра аниме.

## Скриншоты

### Главная страница

![Главная страница](https://github.com/swensi17/FilmoraLands/raw/main/static/images/main_page.png)

### Страница поиска

![Страница поиска](https://github.com/swensi17/FilmoraLands/raw/main/static/images/search_page.png)

### Детальная страница фильма

![Детальная страница фильма](https://github.com/swensi17/FilmoraLands/raw/main/static/images/movie_details.png)

### Модальное окно

![Модальное окно](https://github.com/swensi17/FilmoraLands/raw/main/static/images/modal.png)

## Вклад

Мы приветствуем ваши предложения и вклады! Пожалуйста, следуйте этим шагам для внесения изменений:

1. **Создайте форк репозитория.**
2. **Создайте новую ветку для вашей функциональности:**

    ```bash
    git checkout -b feature/YourFeatureName
    ```

3. **Внесите изменения и зафиксируйте их:**

    ```bash
    git commit -m "Добавлена новая функция"
    ```

4. **Отправьте изменения в свой форк:**

    ```bash
    git push origin feature/YourFeatureName
    ```

5. **Создайте Pull Request на GitHub.**

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в [LICENSE](LICENSE).

## Контакты

Если у вас есть вопросы или предложения, вы можете связаться со мной по следующим каналам:

- **Email:** [your_email@example.com](mailto:your_email@example.com)
- **GitHub:** [swensi17](https://github.com/swensi17)

---

![Powered by FilmoraLands](https://github.com/swensi17/FilmoraLands/raw/main/static/images/powered_by.png)
```
