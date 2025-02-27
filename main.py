from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import random

app = Flask(__name__,
    static_folder='static',
    template_folder='templates'
)

API_KEY = "f07fe1ef73590e66585c2260c45f60b"
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMDdmZTFlZjczNTkwZTY2NTg1OGMyMjYwYzQ1ZjYwYiIsIm5iZiI6MTczMjEyNDAxNy41ODYsInN1YiI6IjY3M2UxZDcxMDRjNmIyMGM3NDZmMDY4MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.c7leSyPfcpenR82ViQ29ETTA3fmNo5xaOrplBaaSuAE"
}

# Добавим словарь для перевода жанров
GENRES_TRANSLATION = {
    'Action': 'Боевик',
    'Adventure': 'Приключения',
    'Animation': 'Мультфильм',
    'Comedy': 'Комедия',
    'Crime': 'Криминал',
    'Documentary': 'Документальный',
    'Drama': 'Драма',
    'Family': 'Семейный',
    'Fantasy': 'Фэнтези',
    'History': 'Исторический',
    'Horror': 'Ужасы',
    'Music': 'Музыка',
    'Mystery': 'Детектив',
    'Romance': 'Мелодрама',
    'Science Fiction': 'Фантастика',
    'TV Movie': 'Телефильм',
    'Thriller': 'Триллер',
    'War': 'Военный',
    'Western': 'Вестерн'
}

