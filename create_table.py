import sqlite3
from models import *
import csv
import time
from itertools import combinations
import os


#Global Variables

wide_recievers = []
runningbacks = []
quarterbacks = []
tight_ends = []
defenses = []
all_players = []
flex_max = 50000
two_rb_combos =[]
three_rb_combos = []
three_wr_combos = []
four_wr_combos = []
two_te_combos = []
qb_dst_combos_unsorted = []
qb_dst_combos = []
flex_combos_unsorted = []
flex_combos = []
roster_tally = 0
player_map = {}
overall_runtime = 0
current_roster = []
current_players = {}
included_players = []
excluded_players = []
conn = None
cur = None


#Functions

def read_csv_files():
    
    with open('input_files/players.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name = str.split(row[0], " (")[0]
                id = str.split(str.split(row[0], " (")[1], ")")[0]
                position = row[1]
                salary = int(row[2])
                player = Player(name, id, position, salary)
                all_players.append(player)
                
                if(position == "QB"):
                    quarterbacks.append(player)
                elif(position == "RB"):
                    runningbacks.append(player)
                elif(position == "WR"):
                    wide_recievers.append(player)
                elif(position == "TE"):
                    tight_ends.append(player)
                elif(position == "DST"):
                    defenses.append(player)
                else:
                    print("Something went wrong with " + row)
            line_count += 1
    
    with open('input_files/projections.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name = row[1]
                position = row[0]
                projection = row[2]
                if(position == "QB"):
                    for element in quarterbacks:
                        if element.name == name:
                            element.projection = float(projection)
                            break
                elif(position == "RB"):
                    for element in runningbacks:
                        if element.name == name:
                            element.projection = float(projection)
                            break
                elif(position == "WR"):
                    for element in wide_recievers:
                        if element.name == name:
                            element.projection = float(projection)
                            break
                elif(position == "TE"):
                    for element in tight_ends:
                        if element.name == name:
                            element.projection = float(projection)
                elif(position == "DST"):
                    for element in defenses:
                        if element.name == name:
                            element.projection = float(projection)
                else:
                    print("check the position for " + name)
                    
            line_count += 1


def check_for_zero_projection():
    print("")
    print("The following players are on the players.csv file but cannot be found on the projections.csv file")
    print("")
    for player in all_players:
        if player.projection == 0:
            print(player.name)
    print("")
    print("Press 1 to continue and represent their projections as 0")
    print("Press 2 to quit this program and correct this issue")
    print("")
    return int(input("Enter Selection: "))


def set_combos():
    
    global flex_max
    global two_rb_combos
    global three_rb_combos
    global three_wr_combos
    global four_wr_combos
    global two_te_combos
    global qb_dst_combos
    global qb_dst_combos_unsorted

    flex_max = 50000 - (min(quarterbacks, key=lambda x: x.salary).salary + min
    (defenses, key=lambda x: x.salary).salary)

    print("")
    print("Calculating the necessary combinations needed to create all of the rosters...")
    print("")

    for qb in quarterbacks:
        for dst in defenses:
            qb_dst_combos_unsorted.append(QbDstCombo(qb, dst))
    qb_dst_combos = sorted(qb_dst_combos_unsorted, key=lambda x: x.salary)
    two_rb_combos = list(combinations(runningbacks, 2))
    three_rb_combos = list(combinations(runningbacks, 3))
    three_wr_combos = list(combinations(wide_recievers, 3))
    four_wr_combos = list(combinations(wide_recievers, 4))
    two_te_combos = list(combinations(tight_ends, 2))

    print("Done calculating the necessary combinations needed to create all of the rosters")
    print("")
    print("For the players provided, the following combinations are possible: ")
    print("")
    print("qb/dst combinations: " + str(len(qb_dst_combos)))
    print("two rb combinations: " + str(len(two_rb_combos)))
    print("three rb combinations: " + str(len(three_rb_combos)))
    print("three wide receiver combinations: " + str(len(three_wr_combos)))
    print("four wide receiver combinations: " + str(len(four_wr_combos)))
    print("two tight end combinations: " + str(len(two_te_combos)))

    value = len(qb_dst_combos) * len(two_rb_combos) * len(three_wr_combos) * len(two_te_combos)
    value += len(qb_dst_combos) * len(three_rb_combos) * len(three_wr_combos) * len(tight_ends)
    value += len(qb_dst_combos) * len(two_rb_combos) * len(four_wr_combos) * len(tight_ends)

    print("")
    print("Without factoring in salary, there are a potential " + str(value) + " rosters that could be created.")
    print("")
    print("Select 1 if you would like to continue")
    print("Select 2 to quit if this is too many combinations and you'd like to reduce the number of players")
    print("")
    return int(input("Enter Selection: "))


def create_player_combos():

    global qb_dst_combos
    global flex_combos
    global overall_runtime
    global flex_combos_unsorted
    
    count = 0
    print("")
    print("Creating positional combinations...")
    print("")
    start = time.time()
    for rb in two_rb_combos:
        for wr in three_wr_combos:
            for te in two_te_combos:
                
                salary = rb[0].salary + rb[1].salary + wr[0].salary + wr[1].salary + wr[2].salary + te[0].salary + te[1].salary
                if salary <= flex_max:
                    if count >= 1000000 and count % 1000000 == 0:
                        print(str(count) + " two te flex combinations have been created.")
                    count += 1
                    flex_combos_unsorted.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te[0], te[1]))
                else:
                    break
    print(str(count) + " two te flex combinations have been created.")
    count = 0
    for rb in three_rb_combos:
        for wr in three_wr_combos:
            for te in tight_ends:    
                salary = rb[0].salary + rb[1].salary + wr[0].salary + wr[1].salary + wr[2].salary + te.salary + rb[2].salary
                if salary <= flex_max:
                    count += 1
                    if count >= 1000000 and count % 1000000 == 0:
                        print(str(count) + " three rb flex combinations have been created.")
                    flex_combos_unsorted.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te, rb[2]))
                else:
                    break
    print(str(count) + " three rb flex combinations have been created.")
    count = 0
    for rb in two_rb_combos:
        for wr in four_wr_combos:
            for te in tight_ends:
                
                salary = rb[0].salary + rb[1].salary + wr[0].salary + wr[1].salary + wr[2].salary + te.salary + wr[3].salary
                if salary <= flex_max:
                    count += 1
                    if count >= 1000000 and count % 1000000 == 0:
                        print(str(count) + " four wr flex combinations have been created.")
                    
                    flex_combos_unsorted.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te, wr[3]))  
                else:
                    break

    print(str(count) + " four wr flex combinations have been created.")
    count = 0

    print("Sorting " + str(len(flex_combos_unsorted)) + " combinations.  This may take some time...")
    
    flex_combos = sorted(flex_combos_unsorted, key=lambda x: x.salary)

    end = time.time()
    overall_runtime += end - start
    print("")
    print("Done Sorting")
    print(str(end - start) + " seconds to sort all of the combos")
    print("Generating valid rosters...")


