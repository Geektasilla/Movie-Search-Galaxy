import pymysql
from settings import MYSQL_CONFIG


class MySQLConnection:
    """
    Class to handling MySQL connections.
    This class provides a context manager for connecting to a MySQL database.
    """
    def __init__(self):
        """
        Initializes the MySQLConnection object with configuration from settings.
        """
        # Store connection settings within the object
        self.config = MYSQL_CONFIG
        # Initialize connection and cursor to None, to be set when entering context
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Enters the context manager and establishes the database connection.
        Connects to the MySQL database using parameters from self.config.
        Initializes a DictCursor for fetching results as dictionaries.
        """
        try:
            # Establish connection to the database server
            # The **self.config unpacks the dictionary into keyword arguments
            self.connection = pymysql.connect(**self.config)
            # Create a cursor object, using DictCursor to return results as dictionaries
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

            # Return the instance itself to be used with the 'as' keyword in a 'with' statement
            return self
        except pymysql.MySQLError as e:
            # Catch and print any MySQL connection errors, then re-raise
            print(f"Error connecting to MySQL: {e}")
            raise

    def __exit__(self, except_type, except_val, except_tb):
        """
        Exits the context manager and closes the database connection.
        This method is automatically called when exiting the 'with' block,
        even if an error occurred.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_min_max_year(self):
        """
        Retrieves the minimum and maximum release years of movies from the 'film' table.
        """
        query_range = (
            "SELECT MIN(release_year) as min_year, MAX(release_year) as max_year "
            "FROM film;"
        )
        self.cursor.execute(query_range)
        return self.cursor.fetchone()

    def get_all_genres(self):
        """
        Retrieves all genres (categories) from the 'category' table, ordered by name.
        """
        query_genres = "SELECT category_id, name FROM category ORDER BY name;"
        self.cursor.execute(query_genres)
        return self.cursor.fetchall()

    def search_films(self, keyword=None, genre_id=None, min_year=None,
                     max_year=None, year=None, offset=0, limit=10):
        """
        Searches for movies based on various criteria such as keyword in title,
        genre, and release year (single year or a range).

        Args:
            keyword (str, optional): Keyword to search in film titles.
            genre_id (int, optional): ID of the genre to filter by.
            min_year (int, optional): Minimum release year for a range search.
            max_year (int, optional): Maximum release year for a range search.
            year (int, optional): Specific release year to filter by.
            offset (int, optional): Offset for pagination. Defaults to 0.
            limit (int, optional): Limit for pagination. Defaults to 10.

        Returns:
            list: A list of dictionaries, each representing a film matching the criteria.
        """
        select_part = ("SELECT f.film_id, f.title, f.description, "
                       "f.release_year, f.length, f.rating ")
        from_part = " FROM film AS f"
        join_part = ""

        where_conditions = []
        params = []

        # Search by keyword in film title
        if keyword:
            where_conditions.append("f.title LIKE %s")
            params.append(f"%{keyword}%")

        # Search by genre
        if genre_id:
            join_part = " JOIN film_category AS fc ON f.film_id = fc.film_id"
            where_conditions.append("fc.category_id = %s")
            params.append(genre_id)

        # Search by range of years
        if min_year and max_year:
            where_conditions.append("f.release_year BETWEEN %s AND %s")
            params.extend([min_year, max_year])

        # Search by specific year
        if year:
            where_conditions.append("f.release_year = %s")
            params.append(year)

        # Construct the WHERE clause
        where_part = ""
        if where_conditions:
            where_part = " WHERE " + " AND ".join(where_conditions)

        # Add LIMIT and OFFSET for pagination
        limit_part = " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        # Assemble the final query
        final_query = (select_part + from_part + join_part +
                       where_part + limit_part + ";")

        self.cursor.execute(final_query, tuple(params))
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword, offset=0, limit=10):
        """
        Searches for movies by keyword in their title.
        """
        return self.search_films(keyword=keyword, offset=offset, limit=limit)

    def search_by_genre_and_year(self, genre_id, min_year, max_year, offset=0):
        """
        Searches for movies by genre and a range of release years.
        """
        return self.search_films(genre_id=genre_id, min_year=min_year,
                                 max_year=max_year, offset=offset)

    def search_by_genre(self, genre_id, offset=0):
        """
        Searches for movies by genre.
        """
        return self.search_films(genre_id=genre_id, offset=offset)

    def search_by_year(self, year, offset=0):
        """
        Searches for movies by a specific release year.
        """
        return self.search_films(year=year, offset=offset)