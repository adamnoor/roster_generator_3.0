import sqlite3
import csv
import os
from datetime import datetime


#Global Variables

conn = None
cur = None
current_rosters = []
current_players_array = []
current_players_tally = {}
number_of_rosters = 0
included_players = []
excluded_players = []
min_projection = 0
max_projection = 1.0
min_budget = 0.0
max_budget = 50000


#Functions

def initialize_current_table():
    global current_players_array
    global current_rosters
    global number_of_rosters
    global included_players
    global excluded_players
    global min_projection
    global max_projection
    global min_budget
    global max_budget
    global cur
    global conn

    newpath = r'output_files' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    current_rosters = []
    current_players_array = []
    number_of_rosters = 0
    included_players = []
    excluded_players = []
    min_projection = 0
    max_projection = 1.0
    min_budget = 0.0
    max_budget = 50000
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    
    print("")
    print("Initializing a local table.  This may take some time...")
    cur.execute('DROP TABLE IF EXISTS current')
    cur.execute('DROP TABLE IF EXISTS included_players')
    cur.execute("CREATE TABLE current AS SELECT * FROM rosters").fetchall()
    cur.execute('''
    CREATE TABLE included_players (
        "id" INTEGER PRIMARY KEY,
        "name" TEXT
    )
    ''')
    
    current_players_array = []

    get_player()


def set_up_values():
    global min_projection
    global max_projection
    global min_budget
    global max_budget
    global number_of_rosters
   
    
    select_statement = "SELECT MIN(projection) FROM current " 
    min_projection = float(cur.execute(select_statement).fetchall()[0][0])
    select_statement = "SELECT MAX(projection) FROM current " 
    max_projection = float(cur.execute(select_statement).fetchall()[0][0])
    select_statement = "SELECT MIN(budget) FROM current "
    min_budget = int(cur.execute(select_statement).fetchall()[0][0])
    select_statement = "SELECT MAX(budget) FROM current " 
    max_budget = int(cur.execute(select_statement).fetchall()[0][0])
    select_statement = "SELECT count(*) FROM current " 
    number_of_rosters = int(cur.execute(select_statement).fetchall()[0][0])



def restrict_players():
    set_up_values()
    print("")
    print("There are " + str(number_of_rosters) + " rosters")
    print("The highest projection score is " + str(max_projection))
    print("The lowhest projection score is " + str(min_projection))
    print("The highest budget is " + str(max_budget))
    print("The lowest budget is " + str(min_budget))
    print("")
    print("How would you like to restrict the rosters?")
    print("")
    print("Select 0 to restrict the rosters by selecting a player to always include")
    print("Select 1 to restrict the rosters by selecting a player to always exclude")
    print("Select 2 to restrict the rosters by selecting a min and max for projections")
    print("Select 3 to restrict the rosters by selecting a min and max for budgets")
    print("Select 4 to write a CSV file containing " + str(number_of_rosters) + " rosters and build a new stack")
    print("Select 5 to write a CSV file containing " + str(number_of_rosters) + " and quit the program")
    print("Select 6 to quit the program without writing a CSV file of the current " + str(number_of_rosters) + " rosters")
    print("")
    return (int(input("Select an option: ")))
   

def get_player():
    global current_players_array
    players = []
    qb = conn.execute("SELECT DISTINCT qb FROM current").fetchall()
    rb1 = conn.execute("SELECT DISTINCT rb1 FROM current").fetchall()
    rb2 = conn.execute("SELECT DISTINCT rb2 FROM current").fetchall()
    wr1 = conn.execute("SELECT DISTINCT wr1 FROM current").fetchall()
    wr2 = conn.execute("SELECT DISTINCT wr2 FROM current").fetchall()
    wr3 = conn.execute("SELECT DISTINCT wr2 FROM current").fetchall()
    te = conn.execute("SELECT DISTINCT te FROM current").fetchall()
    fx = conn.execute("SELECT DISTINCT fx FROM current").fetchall()
    dst = conn.execute("SELECT DISTINCT dst FROM current").fetchall()

    for element in qb:
        if element not in players:
            players.append(element[0])
    
    for element in rb1:
        if element not in players:
            players.append(element[0])
    
    for element in rb2:
        if element not in players:
            players.append(element[0])
    
    for element in wr1:
        if element not in players:
            players.append(element[0])
    
    for element in wr2:
        if element not in players:
            players.append(element[0])
    
    for element in wr3:
        if element not in players:
            players.append(element[0])
    
    for element in te:
        if element not in players:
            players.append(element[0])
    
    for element in fx:
        if element not in players:
            players.append(element[0])
    
    for element in dst:
        if element not in players:
            players.append(element[0])
    
    res = []
    [res.append(x) for x in players if x not in res]  
    
    if len(res)>0:
        current_players_array = res


def get_selected_player(state):
    global current_players_array
    
    temp = current_players_array

    current_players_array = []
    get_player()

    for i, element in enumerate(current_players_array):
        #lcl_array.append(element)
        print("Select " + str(i) + " to " + state + " " + element)
    
    
    if len(current_players_array) > 0:
        
        print("")
        user_input = int(input("Make a selection: "))
        if user_input < 0 or user_input >= len(current_players_array):
            get_selected_player(state)
        else:
            return current_players_array[user_input]
    else:
        current_players_array = temp
    

