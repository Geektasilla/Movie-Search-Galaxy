import sys
from datetime import datetime

# Define ANSI escape codes for text coloring
CRAFT_ORANGE = '\033[38;5;166m'
MEDIUM_GREEN = '\033[38;5;34m'
END = '\033[0m'


def print_welcome_message():
    """
    Prints a formatted welcome message to the console.
    """
    welcome_message = f"""
{CRAFT_ORANGE}{'=' * 65}
                    WELCOME TO MOVIE SEARCH GALAXY
>>>>>>{END} This is an interactive console application for quick {CRAFT_ORANGE}<<<<<<
            >>>>>>>{END} and convenient movie search {CRAFT_ORANGE}<<<<<<<<
{'=' * 65}{END}
"""
    print(welcome_message)
    sys.stdout.flush()  # Ensure the message is displayed immediately


def print_help_intro():
    """
    Prints an introduction to available help commands.
    """
    help_intro = f"""\n{MEDIUM_GREEN}   You can use helpful menu commands (always available)  {END}
 - 'end' — exit the app.
 - 'back' — Cancel the current entry and return to the main menu.
 - 'help' — Command Reference.\n
"""
    print(help_intro)
    sys.stdout.flush()  # Ensure the message is displayed immediately


def print_main_menu():
    """
    Prints the main menu options for the Movie Search Galaxy application.
    """
    menu_text = f"""{MEDIUM_GREEN}{'=' * 60}
             >>>>>>> MAIN MENU <<<<<<<<<
{MEDIUM_GREEN}{'=' * 60}{END}
1. Got a movie in mind? (Search by title or keyword)
2. The perfect combo! (Discover by genre and year)
3. In the mood for a specific vibe? (Browse by genre)
4. Feeling nostalgic? (Travel through time by release year)
5. Curious what's trending? (Top searches & analytics)
"""
    print(menu_text)


def print_movies(movies_list):
    """
    Displays a list of films in a formatted table.

    Args:
        movies_list (list): A list of dictionaries, where each dictionary
                            represents a movie with keys like 'film_id',
                            'title', 'release_year', 'length', 'rating'.
    """
    if not movies_list:
        print(f"\n{MEDIUM_GREEN}No movies found.{END}")
        return

    # Print table header
    print(f"\n{CRAFT_ORANGE}{'=' * 85}")
    print(f"{'ID': <6} | {'Title':<40} | {'Year': <6} | "
          f"{'Length (min)': <15} | {'Rating'}")
    print(f"{'=' * 85}{END}")

    # Print each movie's details
    for movie in movies_list:
        film_id = movie.get('film_id', 'N/A')
        title = movie.get('title', 'N/A')
        # Truncate long titles to fit the table
        if len(title) > 40:
            title = title[:37] + '...'
        year = movie.get('release_year', 'N/A')
        length = movie.get('length', 'N/A')
        rating = movie.get('rating', 'N/A')
        print(f"{film_id:<6} | {title:<40} | {year:<6} | "
              f"{length:<15} | {rating}")
    print(f"{CRAFT_ORANGE}{'=' * 85}{END}\n")


def print_genres(genres_list):
    """
    Displays a list of genres in two columns for better readability.

    Args:
        genres_list (list): A list of dictionaries, where each dictionary
                            represents a genre with keys like 'category_id'
                            and 'name'.
    """
    if not genres_list:
        print(f"{CRAFT_ORANGE}Genres not found.{END}")
        return

    # Print header for genres
    print(f"\n{CRAFT_ORANGE}{'=' * 45}{END}"
          f"\n{CRAFT_ORANGE}   >>>>>>>>> Available Genres <<<<<<<<<{END}"
          f"\n{CRAFT_ORANGE}{'='*45}{END}")

    # Print genres in two columns
    for i in range(0, len(genres_list), 2):
        col1 = genres_list[i]
        str_col1 = f"{col1['category_id']}.".ljust(4) + col1['name']

        if i + 1 < len(genres_list):
            col2 = genres_list[i + 1]
            str_col2 = f"{col2['category_id']}.".ljust(4) + col2['name']
            print(f"{str_col1:<25}{str_col2}")
        else:
            print(f"{str_col1}")
    print(f"{CRAFT_ORANGE}{'='*45}{END}\n")


def print_latest_stats(stats_list):
    """
    Displays the 5 most recent search actions (raw history).
    Shows what was searched last, sorted by time.

    Args:
        stats_list (list): A list of dictionaries, each representing a recent
                           search log entry.
    """
    if not stats_list:
        print(f"\n{MEDIUM_GREEN}No stats yet. Be the first to search!{END}")
        return

    print(f"\n{CRAFT_ORANGE}--- WHAT'S POPULAR RIGHT NOW? ---{END}")
    for i, item in enumerate(stats_list, 1):
        s_type = item.get('_id', 'Unknown')
        count = item.get('count', 0)
        print(f" {i}. {s_type:<15} | Searches: {CRAFT_ORANGE}{count}{END}")


def print_unique_stats(stats_list, title="TOP 5 SEARCHES"):
    """
    Displays the top 5 most popular unique search queries (Trends) or
    recently searched queries.

    Args:
        stats_list (list): A list of dictionaries, each representing a unique
                           search query with its count and last timestamp.
        title (str): The title to display above the statistics table.
    """
    if not stats_list:
        print(f"\n{MEDIUM_GREEN}   No search history yet.{END}")
        return

    sep = f"{CRAFT_ORANGE}{'=' * 75}{END}"

    print(f"\n{sep}")
    print(f"          {CRAFT_ORANGE}>>>>>>>>> {title} <<<<<<<<<{END}")
    print(sep)

    header = f" {'Method':<20} | {'Parameters':<22} | {'Times':<4} | {'Date & Time'}"
    print(header)
    print(f"{CRAFT_ORANGE}{'-' * 75}{END}")

    for i, item in enumerate(stats_list, 1):
        tech_name = item.get('search_type', 'unknown')
        # Format the search type for better readability
        friendly_type = f"By {tech_name.replace('_', ' & ').title()}"

        params = item.get('params', {})
        # Convert parameter values to a comma-separated string
        query_str = ", ".join([str(v) for v in params.values()])

        # Truncate query string if too long to fit in the column
        if len(query_str) > 22:
            query_str = query_str[:19] + "..."

        count = item.get('search_count', 0)
        last_search = item.get('timestamp')
        # Format timestamp if available
        date_str = last_search.strftime("%Y-%m-%d %H:%M") if last_search else "N/A"

        # Print formatted statistics row
        print(f" {i:>2}. {friendly_type:<16} | {query_str:<22} | "
              f"{count:<4} | {date_str}")

    print(f"{sep}\n")


# # This block allows testing the formatter functions directly when the script is run
# if __name__ == '__main__':
#     print_welcome_message()
#     print_help_intro()
#     print_main_menu()
