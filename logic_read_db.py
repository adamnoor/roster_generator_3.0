import sqlite3
import csv
import os
from datetime import datetime

def initialize_current_table():
    
    newpath = r'output_files' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    
    print("")
    print("Initializing a local table.  This may take some time...")
    cur.execute('DROP TABLE IF EXISTS current')
    cur.execute('DROP TABLE IF EXISTS included_players')
    cur.execute("CREATE TABLE current AS SELECT * FROM all_rosters").fetchall()
    cur.execute('''
    CREATE TABLE included_players (
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
    return float(cur.execute(select_statement).fetchall()[0][0])

def get_count():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()

   
    select_statement = "SELECT COUNT(*) FROM current " 
    return float(cur.execute(select_statement).fetchall()[0][0])

def write_csv():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT * from current ORDER BY projection DESC")
    path = "output_files/Final_Roster.csv"

    with open(path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)


def run_read():
    initialize_current_table()
    current_players = get_current_players([])
    min_projection = get_min_max_value("MIN", "projection")
    max_projection = get_min_max_value("MAX", "projection")
    min_budget = get_min_max_value("MIN", "budget")
    max_budget = get_min_max_value("MAX", "budget")
    count = get_count()
    write_csv()


    print(min_projection)
    print(max_projection)
    print(min_budget)
    print(max_budget)
    print(count)
    print(current_players)


run_read()