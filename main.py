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

# проверка цифры ли это
        if not user_text.isdigit():
            print("Oops! Please enter a valid number.")
            continue

# превращаем текст в число, если пользователь нечаянно введет цифры в кавычках
        value = int(user_text)

# проверяем попадает ли число в нужный диапазон
        if value < min_value or value > max_value:
            print(f"Oops! The number must be between {min_value} and {max_value}. Try again.")
            continue
        return value

# основная функция
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

    while True:
        print_main_menu()
        choice = safe_input("Select an action: ")

        if choice in ("help_called", "back_called"):
            continue

# search by keyword
    if choice == '1':
        while True:
            keyword = safe_input("Enter a keyword to search for movies: ")
            if keyword == "back_called":
                break
            if not keyword:
                print("You didn't enter a keyword. Please try again.")
                continue

            offset = 0
            while True:
                with MySQLConnection() as db, MongoConnection() as mongo_db:
                    movies = db.search_by_keyword(keyword, offset)
                    if offset == 0 and movies:
                        mongo_db.write_log_inform("keyword", {"keyword": keyword}, len(movies))
                print_movies(movies)

                if not movies:
                    if offset == 0:
                        pass
                    else:
                        print("No more movies found.")
                    break
    # пагинация результатов поиска  Limit ofset?  Fetch?
                user_action = safe_input("Press Enter to show the next 10, or 'back' to return to the menu: ")
                if user_action == "back_called":
                    break
                offset += 10
            break

    # search by genre and year
    elif choice == '2':
        with MySQLConnection() as db:
           all_genres =


    # search by genre
            elif choice == '3':
                pass
    # search by year
            elif choice == '4':
                pass
    # show the top 5 popular searches
            elif choice == '5':
                pass
    # exit
            elif choice == '0':
                print("\nThanks for stopping by MovieSearch! I hope your evening is filled with amazing scenes. See you soon! ✨🍿")
                sys.exit(0)
            else:
                print("\nOops! Looks like that’s the wrong button... 🍿 Please pick an option from the menu (a number from 0 to 5).")

# запуск
if __name__ == '__main__':
    movie_search_galaxy()




