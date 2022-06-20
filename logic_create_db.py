import sqlite3
from create_table import set_combos
from models import *
import csv
import time
from itertools import combinations
import os


def get_all_players():
    plyrs = []
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
                plyrs.append(player)
            line_count += 1    
    return plyrs


def get_all_projections(plyrs):
    with open('input_files/projections.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name = row[1]
                projection = row[2]
                for element in plyrs:
                    if element.name == name:
                        element.projection = float(projection)
                        break
                    
            line_count += 1
    
    return plyrs

def set_postions(position, plyrs):
    lcl_array = []
    for element in plyrs:
        if element.position == position:
            lcl_array.append(element)
    return lcl_array



def find_zero_projection(plyrs):
    print("")
    print("The following players are on the players.csv file but cannot be found on the projections.csv file")
    print("")
    for player in plyrs:
        if player.projection == 0:
            print(player.name)
    print("")
    print("Press 1 to continue and represent their projections as 0")
    print("Press 2 to quit this program and correct this issue")
    print("")
    return int(input("Enter Selection: "))




def set_flex_max_2(bgt, qbs, dst):
    flex_max = bgt - (min(qbs, key=lambda x: x.salary).salary + min
    (dst, key=lambda x: x.salary).salary)

    return flex_max

def set_qb_dst_combos(qbs, dst):
    qb_dst_combos = []
    for qb in qbs:
        for ds in dst:
            qb_dst_combos.append(QbDstCombo(qb, ds))
    
    return sorted(qb_dst_combos, key=lambda x: x.salary)    


def set_flex_max(bdgt, qb_dst):
    return bdgt - min(qb_dst, key=lambda x: x.salary).salary

def set_flex_combos(plyrs, num):
    
    return list(combinations(plyrs, num))

def sort_one(list):
    return  sorted(list, key=lambda x: x.salary)

def sort_two(list):
    return  sorted(list, key=lambda x: x[0].salary + x[1].salary)

def sort_three(list):
    return  sorted(list, key=lambda x: x[0].salary + x[1].salary + x[2].salary)

def sort_four(list):
    return  sorted(list, key=lambda x: x[0].salary + x[1].salary + x[2].salary + x[3].salary)




def max_combos(qb_dst, rb2, rb3, wr3, wr4, te, te2):
    print("Done calculating the necessary combinations needed to create all of the rosters")
    print("")
   
    value = len(qb_dst) * len(rb2) * len(wr3) * len(te2)
    value += len(qb_dst) * len(rb3) * len(wr3) * len(te)
    value += len(qb_dst) * len(rb2) * len(wr4) * len(te)

    print("Without factoring in salary, there are a potential " + str(value) + " rosters that could be created.")
    print("")
    print("Select 1 if you would like to continue")
    print("Select 2 to quit if this is too many combinations and you'd like to reduce the number of players")
    print("")
    return int(input("Enter Selection: "))

def create_all_flex_combos(two_rb_combos, three_wr_combos, two_te_combos, three_rb_combos, tight_ends, four_wr_combos, flex_max):
    flex_combos = []
   
    count = 0
    print("")
    print("Creating flex combinations...")
    print("")
    for rb in two_rb_combos:
        for wr in three_wr_combos:
            for te in two_te_combos:
                
                salary = rb[0].salary + rb[1].salary + wr[0].salary + wr[1].salary + wr[2].salary + te[0].salary + te[1].salary
                if salary <= flex_max:
                    if count >= 1000000 and count % 1000000 == 0:
                        print(str(count) + " two te flex combinations have been created.")
                    count += 1
                    flex_combos.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te[0], te[1]))
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
                    flex_combos.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te, rb[2]))
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
                    
                    flex_combos.append(FlexCombo(rb[0], rb[1], wr[0], wr[1], wr[2], te, wr[3]))  
                else:
                    break

    print(str(count) + " four wr flex combinations have been created.")
    count = 0

    print("Sorting " + str(len(flex_combos)) + " combinations.  This may take some time...")
    
    flex_combos = sorted(flex_combos, key=lambda x: x.salary)

    print("")
    print("Done Sorting")
   
    print("Generating valid rosters...")

    return flex_combos