def include_player_restriction():
    print("Getting a list of players to include...")
    plyr = get_selected_player("include")
    included_players.append([plyr])
    cur.execute('DROP TABLE IF EXISTS included_players')
    cur.execute('''
    CREATE TABLE included_players (
        "id" INTEGER PRIMARY KEY,
        "name" TEXT
    )
    ''')

    insert_records = "INSERT INTO included_players (name) VALUES(?)"
    
    cur.executemany(insert_records, [[plyr]])
    conn.commit()
    print("you are trying to include " + str(included_players[len(included_players)-1][0]))

    implement_filter('include')
    user_choice()


def exclude_player_restriction():
    print("Getting a list of players to exclude...")
    plyr = get_selected_player("exclude")
    excluded_players.append([plyr])

    cur.execute('DROP TABLE IF EXISTS excluded_players')
    cur.execute('''
    CREATE TABLE excluded_players (
        "id" INTEGER PRIMARY KEY,
        "name" TEXT
    )
    ''')

    insert_records = "INSERT INTO excluded_players (name) VALUES(?)"
    
    cur.executemany(insert_records, excluded_players)
    conn.commit()
    print("you are trying to exclude " + str(excluded_players[len(excluded_players)-1][0]))

    implement_filter('exclude')
    user_choice()


def projection_restriction():
    global min_projection
    global max_projection
    print("")
    print("Currently the projection min is " + str(min_projection))
    user_input = float(input("What would you like the new projection min to be (must be greater than/equal to current)? "))
    if user_input > min_projection and user_input <= max_projection:
        min_projection = user_input
    print("Currently the projection max is " + str(max_projection))
    user_input = float(input("What would you like the new projection max to be (must be less than/equal to current)? "))
    if user_input < max_projection and user_input >= min_projection:
        max_projection = user_input
    
    implement_filter("projection")
    user_choice()


def budget_restriction():
    global min_budget
    global max_budget
    print("")
    print("Currently the budget min is " + str(min_budget))
    user_input = int(input("What would you like the new budget min to be (must be greater than/equal to current)? "))
    if user_input > min_budget and user_input <= max_budget:
        min_budget = user_input
    print("Currently the budget max is " + str(max_budget))
    user_input = int(input("What would you like the new budget max to be (must be less than/equal to current)? "))
    if user_input < max_budget and user_input >= min_budget:
        max_budget = user_input
    
    implement_filter("budget")
    user_choice()


def implement_filter(state):
    global min_budget
    global max_budget
    global min_projection
    global max_projection
    global included_players
    global excluded_players

    select_statement = '''
    SELECT 
    id, qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection 
    FROM current
    WHERE budget >= '''  + str(min_budget) + ''' AND budget <= ''' + str(max_budget) + ''' AND projection >= ''' + str(min_projection) + ''' AND projection <= ''' + str(max_projection) + ''' 
    '''

    if len(included_players) > 0:
        select_statement = select_statement + '''AND EXISTS (
            SELECT name FROM included_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''

    if len(excluded_players) > 0:
        select_statement = select_statement + '''AND NOT EXISTS (
            SELECT name FROM excluded_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''
    
    select_statement = "WITH t AS (" + select_statement + ") SELECT qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection FROM t"
   
    all_rosters = cur.execute(select_statement).fetchall()
    
    if len(all_rosters) > 0:
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('''
        CREATE TABLE current (
            "id" INTEGER PRIMARY KEY,
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
       
        if len(included_players) > 0:
            print("The following players have been included on all rosters:")
            for element in included_players:
                print(element[0])
            print("")

        if len(excluded_players) > 0:
            print("The following players have been excluded from all rosters:")
            for element in excluded_players:
                print(element[0])
            print("")

    else:
        if state == "exclude":
            excluded_players.pop()
        print("This restriction doesn't yield any rosters.")

    

def write_stack():
    now = str(datetime.now())
    cursor = conn.cursor()
    cursor.execute("SELECT * from current ORDER BY projection DESC")
    path = "output_files/Final_Roster_" + str(now) + ".csv"

    with open(path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/" + path
    print ("Data exported Successfully into {}".format(dirpath))


def user_choice():
    user_input = restrict_players()
    if user_input == 0:
        include_player_restriction()
    elif user_input == 1:
        exclude_player_restriction()
    elif user_input == 2:
        projection_restriction()
    elif user_input == 3:
        budget_restriction()
    elif user_input == 4:
        write_stack()
        print("The stack has been written")
        run_script()
    elif user_input == 5:
        write_stack()
        print("The stack has been written")
        print("")
        print("Cleaning out the empty space in the database...")
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('VACUUM')
        print("The program has been ternminated")
    else:
        print("Cleaning out the empty space in the database...")
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('VACUUM')
       
        print("The program has terminated")


def run_script():
    initialize_current_table()
    set_up_values()
    user_choice()
