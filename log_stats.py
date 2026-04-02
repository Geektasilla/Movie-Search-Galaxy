from log_writer import MongoConnection


class MongoStats(MongoConnection):
    """
    A class for extracting analytics and statistics from MongoDB logs.
    It inherits connection logic and the collection object from MongoConnection,
    allowing it to interact with the same MongoDB collection where logs are stored.
    """
    def get_total_logs_count(self):
        """
        Retrieves the total number of search records stored in the database.

        This method counts every document in the configured MongoDB collection
        to provide an overall count of all logged search activities.

        Returns:
            int: The total number of log entries, or 0 if an error occurs.
        """
        try:
            # count_documents({}) counts all documents in the collection
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

    def get_latest_searches(self, limit=5):
        """
        Fetches the most recent search queries from the database.

        Results are sorted in descending order by their 'timestamp' field
        to show the latest search activities first.

        Args:
            limit (int): The maximum number of latest search entries to retrieve.
                         Defaults to 5.

        Returns:
            list: A list of dictionaries, each representing a recent search log.
                  Returns an empty list if an error occurs.
        """
        try:
            # Find all documents, exclude the default '_id', sort by timestamp
            # in descending order (-1), and limit the results.
            cursor = self.collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error retrieving latest searches: {e}")
            return []

    def get_popular_searches(self, limit=5):
        """
        Calculates and retrieves the most popular search trends based on
        unique search queries.

        This method uses a MongoDB aggregation pipeline to group search logs
        and count unique instances of each search type and its parameters.
        It ensures that multiple searches by the same *session* for the exact
        same query are not overcounted, providing a more accurate popularity metric.

        Args:
            limit (int): The maximum number of popular search entries to retrieve.
                         Defaults to 5.

        Returns:
            list: A list of dictionaries, each representing a popular search trend
                  with its type, parameters, count, and last requested timestamp.
                  Returns an empty list if an error occurs.
        """
        try:
            pipeline = [
                # Stage 1: Group by search_type, params, and client_id.
                # This step is crucial for identifying unique search actions
                # performed by individual clients.
                {
                    "$group": {
                        "_id": {
                            "search_type": "$search_type",
                            "params": "$params",
                            "client_id": "$client_id"  # Now using session_id
                        },
                        "max_time": {"$max": "$timestamp"}
                    }
                },
                # Stage 2: Group the results again, this time by search_type and params.
                # This counts how many *unique sessions* performed each specific search.
                # 'search_count' will represent the number of unique sessions for that query.
                # 'last_requested' will store the most recent timestamp among all sessions
                # for this specific query.
                {
                    "$group": {
                        "_id": {
                            "search_type": "$_id.search_type",
                            "params": "$_id.params"
                        },
                        "search_count": {"$sum": 1},  # Count unique session searches
                        "last_requested": {"$max": "$max_time"}
                    }
                },
                # Stage 3: Sort the results by 'search_count' in descending order.
                # This puts the most popular searches at the top.
                {"$sort": {"search_count": -1}},
                # Stage 4: Limit the output to the top 'limit' number of results.
                {"$limit": limit},
                # Stage 5: Project (reshape) the output documents.
                # We rename '_id.search_type' to 'search_type', '_id.params' to 'params',
                # and 'last_requested' to 'timestamp' for cleaner output,
                # and exclude the internal '_id' field.
                {
                    "$project": {
                        "_id": 0,  # Exclude the default MongoDB _id
                        "search_type": "$_id.search_type",
                        "params": "$_id.params",
                        "search_count": 1,
                        "timestamp": "$last_requested"
                    }
                }
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Aggregation error: {e}")
            return []