# Расширенный словарь подборок с тематическими постерами из TMDB
COLLECTIONS = {
    'marvel': {
        'name': 'Вселенная Marvel',
        'id': 1,
        'poster': 'https://image.tmdb.org/t/p/original/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg',  # Постер "Человек-паук: Нет пути домой"
        'description': 'Захватывающие приключения супергероев',
        'category': 'Франшизы'
    },
    'dc': {
        'name': 'DC Comics',
        'id': 2,
        'poster': 'https://image.tmdb.org/t/p/original/5hoS3nEkGGXUfmnu39yw1k52JX5.jpg',  # Постер Лига справедливости Зака Снайдера
        'description': 'Легендарные истории супергероев DC',
        'category': 'Франшизы'
    },
    'pixar': {
        'name': 'Pixar',
        'id': 3,
        'poster': 'https://image.tmdb.org/t/p/original/abW5AzHDaIK1n9C36VdAeOwORRA.jpg',  # Постер "Тачки"
        'description': 'Любимые анимационные фильмы',
        'category': 'Студии'
    },
    'oscar': {
        'name': 'Оскароносные фильмы',
        'id': 4,
        'poster': 'https://image.tmdb.org/t/p/original/8kNruSfhk5IoE4eZOc4UpvDn6tq.jpg',  # Постер Зеленая книга
        'description': 'Лучшие фильмы, получившие премию Оскар',
        'category': 'Награды'
    },
    'animation': {
        'name': 'Лучшие мультфильмы',
        'id': 5,
        'poster': 'https://image.tmdb.org/t/p/original/npHNjldbeTHdKKw28bJKs7lzqzj.jpg',  # Постер Человек-паук: Через вселенные
        'description': 'Волшебный мир анимации',
        'category': 'Жанры'
    },
    'fantasy': {
        'name': 'Фэнтези миры',
        'id': 6,
        'poster': 'https://image.tmdb.org/t/p/original/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',  # Постер Властелин колец
        'description': 'Погрузитесь в магические миры',
        'category': 'Жанры'
    },
    'classics': {
        'name': 'Золотая классика',
        'id': 7,
        'poster': 'https://image.tmdb.org/t/p/original/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',  # Постер Крестный отец
        'description': 'Нестареющие шедевры кинематографа',
        'category': 'Эпохи'
    },
    'horror': {
        'name': 'Лучшие ужасы',
        'id': 8,
        'poster': 'https://image.tmdb.org/t/p/original/7fn624j5lj3xTme2SgiLCeuedmO.jpg',  # Постер Сияние
        'description': 'Самые страшные фильмы всех времен',
        'category': 'Жанры'
    },
    'scifi': {
        'name': 'Научная фантастика',
        'id': 9,
        'poster': 'https://image.tmdb.org/t/p/original/br6krBFpaYmCSglLBWRuhui7tPc.jpg',  # Постер Бегущий по лезвию 2049
        'description': 'Путешествия в будущее и космические приключения',
        'category': 'Жанры'
    },
    'action': {
        'name': 'Экшн',
        'id': 10,
        'poster': 'https://image.tmdb.org/t/p/original/keIxh0wPr2Ymj0Btjh4gW7JJ89e.jpg',  # Постер Джон Уик 4
        'description': 'Захватывающие боевики и приключения',
        'category': 'Жанры'
    },
    'drama': {
        'name': 'Драмы',
        'id': 11,
        'poster': 'https://image.tmdb.org/t/p/original/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',  # Постер Побег из Шоушенка
        'description': 'Глубокие и эмоциональные истории',
        'category': 'Жанры'
    },
    'comedy': {
        'name': 'Комедии',
        'id': 12,
        'poster': 'https://image.tmdb.org/t/p/original/iZjMFSKCrleKolC1gYcz5Rs8bk1.jpg',  # Постер "1+1"
        'description': 'Фильмы для хорошего настроения',
        'category': 'Жанры'
    },
    'thriller': {
        'name': 'Триллеры',
        'id': 13,
        'poster': 'https://image.tmdb.org/t/p/original/rplLJ2hPcOQmkFhTqUte0MkEaO2.jpg',  # Постер Молчание ягнят
        'description': 'Держащие в напряжении истории',
        'category': 'Жанры'
    },
    'romance': {
        'name': 'Романтика',
        'id': 14,
        'poster': 'https://image.tmdb.org/t/p/original/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',  # Постер Ла-Ла Ленд
        'description': 'Лучшие романтические фильмы',
        'category': 'Жанры'
    },
    'anime': {
        'name': 'Аниме',
        'id': 15,
        'poster': 'https://image.tmdb.org/t/p/original/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg',  # Постер Унесенные призраками
        'description': 'Лучшие японские анимационные фильмы',
        'category': 'Жанры'
    },
    'family': {
        'name': 'Семейное кино',
        'id': 16,
        'poster': 'https://image.tmdb.org/t/p/original/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg',  # Постер Гарри Поттер
        'description': 'Фильмы для всей семьи',
        'category': 'Жанры'
    },
    'documentary': {
        'name': 'Документальные',
        'id': 17,
        'poster': 'https://image.tmdb.org/t/p/original/d4J7GotCjvDJBAYayZBTc5nLbbP.jpg',  # Постер Планета Земля
        'description': 'Познавательные истории о реальном мире',
        'category': 'Жанры'
    },
    'war': {
        'name': 'Военные фильмы',
        'id': 18,
        'poster': 'https://image.tmdb.org/t/p/original/kWWAt2FMRbqLFFy8o5R4Zr8cMAb.jpg',  # Постер Спасти рядового Райана
        'description': 'Драматические истории о войне',
        'category': 'Жанры'
    },
    'crime': {
        'name': 'Криминал',
        'id': 19,
        'poster': 'https://image.tmdb.org/t/p/original/6YRQ8l93ZEs6x4rZojWoHIWdguK.jpg',  # Постер Криминальное чтиво
        'description': 'Захватывающие криминальные истории',
        'category': 'Жанры'
    },
    'adventure': {
        'name': 'Приключения',
        'id': 20,
        'poster': 'https://image.tmdb.org/t/p/original/ceG9VzoRAVGwivFU403Wc3AHRys.jpg',  # Постер Индиана Джонс
        'description': 'Увлекательные путешествия и открытия',
        'category': 'Жанры'
    },
    'asian': {
        'name': 'Азиатское кино',
        'id': 21,
        'poster': 'https://image.tmdb.org/t/p/original/bXNvzjULc9jrOVhGfjcc64uKZmZ.jpg',  # Постер "Олдбой"
        'description': 'Лучшие фильмы азиатского кинематографа',
        'category': 'Регионы'
    },
    'musical': {
        'name': 'Мюзиклы',
        'id': 22,
        'poster': 'https://image.tmdb.org/t/p/original/vgpXmVaVyUL7GGiDeiK1mKEKzcX.jpg',  # Постер "Ла-Ла Ленд"
        'description': 'Музыкальные истории на большом экране',
        'category': 'Жанры'
    },
    'sport': {
        'name': 'Спортивные драмы',
        'id': 23,
        'poster': 'https://image.tmdb.org/t/p/original/ggFHVNu6YYI5L9pCfOacjizRGt.jpg',  # Постер "Рокки"
        'description': 'Вдохновляющие истории о спорте и победах',
        'category': 'Жанры'
    },
    'biography': {
        'name': 'Биографии',
        'id': 24,
        'poster': 'https://image.tmdb.org/t/p/original/mfwq2nMBzArzQ7Y9RKE8SKeeTkg.jpg',  # Постер "Социальная сеть"
        'description': 'Истории великих людей',
        'category': 'Жанры'
    },
    'noir': {
        'name': 'Нуар',
        'id': 25,
        'poster': 'https://image.tmdb.org/t/p/original/yF1eOkaYvwiORauRCPWznV9xVvi.jpg',  # Постер "Город грехов"
        'description': 'Атмосферные детективы и криминальные драмы',
        'category': 'Жанры'
    }
}

