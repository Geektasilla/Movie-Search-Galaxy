import sys
import os
import uuid
from mysql_connector import MySQLConnection
from log_writer import MongoConnection
from log_stats import MongoStats
from formatter import (
    print_welcome_message,
    print_help_intro,
    print_movies,
    print_genres,
    print_unique_stats,
    print_main_menu,
    CRAFT_ORANGE,
    END
)


def safe_input(data):
    """
    A wrapper around input() that handles 'end', 'back', 'help' commands
    and unexpected exits like Ctrl+C or Ctrl+Z.

    Args:
        data (str): The prompt message to display to the user.

    Returns:
        str: The user's input, or a special command string ("help_called",
             "back_called", "error_input") if a command is recognized or
             an error occurs.
    """
    try:
        user_input = input(data).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{CRAFT_ORANGE} Please use the menu or type 'end'.{END}")
        return "error_input"

    if user_input == 'help':
        print_help_intro()
        return "help_called"
    elif user_input == 'back':
        return "back_called"
    elif user_input == 'end':
        print(f"\n{CRAFT_ORANGE}Thanks for stopping by MovieSearchGalaxy! See you soon!{END}")
        sys.exit(0)
    else:
        return user_input


def get_number_input(data, min_value, max_value):
    """
    Prompts the user for a number input within a specified range.
    Handles non-numeric input, out-of-range values, and special commands.

    Args:
        data (str): The prompt message to display to the user.
        min_value (int): The minimum acceptable integer value.
        max_value (int): The maximum acceptable integer value.

    Returns:
        int or str: The validated integer input, or a special command string
                    ("help_called", "back_called") if a command is recognized.
    """
    while True:
        user_text = safe_input(data)

        if user_text in ("back_called", "help_called"):
            return user_text

        if user_text == "error_input":
            continue

        # Check if the input is a number
        if not user_text.isdigit():
            print(f"{CRAFT_ORANGE}Oops! That's not a number. Please try again.{END}")
            continue

        # Convert the input to an integer
        value = int(user_text)

        # Check if the number is within the specified range
        if value < min_value or value > max_value:
            print(f"{CRAFT_ORANGE}Oops! Range is {min_value} to {max_value}. Try again!{END}")
            continue
        return value


def handle_search_session(search_function_name, search_params, log_type, log_data, session_id):
    """
    Manages a search session, including executing the search, logging the first
    successful request, and handling paginated output.

    Args:
        search_function_name (str): The name of the search method in MySQLConnection.
        search_params (dict): A dictionary of parameters for the search function.
        log_type (str): The type of search for logging (e.g., "keyword", "genre_year").
        log_data (dict): The data to be logged for this search.
        session_id (str): The unique identifier for the current application session.
    """
    offset = 0
    while True:
        with MySQLConnection() as db:
            search_method = getattr(db, search_function_name)
            movies = search_method(**search_params, offset=offset)

            # 1. First, check if any movies were found.
            if not movies:
                if offset == 0:
                    print(f"\n{CRAFT_ORANGE}Sorry, no movies found for this search. "
                          f"Try a different search!{END}")
                else:
                    print(f"\n{CRAFT_ORANGE}Sorry, no more movies found.{END}")
                break  # Exit the search loop

            # Log the search only for the first page (offset == 0)
            if offset == 0:
                with MongoConnection() as mongo_db:
                    mongo_db.write_log_inform(log_type, log_data, session_id)

            print_movies(movies)
            while True:
                user_action = safe_input("Please, press Enter to show the next 10, "
                                         "or 'back' to return to the menu: ")
                if user_action == "back_called":
                    return
                if user_action in ("help_called", "error_input"):
                    continue
                elif user_action == "":
                    offset += 10
                    break
                else:
                    print(f"{CRAFT_ORANGE}Oops! Just press Enter or type 'back'.{END}")


