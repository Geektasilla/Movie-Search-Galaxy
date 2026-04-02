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
    A wrapper around input() that handles 'end', 'back', 'help' commands.
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
    """
    while True:
        user_text = safe_input(data)
        if user_text in ("back_called", "help_called"):
            return user_text
        if user_text == "error_input":
            continue
        if not user_text.isdigit():
            print(f"{CRAFT_ORANGE}Oops! That's not a number. Please try again.{END}")
            continue
        value = int(user_text)
        if value < min_value or value > max_value:
            print(f"{CRAFT_ORANGE}Oops! Range is {min_value} to {max_value}. Try again!{END}")
            continue
        return value


def handle_search_session(search_function_name, search_params, log_type, log_data, client_id):
    """
    Manages a search session with pagination and logging by Client ID.
    """
    offset = 0
    while True:
        with MySQLConnection() as db:
            search_method = getattr(db, search_function_name)
            movies = search_method(**search_params, offset=offset)

            if not movies:
                if offset == 0:
                    print(f"\n{CRAFT_ORANGE}Sorry, no movies found. Try a different search!{END}")
                else:
                    print(f"\n{CRAFT_ORANGE}Sorry, no more movies found.{END}")
                break

            # We log only the first request (the first page)
            if offset == 0:
                with MongoConnection() as mongo_db:
                    mongo_db.write_log_inform(log_type, log_data, client_id)

            print_movies(movies)

            while True:
                user_action = safe_input("Please, press Enter to show the next 10, or 'back': ")
                if user_action == "back_called":
                    return  # Exit the search function to the main menu
                if user_action in ("help_called", "error_input"):
                    continue
                elif user_action == "":
                    offset += 10
                    break  # Exit the inner loop so that the outer loop (while True) updates the list
                else:
                    print(f"{CRAFT_ORANGE}Oops! Just press Enter or type 'back'.{END}")

            continue


def get_persistent_client_id():
    """
        Retrieves the unique Client ID from a local file or generates a new one
        if the file doesn't exist or is empty. This prevents "phantom" users
        (empty strings) in the database analytics.

        :return: str: The unique client identifier.
        """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "client_id.txt")

    # Check if the file exists and is NOT empty
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            client_id = file.read().strip()

        # If there is something in the file, we return it.
        if client_id:
            return client_id

    # If the file does not exist OR it is empty, create a new ID
    new_id = str(uuid.uuid4())
    with open(file_path, "w") as file:
        file.write(new_id)
    return new_id

def movie_search_galaxy():
    """
    Main function for the MovieSearchGalaxy application.
    """

    client_id = get_persistent_client_id()

    print("Linking to the film galaxy, just a moment...")
    try:
        with MySQLConnection(), MongoConnection():
            pass
    except Exception:
        print(f"\nOops, something went wrong. Check your connection? ☕")
        sys.exit(1)

    print_welcome_message()
    print_help_intro()

    while True:
        print_main_menu()
        choice = safe_input("Please, select an action: ")

        if choice in ("help_called", "back_called"):
            continue

        # Search by keyword
        if choice == '1':
            while True:
                keyword = safe_input("Please, enter a keyword to search: ")
                if keyword == "back_called": break
                if keyword == "help_called": continue
                if not keyword:
                    print(f"{CRAFT_ORANGE}Keyword is empty. Try again.{END}")
                    continue

                handle_search_session(
                    search_function_name="search_by_keyword",
                    search_params={"keyword": keyword},
                    log_type="keyword",
                    log_data={"keyword": keyword},
                    client_id=client_id
                )
                break

        # 2. Search by genre and year
        elif choice == '2':
            with MySQLConnection() as db:
                all_genres = db.get_all_genres()
                years = db.get_min_max_year()
                min_year, max_year = years['min_year'], years['max_year']

            while True:
                print_genres(all_genres)
                genre_id = get_number_input(f"Select a genre ID (or 'back'): ", 1, len(all_genres))
                if genre_id == "back_called": break

                year_min_input = get_number_input(f"Start year ({min_year}-{max_year}): ", min_year, max_year)
                if year_min_input == "back_called": break

                year_max_input = get_number_input(f"End year ({year_min_input}-{max_year}): ", year_min_input, max_year)
                if year_max_input == "back_called": break

                genre_name = next((g['name'] for g in all_genres if g['category_id'] == genre_id), "")
                handle_search_session(
                    search_function_name='search_by_genre_and_year',
                    search_params={'genre_id': genre_id, 'min_year': year_min_input, 'max_year': year_max_input},
                    log_type='genre_year',
                    log_data={'genre': genre_name, 'from_year': year_min_input, 'to_year': year_max_input},
                    client_id=client_id
                )
                break

        # 3. Search by genre
        elif choice == '3':
            with MySQLConnection() as db:
                all_genres = db.get_all_genres()

            while True:
                print_genres(all_genres)
                genre_id = get_number_input(f"Select a genre ID (or 'back'): ", 1, len(all_genres))
                if genre_id == "back_called": break

                genre_name = next((g['name'] for g in all_genres if g['category_id'] == genre_id), "")
                handle_search_session(
                    search_function_name='search_by_genre',
                    search_params={'genre_id': genre_id},
                    log_type='genre',
                    log_data={'genre': genre_name},
                    client_id=client_id
                )
                break

        # Search by year
        elif choice == '4':
            with MySQLConnection() as db:
                years = db.get_min_max_year()
                min_year, max_year = years['min_year'], years['max_year']

            while True:
                year = get_number_input(f"Enter year ({min_year}-{max_year}): ", min_year, max_year)
                if year == "back_called": break

                handle_search_session(
                    search_function_name='search_by_year',
                    search_params={'year': year},
                    log_type='year',
                    log_data={'year': year},
                    client_id=client_id
                )
                break

        # 5. Statistics
        elif choice == '5':
            try:
                with MongoStats() as stats_db:
                    latest_data = stats_db.get_latest_searches(limit=5)
                    popular_data = stats_db.get_popular_searches(limit=5)

                    print_unique_stats(latest_data, title="RECENTLY SEARCHED (Latest 5)")
                    print_unique_stats(popular_data, title="MOST POPULAR (Top 5 Trends)")

                    safe_input(f"\nPress Enter to return to the main menu...")
            except Exception as e:
                print(f"\n[⚠️] Could not load statistics: {e}")
        else:
            print(f"\n{CRAFT_ORANGE}Oops! Pick 1-5 or type 'end' to exit. 🍿{END}")


if __name__ == '__main__':
    movie_search_galaxy()