@app.route('/')
def index():
    # Получаем топ 10 новых фильмов 2024-2025
    response = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'sort_by': 'popularity.desc',
            'primary_release_date.gte': '2024-01-01',
            'primary_release_date.lte': '2025-12-31',
            'vote_count.gte': 50,  # Минимальное количество голосов
            'page': 1
        }
    )
    top_movies = response.json()['results'][:10]  # Берем только первые 10 фильмов

    # Получаем популярные фильмы
    response = requests.get(
        f"{BASE_URL}/movie/popular", 
        headers=HEADERS,
        params={'language': 'ru-RU'}  # Добавляем русский язык
    )
    movies = response.json()['results']
    
    # Получаем фильмы в тренде
    trending = requests.get(
        f"{BASE_URL}/trending/movie/week", 
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    trending_movies = trending.json()['results']
    
    # Получаем топ рейтинговых фильмов
    top_rated = requests.get(
        f"{BASE_URL}/movie/top_rated", 
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    top_rated_movies = top_rated.json()['results']
    
    # Получаем предстоящие фильмы
    upcoming = requests.get(
        f"{BASE_URL}/movie/upcoming",
        headers=HEADERS,
        params={'language': 'ru-RU', 'page': 1}
    ).json()['results']
    
    # Получаем жанры
    genres = requests.get(f"{BASE_URL}/genre/movie/list", headers=HEADERS)
    genres_list = genres.json()['genres']
    
    # Переводим жанры на русский
    for genre in genres_list:
        genre['name'] = GENRES_TRANSLATION.get(genre['name'], genre['name'])
    
    # Добавляем новые запросы для дополнительных категорий
    new_releases = requests.get(
        f"{BASE_URL}/movie/now_playing",
        headers=HEADERS,
        params={'language': 'ru-RU', 'page': 1}
    ).json()['results']

    classics = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 1000,
            'primary_release_date.lte': '1990-12-31'
        }
    ).json()['results']

    # Добавляем новые запросы
    best_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 1000,
            'page': 1
        }
    ).json()['results']

    best_tv = requests.get(
        f"{BASE_URL}/discover/tv",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 500,
            'page': 1
        }
    ).json()['results']

    best_animation = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '16',  # ID анимационного жанра
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 300,
            'page': 1
        }
    ).json()['results']

    anime = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_keywords': '210024',  # ID для аниме
            'sort_by': 'popularity.desc',
            'page': 1
        }
    ).json()['results']

    top_2024 = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'primary_release_year': '2024',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    top_2023 = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'primary_release_year': '2023',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 200,
            'page': 1
        }
    ).json()['results']

    # Добавляем новые запросы для жанров
    action_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '28',  # ID жанра боевик
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    comedy_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '35',  # ID жанра комедия
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    horror_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '27',  # ID жанра ужасы
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    scifi_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '878',  # ID жанра фантастика
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    drama_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '18',  # ID жанра драма
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    mystery_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '9648',  # ID жанра детектив
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    romance_movies = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'with_genres': '10749',  # ID жанра мелодрама
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100,
            'page': 1
        }
    ).json()['results']

    return render_template('index.html',
                         top_movies=top_movies,
                         trending=trending_movies,
                         movies=movies,
                         top_rated=top_rated_movies,
                         new_releases=new_releases,
                         upcoming=upcoming,
                         classics=classics,
                         best_movies=best_movies,
                         best_tv=best_tv,
                         best_animation=best_animation,
                         anime=anime,
                         top_2024=top_2024,
                         top_2023=top_2023,
                         genres=genres_list,
                         collections=COLLECTIONS,
                         action_movies=action_movies,
                         comedy_movies=comedy_movies,
                         horror_movies=horror_movies,
                         scifi_movies=scifi_movies,
                         drama_movies=drama_movies,
                         mystery_movies=mystery_movies,
                         romance_movies=romance_movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    # Получаем информацию о фильме
    movie_response = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'append_to_response': 'belongs_to_collection'
        }
    )
    movie_details = movie_response.json()

    # Получаем трейлеры
    videos_response = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", headers=HEADERS)
    trailers = None
    if videos_response.json().get('results'):
        # Ищем официальный трейлер
        for video in videos_response.json()['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailers = video['key']
                break

    # Получаем актерский состав
    credits_response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/credits",
        headers=HEADERS
    )
    credits = credits_response.json()
    cast = credits.get('cast', [])[:10]  # Берем только первые 10 актеров

    # Получаем похожие фильмы
    similar_response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/similar",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'page': 1
        }
    )
    
    if similar_response.ok:
        similar_movies = similar_response.json().get('results', [])
        
        # Фильтруем фильмы с постерами и рейтингом выше 5
        similar_movies = [movie for movie in similar_movies if movie.get('poster_path') and movie.get('vote_average', 0) > 5]
        
        # Добавляем дополнительные рекомендации если похожих фильмов мало
        if len(similar_movies) < 8:
            recommendations = requests.get(
                f"{BASE_URL}/movie/{movie_id}/recommendations",
                headers=HEADERS,
                params={'language': 'ru-RU', 'page': 1}
            ).json().get('results', [])
            
            # Фильтруем рекомендации
            recommendations = [movie for movie in recommendations 
                             if movie.get('poster_path') and 
                             movie.get('vote_average', 0) > 5 and 
                             movie['id'] not in [m['id'] for m in similar_movies]]
            
            similar_movies.extend(recommendations[:8 - len(similar_movies)])

        # Разделяем фильмы на новые и старые
        current_year = datetime.now().year
        new_movies = []
        old_movies = []
        
        for movie in similar_movies:
            release_date = movie.get('release_date', '')
            if release_date:
                year = int(release_date[:4])
                if year >= current_year - 2:  # Фильмы за последние 2 года считаем новыми
                    new_movies.append(movie)
                else:
                    old_movies.append(movie)
        
        # Сортируем каждую группу по рейтингу и дате
        new_movies.sort(key=lambda x: (x.get('vote_average', 0), x.get('release_date', '')), reverse=True)
        old_movies.sort(key=lambda x: (x.get('vote_average', 0), x.get('release_date', '')), reverse=True)
        
        # Объединяем списки, сначала новые, потом старые
        similar_movies = new_movies + old_movies
    else:
        similar_movies = []

    return render_template('movie.html',
                         movie=movie_details,
                         cast=cast[:8],
                         similar_movies=similar_movies[:8],
                         trailers=trailers,
                         current_year=datetime.now().year)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template('search.html', movies=None)
    
    # Поиск фильмов
    search_response = requests.get(
        f"{BASE_URL}/search/movie",
        headers=HEADERS,
        params={
            'query': query,
            'language': 'ru-RU',
            'page': 1,
            'include_adult': False
        }
    )
    
    if not search_response.ok:
        return render_template('search.html', movies=[], error="Произошла ошибка при поиске")
    
    movies = search_response.json().get('results', [])
    
    # Фильтруем результаты и добавляем дополнительную информацию
    filtered_movies = []
    for movie in movies:
        if movie.get('poster_path'):  # Проверяем наличие постера
            # Получаем дополнительную информацию о фильме
            movie_details = requests.get(
                f"{BASE_URL}/movie/{movie['id']}",
                headers=HEADERS,
                params={'language': 'ru-RU'}
            )
            
            if movie_details.ok:
                details = movie_details.json()
                movie['genres'] = details.get('genres', [])
                movie['runtime'] = details.get('runtime')
                filtered_movies.append(movie)
                
                if len(filtered_movies) >= 20:  # Ограничиваем количество результатов
                    break
    
    return render_template(
        'search.html',
        movies=filtered_movies,
        query=query,
        error=None if filtered_movies else "По вашему запросу ничего не найдено"
    )