def get_persistent_session_id():
    """
    Retrieves the unique user ID from a local file or generates a new one
    if the file doesn't exist. This ensures user persistence across restarts.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "user_id.txt")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            user_id = file.read().strip()
            return user_id
    else:
        new_id = str(uuid.uuid4())
        with open(file_path, "w") as file:
            file.write(new_id)
        return new_id

# Main application function
def movie_search_galaxy():
    """
    Main function for the MovieSearchGalaxy application.
    Handles application initialization, main menu, and user interactions for movie searches.
    """
    # Generate a unique ID for this entire session
    session_id = get_persistent_session_id()

    print("Linking to the film galaxy, just a moment...")
    try:
        # Attempt to establish connections to MySQL and MongoDB to verify availability
        with MySQLConnection(), MongoConnection():
            pass
    except Exception:
        print(f"\nOops, something went wrong. Check your internet or try again in a bit? ☕")
        sys.exit(1)

    print_welcome_message()
    print_help_intro()

    # Main application loop
    while True:
        print_main_menu()
        choice = safe_input("Please, select an action: ")

        if choice in ("help_called", "back_called"):
            continue

        # Search by keyword
        if choice == '1':
            while True:
                keyword = safe_input("Please, enter a keyword to search for movies: ")
                if keyword == "back_called":
                    break
                if keyword == "help_called":
                    continue
                if not keyword:
                    print(f"{CRAFT_ORANGE}You didn't enter a keyword. Please try again.{END}")
                    continue

                handle_search_session(
                    search_function_name="search_by_keyword",
                    search_params={"keyword": keyword},
                    log_type="keyword",
                    log_data={"keyword": keyword},
                    session_id=session_id
                )
                break

        # Search by genre and year range
        elif choice == '2':
            with MySQLConnection() as db:
                all_genres = db.get_all_genres()
                years = db.get_min_max_year()
                min_year, max_year = years['min_year'], years['max_year']

            while True:
                print_genres(all_genres)
                genre_id = get_number_input(f"Select a genre ID (or 'back'): ", 1, len(all_genres))
                if genre_id == "back_called":
                    break
                if genre_id == "help_called":
                    continue

                year_min_input = get_number_input(f"Enter the start year ({min_year} - {max_year}): ",
                                                  min_year, max_year)
                if year_min_input == "back_called":
                    break
                if year_min_input == "help_called":
                    continue

                year_max_input = get_number_input(f"Enter the end year ({year_min_input} - {max_year}): ",
                                                  year_min_input, max_year)
                if year_max_input == "back_called":
                    break
                if year_max_input == "help_called":
                    continue

                # Find the genre name for logging purposes
                genre_name = next((g['name'] for g in all_genres if g['category_id'] == genre_id), "")

                handle_search_session(
                    search_function_name='search_by_genre_and_year',
                    search_params={'genre_id': genre_id, 'min_year': year_min_input, 'max_year': year_max_input},
                    log_type='genre_year',
                    log_data={'genre': genre_name, 'from_year': year_min_input, 'to_year': year_max_input},
                    session_id=session_id
                )
                break

        # Search by genre
        elif choice == '3':
            with MySQLConnection() as db:
                all_genres = db.get_all_genres()

            while True:
                print_genres(all_genres)
                genre_id = get_number_input(f"Select a genre ID (or 'back'): ", 1, len(all_genres))

                if genre_id == "back_called":
                    break
                if genre_id == "help_called":
                    continue

                # Find the genre name for logging purposes
                genre_name = next((g['name'] for g in all_genres if g['category_id'] == genre_id), "")

                handle_search_session(
                    search_function_name='search_by_genre',
                    search_params={'genre_id': genre_id},
                    log_type='genre',
                    log_data={'genre': genre_name},
                    session_id=session_id
                )
                break

        # Search by year
        elif choice == '4':
            with MySQLConnection() as db:
                years = db.get_min_max_year()
                min_year, max_year = years['min_year'], years['max_year']

            while True:
                year = get_number_input(f"Enter a year between {min_year} and "
                                        f"{max_year} (or 'back'): ", min_year, max_year)
                if year == "back_called":
                    break
                if year == "help_called":
                    continue

                handle_search_session(
                    search_function_name='search_by_year',
                    search_params={'year': year},
                    log_type='year',
                    log_data={'year': year},
                    session_id=session_id
                )
                break

        # Show the top 5 popular searches and latest 5 searches
        elif choice == '5':
            try:
                with MongoStats() as stats_db:
                    # 1. Get the 5 most recent search queries
                    latest_data = stats_db.get_latest_searches(limit=5)
                    # 2. Get the 5 most popular search queries (trends)
                    popular_data = stats_db.get_popular_searches(limit=5)

                    # Print them using the formatter with different titles
                    print_unique_stats(latest_data, title="RECENTLY SEARCHED (Latest 5)")
                    print_unique_stats(popular_data, title="MOST POPULAR (Top 5 Trends)")

                    safe_input(f"\nPress Enter to return to the main menu...")
            except Exception as e:
                print(f"\n[⚠️] Could not load statistics: {e}")
        else:
            print(f"\n{CRAFT_ORANGE}Oops! Pick 1-5 or type 'end' to exit. 🍿{END}")


# Application entry point
if __name__ == '__main__':
    movie_search_galaxy()