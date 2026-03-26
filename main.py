import sys
from mysql_connector import MySQLConnection
from log_writer import MongoConnection
from log_stats import MongoStats
from formatter import print_welcome_message, print_help_intro, print_movies, print_genres, print_stats, print_main_menu

#логика безопасного ввода
def safe_input(data):
    """
    A wrapper around input() that handles the global commands “end”, “back” and “help”.
    """
    user_input = input(data).strip().lower()

    if user_input == 'help':
        print_help_intro()
        return "help_called"
    elif user_input == 'back':
        return "back_called"
    elif user_input == 'end':
        print("\nThanks for stopping by MovieSearch! I hope your evening is filled with amazing scenes. See you soon! ✨🍿")
        sys.exit(0)
    else:
        return user_input

# обрабатываем разные ошибки ввода
def get_number_input(data, min_value, max_value):
    """
    Asks for a number (e.g. a year or a genre ID).
    If text or a number outside the range is entered, it asks the user to try again.
    """
    while True:
        user_text = safe_input(data)

        if user_text in ("back_called","help_called"):
            return user_text

        # check if the input is a number
        if not user_text.isdigit():
            print("Oops! Please enter a valid number.")
            continue

        # convert the input to an integer
        value = int(user_text)

        # check if the number is within the specified range
        if value < min_value or value > max_value:
            print(f"Oops! The number must be between {min_value} and {max_value}. Try again.")
            continue
        return value

def handle_search_session(search_function_name, search_params, log_type, log_data):
    """
    Manages a search session with pagination.
    - Executes the search.
    - Logs the first successful request.
    - Handles paginated output.
    """
    offset = 0
    while True:
        with MySQLConnection() as db:
            search_method = getattr(db, search_function_name)
            movies = search_method(**search_params, offset=offset)
            if offset == 0 and movies:
                with MongoConnection() as mongo_db:
                    mongo_db.write_log_inform(log_type, log_data, len(movies))

            print_movies(movies)

            if not movies:
                if offset == 0:
                    print("Sorry, no movies found for this search. Try a different search!")
                else:
                    print("Sorry,no more movies found.")
                break
            while True:
                user_action = safe_input("Please, press Enter to show the next 10, or 'back' to return to the menu: ")
                if user_action == "back_called":
                    return
                elif user_action == "":
                    offset += 10
                    break
                else:
                    print("Oops! Invalid input. Please press Enter or type 'back'.")

def movie_search_galaxy():
    """
    General function app MovieSearchGalaxy
    """
    print("Linking to the film galaxy, just a moment...")
    try:
        with MySQLConnection(), MongoConnection():
            pass
    except Exception as e:
        print(f"\nOops, something went wrong behind the scenes. We couldn't reach the database... Check your internet or try again in a bit? ☕")
        sys.exit(1)

    print_welcome_message()
    print_help_intro()

    # General menu
    while True:
        print_main_menu()
        choice = safe_input("Please, select an action: ")

        if choice in ("help_called", "back_called"):
            continue

    # search by keyword
        if choice == '1':
            while True:
                keyword = safe_input("Please, enter a keyword to search for movies: ")
                if keyword == "back_called":
                    break
                if not keyword:
                    print("You didn't enter a keyword. Please try again.")
                    continue

                handle_search_session(
                    search_function_name="search_by_keyword",
                    search_params={"keyword": keyword},
                    log_type="keyword",
                    log_data={"keyword": keyword}
                )
                break

        # search by genre and year
        elif choice == '2':
            with MySQLConnection() as db:
               all_genres = db.get_all_genres()
               years = db.get_min_max_year()
               min_year, max_year = years['min_year'], years['max_year']

            while True:
                print_genres(all_genres)
                genre_id = get_number_input(f"Select a genre ID (or 'back': ", 1, len(all_genres))
                if genre_id == "back_called":
                    break

                year_min_input = get_number_input(f"Enter the start year ({min_year} - {max_year}): ", min_year, max_year)
                if year_min_input == "back_called":
                    break

                year_max_input = get_number_input(f"Enter the end year({year_min_input} - {max_year}): ", year_min_input, max_year)
                if year_max_input == "back_called":
                    break

                genre_name = next((g['name'] for g in all_genres if g['category_id'] == genre_id), "")

                handle_search_session(
                    search_function_name = 'search_by_genre_and_year',
                    search_params = {'genre_id': genre_id, 'min_year': year_min_input, 'max_year': year_max_input},
                    log_type = 'genre_year',
                    log_data = {'genre': genre_name, 'from_year': year_min_input, 'to_year': year_max_input}
                )
                break

        # search by genre
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
                    log_data={'genre': genre_name}
                )
                break
        # search by year
        elif choice == '4':
            with MySQLConnection() as db:
                years = db.get_min_max_year()
                min_year, max_year = years['min_year'], years['max_year']

            while True:
                year = get_number_input(f"Enter a year between {min_year} and {max_year} (or 'back'): ", min_year,
                                        max_year)
                if year == "back_called": break

                handle_search_session(
                    search_function_name='search_by_year',
                    search_params={'year': year},
                    log_type='year',
                    log_data={'year': year}
                )
                break

        # show the top 5 popular searches
        elif choice == '5':
            try:
                with MongoStats() as stats:
                    popular_searches = stats.get_popular_search_types()
                    total_searches = stats.get_total_searches()
                print_stats(popular_searches, total_searches)
            except Exception as e:
                print(f"Could not retrieve stats. Error: {e}")

            safe_input("Press Enter to return to the main menu.")
            continue

        # exit
        elif choice == '0':
            print("\nThanks for stopping by MovieSearch! I hope your evening is filled with amazing scenes. See you soon! ✨🍿")
            sys.exit(0)
        else:
            print("\nOops! Looks like that’s the wrong button... Please pick an option from the menu (a number from 0 to 5).")

# запуск
if __name__ == '__main__':
    movie_search_galaxy()