@app.route('/genre/<int:genre_id>')
def genre(genre_id):
    response = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params={
            'with_genres': genre_id, 
            'language': 'ru-RU',
            'region': 'RU',
            'sort_by': 'popularity.desc'
        }
    )
    movies = response.json()['results']
    
    # Получаем название жанра
    genres = requests.get(
        f"{BASE_URL}/genre/movie/list", 
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    genre_name = next((g['name'] for g in genres.json()['genres'] if g['id'] == genre_id), '')
    
    return render_template('genre.html', movies=movies, genre_name=genre_name)

@app.route('/api/search')
def api_search():
    query = request.args.get('query', '')
    if query:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            headers=HEADERS,
            params={
                'query': query, 
                'language': 'ru-RU',
                'region': 'RU',
                'include_adult': 'false'
            }
        )
        results = response.json()['results']
    else:
        results = []
    
    return render_template('search.html', results=results, query=query)

@app.route('/collection/<collection_id>')
def collection(collection_id):
    collection_info = next((coll for coll in COLLECTIONS.values() if coll['id'] == int(collection_id)), None)
    if not collection_info:
        return redirect(url_for('index'))
    
    # Получаем фильмы в зависимости от типа подборки
    if collection_id == '1':  # Marvel
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_companies': '420',  # ID компании Marvel
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '2':  # DC
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_companies': '429',  # ID компании DC
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '3':  # Pixar
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_companies': '3',  # ID компании Pixar
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '4':  # Oscar
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_keywords': '1255',  # ID ключевого слова "oscar-winner"
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc'
            }
        )
    elif collection_id == '5':  # Animation
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '16',  # ID жанра анимация
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '6':  # Fantasy
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '14',  # ID жанра фэнтези
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '7':  # Classics
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'primary_release_date.lte': '1990-12-31',
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 1000
            }
        )
    elif collection_id == '8':  # Horror
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '27',  # ID жанра ужасы
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '9':  # Scifi
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '878',  # ID жанра научная фантастика
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '10':  # Action
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '28',  # ID жанра экшн
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '11':  # Drama
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '18',  # ID жанра драма
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '12':  # Comedy
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '35',  # ID жанра комедия
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '13':  # Thriller
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '53',  # ID жанра триллер
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '14':  # Romance
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '10749',  # ID жанра романтика
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '15':  # Anime
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '16',  # ID жанра анимация
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '16':  # Family
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '10751',  # ID жанра семья
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '17':  # Documentary
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '99',  # ID жанра документальный
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '18':  # War
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '10752',  # ID жанра война
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '19':  # Crime
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '80',  # ID жанра криминал
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '20':  # Adventure
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '12',  # ID жанра приключения
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '21':  # Азиатское кино
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_original_language': 'ko|ja|zh',  # Корейский, Японский, Китайский
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 1000
            }
        )
    elif collection_id == '22':  # Мюзиклы
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '10402',  # ID жанра мюзикл
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'popularity.desc'
            }
        )
    elif collection_id == '23':  # Спортивные драмы
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_keywords': '6075|9672|15104',  # Keywords для спорта, бокса, спортивных соревнований
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 500
            }
        )
    elif collection_id == '24':  # Биографии
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_genres': '36',  # ID жанра биография
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 1000
            }
        )
    elif collection_id == '25':  # Нуар
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'with_keywords': '188|691|12565',  # Keywords для нуара, детектива, криминальной драмы
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 500,
                'primary_release_date.gte': '1940-01-01',
                'primary_release_date.lte': '1960-12-31'
            }
        )
    else:  # Classics
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                'primary_release_date.lte': '1990-12-31',
                'language': 'ru-RU',
                'region': 'RU',
                'sort_by': 'vote_average.desc',
                'vote_count.gte': 1000
            }
        )
    
    movies = response.json()['results']
    
    # Дополнительный запрос для получения русских названий и описаний
    for movie in movies:
        details = requests.get(
            f"{BASE_URL}/movie/{movie['id']}", 
            headers=HEADERS,
            params={
                'language': 'ru-RU',
                'region': 'RU'
            }
        )
        movie_details = details.json()
        movie['title'] = movie_details.get('title', movie['title'])
        movie['overview'] = movie_details.get('overview', movie['overview'])

    return render_template('collection.html', 
                         collection=collection_info,
                         movies=movies)

