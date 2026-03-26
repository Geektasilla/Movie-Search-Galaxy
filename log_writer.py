from datetime import datetime
import pymongo
from settings import MONGO_CONFIG, MONGO_AUTH_DB, MONGO_COLLECTION_NAME

class MongoConnection:
    """
    A class for connecting to MongoDB and logging.
    """
    def __init__(self):
        """ Class initialization. """
        # Соохраняю настройки подключения во внутрь обьекта
        self.config_url = MONGO_CONFIG
        self.db_name = MONGO_AUTH_DB
        self.collection_name = MONGO_COLLECTION_NAME

        self.client = None
        self.collection = None

    def __enter__(self):
        """ Enter in context: connect to MongoDB and create a collection.
        :return:
        """
        try:
            # connectin with MongoDB
            self.client = pymongo.MongoClient(self.config_url)
            # choosing a database
            database = self.client[self.db_name]
            # choosing a collection
            self.collection = database[self.collection_name]
            # returning the object to colling methods
            return self

        except pymongo.errors.ConnectionError as e:
            print(f"Ошибка подключения к MongoDB: {e}:")
            raise

    def __exit__(self, except_type, except_val, except_tb):
        """
        Exit from context: clous a network connection.
        :return:
        """
        if self.client:
            self.client.close()

# сохранить информацию о детали поискового запросв в словарь
    def write_log_inform(self, search_type, params, results_count):
        """
        Saves the search query details to a MongoDB collection.
        :param search_type: Search type (e.g., ‘keyword’ or ‘genre_and_year’)
        :param params: Dictionary of search parameters (e.g., {‘keyword’: ‘Matrix’} or {‘genre’: 1, ‘year’: 2005})
        :param results_count: Number of movies found
        """

        log_inform_searching = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }
        try:
            self.collection.insert_one(log_inform_searching)
        except Exception:
            print("\n[⚠️] Unable to save your search history. However, your search results are still available!")






#
# # connections checking
# if __name__ == "__main__":
#     print(f"С")
#     try:
#         with MongoConnection() as db:
#             print(f"connections checking MongoDB: {db.db_name}")
#             print(f"choosed the collection:{db.collection_name}")
#     except Exception as e:
#         print(f"not_successfully{e}")

