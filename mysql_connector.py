import pymysql
from settings import MYSQL_CONFIG

# Формируем код благодаря которому в файле main можно обратится к этому классу и не писать его заново каждый раз
class MySQLConnection:
    """
    Class to handling MySQL connections.
    """
    # импортируем настройки подключения из settings.py
    def __init__(self):
        """
        Class initialization.
        """
        # Соохраняю настройки подключения во внутрь обьекта
        self.config = MYSQL_CONFIG
        # резервирование места и защита от поломок. Мы как бы "бронируем" имена переменных заранее, чтобы другие методы (__exit__) не сошли с ума, если попытаются их использовать.
        self.connection = None
        self.cursor = None

    # магический метод для открытия соединения с БД
    def __enter__(self):
        """
        Enters the context manager and establishes the database connection.
        """
        try:
            # pymysql.connect - устанавливает связь с сервером базы данных.
            # Звездочки (**) распаковывают наш словарь db_settings в аргументы функции
            # (host='...', user='...', и т.д.)
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

            # Возвращаем сам объект класса (self), чтобы переменная 'db' после 'as'
            # получила доступ ко всем будущим методам поиска (например, db.search_movie())
            return self
        # Если пароль неверный или база недоступна, ловим ошибку и выводим её
        except pymysql.MySQLError as e:
            print(f"Ошибка подключения к MySQL: {e}")
            raise

    # Вызывается АВТОМАТИЧЕСКИ при выходе из блока 'with', даже если внутри произошла ошибка.
    def __exit__(self, except_type, except_val, except_tb):
        """
         Exits the context manager and closes the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# запросы поисков. А может по индексу?
    def get_min_max_year(self):
        """
        Retrieves the minimum and maximum release years of movies.
        """
        query_range = (
            "SELECT MIN(release_year) as min_year, MAX(release_year) as max_year "
            "FROM film;"
        )
        self.cursor.execute(query_range)
        return self.cursor.fetchone()

    def get_all_genres(self):
        """
        Retrieves all genres from the database.
        """
        query_genres = "SELECT category_id, name FROM category ORDER BY name;"
        self.cursor.execute(query_genres)
        return self.cursor.fetchall()


    def search_films(self, keyword=None, genre_id=None, min_year=None, max_year=None,year=None, offset=0, limit=10):
        """
        Searches for movies by various criteria(keyword, genres, year)
        """
        query_keyword = (
            "SELECT film_id, title, description, release_year"
            "FROM film"
            "WHERE MATCH(title, description) AGAINST(%s IN NATURAL LANGUAGE MODE"
            "LIMIT %s OFFSET %s;"
        )
        select_part = "SELECT f.film_id, f.title, f.description, f.release_year"
        from_part = "FROM film AS f"
        join_part = ""

        where_conditions = []
        params = []

        # Search by keyword
        if keyword:
            where_conditions.append("MATCH(f.title, f.description) AGAINST(%s IN NATURAL LANGUAGE MODE)")
            params.append(keyword)

        # Search by genre
        if genre_id:
            join_part = "JOIN film_category AS fc ON f.film_id = fc.film_id"
            where_conditions.append("fc.category_id = %s")
            params.append(genre_id)

        # Search by range of years
        if min_year and max_year:
            where_conditions.append("f.release_year BETWEEN %s AND %s")
            params.extend([min_year, max_year])

        # Search by year
        if year:
            where_conditions.append("f.release_year = %s")
            params.append(year)

        # makes a final query
        where_part = ""
        if where_conditions:
            where_part = "WHERE " + " AND ".join(where_conditions)

        limit_part = "LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        final_query = f"{select_part} {from_part} {join_part} {where_part} {limit_part};"

        # для отладки
        # print(f"DEBUG: Query: {final_query}")
        # print(f"DEBUG: Params: {params}")

        self.cursor.execute(final_query, params)
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword, offset=0, limit=10):
        """
        Searches for movies by keyword.
        """
        return self.search_films(keyword=keyword, offset=offset, limit=limit)

    def search_by_genre_and_year(self, genre_id, min_year, max_year, offset=0):
        """
        Searches for movies by genre and release year.
        """
        return self.search_films(genre_id=genre_id, min_year=min_year, max_year=max_year, offset=offset)

    def search_by_genre(self, genre_id, offset=0):
        """
        Searches for movies by genre.
        """
        return self.search_films(genre_id=genre_id, offset=offset)


    def search_by_year(self, year, offset=0):
        """
        Searches for movies by release year.
        """
        return self.search_films(year=year, offset=offset)


# connections checking
# if __name__ == '__main__':
#     print("connections checking MySOL")
#     try:
#         with MySQLConnection() as db:
#             print("successfully")
#     except Exception as e:
#         print(f"not_successfully{e}")