@app.route('/collections')
def collections():
    # Группируем коллекции по категориям
    categories = {}
    for collection in COLLECTIONS.values():
        category = collection['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(collection)
    
    return render_template('collections.html', categories=categories)

@app.route('/random')
def random_movie():
    # Получаем список популярных фильмов
    response = requests.get(
        f"{BASE_URL}/movie/popular",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'page': random.randint(1, 5)  # Случайная страница от 1 до 5
        }
    )
    
    movies = response.json()['results']
    if movies:
        # Выбираем случайный фильм из списка
        random_movie = random.choice(movies)
        # Перенаправляем на страницу этого фильма
        return redirect(url_for('movie_details', movie_id=random_movie['id']))
    
    # Если что-то пошло не так, возвращаемся на главную
    return redirect(url_for('index'))

@app.route('/filter_movies')
def filter_movies():
    media_type = request.args.get('media_type', 'movie')
    
    # Базовые параметры запроса
    params = {
        'language': 'ru-RU',
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'vote_count.gte': 100
    }

    # Выбираем endpoint и параметры в зависимости от типа контента
    if media_type == 'movie':
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif media_type == 'tv':
        response = requests.get(
            f"{BASE_URL}/discover/tv",
            headers=HEADERS,
            params=params
        )
    elif media_type == 'anime':
        params['with_keywords'] = '210024'  # ID для аниме
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif media_type == 'animation':
        params['with_genres'] = '16'  # ID для анимации
        params['vote_count.gte'] = 50  # Снижаем порог голосов для мультфильмов
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    else:
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )

    results = response.json().get('results', [])

    # Для сериалов меняем поле title на name
    if media_type == 'tv':
        for result in results:
            result['title'] = result.get('name')
    
    return render_template('filtered_movies.html', 
                         movies=results,
                         media_type=media_type,
                         genres=get_genres())

