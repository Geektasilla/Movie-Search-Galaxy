import pymysql
from settings import MYSQL_CONFIG

# Формируем код благодаря которому в файле main можно обратится к этому классу и не писать его заново каждый раз
class MySQLConnection:
    """
    Класс для подключения к MySQL.
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
        Enter in context.
        """
        try:
            # pymysql.connect - устанавливает связь с сервером базы данных.
            # Звездочки (**) распаковывают наш словарь db_settings в аргументы функции
            # (host='...', user='...', и т.д.)
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()

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
         Exit from context.
        :param except_type:
        :param except_val:
        :param except_tb:
        :return:
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# запросы поисков
    def get_min_max_year(self):
        pass

    def get_all_genres(self):
        pass

    def search_by_keyword(keyword, offset=0):
        pass

    def search_by_genre_and_year(genre_id, min_year, max_year, offset=0):
        pass

#   принцип наследования у классов а это функция, декоратор?
    def search_by_genre(genre_id, offset=0):
        pass

    def search_by_year(year, offset=0)




# 1. `get_min_max_years()`: [Предстоит добавить]
# 2. `get_all_genres()`: [Предстоит добавить]
# 3. `search_by_keyword(keyword, offset=0)`: [Предстоит добавить]
# 4. `search_by_genre_and_year(genre_id, min_year, max_year, offset=0)`: [Предстоит добавить]
#    - Запрос с `JOIN` таблиц `film`, `film_category` и фильтрацией `WHERE category_id = %s AND release_year BETWEEN %s AND %s LIMIT 10 OFFSET %s`.
# 5. `search_by_genre(genre_id, offset=0)`: [Предстоит добавить]
# 6. `search_by_year(year, offset=0)`: [Предстоит добавить]




# connections checking
# if __name__ == '__main__':
#     print("connections checking MySOL")
#     try:
#         with MySQLConnection() as db:
#             print("successfully")
#     except Exception as e:
#         print(f"not_successfully{e}")