def write_rosters():

    global conn
    global cur
    global roster_tally
    global overall_runtime

    newpath = r'generated_files' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS rosters')
    cur.execute('''
    CREATE TABLE rosters (
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

    count = 0
        
    print ("")
    print("Generating valid rosters for all rosters.  This may take some time...")
    all_rosters = []
    start = time.time()

    for i in qb_dst_combos:
        for j in flex_combos:
            salary = i.salary + j.salary
            projection = round(i.projection + j.projection, 2)
            if salary > 50000:
                print(str(count) + " valid rosters have been generated so far")
                end = time.time()
                print(str(end - start) + " seconds of running time...")
                print(str(len(all_rosters)) + " valid rosters with the qb of " + i.qb.name + " and a defense/special teams of " + i.dst.name + " have been created and are being written to the database")
                
                # SQL query to insert data into the
                # person table
                insert_records = "INSERT INTO rosters (qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                
                # Importing the contents of the file
                # into our person table
                cur.executemany(insert_records, all_rosters)
                conn.commit()
                
                all_rosters = []
                break
            else:
                count += 1
                
                roster = [i.qb.name, j.rb1.name, j.rb2.name, j.wr1.name, j.wr2.name, j.wr3.name, j.te.name, j.fx.name, i.dst.name, salary, projection]
                roster_tally += 1
                

                for element in roster:
                    if element not in player_map:
                        player_map[element] = 1
                    else:
                        player_map[element] += 1
                all_rosters.append(roster)
                if j == flex_combos[len(flex_combos)-1]:
                    print(str(count) + " valid rosters have been generated so far")
                    end = time.time()
                    print(str(end - start) + " seconds of running time...")
                    print(str(len(all_rosters)) + " valid rosters with the qb of " + i.qb.name + " and a defense/special teams of " + i.dst.name + " have been created and are being written to the database")
                    
                    # SQL query to insert data into the
                    # person table
                    insert_records = "INSERT INTO rosters (qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    
                    # Importing the contents of the file
                    # into our person table
                    cur.executemany(insert_records, all_rosters)
                    conn.commit()
                    
                    all_rosters = []
            
    print(str(count) + " valid rosters have been generated and written to the database")  
    print("")

 
    end = time.time()
    print(str(end - start) + " seconds to generate " + str(count) + " rosters")
    overall_runtime += end - start
    

def tally_players():

    global overall_runtime
    global roster_tally
    players = {}
    projections = {}
    salary = {}
    start = time.time()
   
    print("")
    print("Creating CSV files showing a breakdown of the data")
    
    for element in player_map:
        if isinstance(element, str):
            players[element] = player_map[element]
        elif isinstance(element, int):
            salary[element] = player_map[element]
        else:
            projections[element] = player_map[element]
    
    player_keys = sorted (players)
    salary_keys = sorted(salary)
    proj_keys = sorted(projections)
    player_data = []
    salary_data = []
    proj_data = []
    
    for element in player_keys:
        player_data.append([element, players[element], round(float(players[element])/float(roster_tally) * 100, 2)])
    
    for element in salary_keys:
        salary_data.append([element, salary[element], round(float(salary[element])/float(roster_tally) * 100, 4)])
    
    for element in proj_keys:
        proj_data.append([element, projections[element], round(float(projections[element])/float(roster_tally) * 100, 4)])
    
    player_data_sorted = sorted(player_data, key=lambda x: x[0])
    salary_data_sorted = sorted(salary_data, key=lambda x: x[2], reverse=True)
    proj_data_sorted = sorted(proj_data, key=lambda x: x[0], reverse=True)

    with open('generated_files/player_breakdown.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['Player', 'Number of Rosters', 'Percent of Rosters'])

        # write multiple rows
        writer.writerows(player_data_sorted)
    
    with open('generated_files/salary_breakdown.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['Salary', 'Number of Rosters', 'Percent of Rosters'])

        # write multiple rows
        writer.writerows(salary_data_sorted)
    with open('generated_files/projection_breakdown.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['Projections', 'Number of Rosters', 'Percent of Rosters'])

        # write multiple rows
        writer.writerows(proj_data_sorted)
    end = time.time()
    print("")
    print("Finished creating CSV files showing a breakdown of the data in " + str(end-start) + " seconds")
    overall_runtime += end - start
    print("")
    print("Overall Runtime  " + str(overall_runtime) + " seconds")


def run_create():
    read_csv_files()
    if check_for_zero_projection() == 1:
        if set_combos() == 1:
            create_player_combos()
            write_rosters()
            tally_players()
        else:
            print("the create rosters script has terminated")
    else:
        print("The create rosters script has terminated")

