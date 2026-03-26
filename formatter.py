import sys
CRAFT_ORANGE = '\033[38;5;166m'
MEDIUM_GREEN = '\033[38;5;34m'
END = '\033[0m'

def print_welcome_message():
    """
    Print the welcome message.
    """
    welcome_message = f"""
{CRAFT_ORANGE}{'=' * 65}
                    WELCOME TO MOVIE SEARCH
>>>>>>{END} This is an interactive console application for quick {CRAFT_ORANGE}<<<<<<
            >>>>>>>{END} and convenient movie search {CRAFT_ORANGE}<<<<<<<<
{'=' * 65}{END}
"""
    print(welcome_message)
    sys.stdout.flush()

def print_help_intro():
    """
    Print the help introduction.
    """
    help_intro = f"""{MEDIUM_GREEN}   You can use helpful menu commands (always available)  {END}
 - 'end' — exit the app.
 - 'back' — Cancel the current entry and return to the main menu.
 - 'help' — Command Reference.
"""
    print(help_intro)
    sys.stdout.flush()

def print_main_menu():
    """
    Print the main menu.
    """
    menu_text = f"""{MEDIUM_GREEN}{'=' * 65}
                    >>>>>>> MAIN MENU <<<<<<<<<
{MEDIUM_GREEN}{'=' * 65}{END}
1. Search for a movie using a keyword in the title
2. Choose a movie based on your favorite genre and release year.
3. Choose a movie based solely on genre.
4. Choose a movie based solely on release year.
5. See which movies are searched for most often.
0. Exit
"""
    print(menu_text)

# создать функции для меню и вывода таблиц.
def print_movies(movies_list):
    """
    Displays a list of films in a neat table.
    """
    if not movies_list:
        print(f"\n{MEDIUM_GREEN}No movies found.{END}")
        return

    # заголовок таблицы
    print(f"\n{MEDIUM_GREEN}{'-' * 85}")
    print(f"{'ID': <6} | {'Title':<40} | {'Year': <6} | {'Length (min)': <15} | {'Rating'}")
    print(f"{'-' * 85}{END}")

    # вывод строк
    for movie in movies_list:
        film_id = movie.get('film_id', 'N/A')
        title = movie.get('title', 'N/A')
        if len(title) > 40:
            title = title[:37] + '...'
        year = movie.get('release_year', 'N/A')
        length = movie.get('length', 'N/A')
        rating = movie.get('rating', 'N/A')
        print(f"{film_id:<6} | {title:<40} | {year:<6} | {length:<15} | {rating}")
    print(f"{MEDIUM_GREEN}{'-' * 85}{END}\n")

def print_genres(genres_list):
    """
    Displays a list of genres in two columns for clarity.
    """
    if not genres_list:
        print(f"{CRAFT_ORANGE}Genres not found.{END}")
        return

    print(f"\n{CRAFT_ORANGE}{'=' * 45}{END}"
    f"\n{CRAFT_ORANGE}   >>>>>>>>> Available Genres <<<<<<<<<{END}"
    f"\n{CRAFT_ORANGE}{'='*45}{END}")

    # Выводим по 2 жанра в строку
    for i in range(0, len(genres_list), 2):
        col1 = genres_list[i]
        str_col1 = f"[{col1['category_id']}] {col1['name']}"

        # Проверяем, есть ли второй элемент для пары
        if i + 1 < len(genres_list):
            col2 = genres_list[i + 1]
            str_col2 = f"[{col2['category_id']}] {col2['name']}"
            # Выводим две колонки (ширина первой 30 символов)
            print(f"{str_col1:<30} {str_col2}")
        else:
            print(str_col1)
    print()


def print_stats(stats_list):
    """
    Displays statistics on popular search queries.
    """
    if not stats_list:
        print(f"\n{MEDIUM_GREEN}Search history is empty. Make your first search!{END}")
        return

    print(f"\n{CRAFT_ORANGE}==================================================")
    print(f"                <<<< TOP SEARCHES >>>>")
    print(f"=================================================={END}")

    for i, stat in enumerate(stats_list, 1):
        s_type = stat.get('search_type', 'unknown')
        params = stat.get('params', {})
        count = stat.get('count', 0)

        # Формируем читаемое описание параметров
        params_str = ", ".join([f"{k}: {v}" for k, v in params.items()])

        print(
            f"{i}. {CRAFT_ORANGE}Type:{END} {s_type:<15} | {CRAFT_ORANGE}Query:{END} {params_str:<30} | {CRAFT_ORANGE}Searched times:{END} {count}")
    print("\n")

# проверка функций
if __name__ == '__main__':
    print_welcome_message()
    print_help_intro()
    print_main_menu()

