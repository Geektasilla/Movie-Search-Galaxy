from pymongo import MongoClient
from settings import MONGO_CONFIG, MONGO_AUTH_DB, MONGO_COLLECTION_NAME
from log_writer import MongoConnection


class MongoStats(MongoConnection):
    """
    A class for extracting analytics from MongoDB logs.
    Inherits the connection logic (__enter__, __exit__) from the base class MongoConnection.
    """
    def get_top_search_queries(self, limit=5):
        """
         Returns the top N most popular search types (e.g., 'keyword', 'genre_year').

        This method uses the MongoDB aggregation framework to:
        1. Group documents by the 'search_type' field.
        2. Count the number of documents in each group.
        3. Sort the groups by count in descending order.
        4. Limit the result to the top N types.
        """
        if not self.collection:
            raise ConnectionError("Not connected to MongoDB collection.")

        pipeline = [
            {
                "$group": {
                    "_id": "$search_type",  # Group by the search_type field
                    "count": {"$sum": 1}  # Count occurrences of each type
                }
            },
            {
                "$sort": {"count": -1}  # Sort by count, descending
            },
            {
                "$limit": limit  # Limit to the top N results
            }
        ]

        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error during aggregation: {e}")
            return []

    def get_total_searches(self):
        """
        Returns the total number of search logs recorded.
        """
        if not self.collection:
            raise ConnectionError("Not connected to MongoDB collection.")

        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

# for testing
if __name__ == '__main__':
    print("Testing statistics retrieval from MongoDB...")
    try:
        with MongoStats() as stats:
            print("\n1. Retrieving total number of searches...")
            total = stats.get_total_searches()
            print(f"Total searches found: {total}")

            print("\n2. Retrieving top 5 popular search types...")
            popular_types = stats.get_popular_search_types(limit=5)
            if popular_types:
                print("-> Top search types:")
                for i, item in enumerate(popular_types, 1):
                    print(f"  {i}. Type: '{item['_id']}', Count: {item['count']}")
            else:
                print("No search statistics found yet.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")








