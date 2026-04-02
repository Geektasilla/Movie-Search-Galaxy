from datetime import datetime
import pymongo
from settings import MONGO_CONFIG, MONGO_AUTH_DB, MONGO_COLLECTION_NAME


class MongoConnection:
    """
    A class for connecting to MongoDB and logging.
    """
    def __init__(self):
        """
        Initialize connection settings from the config file.
        """
        self.config_url = MONGO_CONFIG
        self.db_name = MONGO_AUTH_DB
        self.collection_name = MONGO_COLLECTION_NAME

        self.client = None
        self.collection = None

    def __enter__(self):
        """
        Enter in context: connect to MongoDB and create a collection.
        """
        try:
            self.client = pymongo.MongoClient(self.config_url)

            self.client.admin.command('ping')

            database = self.client[self.db_name]
            self.collection = database[self.collection_name]

            return self

        except Exception as e:
            print(f"Connection error to MongoDB: {e}:")
            raise

    def __exit__(self, except_type, except_val, except_tb):
        """
        Exit from context: closes the network connection.
        """
        if self.client:
            self.client.close()

    def write_log_inform(self, search_type, params, client_id):
        """
        Saves or updates search query details in the database.

        Args:
            search_type (str): The type of search (e.g., "keyword").
            params (dict): The parameters used for the search.
            client_id (str): The unique identifier for the client.
        """
        if self.collection is None:
            return
        
        # Define the query to find an existing log entry based on search type
        # and parameters.
        filter_query = {
            "search_type": search_type,
            "params": params,
            "client_id": client_id
        }
        now = datetime.now()

        try:
            existing_log = self.collection.find_one(filter_query)
            if existing_log:
                # If the query is found, update the search count and timestamp.
                # The existing document's fields will be updated.
                self.collection.update_one(
                    {"_id": existing_log["_id"]},
                    {
                        "$inc": {"search_count": 1},
                        "$set": {"timestamp": now}
                    }
                )
            else:
                # If the query is new, insert a new log entry.
                new_log = {
                    "timestamp": now,
                    "search_type": search_type,
                    "params": params,
                    "search_count": 1,
                    "client_id": client_id  # Add the client ID to the log
                }
                self.collection.insert_one(new_log)

        except Exception as e:
            print(f"\n[⚠️] MongoDB Error: {e}")


