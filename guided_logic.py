from functions import *

def get_position(position):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    players = []
    player_objects = cur.execute("SELECT DISTINCT " + position + " FROM current")

    for element in player_objects:
        players.append(element[0])
    
    return players

def get_flex():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    players = []
    player_objects = cur.execute('''
        
        SELECT DISTINCT rb1 FROM current
            UNION 
        SELECT DISTINCT rb2 FROM current
            UNION 
        SELECT DISTINCT wr1 FROM current
            UNION 
        SELECT DISTINCT wr2 FROM current
            UNION 
        SELECT DISTINCT wr3 FROM current
            UNION 
        SELECT DISTINCT te FROM current
            UNION 
        SELECT DISTINCT fx FROM current
            UNION 
        SELECT DISTINCT dst FROM current
    ''')

    for element in player_objects:
        players.append(element[0])
    
    
    return players

def get_player_array(plyr_list):
    for i, element in enumerate (plyr_list):
        print("Select " + str(i) + " to include " + element)
    
    
    user_input = input("Select players to include (separate by comma): ")
    players = []
    for element in user_input:
        if plyr_list[element] not in players:
            players.append(plyr_list[element])

    return players


def set_included_players(qb, flex_array):
    players = []
    if qb is not None:
        players.append(qb)
    if len(flex_array) > 0:
        for element in flex_array:
            players.append(element)
    return players

def set_excluded_players(included, all):
    all_players = []
    for element in all:
        if element not in included:
            all_players.append(element)
    for i, element in enumerate (all_players):
        print("Select " + str(i) + " to exclude " + element)
    user_input = input("Select players to exclude (separate by comma): ")
    players = []
    for element in user_input:
        if all_players[element] not in players:
            players.append(all_players[element])

    return players



def run_guided():

    initialize_current_table()
    current_players = get_current_players([])
    all_qbs = get_position("qb")
    all_flex = get_flex()
    excluded_players = []
    print("Select a Quarterback")
    qb = get_player_selection("include", all_qbs)
    
    flex_included = get_player_array(all_flex)
    included_players = set_included_players(qb, flex_included)
    excluded_players = set_excluded_players(flex_included, all_flex)
    print(excluded_players)
   

run_guided()