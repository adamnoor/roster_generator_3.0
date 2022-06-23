import sqlite3
import csv
import os
from datetime import datetime
from xml.etree.ElementInclude import include




def initialize_current_table():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    
    print("")
    print("Initializing a local table.  This may take some time...")
    cur.execute('DROP TABLE IF EXISTS current')
    cur.execute('DROP TABLE IF EXISTS included_players')
    cur.execute('DROP TABLE IF EXISTS excluded_players')
    cur.execute("CREATE TABLE current AS SELECT * FROM rosters").fetchall()
    cur.execute('''
    CREATE TABLE included_players (
        "name" TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE excluded_players (
        "name" TEXT
    )
    ''')



def get_current_players(player_list):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    players = []
    player_objects = cur.execute('''
        SELECT DISTINCT qb FROM current
            UNION
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
    
    if len(players)>0:
        return players
    else:
        return player_list


def get_min_max_value(type, field):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    select_statement = "SELECT " + type + "(" + field + ") FROM current "
    value = float(cur.execute(select_statement).fetchall()[0][0])
    if field == "projection":
        return value
    else:
        return int(value)



def get_count():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    select_statement = "SELECT COUNT(*) FROM current " 
    return int(cur.execute(select_statement).fetchall()[0][0])


def get_user_choice(min_proj, max_proj, min_budg, max_budg, count):
    print("")
    print("There are " + str(count) + " rosters")
    print("The highest projection score is " + str(max_proj))
    print("The lowest projection score is " + str(min_proj))
    print("The highest budget is " + str(max_budg))
    print("The lowest budget is " + str(min_budg))
    print("")
    print("How would you like to restrict the rosters?")
    print("")
    print("Select 0 to restrict the rosters by selecting a player to always include")
    print("Select 1 to restrict the rosters by selecting a player to always exclude")
    print("Select 2 to restrict the rosters by selecting a min and max for budgets")
    print("Select 3 to restrict the rosters by selecting a min and max for projections")
    print("Select 4 to write a CSV file containing " + str(count) + " rosters and build a new stack")
    print("Select 5 to write a CSV file containing " + str(count) + " and quit the program")
    print("Select 6 to quit the program without writing a CSV file of the current " + str(count) + " rosters")
    print("")
    return (str(input("Select an option: ")))



def get_player_selection(type, plyr_list):

    for i, element in enumerate (plyr_list):
        print("Select " + str(i) + " to " + type + " " + element)
    
    user_input = int(input("Select a player to " + type + ": "))
    return plyr_list[user_input]


def add_to_table(type, plyr_list):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    print("Getting a list of players to " + type + "...")
    cur.execute('DROP TABLE IF EXISTS ' + type +'d_players')
    cur.execute('''
    CREATE TABLE ''' + type +'''d_players (
        
        "name" TEXT
    )
    ''')

    insert_records = "INSERT INTO " + type + "d_players (name) VALUES(?)"
    
    cur.executemany(insert_records, [plyr_list[len(plyr_list)-1]])
    conn.commit()
    print("you are trying to " + type + " " + str(plyr_list[len(plyr_list)-1][0]))
    print("These are the players that must be " + type + "d: ", plyr_list)


def exclude_player_restriction(plyr_list):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    print("Getting a list of players to exclude...")
    cur.execute('DROP TABLE IF EXISTS excluded_players')
    cur.execute('''
    CREATE TABLE included_players (
        
        "name" TEXT
    )
    ''')

    insert_records = "INSERT INTO excluded_players (name) VALUES(?)"
    
    cur.executemany(insert_records, [plyr_list[len(plyr_list)-1]])
    conn.commit()
    print("you are trying to exclude " + str(plyr_list[len(plyr_list)-1][0]))
    print("These are the players that must be excluded: ", plyr_list)





def test_filter(state, min_bud, max_bud, min_proj, max_proj, incl_plyrs, excl_plyrs):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()

    # select_statement = "SELECT * FROM current WHERE budget >= " + str(min_bud) 
    # select_statement = "SELECT * FROM current WHERE budget <= " + str(max_bud) 
    # select_statement = "SELECT * FROM current WHERE projection >= " + str(min_proj) 
    # select_statement = "SELECT * FROM current WHERE projection <= " + str(max_proj) 
    select_statement = "SELECT * FROM current WHERE projection <= " + str(max_proj + .01) 
   
    all_rosters = cur.execute(select_statement).fetchall()


    if len(all_rosters) > 1:
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('''
        CREATE TABLE current (
            
            "qb" TEXT,
            "rb1" TEXT,
            "rb2" TEXT,
            "wr1" TEXT,
            "wr2" TEXT,
            "wr3" TEXT,
            "te" TEXT,
            "fx" TEXT,
            "dst" TEXT,
            "budget" REAL,
            "projection" REAL
        )
        ''')

       
        insert_records = "INSERT INTO current (qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(insert_records, all_rosters)
        conn.commit()

        print(max_proj)

    return []






def implement_filter(state, min_bud, max_bud, min_proj, max_proj, incl_plyrs, excl_plyrs):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()

    select_statement = '''
    SELECT 
    qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection 
    FROM current
    WHERE budget >= '''  + str(min_bud) + ''' AND budget <= ''' + str(max_bud) + ''' AND projection >= ''' + str(min_proj) + ''' AND projection <= ''' + str(max_proj + .01) + ''' 
    '''

    if len(incl_plyrs) > 0:
        select_statement = select_statement + '''AND EXISTS (
            SELECT name FROM included_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''

    if len(excl_plyrs) > 0:
        select_statement = select_statement + '''AND NOT EXISTS (
            SELECT name FROM excluded_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''
    

    select_statement = "WITH t AS (" + select_statement + ") SELECT qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection FROM t"
   
    all_rosters = cur.execute(select_statement).fetchall()

    print(len(all_rosters))
    print(all_rosters[0])
    print(all_rosters[len(all_rosters)-1])
    
    if len(all_rosters) > 1:
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('''
        CREATE TABLE current (
            
            "qb" TEXT,
            "rb1" TEXT,
            "rb2" TEXT,
            "wr1" TEXT,
            "wr2" TEXT,
            "wr3" TEXT,
            "te" TEXT,
            "fx" TEXT,
            "dst" TEXT,
            "budget" REAL,
            "projection" REAL
        )
        ''')

       
        insert_records = "INSERT INTO current (qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.executemany(insert_records, all_rosters)
        conn.commit()
       
        if len(incl_plyrs) > 0:
            print("The following players have been included on all rosters:")
            for element in incl_plyrs:
                print(element[0])
            print("")

        if len(excl_plyrs) > 0:
            print("The following players have been excluded from all rosters:")
            for element in excl_plyrs:
                print(element[0])
            print("")

    else:
        if state == "exclude":
            excl_plyrs.pop()
        print("This restriction doesn't yield any rosters.  Try again.")
    
    if state == "include":
        return incl_plyrs
    elif state == "exclude":
        return excl_plyrs
    else:
        return None


def min_max_restriction(type, min, max):
    
    print("")
    print("Currently the " + type + " min is " + str(min))
    user_input = int(input("What would you like the new " + type + " min to be (must be greater than/equal to current)? "))
    if user_input > min and user_input <= max:
        min = user_input
    print("Currently the " + type + " max is " + str(max))
    user_input = int(input("What would you like the new " + type + " max to be (must be less than/equal to current)? "))
    if user_input < max and user_input >= min:
        max = user_input
    return [min, max]


def write_rosters_to_csv():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    newpath = r'output_files' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    cur.execute("SELECT * from current ORDER BY projection DESC")
    path = "output_files/Final_Roster.csv"

    with open(path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)

        
def clear_space():
     print("Cleaning out the empty space in the database...")


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
            clear_space()
        else:
            keep_running = False
            clear_space()

run_read()