def write_combos(qb_dst, flex):
    qb_dst_array = []
    flex_array = []
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS qb_dst')
    cur.execute('''
    CREATE TABLE qb_dst (
        "qb" TEXT,
        "dst" TEXT,
        "budget" REAL,
        "projection" REAL
    )
    ''')
    insert_records = "INSERT INTO qb_dst (qb, dst, budget, projection) VALUES(?, ?, ?, ?)"
    for element in qb_dst:
        qb_dst_array.append([element.qb.name, element.dst.name, element.salary, element.projection])
    cur.executemany(insert_records, qb_dst_array)
    conn.commit()

    cur.execute('DROP TABLE IF EXISTS flex')
    cur.execute('''
    CREATE TABLE flex (
        "rb1" TEXT,
        "rb2" TEXT,
        "wr1" TEXT,
        "wr2" TEXT,
        "wr3" TEXT,
        "te" TEXT,
        "fx" TEXT,
        "budget" REAL,
        "projection" REAL
    )
    ''')
    insert_records = "INSERT INTO flex (rb1, rb2, wr1, wr2, wr3, te, fx, budget, projection) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    for element in flex:
        flex_array.append([element.rb1.name, element.rb2.name, element.wr1.name, element.wr2.name, element.wr3.name, element.te.name, element.fx.name, element.salary, element.projection])
    cur.executemany(insert_records, flex_array)
    conn.commit()



def build_tables():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS rosters')
    cur.execute('''
        CREATE TABLE rosters AS 
            SELECT
                qb,
                rb1,
                rb2, 
                wr1, 
                wr2, 
                wr3, 
                te, 
                fx, 
                dst,
                qb_dst.budget + flex.budget AS budget,
                qb_dst.projection + flex.projection AS projection
            FROM flex 
            CROSS JOIN qb_dst
            WHERE qb_dst.budget + flex.budget <= 50000
            ''')
    print("All valid rosters have been written to the database.")


def write_to_database(qb_dst_combos, flex_combos):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    player_map = {}
    all_rosters = []
    count = 0
    for i in qb_dst_combos:
        for j in flex_combos:
            salary = i.salary + j.salary
            projection = round(i.projection + j.projection, 2)
            if salary > 50000:
                print(str(count) + " valid rosters have been generated so far")
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
                

                for element in roster:
                    if element not in player_map:
                        player_map[element] = 1
                    else:
                        player_map[element] += 1
                all_rosters.append(roster)
                if j == flex_combos[len(flex_combos)-1]:
                    print(str(count) + " valid rosters have been generated so far")
                    
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

    return [player_map, count]


def tally_players(player_map, roster_tally):

    
    players = {}
    projections = {}
    salary = {}
    
   
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
    print("")
    print("Finished creating CSV files showing a breakdown of the data")

def get_time(start, end):
    return str(round(end - start, 2))

def run_create():
    
    all_players = get_all_players()
    all_players = get_all_projections(all_players)
    if find_zero_projection(all_players) == 2:
        print("The program has terminated so that you may adjust the projections")
        return False
    wide_recievers = set_postions("WR", all_players)
    runningbacks = set_postions("RB", all_players)
    quarterbacks = set_postions("QB", all_players)
    tight_ends = set_postions("TE", all_players)
    defenses = set_postions("DST", all_players)
    qb_dst_combos = set_qb_dst_combos(quarterbacks, defenses)
    budget = 50000
    flex_max = set_flex_max(budget, qb_dst_combos)
    two_rb_combos = set_flex_combos(runningbacks, 2)
    three_rb_combos = set_flex_combos(runningbacks, 3)
    three_wr_combos = set_flex_combos(wide_recievers, 3)
    four_wr_combos = set_flex_combos(wide_recievers, 4)
    two_te_combos = set_flex_combos(tight_ends, 2)
    
    if max_combos(qb_dst_combos, two_rb_combos, three_rb_combos, three_wr_combos, four_wr_combos, tight_ends, two_te_combos) == 2:
        print("The program has ended so that you may reduce the number of players considered for a roster")
        return False
    start = time.time()
    print("Sorting positional combinations...")
    print("")
    two_rb_combos = sort_two(two_rb_combos)
    three_rb_combos = sort_three(three_rb_combos)
    three_wr_combos = sort_three(three_wr_combos)
    four_wr_combos = sort_four(four_wr_combos)
    two_te_combos = sort_two(two_te_combos)
    tight_ends = sort_one(tight_ends)
    print("Finished sorting positional combinations.")
    print("")
    flex_combo_end = time.time()
    runtime = get_time(start, flex_combo_end)
    print("The program has taken " + runtime + " seconds to sort all of the positional combinations")
    print("")
    print("Building the valid rosters...")
    print("")

    flex_combos = create_all_flex_combos(two_rb_combos, three_wr_combos, two_te_combos, three_rb_combos, tight_ends, four_wr_combos, flex_max)
    flex_combo_end = time.time()
    runtime = get_time(start, flex_combo_end)
    print("The program has taken " + runtime + " seconds to build all of the flex combinations")
    print("")
    print("Writing all of the combinations to a database.  This may take some time...")
    write_combos(qb_dst_combos, flex_combos)
    build_tables()
    end = time.time()
    print("")
    print("The program has taken " + get_time(start, end) + " seconds to complete")
    
    return True