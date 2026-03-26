import pymongo
from settings import MONGO_CONFIG, MONGO_AUTH_DB, MONGO_COLLECTION_NAME
from log_writer import MongoConnection
class MongoStats(MongoConnection):
    """
    A class for extracting analytics from MongoDB logs.
    Inherits the connection logic (__enter__, __exit__) from the base class MongoConnection.
    """
    def get_top_search_queries(self, limit=5):
        """
        Return top 5 most popular search queries.
        """
# потом пишем тут запрос после того как в базе появятся данные логирования
# и по ним надо будет найти то 5 популярных запросов.
#    log_inform_searching = {
#             "timestamp": datetime.now(),
#             "search_type": search_type,
#             "params": params,
#             "results_count": results_count
#         }


