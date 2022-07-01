from tkinter import *
import time
from functions import *


root = Tk()
root.title('Stack Generator')
root.geometry("1000x1000")
is_player_var = StringVar()
output_line1_var = StringVar()
output_line2_var = StringVar()
output_line3_var = StringVar()
output_line4_var = StringVar()
budget_max_entry = Entry(root, width=25)
budget_min_entry = Entry(root, width=25)
projection_max_entry = Entry(root, width=25)
projection_min_entry = Entry(root, width=25)
max_unspent_entry = Entry(root, width=25)
include_players_entry = Entry(root, width=25)
exclude_players_entry = Entry(root, width=25)
output_line1_var.set(output_opening(check_current_table()))
output_line2_var.set("")
output_line3_var.set(find_zero_projection_new())
output_line4_var.set(output_players(check_current_table()))




def build_new_rosters():

    obj = run_create_new()
    output_line2_var.set(obj[0])
    output_line3_var.set(obj[1])
    output_line4_var.set(output_players(check_current_table()))
    output_line1_var.set(output_opening(check_current_table()))



def build_new_stack():
    if check_current_table():
        output_line2_var.set(build_stack())

    output_line4_var.set(output_players(check_current_table()))
    output_line1_var.set(output_opening(check_current_table()))


def update_current_table():
    output_line4_var.set(get_all_players_new())


def monday_morning():
    output_line2_var.set("Applying the results")



def build_stack():
    budget_min = 0
    budget_max = 50000
    projection_min = 0.0
    projection_max = 50000.0
    included_player_numbers = []
    excluded_player_numbers = []
    if budget_min_entry.get():
        budget_min = int(budget_min_entry.get())

    if budget_max_entry.get():
        budget_max = int(budget_max_entry.get())

    if projection_min_entry.get():
        projection_min = float(projection_min_entry.get())

    if projection_max_entry.get():
        projection_max = float(projection_max_entry.get())

    if include_players_entry.get():
        included_player_numbers = include_players_entry.get().split(", ")

    if exclude_players_entry.get():
        excluded_player_numbers = exclude_players_entry.get().split(", ")
    print(excluded_player_numbers)
    print(included_player_numbers)
    all_players = get_players_new()
    excluded_players = get_player_array(excluded_player_numbers, all_players)
    print(excluded_players)
    included_players = get_player_array(included_player_numbers, all_players)
    print(included_players)
    print_rosters = True

    # add_to_table("exclude", excluded_players)

    # print("")
    print("Filtering all of the non player parameters...")
    print_rosters = filter_array([], [], budget_max, budget_min, projection_max, projection_min)
    if len(excluded_players) > 0:
        print("Filtering all of the excluded players... ")
    for element in excluded_players:
        if print_rosters:
            temp = [element]
            add_to_table("exclude", temp)
            print_rosters = filter_array([], temp, budget_max, budget_min, projection_max, projection_min)

        else:
            break
    if len(included_players) > 0:
        print("Filtering all of the included players... ")
    for element in included_players:
        if print_rosters:
            temp = [element]
            add_to_table("include", temp)
            print_rosters = filter_array(temp, [], budget_max, budget_min, projection_max, projection_min)
        else:
            get_all_players_new()
            break

    if print_rosters:
        count = get_count()
        print("This combination yielded " + str(count) + " rosters")
        write_rosters_to_csv()
        return "This stack has " + str(count) + " valid rosters located in the outputs folder"
    else:
        return "This combinations did not yield any valid rosters, please try again"


def filter_array(incl_plyrs, excl_plyrs, budget_max, budget_min, projection_max, projection_min):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()

    select_statement = '''

    SELECT 
    qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection 
    FROM current
    WHERE budget <= ''' + str(budget_max) + ''' AND budget >= ''' + str(budget_min) + ''' AND projection <= ''' + str(projection_max) + ''' AND projection >= ''' + str(projection_min) + '''  
    '''

    if len(incl_plyrs) > 0:
        select_statement = select_statement + ''' AND EXISTS (
            SELECT name FROM included_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''

    if len(excl_plyrs) > 0:
        select_statement = select_statement + ''' AND NOT EXISTS (
            SELECT name FROM excluded_players WHERE name = QB OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''

    select_statement = "WITH t AS (" + select_statement + ") SELECT qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection FROM t"

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

        return True

    else:

        print("This restriction doesn't yield any rosters.  Try again.")
        return False


def get_player_array(user_input, plyr_list):

    players = []
    for element in user_input:
        if plyr_list[int(element)] not in players:
            players.append([plyr_list[int(element)]])
            print(plyr_list[int(element)])

    return players




create_rosters_button = Button(root, text="Create Rosters", command=build_new_rosters, padx=40, pady=20)
update_rosters_label = Label(root, text="Press button to create all possible rosters", padx=10, pady=10)
max_budget_label = Label(root, text="Maximum Budget:", padx=10, pady=10)
min_budget_label = Label(root, text="Minimum Budget:", padx=10, pady=10)
max_projection_label = Label(root, text="Maximum Projection:", padx=10, pady=10)
min_projection_label = Label(root, text="Minimum Projection:", padx=10, pady=10)
include_players_label = Label(root, text="Players that must be included:\n")
exclude_players_label = Label(root, text="Players that must be excluded:\n")
monday_morning_label = Label(root, text="Press button to apply results")
monday_morning_button = Button(root, text="Get Current Players", command=monday_morning, padx=40, pady=20)
filter_players_label = Label(root, text="Press button to build a stack")
filter_players_button = Button(root, text="Build Stacks", command=build_new_stack, padx=40, pady=20)
output_line1_label = Label(root, textvariable=output_line1_var, padx=10, pady=20)
output_line2_label = Label(root, textvariable=output_line2_var, padx=10, pady=20)
output_line3_label = Label(root, textvariable=output_line3_var, padx=10, pady=20)
output_line4_label = Label(root, textvariable=output_line4_var, padx=10, pady=20)
output_line1_label.grid(row=0, column=0)
update_rosters_label.grid(row=1, column=0)
create_rosters_button.grid(row=2, column=0)
filter_players_label.grid(row=3, column=0)
filter_players_button.grid(row=4, column=0)
monday_morning_label.grid(row=5, column=0)
monday_morning_button.grid(row=6, column=0)
include_players_label.grid(row=0, column=1)
include_players_entry.grid(row=1, column=1)
exclude_players_label.grid(row=2, column=1)
exclude_players_entry.grid(row=3, column=1)
max_budget_label.grid(row=4, column=1)
budget_max_entry.grid(row=5, column=1)
min_budget_label.grid(row=6, column=1)
budget_min_entry.grid(row=7, column=1)
max_projection_label.grid(row=8, column=1)
projection_max_entry.grid(row=9, column=1)
min_projection_label.grid(row=10, column=1)
projection_min_entry.grid(row=11, column=1)


output_line2_label.grid(row=17, column=1)
output_line3_label.grid(row=18, column=1)
output_line4_label.grid(row=19, column=1)

mainloop()