# Добавим функцию для получения жанров
def get_genres():
    genres = requests.get(
        f"{BASE_URL}/genre/movie/list", 
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    genres_list = genres.json()['genres']
    
    # Переводим жанры на русский
    for genre in genres_list:
        genre['name'] = GENRES_TRANSLATION.get(genre['name'], genre['name'])
    
    return genres_list

@app.route('/api/load_more')
def load_more():
    media_type = request.args.get('media_type', 'movie')
    page = request.args.get('page', 1, type=int)
    
    params = {
        'language': 'ru-RU',
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'vote_count.gte': 100,
        'page': page
    }

    if media_type == 'movie':
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif media_type == 'tv':
        response = requests.get(
            f"{BASE_URL}/discover/tv",
            headers=HEADERS,
            params=params
        )
        results = response.json().get('results', [])
        for result in results:
            result['title'] = result.get('name')
        return jsonify(results)
    elif media_type == 'anime':
        params['with_keywords'] = '210024'
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif media_type == 'animation':
        params['with_genres'] = '16'
        params['vote_count.gte'] = 50
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    else:
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )

    return jsonify(response.json().get('results', []))

@app.route('/api/load_more_horizontal')
def load_more_horizontal():
    section = request.args.get('section', 'trending')
    page = request.args.get('page', 1, type=int)
    
    params = {
        'language': 'ru-RU',
        'page': page
    }
    
    # Добавляем новые условия для секций
    if section == 'bestMovies':
        params.update({
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 1000
        })
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif section == 'bestTV':
        params.update({
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 500
        })
        response = requests.get(
            f"{BASE_URL}/discover/tv",
            headers=HEADERS,
            params=params
        )
    elif section == 'bestAnimation':
        params.update({
            'with_genres': '16',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 300
        })
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif section == 'anime':
        params.update({
            'with_keywords': '210024',
            'sort_by': 'popularity.desc'
        })
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif section == 'top2024':
        params.update({
            'primary_release_year': '2024',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 100
        })
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif section == 'top2023':
        params.update({
            'primary_release_year': '2023',
            'sort_by': 'vote_average.desc',
            'vote_count.gte': 200
        })
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    elif section == 'action':
        params.update({
            'with_genres': '28',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'comedy':
        params.update({
            'with_genres': '35',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'horror':
        params.update({
            'with_genres': '27',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'scifi':
        params.update({
            'with_genres': '878',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'drama':
        params.update({
            'with_genres': '18',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'mystery':
        params.update({
            'with_genres': '9648',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    elif section == 'romance':
        params.update({
            'with_genres': '10749',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 100
        })
        response = requests.get(f"{BASE_URL}/discover/movie", headers=HEADERS, params=params)
    else:
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params=params
        )
    
    return jsonify(response.json().get('results', []))

@app.route('/genres')
def genres():
    genres_list = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
    return render_template('genres.html', genres=genres_list)

def get_trailer(movie_id):
    # Запрос к API для получения трейлеров
    response = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", headers=HEADERS)
    trailers = response.json().get('results', [])
    
    # Ищем трейлер на русском
    for trailer in trailers:
        if 'ru' in trailer.get('iso_language', ''):  # Используем get для избежания KeyError
            return trailer['key']  # Возвращаем ключ трейлера на русском
    
    # Если нет трейлера на русском, ищем на английском
    for trailer in trailers:
        if 'en' in trailer.get('iso_language', ''):
            return trailer['key']  # Возвращаем ключ трейлера на английском
    
    return None  # Если трейлеров нет

@app.route('/watch/<int:movie_id>')
def watch_movie(movie_id):
    # Здесь вы можете добавить логику для просмотра фильма
    # Например, перенаправление на страницу с фильмом или на сторонний сервис
    return redirect(f"https://www.example.com/watch/{movie_id}")  # Замените на нужный URL

@app.route('/api/actor/<actor_id>')
def get_actor_info(actor_id):
    # Получаем детальную информацию об актере
    actor_details = requests.get(
        f"{BASE_URL}/person/{actor_id}",
        params={'api_key': API_KEY, 'language': 'ru'},
        headers=HEADERS
    ).json()

    # Получаем фильмографию актера
    actor_credits = requests.get(
        f"{BASE_URL}/person/{actor_id}/movie_credits",
        params={'api_key': API_KEY, 'language': 'ru'},
        headers=HEADERS
    ).json()

    # Объединяем информацию
    actor_details['credits'] = actor_credits

    return jsonify(actor_details)

@app.route('/actor/<int:actor_id>')
def actor_details(actor_id):
    # Получаем детальную информацию об актере
    actor_response = requests.get(
        f"{BASE_URL}/person/{actor_id}",
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    actor = actor_response.json()

    # Получаем фильмографию актера
    credits_response = requests.get(
        f"{BASE_URL}/person/{actor_id}/movie_credits",
        headers=HEADERS,
        params={'language': 'ru-RU'}
    )
    actor['credits'] = credits_response.json()

    return render_template('actor.html', actor=actor)

@app.route('/api/similar_movies/<int:movie_id>')
def get_similar_movies(movie_id):
    page = request.args.get('page', 1, type=int)
    
    # Сначала получаем информацию о фильме, чтобы проверить принадлежность к коллекции
    movie_info = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'append_to_response': 'belongs_to_collection'
        }
    ).json()
    
    all_movies = []
    
    # Если фильм принадлежит коллекции, получаем все фильмы из этой коллекции
    if movie_info.get('belongs_to_collection'):
        collection_id = movie_info['belongs_to_collection']['id']
        collection_response = requests.get(
            f"{BASE_URL}/collection/{collection_id}",
            headers=HEADERS,
            params={'language': 'ru-RU'}
        )
        
        if collection_response.ok:
            collection = collection_response.json()
            # Сортируем фильмы коллекции по дате выхода
            collection_movies = sorted(
                collection.get('parts', []),
                key=lambda x: x.get('release_date', ''),
                reverse=False  # По возрастанию, чтобы части шли по порядку
            )
            all_movies.extend([m for m in collection_movies if m.get('poster_path')])
    
    # Затем получаем похожие фильмы
    similar_response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/similar",
        headers=HEADERS,
        params={
            'language': 'ru-RU',
            'page': page
        }
    )
    
    if similar_response.ok:
        similar_movies = similar_response.json().get('results', [])
        # Фильтруем похожие фильмы, исключая те, что уже есть в коллекции
        similar_movies = [
            movie for movie in similar_movies 
            if movie.get('poster_path') and 
            movie.get('vote_average', 0) > 5 and 
            movie['id'] not in [m['id'] for m in all_movies]
        ]
        all_movies.extend(similar_movies)
    
    # Если фильмов всё ещё мало, добавляем рекомендации
    if len(all_movies) < 20:
        recommendations = requests.get(
            f"{BASE_URL}/movie/{movie_id}/recommendations",
            headers=HEADERS,
            params={'language': 'ru-RU', 'page': page}
        ).json().get('results', [])
        
        # Фильтруем рекомендации
        recommendations = [
            movie for movie in recommendations 
            if movie.get('poster_path') and 
            movie.get('vote_average', 0) > 5 and 
            movie['id'] not in [m['id'] for m in all_movies]
        ]
        
        all_movies.extend(recommendations)
    
    return jsonify(all_movies)

if __name__ == '__main__':
    app.run(debug=True)
