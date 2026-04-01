# MovieSearchGalaxy

## Project Overview
MovieSearchGalaxy is a user-friendly interactive console application designed to help you search for movies from a MySQL database (specifically, it's built to work with a Sakila-like database schema). It provides various search options and logs your search queries to a MongoDB database for statistics.

## Features
*   **Keyword Search**: Find movies by title.
*   **Genre & Year Search**: Search for movies by genre and a specific year range.
*   **Genre Search**: Find movies belonging to a particular genre.
*   **Year Search**: Discover movies released in a specific year.
*   **Search Statistics**: View the 5 most recent and 5 most popular search queries.
*   **Pagination**: Search results are displayed in manageable chunks (10 movies at a time) to prevent console overload.
*   **User-Friendly Interface**: Global commands (`end`, `back`, `help`) are available throughout the application for easy navigation.
*   **Robust Input Validation**: The application handles incorrect user input gracefully, preventing crashes and guiding the user.

## Installation

### Prerequisites
Before you begin, ensure you have the following installed on your system:
*   **Python 3.x** (e.g., Python 3.8 or newer)
*   **MySQL Database**: The application requires access to a MySQL database. It's designed to work with the Sakila sample database schema, but can be adapted for others.
*   **MongoDB Database**: Used for storing search logs and generating statistics.

### Setup Steps

1.  **Clone the Repository**:
    First, clone the project repository to your local machine:
    ```bash
    git clone https://github.com/your-username/MovieSearchGalaxy.git
    cd MovieSearchGalaxy
    ```
    *(Note: Replace `https://github.com/your-username/MovieSearchGalaxy.git` with the actual URL of your repository.)*

2.  **Create a Virtual Environment** (recommended):
    It's good practice to create a virtual environment to manage project dependencies:
    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment**:
    *   **Windows**:
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install Dependencies**:
    Install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables**:
    Create a file named `.env` in the root directory of your project. This file will store your database connection details and other sensitive information. Refer to `settings.py` for the expected variable names.

    Example `.env` file content:
    ```
    MYSQL_READ_HOST=your_mysql_host
    MYSQL_READ_USER=your_mysql_user
    MYSQL_READ_PASSWORD=your_mysql_password
    MYSQL_READ_DB=sakila
    MYSQL_READ_PORT=3306

    MONGO_HOST=your_mongo_host
    MONGO_USER=your_mongo_user
    MONGO_PASSWORD=your_mongo_password
    MONGO_AUTH_DB=admin
    MONGO_COLLECTION_NAME=movie_searches
    ```
    *Replace `your_mysql_host`, `your_mysql_user`, `your_mysql_password`, `your_mongo_host`, `your_mongo_user`, `your_mongo_password` with your actual database credentials. `MONGO_AUTH_DB` is typically `admin` or the database where your MongoDB user is defined.*

## Usage

To start the MovieSearchGalaxy application, ensure your virtual environment is activated and run the `main.py` script:

```bash
python main.py
```

The application will present you with a main menu. Follow the on-screen prompts to navigate through the different search options and interact with the movie database.

### Global Commands
The following commands are available at most input prompts:
*   `end`: Gracefully exits the application.
*   `back`: Returns to the previous menu or the main menu.
*   `help`: Displays a brief overview of available commands and application features.

## Project Structure
*   `main.py`: The primary entry point of the application. It orchestrates user interaction, menu navigation, and calls to other modules.
*   `mysql_connector.py`: This module acts as the Data Access Object (DAO) for MySQL, handling all database queries related to movies, genres, and years.
*   `log_writer.py`: Responsible for writing user search queries and their results into the MongoDB database for logging purposes.
*   `log_stats.py`: Retrieves and processes search statistics (e.g., most popular queries, latest queries) from MongoDB.
*   `formatter.py`: Contains utility functions for formatting and displaying text output in the console, such as movie lists, menus, and welcome messages.
*   `settings.py`: Stores configuration parameters for database connections (MySQL and MongoDB) and other application settings.
*   `requirements.txt`: Lists all external Python libraries required for the project.
*   `BACKLOG.md`: Provides detailed documentation of the application's architecture, logic, and flow.
*   `README.md`: This file, providing a general overview and instructions for the project.
