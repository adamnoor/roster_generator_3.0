from functions import *

def run_read():
    initialize_current_table()
    keep_running = True
    current_players = []
    included_players = []
    excluded_players = []

    while keep_running:
        min_projection = get_min_max_value("MIN", "projection")
        max_projection = get_min_max_value("MAX", "projection")
        min_budget = get_min_max_value("MIN", "budget")
        max_budget = get_min_max_value("MAX", "budget")
        number_of_rosters = get_count()
        user_input = get_user_choice(min_projection, max_projection, min_budget, max_budget, number_of_rosters)
        if user_input == "0":
            current_players = get_current_players(current_players)
            player = get_player_selection("include", current_players)
            if player not in included_players:
                included_players.append([player])
                add_to_table("include", included_players)
                included_players = implement_filter("include", min_budget, max_budget, min_projection, max_projection, included_players, excluded_players)
            else:
                print(player + " is already included.  Let's try this again...")
                print("")
        elif user_input == "1":
            current_players = get_current_players(current_players)
            player = get_player_selection("exclude", current_players)
            excluded_players.append([player])
            add_to_table("exclude", excluded_players)
            excluded_players = implement_filter("exclude", min_budget, max_budget, min_projection, max_projection, included_players, excluded_players)
        elif user_input == "2":
            min_max_obj = min_max_restriction("budget", min_budget, max_budget)
            min_budget = min_max_obj[0]
            max_budget = min_max_obj[1]
            implement_filter("budget", min_budget, max_budget, min_projection, max_projection, included_players, excluded_players)
        elif user_input == "3":
            min_max_obj = min_max_restriction("projection", min_projection, max_projection)
            min_projection = min_max_obj[0]
            max_projection = min_max_obj[1]
            implement_filter("projection", min_budget, max_budget, min_projection, max_projection, included_players, excluded_players)
        elif user_input == "4":
            write_rosters_to_csv()
            run_read()
        elif user_input == "5":
            keep_running = False
            write_rosters_to_csv()
            clear_space(["current", "included_players", "excluded_players"])
        else:
            keep_running = False
            clear_space(["current", "included_players", "excluded_players"])

